# API通信フロー図

FactoryAIAssistantでは、UnityのHMIクライアントがFastAPIサーバーへアクセスします。

## 全体の通信フロー

```mermaid
flowchart LR
    User[作業者] --> Unity[Unity HMI]

    Unity -->|GET /sensor<br/>5秒ごと| API[FastAPI API]
    API -->|温度・圧力・振動・状態<br/>JSON| Unity

    Unity -->|POST /ask<br/>質問メッセージ| API
    API -->|generate_content| Gemini[Google Gemini]
    Gemini -->|AI回答| API
    API -->|JSON形式の回答| Unity
    Unity --> Chat[AIチャット画面]
```

## センサ値取得の流れ

```mermaid
sequenceDiagram
    participant U as Unity HMIClient
    participant A as FastAPI

    loop 5秒ごと
        U->>A: GET /sensor
        A-->>U: temperature, pressure, vibration, status
        U->>U: SensorDataに変換
        U->>U: HMI画面を更新
    end
```

`/sensor` のセンサ値は、現在は実際の設備から取得していません。FastAPIがランダムに生成する動作確認用のモックデータです。

## AI質問応答の流れ

```mermaid
sequenceDiagram
    participant U as Unity HMIClient
    participant A as FastAPI
    participant G as Google Gemini

    U->>U: 作業者が質問を入力
    U->>A: POST /ask { message }
    A->>G: generate_content(message)
    G-->>A: AI回答
    A-->>U: { answer }
    U->>U: AIメッセージをチャット吹き出しに追加
```

## APIのデータ形式

### `GET /sensor`

レスポンス例:

```json
{
  "temperature": 72.4,
  "pressure": 2.13,
  "vibration": 0.45,
  "status": "normal"
}
```

### `POST /ask`

リクエスト例:

```json
{
  "message": "温度が高い理由を教えてください。"
}
```

レスポンス例:

```json
{
  "answer": "温度上昇の主な原因は負荷増加や換気不良です。確認ポイントは送風と保守状態です。"
}
```
