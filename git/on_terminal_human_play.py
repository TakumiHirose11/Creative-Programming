from game import State
from pv_mcts import pv_mcts_action
from tensorflow.keras.models import load_model
from pathlib import Path

# ベストプレイヤーのモデルの読み込み
model = load_model('./model/best.h5')
state = State()

print()
print("Game Start!!")

i=1
while True:
    print(state)
    if state.is_done():
        print("TOTAL TURN : ",i)
        break
    if i%2 == 1:
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
        next_action = pv_mcts_action(model, 0.0)
        action = next_action(state)
        state = state.next(action)


    
    print("--------------------------------------------")
    i+=1