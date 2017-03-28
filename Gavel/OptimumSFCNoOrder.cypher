MATCH (kid:Kid)
WITH count(kid) AS numberOfKids
MATCH path = ((startingRoadJunction)-[:CONNECTED_TO*1..20]-(lastKid:Kid))
WHERE startingRoadJunction.id = 0 and size(filter(x in nodes(path) WHERE (x:Kid))) >= numberOfKids
WITH path, [x IN nodes(path) WHERE (x:Kid) | x] AS kidsList, numberOfKids
UNWIND kidsList AS kidInPath
WITH path, collect(DISTINCT kidInPath) AS kidsInPath, numberOfKids
WHERE size(kidsInPath) = numberOfKids
WITH path, REDUCE(dist = 0, rel in rels(path) | dist + rel.distance) AS pathLength, kidsInPath,
[i in range(0,size(nodes(path))) WHERE (nodes(path)[i]):Kid | i] AS kidPositions, numberOfKids
WHERE
ALL (i in range (0,size(kidPositions)-1) WHERE
reduce(dist = 0, rel in rels(path)[0..kidPositions[i]] | dist + rel.distance) < (kidsInPath[i]).bedtime)
RETURN path, pathLength
ORDER BY pathLength ASC
LIMIT 1

#1 replace all variables with the correct ones
#2. delete unwanted lines
#3. add any specific lines