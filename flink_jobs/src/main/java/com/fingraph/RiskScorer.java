package com.fingraph;

import com.fingraph.model.FraudEvent;

public class RiskScorer {

    public static String calculateRisk(FraudEvent event) {

        if (event.getAmount() >= 9000) {
            return "HIGH";
        }

        if ("SMURFING".equalsIgnoreCase(event.getTransaction_type())) {
            return "HIGH";
        }

        if ("STARBURST".equalsIgnoreCase(event.getTransaction_type())) {
            return "HIGH";
        }

        if ("CIRCULAR".equalsIgnoreCase(event.getTransaction_type())) {
            return "HIGH";
        }

        if (event.getAmount() >= 5000) {
            return "MEDIUM";
        }

        return "LOW";
    }
}
