#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import traceback
import time
import os
import datetime


# inp = html.xpath("//*[contains(@%s, '%s')]" % (rule, num))


class BasePage:
    def __init__(self, driver_path: str, is_maximize_window: bool = True):
        self.driver = webdriver.Chrome(driver_path)
        if is_maximize_window:
            self.driver.maximize_window()

    # 对查找单个页面元素进行封装。
    def find_element(self, by: str, locator: str):
        by = by.lower()
        element = None
        if by in ['id', 'name', 'xpath', 'class', 'tag', 'link', 'plink']:
            try:
                if by == 'id':
                    element = self.driver.find_element_by_id(locator)
                elif by == 'name':
                    element = self.driver.find_element_by_name(locator)
                elif by == 'xpath':
                    element = self.driver.find_element_by_xpath(locator)
                elif by == 'class':
                    element = self.driver.find_element_by_class_name(locator)
                elif by == 'tag':
                    element = self.driver.find_element_by_tag_name(locator)
                elif by == 'link':
                    element = self.driver.find_element_by_link_text(locator)
                elif by == 'plink':
                    element = self.driver.find_element_by_partial_link_text(locator)
                else:
                    print('Not find the element "{}"!'.format(locator))
                return element
            except NoSuchElementException as e:
                print(traceback.print_exc())
        else:
            print('Provided a wrong locator "{}"!'.format(locator))

    # 对查找多个页面元素进行封装。
    def find_elements(self, by: str, locator: str):
        by = by.lower()
        elements = None
        if by in ['id', 'name', 'xpath', 'class', 'tag', 'link', 'plink']:
            try:
                if by == 'id':
                    elements = self.driver.find_elements_by_id(locator)
                elif by == 'name':
                    elements = self.driver.find_elements_by_name(locator)
                elif by == 'xpath':
                    elements = self.driver.find_elements_by_xpath(locator)
                elif by == 'class':
                    elements = self.driver.find_elements_by_class_name(locator)
                elif by == 'tag':
                    elements = self.driver.find_elements_by_tag_name(locator)
                elif by == 'link':
                    elements = self.driver.find_elements_by_link_text(locator)
                elif by == 'plink':
                    elements = self.driver.find_elements_by_partial_link_text(locator)
                else:
                    print('Not find the element "{}"!'.format(locator))
                return elements
            except NoSuchElementException as e:
                print(traceback.print_exc())
        else:
            print('Provided a wrong locator "{}"!'.format(locator))

    # 点击页面元素
    def click(self, by: str, locator: str):
        element = self.find_element(by, locator)
        element.click()

    # 输入框输入新信息
    def type(self, by: str, locator: str, value: str):
        y = [x for x in value if x != '']
        if len(y) > 0:
            element = self.find_element(by, locator)
            element.clear()
            element.send_keys(value.strip())

    # 下拉菜单通过可见文本进行选择
    def select(self, by: str, locator: str, text: str):
        y = [x for x in text if x != '']
        if len(y) > 0:
            element = self.find_element(by, locator)
            element_element = Select(element)
            element_element.select_by_visible_text(text.strip())

    # 复选按钮勾选时我们需要首先勾掉已选选项
    def uncheck(self, by: str, locator: str, options: str):
        y = [x for x in options if x != '']
        if len(y) > 0:
            elements = self.find_elements(by, locator)
            for element in elements:
                element.click()

    # 选择excel表格所提供的选项进行勾选
    def check(self, by, locator, options):
        y = [x for x in options if x != '']
        if len(y) > 0:
            be_options = options.split(',')
            for option in be_options:
                element = self.find_element(by, locator.format(option.strip()))
                element.click()

    # 根据excel表格提供标题所包含的关键字来决定进行哪种数据操作
    def update(self, title, by, values):
        y = [x for x in values if x != '']
        if len(y) > 0:
            if '_Text' in title:  # 文本框
                field = title.strip().split('_')
                locator = field[0]
                self.type(by, locator, values)
            elif '_Select' in title:  # 下拉列表
                field = title.strip().split('_')
                locator = field[0]
                self.select(by, locator, values)
            elif '_Option' in title:  # 复选按钮
                field = title.strip().split('_')
                locator = field[0]
                self.uncheck('xpath', '//input[@checked="" and contains(@id, "{}__")]'.format(locator), values)
                self.check('id', '%s__{}' % locator, values)
            else:
                print('Please indicate the data type for the title "{}" in Excel!!!'.format(title))
        else:
            pass

    # 登录系统进行封装方便以后重用
    def login_orms(self, url, username, password):
        # driver = webdriver.Firefox(executable_path='D:\\Selenium 3.14\\geckodriver.exe')
        self.driver.delete_all_cookies()
        self.driver.get(url)
        self.driver.maximize_window()
        time.sleep(2)

        self.type('id', 'userName', username)
        self.type('id', 'password', password)
        self.click('id', 'okBtnAnchor')
        time.sleep(2)

    # 登录系统后选择Contract
    def goto_manager_page(self, url, username, password, contract, page):
        self.login_orms(url, username, password)
        time.sleep(2)
        self.click('xpath', "//option[text()='" + contract + " Contract']")  # 通过click也可以对下拉列表进行选择
        time.sleep(2)
        self.click('link', page)
        time.sleep(2)

    def get_screenshot(self, point: str = "_"):
        """
        获取 页面截图
        :param point 保存文件名后缀:
        :return:
        """
        day_str = datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
        base_path = os.path.join(os.path.abspath('.'), "temp_img")
        if not os.path.exists(base_path):
            os.makedirs(base_path, exist_ok=True)
        img_path = os.path.join(base_path, f"{day_str}_{point}_截图_img.jpg")
        print(f"img_path: {img_path}")
        self.driver.get_screenshot_as_file(f"u{img_path}")
        save_screenshot_status = self.driver.save_screenshot(img_path)
        print(f"save_screenshot_status: {save_screenshot_status}")
        print("save_screenshot over!")


if __name__ == '__main__':
    driver_path = r"D:\seleium\chromedriver.exe"
    basepage = BasePage(driver_path=driver_path)
