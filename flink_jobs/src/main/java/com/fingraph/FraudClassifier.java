package com.fingraph;

import com.fingraph.model.Transaction;

public class FraudClassifier {

    public static String classify(Transaction transaction) {

        if (transaction.getAmount() >= 9000) {
            return "SUSPICIOUS";
        }

        if ("SMURFING".equalsIgnoreCase(transaction.getTransaction_type())) {
            return "SUSPICIOUS";
        }

        if ("STARBURST".equalsIgnoreCase(transaction.getTransaction_type())) {
            return "SUSPICIOUS";
        }

        if ("CIRCULAR".equalsIgnoreCase(transaction.getTransaction_type())) {
            return "SUSPICIOUS";
        }

        return "NORMAL";
    }
}
