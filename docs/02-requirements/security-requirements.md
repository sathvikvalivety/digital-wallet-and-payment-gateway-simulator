# Comprehensive Security Requirements Specification (SEC-SRS)

This document establishes the formal security requirements for the **Digital Wallet and Payment Gateway Simulator (DWPG)** according to the NIST SP 800-53 controls and the OWASP Application Security Verification Standard (ASVS v4.0).

---

## 1. Security Invariants & Principles
- **Defense in Depth:** Security controls are enforced in layers (Transport Layer TLS -> API Gateway Filter -> Spring Security Method Authorization -> Domain Aggregate Invariants -> Database ACID Constraints).
- **Zero Client Trust:** All financial calculations, wallet ownership verifications, and state machine transitions are performed exclusively server-side.
- **Fail-Safe Defaults:** Requests lacking explicit authentication, idempotency tokens, or role grants are rejected with structured HTTP error codes (`401 Unauthorized`, `403 Forbidden`, `400 Bad Request`).
- **Complete Mediation:** Every REST invocation checks current user identity and ownership before reading or mutating entity state.

---

## 2. Requirement Classifications

### 2.1 Authentication Requirements
- **SEC-001 (Password Hashing):** Passwords must be hashed using BCrypt with a computational work factor of 12. Plaintext passwords must never enter logs or database tables.
- **SEC-002 (Stateless JWT Tokens):** Successful authentication yields an HMAC-SHA256 signed JWT token containing subject, issued-at timestamp, and role authorities. Expiration is set to 24 hours. Tokens must be validated on every request.
- **SEC-003 (Authentication Error Masking):** Login failure responses must return generic `"Invalid credentials"` messages to prevent username enumeration.

### 2.2 Authorization & Access Control Requirements (RBAC & BOLA)
- **SEC-004 (Role-Based Access Control):** The system defines three discrete authority tiers:
  - `ROLE_USER`: Can access own wallet, fund wallet, initiate payments, and view own transaction history.
  - `ROLE_MERCHANT`: Can register merchant profiles, view incoming merchant payments, and initiate refunds.
  - `ROLE_ADMIN`: Can inspect system audit logs, query security alerts, and inspect container health.
- **SEC-005 (Object-Level Authorization):** An authenticated user attempting to query or debit another user's wallet ID must be blocked with an HTTP 403 Forbidden exception.

### 2.3 Transaction Integrity & Financial Concurrency Requirements
- **SEC-006 (Pessimistic Concurrency Locking):** Double-spending attempts must be blocked. During payment processing, the database wallet row must be locked with `SELECT ... FOR UPDATE` (`LockModeType.PESSIMISTIC_WRITE`).
- **SEC-007 (Atomic Balance Transfer):** The debit of the user wallet and credit of the merchant wallet must execute within a single atomic `@Transactional` boundary. If an exception occurs, the entire state mutation rolls back.
- **SEC-008 (Negative Balance Prevention):** Wallets must never hold a balance `< 0.00`. Database schemas must enforce a check constraint `CHECK (balance >= 0)`.

### 2.4 Idempotency & Replay Protection Requirements
- **SEC-009 (Idempotency Enforcement):** All state-mutating payment and refund endpoints require an `Idempotency-Key` HTTP header. 
- **SEC-010 (Payload Binding & Replay Detection):** The idempotency record stores a SHA-256 hash of the request body. If a duplicate key is presented with mismatched arguments, the gateway flags the request as `REPLAY_DETECTED`, rejects the transaction, and records an audit alert.

### 2.5 Audit & Non-Repudiation Requirements
- **SEC-011 (Immutable Security Audit Trail):** Every security-relevant lifecycle event must be logged in an append-only `audit_logs` table containing timestamp, actor ID, action type, resource ID, outcome, and client IP.
- **SEC-012 (Data Sanitization in Logs):** Sensitive elements (credit card PANs, passwords, JWT secrets) must be sanitized and scrubbed prior to logging.
