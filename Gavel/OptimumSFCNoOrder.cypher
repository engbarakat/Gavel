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

Kid
kid
numberOfKids
1. Match and get Functions
2. You are looking for a subgraph contains:
    a. start node is Hostsrc
    b. end node is Hostend
    c. all functions need to be associated with some nodes(relationships) //size(filter(x in nodes(path) WHERE (x:Kid))) >= numberOfKids
    d. every path matches above are saved to validpaths list
<<<<<<< HEAD
    
3. 
=======
   
3.Exempt all path that appears to go through functions more than once.

4. Exempt paths that Functions appear in different order (OPT)

5. exempt all paths that doesnt go through all required functions. review line No. 8

6. Later could be extented to implement BW constrains or delay constrains (OPT)

Match (function:MB) where MB.dpid in {values} return MBsSet
Match path = (startnode)->(endnode) return path as pathsetraw
with pathsetraw, MBsSet
-- for every switch in the path get all functions connected to it, return distinct set of all functions supported by the path. (write function that take path and return supported functions)


************************New algorithm

Build the routing solution

for every Function in the list:

1. find the shortest path for every node hosts this function
2. build a decision tree then find the route to the end. 
>>>>>>> GavelMBs
