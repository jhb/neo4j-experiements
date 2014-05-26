import sys,urlparse,re,cPickle
from pprint import pprint

f = open(sys.argv[1])
#for i in range(100000):   
i = 0
nodes = {}
relations = {}

reg_schema = re.compile('"(.*)"\^\^<.*/([^/>]*)>')
reg_lang = re.compile('@[a-z]{2}$')

printline=False
currencies = ['japaneseYen',
              'euro',
              'poundSterling',
              'usDollar',
              'southAfricanRand',
              'swissFranc',
              'swedishKrona']

valtypes = {}
while i<1000000: 
    line = f.readline()
    if not line:
        break
    i += 1
    if line.startswith('#'):
        continue
    start,rel,target = line.strip().rstrip(' .').split(' ',2)
    start = start[1:-1]
    startparts = urlparse.urlparse(start)
    startprefix=  startparts.hostname.split('.')[1]
    startresource = startparts.path.split('/',2)[2]
    startresource = startresource.decode('unicode-escape')
    
    origin = '%s:%s' % (startprefix,startresource)
    
    rel = rel[1:-1]
    relparts = urlparse.urlparse(rel)
    relprefix = relparts.hostname.split('.')[-2]
    relend = relparts.path.split('/')[-1]
    reltype = '%s:%s' % (relprefix,relend)
   
    if printline:
        print origin,reltype,
    
    target =  target.decode('unicode-escape')
    if reg_lang.search(target):
        value = target[1:-4]
    
    elif target.startswith('<http'):
        target = target[1:-1]
        targeturl = urlparse.urlparse(target)
        try:
            targetprefix = targeturl.hostname.split('.')
        except:
            targetprefix = 'invalidhost'

        if len(targetprefix)> 1:
            targetprefix=targetprefix[1]
        
        if targetprefix == 'dbpedia':
            targetresource = targeturl.path.split('/')[2]
            value = 'dbpedia:%s' % targetresource

            #node
        else:
            value = target
    else:
        result = reg_schema.match(target)
        if result !=None:
            valstring = result.group(1)
            valtype = result.group(2)
            #print valstring, valtype,
            if valtype.startswith('XMLSchema#'):
                valtype = valtype[10:]
                if valtype in ['double','float']:
                    value = float(valstring)
                elif valtype.lower().endswith('integer') or valtype=='gYear':
                    value = int(valstring)
                else:
                    value = valstring
            elif valtype in currencies:
                value=float(valstring)
                reltype = reltype+'#'+valtype
                #print reltype,value
                #value = valstring+' '+valtype
            else:
                value = valstring
            valtypes[valtype]=value
        else:
            value = target
    if printline:
        print value
    
    startnode = nodes.setdefault(origin,{})
    if type(value) in [str,unicode] and (value.startswith('dbpedia:') or value.startswith('http://')):

        nodes.setdefault(value,{})
        relations.setdefault(origin,{}).setdefault(reltype,[]).append(value)
    else:
        startnode.setdefault(reltype,[]).append(value)
    if not printline and i%10000 == 0: 
        print i
#print valtypes.items()       
#pprint(nodes)
print 'writing'
cPickle.dump(nodes,open('nodes.pickle','w'),2)        
cPickle.dump(relations,open('relations.pickle','w'),2)        
print 'fini'
