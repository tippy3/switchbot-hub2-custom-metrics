import cloudwatch
import switchbot


def lambda_handler(event, context):
  data = switchbot.get_data()
  temperature = data['temperature']
  humidity = data['humidity']
  light_level = data['lightLevel']

  cloudwatch.post_data(temperature, humidity, light_level)


if __name__ == "__main__":
  lambda_handler(None, None)
  print('success')
