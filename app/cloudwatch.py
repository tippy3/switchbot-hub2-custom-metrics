import boto3

def post_data(temperature, humidity, light_level):
  # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/put_metric_data.html

  namespace = 'Switchbot'
  dimentions = [
    {
      'Name': 'DeviceName',
      'Value': 'hub2'
    }
  ]
  metric_data = [
    {
      'MetricName': 'Temperature',
      'Value': temperature,
      'Unit': 'Count',
      'Dimensions': dimentions
    },
    {
      'MetricName': 'Humidity',
      'Value': humidity,
      'Unit': 'Percent',
      'Dimensions': dimentions
    },
    {
      'MetricName': 'LightLevel',
      'Value': light_level,
      'Unit': 'Count',
      'Dimensions': dimentions
    },
  ]

  cloudwatch = boto3.client('cloudwatch')

  cloudwatch.put_metric_data(Namespace = namespace, MetricData = metric_data)


if __name__ == "__main__":
  post_data(28.5, 65, 10)
  print('success')
