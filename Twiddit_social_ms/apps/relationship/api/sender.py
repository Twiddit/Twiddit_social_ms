#!/usr/bin/env python
import pika

class MQConnection():
    def __init__(self):
        self.connection = None
        self.channel = None 

    def createConnection(self, hostAdress, queueName):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostAdress))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queueName)

    def sendNotification(self, queueName, notificationBody):
        self.channel.basic_publish(exchange='', routing_key='notifications', body=notificationBody)
        print(" [x] Sent " + notificationBody)
    
    def closeConnection(self):
        self.connection.close()