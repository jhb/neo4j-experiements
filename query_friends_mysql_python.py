import MySQLdb
import cPickle, time, uuid, sys, random
db = MySQLdb.connect("localhost","friends","","friends" )

if len(sys.argv) < 3:
    print 'usage:%s number_of_hops repetitions' % sys.argv[0]
    sys.exit()


pathlength,repeats = sys.argv[1:3]


pathlength=int(pathlength)
repeats = int(repeats)

for i in range(0,repeats):
    print 'run %s' % i
    target = 'person%s' % random.randint(1,10001)
    c = db.cursor()
    start = time.time()
    c.execute("select id from t_user where name=%s",(target,))
    id = c.fetchone()[0]
    ids = set([str(id)])
    for i in range(0,pathlength):
        format_strings = ','.join(['%s' for i in range(0,len(ids))])
        sql = 'select user_2 from t_user_friend where user_1 in (%s)' % format_strings
        c.execute(sql,tuple(ids))
        ids = set()
        for row in c.fetchall():
            ids.add(str(int(row[0])))
    print time.time()-start
    print len(ids)
