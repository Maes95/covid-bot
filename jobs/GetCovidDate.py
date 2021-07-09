from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import DesiredCapabilities
from testcontainers.selenium import BrowserWebDriverContainer
import telebot
import os

def click(driver, xpath):
    driver.find_element_by_xpath(xpath).click()

def write(driver, xpath, text):
    driver.find_element_by_xpath(xpath).send_keys(text)

def check_exists_by_text(driver, text):
    try:
        wait = WebDriverWait(driver, 5)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[contains(text(), "' + text + '")]')))
    except NoSuchElementException:
        return False
    return True
    

def tryGetDate():
    bot = telebot.TeleBot(os.environ['TELEGRAM_TOKEN']) 

    with BrowserWebDriverContainer(DesiredCapabilities.CHROME) as chrome:
        driver = chrome.get_driver()

        driver.implicitly_wait(5)

        driver.get('https://autocitavacuna.sanidadmadrid.org/ohcitacovid/')

        write(driver, '//*[@id="surname-container"]/hn-input-text-component/input', os.environ['SURNAME'])
        write(driver, '//*[@id="birthday-container"]/hn-input-mask-component/p-inputmask/input', os.environ['BIRTHDAY'])
        write(driver, '//*[@id="typedoc-container"]/div[2]/hn-input-text-component/input',os.environ['DNI'])
        click(driver, '//*[@id="usecondition-container"]')
        click(driver, '//*[@id="condiciones"]/div[7]/div[1]/hn-button-component/button/span')
        click(driver, '//*[@id="button-container"]/hn-button-component/button/span')
        write(driver, '//*[@id="phone-container"]/hn-input-text-component/input',os.environ['TLF'])
        click(driver, '//*[@id="button-container-form"]/hn-button-component/button')

        exist = check_exists_by_text(driver, 'You do not meet the criteria to request an appointment through this channel')

        if not exist:
            bot.send_message( os.environ['TELEGRAM_USER_1'], "CITA DISPONIBLE")
            bot.send_message( os.environ['TELEGRAM_USER_2'], "CITA DISPONIBLE")
        else:
            print("Cita no disponible")
            # bot.send_message( TELEGRAM_USER_1, "Cita no disponible")
            # bot.send_message( TELEGRAM_USER_2, "Cita no disponible")

        driver.quit()
    

    






