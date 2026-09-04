// FinGraph - Starburst Fraud Detection
// Detect receivers receiving suspicious transactions
// from at least 3 distinct sender accounts.

MATCH (sender:Account)-[t:SENT]->(receiver:Account)
WHERE t.fraudStatus = "SUSPICIOUS"

WITH receiver,
     count(DISTINCT sender) AS uniqueSenders,
     sum(t.amount) AS totalAmount

WHERE uniqueSenders >= 3

RETURN
    receiver.id AS suspiciousReceiver,
    uniqueSenders,
    totalAmount
ORDER BY uniqueSenders DESC;
