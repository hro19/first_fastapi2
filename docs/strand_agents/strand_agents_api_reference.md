# Strand Agents APIリファレンス: Agentクラス

`Agent`クラスは、Strand Agentsフレームワークにおける中心的なコンポーネントです。大規模言語モデル（LLM）との対話、ツールの実行、会話履歴の管理など、エージェントの動作全体を調整します。

## `Agent`の初期化

エージェントは`Agent`クラスをインスタンス化することで作成します。初期化時には、エージェントの振る舞いを定義する様々なパラメータを指定します。

```python
from strands_agents import Agent

agent = Agent(
    model="openai/gpt-4-turbo-preview",
    system_prompt="You are a helpful assistant.",
    tools=[...],
    # その他のパラメータ
)
```

### 主要な初期化パラメータ

- `model` (str):
  エージェントが使用するLLMのモデル名を指定します。 (例: `"openai/gpt-4-turbo-preview"`)

- `system_prompt` (str):
  エージェントの役割や振る舞いを定義するシステムプロンプトです。LLMに与える基本的な指示となります。

- `tools` (list[Callable]):
  エージェントが使用できるツールのリストを渡します。各ツールはPythonの関数として定義します。

- `client` (Any | None):
  使用するモデルプロバイダーのクライアントインスタンスです。（例: `OpenAI()`）

- `conversation_manager` (ConversationManager | None):
  会話の履歴を管理する方法を定義するコンポーネントです。指定しない場合、デフォルトのマネージャーが使用されます。

- `temperature` (float):
  モデルの応答のランダム性を制御します。0に近いほど決定的になり、1に近いほど多様な応答が生成されます。デフォルトは`0.0`です。

- `max_tool_calls_per_turn` (int):
  1つの対話ターンでエージェントがツールを呼び出せる最大回数を制限します。デフォルトは`5`です。

## `run`メソッド

エージェントにタスクを実行させるには`run`メソッドを使用します。

```python
response = agent.run("ユーザーからの入力メッセージ")
```

- **引数**: ユーザーからのプロンプトを文字列として渡します。
- **戻り値**: エージェントが生成した最終的な応答を文字列として返します。

`run`メソッドの内部では、ユーザー入力の処理、LLMへの問い合わせ、適切なツールの選択と実行、そして最終応答の生成という一連のワークフローが管理されます。
