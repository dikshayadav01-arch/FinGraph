package com.fingraph;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fingraph.model.FraudEvent;
import com.fingraph.model.GraphTransaction;
import com.fingraph.model.Transaction;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

public class FinGraphProcessor {

    public static void main(String[] args) throws Exception {

        StreamExecutionEnvironment env =
                StreamExecutionEnvironment.getExecutionEnvironment();

        env.enableCheckpointing(10000);

        KafkaSource<String> source = KafkaSource.<String>builder()
                .setBootstrapServers("172.19.176.1:9092")
                .setTopics("fin_transactions")
                .setGroupId("fingraph-flink")
                .setStartingOffsets(
                        OffsetsInitializer.earliest()
                )
                .setValueOnlyDeserializer(
                        new SimpleStringSchema()
                )
                .build();

        DataStream<String> kafkaStream =
                env.fromSource(
                        source,
                        WatermarkStrategy.noWatermarks(),
                        "Kafka Transaction Source"
                );

        ObjectMapper objectMapper = new ObjectMapper();

        DataStream<Transaction> transactions =
                kafkaStream.map(json ->
                        objectMapper.readValue(
                                json,
                                Transaction.class
                        )
                );

        DataStream<FraudEvent> fraudEvents =
                transactions.map(transaction -> {

                    String fraudStatus =
                            FraudClassifier.classify(transaction);

                    return new FraudEvent(
                            transaction.getTransaction_id(),
                            transaction.getSender(),
                            transaction.getReceiver(),
                            transaction.getAmount(),
                            transaction.getTransaction_type(),
                            fraudStatus
                    );
                });

        DataStream<GraphTransaction> graphTransactions =
                fraudEvents.map(event -> {

                    String riskLevel =
                            RiskScorer.calculateRisk(event);

                    return new GraphTransaction(
                            event.getTransaction_id(),
                            event.getSender(),
                            event.getReceiver(),
                            event.getAmount(),
                            event.getTransaction_type(),
                            event.getFraud_status(),
                            riskLevel
                    );
                });

        graphTransactions.print("GRAPH TRANSACTION");

        graphTransactions.addSink(
                new Neo4jSink()
        );

        env.execute("FinGraph Transaction Processor");
    }
}
