import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def test_login_functional():
    # Configurar Selenium con ChromeDriver automático
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Abre la página de login
        driver.get("http://localhost:8000/login")
        time.sleep(1)

        # Completar formulario
        username = driver.find_element(By.NAME, "username")
        password = driver.find_element(By.NAME, "password")

        username.send_keys("admin")
        password.send_keys("admin")

        # Enviar
        submit = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit.click()
        time.sleep(1)

        # Validar redirección
        assert "/books" in driver.current_url

    finally:
        driver.quit()
