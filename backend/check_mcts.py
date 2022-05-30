from evaluate_best_player import *


# ベストプレイヤーのモデルの読み込み
model = load_model('./model/best.h5')

# PV MCTSで行動選択を行う関数の生成
next_pv_mcts_action = pv_mcts_action(model, 0.0)
# VSモンテカルロ木探索
next_actions = (next_pv_mcts_action, mcts_action)
evaluate_algorithm_of('VS_MCTS', next_actions)