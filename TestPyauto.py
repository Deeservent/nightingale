import time
import pyautogui

def main():
    working = True

    while working == True:
        time.sleep(2)
        print("休眠结束")
        location = pyautogui.locateOnWindow('extend/point/cjzg/确定挖矿.bmp', '夜莺辅助-789')
        print(location)
        if location is not None:
            pyautogui.click(location)






if __name__ == '__main__':
    main()