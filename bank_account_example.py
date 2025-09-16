"""
実用的なクラス例：銀行口座
"""

class BankAccount:
    def __init__(self, owner_name, initial_balance=0):
        self.owner_name = owner_name
        self.balance = initial_balance
        self.transaction_history = []
        print(f"{owner_name}さんの口座を開設しました。残高: {initial_balance}円")

    def deposit(self, amount):
        if amount <= 0:
            print("入金額は0より大きくする必要があります")
            return False

        self.balance += amount
        self.transaction_history.append(f"入金: +{amount}円")
        print(f"{amount}円を入金しました。残高: {self.balance}円")
        return True

    def withdraw(self, amount):
        if amount <= 0:
            print("出金額は0より大きくする必要があります")
            return False

        if amount > self.balance:
            print(f"残高不足です。現在の残高: {self.balance}円")
            return False

        self.balance -= amount
        self.transaction_history.append(f"出金: -{amount}円")
        print(f"{amount}円を出金しました。残高: {self.balance}円")
        return True

    def get_balance(self):
        return self.balance

    def get_transaction_history(self):
        print(f"\n=== {self.owner_name}さんの取引履歴 ===")
        for transaction in self.transaction_history:
            print(transaction)
        print(f"現在の残高: {self.balance}円")

# 使用例
if __name__ == "__main__":
    # 口座作成
    account1 = BankAccount("田中太郎", 10000)
    account2 = BankAccount("佐藤花子")

    print("\n=== 取引開始 ===")

    # 田中さんの取引
    account1.deposit(5000)
    account1.withdraw(3000)
    account1.withdraw(15000)  # エラー：残高不足

    # 佐藤さんの取引
    account2.deposit(20000)
    account2.withdraw(5000)

    # 履歴確認
    account1.get_transaction_history()
    account2.get_transaction_history()