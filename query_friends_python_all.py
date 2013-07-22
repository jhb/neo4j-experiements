import cPickle, sys,time,random

repeats = 3

print 'reading'
friends = cPickle.load(open('friends.pickle'))


print 'searching'
for pathlength in range(1,6):
    for i in range(repeats):
        start = time.time()
        a = random.randint(1,100001)
        print 'start at',a,'search depth',pathlength, 
        startingpoints = [a]
        x = 0
        for j in range(pathlength):
            paths = 0
            results = set()
            for k in startingpoints:
                results.update(friends[k])
                paths+=len(friends[k])
            startingpoints=results     
        print 'found',len(results),'after', time.time()-start,'secs, num paths:',paths
print 'fini'        



