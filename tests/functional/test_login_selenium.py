import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


@pytest.mark.skipif(
    os.getenv("CI") == "true",
    reason="Se omite Selenium en CI porque no hay navegador real disponible.",
)
def test_login_functional():
    # Configurar Selenium con ChromeDriver (para ejecución LOCAL)
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("http://127.0.0.1:8000/login")

        # Localiza campos del formulario
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        # Hace login como admin/admin
        username_input.send_keys("admin")
        password_input.send_keys("admin")
        submit_button.click()

        # Verifica que redirige a /books
        assert "/books" in driver.current_url
    finally:
        driver.quit()
