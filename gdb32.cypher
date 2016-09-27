Match (n) detach delete n;

USING PERIODIC COMMIT 10000
LOAD CSV WITH HEADERS FROM "file:///switches32.csv" AS row
CREATE (:Switch {id: row.id, layer: toInt(row.layer), dpid: row.dpid});

USING PERIODIC COMMIT 10000
LOAD CSV WITH HEADERS FROM "file:///hosts32.csv" AS row
CREATE (:Host {id: row.id, layer: toInt(row.layer), dpid: row.dpid, mac: row.mac, ip:row.ip});

DROP INDEX ON :Switch(dpid);
DROP INDEX ON :Host(ip);
CREATE CONSTRAINT ON (book:Switch) ASSERT book.dpid IS UNIQUE;
CREATE CONSTRAINT ON (book:Host) ASSERT book.ip IS UNIQUE;

USING PERIODIC COMMIT 10000
LOAD CSV WITH HEADERS FROM "file:///connected_to32.csv" AS row
MATCH (s:Switch {id: row.node2})
MATCH (h:Host {id: row.node1})
MERGE (h)-[pu:Connected_to]->(s)
ON CREATE SET pu.port1 = toInt(row.port1), pu.port2 = toInt(row.port2), pu.node1 = h.ip, pu.node2=s.dpid;

USING PERIODIC COMMIT 10000
LOAD CSV WITH HEADERS FROM "file:///switched_to32.csv" AS row
MATCH (s2:Switch {id: row.node2})
MATCH (s1:Switch {id: row.node1})
MERGE (s1)-[pu:Switched_to]->(s2)
ON CREATE SET pu.port1 = toInt(row.port1), pu.port2 = toInt(row.port2), pu.node1 = s1.dpid, pu.node2=s2.dpid;

USING PERIODIC COMMIT 10000
LOAD CSV WITH HEADERS FROM "file:///switched_to32.csv" AS row
MATCH (s2:Switch {id: row.node2})
MATCH (s1:Switch {id: row.node1})
MERGE (s2)-[pu:Switched_to]->(s1)
ON CREATE SET pu.port1 = toInt(row.port2), pu.port2 = toInt(row.port1), pu.node1 = s2.dpid, pu.node2=s1.dpid;
