from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from fake_useragent import UserAgent
import credentials
import pickle
import time


ua = UserAgent()

# options
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={ua.chrome}")
options.add_argument("--start-maximized")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("--ignore-certificate-error")
options.add_argument("--ignore-ssl-errors")

# disable webdriver-mode
options.add_argument("--disable-blink-features=AutomationControlled")


def main():

    try:
        # initiate webdriver
        driver = webdriver.Chrome(
            'chromeDriver/chromedriver.exe',
            options=options
        )

        driver.get('https://betfury.io/live/baccarat-2-3-4')

        # authenticate
        WebDriverWait(driver, 20).until(ec.visibility_of_element_located(
            (By.CSS_SELECTOR, ".btn.btn_outline.btn_medium")))
        driver.find_element_by_css_selector(
            '.btn.btn_outline.btn_medium').click()

        WebDriverWait(driver, 20).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, ".input__value")))
        loginInput = driver.find_elements_by_css_selector('.input__value')[0]
        loginInput.clear()
        loginInput.send_keys(credentials.login)
        time.sleep(2)

        passInput = driver.find_elements_by_css_selector('.input__value')[1]
        passInput.clear()
        passInput.send_keys(credentials.password)

        submit_button = driver.find_element_by_css_selector(
            '.btn.btn_large.btn_block.btn_red')
        submit_button.click()

        # Set TRX currency
        WebDriverWait(driver, 20).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, ".balance__inner")))

        driver.find_element_by_css_selector('.balance__inner').click()
        driver.find_element_by_css_selector(
            'div.balance-dropdown__inner.balance-dropdown__inner--darkened > ul > li:nth-child(4)').click()
        
        WebDriverWait(driver, 20).until(ec.visibility_of_element_located(
            (By.CSS_SELECTOR, "#play_button")))
        driver.find_element_by_css_selector('#play_button').click()

        # Start game
        WebDriverWait(driver, 200).until(ec.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.multiplayButtonContainer--a_4PI > div > div > button")))
        driver.find_element_by_css_selector(
            'div.multiplayButtonContainer--a_4PI > div > div > button').click()

        time.sleep(100)
        # driver.close()

    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
