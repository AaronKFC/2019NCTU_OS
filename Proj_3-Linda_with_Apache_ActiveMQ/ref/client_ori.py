import stomp
import os
topic_ClientToServer = '/topic/ClientToServer'
topic_ServerToClient = '/topic/ServerToClient'
listener_name = 'SampleListener'
pid = str(os.getpid())

class SampleListener(object):
    def on_message(self, headers, message):
        #print('headers: %s' % headers)
        print('message: %s' % message)
        client()
#推送到主題
def send_to_topic(topic_name, msg):
    conn.send(topic_name, msg, headers={'client': pid})


#從主題接收消息
def receive_from_topic():
    conn = stomp.Connection10([('ec2-54-80-14-165.compute-1.amazonaws.com', 61613)])
    conn.set_listener(listener_name, SampleListener())
    conn.start()
    conn.connect(wait = True)
    conn.subscribe(topic_ServerToClient, headers={'selector': "client = " + pid})
    while True:
        pass
def client():
    while True:
        inputMsg = input("Send message to tuple space:")
        message = inputMsg.split(' ', 1)
        instruction = message[0]
        if instruction == 'out':
            send_to_topic(topic_ClientToServer, inputMsg)
        elif instruction == 'in':
            send_to_topic(topic_ClientToServer, inputMsg)
            print('Wait for server response...')
            receive_from_topic()
        elif instruction == 'read':
            send_to_topic(topic_ClientToServer, inputMsg)
            print('Wait for server response...')
            receive_from_topic()
        else:
            print('Usage fault')

if __name__ == '__main__':
    ##-----連接到ActiveMQ-----##
    conn = stomp.Connection10([('ec2-54-80-14-165.compute-1.amazonaws.com', 61613)])
    conn.start()
    conn.connect()
    ##-----------------------##
    client()















