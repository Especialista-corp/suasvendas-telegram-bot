import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AutomacaoSuasVendas:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.email = os.getenv('SUASVENDAS_EMAIL')
        self.senha = os.getenv('SUASVENDAS_SENHA')
        
    def inicializar(self):
        """Inicializa o navegador Chrome"""
        try:
            logger.info("🔧 Inicializando navegador Chrome...")
            
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Detectar Chrome automaticamente
            chrome_binary = None
            possible_paths = [
                '/usr/bin/google-chrome',
                '/usr/bin/chromium-browser',
                '/usr/bin/chromium'
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    chrome_binary = path
                    break
            
            if chrome_binary:
                chrome_options.binary_location = chrome_binary
                logger.info(f"✅ Chrome encontrado em: {chrome_binary}")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 60)  # TIMEOUT AUMENTADO PARA 60 SEGUNDOS
            
            logger.info("✅ Chrome inicializado com sucesso!")
            
            # Fazer login
            return self._fazer_login()
            
        except Exception as e:
            logger.error(f"❌ Erro na inicialização: {e}")
            if self.driver:
                self.driver.quit()
            raise
    
    def _fazer_login(self):
        """Faz login no SuasVendas"""
        try:
            logger.info("🌐 Acessando https://account.suasvendas.com/login...")
            self.driver.get('https://account.suasvendas.com/login')
            
            # Aguardar campo de email
            time.sleep(3)
            
            logger.info("📧 Preenchendo email...")
            email_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"], input[name="email"], #email'))
            )
            email_input.clear()
            email_input.send_keys(self.email)
            
            # Aguardar Cloudflare
            time.sleep(5)
            
            # MÚLTIPLOS SELETORES PARA O BOTÃO CONTINUAR
            logger.info("🔍 Procurando botão 'Continuar'...")
            continuar_seletores = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button.btn-primary',
                'button.submit-button',
                '//button[contains(text(), "Continuar")]',
                '//button[contains(text(), "Continue")]',
                '//input[@type="submit"]',
                '//button[@type="submit"]'
            ]
            
            botao_continuar = None
            for seletor in continuar_seletores:
                try:
                    if seletor.startswith('//'):
                        botao_continuar = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, seletor))
                        )
                    else:
                        botao_continuar = self.wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, seletor))
                        )
                    logger.info(f"✅ Botão encontrado com seletor: {seletor}")
                    break
                except:
                    continue
            
            if not botao_continuar:
                logger.error("❌ Nenhum botão 'Continuar' encontrado!")
                self._salvar_screenshot("erro_botao_continuar")
                raise Exception("Botão 'Continuar' não encontrado após 60 segundos")
            
            logger.info("👆 Clicando em 'Continuar'...")
            botao_continuar.click()
            
            # Aguardar campo de senha
            time.sleep(3)
            
            logger.info("🔒 Preenchendo senha...")
            senha_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"], input[name="password"], #password'))
            )
            senha_input.clear()
            senha_input.send_keys(self.senha)
            
            # Procurar botão Enter/Login
            logger.info("🔍 Procurando botão 'Enter' ou 'Login'...")
            enter_seletores = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button.btn-primary',
                '//button[contains(text(), "Enter")]',
                '//button[contains(text(), "Login")]',
                '//button[contains(text(), "Entrar")]',
                '//button[@type="submit"]'
            ]
            
            botao_enter = None
            for seletor in enter_seletores:
                try:
                    if seletor.startswith('//'):
                        botao_enter = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, seletor))
                        )
                    else:
                        botao_enter = self.wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, seletor))
                        )
                    logger.info(f"✅ Botão Enter encontrado com seletor: {seletor}")
                    break
                except:
                    continue
            
            if not botao_enter:
                logger.error("❌ Nenhum botão 'Enter' encontrado!")
                self._salvar_screenshot("erro_botao_enter")
                raise Exception("Botão 'Enter' não encontrado")
            
            logger.info("👆 Clicando em 'Enter'...")
            botao_enter.click()
            
            # Aguardar redirecionamento
            time.sleep(5)
            
            # Verificar se está logado
            if 'app5.suasvendas.com' in self.driver.current_url or 'dashboard' in self.driver.current_url.lower():
                logger.info("✅ Login realizado com sucesso!")
                return True
            else:
                logger.error(f"❌ Login falhou. URL atual: {self.driver.current_url}")
                self._salvar_screenshot("erro_login_final")
                return False
                
        except TimeoutException as e:
            logger.error(f"❌ Timeout no login: {e}")
            self._salvar_screenshot("timeout_login")
            raise
        except Exception as e:
            logger.error(f"❌ Erro no login: {e}")
            self._salvar_screenshot("erro_login")
            raise
    
    def _salvar_screenshot(self, nome):
        """Salva screenshot para debug"""
        try:
            caminho = f"/tmp/{nome}_{int(time.time())}.png"
            self.driver.save_screenshot(caminho)
            logger.info(f"📸 Screenshot salvo em: {caminho}")
        except:
            pass
    
    def buscar_pedidos(self, termo_busca):
        """Busca pedidos no SuasVendas"""
        try:
            logger.info(f"🔍 Buscando por: {termo_busca}")
            
            # Acessar página de pedidos
            self.driver.get('https://app5.suasvendas.com/Pedido')
            time.sleep(3)
            
            # Procurar campo de busca
            logger.info("📝 Preenchendo campo de busca...")
            busca_seletores = [
                'input[type="search"]',
                'input[placeholder*="Pesquisar"]',
                'input[placeholder*="Buscar"]',
                '#search',
                '.search-input'
            ]
            
            campo_busca = None
            for seletor in busca_seletores:
                try:
                    campo_busca = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, seletor))
                    )
                    break
                except:
                    continue
            
            if not campo_busca:
                logger.error("❌ Campo de busca não encontrado!")
                self._salvar_screenshot("erro_campo_busca")
                return []
            
            campo_busca.clear()
            campo_busca.send_keys(termo_busca)
            
            # Aguardar resultados
            time.sleep(5)
            
            # Extrair tabela de pedidos
            logger.info("📊 Extraindo resultados...")
            linhas = self.driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')
            
            pedidos = []
            for linha in linhas[:10]:  # Primeiros 10
                try:
                    colunas = linha.find_elements(By.TAG_NAME, 'td')
                    if len(colunas) >= 3:
                        pedido = {
                            'numero': colunas[0].text.strip(),
                            'cliente': colunas[1].text.strip(),
                            'valor': colunas[2].text.strip() if len(colunas) > 2 else '',
                            'status': colunas[3].text.strip() if len(colunas) > 3 else '',
                            'data': colunas[4].text.strip() if len(colunas) > 4 else ''
                        }
                        pedidos.append(pedido)
                except:
                    continue
            
            logger.info(f"✅ Encontrados {len(pedidos)} pedidos")
            return pedidos
            
        except Exception as e:
            logger.error(f"❌ Erro na busca: {e}")
            self._salvar_screenshot("erro_busca")
            return []
    
    def fechar(self):
        """Fecha o navegador"""
        if self.driver:
            self.driver.quit()
            logger.info("🔚 Navegador fechado")
