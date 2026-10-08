package com.dwpg.simulator.dto;

public class CompleteCheckoutSessionRequest {

    private String paymentMethod = "UPI"; // UPI, CARD, WALLET
    private String utrNumber;
    private String cardNumber;
    private String cardExpiry;
    private String cardCvv;
    private String payerUsername;

    public CompleteCheckoutSessionRequest() {}

    public CompleteCheckoutSessionRequest(String paymentMethod, String utrNumber) {
        this.paymentMethod = paymentMethod;
        this.utrNumber = utrNumber;
    }

    public String getPaymentMethod() { return paymentMethod; }
    public void setPaymentMethod(String paymentMethod) { this.paymentMethod = paymentMethod; }

    public String getUtrNumber() { return utrNumber; }
    public void setUtrNumber(String utrNumber) { this.utrNumber = utrNumber; }

    public String getCardNumber() { return cardNumber; }
    public void setCardNumber(String cardNumber) { this.cardNumber = cardNumber; }

    public String getCardExpiry() { return cardExpiry; }
    public void setCardExpiry(String cardExpiry) { this.cardExpiry = cardExpiry; }

    public String getCardCvv() { return cardCvv; }
    public void setCardCvv(String cardCvv) { this.cardCvv = cardCvv; }

    public String getPayerUsername() { return payerUsername; }
    public void setPayerUsername(String payerUsername) { this.payerUsername = payerUsername; }
}
