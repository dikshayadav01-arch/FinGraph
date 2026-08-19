package com.fingraph;

import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

public class FinGraphProcessor {

    public static void main(String[] args) throws Exception {

        StreamExecutionEnvironment env =
                StreamExecutionEnvironment.getExecutionEnvironment();

        DataStream<String> transactions = env.fromData(
                "ACC001,ACC002,5000,NORMAL",
                "ACC003,ACC004,9500,SMURFING",
                "ACC005,SHELL001,9700,STARBURST",
                "ACC006,ACC007,1200,NORMAL"
        );

        DataStream<String> processedTransactions =
                transactions.map(new MapFunction<String, String>() {

                    @Override
                    public String map(String transaction) {

                        String[] parts = transaction.split(",");

                        String sender = parts[0];
                        String receiver = parts[1];
                        String amount = parts[2];
                        String type = parts[3];

                        return "PROCESSED | "
                                + sender
                                + " -> "
                                + receiver
                                + " | Rs."
                                + amount
                                + " | "
                                + type;
                    }
                });

        processedTransactions.print();

        env.execute("FinGraph Transaction Processor");
    }
}