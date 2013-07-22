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
    paths = []
    startingpoints = [a]
    for j in range(pathlength):
        results = set()
        for k in startingpoints:
            results.update(friends[k])
        startingpoints=results     
    print 'found',len(results),'after', time.time()-start
print 'fini'        



