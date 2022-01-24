import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
  loginTime = 0
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setWindowTitle('夜莺辅助')
    self.setWindowIcon(QIcon("extend/images/title.jpeg"))
    self.showMaximized()
    self.webview = WebEngineView(self)
    self.webview.settings().setAttribute(QWebEngineSettings.PluginsEnabled,True)
    self.webview.settings().setAttribute(QWebEngineSettings.JavascriptEnabled,True)
    self.webview.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled,True)
    self.setCentralWidget(self.webview)
    self.webview.page().load(QUrl("https://wan.ludashi.com"))
    self.webview.loadFinished.connect(self.autoLogin)

    self.webview.page().load(QUrl(
      "http://wan.ludashi.com/yeyou/cjzg?sub=default&s=1382&needfancy=0&channel=newsweb&from=allgame_cjzg"))

  def autoLogin(self):
      userName = "smpyxy01"
      passWord = "123123"
      js_function = '''
          function autoLogin()
          {{
              var usernameInput = document.getElementsByName("username")[0];
              var passwordInput = document.getElementsByName("password")[0];
              if(usernameInput == undefined){{
                return "faild"
              }}
              else{{
               usernameInput.value="{un}";
               passwordInput.value="{pwd}";
               var loginSubmit = document.getElementById("loginSubmit");
               loginSubmit.click();
                return "success"
              }}
          }}
          autoLogin();
          '''.format(un=userName, pwd=passWord)
      self.webview.page().runJavaScript(js_function,self.auto_callback)

  def auto_callback(self,result):
      if(self.loginTime<5):
          if result == 'faild':
            self.webview.loadFinished.connect(self.autoLogin)
          else: #登录成功,进入游戏页面
            self.loginTime += 1
      else:
          print(result)

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