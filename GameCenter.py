import logging

import pyautogui
from PyQt5.QtCore import QUrl, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import  QMainWindow
import time
import json

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')

class GameCenter(QMainWindow):
    baseUrl = "https://wan.ludashi.com/"
    loginUrl = "https://wan.ludashi.com/account/index"
    gamePage = "http://wan.ludashi.com/yeyou/cjzg"
    repair = "https://www.flash.cn/help/service0.html" #需要修复flash
    serverArea = 789
    loginStatus = False
    ckCode = False
    userName = ""
    passWord = ""
    userInfo = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.info(args)
        self.setWindowTitle('夜莺辅助')
        self.setWindowIcon(QIcon("extend/images/title.jpeg"))

        self.browser = GameWebEngineView(self)
        self.browser.page().profile().cookieStore().deleteAllCookies()
        self.browser.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        self.browser.page().loadFinished.connect(self.autoLogin)
        # 让浏览器相应url地址的变化
        self.browser.urlChanged.connect(self.opendGame)
        self.setCentralWidget(self.browser)
        self.resize(1500, 1000)
        self.show()
        # self.showMaximized()

    def start_game(self,userInfo):
        logging.info("account:{0}".format(userInfo))
        self.userInfo = userInfo
        server = userInfo["server"]
        self.serverArea = int(server)
        self.setWindowTitle('夜莺辅助-{0}'.format(self.serverArea))
        self.browser.setUrl(QUrl(self.loginUrl))  # 指定打开界面的 URL


    def autoLogin(self):
        if self.loginStatus == 1 :
            return
        uname = self.userInfo["accout"]
        pwd =   self.userInfo["password"]
        js_function = '''
                function autoLogin()
                {{
                    var usernameInput = document.getElementsByName("username")[0];
                    var passwordInput = document.getElementsByName("password")[0];
                    var loginSubmit = document.getElementById("loginSubmit");
                    if(loginSubmit == undefined){{
                      return "faild"
                    }}
                    else{{
                      usernameInput.value="{un}";
                      passwordInput.value="{pwd}";
                      loginSubmit.click();
                      return "success"
                    }}
                }}
                autoLogin();
                '''.format(un=uname, pwd=pwd)
        self.browser.page().runJavaScript(js_function, self.login_callback)

    def login_callback(self, result):
        if result == 'success':
            logging.info("登录成功!")
            self.loginStatus = True
            self.checkCaptchaCode()
        else:
            logging.info("登录失败！ {0}".format(result))

    def checkCaptchaCode(self):
        if self.ckCode == 1 :
            return
        js_function = '''
            function getCaptchaCode()
            {
              var captchaCode = document.getElementsByClassName('captcha_img')[0]
              if(captchaCode.children[0] == undefined){{
                  return "faild"
              }}else{{
                  return captchaCode.children[0].src
              }}
            }
            getCaptchaCode();
            '''
        self.browser.page().runJavaScript(js_function, self.ckCaptchaCode_callback)

    def ckCaptchaCode_callback(self, result):
        if result == "faild" :
            self.checkCaptchaCode()
        else:
            logging.info("获取验证码 {0}".format(result))
            return

    def opendGame(self, qurl):
        # 将当前网页的链接更新到地址栏
        urlStr = qurl.toString()
        logging.info(urlStr)
        gameUrl = "{0}?s={1}".format(self.gamePage, self.serverArea)
        if urlStr == self.baseUrl:
            self.ckCode = True
            logging.info("进入游戏页面")
            self.browser.page().load(QUrl(gameUrl))
        elif urlStr.find(self.gamePage) >= 0 or urlStr.find(self.repair) >= 0:
            logging.info("play game")
            self.thread = Worker(self.userInfo)
            self.thread.start()



class Worker(QThread):
    sinOut = pyqtSignal(str)    # 创建一个信号，信号必须在类创建时定义，不能在类创建后作为类的属性动态添加进来

    def __init__(self,gameParam,parent=None):
        super(Worker, self).__init__(parent)
        confName = gameParam["extConf"]
        pyautogui.PAUSE = 0.01
        self.gameConf = None
        self.server = gameParam["server"]
        with open('extend/data/conf/{0}'.format(confName), 'r') as conf:
            self.gameConf = json.load(conf)

    def __del__(self):
        self.working = False
        self.wait()

    def run(self):
        self.sleep(10)
        try:
            winTitle = '夜莺辅助-{0}'.format(self.server)
            for gcf in self.gameConf:
                print(gcf)
                taskName = gcf["taskName"]
                taskProcess = gcf["taskProcess"]
                for task in taskProcess:
                    pointPath = 'extend/point/cjzg/{0}/{1}'.format(taskName,task)
                    logging.info(pointPath)
                    location = None
                    while location is None:
                        location = pyautogui.locateOnWindow(pointPath,winTitle,grayscale=True,confidence=0.2)
                        self.sleep(2)
                        if location is not None:
                            logging.info(location)
                            pyautogui.click(location)
                            pyautogui.cl

        except Exception as e:
            print("except",e)
        # finally:
        #     print("finally")



class GameWebEngineView(QWebEngineView):
    windowList = []
    def createWindow(self, QWebEnginePage_WebWindowType):
        new_webview = GameWebEngineView()
        new_webview.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        new_webview.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        new_webview.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        new_window = GameCenter()
        new_window.setCentralWidget(new_webview)
        new_window.showMaximized()
        # new_window.resize(1300, 700)
        # new_window.show()
        self.windowList.append(new_window)  # 注：没有这句会崩溃！！！
        return new_webview