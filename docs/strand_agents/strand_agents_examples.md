# Strand Agents 使用例

Strand Agentsでは、特定のタスクを実行するための「ツール」を定義し、それをエージェントに組み込むことで、自律的な処理を実現します。以下は、基本的なエージェントを作成・実行するための典型的なコード例です。

## 基本的なエージェントの作成

この例では、ユーザーに挨拶を返す簡単なツールを持つエージェントを作成します。

### 1. 必要なライブラリのインポート

まず、`Agent`クラスと、使用するLLMのクライアント（この場合はOpenAI）をインポートします。

```python
from strands_agents import Agent
from openai import OpenAI

client = OpenAI()
```

### 2. ツールの定義

エージェントが使用できるツールをPythonの関数として定義します。関数には型アノテーションとdocstringを記述することが推奨されます。

```python
def say_hello(name: str) -> str:
    """
    指定された名前に挨拶を返します。

    :param name: 挨拶する相手の名前。
    :return: 挨拶の文字列。
    """
    return f"Hello, {name}!"
```

### 3. エージェントの初期化

モデル、システムプロンプト、そして先ほど定義したツールリストを渡して、`Agent`を初期化します。

```python
agent = Agent(
    model="openai/gpt-4-turbo-preview",
    system_prompt="あなたは親切なアシスタントです。利用可能なツールを使ってユーザーを助けてください。",
    tools=[
        say_hello,
    ],
    client=client,
)
```

### 4. エージェントの実行

`run`メソッドを呼び出して、エージェントにタスクを指示します。

```python
if __name__ == "__main__":
    response = agent.run("ボブに挨拶してください")
    print(response)
```

## 実行結果

エージェントはユーザーの指示を理解し、`say_hello`ツールを呼び出して、以下のような結果を返します。

```
Hello, Bob!
```

このように、Strand AgentsはPythonの関数をツールとして簡単に統合し、LLMを活用した自律的なエージェントを構築することができます。
