package com.fingraph.model;

public class FraudEvent {

    private String transaction_id;
    private String sender;
    private String receiver;
    private double amount;
    private String transaction_type;
    private String fraud_status;

    public FraudEvent() {
    }

    public FraudEvent(
            String transaction_id,
            String sender,
            String receiver,
            double amount,
            String transaction_type,
            String fraud_status) {

        this.transaction_id = transaction_id;
        this.sender = sender;
        this.receiver = receiver;
        this.amount = amount;
        this.transaction_type = transaction_type;
        this.fraud_status = fraud_status;
    }

    public String getTransaction_id() {
        return transaction_id;
    }

    public void setTransaction_id(String transaction_id) {
        this.transaction_id = transaction_id;
    }

    public String getSender() {
        return sender;
    }

    public void setSender(String sender) {
        this.sender = sender;
    }

    public String getReceiver() {
        return receiver;
    }

    public void setReceiver(String receiver) {
        this.receiver = receiver;
    }

    public double getAmount() {
        return amount;
    }

    public void setAmount(double amount) {
        this.amount = amount;
    }

    public String getTransaction_type() {
        return transaction_type;
    }

    public void setTransaction_type(String transaction_type) {
        this.transaction_type = transaction_type;
    }

    public String getFraud_status() {
        return fraud_status;
    }

    public void setFraud_status(String fraud_status) {
        this.fraud_status = fraud_status;
    }

    @Override
    public String toString() {
        return "FraudEvent{" +
                "transaction_id='" + transaction_id + '\'' +
                ", sender='" + sender + '\'' +
                ", receiver='" + receiver + '\'' +
                ", amount=" + amount +
                ", transaction_type='" + transaction_type + '\'' +
                ", fraud_status='" + fraud_status + '\'' +
                '}';
    }
}
