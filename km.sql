DROP TABLE IF EXISTS topic;
CREATE TABLE topic (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(255) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS article;
CREATE TABLE article (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(255) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS person;
CREATE TABLE person (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(255) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS project;
CREATE TABLE project (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(255) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS node;
CREATE TABLE node (
  id int(11) NOT NULL AUTO_INCREMENT,
  ntable varchar(255) NOT NULL,
  nid int(11) NOT NULL,
  name varchar(255) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS edge;
CREATE TABLE edge (
  id int(11) NOT NULL AUTO_INCREMENT,
  stype varchar(255) NOT NULL,
  sid int(11) NOT NULL,
  ttype varchar(255) NOT NULL,
  tid int(11) NOT NULL,
  etype varchar(255) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*

alter table topic add index name (name);
alter table person add index name (name);
alter table article add index name (name);
alter table project add index name (name);
alter table node add index name (name);
alter table node add index nodetable (ntable,nid);
alter table node add index nodetable2 (nid,ntable);
alter table edge add index sid (sid);
alter table edge add index stype (stype);
alter table edge add index tid (tid);
alter table edge add index ttype (ttype);
alter table edge add index x (sid,stype,etype);
alter table edge add index y (tid,ttype,etype);

*/


