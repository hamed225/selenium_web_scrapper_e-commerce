#e-commerce using selenium by enetering upc number for the product.
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
from time import strftime
import os


class ECommerceList(object):
    # parent class for the e-commerce  websites

    def __init__(self):
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

        """Used to open thw website using selenium driver.
            This function will be inherited by child classes."""

        # i is passed from child classes to make sure correct site is loaded from the self.stores dictionary

        self.driver.get(self.store_url_list[self.i])
        assert self.store_name_list[self.i] in self.driver.title

    def write_to_RFile(self, the_upc, file_name="flask_price_finder.txt"):

        """Used to open a '.txt' file and save the required items on the the txt file by default it
                creates 'flask_price_finder.txt'
                This function will be inherited by child classes."""

        # the lines wriiten to the file.
        lines_to_write = ["\n\nCurrent time:{0}".format(self.now),
                          "\nStore: {0}".format(self.store_name_list[self.i]),
                          "\nProduct Title: {0}".format(self.product_title),
                          "\nProduct Price: {0}".format(self.product_price_value),
                          "\nIndividual seller: {0}".format(self.product_seller_information),
                          "\nInStock: {0}".format(self.stock),
                          "\nurl: {0}".format(self.driver.current_url)]
        with open(file_name, "a") as RFile:
            if os.stat(file_name).st_size == 0:
                # checking if the file has already been created, if
                # not it writes the upc to the top of the file
                RFile.write("For the upc:{0} ".format(the_upc))
                RFile.writelines(lines_to_write)
            else:
                RFile.writelines(lines_to_write)
            self.driver.close()


class BestBuy(ECommerceList):

    """Child class inheriting the functions of parent class"""

    def __init__(self):
        self.i = 0
        # i is the value passed to parent class to make sure the correct site is loaded.
        # This is required for all child classes if additional child classes are made
        super(BestBuy, self).__init__()

    def find_item(self, upc):

        """Function which finds the particular item from the e-commerce website.
            The selenium code goes here. It also requires a upc number as its parameter."""

        try:
            try:
                search_box = self.driver.find_element_by_id("gh-search-input")
            except ElementNotInteractableException:
                print("subscription_cancel_button found.")
                self.action = ActionChains(self.driver)
                self.action.find_element_by_css_selector("#modal894 > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > button:nth-child(1)")
                self.action.click()
                self.action.perform()
            else:
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
                    pass

                    try:
                        product_stock = self.driver.find_element_by_class_name("button-state-sold-out")
                        self.stock = False
                        print("Out of stock.")

                    except NoSuchElementException:
                        pass

        except NoSuchElementException:
            print("A product satisfying the upc is not found.")
            ActionToRunInCaseNoSuchElement = True
            self.stock = False
            self.product_title = "Not Found."
            self.product_price_value = "Not applicable."
            self.product_seller_information = "Not applicable."


class Amazon(ECommerceList):

    """Child class inheriting the functions of parent class"""

    def __init__(self):
        # i is the value passed to parent class to make sure the correct site is loaded.
        # This is required for all child classes if additional child classes are made
        self.i = 1
        super(Amazon, self).__init__()

    def find_item(self, upc):
        try:

            """Function which finds the particular item from the e-commerce website.
                The selenium code goes here. It also requires a upc number as its parameter."""

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
            pass
