import os
import sys
import json

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl, QFileInfo
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMainWindow



class MainWindow(QMainWindow):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setWindowTitle('夜莺辅助')
    self.setWindowIcon(QIcon("extend/images/title.jpeg"))
    self.resize(1300, 700)
    self.browser_init()

  def browser_init(self):
      self.webview = WebEngineView(self)
      self.webview.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
      self.webview.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
      self.webview.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
      self.webview.load(QUrl(QFileInfo("extend/start.html").absoluteFilePath()))
      self.saveconfBtn = QPushButton("保存配置")
      self.saveconfBtn.clicked.connect(self.saveconf)
      self.playGameBtn = QPushButton("启动游戏")
      self.playGameBtn.clicked.connect(self.startSelectGame)

      main_frame = QWidget()
      layout = QVBoxLayout(self)
      layout.addWidget(self.saveconfBtn)
      layout.addWidget(self.playGameBtn)
      layout.addWidget(self.webview)
      main_frame.setLayout(layout)
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
            self.gameExePath = os.getcwd()+"\\dist\Game.exe"
            print(self.gameExePath)
            self.process = QtCore.QProcess()
            self.process.start(self.gameExePath)

  def playGame(self):
      try:
        print("")
      except Exception as e:
        print(e)


class WebEngineView(QWebEngineView):
    windowList = []
    def createWindow(self, QWebEnginePage_WebWindowType):
        new_webview = WebEngineView()
        new_window = MainWindow()
        new_window.setCentralWidget(new_webview)
        new_window.show()
        self.windowList.append(new_window)  # 注：没有这句会崩溃！！！
        return new_webview

if __name__ == "__main__":
    argvs = sys.argv
    app = QApplication(argvs)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())