# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# OPTIONS trades

# Company,ISIN,symbol,call/put date,Date/Time,Quantity,
# T. Price,C. Price,Proceeds,Comm/Fee,Basis,
# Realized P/L,Realized P/L %,MTM P/L,Code

options = True
commonStock = False

stonk = []  # 0
isin = []   # 1
date = []   # 4
action = [] # if 6 neg then buy, ig pos then sell
# type = []   # - always options
amount = [] # 6 (take absolute) * 100
cost = []   # 9 if action == buy else 0
appropriationCost = []  # 10
sellPrice = []  # 9 if action == sell else 0
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
        # for i in range(1):
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

# paid tax
            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "add_stockfunds_incomeTax")))
            element.send_keys( paidTax ) # 0

# country
            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "add_stockfunds_state")))
            element.click()
            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "select-user-input-element")))
            element.click()
            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "add_stockfunds_state-5"))) # select US
            element.click()
# type
            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "add_stockfunds_type")))
            element.click()
            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "add_stockfunds_type-7")))  # select options
            element.click()

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
        temp_line_list = line.split(",")

        stonk.append(temp_line_list[0])
        isin.append(temp_line_list[1])
        date.append(reform_date(temp_line_list[4]))
        temp_action = decide_buy_sell(temp_line_list[6])
        action.append(temp_action)
        amount.append(str(abs(int(temp_line_list[6]))))

        if temp_action == "buy" :
            cost.append(str(round(abs(float(temp_line_list[9])), 3 )))
            sellPrice.append('0')
        elif temp_action == "sell" :
            cost.append('0')
            sellPrice.append(str(round(abs(float(temp_line_list[9]) ), 3 )))
        else :
            print("idk something broke")

        appropriationCost.append(str(abs(float(temp_line_list[10]))))

def decide_buy_sell(value) :
    if int(value) > 0:
        return "buy"
    elif int(value) < 0:
        return "sell"
    else :
        print("how the f is the price 0")

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

#yyyy/mm/dd -> dd.mm.yyyy
def reform_date(old_date):
    temp_date = old_date.partition(" ")[0]
    new_date = temp_date[8:10] + "." + temp_date[5:7] + "." + temp_date[0:4]
    return new_date


def print_out(i):
    # for i in range(len(stonk)) :
    print(action[i] + ' ' + date[i] + ' ' + isin[i] + ' ' + stonk[i] + ' ' + amount[i] + ' ' + cost[i] + ' ' + sellPrice[i] + ' ' + appropriationCost[i])
        # print(sellPrice[i] )

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
