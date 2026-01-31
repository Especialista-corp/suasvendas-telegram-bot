# 📸 GUIA VISUAL COMPLETO - TELEGRAM

## 🎯 PARTE 1: CRIAR BOT NO TELEGRAM

### **PASSO 1.1: Abrir BotFather**

```
1. Abra o Telegram (celular ou computador)
2. Na busca, digite: @BotFather
3. Clique no bot oficial (tem verificado azul ✓)
4. Clique em "START" ou "INICIAR"
```

---

### **PASSO 1.2: Criar Novo Bot**

**Digite no chat:**
```
/newbot
```

**BotFather vai perguntar o nome:**
```
┌─────────────────────────────────────┐
│ BotFather:                          │
│ Alright, a new bot.                 │
│ How are we going to call it?        │
│ Please choose a name for your bot.  │
└─────────────────────────────────────┘

Você digita:
SuasVendas Bot
(pode ser qualquer nome bonito)
```

---

### **PASSO 1.3: Escolher Username**

**BotFather vai pedir o username:**
```
┌─────────────────────────────────────┐
│ BotFather:                          │
│ Good. Now let's choose a username   │
│ for your bot. It must end in `bot`. │
│ Like this, for example: TetrisBot   │
└─────────────────────────────────────┘

Você digita:
suasvendas_jackson_bot
(PRECISA terminar com "bot")
```

**Sugestões de usernames:**
- `suasvendas_jackson_bot`
- `representante_pedidos_bot`
- `consulta_vendas_bot`

---

### **PASSO 1.4: COPIAR O TOKEN** ⚠️ IMPORTANTE!

**BotFather vai retornar:**
```
┌─────────────────────────────────────┐
│ Done! Congratulations on your       │
│ new bot. You will find it at        │
│ t.me/suasvendas_jackson_bot         │
│                                     │
│ Use this token to access the HTTP   │
│ API:                                │
│ 1234567890:ABCdefGHI-1234567890     │ ← COPIE ISSO!
│                                     │
│ Keep your token secure and store    │
│ it safely...                        │
└─────────────────────────────────────┘
```

**⚠️ COPIE E GUARDE ESSE TOKEN!**

---

## 🎯 PARTE 2: GITHUB

### **PASSO 2.1: Criar Repositório**

```
1. Acesse: https://github.com
2. Clique no "+" → "New repository"
3. Preencha:
   ┌─────────────────────────────────┐
   │ Repository name*                │
   │ suasvendas-telegram-bot         │ ← Digite
   ├─────────────────────────────────┤
   │ Description                     │
   │ Bot Telegram para SuasVendas    │ ← Digite
   ├─────────────────────────────────┤
   │ ⚫ Public  ⚪ Private            │ ← Public
   │ [✓] Add a README file           │ ← Marque
   ├─────────────────────────────────┤
   │ [ Create repository ]           │ ← Clique
   └─────────────────────────────────┘
```

---

### **PASSO 2.2: Upload dos Arquivos**

```
1. No repositório criado
2. Clique "Add file" → "Upload files"
3. Arraste TODOS os 7 arquivos:
   ✅ bot_telegram.py
   ✅ automacao_suasvendas.py
   ✅ processador_dados.py
   ✅ requirements.txt
   ✅ render.yaml
   ✅ Dockerfile
   ✅ .gitignore

4. Clique "Commit changes"
```

---

## 🎯 PARTE 3: RENDER.COM

### **PASSO 3.1: Criar Conta**

```
1. Acesse: https://render.com
2. Clique "Get Started for Free"
3. Selecione "Sign up with GitHub"
4. Autorize o Render
```

---

### **PASSO 3.2: Criar Web Service**

```
┌─────────────────────────────────────┐
│ RENDER DASHBOARD                    │
├─────────────────────────────────────┤
│ [ New + ]                           │ ← Clique
│   └─ Web Service                    │ ← Selecione
└─────────────────────────────────────┘
```

---

### **PASSO 3.3: Conectar Repositório**

```
┌─────────────────────────────────────┐
│ Connect a repository                │
├─────────────────────────────────────┤
│ 🔍 Search repositories              │
│                                     │
│ ○ suasvendas-telegram-bot           │ ← Selecione
│   [ Connect ]                       │ ← Clique
└─────────────────────────────────────┘
```

---

### **PASSO 3.4: Configurar Serviço**

**Preencha EXATAMENTE:**

```
┌─────────────────────────────────────────┐
│ Name*                                   │
│ suasvendas-telegram-bot                 │ ← Nome
├─────────────────────────────────────────┤
│ Region                                  │
│ [ Oregon (US West) ▼ ]                 │ ← Selecione
├─────────────────────────────────────────┤
│ Branch                                  │
│ main                                    │ ← Padrão
├─────────────────────────────────────────┤
│ Runtime                                 │
│ [ Docker ▼ ]                           │ ← IMPORTANTE!
└─────────────────────────────────────────┘
```

**⚠️ IMPORTANTE: Runtime = Docker!**

---

### **PASSO 3.5: Plano Gratuito**

```
┌─────────────────────────────────────┐
│ Instance Type                       │
├─────────────────────────────────────┤
│ ⚫ Free                              │ ← Selecione
│    $0/month                         │
│    512 MB RAM                       │
│    750 hours/month                  │
└─────────────────────────────────────┘
```

---

### **PASSO 3.6: Variáveis de Ambiente** ⚠️ CRÍTICO!

**Clique em "Advanced" e adicione:**

```
┌──────────────────────────────────────────────────┐
│ Environment Variables                            │
├──────────────────────────────────────────────────┤
│ [ Add Environment Variable ]                     │ ← Clique
├──────────────────────────────────────────────────┤
│ Key: TELEGRAM_TOKEN                              │
│ Value: [Cole o token do BotFather aqui]         │
│        1234567890:ABCdefGHI-1234567890           │
├──────────────────────────────────────────────────┤
│ [ Add Environment Variable ]                     │ ← Clique
├──────────────────────────────────────────────────┤
│ Key: SUASVENDAS_EMAIL                            │
│ Value: especialista.representacoes@yahoo.com     │
├──────────────────────────────────────────────────┤
│ [ Add Environment Variable ]                     │ ← Clique
├──────────────────────────────────────────────────┤
│ Key: SUASVENDAS_SENHA                            │
│ Value: 7890                                      │
└──────────────────────────────────────────────────┘
```

**⚠️ IMPORTANTE:**
- TELEGRAM_TOKEN = O token que você copiou do BotFather
- Não esqueça NENHUMA variável!

---

### **PASSO 3.7: DEPLOY!**

```
┌─────────────────────────────────────┐
│                                     │
│ [ Create Web Service ]              │ ← CLIQUE!
│                                     │
└─────────────────────────────────────┘
```

**Aguarde ~10-15 minutos...**

**Logs que você vai ver:**
```
Building...
 => [1/8] FROM docker.io/library/python:3.11-slim
 => [2/8] Installing system dependencies...
 => [3/8] Installing Google Chrome...
 => [4/8] Installing ChromeDriver...
 => [5/8] Installing Python packages...
 => [6/8] Copying application files...
 => [7/8] Build complete!
 => [8/8] Starting bot...

✅ Chrome inicializado
🌐 Acessando login...
📧 Preenchendo email...
🔐 Preenchendo senha...
✅ Login realizado!
🤖 Bot Telegram inicializado!
✅ Sistema pronto!
```

**Quando ver "Sistema pronto!" = FUNCIONANDO!** ✅

---

## 🎯 PARTE 4: TESTAR NO TELEGRAM

### **PASSO 4.1: Abrir Seu Bot**

```
1. Abra o Telegram
2. Busque: @suasvendas_jackson_bot (seu username)
3. Clique no bot
4. Clique "START" ou envie: /start
```

---

### **PASSO 4.2: Testar Comandos**

**Envie:**
```
/status
```

**Deve responder:**
```
✅ Bot Online e Funcionando!

🤖 Sistema operacional
🔗 Conectado ao SuasVendas
✨ Pronto para buscar pedidos!
```

---

### **PASSO 4.3: Fazer Busca**

**Digite (sem comando):**
```
americana casa bonita
```

**Bot vai responder:**
```
🔍 Buscando pedidos...
Termo: americana casa bonita
⏳ Aguarde alguns segundos...

[depois de ~10 segundos]

🔍 RESULTADOS: AMERICANA CASA BONITA
📊 Total: 10 pedidos
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 PEDIDO #23604
📅 Data: 27/01/2026
...
```

---

## ✅ CHECKLIST FINAL

Antes de usar, confirme:

- [ ] Bot criado no BotFather ✅
- [ ] Token copiado ✅
- [ ] Repositório GitHub criado ✅
- [ ] Arquivos enviados (7 arquivos) ✅
- [ ] Web Service criado no Render ✅
- [ ] Runtime = Docker ✅
- [ ] 3 variáveis adicionadas ✅
- [ ] Deploy concluído sem erros ✅
- [ ] Bot responde /status ✅
- [ ] Busca funciona ✅

**Tudo OK? PRONTO PARA USAR!** 🎉

---

## 🆘 PROBLEMAS COMUNS

### ❌ "Bot doesn't respond"
**Solução:**
1. Vá no Render → Logs
2. Procure por erros
3. Verifique se TELEGRAM_TOKEN está correto
4. Reinicie o serviço

### ❌ "Deploy failed - Chrome not found"
**Solução:**
1. Certifique que Runtime = Docker
2. Dockerfile está no repositório?
3. Force redeploy

### ❌ "Login falhou"
**Solução:**
1. Confirme email e senha nas variáveis
2. Veja logs detalhados
3. SuasVendas pode estar fora do ar

---

**Dúvidas? Volte no README.md!** 📖
