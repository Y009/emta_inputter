from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep

stonk = []
isin = []
type = []
date = []
amount = []
cost = []
appropriationCost = []
sellPrice = []

def est_stonk_input(driver):
    try:
        driver.find_element_by_id("local-stockfunds-stock-funds-new-row-button").click()
        for i in range(len(stonk)):
            driver.find_element_by_id("add_localStockfunds_STOCK_FUNDS_code").send_keys( isin[i] )
            driver.find_element_by_id("add_localStockfunds_STOCK_FUNDS_name").send_keys( stonk[i] )
            driver.find_element_by_id("add_localStockfunds_STOCK_FUNDS_type").send_keys( Keys.DOWN + Keys.RETURN )
            driver.find_element_by_id("add_localStockfunds_STOCK_FUNDS_appropriationDate").send_keys( date[i] )
            driver.find_element_by_id("add_localStockfunds_STOCK_FUNDS_amount").send_keys( amount[i] )
            driver.find_element_by_id("add_localStockfunds_STOCK_FUNDS_costAmount").send_keys( cost[i] )
            driver.find_element_by_id("add_localStockfunds_STOCK_FUNDS_appropriationCost").send_keys( appropriationCost[i] )
            driver.find_element_by_id("add_localStockfunds_STOCK_FUNDS_sellingPrice").send_keys( sellPrice[i] )
            if i is not 0:
                driver.find_elements_by_class_name("icon-close ")[0].click()
            driver.find_element_by_id("add-local-stockfunds-stock-funds-save-button").click()
            sleep(0.1)
    except Exception as e:
        print(e)
        print("You gotta open the section manually, cus idk how tf to get it open sadge")


def read_file(file_name):
    file = open(file_name, "r")
    lines = file.readlines()
    for line in lines :
        line = line.replace("\n", "")
        line = line.replace(", ", ",")       # replace ', ' with ','
        line = line.replace('"', '')         # replace '"' with ''
        temp_line_list = line.split(",")
        stonk.append(temp_line_list[0])
        isin.append(temp_line_list[1])
        type.append(temp_line_list[2])
        date.append(temp_line_list[3])
        amount.append(temp_line_list[4])
        cost.append(temp_line_list[5])
        appropriationCost.append(temp_line_list[6])
        sellPrice.append(temp_line_list[7])


def main():
    read_file("ptk_6_1.txt")
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_driver = "chromedriver.exe"  # chromedriver should be in the same folder or findable from PATH
    driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
    est_stonk_input(driver)


if __name__ == "__main__":
    main()
