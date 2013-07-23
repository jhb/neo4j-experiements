import os,jpype,time,random, cPickle
os.environ['NEO4J_PYTHON_JVMARGS'] = '-Xms4G -Xmx8G -XX:MaxPermSize=1G'
os.environ['JAVA_HOME']='/usr/lib/jvm/jdk1.7.0/'

from neo4j import GraphDatabase
db = GraphDatabase('data')

print 'deleting'
with db.transaction:
    db.query('start r=relationship(*) delete r');
    db.query('start n=node(*) delete n;')

print 'reading'
friends = cPickle.load(open('friends.pickle'))

print 'nodes'
nodes = {}
with db.transaction:
    for a,data in friends.items():
        n = db.node(noscenda_name='person%s'%a)
        nodes[a]=n
        if a%1000==0:
            print 'n ',a

print 'relations'
frienditems = friends.items()
i = 1
p = 0
slicesize = 1000
while p<len(frienditems):
    items = frienditems[p:p+slicesize]
    with db.transaction:
        print 'transaction itemslice start: ',p
        for a,targets in items:
            for b in targets:
                i+=1
                getattr(nodes[a],'friend')(nodes[b])
                if i%10000==0:
                    print 'r ',i
    p+=slicesize
print 'fini'
