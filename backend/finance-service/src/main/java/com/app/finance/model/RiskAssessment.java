package com.app.finance.model;

public class RiskAssessment {
    private String supplierId;
    private double score;
    private String assessmentDetails;

    // Constructors
    public RiskAssessment() {}

    public RiskAssessment(String supplierId, double score, String assessmentDetails) {
        this.supplierId = supplierId;
        this.score = score;
        this.assessmentDetails = assessmentDetails;
    }

    // Getters and Setters
    public String getSupplierId() {
        return supplierId;
    }

    public void setSupplierId(String supplierId) {
        this.supplierId = supplierId;
    }

    public double getScore() {
        return score;
    }

    public void setScore(double score) {
        this.score = score;
    }

    public String getAssessmentDetails() {
        return assessmentDetails;
    }

    public void setAssessmentDetails(String assessmentDetails) {
        this.assessmentDetails = assessmentDetails;
    }
}