from random import randint
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager


class Scrapping:
    """
    A class used for webscrap web elements using BeautifulSoup and Selenium.
    It's possible to use both or one, but all methods are not perfect and exhaustive

    Attributes
    ----------
    url : str
        page/website url
    page : None | soup
        current page visited
    enable_selenium : bool
        say whether selenium is enabled or not
    options : None | ChromeOptions
        options from webdriver
    driver : None | WebDriver
        control web browser and do actions
    action : None | ActionChains
        perform multiple actions

    Methods
    -------
    open_url(link)
        save link to url attribute, open it and return an _UrlopenRet value
    save_page(reading)
        open link and parse the page
    take_tag(tag, attrs = list or tuple or None)
        find tag and return it, if its an <a> tag href will be returned
    take_tags(tag, attrs = list or tuple or None)
        same as take_tag but with multiple tags
    take_specific_subtag(parent_tag, child_tag)
        find child tag with given parent tag, both must exist
    take_specific_subtags(parent_tag, child_tag)
        same as above but find all children from parent tag
    take_text(the_tag)
        return text inside tag
    store_as(filename, extension, *args)
        save data in file (only .txt or .csv available)
    store_as_txt(path, line)
        save data in .txt file
    store_as_csv(path, column, value)
        save data in .csv file
    """

    def __init__(self, selenium=False):
        self.url = ""
        self.page = None
        self.enable_selenium = selenium
        self.options = None
        self.driver = None
        self.action = None

    def open_url(self, link):
        self.url = link
        data = urlopen(self.url)
        read = data.read()
        data.close()
        return read

    def save_page(self, reading):
        self.page = soup(reading, 'html.parser')

    def take_tag(self, tag, attrs=list or tuple or None):
        res = self.page.find(tag, attrs)
        if tag == "a":
            res = self.page.find(tag, attrs, href=True)
            return res['href']
        return res

    def take_tags(self, tag, attrs=list or tuple or None):
        res = self.page.findAll(tag, attrs)
        if tag == "a":
            href = []
            res = self.page.findAll(tag, attrs, href=True)
            for r in res:
                href.append(r['href'])
            return href
        return res

    def take_specific_subtag(self, parent_tag, child_tag):
        assert parent_tag is not None, "Tag {} not found !".format(parent_tag)
        assert child_tag is not None, "Error, no child tag called {}.".format(
            child_tag)
        if isinstance(parent_tag, (list, tuple)):
            tags = []
            for p_tag in parent_tag:
                tags.append(p_tag.find(child_tag, recursive=False))
            return tags
        else:
            return parent_tag.find(child_tag, recursive=False)

    def take_specific_subtags(self, parent_tag, child_tag):
        assert parent_tag is not None, "Tag {} not found !".format(parent_tag)
        assert child_tag is not None, "Error, no child tag called {}.".format(
            child_tag)
        if isinstance(parent_tag, (list, tuple)):
            tags = []
            for p_tag in parent_tag:
                tags.append(p_tag.findAll(child_tag, recursive=False))
            return tags
        else:
            return parent_tag.findAll(child_tag, recursive=False)

    def tag_text(self, the_tag):
        assert the_tag is not None, "TypeError: {} is a None type.".format(
            the_tag)
        if isinstance(the_tag, (list, tuple)):
            tags = []
            for p_tag in the_tag:
                tags.append(p_tag.getText().replace(
                    "\n", "").replace(r"[(\d)]", ""))
            return tags
        else:
            return the_tag.getText().replace("\n", "").replace(r"[(\d)]", "")

    def load_selenium(self, detach=False, headless=False):
        if self.enable_selenium is True:
            self.options = webdriver.ChromeOptions()
            if detach is True: self.options.add_experimental_option(
                "detach", detach)
            if headless is True: self.options.add_argument("--headless")
            # take browser driver version matching current browser version
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(
                service=service, options=self.options)
            self.action = ActionChains(self.driver)

    def change(self, tool='\0', new_driver=None, new_options=None, new_action=None):
        if(tool == 'driver'):
            if(new_driver is not None):
                self.driver = new_driver
                print("[INFO] : new driver set.")
        elif(tool == 'options'):
            if(new_options is not None):
                self.options = new_options
                print("[INFO] : new options set.")
        elif(tool == 'action'):
            if(new_action is not None):
                self.action = new_action
                print("[INFO] : new action set.")
        else:
            print("[INFO] : no change done.")

    def get_driver(self):
        return self.driver

    def get_options(self):
        return self.options

    def get_action(self):
        return self.action

    def get(self, driver, link):
        driver.get(link)

    def wait(self, duration):
        time.sleep(duration)

    def maximize(self):
        self.driver.maximize_window()

    def minimize(self):
        self.driver.minimize_window()

    def wait_until(self, driver, duration, method, element):
        wait = WebDriverWait(driver, duration)
        response = wait.until(EC.visibility_of_element_located((method, element)))
        return response

    def mute(self, driver):
        self.script(driver, """
           let video = document.querySelector('video')
           video.muted = true
        """)

    def async_script(self, driver, script, response = None):
        driver.execute_async_script(script, response)

    def script(self, driver, script, response = None):
        driver.execute_script(script, response)

    def find(self, driver, method, element, clickable=False, multiple=False, index = 0):
        if multiple is True:
            if clickable is True:
                driver.find_elements(method, element)[index].click()
                return driver
            else:
                return driver.find_elements(method, element)
        else:
            if clickable is True:
                driver.find_element(method, element).click()
                return driver
            else:
                return driver.find_element(method, element)

    def find_input(self, action, driver, method, element, text = str(), *keys):
        result = self.find(driver, method, element)
        action.move_to_element(result).click().perform()
        action.move_to_element(result).send_keys(text, *keys).perform()

    def find_link(self, action, driver, method, element, multiple = False, text = str(), keys = str() or []):
        result = self.find(driver, method, element, multiple=multiple)
        if(isinstance(result, list or tuple or dict or str) is True):
            index = randint(0, len(result) - 1)
            action.move_to_element(result[index]).click().perform()
            if(text or keys):
                action.move_to_element(result[index]).send_keys(text, keys).perform()
        else:
            action.move_to_element(result).click().perform()
            if(text or keys):
                action.move_to_element(result).send_keys(text, keys).perform()

    def open(self, driver, link, option = '_blank'):
        driver.execute_script(f"window.open('{link}','{option}');")

    def get_handles(self, driver):
        return driver.window_handles

    def get_specific_handle(self, driver, index):
        if index >= len(driver.window_handles) or index < -1: print(f"{index} is not valid"), exit(1)
        return driver.window_handles[index]

    def switch(self, driver, index):
        driver.switch_to.window(self.get_specific_handle(driver, index))

    def quit(self, *driver):
        for d in driver:
            d.quit()

    def __str__(self):
        display = "--- Status ---\n"
        if not self.url: display += "[INFO] no url found with urlopen\n"
        else: display += "[INFO] url = {}\n".format(self.url)
        if self.enable_selenium is False:
            display += "[INFO] selenium not used"
        else:
            display += f"[INFO] url found by Selenium : {self.driver.current_url}"
        return display