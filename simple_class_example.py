"""
Pythonクラスの基本例
"""

# 1. シンプルなクラス
class Dog:
    # クラス変数（全インスタンス共通）
    species = "イヌ"
    total_dogs = 0

    def __init__(self, name, age, breed="雑種"):
        # インスタンス変数（各犬固有）
        self.name = name
        self.age = age
        self.breed = breed
        Dog.total_dogs += 1
        print(f"{name}が生まれました！")

    def bark(self):
        return f"{self.name}がワンワン！"

    def get_info(self):
        return f"名前: {self.name}, 年齢: {self.age}歳, 犬種: {self.breed}"

    def get_age_in_human_years(self):
        return self.age * 7

    def have_birthday(self):
        self.age += 1
        print(f"{self.name}は{self.age}歳になりました！")

# 2. 使用例
if __name__ == "__main__":
    # 犬を作成
    dog1 = Dog("ポチ", 3, "柴犬")
    dog2 = Dog("タロー", 5, "ゴールデンレトリバー")
    dog3 = Dog("ハナ", 2)  # breedはデフォルトの"雑種"

    print("\n=== 犬の情報 ===")
    print(dog1.get_info())
    print(dog2.get_info())
    print(dog3.get_info())

    print("\n=== 鳴き声 ===")
    print(dog1.bark())
    print(dog2.bark())

    print("\n=== 人間年齢 ===")
    print(f"{dog1.name}の人間年齢: {dog1.get_age_in_human_years()}歳")

    print("\n=== 誕生日 ===")
    dog1.have_birthday()

    print(f"\n=== 総犬数: {Dog.total_dogs}匹 ===")
    print(f"種類: {Dog.species}")