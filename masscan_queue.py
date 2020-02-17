import pika
import json
import re
import sys
import os
from dotenv import load_dotenv
load_dotenv()


credentials = pika.PlainCredentials(os.environ['RABBIT_USER'], os.environ['RABBIT_PW'])
parameters = pika.ConnectionParameters(os.environ['RABBIT_HOST'],
                                       os.environ['RABBIT_PORT'],
                                       os.environ['RABBIT_VHOST'],
                                       credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=os.environ['RABBIT_QUEUE'], durable=True)

res = re.compile(r'(\d+)\/.+ (\d+.\d+.\d+.\d+)')

for line in sys.stdin:
    result = res.search(line)
    if not result:
        continue
    port = result.group(1)
    ip = result.group(2)
    message_dict = {
        'ip': ip,
        'port': int(port)
    }
    channel.basic_publish(exchange='',
                      routing_key=os.environ['RABBIT_QUEUE'],
                      body=json.dumps(message_dict))
    print('published', message_dict)