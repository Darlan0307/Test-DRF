from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from django.test import LiveServerTestCase
import time


class CustomerE2ETest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Remove isso se quiser ver o navegador abrir
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_create_customer(self):
        driver = self.driver
        driver.get(f'{self.live_server_url}/api/clientes/novo/')

        driver.find_element(By.NAME, "name").send_keys("Teste Selenium")
        driver.find_element(By.NAME, "cpf_cnpj").send_keys("12345678901")
        driver.find_element(By.NAME, "email").send_keys("selenium@teste.com")
        driver.find_element(By.NAME, "qtd_seller").clear()
        driver.find_element(By.NAME, "qtd_seller").send_keys("2")

        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type=submit]")
        submit_button.click()

        # Verifica se redirecionou para a lista
        self.assertIn("/api/clientes", driver.current_url)
        body_text = driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("Teste Selenium", body_text)

    def test_search_customer(self):
        # Pré-condição: Criação direta via ORM
        from customer.models import Customer
        Customer.objects.create(name="Buscar Teste", cpf_cnpj="98765432100", email="buscar@e2e.com")

        driver = self.driver
        driver.get(f'{self.live_server_url}/api/clientes/')
        search_box = driver.find_element(By.ID, "searchInput")
        search_box.send_keys("Buscar Teste")
        time.sleep(1)  # Espera a resposta da API

        table_text = driver.find_element(By.ID, "customerTable").text
        self.assertIn("Buscar Teste", table_text)
