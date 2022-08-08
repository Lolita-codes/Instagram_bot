import time
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv
load_dotenv('.env')

RANDOM_ACCOUNT = os.environ['SIMILAR_ACCOUNT']
USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']
CHROME_DRIVER_PATH = os.environ['CHROME_DRIVER_PATH']


class InstaFollower:
    #Creates the Selenium driver
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

    # Automatically log in to Instagram
    def login(self):
        self.driver.get('https://www.instagram.com/accounts/login/')
        time.sleep(5)
        email = self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
        email.send_keys(USERNAME)
        password = self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')
        password.send_keys(PASSWORD)
        log_in = self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]').click()

    #
    def find_followers(self):
        time.sleep(5)
        # Goes to the target account with the URL being the name of the Instagram account added to the end of instagram.com
        self.driver.get(f'https://www.instagram.com/{RANDOM_ACCOUNT}/')
        time.sleep(5)

        # Clicks on the follower count to see all their followers
        followers = self.driver.find_element(By.CSS_SELECTOR, 'section main div ul li:nth-child(2) a div').click()
        time.sleep(5)

        #  The list of followers in the popup is limited to around 15 when it first loads, so in order to see more followers, we need to scroll down in the popup
        pop_up = self.driver.find_element(By.CSS_SELECTOR, 'div div div div div._aano')
        for i in range(2):
            time.sleep(1)
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pop_up)
            time.sleep(3)

    # Finds all the follow buttons in the popup and clicks on each of them in turn
    def follow(self):
        follow = self.driver.find_elements(By.CSS_SELECTOR, 'div div div div._aaes button')
        for i in follow:
            try:
                i.click()
                time.sleep(1)

            # In case of an account already been followed, cancels the option to unfollow
            except ElementClickInterceptedException:
                self.driver.find_element(By.LINK_TEXT, 'Cancel').click()

    # Goes to own account and automatically unfollows accounts you're following
    def unfollow(self):
        time.sleep(5)
        self.driver.get(f'https://www.instagram.com/{USERNAME}/')
        time.sleep(5)
        following = self.driver.find_element(By.CSS_SELECTOR, 'main div ul li:nth-child(3) a').click()
        time.sleep(5)
        pop_up = self.driver.find_element(By.CSS_SELECTOR, 'div div div div div._aano')
        for i in range(2):
            time.sleep(1)
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pop_up)
            time.sleep(3)
        unfollow = self.driver.find_elements(By.CSS_SELECTOR, 'div div._aaes button')
        for i in unfollow:
            i.click()
            confirm = self.driver.find_element(By.CSS_SELECTOR, 'div div div div._a9-z button._a9--._a9-_').click()
            time.sleep(1)

# Calls to execute the commands
automate = InstaFollower()
automate.login()
#automate.find_followers()
#automate.follow()
automate.unfollow()