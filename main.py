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
        for game in games:
            table = game.find_elements_by_css_selector(
                'div.roadContainer--2ujMr svg')

            dot_dict = {}
            # y_array = []

            table_name = game.find_element_by_css_selector(
                'span.tableName--3PUPn')
            print("\n" + table_name.text)

            x_coor = None
            old_x = x_coor

            for dot in table:
                x_coor = dot.get_attribute('data-x')
                y_coor = dot.get_attribute('data-y')
                data_type = dot.get_attribute('data-type')

                try:
                    if int(x_coor) != int(old_x) and int(x_coor) - int(old_x) == 1:

                        dot_dict[str(x_coor)] = []

                    # if int(x_coor) != int(old_x) :

                    #     dot_dict[str(x_coor)] = []

                except Exception as ex:
                    try:
                        if isinstance(int(x_coor), int):
                            dot_dict[str(x_coor)] = []
                    except Exception as ex:
                        a = 0

                if data_type == 'coordinates':
                    # print(f'data-type: {data_type}\n x: {x_coor}, y: {y_coor} ')
                    # y_array.append(y_coor)
                    # dot_dict.update({x_coor : y_array})
                    # dot_dict[str(x_coor)] = []
                    dot_dict[str(x_coor)].append(y_coor)
                    old_x = x_coor

            print(dot_dict.items())

            # print(max(int(dot_dict.keys())))

        time.sleep(10)
        driver.close()

    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
