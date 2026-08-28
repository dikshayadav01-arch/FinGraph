package com.fingraph.model;

public class GraphTransaction {

    private String transactionId;
    private String sender;
    private String receiver;
    private double amount;
    private String transactionType;
    private String fraudStatus;
    private String riskLevel;

    public GraphTransaction() {
    }

    public GraphTransaction(
            String transactionId,
            String sender,
            String receiver,
            double amount,
            String transactionType,
            String fraudStatus,
            String riskLevel) {

        this.transactionId = transactionId;
        this.sender = sender;
        this.receiver = receiver;
        this.amount = amount;
        this.transactionType = transactionType;
        this.fraudStatus = fraudStatus;
        this.riskLevel = riskLevel;
    }

    public String getTransactionId() {
        return transactionId;
    }

    public void setTransactionId(String transactionId) {
        this.transactionId = transactionId;
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

    public String getTransactionType() {
        return transactionType;
    }

    public void setTransactionType(String transactionType) {
        this.transactionType = transactionType;
    }

    public String getFraudStatus() {
        return fraudStatus;
    }

    public void setFraudStatus(String fraudStatus) {
        this.fraudStatus = fraudStatus;
    }

    public String getRiskLevel() {
        return riskLevel;
    }

    public void setRiskLevel(String riskLevel) {
        this.riskLevel = riskLevel;
    }

    @Override
    public String toString() {
        return "GraphTransaction{" +
                "transactionId='" + transactionId + '\'' +
                ", sender='" + sender + '\'' +
                ", receiver='" + receiver + '\'' +
                ", amount=" + amount +
                ", transactionType='" + transactionType + '\'' +
                ", fraudStatus='" + fraudStatus + '\'' +
                ", riskLevel='" + riskLevel + '\'' +
                '}';
    }
}
