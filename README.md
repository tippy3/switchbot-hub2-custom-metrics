# switchbot

Switchbot Hub 2 の気温・湿度・照度をAmazon CloudWatchにカスタムメトリクスとして送信するコード。

AWS LambdaとAmazon EventBridgeで定期実行しています。

## 参考

- https://github.com/aws/aws-secretsmanager-caching-python
- https://github.com/OpenWonderLabs/SwitchBotAPI
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/put_metric_data.html
- https://tgctkkz.com/763
