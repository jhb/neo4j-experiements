import cPickle, random,pprint
max = 100000
num = 50

friendids = range(1,max+1)
friends={}
for i in range(1,max+1):
    while 1:
        sample = random.sample(friendids,num)
        if i not in sample:
            break
    friends[i]=sample
    if i % 10000 == 0:
        print i
#pprint.pprint(friends)        
cPickle.dump(friends,open('friends.pickle','w'))
    
