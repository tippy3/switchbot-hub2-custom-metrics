# Switchbot Hub 2 -> AWS CloudWatch

Switchbot Hub 2 の気温・湿度・照度をAmazon CloudWatchにカスタムメトリクスとして送信するPythonコード

LambdaとEventBridgeで5分ごとに定期実行しています

## 使い方

**#1** [app/switchbot.py](app/switchbot.py)で使う3つのシークレットをAWS Secrets Managerに登録します

マネジメントコンソール → Secrets Manager → Secrets → Store a new secret

シークレット名: `switchbot`

|Key|説明|
|---|---|
|`token`|SwitchbotアカウントのToken|
|`secret`|SwitchbotアカウントのSecret Key|
|`device_id`|Switchbot Hub 2のDevice ID|

**#2** ソースコードと外部ライブラリをそれぞれzip化します

```bash
./zip.sh
```

**#3** AWSリソースを全て作ります

```bash
./create_aws_resources.sh
```

## クリーンアップ

全てのAWSリソースを削除するには次のようにします。デプロイが途中で失敗した場合もこれで最初からやり直せます

```bash
./delete_aws_resources.sh
```

## 参考

- PythonでSecrets Managerのシークレットを取得する
  - https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets_cache-python.html
  - https://github.com/aws/aws-secretsmanager-caching-python
- SwitchBotAPIを叩くときのリクエストヘッダー
  - https://github.com/OpenWonderLabs/SwitchBotAPI
- PythonでCloudWatchにカスタムメトリクスを送る
  - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/put_metric_data.html
  - https://tgctkkz.com/763
    - ↑ Namespace, Dimensions, MetricName の図説がわかりやすいです
