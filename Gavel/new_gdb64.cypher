match ()-[n:PathSlice_to]-() detach delete n;
match (:Host)-[n:Connected_to]-(:Switch) delete n;
match (n: Host) detach delete n;
match (n: Switch) detach delete n;

Match (n) detach delete n;

USING PERIODIC COMMIT 10000
LOAD CSV WITH HEADERS FROM "file:///TestedTopologies/switches64.csv" AS row
CREATE (:Switch {id: row.id, layer: toInt(row.layer), dpid: row.dpid});

USING PERIODIC COMMIT 10000
LOAD CSV WITH HEADERS FROM "file:///TestedTopologies/hosts64.csv" AS row
CREATE (:Host {id: row.id, layer: toInt(row.layer), dpid: row.dpid, mac: row.mac, ip:row.ip});

DROP INDEX ON :Switch(dpid);
DROP INDEX ON :Host(ip);
CREATE CONSTRAINT ON (book:Switch) ASSERT book.dpid IS UNIQUE;
CREATE CONSTRAINT ON (book:Host) ASSERT book.ip IS UNIQUE;

USING PERIODIC COMMIT 10000
LOAD CSV WITH HEADERS FROM "file:///TestedTopologies/connected_to64.csv" AS row
MATCH (s:Switch {id: row.node2})
MATCH (h:Host {id: row.node1})
MERGE (h)-[pu:Connected_to]->(s)
ON CREATE SET pu.port1 = toInt(row.port1), pu.port2 = toInt(row.port2), pu.node2 = h.ip, pu.node1=s.dpid, pu.cost = toInt(row.port1)
MERGE (s)-[up:Connected_to]->(h)
ON CREATE SET up.port2 = toInt(row.port1), up.port1 = toInt(row.port2), up.node1 = h.ip, up.node2=s.dpid,up.cost = toInt(row.port2);

USING PERIODIC COMMIT 10000
LOAD CSV WITH HEADERS FROM "file:///TestedTopologies/switched_to64.csv" AS row
MATCH (s2:Switch {id: row.node2})
MATCH (s1:Switch {id: row.node1})
MERGE (s1)-[r:Connected_to]->(s2)
ON CREATE SET r.port1 = toInt(row.port1), r.port2 = toInt(row.port2), r.node1 = s1.dpid, r.node2=s2.dpid,r.cost = toInt(row.port1)
MERGE (s2)-[re:Connected_to]->(s1)
ON CREATE SET re.port1 = toInt(row.port2), re.port2 = toInt(row.port1), re.node1 = s2.dpid, re.node2=s1.dpid,re.cost = toInt(row.port2);

