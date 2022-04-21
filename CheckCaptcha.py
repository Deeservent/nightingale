
class CheckCaptcha():
    ckTime = 0
    ckCaptchaCode = False
    baseUrl = "https://wan.ludashi.com/"
    def __init__(self,webview):
        super().__init__()
        self.webview = webview

    def start(self):
        print("start")

    def checkCaptchaCode(self):
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
        self.webview.page().runJavaScript(js_function, self.ckCaptchaCode_callback)

    def ckCaptchaCode_callback(self, result):
        self.passCheck()
        print("获取验证码", result)
        if self.ckTime > 1000:
            print("不在请求")
            return
        if self.ckCaptchaCode == 0:
            if result == 'faild':
                print("登录成功(无验证码),进入游戏页面")
                self.checkCaptchaCode()
                self.ckTime += 1
            else:
                self.ckCaptchaCode = True