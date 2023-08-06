# -*- coding = UTF-8 -*-
# Author   :buxiubuzhi
# File     : cli.py
# project  : UIAutoProject
# time     : 2020/12/14 16:39
# Describe : 
# ---------------------------------------

import argparse
import os, sys
from lazyTest import __version__, __description__

PY3 = sys.version_info[0] == 3


def main():
    """
    API test: parse command line options and run commands.
    """

    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        '-v', '--version', dest='version', action='store_true',
        help="show version")

    parser.add_argument(
        '--project',
        help="Create an lazyTest automation test project.")

    parser.add_argument(
        '-r',
        help="run test case")

    args = parser.parse_args()

    # 获取版本
    if args.version:
        print("version {}".format(__version__))
        return 0

    # 创建项目
    project_name = args.project
    if project_name:
        create_scaffold(project_name)
        return 0

    # 运行用例
    run_file = args.r
    if run_file:
        if PY3:
            ret = os.system("python -V")
            if ret != 0:
                os.system("python3 -V")
                command = "python3 " + run_file
            else:
                command = "python " + run_file
        else:
            raise NameError("Does not support python2")
        os.system(command)
        return 0


def create_scaffold(project_name):
    """
    create scaffold with specified project name.
    """
    if os.path.isdir(project_name):
        print("{}:Not a directory".format(project_name))
        return

    def create_folder(path):
        print("create dir:{}".format(path))
        os.makedirs(path)

    def create_file(path, file_content=""):
        print("create file:{}".format(path))
        with open(path, 'w', encoding='utf-8') as f:
            f.write(file_content)

    # ----------------------------------------------
    conftest = """
# -*- coding = UTF-8 -*-
# Author   :buxiubuzhi
# File     : conftest.py
# time     : 
# Describe :
# ---------------------------------------
import os
import sys
import time

import allure
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lazyTest import *

globals()["driver"] = None


def pytest_addoption(parser):
    # 添加参数到pytest.ini
    parser.addini('Terminal', help='访问浏览器参数')
    parser.addini('URL', help='添加 url 访问地址参数')
    parser.addini('filepath', help='添加 截图路径')
    parser.addini('logpath', help='添加 日志路径')


@pytest.fixture(scope='session')
def getdriver(pytestconfig):
    Terminal = pytestconfig.getini("Terminal")
    URL = pytestconfig.getini("URL")
    driver = browser_Config(Terminal, URL)
    globals()["driver"] = driver.base_driver
    yield driver
    driver.browser_close()


@pytest.fixture(scope="function")
def flush_browser(getdriver):
    yield
    getdriver.flush_browser()
    getdriver.sleep(1)


# 用例出现异常或失败时截图
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    config = item.config
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call':
        xfail = hasattr(report, 'wasxfail')
        if report.failed and not xfail:
            project = str(config.rootpath)
            filepath = config.getini("filepath")
            picture_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
            filename = project + filepath + picture_time + ".png"
            globals()["driver"].save_screenshot(filename)
            with open(filename, "rb") as f:
                file = f.read()
                allure.attach(file, "失败截图", allure.attachment_type.PNG)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_setup(item):
    config = item.config
    project = str(config.rootpath)
    logpath = config.getini("logpath")
    logging_plugin = config.pluginmanager.get_plugin("logging-plugin")
    logging_plugin.set_log_path(project + logpath)
    yield

    """

    pytest = """
[pytest]


log_cli = true
log_cli_level = INFO
log_format = %(levelname)s %(asctime)s [%(filename)s:%(lineno)-s] %(message)s
log_date_format = %Y-%M-%D %H:%M:%S



log_file_level = INFO
log_file_format = %(levelname)s %(asctime)s [%(filename)s:%(lineno)-s] %(message)s
log_file_date_format = %Y-%M-%D %H:%M:%S


Terminal = ChromeOptions
URL = 
filepath = /result/screenshot/
logpath = /result/log/log.log
    """

    main = """
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lazyTest import ClearTestResult


def getPorjectPath():
    '''
    获取项目路径
    '''
    return os.path.dirname(os.path.dirname(__file__))


def clearLogAndReport():
    print("----------清空上次测试结果----------")
    path = getPorjectPath() + "/result"
    ClearTestResult(path)
    time.sleep(2)
    print("----------测试结果清空成功----------")


def runlastFailed():
    print("启动失败用例重跑")
    cmd = "pytest -s --lf {}/case --alluredir {}/result/report".format(getPorjectPath(), getPorjectPath())
    print(os.system(cmd))


def startReport():
    print("-------------启动测试报告--------------")
    cmd = "allure serve {}/result/report".format(getPorjectPath())
    print(os.system(cmd))


def startCase(cases):
    print("------------开始执行测试------------")
    cmd = "pytest -s {}/case/{} --alluredir {}/result/report".format(getPorjectPath(), cases, getPorjectPath())
    print(os.system(cmd))


def run(cases=" "):
    clearLogAndReport()
    startCase(cases)
    s = input("请选择要启用的服务:1:启动失败用例重跑;\t2：启动测试报告;")
    if s == "1":
        runlastFailed()
        s = input("是否启动测试报告:y/n")
    if s == "2" or s == "y":
        startReport()


run()
    """
    # ----------------------------------------------
    RegisterCase = """
# -*- coding = UTF-8 -*-
# Author   :buxiubuzhi
# File     :test_RegisterCase.py
# time     :2020/11/28  14:55
# Describe : 注册的测试用例
# ---------------------------------------
import allure
import pytest

import lazyTest
from service.RegisterService import RegisterService


class TestRegister(lazyTest.TestCase):

    @pytest.fixture(scope="function")
    def setUp(self, getdriver, flush_browser):
        self.reg = RegisterService(getdriver)

    @allure.title("用户注册")
    def testRegister(self, setUp):
        account = lazyTest.createData("account{}")
        result = self.reg.userRegister(account, account, "123456", "123456", "问题", "答案")
        assert result == "注册成功,快去登录吧！"
    """

    RegisterService = """
# -*- coding = UTF-8 -*-
# Autohr   :buxiubuzhi
# File     :RegisterService.py
# time     :2020/11/28  14:46
# Describe : 注册流程
# ---------------------------------------
import allure

from pages.RegisterPage import RegisterPage


@allure.feature("注册业务")
class RegisterService:

    def __init__(self, driver):
        self.r = RegisterPage(driver)

    @allure.story("用户注册")
    def userRegister(self, account, username, password, repassword, issue, answer):
        self.r.getRegisterPage()
        self.r.inputAccount(account)
        self.r.inputUsername(username)
        self.r.inputPassword(password)
        self.r.inputRepassword(repassword)
        self.r.inputIssue(issue)
        self.r.inputAnswer(answer)
        self.r.clickSubmit()
        return self.reg.getalertText()
    """

    RegisterPage = """
# -*- coding = UTF-8 -*-
# Autohr   :buxiubuzhi
# File     :RegisterPage.py
# time     :2020/11/28  14:36
# Describe : 注册页面
# ---------------------------------------
import os

import allure
import lazyTest



class RegisterPage(lazyTest.Page):

    def getProjectPath(self) -> str:
        return os.path.dirname(os.path.dirname(__file__))

    @lazyTest.Sleep()
    @allure.step("进入注册页面")
    def getRegisterPage(self):
        self.log.info("进入注册页面")
        self.base_driver.get(self.selector["REGISTER"])

    @lazyTest.Sleep()
    @allure.step("输入账号:{account}")
    def inputAccount(self, account):
        self.log.info("输入账号：%s" % account)
        self.base_driver.element_clear_input(self.selector["ACCOUNT"], account)

    @lazyTest.Sleep()
    @allure.step("输入用户名:{username}")
    def inputUsername(self, username):
        self.log.info("输入用户名：%s" % username)
        self.base_driver.element_clear_input(self.selector["USERNAME"], username)

    @lazyTest.Sleep()
    @allure.step("输入密码:{password}")
    def inputPassword(self, password):
        self.log.info("输入密码：%s" % password)
        self.base_driver.element_clear_input(self.selector["PASSWORD"], password)

    @lazyTest.Sleep()
    @allure.step("在次输入密码:{repassword}")
    def inputRepassword(self, repassword):
        self.log.info("在次输入密码：%s" % repassword)
        self.base_driver.element_clear_input(self.selector["REPASSWORD"], repassword)

    @lazyTest.Sleep()
    @allure.step("输入安全问题:{issue}")
    def inputIssue(self, issue):
        self.log.info("输入安全问题：%s" % issue)
        self.base_driver.element_clear_input(self.selector["ISSUE"], issue)

    @lazyTest.Sleep()
    @allure.step("输入答案:{answer}")
    def inputAnswer(self, answer):
        self.log.info("输入答案：%s" % answer)
        self.base_driver.element_clear_input(self.selector["ANSWER"], answer)

    @lazyTest.Sleep()
    @allure.step("点击提交")
    def clickSubmit(self):
        self.log.info("点击提交")
        self.base_driver.element_click(self.selector["SUBMIT"])

    @lazyTest.Sleep()
    @allure.step("获取注册后的弹窗文本")
    def getalertText(self):
        text = self.base_driver.getAlertText()
        self.log.info("弹窗的文本：%s" % text)
        return text
    """

    RegisterPageyaml = """
REGISTER: /view/register.html
ACCOUNT: x,//*[@id="account"]/input
USERNAME: x,/html/body/div/div/div/form/div[2]/input
PASSWORD: x,/html/body/div/div/div/form/div[3]/input
REPASSWORD: x,/html/body/div/div/div/form/div[4]/input
ISSUE: x,/html/body/div/div/div/form/div[5]/input
ANSWER: x,/html/body/div/div/div/form/div[6]/input
SUBMIT: x,/html/body/div/div/div/form/div[7]/button
    """
    # ----------------------------------------------

    create_folder(project_name)  # 创建项目目录
    # 创建目录结构
    create_folder(os.path.join(project_name, "pages"))
    create_folder(os.path.join(project_name, "service"))
    create_folder(os.path.join(project_name, "case"))
    create_folder(os.path.join(project_name, "main"))
    create_folder(os.path.join(project_name, "result"))
    create_folder(os.path.join(project_name, "result", "log"))
    create_folder(os.path.join(project_name, "result", "report"))
    create_folder(os.path.join(project_name, "result", "screenshot"))
    create_folder(os.path.join(project_name, "resources"))
    create_folder(os.path.join(project_name, "resources", "element"))
    # 创建核心文件
    create_file(os.path.join(project_name, "__init__.py"))
    create_file(os.path.join(project_name, "case", "conftest.py"), conftest)
    create_file(os.path.join(project_name, "pytest.ini"), pytest)
    create_file(os.path.join(project_name, "main", "main.py"), main)
    # 创建demo文件
    create_file(os.path.join(project_name, "case", "test_RegisterCase.py"), RegisterCase)
    create_file(os.path.join(project_name, "service", "RegisterService.py"), RegisterService)
    create_file(os.path.join(project_name, "pages", "RegisterPage.py"), RegisterPage)
    create_file(os.path.join(project_name, "resources","element","RegisterPage.yaml"), RegisterPageyaml)


if __name__ == '__main__':
    main()

