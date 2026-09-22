# FactoryAIAssistant 技術仕様書

## 1. 概要

本リポジトリは、工場内の設備監視と作業支援を目的としたHMI（Human Machine Interface）システムのプロトタイプです。

主な構成は次の2層です。

- UnityベースのHMIクライアント
- FastAPIベースのAI応答・センサAPI

Unity側は設備の状態表示と作業者からの質問入力を担い、バックエンドのAPIへアクセスしてセンサ値の取得とAI応答の受け取りを行います。AI側はGoogle Geminiを利用して、工場作業者向けの簡潔で実用的な日本語回答を返します。

## 2. 目的とスコープ

### 2.1 目的

- 工場設備の状態を可視化する
- 作業者が設備に関する簡単な質問を入力できる
- AIアシスタントが短時間で判断材料を返す
- モックセンサ値とUIデモを通じて、現場向けHMIの動作検証を行う

### 2.2 対象範囲

- 5秒間隔のセンサ値表示
- AIチャット形式の質問応答
- ローカル開発環境でのAPI連携
- Unityエディタでのプレイモードテスト

## 3. システム構成

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

## 4. ディレクトリ構成

- `FactoryAIAssistant/` : Unityプロジェクト本体
- `factory-hmi-api/` : Python APIサーバー
- `README.md` : 全体設計の概要

## 5. 技術スタック

- Unity 6000系
- C# と UnityWebRequest
- FastAPI
- Pydantic
- Python-dotenv
- Google Generative AI SDK
- pytest

## 6. 主要機能

### 6.1 センサ可視化

HMI側の `HMIClient` が5秒ごとに `/sensor` を呼び、以下の値を表示します。

- 温度
- 圧力
- 振動
- 状態（normal / warning）

### 6.2 AI質問応答

HMI側の入力欄で作業者が質問を入力すると、`/ask` にJSONで送信され、バックエンドがGeminiへ問い合わせます。

応答は以下の方針で生成されます。

- 日本語で簡潔に回答する
- 3行以内で返す
- 工場設備の専門家として説明する
- 専門用語はわかりやすく表現する

### 6.3 UI再現性

Unityプロジェクトには工場のような見た目を持つ3Dシーンと、会話UIが含まれており、HMIのプロトタイプとして可視化されています。

## 7. 通信仕様

### 7.1 GET /sensor

センサ値のサンプルを返します。

レスポンス例:

```json
{
  "temperature": 72.4,
  "pressure": 2.13,
  "vibration": 0.45,
  "status": "normal"
}
```

### 7.2 POST /ask

ユーザーの質問文をJSONで受け取り、AIの回答を返します。

リクエスト例:

```json
{
  "message": "圧力が上がっている原因を教えてください。"
}
```

レスポンス例:

```json
{
  "answer": "圧力上昇の主な要因は流量増加や詰まりです。確認ポイントはフィルタと弁の状態です。"
}
```

## 8. 運用時の制約

- `GEMINI_API_KEY` が設定されていない場合、Gemini APIの呼び出しが失敗する可能性があります。
- 現在の実装ではAPIが返すセンサ値がランダム生成であり、現実の設備データではありません。
- FastAPIサーバーはローカル開発用途を前提としています。
- Unity側は `http://localhost:8000` を前提に通信しています。

## 9. 開発・テスト

- APIテスト: `factory-hmi-api/test_main.py`
- Unityテスト: `FactoryAIAssistant/Assets/Tests/PlayMode/Tests`

主要な確認観点:

- `/` が正常に応答するか
- `/sensor` がJSON形式で返るか
- `/ask` がAI依存のモック応答で正しく動作するか
- Unity側がセンサ値とAI応答をUIへ表示できるか
- センサ取得に失敗した場合にUnityのコンソールへ警告を出力できるか

## 10. 参照ドキュメント

- [Unityクライアント仕様書](./FactoryAIAssistant/README.md)
- [FastAPI仕様書](./factory-hmi-api/README.md)

## 11. 解説動画
[FactoryAIAssistant\Movies\FactoryAIAssistant解説.mp4](https://github.com/yn919/FactoryAIAssistant/blob/create-movie/Movies/FactoryAIAssistant%E8%A7%A3%E8%AA%AC.mp4)

## 初回セットアップ

1. `factory-hmi-api` フォルダーでPythonの仮想環境を作成し、依存パッケージをインストールします。詳しい手順は [API README](./factory-hmi-api/README.md) を参照してください。
2. `factory-hmi-api/.env.example` を `.env` にコピーし、`GEMINI_API_KEY` を設定します。
3. Unity Hubで `FactoryAIAssistant` フォルダーをUnity 6000系（`FactoryAIAssistant/ProjectSettings/ProjectVersion.txt` の記載バージョン）で開きます。

## 起動方法

### 1. APIサーバーを起動する

Windows PowerShellでは、リポジトリのルートで次を実行します。

```powershell
cd factory-hmi-api
.\.venv\Scripts\Activate.ps1
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

ブラウザーで <http://localhost:8000/> を開き、JSONが表示されれば起動しています。停止するときは、APIを実行している画面で `Ctrl+C` を押します。

### 2. Unityシーンを再生する

1. Unity Editorで `Assets/Scenes/FactoryAIAssistantScene.unity` を開きます。
2. **Play** ボタンを押します。
3. センサ値の表示と質問入力を確認します。
4. 終了するときは、もう一度 **Play** ボタンを押します。

全体の運用では、APIを先に起動し、Unityを再生し、Unityを停止してからAPIを停止します。APIが起動していない場合、Unityからセンサ値やAI回答を取得できません。センサ取得の失敗はUnityのコンソールに警告として出力され、AI問い合わせの失敗はチャット欄にエラーとして表示されます。
