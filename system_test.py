from django.test import LiveServerTestCase, Client
from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
from wechat.models import *
from django.utils import timezone
from django.utils.dateformat import format

class remind_admin_Test(LiveServerTestCase):
    browser = None
    @classmethod
    def setUpClass(cls):
        super(remind_admin_Test,cls).setUpClass()
        cls.browser = webdriver.PhantomJS()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(remind_admin_Test,cls).tearDownClass()


    def test_all_reminds(self):
        remind = Reminds.objects.create(confid="1", info="这是 0", publish_time=timezone.now())
        remind.save()
        self.browser.get('%s%s' % (self.live_server_url, '/a/conf/remindAdmin?confid=1'))

        time.sleep(2)

        box = WebDriverWait(self.browser, 2).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "html"))
        )
        print(box.text)

    def test_create_remind(self):

        remind = Reminds.objects.create(confid="1", info="这是 0", publish_time=timezone.now())
        remind.save()

        self.browser.get('%s%s' % (self.live_server_url, '/a/conf/remindAdmin?confid=1'))

        time.sleep(2)

        createpage_button = self.browser.find_element_by_id('passNav1')
        createpage_button.click()

        write_box = self.browser.find_element_by_id('remindCreated')
        write_box.send_keys("这是 1")

        create_button = self.browser.find_element_by_id('createButton')
        create_button.click()

        listpage_button = self.browser.find_element_by_id('actNav1')
        listpage_button.click()

        box = WebDriverWait(self.browser, 2).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "html"))
        )
        print(box.text)

        self.browser.get('%s%s' % (self.live_server_url, '/a/conf/remindAdmin?confid=1'))

        time.sleep(2)

        createpage_button = self.browser.find_element_by_id('passNav1')
        createpage_button.click()

        write_box = self.browser.find_element_by_id('remindCreated')
        write_box.send_keys("这是 2")

        create_button = self.browser.find_element_by_id('createButton')
        create_button.click()

        listpage_button = self.browser.find_element_by_id('actNav1')
        listpage_button.click()

        box = WebDriverWait(self.browser, 2).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "html"))
        )
        print(box.text)

        self.browser.get('%s%s' % (self.live_server_url, '/a/conf/remindAdmin?confid=1'))

        time.sleep(2)

        box = WebDriverWait(self.browser, 2).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "html"))
        )
        print(box.text)


class check_member_Test(LiveServerTestCase):
    browser = None

    @classmethod
    def setUpClass(cls):
        super(check_member_Test, cls).setUpClass()
        cls.browser = webdriver.PhantomJS()

        test = User()
        test.open_id = "t"
        test.union_id = 'e'
        test.nickname ='s'
        test.headimgurl = 't'
        test.pageNum = 1
        test.pageState = 1
        test.searchWords = 'i'
        test.userid = '1'
        test.save()

        test = User()
        test.open_id = "tt"
        test.union_id = 'ee'
        test.nickname ='s'
        test.headimgurl = 't'
        test.pageNum = 1
        test.pageState = 1
        test.searchWords = 'i'
        test.userid = '2'
        test.save()

        test = User()
        test.open_id = "ttt"
        test.union_id = 'eee'
        test.nickname = 's'
        test.headimgurl = 't'
        test.pageNum = 1
        test.pageState = 1
        test.searchWords = 'i'
        test.userid = '3'
        test.save()

        userinfo = UserSignUpDetail()
        userinfo.user = User.objects.get(userid = '1')
        userinfo.confid = '3'
        userinfo.sex = 1
        userinfo.name ="cc"
        userinfo.telephone = "1"
        userinfo.email ="110"
        userinfo.checked_status =1
        userinfo.signup_time = '2017-1-1 0:0:0'
        userinfo.save()

        userinfo = UserSignUpDetail()
        userinfo.user = User.objects.get(userid='2')
        userinfo.confid = '3'
        userinfo.sex = 1
        userinfo.name = "cc"
        userinfo.telephone = "1"
        userinfo.email = "110"
        userinfo.checked_status = 1
        userinfo.signup_time = '2017-1-1 0:0:0'
        userinfo.save()

        userinfo = UserSignUpDetail()
        userinfo.user = User.objects.get(userid='3')
        userinfo.confid = '3'
        userinfo.sex = 1
        userinfo.name = "cc"
        userinfo.telephone = "1"
        userinfo.email = "110"
        userinfo.checked_status = 0
        userinfo.signup_time = '2017-1-1 0:0:0'
        userinfo.save()

        theParts = ChoosedSignUpParts()
        theParts.confid = 3
        theParts.maxJoinNum = 1000
        theParts.setSignUpParts([])
        theParts.save()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(check_member_Test,cls).tearDownClass()


    def test_all_members(self):
        self.browser.get('%s%s' % (self.live_server_url, '/a/conf/checkMember/?confid=3'))

        time.sleep(2)

        box = WebDriverWait(self.browser, 2).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "html"))
        )
        print(box.text)


class set_module_Test(LiveServerTestCase):
    browser = None

    @classmethod
    def setUpClass(cls):
        super(set_module_Test, cls).setUpClass()
        cls.browser = webdriver.PhantomJS()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(set_module_Test, cls).tearDownClass()

    def test_html(self):
        self.browser.get('%s%s' % (self.live_server_url, '/a/conf/signUpModule/?confid=7'))

        time.sleep(2)

        box = self.browser.find_element_by_id('num')
        box.send_keys("1000")
        button = self.browser.find_element_by_id('place')
        button.click()
        button = self.browser.find_element_by_id('mail')
        button.click()
        button = self.browser.find_element_by_id('company')
        button.click()
        button = self.browser.find_element_by_id('place')
        button.click()
        button = self.browser.find_element_by_id('accomodation')
        button.click()

        #showfeelist_button = self.browser.find_element_by_id('costfee')
        #showfeelist_button.click()

        button = self.browser.find_element_by_id('submitTotal')
        button.click()

        alert = self.browser.switch_to_alert()
        print (alert)
        print("pipipipipipipipipipipipipipipipipipipipipipiip")
        #box = WebDriverWait(self.browser, 2).until(
        #    expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "html"))
        #)
        #print(box.text)



class sign_up_Test(LiveServerTestCase):
    browser = None

    @classmethod
    def setUpClass(cls):
        super(sign_up_Test, cls).setUpClass()
        cls.browser = webdriver.PhantomJS()

        theParts = ChoosedSignUpParts()
        theParts.confid = 7
        theParts.setSignUpParts([1,2,3,4,5,6])
        theParts.maxJoinNum=1000
        theParts.save()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(sign_up_Test, cls).tearDownClass()

    def test_html(self):
        self.browser.get('%s%s' % (self.live_server_url, '/u/user/signUpConf/?confid=7'))

        time.sleep(2)

        box = WebDriverWait(self.browser, 2).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "html"))
        )
        print(box.text)

        box = self.browser.find_element_by_id('name')
        box.send_keys("nihao")
        box = self.browser.find_element_by_id('optionsRadios1')
        box.click()
        box = self.browser.find_element_by_id('phone')
        box.send_keys("123")
        box = self.browser.find_element_by_id('email')
        box.send_keys("123@163.com")
        box = self.browser.find_element_by_id('nextstep1')
        box.click()

        time.sleep(2)

        box = WebDriverWait(self.browser, 2).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "html"))
        )
        print(box.text)

        box = self.browser.find_element_by_id('contryList')
        box.click()

        select = self.browser.find_element_by_tag_name("select")
        allOptions = select.find_elements_by_tag_name("option")
        for option in allOptions:
            if option.get_attribute("value")=="China":
                option.click()
        box = self.browser.find_element_by_id('liveplace')
        box.send_keys("nihao")
        box = self.browser.find_element_by_id('mail')
        box.send_keys("nihao")
        box = self.browser.find_element_by_id('companyname')
        box.send_keys("nihao")
        box = self.browser.find_element_by_id('companyplace')
        box.send_keys("nihao")
        box = self.browser.find_element_by_id('companyduty')
        box.send_keys("nihao")
        box = self.browser.find_element_by_id('optionsRadios3')
        box.click()
        box = self.browser.find_element_by_id('nextstep2')
        box.click()

        time.sleep(2)

        box = WebDriverWait(self.browser, 2).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "html"))
        )
        print(box.text)

        box = self.browser.find_element_by_id('nextstep3')
        box.click()

        time.sleep(2)

        box = WebDriverWait(self.browser, 2).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "html"))
        )
        print(box.text)
