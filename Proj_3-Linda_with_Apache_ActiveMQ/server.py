import stomp
listenerName = 'Listener'
topic_name = '/topic/'
topic_CtoS = '/topic/Client_To_Server'
topic_StoC = '/topic/Server_To_Client'
tupleSpace = []
tmpC = ""
tmpTp = None
#client request non-exist tuple
tmpIn = []
#client request non-exist tuple with "?"
tmpIn_wc = []
wc_str = '?'
wc_dic = {}
susp_dic = {}

#search tuple without variable
def search(tuple_space, inTuple, index):
    Match = True
    for tp in tuple_space:
        if len(tp) == len(inTuple):
            for i in range(len(tp)):
                if i in index:
                    continue
                if tp[i] != inTuple[i]:
                    Match = False
            if Match:
                for i in index:
                    keyForWc = inTuple[i].split('?')[1]
                    wc_dic[keyForWc] = tp[i]
                return tp

#search tuple including variable
def searchWildcard(tuple_wc, inTuple):
    Match = True
    index = []
    index.append([])
 #   index.append([])

    for j in range(len(tuple_wc)):
        for i in range(len(tuple_wc[j])):
                if tuple_wc[j][i].count(wc_str) and type(tuple_wc[j][i]) == str:
                    index[j].append(i)

    for j in range(len(tuple_wc)):
        if len(inTuple) == len(tuple_wc[j]):
            for i in range(len(tuple_wc[j])):
                if i in index[j]:
                    continue
                if tuple_wc[j][i] != inTuple[i]:
                    Match = False

            if Match:
                for i in index[j]:
                    keyForWc = tuple_wc[j][i].split('?')[1]
                    wc_dic[keyForWc] = inTuple[i]
                susp_dic[inTuple] = susp_dic.pop(tuple_wc[j])
                tmpIn_wc.remove(tuple_wc[j])
                return inTuple

class SampleListener(object):
    def on_message(self, headers, message):
        global tmpIn, wc_str, tmpC, tmpTp
        cltID = headers['client']
        wc_idx = []
        print('msg from client: %s' % message)
        message = message.split(' ', 1)
        #command is out/in/read
        msg_in = message[0]
        #tuple
        tupleMsg = message[1]
        #every element in tuple
        item = tupleMsg.split(' ')
        tpItem = []
        # turn the string to value if the string is a variable 
        for i in item:
            if i in wc_dic:
                idx = item.index(i)
                item[idx] = wc_dic[item[idx]]
        #turn the string to number if it is a number
        for i in range(len(item)):
            if type(item[i]) == str and item[i].isnumeric():
                item[i] = int(item[i])
            tpItem.append(item[i])
        #transform the list to tuple
        tpItem = tuple(tpItem)
        # detect whether "?" exists
        for i in range(len(item)):
            if type(item[i]) == str and item[i].count(wc_str):
                wc_idx.append(i)
        #search if "?" exists
        if len(wc_idx) > 0:
            searchTp = search(tupleSpace, tpItem, wc_idx)
            if searchTp is not None:
                tpItem = searchTp
            else:
                tmpIn_wc.append(tpItem)
                susp_dic[tpItem] = cltID
                return

        #-----if command is 'out'-----#
        if msg_in == 'out':
            search_wc = searchWildcard(tmpIn_wc, tpItem)
            if search_wc is not None:
                tpItem = search_wc
                sendmsg_to_topic(topic_StoC, ''.join(str(tpItem)), susp_dic[tpItem])
                if tpItem == tmpTp:
                    susp_dic[tpItem] = tmpC
                print('This tuple was requested before')
            elif tpItem in tmpIn:
                tmpIn.remove(tpItem)
                sendmsg_to_topic(topic_StoC, ''.join(str(tpItem)), susp_dic[tpItem])
                if tpItem == tmpTp:
                    susp_dic[tpItem] = tmpC
                print('This tuple was requested before')
            else:
                # sendmsg_to_topic(topic_name+tupleMsg, ''.join(str(tpItem)), headers['client'])
                sendmsg_to_topic(topic_name+tupleMsg, ''.join(str(tpItem)), cltID)
                #add new data to tupleSpace
                tupleSpace.append(tpItem)

        #-----if command is 'read'-----#
        elif msg_in == 'read':
            if tpItem in tupleSpace:
                sendmsg_to_topic(topic_StoC, ''.join(str(tpItem)), cltID)
                print('send tuple data to the client')
            else:
                tmpIn.append(tpItem)
                if tpItem not in susp_dic:
                    susp_dic[tpItem] = cltID
                else:
                    tmpC = cltID
                    tmpTp = tpItem

        #-----if command is 'in'-----#
        elif msg_in == 'in':
            if tpItem in tupleSpace:
                sendmsg_to_topic(topic_StoC, ''.join(str(tpItem)), cltID)
                print('send tuple data to the client')
                tupleSpace.remove(tpItem)
            else:
                tmpIn.append(tpItem)
                if tpItem not in susp_dic:
                    susp_dic[tpItem] = cltID
                else:
                    tmpC = cltID
                    tmpTp = tpItem

        print("Tuple Space : ", tuple(tupleSpace))


#receive msg from topic
def receivemsg_from_topic():
    connect = stomp.Connection10([('ec2-54-80-14-165.compute-1.amazonaws.com', 61613)])
    connect.set_listener(listenerName, SampleListener())
    connect.start()
    connect.connect(wait = True)
    connect.subscribe(topic_CtoS)
    while True:
        pass

#Send msg to topic
def sendmsg_to_topic(topic, msg, client):
    connect = stomp.Connection10([('ec2-54-80-14-165.compute-1.amazonaws.com', 61613)])
    connect.start()
    connect.connect()
    # connect.send(topic, msg, headers={'client': pid})
    connect.send(topic, msg, headers={'client': client})
    connect.disconnect()


if __name__ == '__main__':
    print("Linda server is in progress")
    receivemsg_from_topic()

