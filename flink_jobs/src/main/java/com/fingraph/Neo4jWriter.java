package com.fingraph;

import com.fingraph.model.GraphTransaction;
import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.Driver;
import org.neo4j.driver.GraphDatabase;
import org.neo4j.driver.Session;

public class Neo4jWriter implements AutoCloseable {

    private final Driver driver;

    public Neo4jWriter(String uri, String username, String password) {
        this.driver = GraphDatabase.driver(
                uri,
                AuthTokens.basic(username, password)
        );
    }

    public void writeTransaction(GraphTransaction transaction) {

        try (Session session = driver.session()) {

            session.run(
                    """
                    MERGE (sender:Account {id: $sender})
                    MERGE (receiver:Account {id: $receiver})
                    MERGE (sender)-[tx:SENT {transactionId: $transactionId}]->(receiver)
                    SET tx.amount = $amount,
                        tx.transactionType = $transactionType,
                        tx.fraudStatus = $fraudStatus,
                        tx.riskLevel = $riskLevel
                    """,
                    org.neo4j.driver.Values.parameters(
                            "sender", transaction.getSender(),
                            "receiver", transaction.getReceiver(),
                            "transactionId", transaction.getTransactionId(),
                            "amount", transaction.getAmount(),
                            "transactionType", transaction.getTransactionType(),
                            "fraudStatus", transaction.getFraudStatus(),
                            "riskLevel", transaction.getRiskLevel()
                    )
            );
        }
    }

    @Override
    public void close() {
        driver.close();
    }
}