import random

class RPSGame:
    def __init__(self):
        """
        初始化遊戲邏輯。
        """
        self.moves = ["rock", "paper", "scissors"]
        self.player_score = 0
        self.ai_score = 0

    def get_ai_choice(self):
        """
        為 AI 隨機選擇一個出拳。
        :return: AI 的出拳 ("rock", "paper", 或 "scissors")。
        """
        return random.choice(self.moves)

    def get_winner(self, player_move, ai_move):
        """
        根據玩家和 AI 的出拳判斷勝負。
        
        :param player_move: 玩家的出拳。
        :param ai_move: AI 的出拳。
        :return: 一個包含勝者和原因的元組 (winner, reason)。
                 例如 ("Player", "Paper covers Rock")。
        """
        if player_move not in self.moves:
            return "Invalid", "無效的出拳"

        if player_move == ai_move:
            return "Tie", f"平手 ({player_move})"

        winning_combinations = {
            ("rock", "scissors"): "Rock smashes Scissors",
            ("scissors", "paper"): "Scissors cuts Paper",
            ("paper", "rock"): "Paper covers Rock",
        }

        if (player_move, ai_move) in winning_combinations:
            reason = winning_combinations[(player_move, ai_move)]
            self.player_score += 1
            return "Player", reason
        else:
            reason = winning_combinations[(ai_move, player_move)]
            self.ai_score += 1
            return "AI", reason
            
    def get_scores(self):
        """
        獲取目前的分數。
        :return: 一個包含玩家和 AI 分數的字典。
        """
        return {"player": self.player_score, "ai": self.ai_score}

    def reset_scores(self):
        """
        重置分數。
        """
        self.player_score = 0
        self.ai_score = 0

# --- 以下為單獨測試此模組的程式碼 ---
if __name__ == '__main__':
    game = RPSGame()
    
    # 模擬一局遊戲
    player_action = "rock"
    ai_action = game.get_ai_choice()
    
    print(f"玩家出拳: {player_action}")
    print(f"AI 出拳: {ai_action}")
    
    winner, reason = game.get_winner(player_action, ai_action)
    
    print(f"結果: {winner}")
    print(f"原因: {reason}")
    print(f"目前分數: {game.get_scores()}")

    # 模擬另一局
    player_action = "paper"
    ai_action = game.get_ai_choice()
    
    print(f"\n玩家出拳: {player_action}")
    print(f"AI 出拳: {ai_action}")
    
    winner, reason = game.get_winner(player_action, ai_action)
    
    print(f"結果: {winner}")
    print(f"原因: {reason}")
    print(f"目前分數: {game.get_scores()}")
