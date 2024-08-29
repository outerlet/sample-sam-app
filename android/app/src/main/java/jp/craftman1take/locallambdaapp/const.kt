package jp.craftman1take.locallambdaapp

/*
 * LocalStackを動かしているマシンのIPアドレス
 */
const val LOCALSTACK_HOST_IP_ADDRESS = "192.168.0.140"

/*
 * LocalStackがListenしているポート番号
 * 初期状態のままなら変更は不要
 */
const val LOCALSTACK_PORT = 4566

/*
 * `awslocal apigateway get-rest-apis` で確認できる REST API ID
 */
const val REST_API_ID = "hek5sjhko5"
