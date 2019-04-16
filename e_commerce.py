from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from time import sleep, strftime
import os
# from open_tor import OpenTor


class ECommerceList(object):

    def __init__(self):
        # open_tor = OpenTor()
        self.now = strftime("%c")
        self.driver = webdriver.Firefox()
        self.store_name_list = []
        self.store_url_list = []
        self.stores = {
                "Best Buy": "https://www.bestbuy.com/",
                "Amazon": "https://www.amazon.com/"}
        for store_name, store_url in self.stores.items():
            self.store_name_list.append(store_name)
            self.store_url_list.append(store_url)

    def get_website(self):
        """
        open_tor_browser = OpenTor()
        open_tor_browser.get_url(url=self.store_url_list[i])
        assert self.store_name_list[i] in self.browser.title
        """
        self.driver.get(self.store_url_list[self.i])
        assert self.store_name_list[self.i] in self.driver.title

    """def write_top_page(self, the_upc,):
        with open(self.file_name, "w") as RFile:
            RFile.write("For the {0} ".format(the_upc))"""

    def write_to_RFile(self, the_upc, file_name="flask_prce_finder.txt"):
        lines_to_write = ["\n\nCurrent time:{0}".format(self.now),
                          "\nStore: {0}".format(self.store_name_list[self.i]),
                          "\nProduct Title: {0}".format(self.product_title),
                          "\nProduct Price: {0}".format(self.product_price_value),
                          "\nIndividual seller: {0}".format(self.product_seller_information),
                          "\nInStock: {0}".format(self.stock),
                          "\nurl: {0}".format(self.driver.current_url)]
        with open(file_name, "a") as RFile:
            if os.stat(file_name).st_size == 0:
                RFile.write("For the upc:{0} ".format(the_upc))
                RFile.writelines(lines_to_write)
            else:
                RFile.writelines(lines_to_write)


class BestBuy(ECommerceList):

    def __init__(self):
        self.i = 0
        super(BestBuy, self).__init__()

    def find_item(self, upc):
        try:
            search_box = self.driver.find_element_by_id("gh-search-input")
            search_box.clear()
            search_box.send_keys(upc)
            search_icon = self.driver.find_element_by_class_name("header-search-button")
            search_icon.click()
            product = self.driver.find_element_by_class_name("product-image")
            product_description = self.driver.find_element_by_class_name("sku-header")

            self.product_title = product_description.text

            product.click()
            product_price = self.driver.find_element_by_css_selector(".priceView-hero-price > span:nth-child(1)")
            self.product_price_value = eval(product_price.text[1:])
            self.product_seller_information = "Best Buy"

            print(self.product_title)
            print(product_price.text)
            print(self.product_seller_information)

            try:
                product_stock = self.driver.find_element_by_class_name("btn-primary")
                self.stock = True
                print("In stock.")
            except NoSuchElementException:
                ActionToRunInCaseNoSuchElement = True
            try:
                product_stock = self.driver.find_element_by_class_name("button-state-sold-out")
                self.stock = False
                print("Out of stock.")
            except NoSuchElementException:
                ActionToRunInCaseNoSuchElement = True

        except NoSuchElementException:
            print("A product satisfying the upc is not found.")
            ActionToRunInCaseNoSuchElement = True
            self.stock = False
            self.product_title = "Not Found."
            self.product_price_value = "Not applicable."
            self.product_seller_information = "Not applicable."


class Amazon(ECommerceList):

    def __init__(self):
        self.i = 1
        super(Amazon, self).__init__()

    def find_item(self, upc):
        try:
            search_box = self.driver.find_element_by_id("twotabsearchtextbox")
            search_box.clear()
            search_box.send_keys(upc)
            search_icon = self.driver.find_element_by_class_name("nav-input")
            search_icon.click()
            product = self.driver.find_element_by_class_name("s-image")
            product.click()
            product_description = self.driver.find_element_by_id("productTitle")
            product_price = self.driver.find_element_by_id("price_inside_buybox")
            product_seller = self.driver.find_element_by_id("merchant-info")

            self.product_title = product_description.text
            self.product_price_value = eval(product_price.text[1:])
            self.product_seller_information = product_seller.text

            self.stock = True
            print(self.product_title)
            print(product_price.text)
            print(self.product_seller_information)

        except NoSuchElementException:
            print("A product satisfying the upc is not found.")
            self.product_title = "Not Found"
            self.product_price_value = "Not applicable"
            self.product_seller_information = "Not applicable"
            self.stock = False
            ActionToRunInCaseNoSuchElement = True
