# FactoryAIAssistant Unity クライアント技術仕様書

## 1. 目的

本モジュールは、工場向けHMIのプロトタイプとして動作するUnityアプリケーションです。作業者が設備状態を確認し、質問を入力してAI支援を受けられるように設計されています。

主な役割は次のとおりです。

- センサ値の表示
- AIアシスタントへの問い合わせ
- 会話履歴の画面表示
- 3D空間内での工場環境の可視化

## 2. 対象範囲

- Unityエディタでの実行
- HMI UIの構築
- FastAPI APIとの通信
- 監視データとAI応答の画面表示

## 3. システム概要

本プロジェクトは、UnityクライアントとAPIサーバーの2層構成で動作します。

- Unity側: UI表示、センサ値の更新、会話入力
- API側: `/sensor` でセンサ値を返し、`/ask` でAI応答を返す

データの流れは次の通りです。

1. Unityが起動時に `HMIClient` の `SensorLoop` を開始する
2. `HMIClient` が5秒ごとに `/sensor` を呼び出す
3. JSONから `SensorData` を作成し、温度・圧力・振動・状態を画面に反映する
4. 作業者が質問を入力し、「Ask」操作を実行すると `/ask` にPOSTする
5. 応答を `AnswerData` で受け取り、AIチャットの吹き出しとして表示する

## 4. 主要コンポーネント

### 4.1 HMIClient

ファイル: `Assets/Scripts/Client/HMIClient.cs`

役割:

- APIとの通信制御
- センサループの起動
- 質問入力の受信とAI呼び出し
- 会話メッセージの表示

主なメソッド:

- `Start()`
  - センサ更新ループを開始する
- `SensorLoop()`
  - 5秒間隔でセンサ値を取得する
- `GetSensor()`
  - `GET /sensor` を実行する
- `OnAskButton()`
  - ユーザー入力に対して質問送信を開始する
- `AskAI()`
  - `POST /ask` を実行し、回答をUIに追加する
- `AddMessage()`
  - ユーザーメッセージまたはAIメッセージの吹き出しを描画する

### 4.2 SensorDisplay（単体デモ用）

ファイル: `Assets/Scripts/SensorDisplay.cs`

役割:

- センサ表示用のテキストコンポーネントへの値設定
- APIを使わず、Unity内で1秒ごとにモック値を更新

`SensorDisplay` はローカルな表示動作を確認するための独立したコンポーネントです。
現在の実行シーンでAPIからセンサ値を取得する経路は `HMIClient` であり、
`SensorDisplay` はそのAPI通信には関与しません。

### 4.3 Dataモデル

ファイル:

- `Assets/Scripts/Data/SensorData.cs`
- `Assets/Scripts/Data/Question.cs`
- `Assets/Scripts/Data/AnswerData.cs`

データ仕様:

- `SensorData`
  - `temperature`: 温度
  - `pressure`: 圧力
  - `vibration`: 振動
  - `status`: normal / warning
- `Question`
  - `message`: 発話内容
- `AnswerData`
  - `answer`: AIの返答

## 5. UI設計

Unity側では以下のUI要素が想定されます。

- 入力フィールド
- 送信ボタン
- チャット表示領域
- センサ値表示テキスト
- ステータス表示テキスト

チャット領域では、ユーザー側とAI側のメッセージを左右に分けて表示する設計になっています。レイアウトでは `HorizontalLayoutGroup` と `LayoutElement` を利用して、吹き出しの幅や配置を制御しています。

## 6. 通信設計

### 6.1 ベースURL

Unityクライアントは `http://localhost:8000` を前提に通信します。

本番環境では以下の構成に変更することを想定しています。

- APIのホスト名を変更
- HTTPSの導入
- リバースプロキシの追加
- 認証トークンの付与

### 6.2 通信方式

- `GET /sensor` でセンサ値取得
- `POST /ask` でAI質問送信
- `UnityWebRequest` を使用してHTTP通信

## 7. テスト戦略

本UnityプロジェクトにはPlayModeテストが用意されています。

対象テスト:

- `AutoRotateTest.cs`
- `SensorDisplayTest.cs`
- `HMIClientTests.cs`

テストの観点:

- 自動回転コンポーネントが正常に動作するか
- センサ表示テキストが更新されるか
- HMIClientがAPIとの通信を想定どおり扱えるか
- 例外時に警告ログを出力できるか

## 8. 非機能要件

### 8.1 性能

- API経由のセンサ更新周期: 5秒
- `SensorDisplay` 単体デモのUI更新: 1秒ごとのモック値更新
- 会話生成: 数秒程度を想定

### 8.2 可用性

- センサ取得に失敗した場合はUnityのコンソールへ警告を出力し、AI問い合わせに失敗した場合はチャット欄へエラーを表示する
- 通信に失敗しても、アプリ全体が停止しないように設計されている

### 8.3 保守性

- 通信ロジックとUI描画ロジックが分離されている
- 型定義を `Data` フォルダに集約している
- 3Dシーンとスクリプトが分離可能な構造になっている

## 9. 現状の制約

- センサ値はモックデータであり、設備からの実データではない
- AI応答はGemini APIへ依存するため、API側の設定が必要である
- Unityエディタ上での動作を前提としており、端末配布の設計は未実装である
- ログ管理やメトリクス監視の仕組みはまだ最小構成である

## 10. 運用方法

1. Unity Hub または Unity Editor から `FactoryAIAssistant` フォルダを開く
2. 必要なシーンを読み込む
3. `factory-hmi-api` の FastAPI を起動する
4. Unityで再生モードを開始する
5. センサ値とAI会話の動作を確認する
