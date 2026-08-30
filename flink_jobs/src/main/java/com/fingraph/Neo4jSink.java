package com.fingraph;

import com.fingraph.model.GraphTransaction;
import org.apache.flink.api.common.functions.OpenContext;
import org.apache.flink.streaming.api.functions.sink.legacy.RichSinkFunction;

public class Neo4jSink extends RichSinkFunction<GraphTransaction> {

    private transient Neo4jWriter writer;

    @Override
    public void open(OpenContext openContext) throws Exception {

        String password = System.getenv("NEO4J_PASSWORD");

        if (password == null || password.isEmpty()) {
            throw new IllegalStateException(
                    "NEO4J_PASSWORD environment variable is not set."
            );
        }

        writer = new Neo4jWriter(
                "bolt://172.19.176.1:7687",
                "neo4j",
                password
        );
    }

    @Override
    public void invoke(
            GraphTransaction transaction,
            Context context
    ) throws Exception {

        writer.writeTransaction(transaction);

        System.out.println(
                "NEO4J ✓ " + transaction.getTransactionId()
                        + " | " + transaction.getSender()
                        + " → " + transaction.getReceiver()
                        + " | risk=" + transaction.getRiskLevel()
        );
    }

    @Override
    public void close() throws Exception {

        if (writer != null) {
            writer.close();
        }
    }
}