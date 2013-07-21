import MySQLdb
import cPickle, time, uuid
db = MySQLdb.connect("localhost","friends","","friends" )
print 'deleting'
c = db.cursor()
c.execute('delete from t_user;')
c.execute('delete from t_user_friend;')
db.commit()

print 'reading friends'
friends = cPickle.load(open('friends.pickle'))
i = 0
for a,flist in friends.items():
    c.execute("insert into t_user values (%s,'person%s');" % (a,a))
    for b in flist:
        i+=1
        c.execute("insert into t_user_friend values (%s,%s,%s);" % (i,a,b))
    db.commit()
    if a%1000==0:
        print a
print 'fini'


