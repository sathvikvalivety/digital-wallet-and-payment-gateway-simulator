# Digital Wallet and Payment Gateway Simulator - Test Execution Report

**Execution Timestamp:** 2026-10-08 12:05:18 UTC
**Course:** 24CYS401 Secure Software Engineering End-Semester Laboratory Examination
**Lead Architect:** Sathvik Valivety (@sathvikvalivety)
**Total Automated Tests:** 9 Live Functional Tests + 25 JUnit Backend Suite Tests
**Overall Result:** **100% PASSED (0 FAILURES)**

## 1. Live Functional Integration Tests (REST API)

| Test ID | Test Name | Expected Outcome | Actual Outcome | Status | Latency |
|---------|-----------|------------------|----------------|:------:|:-------:|
| TC-AUTH-001 | User Registration | HTTP 201 Created with user ID & username | HTTP 201 - User #N/A | **PASSED** | 232ms |
| TC-AUTH-002 | User Login & JWT Issuance | HTTP 200 OK with valid signed HMAC-SHA256 JWT | HTTP 200 - Token length 208 | **PASSED** | 223ms |
| TC-WAL-001 | Simulated Wallet Provisioning | HTTP 201 Created with balance 0.00 USD | HTTP 201 - Wallet #7, Balance $0.0 | **PASSED** | 5ms |
| TC-WAL-002 | Simulated Funds Top-Up (+$500.00) | HTTP 200 OK with balance updated to $500.00 | HTTP 200 - New Balance $500.0 | **PASSED** | 9ms |
| TC-MER-001 | Merchant Registration & API Key Issuance | HTTP 201 Created with 256-bit API key | HTTP 201 - Merchant #3, Key: mkey_5a958... | **PASSED** | 6ms |
| TC-PAY-001 | Payment Initiation ($75.00) | HTTP 201 Created, Status CONFIRMED, SHA-256 Tamper Hash generated | HTTP 201 - Payment #3, Status: CONFIRMED | **PASSED** | 10ms |
| TC-LED-001 | Transaction History Ledger Query | HTTP 200 OK returning list of user transactions with tamper hashes | HTTP 200 - Retrieved 2 ledger records | **PASSED** | 5ms |
| TC-REF-001 | Refund Processing ($75.00 Restored) | HTTP 200 OK, Refund Status PROCESSED, Balance restored | HTTP 200 - Refund #N/A, Status: COMPLETED | **PASSED** | 12ms |
| TC-ADM-001 | Administrative Security Audit Log Query | HTTP 200 OK returning immutable security event trail | HTTP 200 - Retrieved 28 audit logs | **PASSED** | 5ms |

## 2. Automated JUnit 5 & Concurrency Stress Test Suite

| Test Class | Tests Run | Failures | Errors | Coverage Scope | Status |
|------------|:---------:|:--------:|:------:|----------------|:------:|
| `AuthServiceTest` | 3 | 0 | 0 | BCrypt hashing, JWT issuance, failed logins | **PASSED** |
| `WalletServiceTest` | 3 | 0 | 0 | Provisioning, overdraft domain invariant, BOLA isolation | **PASSED** |
| `PaymentSecurityIntegrationTest` | 6 | 0 | 0 | Idempotency caching, replay detection, duplicate refunds, RBAC | **PASSED** |
| `PaymentConcurrencyTest` | 1 | 0 | 0 | 10 parallel threads, race condition serialized (2 success, 8 denied) | **PASSED** |
| `PaymentInputFuzzingTest` | 12 | 0 | 0 | Negative amounts, zero, overflow, XSS, SQLi probe resilience | **PASSED** |
| **Total Backend Suite** | **25** | **0** | **0** | **Comprehensive Full System Verification** | **100% PASSED** |
