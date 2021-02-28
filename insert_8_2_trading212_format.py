# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Action,Time,ISIN,Ticker,Name,No. of shares,Price / share,Currency (Price / share),
# Exchange rate,Result (USD),Total (USD),Charge amount (USD),Transaction fee (USD),
# Finra fee (USD),Notes,ID

action = [] # 0
date = []   # 1
isin = []   # 2
stonk = []  # 4
# type = []   # - always common stock
amount = [] # 5
cost = []   # 6 action determines whether cost or sell get price
appropriationCost = []  # 12 + 13
sellPrice = []  # 6 action determines whether cost or sell get price
paidTax = '0'    # 0

def fill_currency_calc(driver, element, local_date, local_cost) :
    element.click()
    element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "currency")))
    element.click()
    element.send_keys(Keys.DOWN)  # 1st option is USD
    element.send_keys(Keys.RETURN)  # 1st option is USD
    element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "currencyDate")))
    element.send_keys( local_date )
    element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "currencySum")))
    element.send_keys( local_cost )
    element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "currency-calculator-calculate-button")))
    element.click()
    sleep(0.5)


def stonk_input(driver):
    try:
        driver.find_element_by_id("stockfunds-new-row-button").click()
        # okei fain added selenium wait conditions in
        # for i in range(len(stonk)):
        for i in range(len(stonk)):
            print_out(i)
            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "add_stockfunds_date")))
            element.send_keys( date[i] )
            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "add_stockfunds_isinCode")))
            element.send_keys( isin[i] )
            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "add_stockfunds_name")))
            element.send_keys( stonk[i] )
            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "add_stockfunds_amount")))
            element.send_keys( amount[i] )
            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "add_stockfunds_date")))
            element.send_keys( date[i] )

# fill in buy cost
            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "add-stockfunds-cost-amount-calculator-link")))
            fill_currency_calc(driver, element, date[i], cost[i])

# fill in fee cost
            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "add-stockfunds-appropriation-cost-calculator-link")))
            fill_currency_calc(driver, element, date[i], appropriationCost[i])

# fill in sell cost
            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "add-stockfunds-selling-price-calculator-link")))
            fill_currency_calc(driver, element, date[i], sellPrice[i])

            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "add_stockfunds_incomeTax")))
            element.send_keys( paidTax ) # 0

            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "add_stockfunds_state")))
            element.click()
            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "select-user-input-element")))
            element.click()
            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "add_stockfunds_state-5")))
            element.click()
            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "add_stockfunds_type")))
            element.send_keys(Keys.DOWN)  # 1st  option is common stock
            element.send_keys(Keys.RETURN)

            try:
                element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "add-stockfunds-save-button")))
                element.click()
            except Exception as e:
                element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "icon-close"))).click
                element.click()
                element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "add-stockfunds-save-button"))).click
                element.click()
            finally:
                sleep(2)  # gotta wait for emta to load

    except Exception as e:
        print(e)
        print("You gotta open the section manually, cus idk how tf to get it open sadge")


def read_file(file_name):
    file = open(file_name, "r", encoding='utf8')
    lines = file.readlines()

    for line in lines :
        line = line.replace("\n", "")
        line = line.replace(", ", ",")      # replace ', ' with ','
        line = line.replace('"', '')        # replace '"' with ''
        line = line.replace("Limit ", "")   # remove limit and market from string
        line = line.replace("Market ", "")
        temp_line_list = line.split(",")

        action.append(temp_line_list[0])
        date.append(reform_date(temp_line_list[1]))
        isin.append(temp_line_list[2])
        stonk.append(temp_line_list[4])
        amount.append(temp_line_list[5])

        if temp_line_list[0] == "buy" :
            cost.append(str(round( (float(temp_line_list[6]) * float(temp_line_list[5])), 3 )))
            sellPrice.append('0')
        elif temp_line_list[0] == "sell" :
            cost.append('0')
            sellPrice.append(str(round( (float(temp_line_list[6]) * float(temp_line_list[5])), 3 )))
        else :
            print("idk something broke")

        appropriationCost.append(get_appropriationCost(temp_line_list[12], temp_line_list[13]))


def get_appropriationCost (i, j) :
    if i == '' and j == '' :
        return '0'
    elif i != '' and j == '' :
        return i
    elif i == '' and j != '' :
        return j
    elif i != '' and j != '' :
        return str(float(i) + float(j))
    else :
        print("howd u break it again")
        return


def reform_date(old_date):
    temp_date = old_date.partition(" ")[0]
    new_date = temp_date[8:10] + "." + temp_date[5:7] + "." + temp_date[0:4]
    return new_date


def print_out(i):
    # for i in range(len(stonk)) :
    print(action[i] + ' ' + date[i] + ' ' + isin[i] + ' ' + stonk[i] + ' ' + amount[i] + ' ' + cost[i] + ' ' + sellPrice[i] + ' ' + appropriationCost[i])

def main():
    read_file("ptk_8_2.txt")
    # print_out()
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_driver = "chromedriver.exe"  # chromedriver should be in the same folder or findable from PATH
    driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
    driver.implicitly_wait(2) # seconds
    stonk_input(driver)
    driver.quit()


if __name__ == "__main__":
    main()
