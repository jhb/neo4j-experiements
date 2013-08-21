import cPickle, neo4jrest,simplejson, sys,time, random

if len(sys.argv) < 4:
    print 'usage:%s number_of_persons number_of_hops repetitions' % sys.argv[0]
    sys.exit()

namerange,pathlength,repeats = sys.argv[1:4]
namerange = int(namerange)
pathlength=int(pathlength)
repeats = int(repeats)
# "match  p=n:node<-[*4..4]-m where n.noscenda_name='dbpedia:Berlin' return count(p);"

g = neo4jrest.Neo4jRestConnector(debug=0)
#g.debug=1
times = []
for i in range(0,repeats):
    print 'run %s' % i
    target = 'person%s' % random.randint(1,namerange+1)
    hops ='-[:friend]->()' * (pathlength-1)
    query = 'start person=node:node_auto_index(noscenda_name={target}) match (person)%s-[:friend]->(friend) return count(distinct friend);' % hops
    #query = 'start person=node:node_auto_index(noscenda_name={target}) match (person)%s-[:friend]->(friend) return count(friend);' % hops
    print query.replace('{target}',"'%s'" % target)
    #query = 'start n=node:node_auto_index(noscenda_name={target}) return count(n)'
    start = time.time()
    result = g.cypher(query,dict(target=target))
    tt = time.time()-start
    print tt
    times.append(tt)
    print 'starting at',target,'found rels: ', 
    print result['data'][0][0]
avg = sum(times)/len(times)
print
print 'average ',avg
