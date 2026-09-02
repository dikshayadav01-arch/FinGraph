package com.fingraph.model;

public class Transaction {

    private String transaction_id;
    private String timestamp;
    private String sender;
    private String receiver;
    private double amount;
    private String transaction_type;
    private String sender_ip;
    private String sender_country;
    private String receiver_country;

    public Transaction() {
    }

    public String getTransaction_id() {
        return transaction_id;
    }

    public void setTransaction_id(String transaction_id) {
        this.transaction_id = transaction_id;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
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

    public String getSender_ip() {
        return sender_ip;
    }

    public void setSender_ip(String sender_ip) {
        this.sender_ip = sender_ip;
    }

    public String getSender_country() {
        return sender_country;
    }

    public void setSender_country(String sender_country) {
        this.sender_country = sender_country;
    }

    public String getReceiver_country() {
        return receiver_country;
    }

    public void setReceiver_country(String receiver_country) {
        this.receiver_country = receiver_country;
    }

    @Override
    public String toString() {
        return "Transaction{" +
                "transaction_id='" + transaction_id + '\'' +
                ", timestamp='" + timestamp + '\'' +
                ", sender='" + sender + '\'' +
                ", receiver='" + receiver + '\'' +
                ", amount=" + amount +
                ", transaction_type='" + transaction_type + '\'' +
                ", sender_ip='" + sender_ip + '\'' +
                ", sender_country='" + sender_country + '\'' +
                ", receiver_country='" + receiver_country + '\'' +
                '}';
    }
}