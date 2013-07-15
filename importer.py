import cPickle, neo4jconnector,simplejson, uuid,time
print 'reading rels'
rels = cPickle.load(open('relations.pickle'))
print 'reading nodes'
nodes = cPickle.load(open('nodes.pickle'))

print 'delete old'
g = neo4jconnector.BaseNeo4jConnector(debug=0)
g.query('match n-[r]->m delete r;')
g.query('match n delete n;')
g.commitTx()

dbnodes={}
dbrels={}
testing = 0

print
print 'processing nodes'
print
starttime = time.time()

i=0
statements = []
names = []
try:
    for nodename,nodedata in nodes.items():
        i+=1
        if testing and i>testing:
            break
        kw = {}
        nodedata['noscenda:name'] = nodename
        nodedata['noscenda:origin'] = 'dbp_m'
        nodedata['noscenda:uid'] = uuid.uuid4().hex
        for propname,propvalue in nodedata.items():
            if len(propvalue) == 1:
                propvalue=propvalue[0]
            kw[propname.replace(':','_')]=propvalue
        #import ipdb; ipdb.set_trace()
        statements.append(['create (n:node {kw}) return id(n) as nid;',dict(kw=kw)])
        names.append(nodename)
        if i%100==0:
            result = g.queryd(statements)
            for j in range(len(names)):
                dbnodes[names[j]]=result[j]['nid']
            statements=[]
            names=[]
        if i%1000==0:
            g.commitTx()
            print 'n ',i
    if len(statements):
        result = g.queryd(statements)
        for j in range(len(names)):
            dbnodes[names[j]]=result[j]['nid']
        print 'finally ',len(statements)
    g.commitTx()
except:
    g.rollbackTx()
    raise

timetaken = time.time() - starttime
print 'finished %s nodes after %s secs, %s per node' % (i,timetaken,timetaken/i)

print
print 'processing relations'
print 

starttime = time.time()
#import ipdb; ipdb.set_trace()
g.debug=0
i = 0
statements=[]
reltypes = set()
try:
    for origin,data in rels.items():
        for reltype,targets in data.items():
            rt = reltype.replace(':','_')
            reltypes.add(rt)
            for target in targets:
                i+=1   
                if testing and (origin not in dbnodes or target not in dbnodes):
                    continue
                uid=uuid.uuid4().hex
                kw = dict(noscenda_origin='dbp_m',
                          noscenda_uid=uid)
                statement = ['start n=node({origin}),m=node({target}) create unique n-[:`%s` {kw}]->m' % rt,dict(kw=kw,
                                                                                                                 origin=dbnodes[origin],
                                                                                                                 target=dbnodes[target])]
                statements.append(statement)
                if i%100==0 and len(statements)>=0:
                    result = g.query(statements)
                    statements=[]
                if i%1000==0:
                    g.commitTx()
                    print 'r',i
    if len(statements):
        result = g.query(statements)
        print 'finally ',len(statements)
    g.commitTx()
except:
    g.rollbackTx()
    raise
                    
timetaken = time.time() - starttime
print 'finished %s relations after %s secs, %s per relation' % (i,timetaken,timetaken/(i or 1))

print 'setting up indexes'

statements = ['create index on :node(noscenda_name)',
              'create index on :node(noscenda_uid)',
              'create index on :node(noscenda_origin)',
              'create index on :node(xmlns_name)']
for statement in statements:
    try:
        print statement, 
        g.query(statement)
        print 'ok'
    except:
        print 'failed', e
print 'done'        




