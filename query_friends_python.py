import cPickle, sys,time,random


if len(sys.argv) < 3:
    print 'usage:%s number_of_hops repetitions' % sys.argv[0]
    sys.exit()

pathlength,repeats = sys.argv[1:3]
pathlength=int(pathlength)
repeats = int(repeats)

print 'reading'
friends = cPickle.load(open('friends.pickle'))

print 'searching'
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



