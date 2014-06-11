"""
(c) 2013 Joerg Baach, GPL

A simple connector to the transactional http endpoint of neo4j v.2.
It creates transactions as needed, and does automatic rollback if it
sees an error from the server side.

Usage:

g = BaseNeo4jConnector()

#for the raw requests response
result = g.query('match n return count(n);')

#for a data object
result = g.queryd('match n return count(n);')

g.commitTx()
"""



import requests, simplejson, time

def special_sort(item):
    if item[0]=='statement':
        return 0
    else:
        return item

class BaseNeo4jConnector(object):
    
    def __init__(self,baseurl=None,debug=False,auto_rollback=True,timed=False):
        self.debug = debug
        if baseurl==None:
            baseurl='http://localhost:7474/db/data/transaction'
        self.baseurl = baseurl
        self.transactionid=None
        self.transactionurl=None
        self.auto_rollback=auto_rollback
        self.headers = {'content-type': 'application/json',
                        'accept': 'application/json',
                        'max-execution-time':10000}
        self.timed = timed
    
    def __del__(self):
        transactionurl = getattr(self,'transactionurl',None)
        if transactionurl !=None:
            #print 'rollback on __del__'
            import requests,simplejson
            self.rollbackTx()

    def call(self,data,method='post',url=None,reverse=1):
        
        if reverse:
            datastring = simplejson.dumps(data,item_sort_key=special_sort)
        else:
            datastring = simplejson.dumps(data)
        if self.debug:
            print datastring

        if url==None:
            if self.transactionurl !=None:  
                url = self.transactionurl
            else:
                url = self.baseurl

        if self.debug:
            print '%s to %s with %s' % (method,url,datastring)

        if self.timed:
            start = time.time()

        result = getattr(requests,method)(url,data=datastring,headers=self.headers)
        
        if self.timed:
            print 'time: ', time.time() - start

        if self.transactionurl==None:
            self.transactionurl = result.headers['location']

            #data = result.json()
            #parts = data['commit'].split('/')
            #self.transactionid=parts[-2]
            #self.transactionurl='%s/%s' %(self.baseurl,self.transactionid)
        data = result.json()
        if self.debug:
            print data
        if data['errors']:
            if self.auto_rollback:
                self.rollbackTx()
            e = Exception(data['errors'][0]['message'])
            e.errors = data['errors']
            raise e
                   
        return result

    def query(self,statements):
        if type(statements) == str:
            statements = [statements]
        s = []
        for statement in statements:
            if type(statement) in [list,tuple] and len(statement)==2:
                s.append(dict(statement=statement[0],parameters=statement[1]))
            else:
                s.append(dict(statement=statement))
        payload = { "statements" : s}            
        return self.call(payload)

    def queryd(self,statements):
        return self.r2d(self.query(statements))

    def r2d(self,result):
        data = result.json()
        results = data['results']
        out = []
        for res in results:
            cols = res['columns']
            rows = []
            for r in res['data']:
                #out.append(dict(zip(cols,r)))
                out.append(dict(zip(cols,r["row"])))
            #out.append(rows)
        return out


    def commitTx(self):
        if self.debug:
            print 'commit neo4j'
        if self.transactionurl == None:
            return 
        data=dict(statements=[])
        result = self.call(data,url=self.transactionurl+'/commit')
        self.transactionurl = None
        return result

    def rollbackTx(self):
        if self.transactionurl == None:
            return
        if self.debug:
            print 'rollback neo4j'
        result = requests.delete(self.transactionurl)
        self.transactionurl = None
        return result

