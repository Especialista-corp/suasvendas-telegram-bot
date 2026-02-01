#!/usr/bin/env python3
"""
Bot Telegram - SuasVendas Automação (com HTTP server para Render)
"""

import os
import logging
import json
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from automacao_suasvendas import AutomacaoSuasVendas
from processador_dados import ProcessadorDados

# HTTP Server para Render
from http.server import HTTPServer, BaseHTTPRequestHandler

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token do bot
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
PORT = int(os.getenv('PORT', 10000))

# Instâncias globais
automacao = None
processador = ProcessadorDados()

# Servidor HTTP simples para o Render não reclamar
class SimpleHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        status = {
            'status': 'online',
            'bot': 'SuasVendas Telegram Bot',
            'ready': automacao is not None and automacao.is_ready() if automacao else False
        }
        self.wfile.write(json.dumps(status).encode())
    
    def log_message(self, format, *args):
        pass  # Silencia logs HTTP

def inicializar_automacao():
    """Inicializa a automação do SuasVendas"""
    global automacao
    try:
        logger.info("🔧 Inicializando automação SuasVendas...")
        automacao = AutomacaoSuasVendas()
        logger.info("✅ Automação inicializada!")
        return True
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar: {e}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    mensagem = """
🤖 *BOT SUASVENDAS - BEM-VINDO!*

Olá! Sou seu assistente para consultar pedidos no SuasVendas.

📝 *Como usar:*
Digite o nome do cliente ou cidade para buscar pedidos.

*Exemplos:*
• `americana casa bonita`
• `Americana`
• `KORA MOBILIARIO`

⚙️ *Comandos:*
/start - Mostra esta mensagem
/ajuda - Instruções detalhadas
/status - Verifica se estou online
/teste - Busca de teste

💡 Retorno os últimos 10 pedidos encontrados!
🕐 Funciono 24 horas por dia!

🚀 Comece digitando o nome do cliente!
    """
    await update.message.reply_text(mensagem, parse_mode='Markdown')

async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /ajuda"""
    mensagem = """
📖 *GUIA COMPLETO - BOT SUASVENDAS*

🔍 *BUSCAR PEDIDOS:*
Digite o nome do cliente ou cidade

*Exemplos:*
• `americana casa bonita`
• `Americana`
• `KORA MOBILIARIO`

📊 *O QUE RECEBO:*
• 📦 Número do Pedido
• 📅 Data da Venda
• 🏭 Indústria
• 🏢 Cliente completo
• 📍 Cidade
• 💰 Valor
• 📦 Itens

*BÔNUS:* Totais calculados!

⚙️ *COMANDOS:*
/start - Boas-vindas
/ajuda - Este guia
/status - Status do bot
/teste - Busca teste
    """
    await update.message.reply_text(mensagem, parse_mode='Markdown')

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /status"""
    if automacao and automacao.is_ready():
        mensagem = "✅ *Bot Online e Funcionando!*\n\n🤖 Sistema operacional\n🔗 Conectado ao SuasVendas\n✨ Pronto para buscar pedidos!"
    else:
        mensagem = "⚠️ *Bot Iniciando...*\n\n⏳ Aguarde alguns segundos."
    await update.message.reply_text(mensagem, parse_mode='Markdown')

async def teste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /teste"""
    await update.message.reply_text("🧪 *Teste em andamento...*\n\n🔍 Buscando: 'americana casa bonita'", parse_mode='Markdown')
    await buscar_pedidos(update, context, "americana casa bonita")

async def buscar_pedidos(update: Update, context: ContextTypes.DEFAULT_TYPE, termo_override=None):
    """Busca pedidos no SuasVendas"""
    try:
        termo_busca = termo_override or update.message.text.strip()
        
        if termo_busca.startswith('/'):
            return
        
        logger.info(f"🔍 Busca recebida de {update.effective_user.username}: {termo_busca}")
        
        if not automacao:
            logger.warning("⚠️ Automação não inicializada, tentando inicializar...")
            await update.message.reply_text("⏳ *Iniciando sistema...*\n\nAguarde...", parse_mode='Markdown')
            
            if not inicializar_automacao():
                await update.message.reply_text(
                    "❌ *Erro ao inicializar*\n\nTente novamente em alguns segundos.",
                    parse_mode='Markdown'
                )
                return
        
        msg_aguardo = await update.message.reply_text(
            f"🔍 *Buscando pedidos...*\n\nTermo: `{termo_busca}`\n⏳ Aguarde...",
            parse_mode='Markdown'
        )
        
        resultados = automacao.buscar_pedidos(termo_busca, limite=10)
        
        if not resultados:
            await msg_aguardo.edit_text(
                f"❌ *Nenhum pedido encontrado*\n\n"
                f"Termo: `{termo_busca}`\n\n"
                f"💡 *Dicas:*\n"
                f"• Verifique ortografia\n"
                f"• Tente buscar por cidade\n"
                f"• Use termos mais genéricos",
                parse_mode='Markdown'
            )
            return
        
        resposta = processador.formatar_resultados(resultados, termo_busca)
        
        if len(resposta) > 4000:
            partes = []
            linhas = resposta.split('\n')
            parte_atual = ""
            
            for linha in linhas:
                if len(parte_atual) + len(linha) + 1 < 4000:
                    parte_atual += linha + "\n"
                else:
                    partes.append(parte_atual)
                    parte_atual = linha + "\n"
            
            if parte_atual:
                partes.append(parte_atual)
            
            await msg_aguardo.edit_text(partes[0], parse_mode='Markdown')
            for parte in partes[1:]:
                await update.message.reply_text(parte, parse_mode='Markdown')
        else:
            await msg_aguardo.edit_text(resposta, parse_mode='Markdown')
        
        logger.info(f"✅ Busca concluída: {len(resultados)} resultados")
        
    except Exception as e:
        logger.error(f"❌ Erro na busca: {e}")
        import traceback
        traceback.print_exc()
        await update.message.reply_text(
            f"❌ *Erro ao buscar*\n\nTente novamente.",
            parse_mode='Markdown'
        )

async def mensagem_desconhecida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Trata mensagens"""
    await buscar_pedidos(update, context)

def iniciar_http_server():
    """Inicia servidor HTTP em thread separada para o Render"""
    logger.info(f"🌐 Iniciando HTTP server na porta {PORT}...")
    server = HTTPServer(('0.0.0.0', PORT), SimpleHTTPHandler)
    logger.info(f"✅ HTTP server rodando na porta {PORT}")
    server.serve_forever()

def main():
    """Função principal"""
    logger.info("=" * 70)
    logger.info("🚀 INICIANDO BOT TELEGRAM SUASVENDAS")
    logger.info("=" * 70)
    
    if not TELEGRAM_TOKEN:
        logger.error("❌ TELEGRAM_TOKEN não configurado!")
        return
    
    # Inicia HTTP server em thread separada
    http_thread = Thread(target=iniciar_http_server, daemon=True)
    http_thread.start()
    
    # Inicializa automação
    logger.info("⏳ Inicializando automação...")
    if inicializar_automacao():
        logger.info("✅ Automação inicializada!")
    else:
        logger.warning("⚠️ Automação será inicializada na primeira busca")
    
    # Cria aplicação Telegram
    logger.info("🤖 Criando aplicação Telegram...")
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ajuda", ajuda))
    application.add_handler(CommandHandler("help", ajuda))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("teste", teste))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensagem_desconhecida))
    
    logger.info("✅ Bot inicializado!")
    logger.info("🎉 Sistema pronto!")
    logger.info("=" * 70)
    
    # Roda o bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
