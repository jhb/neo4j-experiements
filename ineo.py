import neo4jconnector,time
g = neo4jconnector.BaseNeo4jConnector(debug=0)
g.timed = 1

def q(query):
    result = g.queryd(query)
    return result
