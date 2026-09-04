// FinGraph - Circular Fraud Detection
// Detect 3-account transaction cycles where every transaction
// in the cycle is classified as CIRCULAR.

MATCH path = (a:Account)-[:SENT*3..3]->(a)
WHERE ALL(rel IN relationships(path)
          WHERE rel.transactionType = "CIRCULAR")

RETURN
    [node IN nodes(path) | node.id] AS accounts,
    [rel IN relationships(path) | rel.transactionType] AS transactionTypes,
    [rel IN relationships(path) | rel.amount] AS amounts;
