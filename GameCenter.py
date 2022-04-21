import logging

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import  QMainWindow

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')

class GameCenter(QMainWindow):
    baseUrl = "https://wan.ludashi.com/"
    loginUrl = "https://wan.ludashi.com/account/index"
    gamePage = "http://wan.ludashi.com/yeyou/cjzg"
    serverArea = 789
    loginStatus = False
    ckCode = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.info(args)
        self.setWindowTitle('夜莺辅助')
        self.setWindowIcon(QIcon("extend/images/title.jpeg"))
        self.browser_init()

    def browser_init(self):
      self.browser = QWebEngineView()
      self.browser.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
      self.browser.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
      self.browser.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
      self.setCentralWidget(self.browser)
      self.showMaximized()
      # 指定打开界面的 URL
      self.browser.setUrl(QUrl(self.loginUrl))
      self.browser.page().loadFinished.connect(self.autoLogin)
      # 让浏览器相应url地址的变化
      self.browser.urlChanged.connect(self.opendGame)



    def autoLogin(self):
        if self.loginStatus == 1 :
            return
        userName = "13437176465"
        passWord = "Ding1990"
        # userName = "smpyxy01"
        # passWord = "123123"
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
                '''.format(un=userName, pwd=passWord)
        self.browser.page().runJavaScript(js_function, self.login_callback)

    def login_callback(self, result):
        if result == 'success':
            print("登录成功!")
            self.loginStatus = True
            self.checkCaptchaCode()
        else:
            print("登录失败！", result)

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
        print("获取验证码", result)
        if result == "faild" :
            self.checkCaptchaCode()
        else:
            return

    def opendGame(self, qurl):
        # 将当前网页的链接更新到地址栏
        urlStr = qurl.toString()
        print(urlStr)
        if urlStr == self.baseUrl:
            self.ckCode = True
            gameUrl = "{0}?s={1}".format(self.gamePage, self.serverArea)
            print("进入游戏页面")
            self.browser.page().load(QUrl(gameUrl))
        elif urlStr.find(self.gamePage) >= 0:
            print("play game")
