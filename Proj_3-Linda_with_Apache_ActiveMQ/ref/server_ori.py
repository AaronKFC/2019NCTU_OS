import stomp
topic_name = '/topic/'
topic_ClientToServer = '/topic/ClientToServer'
topic_ServerToClient = '/topic/ServerToClient'
listener_name = 'SampleListener'
tupleSpace = []
#client request non-exist tuple
tmpIn = []
#client request non-exist tuple with "?"
tmpIn_wc = []
wildcard_str = '?'
wildcard_dic = {}
suspend_dic = {}
tmpClient = ""
tmpTuple = None
#搜尋的tuple不含變數
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
#搜尋的tuple含變數
def searchWild(tuple_wc, inputTuple):
    isMatch = True
    index = []
    index.append([])
    index.append([])
    for j in range(len(tuple_wc)):
        for i in range(len(tuple_wc[j])):
                if type(tuple_wc[j][i]) == str and tuple_wc[j][i].count(wildcard_str):
                    index[j].append(i)
    for j in range(len(tuple_wc)):
        if len(tuple_wc[j]) == len(inputTuple):
            for i in range(len(tuple_wc[j])):
                if i in index[j]:
                    continue
                if tuple_wc[j][i] != inputTuple[i]:
                    isMatch = False
            if isMatch:
                for i in index[j]:
                    keyForWc = tuple_wc[j][i].split('?')[1]
                    wildcard_dic[keyForWc] = inputTuple[i]
                suspend_dic[inputTuple] = suspend_dic.pop(tuple_wc[j])
                tmpIn_wc.remove(tuple_wc[j])
                return inputTuple
class SampleListener(object):
    def on_message(self, headers, message):
        global tmpIn, wildcard_str, tmpClient, tmpTuple
        clientID = headers['client']
        wildcard_idx = []
        #print('headers: ', headers['client'])
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
        #如果字串是數字就轉為數字
        for i in range(len(item)):
            if type(item[i]) == str and item[i].isnumeric():
                item[i] = int(item[i])
            tupleItem.append(item[i])
        #將list轉為tuple
        tupleItem = tuple(tupleItem)
        #偵測有沒有"?"
        for i in range(len(item)):
            if type(item[i]) == str and item[i].count(wildcard_str):
                wildcard_idx.append(i)
        #若有"?"便搜尋
        if len(wildcard_idx) > 0:
            searchTuple = search(tupleSpace, tupleItem, wildcard_idx)
            if searchTuple is not None:
                #suspend_dic[searchTuple] = suspend_dic.pop(tupleItem)
                tupleItem = searchTuple
            else:
                tmpIn_wc.append(tupleItem)
                suspend_dic[tupleItem] = clientID
                return
        #-----如果指令為out-----#
        if instruction == 'out':
            search_wc = searchWild(tmpIn_wc, tupleItem)
            if search_wc is not None:
                tupleItem = search_wc
                send_to_topic(topic_ServerToClient, ''.join(str(tupleItem)), suspend_dic[tupleItem])
                if tupleItem == tmpTuple:
                    suspend_dic[tupleItem] = tmpClient
                print('A client requested this tuple before')
            elif tupleItem in tmpIn:
                tmpIn.remove(tupleItem)
                send_to_topic(topic_ServerToClient, ''.join(str(tupleItem)), suspend_dic[tupleItem])
                if tupleItem == tmpTuple:
                    suspend_dic[tupleItem] = tmpClient
                print('A client requested this tuple before')
            else:
                send_to_topic(topic_name+tupleMsg, ''.join(str(tupleItem)), headers['client'])
                #新增資料到tupleSpace
                tupleSpace.append(tupleItem)
        #-----如果指令為in-----#
        elif instruction == 'in':
            if tupleItem in tupleSpace:
                send_to_topic(topic_ServerToClient, ''.join(str(tupleItem)), clientID)
                print('send tuple to client')
                tupleSpace.remove(tupleItem)
            else:
                tmpIn.append(tupleItem)
                if tupleItem not in suspend_dic:
                    suspend_dic[tupleItem] = clientID
                else:
                    tmpClient = clientID
                    tmpTuple = tupleItem
        #-----如果指令為read-----#
        elif instruction == 'read':
            if tupleItem in tupleSpace:
                send_to_topic(topic_ServerToClient, ''.join(str(tupleItem)), clientID)
                print('send tuple to client')
            else:
                tmpIn.append(tupleItem)
                if tupleItem not in suspend_dic:
                    suspend_dic[tupleItem] = clientID
                else:
                    tmpClient = clientID
                    tmpTuple = tupleItem
        #印出Tuple Space
        print("Tuple Space : ", tuple(tupleSpace))

#推送到主題
def send_to_topic(topic, msg, client):
    conn = stomp.Connection10([('ec2-54-80-14-165.compute-1.amazonaws.com', 61613)])
    conn.start()
    conn.connect()
    conn.send(topic, msg, headers={'client': client})
    conn.disconnect()
#從主題接收消息
def receive_from_topic():
    conn = stomp.Connection10([('ec2-54-80-14-165.compute-1.amazonaws.com', 61613)])
    conn.set_listener(listener_name, SampleListener())
    conn.start()
    conn.connect(wait = True)
    conn.subscribe(topic_ClientToServer)
    while True:
        pass
if __name__ == '__main__':
    print("Welcome to Linda server")
    receive_from_topic()

