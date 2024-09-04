import tkinter as tk
import random

class HighAndLowGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ハイアンドローゲーム")
        self.root.geometry("500x400")

        self.suits = ['クラブ', 'ダイヤ', 'ハート', 'スペード']
        self.suit_symbols = {'クラブ': '♣', 'ダイヤ': '♦', 'ハート': '♥', 'スペード': '♠'}
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

        self.current_card = self.draw_card()
        self.turn_num = 0
        self.coins = 100  # 初期コイン数
        self.round_coins = 0  # 現在のラウンドで獲得したコイン数
        self.correct_streak = 0  # 正解の連続回数
        self.current_bet = 0  # 現在の賭け金

        self.card_label = tk.Label(self.root, text=self.format_card(self.current_card), font=("Helvetica", 40))
        self.card_label.pack()

        self.coins_label = tk.Label(self.root, text=f"現在のコイン: {self.coins}", font=("Helvetica", 20))
        self.coins_label.pack()

        self.bet_label = tk.Label(self.root, text="賭けるコイン数:", font=("Helvetica", 15))
        self.bet_label.pack()

        self.bet_entry = tk.Entry(self.root)
        self.bet_entry.pack()

        self.high_button = tk.Button(self.root, text="High", command=self.high_guess)
        self.high_button.pack()

        self.low_button = tk.Button(self.root, text="Low", command=self.low_guess)
        self.low_button.pack()

        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 20))
        self.result_label.pack()

        self.collect_button = tk.Button(self.root, text="コインを受け取る", command=self.collect_coins, state='disabled')
        self.collect_button.pack()

    def draw_card(self):
        suit = random.choice(self.suits)
        rank = random.choice(self.ranks)
        return suit, rank

    def format_card(self, card):
        suit, rank = card
        return f"{rank}{self.suit_symbols[suit]}"

    def place_bet(self):
        try:
            bet = int(self.bet_entry.get())
            if bet <= 0:
                raise ValueError("賭け金は1以上にしてください。")
            if bet > self.coins:
                raise ValueError("コインが不足しています。")
            self.coins -= bet  # 賭けたコインを現在のコインから減らす
            self.coins_label['text'] = f"現在のコイン: {self.coins}"
            self.current_bet = bet  # 現在の賭け金を設定
            return bet
        except ValueError as e:
            self.result_label['text'] = str(e)
            return None

    def calculate_winnings(self):
        return self.current_bet * (2 ** self.correct_streak)

    def high_guess(self):
        if self.turn_num == 0:
            bet = self.place_bet()
            if bet is None:
                return
        self.turn_num += 1
        next_card = self.draw_card()
        self.card_label['text'] = self.format_card(next_card)
        if self.values[next_card[1]] >= self.values[self.current_card[1]]:
            self.correct_streak += 1
            self.round_coins = self.calculate_winnings()
            self.result_label['text'] = f"正解！獲得可能コイン: {self.round_coins}"
            self.collect_button['state'] = 'normal'
        else:
            self.result_label['text'] = "不正解。賭けたコインを失いました。"
            self.round_coins = 0
            self.end_round()
        self.current_card = next_card

    def low_guess(self):
        if self.turn_num == 0:
            bet = self.place_bet()
            if bet is None:
                return
        self.turn_num += 1
        next_card = self.draw_card()
        self.card_label['text'] = self.format_card(next_card)
        if self.values[next_card[1]] <= self.values[self.current_card[1]]:
            self.correct_streak += 1
            self.round_coins = self.calculate_winnings()
            self.result_label['text'] = f"正解！獲得可能コイン: {self.round_coins}"
            self.collect_button['state'] = 'normal'
        else:
            self.result_label['text'] = "不正解。賭けたコインを失いました。"
            self.round_coins = 0
            self.end_round()
        self.current_card = next_card

    def collect_coins(self):
        self.coins += self.round_coins  # 獲得したコインを追加
        self.coins_label['text'] = f"現在のコイン: {self.coins}"
        self.end_round()

    def end_round(self):
        self.correct_streak = 0  # 連続正解数をリセット
        self.round_coins = 0  # ラウンドコインをリセット
        self.current_bet = 0  # 現在の賭け金をリセット
        self.turn_num = 0  # ターン数リセット
        self.collect_button['state'] = 'disabled'
        if self.coins <= 0:
            self.result_label['text'] = "ゲームオーバー！"
            self.high_button['state'] = 'disabled'
            self.low_button['state'] = 'disabled'
            self.collect_button['state'] = 'disabled'

            # ゲームオーバー画面の表示
            self.game_over_label = tk.Label(self.root, text="ゲームオーバー！", font=("Helvetica", 30), fg="red")
            self.game_over_label.pack()

            # リスタートボタンの作成
            self.restart_button = tk.Button(self.root, text="リスタート", command=self.restart_game)
            self.restart_button.pack()

    def restart_game(self):
        # ゲームを初期状態に戻す
        self.current_card = self.draw_card()
        self.turn_num = 0
        self.coins = 100
        self.round_coins = 0
        self.correct_streak = 0
        self.current_bet = 0

        # ラベルのテキストを初期化
        self.card_label['text'] = self.format_card(self.current_card)
        self.coins_label['text'] = f"現在のコイン: {self.coins}"
        self.result_label['text'] = ""

        # ボタンの状態を有効化
        self.high_button['state'] = 'normal'
        self.low_button['state'] = 'normal'
        self.collect_button['state'] = 'disabled'

        # ゲームオーバー画面を削除
        self.game_over_label.destroy()
        self.restart_button.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = HighAndLowGame()
    game.run()
