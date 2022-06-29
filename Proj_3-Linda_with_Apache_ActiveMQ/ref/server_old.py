import stomp

topic_name = '/topic/'
topic_ClientToServer = '/topic/ClientToServer'
topic_ServerToClient = '/topic/ServerToClient'
listener_name = 'SampleListener'
tupleSpace = []
#client request non-exist tuple
tmpIn = []
tmpIn_wc = []
wildcard_str = '?'
wildcard_dic = {}
def search(tuple_space, inputTuple, index):
    isMatch = True
    for tuples in tuple_space:
        if len(tuples) == len(inputTuple):
            for i in range(len(tuples)):
                if i in index:
                    continue
                if tuples[i] != inputTuple[i]:
                    isMatch = False
            if isMatch:
                for i in index:
                    keyForWc = inputTuple[i].split('?')[1]
                    wildcard_dic[keyForWc] = tuples[i]
                return tuples
class SampleListener(object):
    def on_message(self, headers, message):
        global tmpIn, wildcard_str
        wildcard_idx = []
        var_idx = []
        #print ('headers: %s' % headers)
        print('message: %s' % message)
        message = message.split(' ', 1)
        #指令為out/in/read
        instruction = message[0]
        #tuple
        tupleMsg = message[1]
        #tuple中的每樣元素
        item = tupleMsg.split(' ')
        tupleItem = []
        #如果字串為變數便改為值
        for i in item:
            if i in wildcard_dic:
                idx = item.index(i)
                item[idx] = wildcard_dic[item[idx]]
                var_idx.append(idx)
        #如果字串是數字就轉為數字
        for i in range(len(item)):
            if type(item[i]) == str and item[i].isnumeric():
                item[i] = int(item[i])
            tupleItem.append(item[i])
        #偵測有沒有"?"
        for i in range(len(item)):
            if type(item[i]) == str and item[i].count(wildcard_str):
                wildcard_idx.append(i)
        #若有"?"便搜尋
        if len(wildcard_idx) > 0:
            searchTuple = search(tupleSpace, tupleItem, wildcard_idx)
            if searchTuple is not None:
                tupleItem = searchTuple
            else:
                tmpIn_wc.append(tupleItem)
                return
        #將list轉為tuple
        tupleItem = tuple(tupleItem)
        #-----如果指令為out-----#
        if instruction == 'out':
            for tuples in tmpIn_wc:
                searchTuple = search(tupleSpace, tuples, var_idx)
                if searchTuple is not None:
                    tupleItem = searchTuple
            if tupleItem in tmpIn:
                tmpIn.remove(tupleItem)
                send_to_topic(topic_ServerToClient, ''.join(str(tupleItem)))
                print('A client requested this tuple before')
                #break
            else:
                send_to_topic(topic_name+tupleMsg, ''.join(str(tupleItem)))
                #新增資料到tupleSpace
                tupleSpace.append(tupleItem)
        #-----如果指令為in-----#
        elif instruction == 'in':
            if tupleItem in tupleSpace:
                send_to_topic(topic_ServerToClient, ''.join(str(tupleItem)))
                print('send tuple to client')
                tupleSpace.remove(tupleItem)
            else:
                tmpIn.append(tupleItem)
        #-----如果指令為read-----#
        elif instruction == 'read':
            if tupleItem in tupleSpace:
                send_to_topic(topic_ServerToClient, ''.join(str(tupleItem)))
                print('send tuple to client')
        #印出Tuple Space
        print("Tuple Space : ", tuple(tupleSpace))


#推送到主題
def send_to_topic(topic, msg):
    conn = stomp.Connection10([('ec2-34-207-213-221.compute-1.amazonaws.com', 61613)])
    conn.start()
    conn.connect()
    conn.send(topic, msg)
    conn.disconnect()
#從主題接收消息
def receive_from_topic():
    conn = stomp.Connection10([('ec2-34-207-213-221.compute-1.amazonaws.com', 61613)])
    conn.set_listener(listener_name, SampleListener())
    conn.start()
    conn.connect(wait = True)
    conn.subscribe(topic_ClientToServer)
    while True:
        pass
if __name__ == '__main__':
    print("Welcome to Linda server")
    receive_from_topic()

