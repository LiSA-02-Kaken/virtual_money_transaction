# Virtual Money Transaction 
2022 情報系課題研究用 <br>

## How to
サーバーの開始にはuvicornを使用します。
ターミナルにて`uvicorn main:app --reload`を実行します。<br>
`--reload`はアプリケーションに変更が加えられると自動的に再起動されるオプションです。必要ない場合は適宜外してください。！

<br>また、コード内に
```python
~中略~

if __name__ == "__main_":
  app.run("ThisIsExampleFunction")
```
のような自動起動を行う関数を入れないでください。<br>
サーバーの起動はコマンドラインから行ってください。

# Branch
`master`ブランチは完成形を保管したいので基本的にブランチは自分のものを作りましょう。

## Licence
教育目的に使用され作成されたリポジトリです。外部公開厳禁。
<br>コードに関する著作権はその開発者に帰属します。

