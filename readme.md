# Data Generator アプリ ドキュメント

AI・ランダムデータ・静的な値・ネストされたオブジェクトを生成できるアプリの機能説明です。JSON形式で設定を記述することで、柔軟なデータ生成が可能です。

## 🚀 主な機能
1. **AIによるデータ生成**（OpenAI API連携）
2. **ランダムデータ生成**（UUID/数値/真偽値）
3. **静的な値の設定**
4. **ネストされたオブジェクト生成**

## 📋 使用方法
### 基本構造
```json
{
  "source": "データソース種別",
  // 各ソースに応じたパラメータ
}