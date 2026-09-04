// FinGraph - Smurfing Fraud Detection
// Detect target accounts receiving multiple SMURFING transactions
// from distinct sender accounts.

MATCH (sender:Account)-[t:SENT]->(receiver:Account)
WHERE t.transactionType = "SMURFING"

WITH receiver,
     count(DISTINCT sender) AS uniqueSenders,
     count(t) AS transactionCount,
     sum(t.amount) AS totalAmount

WHERE uniqueSenders >= 3

RETURN
    receiver.id AS targetAccount,
    uniqueSenders,
    transactionCount,
    totalAmount
ORDER BY transactionCount DESC;
