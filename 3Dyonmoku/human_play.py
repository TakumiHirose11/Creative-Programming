# ====================
# 人とAIの対戦
# ====================

# パッケージのインポート
from game import State
from pv_mcts import pv_mcts_action
from tensorflow.keras.models import load_model
from pathlib import Path
from threading import Thread
import tkinter as tk

# ベストプレイヤーのモデルの読み込み
model = load_model('./model/best.h5')

# ゲームUIの定義
class GameUI(tk.Frame):
    # 初期化
    def __init__(self, master=None, model=None):
        tk.Frame.__init__(self, master)
        self.master.title('立体四目並べ')

        # ゲーム状態の生成
        self.state = State()

        # PV MCTSで行動選択を行う関数の生成
        self.next_action = pv_mcts_action(model, 0.0)

        # キャンバスの生成
        self.c = tk.Canvas(self, width = 1400, height = 320, highlightthickness = 0)
        self.c.bind('<Button-1>', self.turn_of_human)
        self.c.pack()

        # 描画の更新
        self.on_draw()

    # 人間のターン
    def turn_of_human(self, event):
        #print("turn of human")
        # ゲーム終了時
        if self.state.is_done():
            print("END")
            print(self.state)
            self.state = State()
            self.on_draw()
            return

        # 先手でない時
        if not self.state.is_first_player():
            return

        x=0
        y=0
        z=0

        if event.x < 320:
            z = 0
            x = int(event.x / 80)
        elif event.x>360 and event.x<680:
            z = 1
            x = int((event.x-360)/80)
        elif event.x>720 and event.x<1040:
            z = 2
            x = int((event.x-720)/80)
        else:
            z = 3
            x = int((event.x-1080)/80)

        if x<0 or x>3 or y<0 or y>3:
            return
        y = int(event.y / 80)
        action = x + int(y*4) + int(z*16)

        """
        print(self.state.legal_actions())
        print(x,y,z)
        print(action)
        """

        # 合法手でない時
        if not (action in self.state.legal_actions()):
            return

        # 次の状態の取得
        self.state = self.state.next(action)
        self.on_draw()

        print(self.state)

        # AIのターン
        self.master.after(1, self.turn_of_ai)

    # AIのターン
    def turn_of_ai(self):
        #print("turn of ai")

        # ゲーム終了時
        if self.state.is_done():
            return

        # 行動の取得
        action = self.next_action(self.state)

        # 次の状態の取得
        self.state = self.state.next(action)
        self.on_draw()

    # 石の描画
    def draw_piece(self, index, first_player):
        ps = 0
        if index < 16:
            ps=0
        elif index < 32:
            ps=360
        elif index < 48:
            ps=720
        else:
            ps=1080

        x = ps + 80 * (index%4) + 10
        y = int((index%16) / 4)*80 + 10
        """
        print("on draw------------------------------")
        print(x)
        print(y)
        """
        if first_player:
            self.c.create_oval(x, y, x+60, y+60, width = 2.0, outline = '#FFFFFF', fill='#FFFFFF')
        else:
            self.c.create_oval(x, y, x+60, y+60, width = 2.0, outline = '#000000', fill='#000000')



    # 描画の更新
    def on_draw(self):
        self.c.delete('all')
        self.c.create_rectangle(0, 0, 1400, 320, width = 0.0, fill = '#00A0FF', outline = '#0077BB')

        def draw_line(ps):
            for i in range(5):
                self.c.create_line(ps+80*i, 0, ps+80*i, 320, width = 2.0, fill = '#0077BB')
            for i in range(5):
                self.c.create_line(ps, 80*i, ps+320, 80*i, width = 2.0, fill = '#0077BB')
        
        draw_line(0)
        draw_line(360)
        draw_line(720)
        draw_line(1080)

                
        for i in range(64):
            if self.state.pieces[i] == 1:
                self.draw_piece(i, self.state.is_first_player())
            if self.state.enemy_pieces[i] == 1:
                self.draw_piece(i, not self.state.is_first_player())

# ゲームUIの実行
f = GameUI(model=model)
f.pack()
f.mainloop()