import cPickle, neo4jconnector,simplejson, sys,time, random

if len(sys.argv) < 3:
    print 'usage:%s number_of_hops repetitions' % sys.argv[0]
    sys.exit()

pathlength,repeats = sys.argv[1:3]
pathlength=int(pathlength)
repeats = int(repeats)
# "match  p=n:node<-[*4..4]-m where n.noscenda_name='dbpedia:Berlin' return count(p);"

g = neo4jconnector.BaseNeo4jConnector(debug=0)
#g.debug=1
times = []
for i in range(0,repeats):
    print 'run %s' % i
    target = 'person%s' % random.randint(1,10001)
    start = time.time()
    result = g.queryd([['match n:node-[r*%s..%s]->m:node where n.noscenda_name={target} return count(r);' % (pathlength,pathlength),
                       dict(target=target)]])
    tt = time.time()-start
    print tt
    times.append(tt)
    print target, 
    print result[0]['count(r)']
avg = sum(times)/len(times)
print 'average ',avg
