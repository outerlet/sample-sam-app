# sample-sam-app

## ディレクトリ構成

- docker/
  - docker-compose.yaml　などDocker関連のリソースを配置（する想定）
  - ここで `docker compose up` すれば、LocalStackがデフォルトの設定で起動します
- sam/
  - SAMアプリを構成する一連のファイル群。設定ファイル、テンプレート、Lambdaのソースコードなど
  - `samlocal` コマンドを使ってSAMアプリをデプロイするのはここで行う
- android/
  - LocalStackにデプロイした `SimpleResponseFunction` 関数にリクエストをかけるAndroidアプリのプロジェクトディレクトリ
- README.md
  - 本テキスト

## リソース

### S3 Bucket

- `SampleAppBucket`
  - アプリが使用するバケット

### DynamoDB Table

- `MessageTable`
  - `AddMessageFunction` 関数が書き込む先のテーブル
- `MemberTable`
  - `UpdateMemberFileFunction` 関数がデータを受け取るテーブル

### Lambda関数群

- `HelloWorldFunction`
  - `sam init` コマンドの実行時に生成されたデフォルトの関数
- `SimpleResponseFunction`
  - 数値を受け取り、文字列を返す関数
- `AddMessageFunction`
  - JSON形式のペイロードを受け取り、1件の項目をDynamoDBテーブルに追加する関数
- `UpdateMemberFileFunction`
  - DynamoDBに項目が追加されたことをトリガーに、その内容に応じたデータをS3のCSVファイルに追加する関数
- `UpdateBookFileFunction`
  - DynamoDBに項目が追加されたことをトリガーに、その内容に応じたデータをS3のCSVファイルに追加する関数
  - 対象のテーブルはこのSAMアプリに含まれる想定ではないので、予め作っておく必要がある(後述)

## LocalStackへのデプロイ

1. `sam build --config-env local` または `samlocal build --config-env local` でビルド
2. `samlocal deploy --config-env local` でLocalStackにデプロイ

```bash
# ビルド時の sam コマンドは samlocal コマンドでも可
sam build --config-env local --use-container

# デプロイは samlocal
samlocal deploy --config-env local --guided
```

## Lambdaの実行

- `awslocal` コマンドは `aws --profile xxxxx --endpoint-url http://localhost:4566` のように、パラメータ付きの `aws` コマンドでも可
- `lambda invoke` でLambdaを実行する前に、 `lambda list-functions` コマンドでLambdaが正しくデプロイされているかご確認下さい

### HelloWorldFunction

- HTTPステータスコード200とメッセージを返すだけの関数です

```bash
# 関数が作成されているか確認
awslocal lambda list-functions
awslocal lambda get-function --function-name "sample-sam-app-HelloWorldFunction-93a343b8"

# 関数を実行してレスポンスを確認
awslocal lambda invoke --function-name "sample-sam-app-HelloWorldFunction-93a343b8" /tmp/response-helloworld.json
```

### SimpleResponseFunction

- 実行時にペイロードで渡した数値に対応するHTTPステータスコードとメッセージを返す関数です
- REST APIとして、GETメソッドで呼び出される想定です
- 下記のようにcURLでもリクエストをかけられますが android/ にあるプロジェクトをビルドしてできるAndroidアプリからも呼び出すことができます
  - Androidアプリからリクエストをかける場合は、SAMアプリをデプロイした上で後述の手順を実施してください

```bash
# 関数が作成されているか確認
awslocal lambda list-functions
awslocal lambda get-function --function-name "sample-sam-app-SimpleResponseFunction-96533490"

# REST API ID を確認
awslocal apigateway get-rest-apis

# cURLのGETパラメータで number を指定して呼び出す
curl "http://localhost:4566/restapis/<REST-API-ID>/simple_response/_user_request_/simple_response?number=3"
```

#### Androidアプリからリクエストをかける場合

1. android/ ディレクトリにあるAndroidプロジェクトをAndroid Studioで開く
2. const.kt にある3つの定数の値を環境に合わせて変更
3. アプリをビルドして実行

### AddMessageFunction

- 実行時に渡したペイロードに応じて、1件の項目を Message というDynamoDBテーブルに追加する関数です

```bash
# 関数が作成されているか確認
awslocal lambda list-functions
awslocal lambda get-function --function-name "sample-sam-app-SimpleDynamodbFunction-cdd357d1"

# 適当なペイロードを与えて関数を実行
awslocal lambda invoke \
  --function-name "sample-sam-app-local-AddMessageFunction-01e7712a" \
  --payload $(echo '{"sender":"Taro","receiver":"Jiro","message":"Hello, world!!"}' | base64) \
  /tmp/response-dynamodb.json
```

### UpdateMemberFileFunction

- Member というDynamoDBテーブルに項目が追加されたことをトリガーに、その内容に応じたデータをS3上のCSVファイルに追加する関数です

```bash
# put-item で Member にデータを投入
awslocal dynamodb put-item \
  --table-name Member \
  --item '{"seq":{"N":"1"},"name":{"S":"Taro"},"age":{"N":"30"},"sex":{"S":"MALE"}}'
  
# データができているか、できていたらその中身が期待通りか確認
awslocal dynamodb scan --table-name Member
awslocal s3 ls s3://sample-app-bucket
awslocal s3 cp s3://sample-app-bucket/members.csv ~/Downloads/members-copy.csv
cat ~/Downloads/members-copy.csv
```

### UpdateBookFileFunction

- Book という **既存のDynamoDBテーブル** に項目が追加されたことをトリガーに、その内容に応じたデータをS3上のCSVファイルに追記する関数です
- この関数は `Book` テーブルが存在する前提ですので、**SAMアプリをビルド＆デプロイする前**に作成しておく必要があります
  - 先述の『LocalStackへのデプロイ』を実施する前に、『Book テーブルの作成と UpdateBookFileFunction 関数の有効化』を実施してください

#### Book テーブルの作成と UpdateBookFileFunction 関数の有効化

1. Book という DynamoDB を事前に作成
2. 1の結果 DynamoDB Streams のARNを確認
3. `UpdateBookFileFunction` の定義は全てコメントアウトしているので template.yaml のコメントを全て外す
4. 2で確認したARNを samconfigm.toml にある `local.global.parameters` の `parameter_overrides` に含まれる `BookTableStreamArn` にセット

```bash
# create-table の結果から LatestStreamArn を確認し、 samconfig.toml の parameter_overrides の BookTableStreamArn 値としてコピー
awslocal dynamodb create-table \
  --table-name Book \
  --attribute-definitions '[{"AttributeName":"seq","AttributeType":"N"}]' \
  --key-schema '{"AttributeName":"seq","KeyType":"HASH"}' \
  --provisioned-throughput '{"ReadCapacityUnits": 5,"WriteCapacityUnits": 5}' \
  --stream-specification '{"StreamEnabled": true,"StreamViewType": "NEW_IMAGE"}'
  
# (補足) ARNを確認するのはこちらでも可
awslocal dynamodb describe-table --table-name Book

# DynamoDB Stream が有効になっているかの確認
awslocal dynamodbstreams describe-stream --stream-arn [any-stream-arn]
```

#### 動作確認

```bash
# put-item で Book にデータを投入
awslocal dynamodb put-item \
  --table-name Book \
  --item '{"seq":{"N":"1"},"title":{"S":"書籍のタイトル"},"price":{"N":"3740"},"publisher":{"S":"出版社名"}}'
  
# データができているか、できていたらその中身が期待通りか確認
awslocal dynamodb scan --table-name Book
awslocal s3 ls s3://sample-app-bucket
awslocal s3 cp s3://sample-app-bucket/books.csv ~/Downloads/books-copy.csv
cat ~/Downloads/books-copy.csv
```
