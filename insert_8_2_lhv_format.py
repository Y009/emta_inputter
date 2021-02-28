# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep

country = []
stonk = []
isin = []
type = []
date = []
amount = []
cost = []
appropriationCost = []
sellPrice = []
paidTax = []

def stonk_input(driver):
    try:
        driver.find_element_by_id("stockfunds-new-row-button").click()
        sleep(0.2)
        for i in range(len(stonk)):
            driver.find_element_by_id("add_stockfunds_date").send_keys( date[i] )
            print(date[i])
            driver.find_element_by_id("add_stockfunds_isinCode").send_keys( isin[i] )
            print(isin[i])
            driver.find_element_by_id("add_stockfunds_name").send_keys( stonk[i] )
            print(stonk[i])
            driver.find_element_by_id("add_stockfunds_amount").send_keys( amount[i] )
            print(amount[i])
            driver.find_element_by_id("add_stockfunds_costAmount").send_keys( cost[i] )
            print(cost[i])
            driver.find_element_by_id("add_stockfunds_appropriationCost").send_keys( appropriationCost[i] )
            print(appropriationCost[i])
            driver.find_element_by_id("add_stockfunds_sellingPrice").send_keys( sellPrice[i] )
            print(sellPrice[i])
            driver.find_element_by_id("add_stockfunds_incomeTax").send_keys( paidTax[i] )
            print(paidTax[i])

            driver.find_element_by_id("add_stockfunds_state").click()
            driver.find_element_by_id("select-user-input-element").send_keys( country[i] )
            driver.find_element_by_id("select-user-input-element").send_keys(Keys.RETURN )  # choose 1sts returened value
            driver.find_element_by_id("add_stockfunds_type").click()
            driver.find_element_by_id("add_stockfunds_type").send_keys( Keys.DOWN + Keys.RETURN )  # choose aktsiad from dropdown

            driver.find_element_by_id("add-stockfunds-save-button").click()

            try:            # should change to wait until clickable, but meh try catch go brrrr
                sleep(0.2)
                driver.find_elements_by_class_name("icon-close")[0].click()
            except Exception as e:

                print("failed clicking this stupid pop-up")
                print(e)
                sleep(0.5)
                    try:            # shpuld change to wait until clickable, but meh
                        sleep(0.5)
                        driver.find_elements_by_class_name("icon-close")[0].click()
                    except Exception as e:
                        print("failed clicking this stupid pop-up again")
                        print(e)
                        driver.find_elements_by_class_name("icon-close")[0].click()

    except Exception as e:
        print(e)
        print("You gotta open the section manually, cus idk how tf to get it open sadge")


def read_file(file_name):
    file = open(file_name, "r", encoding='utf8')
    lines = file.readlines()
    for line in lines :
        line = line.replace("\n", "")
        line = line.replace(", ", ",")       # replace ', ' with ','
        line = line.replace('"', '')         # replace '"' with ''
        temp_line_list = line.split(",")
        country.append(temp_line_list[0][:4])
        stonk.append(temp_line_list[1])
        isin.append(temp_line_list[2])
        type.append(temp_line_list[3])
        date.append(temp_line_list[4])
        amount.append(temp_line_list[5])
        cost.append(temp_line_list[6])
        appropriationCost.append(temp_line_list[7])
        sellPrice.append(temp_line_list[8])
        paidTax.append(temp_line_list[9])

def main():
    read_file("ptk_8_2.txt")
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_driver = "chromedriver.exe"  # chromedriver should be in the same folder or findable from PATH
    driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
    driver.implicitly_wait(2) # seconds
    stonk_input(driver)
    driver.quit()


if __name__ == "__main__":
    main()
