t1 = []
f1 = open('clientA_lock.txt', 'r', encoding = 'UTF-8')
while True :
	i = f1.readline()
	if i=='': 
		break
	t1.append(int(i))
f1.close()
f2 = open('clientB_lock.txt', 'r', encoding = 'UTF-8')
while True :
	x = f2.readline()
	if x=='': 
		break
	t1.append(int(x))
f2.close()
t1.sort()
for y in range(99999):
	if t1[y] == t1[y+1]:
		print('race condition')
    else:
        print('no race condition')
