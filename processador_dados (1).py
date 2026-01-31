#!/usr/bin/env python3
"""
Processador de Dados - Telegram
Descrição: Formata os dados extraídos para envio no Telegram
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ProcessadorDados:
    """Classe para processar e formatar dados dos pedidos para Telegram"""
    
    def formatar_resultados(self, pedidos, termo_busca):
        """
        Formata os resultados da busca para envio no Telegram
        
        Args:
            pedidos (list): Lista de pedidos
            termo_busca (str): Termo que foi buscado
        
        Returns:
            str: Mensagem formatada com emojis (Markdown)
        """
        if not pedidos:
            return f"❌ *Nenhum pedido encontrado para:* `{termo_busca}`"
        
        # Cabeçalho
        mensagem = f"🔍 *RESULTADOS: {termo_busca.upper()}*\n"
        mensagem += f"📊 Total: *{len(pedidos)} pedido{'s' if len(pedidos) > 1 else ''}*\n"
        mensagem += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        # Calcula totais
        total_valor = 0
        total_itens = 0
        
        # Lista cada pedido
        for i, pedido in enumerate(pedidos, 1):
            mensagem += f"📦 *PEDIDO #{pedido['numero']}*\n"
            mensagem += f"📅 Data: `{pedido['data_venda']}`\n"
            
            if pedido.get('industria'):
                mensagem += f"🏭 Indústria: {pedido['industria']}\n"
            
            mensagem += f"🏢 Cliente: {pedido['razao_social']}\n"
            mensagem += f"📍 Cidade: {pedido['cidade']}\n"
            mensagem += f"💰 Valor: *{pedido['valor']}*\n"
            mensagem += f"📦 Itens: {pedido['itens']}\n"
            
            # Soma valores
            try:
                valor_limpo = pedido['valor'].replace('R$', '').replace('.', '').replace(',', '.').strip()
                total_valor += float(valor_limpo)
            except:
                pass
            
            try:
                itens_limpo = pedido['itens'].replace(',', '.').strip()
                total_itens += float(itens_limpo)
            except:
                pass
            
            # Separador
            if i < len(pedidos):
                mensagem += "\n" + "─" * 30 + "\n\n"
        
        # Rodapé com totais
        mensagem += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        mensagem += "📊 *RESUMO GERAL*\n"
        mensagem += f"💰 Valor Total: *R$ {total_valor:,.2f}*\n"
        mensagem += f"📦 Total Itens: *{total_itens:.0f}*\n"
        mensagem += f"🕐 {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        
        return mensagem
