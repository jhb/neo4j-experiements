#!/bin/bash

#Settup up neo4j playground on linux, using dbpedia data
#Requires a functioning python + virtualenv setup, tar, bunzip
#(c) 2013 jhb, GPL

echo 'setting up python and packages'
virtualenv --no-site-packages .
./bin/easy_install ipython ipdb simplejson requests wget

echo 'downloading and setting up neo4j'
#put in the proper download location if another version/platform is needed
./bin/python -m wget "http://download.neo4j.org/artifact?edition=community&version=2.0.0-M03&distribution=tarball&dlid=notread"
tar xf neo4j-community-2.0.0-M03-unix.tar.gz
ln -s neo4j-community-2.0.0-M03 server
cp neo4j.properties server/conf

echo 'starting the server'
./server/bin/neo4j start

echo '(re)creating indexes (might throw errors, ignore)'
./server/bin/neo4j-shell -c "index --delete node_auto_index"
./server/bin/neo4j-shell -c "index --delete relationship_auto_index"
./server/bin/neo4j-shell -c "index --create node_auto_index \"{'type': 'fulltext'};\""
./server/bin/neo4j-shell -c "index --create -t Relationship relationship_auto_index"

echo 'downloading data'
./bin/python -m wget "http://downloads.dbpedia.org/3.8/de/mappingbased_properties_de.nt.bz2"
echo 'unpacking data'
bunzip2 mappingbased_properties_de.nt.bz2

echo 'parsing the data (up to ca. 3050000)'
sleep 2
./bin/python parser.py mappingbased_properties_de.nt


echo 'importing the data (nodes ca 576200, relations ca 1300000)'
./bin/python importer.py

processing relations
echo 
echo 'now start ./server/bin/neo4j-shell or go to http://localhost:7474/'
echo 'you could query for:'
echo 
echo "match n where n.noscenda_name='dbpedia:Bielefeld' return n;"
echo
echo "have fun"
