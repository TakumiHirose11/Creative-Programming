

# パッケージのインポート
import random
import math

class State:
    def __init__(self,pieces=None,enemy_pieces=None):
        self.pieces = pieces if pieces != None else [0]*64
        self.enemy_pieces = enemy_pieces if enemy_pieces !=None else [0]*64

    def piece_count(self, pieces):
        count=0
        for i in pieces:
            if i==1:
                count+=1
        return count
    
    def is_lose(self):
        def is_comp(x,y,z,dx,dy,dz):
            for k in range(4):
                if y<0 or 3<y or x<0 or 3<x or z<0 or z>3 or self.enemy_pieces[x + y*4 + z*16]==0:
                    return False
                x,y,z=x+dx,y+dy,z+dz
            return True
        
        #平面縦と横(x方向のみ、またはy方向のみ)
        for i in range(4):
            #高さで4つ
            for z in range(4):
                if is_comp(i,0,z,0,1,0) or is_comp(0,i,z,1,0,0):
                    return True
        
        #平面斜め（x,y方向）
        for z in range(4):
            if is_comp(0,0,z,1,1,0) or is_comp(0,3,z,1,-1,0):
                return True
            
        #立体縦と横
        for i in range(4):
            if is_comp(i,0,0,0,1,1) or is_comp(i,3,0,0,-1,1) or is_comp(0,i,0,1,0,1) or is_comp(3,i,0,-1,0,1):
                return True 

        #立体斜め
        if is_comp(0,0,0,1,1,1) or is_comp(3,3,0,-1,-1,1) or is_comp(0,3,0,1,-1,1) or is_comp(3,0,0,-1,1,1):
            return True

        #立体高さ（z方向のみ）
        for x in range(4):
            for y in range(4):
                if is_comp(x, y, 0, 0, 0, 1):
                    return True
            
        return False


    # 引き分けかどうか
    def is_draw(self):
        return self.piece_count(self.pieces) + self.piece_count(self.enemy_pieces) == 64

    # ゲーム終了かどうか
    def is_done(self):
        return self.is_lose() or self.is_draw()

    # 次の状態の取得
    def next(self, action):
        pieces = self.pieces.copy()
        pieces[action] = 1
        return State(self.enemy_pieces, pieces)

    # 合法手のリストの取得
    def legal_actions(self):
        actions = []
        for i in range(16):
            if self.pieces[i] == 0 and self.enemy_pieces[i] == 0:
                actions.append(i)
            else:
                 if self.pieces[i+16] == 0 and self.enemy_pieces[i+16] == 0:
                    actions.append(i+16)
                 else:
                    if self.pieces[i+32] == 0 and self.enemy_pieces[i+32] == 0:
                        actions.append(i+32)
                    else:
                        if self.pieces[i+48] == 0 and self.enemy_pieces[i+48] == 0:
                            actions.append(i+48)
        return actions

    # 先手かどうか
    def is_first_player(self):
        check=self.piece_count(self.pieces) == self.piece_count(self.enemy_pieces)
        return self.piece_count(self.pieces) == self.piece_count(self.enemy_pieces)

    # 文字列表示
    def __str__(self):
        ox = ('o', 'x') if self.is_first_player() else ('x', 'o')
        text = ''
        text+="------------------------------------\n"
        for i in range(64):
            if i%16==0:
                text+=str(int(i/16 +1))+"段目"+"\n"
            
            if self.pieces[i] == 1:
                text += ox[0]
            elif self.enemy_pieces[i] == 1:
                text += ox[1]
            else:
                text += '-'
            if i % 4 == 3:
                text += '\n'
            if i%16==15:
                text+='\n'
        return text

# ランダムで行動選択
def random_action(state):
    legal_actions = state.legal_actions()
    return legal_actions[random.randint(0, len(legal_actions)-1)]

# アルファベータ法で状態価値計算
def alpha_beta(state, alpha, beta):
    # 負けは状態価値-1
    if state.is_lose():
        return -1

    # 引き分けは状態価値0
    if state.is_draw():
        return  0

    # 合法手の状態価値の計算
    for action in state.legal_actions():
        score = -alpha_beta(state.next(action), -beta, -alpha)
        if score > alpha:
            alpha = score

        # 現ノードのベストスコアが親ノードを超えたら探索終了
        if alpha >= beta:
            return alpha

    # 合法手の状態価値の最大値を返す
    return alpha

# アルファベータ法で行動選択
def alpha_beta_action(state):
    # 合法手の状態価値の計算
    best_action = 0
    alpha = -float('inf')
    for action in state.legal_actions():
        score = -alpha_beta(state.next(action), -float('inf'), -alpha)
        if score > alpha:
            best_action = action
            alpha = score

    # 合法手の状態価値の最大値を持つ行動を返す
    return best_action

# プレイアウト
def playout(state):
    # 負けは状態価値-1
    if state.is_lose():
        return -1

    # 引き分けは状態価値0
    if state.is_draw():
        return  0

    # 次の状態の状態価値
    return -playout(state.next(random_action(state)))

# 最大値のインデックスを返す
def argmax(collection):
    return collection.index(max(collection))

# モンテカルロ木探索の行動選択
def mcts_action(state):
    # モンテカルロ木探索のノード
    class node:
        # 初期化
        def __init__(self, state):
            self.state = state # 状態
            self.w = 0 # 累計価値
            self.n = 0 # 試行回数
            self.child_nodes = None  # 子ノード群

        # 評価
        def evaluate(self):
            # ゲーム終了時
            if self.state.is_done():
                # 勝敗結果で価値を取得
                value = -1 if self.state.is_lose() else 0 # 負けは-1、引き分けは0

                # 累計価値と試行回数の更新
                self.w += value
                self.n += 1
                return value

            # 子ノードが存在しない時
            if not self.child_nodes:
                # プレイアウトで価値を取得
                value = playout(self.state)

                # 累計価値と試行回数の更新
                self.w += value
                self.n += 1

                # 子ノードの展開
                if self.n == 10:
                    self.expand()
                return value

            # 子ノードが存在する時
            else:
                # UCB1が最大の子ノードの評価で価値を取得
                value = -self.next_child_node().evaluate()

                # 累計価値と試行回数の更新
                self.w += value
                self.n += 1
                return value

        # 子ノードの展開
        def expand(self):
            legal_actions = self.state.legal_actions()
            self.child_nodes = []
            for action in legal_actions:
                self.child_nodes.append(node(self.state.next(action)))

        # UCB1が最大の子ノードを取得
        def next_child_node(self):
             # 試行回数nが0の子ノードを返す
            for child_node in self.child_nodes:
                if child_node.n == 0:
                    return child_node

            # UCB1の計算
            t = 0
            for c in self.child_nodes:
                t += c.n
            ucb1_values = []
            for child_node in self.child_nodes:
                ucb1_values.append(-child_node.w/child_node.n+2*(2*math.log(t)/child_node.n)**0.5)

            # UCB1が最大の子ノードを返す
            return self.child_nodes[argmax(ucb1_values)]

    # ルートノードの生成
    root_node = node(state)
    root_node.expand()

    # ルートノードを100回評価
    for _ in range(100):
        root_node.evaluate()

    # 試行回数の最大値を持つ行動を返す
    legal_actions = state.legal_actions()
    n_list = []
    for c in root_node.child_nodes:
        n_list.append(c.n)
    return legal_actions[argmax(n_list)]




def vs_human():
     # 状態の生成
    state = State()
    print()
    print("Game Start!!")
    # ゲーム終了までのループ

    i=0
    while True:
        print(state)
        if state.is_done():
            break
        if i%2 == 0:
            legal_actions = state.legal_actions()
            print("x→  y↓")
            x= int(input("enter x!"))
            y= int(input("enter y!"))
            z= int(input("enter z!"))
            if not x+y*4+z*16 in legal_actions:
                print()
                print("This move is not legal.")
                print()
                continue
            state = state.next(x+y*4+z*16)
            
        else:
            state = state.next(random_action(state))
        # 次の状態の取得
        #state = state.next(random_action(state))

        # 文字列表示
       
        print("--------------------------------------------")
        i+=1

def check_rule():
    state = State()
    print()
    print("Game Start!!")
    # ゲーム終了までのループ

    i=0
    while True:
        print(state)
        if state.is_done():
            break
        if i%2 == 0:
            legal_actions = state.legal_actions()
            print("x→  y↓")
            x= int(input("enter x!"))
            y= int(input("enter y!"))
            z= int(input("enter z!"))
            
            if not x+y*4+z*16 in legal_actions:
                print()
                print("This move is not legal.")
                print()
                continue
            state = state.next(x+y*4+z*16)
            
        else:
            state = state.next(random_action(state))
            state.enemy_pieces = [0]*64
        # 次の状態の取得
        #state = state.next(random_action(state))

        # 文字列表示
       
        print("--------------------------------------------")
        i+=1

# 動作確認
if __name__ == '__main__':
    #vs_human()
    check_rule()