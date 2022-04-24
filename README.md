# Virtual Money Transaction 
2022 情報系課題研究用 <br>

## How to Use
サーバーの開始にはuvicornを使用します。
ターミナルにて`uvicorn main:app --reload`を実行します。<br>
`--reload`はアプリケーションに変更が加えられると自動的に再起動されるオプションです。必要ない場合は適宜外してください。

<br>また、コード内に
```python
~中略~
if __name__ == "__main_":
  app.run("ThisIsExampleFunction")
```
のような自動起動を行う関数を入れないでください。<br>
サーバーの起動はコマンドラインから行ってください。
<br>

実際にこのコードを動かす際にはトークンの設定が必要です。<br>
`secret_example.py`の名前を`secret.py`に変更し、
```bash
mv secret_example.py secret.py
```

内部の定数をランダムな予測不可な値に書き換えてください。

```python
PASS_SALT = "PASS_SALT"
OAUTH_TOKEN = "OAUTH_TOKEN"
JWT_TOKEN = "JWT_TOKEN"
```

値の生成には`openssl`コマンドを推奨します。

```bash
openssl rand -hex 32
```

## Structure
仕組みについては以下を参照してください。

### Auth - 認証
JWT認証方式を採用しています。データベースには`peewee`による`sqlite3`で管理しています。<br>

最初に、クライアントはサーバー(`/token`)に対して`POST`リクエストを送信し、`access_token`と`refresh_token`を取得します。
その際のリクエスト形式は`application/x-www-form-urlencoded`、パラメーターは`username`,`password`です。<br>

_curlによるトークン取得の例_
```bash
curl -X POST "http://example.com/token" -H  "accept: application/json" -H  "Content-Type: application/x-www-form-urlencoded" -d "username=hoge&password=fuga
```

リクエストが正常に処理されれば以下のようなスキーマでレスポンスが行われます。

```json
{
  "access_token": "string",
  "refresh_token": "string",
  "type": "string"
}
```
<br>

取得した`access_token`を使用してユーザー情報にアクセスできます。<br>


_curlによるユーザー名取得の例_
```bash
curl -X GET "http://example.com/users/me/" -H  "accept: application/json" -H  "Authorization: Bearer access_token"
```

リクエストが正常に処理されれば以下のようなスキーマでレスポンスが行われます。

```json
{
  "name": "NAME",
  "balance": 0
}
```
<br>

トークンの有効期限は発行日より`access_token`は`1 Hour`、`refresh_token`は`60 Days`に設定されています。<br>
トークンはリクエストが行われた`username`と`password`に基づき`user_id`を検索し、そのidに基づいて生成されています。<br>
トークンのペイロードには`トークンタイプ`、`有効期限`、`user_id`が格納されています。<br>
トークンは`JWT_TOKEN`と`HS256アルゴリズム`によってエンコードされています。
<br>

`refresh_token`は`access_token`の再発行に使用されます。`refresh_token`を使用してユーザーの情報を取得することはできません。
サーバーは`refresh_token`の有効期限内かを確認しデータベースと情報が一致するか検証します。<br>
正常に認証されればクライアントが正規ユーザーとして扱われ、そのユーザーの`user_id`に基づき新しい`access_token`が発行されます。



## Branch
`master`ブランチは完成形を保管したいので基本的にブランチは自分のものを作りましょう。

## Licence
教育目的に使用され作成されたリポジトリです。
<br>コードに関する著作権はその開発者に帰属します。

