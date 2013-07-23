import requests,simplejson

sort_keys = dict(method=0,
                 to=1,
                 body=2,
                 id=3,
                 query=0,
                 params=1,
                 script=0)

def special_sort(item):
    key = item[0]
    return sort_keys.get(key,item)
    

class Neo4jRestConnector(object):

    def __init__(self,baseurl=None,debug=False):
        self.debug = debug
        if baseurl==None:
            baseurl='http://localhost:7474/db/data'
        self.baseurl = baseurl
        self.headers = {'content-type': 'application/json',
                        'accept': 'application/json'}

    def batch_call(self,statements):
        i = 0
        batch = []
        for statement in statements:
            i+=1
            method,to,body = statement
            batch.append(dict(method=method,
                              to=to,
                              body=body,
                              id=i))
        datastring = simplejson.dumps(batch,item_sort_key=special_sort)
        result = requests.post(self.baseurl+'/batch',data=datastring,headers=self.headers)
        return result

    def batch_call_ids(self,statements):
        r = self.batch_call(statements)
        r = r.json()
        out = []
        for data in r:
            out.append(int(data['location'].split('/')[-1]))
        return out

    def create_nodes(self,properties):
        statements = []
        for props in properties:
            if props == None:
                props = {}
            statement = ['post','/node',props]
            statements.append(statement)
        return self.batch_call_ids(statements)

    def create_relationships(self,definitions):
        statements = []
        for definition in definitions:
            source,target,reltype,props = definition
            body = dict(to='%s/node/%s' % (self.baseurl,target),
                        type=reltype)
            if props != None:
                body['data']=props

            statement = ['post',
                         '/node/%s/relationships'%source,
                         body]
            statements.append(statement)
        return self.batch_call(statements)   

    def cypher(self,query,params={}):
        data = dict(query=query,
                    params=params)
        datastring = simplejson.dumps(data,item_sort_key=special_sort)
        result = requests.post(self.baseurl+'/cypher',data=datastring,headers=self.headers)
        return result.json()
       

    def traverse(self,start,what,query,paged=False):
        datastring = simplejson.dumps(query)
        if paged == True:            
            url = self.baseurl+'/node/%s/paged/traverse/%s' % (start,what)
        else:
            url = self.baseurl+'/node/%s/traverse/%s' % (start,what)
        result = requests.post(url,data=datastring,headers=self.headers)
        return result.json()
   
    def gremlin(self,script,params=None):
        if params==None:
            params = {}
        data = dict(script=script,
                    params=params)
        datastring = simplejson.dumps(data,item_sort_key=special_sort)
        result = requests.post(self.baseurl+'/ext/GremlinPlugin/graphdb/execute_script',data=datastring,headers=self.headers)  
        return result.json()
        
if __name__ == '__main__':
    g = Neo4jRestConnector()
    g.cypher('start r=relationship(*) delete r')
    g.cypher('start n=node(*) delete n')
    r = g.create_nodes([dict(noscenda_name='testperson1'),
                        dict(noscenda_name='testperson2')])
    r2 = g.create_relationships([[r[0],r[1],'friend',None]])
