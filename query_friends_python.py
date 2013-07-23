import cPickle, sys,time,random

if len(sys.argv) < 5:
    print 'usage:%s filename number_of_persons number_of_hops repetitions' % sys.argv[0]
    sys.exit()

filename,namerange,pathlength,repeats = sys.argv[1:5]
namerange = int(namerange)
pathlength=int(pathlength)
repeats = int(repeats)


print 'reading'
friends = cPickle.load(open(filename))

print 'searching'
times = []
for i in range(repeats):
    start = time.time()
    a = random.randint(1,namerange+1)
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
    tt = time.time()-start
    times.append(tt)
    print 'found',len(results),'after', tt,'secs, num paths:',paths
avg = sum(times)/len(times)
print 'average ',avg     
print 'fini'        



