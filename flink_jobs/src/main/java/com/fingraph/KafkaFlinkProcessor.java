package com.fingraph;

import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fingraph.model.Transaction;
import com.fingraph.model.FraudEvent;
import com.fingraph.model.GraphTransaction;

public class KafkaFlinkProcessor {

    public static void main(String[] args) throws Exception {

        StreamExecutionEnvironment env =
                StreamExecutionEnvironment.getExecutionEnvironment();

        // Enable checkpointing for fault tolerance
        env.enableCheckpointing(10000);

        KafkaSource<String> source = KafkaSource.<String>builder()
                .setBootstrapServers("172.19.176.1:9092")
                .setTopics("fin_transactions")
                .setGroupId("fingraph-flink")
                .setStartingOffsets(OffsetsInitializer.earliest())
                .setValueOnlyDeserializer(new SimpleStringSchema())
                .build();

        DataStream<String> transactions = env.fromSource(
                source,
                WatermarkStrategy.noWatermarks(),
                "FinGraph Kafka Source"
        );

        DataStream<Transaction> parsedTransactions = transactions.map(json -> {
                     ObjectMapper mapper = new ObjectMapper();
                     return mapper.readValue(json, Transaction.class);
                   });

        DataStream<FraudEvent> fraudEvents = parsedTransactions.map(transaction ->
                new FraudEvent(
                       transaction.getTransaction_id(),
                       transaction.getSender(),
                       transaction.getReceiver(),
                       transaction.getAmount(),
                       transaction.getTransaction_type(),
                       FraudClassifier.classify(transaction)
        )
);

        DataStream<FraudEvent> suspiciousEvents = fraudEvents
                   .filter(event ->
                          "SUSPICIOUS".equalsIgnoreCase(event.getFraud_status())
                   );

        DataStream<GraphTransaction> graphTransactions = fraudEvents.map(event ->
           new GraphTransaction(
                event.getTransaction_id(),
                event.getSender(),
                event.getReceiver(),
                event.getAmount(),
                event.getTransaction_type(),
                event.getFraud_status(),
                RiskScorer.calculateRisk(event)
        )
);

        //graphTransactions
          // .filter(event ->
            //    "SUSPICIOUS".equalsIgnoreCase(event.getFraudStatus())
        //)
          // .addSink(new Neo4jSink())
           //.name("Neo4j Graph Sink");

            graphTransactions
    .filter(event ->
        "SUSPICIOUS".equalsIgnoreCase(event.getFraudStatus())
    )
    .print()
    .name("Fraud Event Output");

        env.execute("FinGraph Kafka Transaction Processor");
    }

}

