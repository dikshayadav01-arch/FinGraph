package com.fingraph;

import com.fingraph.model.Transaction;

public class FraudClassifierTest {

    public static void main(String[] args) {

        Transaction normal = new Transaction();
        normal.setTransaction_id("TEST_NORMAL");
        normal.setSender("ACC001");
        normal.setReceiver("ACC002");
        normal.setAmount(5000.00);
        normal.setTransaction_type("NORMAL");

        Transaction suspicious = new Transaction();
        suspicious.setTransaction_id("TEST_SMURFING");
        suspicious.setSender("ACC003");
        suspicious.setReceiver("ACC004");
        suspicious.setAmount(9500.00);
        suspicious.setTransaction_type("SMURFING");

        System.out.println(
                "NORMAL TEST: " +
                FraudClassifier.classify(normal)
        );

        System.out.println(
                "SMURFING TEST: " +
                FraudClassifier.classify(suspicious)
        );
    }
}
