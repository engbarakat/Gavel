Match (n) detach delete n;

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///switches32.csv" AS row
CREATE (:Switch {id: row.id, layer: toInt(row.layer), dpid: row.dpid});

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///hosts32.csv" AS row
CREATE (:Host {id: row.id, layer: toInt(row.layer), dpid: row.dpid, mac: row.mac, ip:row.ip});

DROP INDEX ON :Switch(dpid);
DROP INDEX ON :Host(ip);
CREATE CONSTRAINT ON (book:Switch) ASSERT book.dpid IS UNIQUE;
CREATE CONSTRAINT ON (book:Host) ASSERT book.ip IS UNIQUE;

