import sys
import json

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl, QFileInfo
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMainWindow

from GameCenter import GameCenter


class MainWindow(QMainWindow):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setWindowTitle('夜莺辅助')
    self.setWindowIcon(QIcon("extend/images/title.jpeg"))
    self.browser_init()

  def browser_init(self):
      self.webview = WebEngineView(self)
      self.webview.load(QUrl(QFileInfo("extend/start.html").absoluteFilePath()))
      self.saveconfBtn = QPushButton("保存配置")
      self.saveconfBtn.clicked.connect(self.saveconf)
      self.playGameBtn = QPushButton("启动游戏")
      self.playGameBtn.clicked.connect(self.startSelectGame)
      main_frame = QWidget()
      layout = QVBoxLayout(main_frame)
      layout.addWidget(self.saveconfBtn)
      layout.addWidget(self.playGameBtn)
      layout.addWidget(self.webview)
      self.setCentralWidget(main_frame)



  def saveconf(self):
      value = "saveconf"
      self.webview.page().runJavaScript('saveconf("' + value + '");',self.saveconf_callback)

  def saveconf_callback(self, result):
      jsonStr = json.dumps(result,ensure_ascii=False)
      print(jsonStr)
      with open('extend/data/conf.json', 'w') as conf:
          json.dump(result, conf)

  def startSelectGame(self):
      value = "startSelectGame"
      self.webview.page().runJavaScript('getSelectRows("' + value + '");',self.startSelectGame_callback)

  def startSelectGame_callback(self, result):
      if result is None:
          print("请选择账号")
      else:
          for acount in result:
            username = acount["accout"]
            password = acount["password"]
            print(username,password)
            self.gameweb = GameCenter()
            self.gameweb.start_game(username,password)



class WebEngineView(QWebEngineView):
    windowList = []
    def createWindow(self, QWebEnginePage_WebWindowType):
        new_webview = WebEngineView()
        new_webview.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        new_webview.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        new_webview.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        new_window = MainWindow()
        new_window.setCentralWidget(new_webview)
        new_window.showMaximized()
        self.windowList.append(new_window)  # 注：没有这句会崩溃！！！
        return new_webview

if __name__ == "__main__":
    argvs = sys.argv
    app = QApplication(argvs)
    mainWin = MainWindow()
    mainWin.showMaximized()
    sys.exit(app.exec_())