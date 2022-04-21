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
    icenter = "https://wan.ludashi.com/icenter/index"
    serverArea = 789
    loginStatus = False
    ckCode = False
    userName = "13437176465"
    passWord = "Ding1990"

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
        self.showMaximized()
        # self.browser_init()

    def start_game(self,uname,pwd):
      logging.info("account:{0},{1}".format(uname,pwd))
      self.userName = uname
      self.passWord = pwd
      # 指定打开界面的 URL
      self.browser.setUrl(QUrl(self.loginUrl))


    def autoLogin(self):
        if self.loginStatus == 1 :
            return

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
                '''.format(un=self.userName, pwd=self.passWord)
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
        gameUrl = "{0}?s={1}".format(self.gamePage, self.serverArea)
        if urlStr == self.baseUrl:
            self.ckCode = True
            print("进入游戏页面")
            self.browser.page().load(QUrl(gameUrl))
        elif urlStr.find(self.gamePage) >= 0:
            print("play game")
        elif urlStr.find(self.icenter) >= 0:
            print("进入游戏页面")
            self.browser.page().load(QUrl(gameUrl))

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
        self.windowList.append(new_window)  # 注：没有这句会崩溃！！！
        return new_webview