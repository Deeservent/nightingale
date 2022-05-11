import time
import pyautogui

def main():
    working = True

    while working == True:
        time.sleep(2)
        print("休眠结束")
        location = pyautogui.locateOnWindow('extend/point/cjzg/TLGQT/1.bmp','夜莺辅助-792',grayscale=True,confidence=0.2)
        print(location)
        if location is not None:
            working = False
            pyautogui.click(location)




if __name__ == '__main__':
    main()