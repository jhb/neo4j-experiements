import cPickle, random,pprint
max = 100000
num = 50

friendids = range(1,max+1)
friends={}
for i in range(1,max+1):
    possible = list(friendids)
    possible.pop(i-1) #remove i itself
    friends[i]=random.sample(possible,num)
cPickle.dump(friends,open('friends.pickle','w'))
    
