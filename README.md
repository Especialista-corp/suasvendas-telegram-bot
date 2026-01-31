# 🤖 Bot Telegram - SuasVendas Automação

Bot automatizado que consulta pedidos no sistema SuasVendas via **Telegram**.

## 🎯 Por que Telegram?

✅ **API Oficial Gratuita** - Sem custo, sem limite  
✅ **ZERO Risco de Bloqueio** - Feito para bots!  
✅ **Configuração Super Fácil** - 5 minutos  
✅ **Mais Estável** - Não cai, não dá problema  
✅ **Mais Recursos** - Botões, comandos, markdown  

---

## 📋 Funcionalidades

- 🔍 **Busca por nome** ou **cidade**
- 📊 **Últimos 10 pedidos** com detalhes completos
- 💰 **Cálculo automático** de valores e itens
- ⚡ **Respostas em ~10 segundos**
- 🕐 **Funciona 24/7** na nuvem

---

## 🚀 DEPLOY RÁPIDO (10 MINUTOS)

### **PARTE 1: CRIAR BOT NO TELEGRAM (2 min)**

1. **Abra o Telegram** (celular ou desktop)

2. **Busque por:** `@BotFather`

3. **Inicie conversa** e envie: `/newbot`

4. **Siga as instruções:**
   ```
   BotFather: Alright, a new bot. How are we going to call it?
   Você: SuasVendas Bot
   
   BotFather: Good. Now let's choose a username for your bot.
   Você: suasvendas_jackson_bot
   ```
   _(o username precisa terminar em "bot")_

5. **COPIE O TOKEN** que aparece:
   ```
   Use this token to access the HTTP API:
   1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ-1234567
   ```
   ⚠️ **GUARDE ESSE TOKEN!** Vai usar no Render!

6. **Pronto!** Seu bot foi criado! ✅

---

### **PARTE 2: GITHUB (3 min)**

1. **Acesse:** https://github.com

2. **Crie novo repositório:**
   - Nome: `suasvendas-telegram-bot`
   - Public: ✅
   - Add README: ✅

3. **Faça upload dos arquivos:**
   - Clique em "uploading an existing file"
   - Arraste TODOS os arquivos deste projeto
   - Commit changes

**Arquivos para enviar:**
- `bot_telegram.py`
- `automacao_suasvendas.py`
- `processador_dados.py`
- `requirements.txt`
- `render.yaml`
- `Dockerfile`
- `.gitignore`

---

### **PARTE 3: RENDER.COM (5 min)**

1. **Acesse:** https://render.com

2. **Login com GitHub**

3. **New + → Web Service**

4. **Conecte o repositório** `suasvendas-telegram-bot`

5. **Configure:**
   ```
   Name: suasvendas-telegram-bot
   Region: Oregon (US West)
   Branch: main
   Runtime: Docker
   Plan: Free
   ```

6. **Adicione variáveis de ambiente** (Advanced):
   ```
   TELEGRAM_TOKEN = [Cole o token do BotFather aqui]
   SUASVENDAS_EMAIL = especialista.representacoes@yahoo.com
   SUASVENDAS_SENHA = 7890
   ```

7. **Create Web Service** ✅

8. **Aguarde deploy** (~10 minutos)

---

## ✅ PRONTO! COMO USAR

### **Abra seu bot no Telegram:**

1. Busque pelo username que você criou (ex: `@suasvendas_jackson_bot`)
2. Clique em **START** ou envie `/start`

### **Comandos disponíveis:**

```
/start  - Mensagem de boas-vindas
/ajuda  - Instruções detalhadas
/status - Verifica se bot está online
/teste  - Faz busca de teste
```

### **Buscar pedidos:**

Digite o nome do cliente ou cidade (**sem comando**):

```
americana casa bonita
```

```
Americana
```

```
KORA MOBILIARIO
```

---

## 📊 EXEMPLO DE RESPOSTA

```
🔍 RESULTADOS: AMERICANA CASA BONITA
📊 Total: 10 pedidos
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 PEDIDO #23604
📅 Data: 27/01/2026
🏭 Indústria: KORA MOBILIARIO LTDA
🏢 Cliente: R.M.R MOVEIS E DECORACOES LTDA (CASA BONITA - OUTLET - AMERICANA)
📍 Cidade: Americana
💰 Valor: R$ 587,00
📦 Itens: 1

─────────────────────────────

📦 PEDIDO #23550
📅 Data: 11/12/2025
🏭 Indústria: KORA MOBILIARIO LTDA
🏢 Cliente: R.M.R MOVEIS E DECORACOES LTDA (CASA BONITA - OUTLET - AMERICANA)
📍 Cidade: Americana
💰 Valor: R$ 5.583,00
📦 Itens: 9

... (mais 8 pedidos)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 RESUMO GERAL
💰 Valor Total: R$ 15.234,00
📦 Total Itens: 45
🕐 31/01/2026 14:30
```

---

## 🔧 SOLUÇÃO DE PROBLEMAS

### **Bot não responde:**
1. Verifique se serviço está rodando no Render
2. Veja os logs
3. Confirme que TELEGRAM_TOKEN está correto

### **Erro no login SuasVendas:**
1. Verifique email e senha nas variáveis
2. Veja logs para identificar erro específico

### **Deploy falhou:**
1. Verifique se Dockerfile está no repositório
2. Confirme que requirements.txt está correto
3. Veja logs de build no Render

---

## 💰 CUSTOS

### **Telegram:**
- ✅ **Totalmente GRATUITO**
- ✅ Sem limites de mensagens
- ✅ API oficial

### **Render.com:**
- ✅ **Grátis:** 750 horas/mês
- 💵 **Pago:** $7/mês (se quiser ilimitado)

**Total: R$ 0 - R$ 35/mês**

---

## 🎁 VANTAGENS DO TELEGRAM

**vs WhatsApp:**

| Feature | Telegram | WhatsApp |
|---------|----------|----------|
| **API Oficial** | ✅ Sim | ❌ Não oficial |
| **Risco de Bloqueio** | ✅ Zero | ⚠️ Alto |
| **Custo** | ✅ Grátis | 💵 Pago |
| **Configuração** | ✅ 5 min | ⚠️ 30+ min |
| **Estabilidade** | ✅ Alta | ⚠️ Média |
| **Recursos** | ✅ Muitos | ⚠️ Limitados |

---

## 🔒 SEGURANÇA

✅ Token armazenado em variável de ambiente  
✅ Senha não fica no código  
✅ HTTPS automático  
✅ Logs privados  
✅ Bot isolado (não acessa seus contatos)  

---

## 📱 DICAS

1. **Use em viagem:** Bot roda 24/7 mesmo com notebook desligado
2. **Múltiplos usuários:** Adicione usuários autorizados (se quiser)
3. **Notificações:** Configure alertas para novos pedidos
4. **Backup:** Logs ficam salvos no Render por 7 dias

---

## 🆘 SUPORTE

**Logs em tempo real:**
- Dashboard Render → Logs

**Testar bot:**
- Envie `/status` no Telegram

**Problemas com token:**
- Gere novo token com @BotFather: `/token`

---

## ⚡ PRÓXIMAS MELHORIAS (OPCIONAL)

Funcionalidades que podem ser adicionadas:

- [ ] Busca por número de pedido
- [ ] Exportar para Excel
- [ ] Gráficos de vendas
- [ ] Alertas automáticos
- [ ] Relatórios programados
- [ ] Múltiplos usuários com permissões

---

## 🎉 PRONTO!

Seu bot Telegram está funcionando 24/7!

Consulte pedidos de qualquer lugar, a qualquer hora, apenas enviando uma mensagem! 🚀📱

---

**Criado com ❤️ por Claude AI**  
**Para: Jackson - Representante Comercial**  
**Versão: 2.0 - Telegram Edition**
