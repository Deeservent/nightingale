import logging
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEnginePage
from PyQt5.QtWidgets import QApplication, QMainWindow

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')

class MainWindow(QMainWindow):
    ckTime = 0
    loginTime = 0
    loginStatas = False
    ckCaptchaCode = False
    baseUrl = "https://wan.ludashi.com/"
    firstLogin = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.info(args)
        self.setWindowTitle('夜莺辅助')
        self.setWindowIcon(QIcon("extend/images/title.jpeg"))
        self.showMaximized()
        self.webview = WebEngineView(self)
        if self.firstLogin:
            # self.webview.page().profile().cookieStore().deleteAllCookies()
            self.firstLogin = False

        self.webview.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.webview.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.webview.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        self.setCentralWidget(self.webview)
        self.webview.page().load(QUrl(self.baseUrl))
        self.webview.page().loadFinished.connect(self.autoLogin)
        gameUrl = "{0}yeyou/cjzg?sub=default&s=1392".format(self.baseUrl)
        self.webview.page().load(QUrl(gameUrl))
        # self.webview.page().loadFinished.connect(self.checkCaptchaCode)
        # self.webview.page().urlChanged.connect(self.passCheck)

    def autoLogin(self):
        userName = "13437176465"
        passWord = "Ding1990"
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
        self.webview.page().runJavaScript(js_function, self.login_callback)

    def login_callback(self, result):
        print("自动登录", result)
        if self.loginTime > 100 or self.loginStatas:
            print("不在请求")
            return
        if self.loginStatas == 0:
            if result == 'faild':
                self.autoLogin()
                self.loginTime += 1
            elif result == 'success':  # 登录成功,进入游戏页面
                self.loginStatas = True

    def checkCaptchaCode(self):
        print("")
        # checkCaptcha  = CheckCaptcha()
        # checkCaptcha.start()

    def passCheck(self):
        changeUrl = self.webview.page().url().toString()
        print(changeUrl, self.baseUrl)
        if self.ckCaptchaCode:
            return
        if self.baseUrl != changeUrl :
            print("页面跳转")
            self.ckCaptchaCode = True
            gameUrl = "{0}yeyou/cjzg?sub=default&s=1387".format(self.baseUrl)
            self.webview.page().load(QUrl(gameUrl))


class WebEngineView(QWebEngineView):
    windowList = []
    def createWindow(self, QWebEnginePage_WebWindowType):
        new_webview = WebEngineView()
        new_window = MainWindow()
        new_window.setCentralWidget(new_webview)
        new_window.showMaximized()
        self.windowList.append(new_window)
        return new_webview


if __name__ == "__main__":
    argvs = sys.argv
    app = QApplication(argvs)
    mainWin = MainWindow()
    mainWin.showMaximized()
    sys.exit(app.exec_())
