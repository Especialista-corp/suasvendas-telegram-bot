#!/usr/bin/env python3
"""
Bot Telegram - SuasVendas Automação
Autor: Claude AI para Jackson
Descrição: Bot Telegram que consulta pedidos no SuasVendas
"""

import os
import logging
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from automacao_suasvendas import AutomacaoSuasVendas
from processador_dados import ProcessadorDados

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token do bot (você vai pegar com o @BotFather)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Instâncias globais
automacao = None
processador = ProcessadorDados()

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
    """Comando /start - Apresentação do bot"""
    mensagem = """
🤖 *BOT SUASVENDAS - BEM-VINDO!*

Olá! Sou seu assistente para consultar pedidos no SuasVendas.

📝 *Como usar:*
Digite o nome do cliente ou cidade para buscar pedidos.

*Exemplos:*
• `americana casa bonita`
• `Americana`
• `KORA MOBILIARIO`

⚙️ *Comandos disponíveis:*
/start - Mostra esta mensagem
/ajuda - Instruções detalhadas
/status - Verifica se estou online
/teste - Faz uma busca de teste

💡 *Dica:*
Retorno os últimos 10 pedidos encontrados!

🕐 Funciono 24 horas por dia, 7 dias por semana!

🚀 Comece digitando o nome do cliente!
    """
    
    await update.message.reply_text(mensagem, parse_mode='Markdown')

async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /ajuda - Instruções detalhadas"""
    mensagem = """
📖 *GUIA COMPLETO - BOT SUASVENDAS*

🔍 *BUSCAR PEDIDOS:*
Digite o nome do cliente ou cidade (sem comando)

*Exemplos:*
• `americana casa bonita`
• `Americana`
• `KORA MOBILIARIO`
• `C.C.L - Moveis`

📊 *O QUE RECEBO:*
Para cada pedido encontrado:
• 📦 Número do Pedido
• 📅 Data da Venda
• 🏭 Indústria
• 🏢 Razão Social (Cliente completo)
• 📍 Cidade
• 💰 Valor
• 📦 Quantidade de Itens

*BÔNUS:* Cálculo automático do total!

⚙️ *COMANDOS:*
/start - Mensagem de boas-vindas
/ajuda - Este guia
/status - Verifica se estou online
/teste - Busca de teste

❓ *DÚVIDAS?*
Digite qualquer nome de cliente para começar!
    """
    
    await update.message.reply_text(mensagem, parse_mode='Markdown')

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /status - Verifica status do bot"""
    if automacao and automacao.is_ready():
        mensagem = "✅ *Bot Online e Funcionando!*\n\n🤖 Sistema operacional\n🔗 Conectado ao SuasVendas\n✨ Pronto para buscar pedidos!"
    else:
        mensagem = "⚠️ *Bot Iniciando...*\n\n⏳ Aguarde alguns segundos e tente novamente."
    
    await update.message.reply_text(mensagem, parse_mode='Markdown')

async def teste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /teste - Faz busca de teste"""
    await update.message.reply_text("🧪 *Teste em andamento...*\n\n🔍 Buscando: 'americana casa bonita'", parse_mode='Markdown')
    await buscar_pedidos(update, context, "americana casa bonita")

async def buscar_pedidos(update: Update, context: ContextTypes.DEFAULT_TYPE, termo_override=None):
    """Busca pedidos no SuasVendas"""
    try:
        # Pega o termo de busca
        termo_busca = termo_override or update.message.text.strip()
        
        # Ignora se for comando
        if termo_busca.startswith('/'):
            return
        
        logger.info(f"🔍 Busca recebida de {update.effective_user.username}: {termo_busca}")
        
        # Verifica se automação está pronta
        if not automacao:
            logger.warning("⚠️ Automação não inicializada, tentando inicializar...")
            await update.message.reply_text("⏳ *Iniciando sistema...*\n\nAguarde alguns segundos...", parse_mode='Markdown')
            
            if not inicializar_automacao():
                await update.message.reply_text(
                    "❌ *Erro ao inicializar*\n\nTente novamente em alguns segundos.",
                    parse_mode='Markdown'
                )
                return
        
        # Mensagem de aguardo
        msg_aguardo = await update.message.reply_text(
            f"🔍 *Buscando pedidos...*\n\nTermo: `{termo_busca}`\n⏳ Aguarde alguns segundos...",
            parse_mode='Markdown'
        )
        
        # Executa a busca
        resultados = automacao.buscar_pedidos(termo_busca, limite=10)
        
        if not resultados:
            await msg_aguardo.edit_text(
                f"❌ *Nenhum pedido encontrado*\n\n"
                f"Termo buscado: `{termo_busca}`\n\n"
                f"💡 *Dicas:*\n"
                f"• Verifique a ortografia\n"
                f"• Tente buscar por cidade\n"
                f"• Use termos mais genéricos",
                parse_mode='Markdown'
            )
            return
        
        # Formata a resposta
        resposta = processador.formatar_resultados(resultados, termo_busca)
        
        # Telegram tem limite de 4096 caracteres por mensagem
        # Se resposta for muito grande, divide
        if len(resposta) > 4000:
            # Divide em partes
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
            
            # Envia primeira parte (editando mensagem de aguardo)
            await msg_aguardo.edit_text(partes[0], parse_mode='Markdown')
            
            # Envia demais partes
            for parte in partes[1:]:
                await update.message.reply_text(parte, parse_mode='Markdown')
        else:
            # Resposta cabe em uma mensagem
            await msg_aguardo.edit_text(resposta, parse_mode='Markdown')
        
        logger.info(f"✅ Busca concluída: {len(resultados)} resultados para '{termo_busca}'")
        
    except Exception as e:
        logger.error(f"❌ Erro na busca: {e}")
        import traceback
        traceback.print_exc()
        
        await update.message.reply_text(
            f"❌ *Erro ao buscar pedidos*\n\n"
            f"🔧 Tente novamente em alguns segundos.\n\n"
            f"Se o erro persistir, use /status para verificar o sistema.",
            parse_mode='Markdown'
        )

async def mensagem_desconhecida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Trata qualquer mensagem que não seja comando"""
    await buscar_pedidos(update, context)

def main():
    """Função principal - inicia o bot"""
    logger.info("=" * 70)
    logger.info("🚀 INICIANDO BOT TELEGRAM SUASVENDAS")
    logger.info("=" * 70)
    
    # Verifica token
    if not TELEGRAM_TOKEN:
        logger.error("❌ TELEGRAM_TOKEN não configurado!")
        logger.error("Configure a variável de ambiente TELEGRAM_TOKEN")
        return
    
    # Inicializa a automação
    logger.info("⏳ Inicializando automação do SuasVendas...")
    if inicializar_automacao():
        logger.info("✅ Automação inicializada com sucesso!")
    else:
        logger.warning("⚠️ Falha na inicialização da automação")
        logger.warning("Bot vai tentar inicializar na primeira busca")
    
    # Cria aplicação
    logger.info("🤖 Criando aplicação Telegram...")
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Adiciona handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ajuda", ajuda))
    application.add_handler(CommandHandler("help", ajuda))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("teste", teste))
    
    # Handler para mensagens de texto (buscas)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensagem_desconhecida))
    
    # Inicia o bot
    logger.info("✅ Bot Telegram inicializado!")
    logger.info("🎉 Sistema pronto para receber comandos!")
    logger.info("=" * 70)
    
    # Roda o bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
