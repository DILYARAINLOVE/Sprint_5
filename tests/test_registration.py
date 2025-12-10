import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from locators import MainPageLocators, AuthModalLocators
from data import TestData
import time

class TestRegistration:
    
    def find_element_with_fallback(self, driver, *locators):
        """Поиск элемента с несколькими вариантами локаторов"""
        for locator in locators:
            try:
                elements = driver.find_elements(*locator)
                if elements:
                    return elements[0]
            except:
                continue
        return None
    
    def test_successful_registration(self, driver, wait):
        """Тест успешной регистрации"""
        
        # 1. Открываем главную страницу
        driver.get(TestData.BASE_URL)
        time.sleep(3)
        
        # 2. Нажимаем кнопку "Вход и регистрация"
        login_button = self.find_element_with_fallback(
            driver,
            MainPageLocators.LOGIN_REGISTRATION_BUTTON,
            (By.XPATH, "//button"),
            (By.CLASS_NAME, "button")
        )
        
        if not login_button:
            
            driver.save_screenshot("debug_no_login_button.png")
            pytest.fail("Не найдена кнопка входа")
        
        login_button.click()
        time.sleep(2)
        
        # 3. Нажимаем кнопку "Нет аккаунта"
        no_account_button = self.find_element_with_fallback(
            driver,
            AuthModalLocators.NO_ACCOUNT_BUTTON,
            (By.XPATH, "//button[contains(., 'Нет')]"),
            (By.XPATH, "//button[contains(., 'регистрация')]")
        )
        
        if no_account_button:
            no_account_button.click()
        time.sleep(2)
        
        # 4. Заполняем форму регистрации
        email_input = self.find_element_with_fallback(
            driver,
            AuthModalLocators.REG_EMAIL_INPUT,
            (By.XPATH, "//input[@type='email']"),
            (By.XPATH, "//input[contains(@placeholder, 'Email')]")
        )
        
        if email_input:
            email_input.send_keys(TestData.generate_email())
        
        
        password_inputs = driver.find_elements(By.XPATH, "//input[@type='password']")
        if len(password_inputs) >= 2:
            password_inputs[0].send_keys("TestPassword123!")
            password_inputs[1].send_keys("TestPassword123!")
        elif password_inputs:
            password_inputs[0].send_keys("TestPassword123!")
        
        # 5. Нажимаем кнопку "Создать аккаунт"
        create_button = self.find_element_with_fallback(
            driver,
            AuthModalLocators.CREATE_ACCOUNT_BUTTON,
            (By.XPATH, "//button[contains(., 'Создать')]"),
            (By.XPATH, "//button[contains(., 'Зарегистрировать')]")
        )
        
        if create_button:
            create_button.click()
        
        time.sleep(3)
        
        # 6. Проверяем успешную регистрацию
        
        avatar_found = False
        for locator in [MainPageLocators.USER_AVATAR, MainPageLocators.USER_NAME]:
            elements = driver.find_elements(*locator)
            if elements:
                avatar_found = True
                break
        
        assert avatar_found, "После регистрации не отображается аватар или имя пользователя"
    
    def test_registration_invalid_email(self, driver, wait):
        """Регистрация с невалидным email"""
        driver.get(TestData.BASE_URL)
        time.sleep(3)
        
        login_button = driver.find_element(*MainPageLocators.LOGIN_REGISTRATION_BUTTON)
        login_button.click()
        time.sleep(2)
        
        # Переходим к регистрации
        no_account_button = driver.find_element(*AuthModalLocators.NO_ACCOUNT_BUTTON)
        no_account_button.click()
        time.sleep(2)
        
        # Вводим невалидный email
        email_input = driver.find_element(*AuthModalLocators.REG_EMAIL_INPUT)
        email_input.send_keys("invalid-email")
        
        # Нажимаем кнопку создания
        create_button = driver.find_element(*AuthModalLocators.CREATE_ACCOUNT_BUTTON)
        create_button.click()
        time.sleep(2)
        
        # Проверяем наличие ошибок
        error_elements = driver.find_elements(*AuthModalLocators.ERROR_MESSAGE)
        assert len(error_elements) > 0, "Должно появиться сообщение об ошибке"
    
    def test_registration_existing_user(self, driver, wait):
        """Регистрация уже существующего пользователя"""
        driver.get(TestData.BASE_URL)
        time.sleep(3)
        
        login_button = driver.find_element(*MainPageLocators.LOGIN_REGISTRATION_BUTTON)
        login_button.click()
        time.sleep(2)
        
        no_account_button = driver.find_element(*AuthModalLocators.NO_ACCOUNT_BUTTON)
        no_account_button.click()
        time.sleep(2)
        
        # Используем существующий email
        email_input = driver.find_element(*AuthModalLocators.REG_EMAIL_INPUT)
        email_input.send_keys(TestData.EXISTING_USER_EMAIL)
        
        # Заполняем пароли
        password_inputs = driver.find_elements(By.XPATH, "//input[@type='password']")
        if password_inputs:
            password_inputs[0].send_keys("SomePassword123")
            if len(password_inputs) > 1:
                password_inputs[1].send_keys("SomePassword123")
        
        create_button = driver.find_element(*AuthModalLocators.CREATE_ACCOUNT_BUTTON)
        create_button.click()
        time.sleep(2)
        
        # Проверяем ошибку
        error_elements = driver.find_elements(*AuthModalLocators.ERROR_MESSAGE)
        assert len(error_elements) > 0, "Должно появиться сообщение об ошибке существующего пользователя"