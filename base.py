from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from pathlib import Path
import subprocess
import time
import pickle
from datetime import datetime

class Base:
    
    def __init__(self):
        super().__init__()
        self.current_dir = Path(__file__).parent.absolute()
        self.driver_pkl_file_path = self.current_dir / "driver_path.pkl"
        self.cookies_pkl_file_path = self.current_dir / "cookies.pkl"
        
    def launch_chrome(self, 
                      headless = False, 
                      ignore_notifs = False):
        
        """
        Launches a chrome browser.
        """
        # Set Chrome Options
        chrome_options = Options()

        if headless:
            chrome_options.add_argument("--no-sandbox") # linux only
            chrome_options.add_argument("--headless")
        
        if ignore_notifs:
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("start-maximized")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_experimental_option("prefs", {
                "profile.default_content_setting_values.notifications": 2 
            })
        
        # Initialize Driver
        self.driver = webdriver.Chrome(self.driver_path, options = chrome_options)

    def find_element(self, x_path):
        """
        Returns the element if it exists. If it does not exist, it waits 2 seconds and tries again.
        """
        if self.exists_by_xpath(x_path):
            return self.driver.find_element_by_xpath(x_path)
        else:
            time.sleep(2)
            return self.driver.find_element_by_xpath(x_path)

    def exists_by_xpath(self, x_path):
        """Returns bool on if the element given exists"""
        try:
            self.driver.find_element_by_xpath(x_path)
        except NoSuchElementException:
            return False
        return True

    def open(self, url):
        url = self.base_url + url
        self.driver.get(url)

    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url

    def hover(self, x_path):
        element = self.find_element(x_path)
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()
        
    def find_file(self, file_name):
        command = ['locate'+ ' ' + file_name]
        output = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]
        output = output.decode()
        self.search_results = output.split('\n')
        return self.search_results

    def save_driver_path(self):
        """Saves the driver path string object as a pkl file."""
        print("Trying to find the path to your chromedriver. See the list below:")
        try:
            self.find_file('chromedriver')
            for path in self.search_results:
                print(path)
        except:
            print('Search function to find a chromedriver on your system failed. This search only works on linux.')
        self.driver_path = input("What is the path to your chromedriver?\n")
        pickle.dump( self.driver_path , open(self.driver_pkl_file_path,"wb"))

    def load_driver_path(self):
        """Loads the driver path string object from the pkl file."""
        self.driver_path = pickle.load(open(self.driver_pkl_file_path, "rb"))
        
    def save_cookies(self,):
        """Saves the current cookies. Use this after you log in for the first time."""
        pickle.dump( self.driver.get_cookies() , open(self.cookies_pkl_file_path,"wb"))

    def load_cookies(self):
        """Loads cookies from the pickle cookies file. Browser needs to exist already"""
        print("Logging in to Google.")
        self.open("")
        cookies = pickle.load(open(self.cookies_pkl_file_path, "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.open("")
        print("Logged in.")

    def current_time(self):
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def quit(self):
        self.driver.quit()
        
    def print_update(self):
        print(f"{self.current_time()} |  Sleeping.", end="\r", flush=True)