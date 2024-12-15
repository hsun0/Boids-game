# Boids模擬鳥類群集行為規則

## Note
這不是紙本報告

## Install environment
```
pip install -r requirements.txt
```
## Run
```
python3 main/main.py
```

## 調整參數
一開始進入遊戲時會跳出調整參數的頁面，可以調整各式各樣的參數
<img src="/img/firstSetting.png" alt="firstSetting" style="width:70%;">


在遊玩畫面中也可以隨時按下Tab鍵調整參數，不過不能調整Fish Number 和 Group Number

<img src="/img/setting.png" alt="setting" style="width:70%;">


## 遊玩畫面
<img src="/img/demo.png" alt="demo" style="width:70%;">

<img src="/img/demo2.png" alt="demo2" style="width:70%;">

## 規則簡介
玩家可以控制鯊魚去吃在畫面中移動的小魚、放置障礙物在遊戲畫面中，還可以控制大海中的洋流。

## 按鍵
- 按左鍵提供食物
- WSAD鍵分別控制鯊魚上下左右移動
- E鍵在滑鼠位置方下障礙物
- 空白鍵開關洋流
- 上下左右鍵控制洋流流動方向
- Tab進入設定頁面
- ESC退出