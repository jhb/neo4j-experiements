import cPickle, neo4jconnector,simplejson, uuid,time

print 'deleting'
g = neo4jconnector.BaseNeo4jConnector(debug=0)
g.query('match n-[r]->m delete r;')
g.query('match n delete n;')
g.commitTx()

print 'reading friends'
friends = cPickle.load(open('friends.pickle'))

print 'adding nodes'
nids = {}
g.debug=0

statements = []
names = []
for a,targets in friends.items():
    name = 'person%s' % a
    statements.append(['create (n:node{kw}) return id(n) as nid',dict(kw=dict(noscenda_name=name))])
    names.append(a)
    if a%100 == 0:
        result = g.queryd(statements)
        for j in range(len(names)):
            nids[names[j]]=int(result[j]['nid'])
        statements = []
        names = []
    if a%1000 ==0:
        g.commitTx()
        print 'a ',a
if len(statements):
    result = g.queryd(statements)
    for j in range(len(names)):
        nids[names[j]]=result[j]['nid']
    print 'final ', len(statements)
g.commitTx()  
print 'adding relations'
i = 0
for a,targets in friends.items():
    for b in targets:
        i+=1
        statements.append(['start n=node({origin}),m=node({target}) create unique n-[:friend]->m',dict(origin=nids[a],target=nids[b])])
        if i%100 == 0:
            g.query(statements)
            statements=[]
        if i%1000 ==0:
            g.commitTx()
            print 'r ',i
if len(statements):
    g.query(statements)
    print 'final ',len(statements)
g.commitTx()
print 'fini'        
