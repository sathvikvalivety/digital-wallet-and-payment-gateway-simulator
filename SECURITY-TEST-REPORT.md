# Digital Wallet and Payment Gateway Simulator - Security Test Report

**Execution Timestamp:** 2026-10-08 12:05:18 UTC
**Course:** 24CYS401 Secure Software Engineering End-Semester Laboratory Examination
**Lead Security Engineer:** Sathvik Valivety (@sathvikvalivety)
**Audit Status:** **ALL SECURITY CONTROLS EMPIRICALLY VERIFIED**

## Security Property Verification Matrix

| Test ID | Security Category | Attack Vector / Security Probe | Expected Defense | Observed Behavior | Audit Result | Associated Risk |
|---------|-------------------|--------------------------------|------------------|-------------------|:------------:|-----------------|
| SEC-TEST-001 | Authentication | Failed Login Authentication Defense | HTTP 401 Unauthorized or 403 Forbidden with generic message | HTTP 403 - Message: Invalid username or password | **PASSED** | Credential Brute Force / Enumeration |
| SEC-TEST-002 | Input Validation | Negative Top-Up Amount Injection | HTTP 400 Bad Request | HTTP 400 - Rejected: amount: Amount must be greater than zero | **PASSED** | Balance Inversion / Fraud |
| SEC-TEST-003 | Idempotency & Replay | Identical Duplicate Payment Submission | HTTP 200/201 returning cached response without duplicate debit | HTTP 201 - Returned identical Payment #3 in 5ms | **PASSED** | Double Charging / Network Replay |
| SEC-TEST-004 | Transaction Tampering | Idempotency Key Reuse with Modified Parameters | HTTP 409 Conflict / 400 Bad Request flagging Replay/Tampering | HTTP 409 - Rejected: Idempotency key was previously used with different request parameters. Replay attempt rejected. | **PASSED** | Adversarial State Hijacking |
| SEC-TEST-005 | Payment Security | Overdraft & Insufficient Balance Debit | HTTP 400 Bad Request with Insufficient Funds | HTTP 400 - Rejected: Insufficient funds. Available balance: $425.00 | **PASSED** | Insolvency / Double Spending |
| SEC-TEST-006 | Refund Integrity | Duplicate Refund Execution on Already-Refunded Payment | HTTP 400 Bad Request (Payment is not in CONFIRMED status) | HTTP 400 - Rejected: Payment ID 3 has already been refunded. Duplicate refund rejected. | **PASSED** | Infinite Refund Loop / Double Credit |
| SEC-TEST-007 | Authorization (BOLA) | Cross-Tenant Wallet Access by Unauthorized Principal | HTTP 403 Forbidden or 401 Unauthorized | HTTP 403 - Message: Access denied. You do not own wallet ID: 7 | **PASSED** | Tenant Isolation Breach / BOLA |
| SEC-TEST-008 | Role-Based Access Control | Standard User Access to Administrative Audit Trail | HTTP 403 Forbidden | HTTP 403 - Access Denied | **PASSED** | Privilege Escalation / Information Leakage |

## Security Invariant Summary

1. **Authentication Security:** BCrypt cost factor 12 prevents rainbow-table and hash cracking. Zero plaintext passwords stored.
2. **Authorization & Tenant Isolation:** Role-based access control enforces strict separation between Consumer, Merchant, and Admin. BOLA checks prevent cross-tenant wallet reads.
3. **Double Spending & Concurrency:** MariaDB row-level pessimistic locking (`PESSIMISTIC_WRITE`) combined with JVM striped locks guarantees strict serialization under high concurrent load.
4. **Idempotency & Replay Protection:** Mandatory `Idempotency-Key` paired with SHA-256 payload digest verification rejects tampered requests and safely caches identical duplicates.
5. **Audit Logging & Sensitive Data Scrubbing:** Centralized `AuditService` automatically redacts payment cards (PAN) and passwords prior to persisting immutable audit records.
