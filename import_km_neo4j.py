import cPickle, neo4jconnector,simplejson, uuid,time



def add_nodes(nodenames,labels,text):
    print 'adding %s' % text
    labels.insert(0,'n')
    labelstring = ':'.join(labels)
    
    nids = []
    names = []
    nids = {}
    statements = []
    i = 1;

    for name in nodenames:
        statements.append(['create (%s{kw}) return id(n) as nid' % labelstring,{'kw':{'name':name}}])
        names.append(name)
        if not i%100:
            result = g.queryd(statements)
            for j in range(len(names)):
                nids[names[j]]=int(result[j]['nid'])
            statements = []
            names = []
        
        if not i%1000:
            g.commitTx()
            print '%s: %s' % (text,i)
        i+=1

    if len(statements):
        print '%s final: %s' % (text,len(statements))
        result = g.queryd(statements)
        for j in range(len(names)):
            nids[names[j]]=int(result[j]['nid'])

    g.commitTx()
    return nids

def add_links(links,text):
    i = 0;
    statements = []
    print 'adding %s relations' % text
    for link in links:
        i+=1
        query = 'start n=node({origin}),m=node({target}) create unique n-[:%s]->m' % link[2]
        data = dict(origin=link[0],target=link[1])
        statements.append([query,data])
        if not i%100:
            g.query(statements)
            statements=[]
        if not i%1000:
            g.commitTx()
            print '%s: %s' % (text,i)
    if len(statements):
         g.query(statements)
         print 'final %s: %s' % (text,len(statements))
    g.commitTx()


ntypes = ['node','person','article','topic','project']
print 'deleting'
g = neo4jconnector.BaseNeo4jConnector(debug=0)
g.query('match n-[r]->m delete r;')
g.query('match n delete n;')
for ntype in ntypes:
    try:
        query = 'drop index on :%s(name)' % ntype
        print query,
        g.query(query)
        print 'ok'
    except:
        print 'e'
        pass        
g.commitTx()

print 'reading kmdata'
kmdata = cPickle.load(open('kmdata.pickle'))

person_nids = add_nodes(kmdata['people'].keys(),['node','person'],'people')
topic_nids = add_nodes(kmdata['topics'],['node','topic'],'topics')
article_nids = add_nodes(kmdata['articles'].keys(),['node','article'],'articles')
project_nids = add_nodes(kmdata['projects'].keys(),['node','project'],'projects')




if 1:
    links = []
    for person,topics in kmdata['people'].items():
        for topic in topics:
            links.append([person_nids[person],topic_nids[topic],'topic'])
    add_links(links,'people topics')    

if 1:
    authorlinks = []
    topiclinks = []
    print 'preparing article data'
    i=0;
    for article,data in kmdata['articles'].items():
        i+=1
        if not i % 1000:
            print 'preparing article %s' % i
        for topic in data['topics']:
            topiclinks.append([article_nids[article],topic_nids[topic],'topic'])
        authorlinks.append([article_nids[article],person_nids[data['author']],'author'])
    add_links(authorlinks,'authors')
    add_links(topiclinks,'article topics')    

if 1:
    memberlinks = []
    topiclinks = []
    print 'preparing project data'
    for projectname,data in kmdata['projects'].items():
        for membername in data['members']:
            memberlinks.append([project_nids[projectname],person_nids[membername],'member'])
        for topic in data['topics']:
            topiclinks.append([project_nids[projectname],topic_nids[topic],'topic'])

    add_links(memberlinks,'membership')
    add_links(topiclinks,'project topics') 
print 'fini'



for ntype in ntypes:
    try:
        query = 'create index on :%s(name)' % ntype
        print query,
        g.query(query)
        print 'ok'
    except:
        print 'e'
        pass        
g.commitTx()

