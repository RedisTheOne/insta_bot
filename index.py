from selenium import webdriver
from time import sleep
from getpass import getpass

class InstaBot:
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome()
        self.driver.get("https://instagram.com")
        self.username = username
        self.pw = pw
        self.follwers = 0
        self.following = 0
        self.difference = 0
        self.followers_array = []
        self.following_array = []
        self.not_following = []
        sleep(2)

    def log_in(self):
        print("Logging in, pelase wait...")
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input').send_keys(self.username)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input').send_keys(self.pw)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[4]/button').click()
        sleep(4)
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]').click()

    def scroll_down(self):
        articles = self.driver.find_elements_by_class_name("_9AhH0")
        print(len(articles))

    def go_to_profile(self):
        self.driver.find_element_by_xpath("//a[contains(@href, '/{}')]".format(self.username)).click()
        sleep(2)
        follower_a = self.driver.find_element_by_xpath("//a[contains(@href, '/{}/followers')]".format(self.username))
        follower_span = follower_a.find_element_by_tag_name("span")
        self.followers = follower_span.get_attribute("title")
        following_a = self.driver.find_element_by_xpath("//a[contains(@href, '/{}/following')]".format(self.username))
        following_span = following_a.find_element_by_tag_name("span")
        self.following = following_span.get_attribute("innerHTML")
        self.difference = int(self.followers) - int(self.following)

    def get_followers_as_elements(self):
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href, '/{}/followers')]".format(self.username)).click()
        sleep(2)
        scroll_box = self.driver.find_element_by_xpath('/html/body/div[4]/div')
        elements = scroll_box.find_elements_by_xpath("//a[contains(@class, '_0imsa')]")
        self.driver.find_element_by_class_name("isgrP").click()
        print("Getting the followers...")
        while len(elements) < int(self.followers):
            self.driver.execute_script("document.querySelector('.isgrP').scrollTop += 250")
            elements = scroll_box.find_elements_by_xpath("//a[contains(@class, '_0imsa')]")
        print("Processing the followers...")
        for element in elements:
            if element.get_attribute("title") is not '':
                self.followers_array.append(element.get_attribute("title"))
        print("Got the followers!\n")
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/button').click()
    
    def get_unfollowers_as_elements(self):
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href, '/{}/following')]".format(self.username)).click()
        sleep(2)
        scroll_box = self.driver.find_element_by_xpath('/html/body/div[4]/div')
        elements = scroll_box.find_elements_by_xpath("//a[contains(@class, '_0imsa')]")
        self.driver.find_element_by_class_name("isgrP").click()
        print("Getting the following...")
        while len(elements) < int(self.following):
            self.driver.execute_script("document.querySelector('.isgrP').scrollTop += 250")
            elements = scroll_box.find_elements_by_xpath("//a[contains(@class, '_0imsa')]")
        print("Processing the following...")
        for element in elements:
            if element.get_attribute("title") is not '':
                self.following_array.append(element.get_attribute("title"))
        print("Got the following!\n")
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/button').click()

    def get_mean_people(self):
        print("Processing the mean people:")
        self.not_following = [user for user in self.following_array if user not in self.followers_array]
        print("People that you follow but don't follow you back:\n")
        print(self.not_following)

username = input("Username: ")
password = getpass()
try:
    my_bot = InstaBot(username, password)
    my_bot.log_in()
    sleep(2)
    my_bot.go_to_profile()
    my_bot.get_followers_as_elements()
    my_bot.get_unfollowers_as_elements()
    my_bot.get_mean_people()
except:
    print("Error occured, make sure you enter a valid username and password!")