import cPickle, neo4jrest,simplejson, uuid,time, sys

if len(sys.argv) < 2:
    filename = 'friends.pickle'
else:
    filename = sys.argv[1]

g = neo4jrest.Neo4jRestConnector(debug=0)
print 'deleting'
g.cypher('start r=relationship(*) delete r')
g.cypher('start n=node(*) delete n')

print 'reading friends'
f = open(filename)
friends = cPickle.load(f)
f.close()

print 'adding nodes'
nids = {}
g.debug=0

statements = []
names = []
p = 0
size = 1000
for a,targets in friends.items():
    name = 'person%s' % a
    statements.append(dict(noscenda_name=name))
    names.append(a)
    if a%size == 0:
        result = g.create_nodes(statements)
        for j in range(len(names)):
            nids[names[j]]=result[j]
        statements = []
        names = []
    if a%(size*10) ==0:
        print 'n ',a
if len(statements):
    result = g.create_nodes(statements)
    for j in range(len(names)):
        nids[names[j]]=result[j]
    print 'final ', len(statements)

print 'adding relations'
i = 0
size = 10000
for a,targets in friends.items():
    for b in targets:
        i+=1
        statements.append([nids[a],nids[b],'friend',None])
        if i%size == 0:
            g.create_relationships(statements)
            statements=[]
        if i%(size*10) ==0:
            print 'r ',i
if len(statements):
    g.create_relationships(statements)
    print 'final ',len(statements)
print 'fini'        
