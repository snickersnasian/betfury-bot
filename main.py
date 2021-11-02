from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from fake_useragent import UserAgent
import credentials
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

        time.sleep(5)

        try: #pop-up detect and close
            WebDriverWait(driver, 5).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, ".new-popup__container")))
            driver.find_element_by_css_selector('button.new-popup__btn-close').click()
        except:
            print('No pop-up found')

        # authenticate
        WebDriverWait(driver, 200).until(ec.visibility_of_element_located(
            (By.CSS_SELECTOR, ".btn.btn_outline.btn_medium")))
        driver.find_element_by_css_selector(
            '.btn.btn_outline.btn_medium').click()

        WebDriverWait(driver, 200).until(
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
        WebDriverWait(driver, 200).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, ".balance__inner")))

        driver.find_element_by_css_selector('.balance__inner').click()
        driver.find_element_by_css_selector(
            'div.balance-dropdown__inner.balance-dropdown__inner--darkened > ul > li:nth-child(4)').click()

        # Start game
        WebDriverWait(driver, 200).until(ec.visibility_of_element_located(
            (By.CSS_SELECTOR, "#play_button")))
        driver.find_element_by_css_selector('#play_button').click()

        # Switch to game iframe
        WebDriverWait(driver, 200).until(ec.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.single-game-modal-body-block iframe")))
        driver.switch_to.frame(driver.find_element_by_css_selector(
            "div.single-game-modal-body-block iframe"))

        WebDriverWait(driver, 200).until(ec.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.multiplayButtonContainer--a_4PI > div > div > button")))
        driver.find_element_by_css_selector(
            "div.multiplayButtonContainer--a_4PI > div > div > button").click()

        # Switch to game side-bar iframe
        WebDriverWait(driver, 200).until(ec.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.sidebar-container > iframe")))
        driver.switch_to.frame(driver.find_element_by_css_selector(
            "div.sidebar-container > iframe"))

        # Collect games
        WebDriverWait(driver, 200).until(ec.visibility_of_element_located(
            (By.CSS_SELECTOR, ".item--1TwGJ")))
        games = driver.find_elements_by_css_selector(".item--1TwGJ")

        WebDriverWait(driver, 200).until(ec.visibility_of_element_located(
            (By.CSS_SELECTOR, "svg > svg > g")))
        
        time.sleep(5)

        for game in games:

            streak = 0

            table_name = game.find_element_by_css_selector(
                'span.tableName--3PUPn')
            # print("\n" + table_name.text)

            last_dot = game.find_element_by_css_selector(
                '.item--1TwGJ div.roadContainer--2ujMr svg svg[data-type="coordinates"]:last-child')

            # print('X:' + last_dot.get_attribute("x"))
            # print('Y:' + last_dot.get_attribute("y"))

            x_coor = last_dot.get_attribute("x")
            y_coor = last_dot.get_attribute("y")

            if y_coor == "5":
                print("\n" + table_name.text)

                upper_dot = True

                while (upper_dot):
                    try:
                        game.find_element_by_css_selector (f'.item--1TwGJ div.roadContainer--2ujMr svg svg[data-type="coordinates"][x="{x_coor}"][y="{str(int(y_coor) - 1)}"]')
                        upper_dot = False
                    except:
                        upper_dot = True
                    
                    streak += 1

                    x_coor = str(int(x_coor) - 1)
                print(streak)    


                

        time.sleep(10)
        driver.close()

    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
