
import sys
# ランダムAI
# from ezRL import RandomPlayer	# 本番環境での使用法
from __init__ import RandomPlayer	# 開発時

# ランダムAI
train_ai = RandomPlayer(action_ls = ["act_0", "act_1"])

# 学習
for _ in range(3):
	action = train_ai.think(state = None, reward = 1)
	print(action)

# テスト用プレーヤーを生成
test_ai = train_ai.gen_test()

# テスト
for _ in range(3):
	action = test_ai.think(state = None, reward = 1)
	print(action)

sys.exit()

######### 以下、未整備

# # debug用人間プレーヤー
# from ezRL import HumanPlayer
# # 学習用AI, 対戦フィールド (arena)
# from ezRL import DQN_AI, arena
# # テスト用ゲーム (紅白ゲーム)
# from ezRL import RW_Game

# # # debug用人間プレーヤー
# # human_p = HumanPlayer(action_dic = {"Red": [1,0], "White": [0,1]})
# # game = RW_Game(round_n = 5)	# テスト用ゲーム (紅白ゲーム)
# # # 対戦して学習
# # arena(game, [human_p])	# 対戦フィールド (arena)
# # sys.exit()

# train_ai = DQN_AI(action_dim = 2)	# 学習用AI
# game = RW_Game(round_n = 100)	# テスト用ゲーム (紅白ゲーム)
# # 対戦して学習
# arena(game, [train_ai])	# 対戦フィールド (arena)

# # テスト用プレーヤーを生成
# test_ai = train_ai.gen_test()
# game = RW_Game(round_n = 100)	# テスト用ゲーム (紅白ゲーム)
# # 対戦して性能テスト (学習済みAI)
# arena(game, [test_ai])	# 対戦フィールド (arena)
