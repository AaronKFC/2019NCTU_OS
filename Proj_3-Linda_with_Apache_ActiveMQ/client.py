import stomp
import os
pid = str(os.getpid())
listenName = 'Listener'
topic_CtoS = '/topic/Client_To_Server'
topic_StoC = '/topic/Server_To_Client'


class SampleListener(object):
    def on_message(self, headers, message):
        print('message: %s' % message)
        clt()

def clt():
    while True:
        inMsg = input("Key in msg (to tuple space):")
        message = inMsg.split(' ', 1)
        msg_in = message[0]
        if msg_in == 'out':
            sendmsg_to_topic(topic_CtoS, inMsg)
        elif msg_in == 'read':
            sendmsg_to_topic(topic_CtoS, inMsg)
            print('Waiting response from server...')
            receivemsg_from_topic()
        elif msg_in == 'in':
            sendmsg_to_topic(topic_CtoS, inMsg)
            print('Waiting response from server...')
            receivemsg_from_topic()
        else:
            print('Wrong usage')


#receive msg from topic
def receivemsg_from_topic():
    connect = stomp.Connection10([('ec2-54-80-14-165.compute-1.amazonaws.com', 61613)])
    connect.set_listener(listenName, SampleListener())
    connect.start()
    connect.connect(wait = True)
    connect.subscribe(topic_StoC, headers={'selector': "client = " + pid})
    while True:
        pass


#send msg to topic
def sendmsg_to_topic(topicName, msg):
    connect.send(topicName, msg, headers={'client': pid})


if __name__ == '__main__':
    ##-----connect to ActiveMQ
    connect = stomp.Connection10([('ec2-54-80-14-165.compute-1.amazonaws.com', 61613)])
    connect.start()
    connect.connect()

    clt()

