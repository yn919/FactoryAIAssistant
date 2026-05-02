# Factory AI Assistant Backend

FastAPI + Gemini APIを使用したUnity連携用AIアシスタントバックエンド

## 機能概要

- テキストチャット機能（Gemini AI連携）
- UnityアプリとのHTTP API連携
- ヘルスチェック機能
- ローカル環境での完結（Docker不要）

## 動作要件

- **Python**: 3.12 または 3.13（Python 3.14は非対応）
- **OS**: Windows 10/11, macOS, Linux
- **追加ツール**: Build Tools for Visual Studio（Windowsの場合、C++デスクトップ開発）

## セットアップ手順

### 1. 仮想環境の作成と有効化

```bash
# プロジェクトルートで実行
cd backend

# 仮想環境作成
python -m venv venv

# Windowsで仮想環境を有効化
venv\Scripts\activate

# macOS/Linuxで仮想環境を有効化
source venv/bin/activate
```

### 2. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 3. 環境変数の設定

```bash
# .env.exampleをコピーして.envを作成
cp .env.example .env

# .envファイルをテキストエディタで編集し、Gemini APIキーを設定
# GEMINI_API_KEY=your_actual_gemini_api_key_here
```

**Gemini APIキーの取得方法:**
1. [Google AI Studio](https://makersuite.google.com/app/apikey)にアクセス
2. Googleアカウントでログイン
3. 「Create API Key」をクリック
4. 生成されたAPIキーをコピーして.envファイルに貼り付け

### 4. サーバーの起動

```bash
# 方法1: 起動スクリプトを使用
python run_server.py

# 方法2: 直接uvicornを実行
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

サーバーが起動すると以下のURLでアクセス可能になります：
- APIドキュメント: http://localhost:8000/docs
- ヘルスチェック: http://localhost:8000/health
- チャットエンドポイント: http://localhost:8000/chat

## テストの実行

```bash
# すべてのテストを実行
pytest tests/ -v

# 特定のテストファイルを実行
pytest tests/test_chat.py -v

# カバレッジ付きでテストを実行
pytest tests/ -v --cov=app
```

## プロジェクト構成

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPIアプリケーション
│   ├── config.py            # 設定管理
│   ├── services/
│   │   ├── __init__.py
│   │   └── gemini_service.py # Gemini API連携
│   └── models/
│       ├── __init__.py
│       └── chat.py          # リクエスト/レスポンスモデル
├── tests/
│   ├── __init__.py
│   ├── test_chat.py         # チャット機能テスト
│   └── conftest.py          # テスト設定
├── requirements.txt         # 依存パッケージ
├── .env.example            # 環境変数テンプレート
├── run_server.py           # サーバー起動スクリプト
└── README.md               # このファイル
```

## トラブルシューティング

### APIキー関連のエラー
- `.env`ファイルに正しいAPIキーが設定されているか確認
- APIキーが有効であるか確認（Google AI Studioで確認）

### サーバー起動エラー
- 仮想環境が正しく有効化されているか確認
- ポート8000が他のアプリで使用されていないか確認

### Unityからの接続エラー
- サーバーが起動しているか確認
- ファイアウォール設定を確認
- CORS設定が正しいか確認（現在はすべてのオリジンを許可）

## ライセンス

このプロジェクトはMITライセンスの下で提供されています。
