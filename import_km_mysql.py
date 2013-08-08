import MySQLdb
import cPickle, time, uuid, sys

if len(sys.argv) < 2:
    filename = 'kmdata.pickle'
else:
    filename = sys.argv[1]

db = MySQLdb.connect("localhost","km","","km" )
print 'deleting'
c = db.cursor()
c.execute('delete from topic;')
c.execute('delete from article;')
c.execute('delete from person;')
c.execute('delete from project;')
c.execute('delete from node;')
c.execute('delete from edge;')

print 'reading'
f = open(filename)
kmdata = cPickle.load(f)
f.close()
#  c.execute("insert into t_user values (%s,'person%s');" % (a,a))

print 'topics'
i = 0
for name in kmdata['topics']:
    i+=1
    id = int(name[5:])
    c.execute("insert into topic values (%s,'%s');" % (id,name))
    if not i % 1000:
        print 'topic: ',i

print 'people'
i = 0
for name,data in kmdata['people'].items():
    i+=1
    id = int(name[6:])
    c.execute("insert into person values (%s,'%s');" % (id,name))
    for topic in data:
        tid = int(topic[5:])
        c.execute("insert into edge values (NULL,'person',%s,'topic','%s','topic');" % (id,tid))
    if not i % 1000:
        print 'person: ',i

print 'projects'
i = 0
for name,data in kmdata['projects'].items():
    i+=1
    id = int(name[7:])
    c.execute("insert into project values (%s,'%s');" % (id,name))
    for topic in data['topics']:
        tid = int(topic[5:])
        c.execute("insert into edge values (NULL,'project',%s,'topic','%s','topic');" % (id,tid))
    for membername in data['members']:
        mid = int(membername[6:])
        c.execute("insert into edge values (NULL,'project',%s,'person','%s','member');" % (id,mid))
    if not i % 1000:
        print 'project: ',i

print 'articles'
i = 0
for name,data in kmdata['articles'].items():
    i+=1
    id = int(name[7:])
    c.execute("insert into article values (%s,'%s');" % (id,name))
    for topic in data['topics']:
        tid = int(topic[5:])
        c.execute("insert into edge values (NULL,'article',%s,'topic','%s','topic');" % (id,tid))
    aid = int(data['author'][6:])
    c.execute("insert into edge values (NULL,'article',%s,'person','%s','author');" % (id,aid))
    if not i % 1000:
        print 'article: ',i

