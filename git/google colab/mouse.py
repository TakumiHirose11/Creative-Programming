import time
import pyautogui as pgui

for _ in range(72):
    pgui.position()
    time.sleep(600) # 10分待機
    pgui.click(x=1000, y=1000, duration=1) # 指定した座標に1秒かけて移動してクリック
    time.sleep(600) # 1秒待機
    pgui.click(x=1200, y=1000, duration=1)