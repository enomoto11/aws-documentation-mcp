# AWS Documentation MCP Server

AWS公式ドキュメントを活用したMCPサーバーです。AWS CLIやSDKの使用方法、AWSサービスの設定方法などについて、AWS公式ドキュメントを基にした回答を提供します。

## 機能

- AWS公式ドキュメントを基にした質問応答
- AWS CLIコマンドの使用方法の説明
- AWSサービスの設定手順の案内
- ベストプラクティスの提案

## セットアップ

1. 環境変数の設定
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=your_region
```

2. 依存関係のインストール
```bash
pip install -r requirements.txt
```

3. サーバーの起動
```bash
python main.py
```

## 使用方法

1. HTTPリクエストの例：
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "S3バケットの作成方法を教えてください"}'
```

2. レスポンスの例：
```json
{
  "response": "S3バケットを作成するには以下の手順に従ってください：\n1. AWS CLIを使用する場合：\n   aws s3api create-bucket --bucket バケット名 --region リージョン名\n\n2. AWS Management Consoleを使用する場合：\n   - S3コンソールにアクセス\n   - [バケットを作成]をクリック\n   - バケット名とリージョンを指定\n   - 設定を確認して作成\n"
}
```

## ライセンス

MITライセンス