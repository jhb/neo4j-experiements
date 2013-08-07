import readline, neo4jconnector,time, pprint,os

histfile = os.path.join(os.path.expanduser("~"), ".nconsolehistory")
try:
    readline.read_history_file(histfile)
except IOError:
    pass
import atexit
atexit.register(readline.write_history_file, histfile)

g = neo4jconnector.BaseNeo4jConnector(debug=0)

while 1:
    try:
        line = raw_input('neo: ')
        start = time.time()
        result = g.queryd(line)
        needed = time.time()-start
        pprint.pprint(result)
        print 'time: ',needed
    except (KeyboardInterrupt,EOFError):
        break
print
