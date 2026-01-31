#!/usr/bin/env python3
"""
Automação SuasVendas - Otimizada para Render.com
Descrição: Controla o browser e executa buscas no sistema SuasVendas
"""

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

logger = logging.getLogger(__name__)

# Configurações do SuasVendas
EMAIL = os.getenv('SUASVENDAS_EMAIL', 'especialista.representacoes@yahoo.com')
SENHA = os.getenv('SUASVENDAS_SENHA', '7890')
URL_LOGIN = 'https://account.suasvendas.com/login'

class AutomacaoSuasVendas:
    """Classe para automação do SuasVendas"""
    
    def __init__(self):
        """Inicializa o navegador"""
        logger.info("🔧 Inicializando navegador Chrome...")
        
        self.driver = None
        self.wait = None
        self.logado = False
        
        try:
            self._inicializar_driver()
            self._fazer_login()
            logger.info("✅ Navegador inicializado e login realizado!")
        except Exception as e:
            logger.error(f"❌ Erro na inicialização: {e}")
            raise
    
    def _inicializar_driver(self):
        """Inicializa o Chrome com configurações otimizadas para Render.com"""
        chrome_options = Options()
        
        # Configurações essenciais para Render.com
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--disable-dev-tools')
        chrome_options.add_argument('--no-zygote')
        
        # User agent
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Tamanho da janela
        chrome_options.add_argument('--window-size=1920,1080')
        
        # Configurações anti-detecção
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Detecta se está no Render.com (Linux)
        chrome_binary = None
        chromedriver_path = None
        
        # Tenta localizar Chrome/Chromium
        possible_paths = [
            '/usr/bin/chromium',
            '/usr/bin/chromium-browser', 
            '/usr/bin/google-chrome',
            '/usr/bin/google-chrome-stable',
            '/opt/google/chrome/chrome',
            '/opt/render/project/.render/chrome/opt/google/chrome/chrome'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                chrome_binary = path
                logger.info(f"✅ Chrome encontrado em: {path}")
                break
        
        if chrome_binary:
            chrome_options.binary_location = chrome_binary
        
        try:
            # Tenta inicializar com Service (se chromedriver estiver disponível)
            if chromedriver_path and os.path.exists(chromedriver_path):
                service = Service(chromedriver_path)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            else:
                # Deixa Selenium encontrar automaticamente
                self.driver = webdriver.Chrome(options=chrome_options)
            
            self.wait = WebDriverWait(self.driver, 20)
            logger.info("✅ Chrome inicializado com sucesso!")
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar Chrome: {e}")
            raise
    
    def _fazer_login(self):
        """Faz login no SuasVendas"""
        try:
            logger.info(f"🌐 Acessando {URL_LOGIN}...")
            self.driver.get(URL_LOGIN)
            time.sleep(3)
            
            # Passo 1: Preencher email
            logger.info("📧 Preenchendo email...")
            campo_email = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
            )
            campo_email.clear()
            campo_email.send_keys(EMAIL)
            
            # Marcar "Lembrar email"
            try:
                checkboxes = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
                if len(checkboxes) >= 2 and not checkboxes[1].is_selected():
                    checkboxes[1].click()
            except:
                pass
            
            # Aguardar Cloudflare
            logger.info("⏳ Aguardando Cloudflare...")
            time.sleep(3)
            
            # Clicar em Continuar
            logger.info("▶️ Clicando em Continuar...")
            botao_continuar = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Continuar")]'))
            )
            botao_continuar.click()
            time.sleep(2)
            
            # Passo 2: Preencher senha
            logger.info("🔐 Preenchendo senha...")
            campo_senha = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
            )
            time.sleep(1)
            campo_senha.clear()
            campo_senha.send_keys(SENHA)
            
            # Fazer login
            logger.info("🔓 Fazendo login...")
            botao_entrar = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
            )
            botao_entrar.click()
            time.sleep(4)
            
            # Verifica se login foi bem sucedido
            if 'login' not in self.driver.current_url.lower():
                logger.info("✅ Login realizado com sucesso!")
                self.logado = True
            else:
                logger.error("❌ Login falhou - ainda na página de login")
                raise Exception("Falha no login")
                
        except Exception as e:
            logger.error(f"❌ Erro no login: {e}")
            raise
    
    def buscar_pedidos(self, termo_busca, limite=10):
        """
        Busca pedidos no SuasVendas
        
        Args:
            termo_busca (str): Termo para buscar (nome cliente, cidade, etc)
            limite (int): Número máximo de pedidos para retornar
        
        Returns:
            list: Lista de dicionários com dados dos pedidos
        """
        try:
            logger.info(f"🔍 Buscando pedidos para: {termo_busca}")
            
            # Navegar para Pedidos
            logger.info("📂 Navegando para seção Pedidos...")
            menu_pedidos = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Pedidos")]'))
            )
            menu_pedidos.click()
            time.sleep(2)
            
            # Localizar campo de busca
            logger.info("🔎 Localizando campo de busca...")
            campo_busca = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"], input[type="search"]'))
            )
            
            # Limpar e digitar termo de busca
            campo_busca.clear()
            time.sleep(0.5)
            campo_busca.send_keys(termo_busca)
            time.sleep(1)
            
            # Clicar no botão Procurar
            logger.info("🔍 Clicando em Procurar...")
            botao_procurar = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Procurar")]'))
            )
            botao_procurar.click()
            time.sleep(3)
            
            # Extrair dados da tabela
            logger.info("📊 Extraindo dados da tabela...")
            pedidos = self._extrair_dados_tabela(limite)
            
            logger.info(f"✅ {len(pedidos)} pedidos encontrados")
            return pedidos
            
        except Exception as e:
            logger.error(f"❌ Erro na busca: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _extrair_dados_tabela(self, limite=10):
        """Extrai dados da tabela de pedidos"""
        pedidos = []
        
        try:
            time.sleep(2)
            linhas = self.driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')
            logger.info(f"📋 {len(linhas)} linhas encontradas na tabela")
            
            for i, linha in enumerate(linhas[:limite]):
                try:
                    celulas = linha.find_elements(By.TAG_NAME, 'td')
                    
                    if len(celulas) < 8:
                        continue
                    
                    pedido = {
                        'numero': celulas[2].text.strip(),
                        'data_venda': celulas[4].text.strip(),
                        'industria': celulas[5].text.strip(),
                        'razao_social': celulas[6].text.strip(),
                        'cidade': celulas[7].text.strip(),
                        'valor': celulas[8].text.strip(),
                        'itens': celulas[9].text.strip()
                    }
                    
                    if pedido['numero']:
                        pedidos.append(pedido)
                        logger.debug(f"📦 Pedido #{pedido['numero']} extraído")
                    
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao extrair linha {i}: {e}")
                    continue
            
            return pedidos
            
        except Exception as e:
            logger.error(f"❌ Erro ao extrair dados: {e}")
            return []
    
    def is_ready(self):
        """Verifica se a automação está pronta"""
        return self.driver is not None and self.logado
    
    def fechar(self):
        """Fecha o navegador"""
        try:
            if self.driver:
                self.driver.quit()
                logger.info("🔚 Navegador fechado")
        except:
            pass
    
    def __del__(self):
        """Destrutor"""
        self.fechar()
