# Security Policy - Digital Wallet and Payment Gateway Simulator (DWPG)

## 1. Security Architecture Overview
The Digital Wallet and Payment Gateway Simulator is engineered with defense-in-depth principles:
- **Authentication:** Stateless JSON Web Tokens (JJWT 0.12.5) signed with HMAC-SHA256 (256-bit entropy). BCrypt hashing (strength factor 12) for salted password storage.
- **Authorization:** Fine-grained Spring Security Method Security (`@PreAuthorize`) enforcing Role-Based Access Control (`ROLE_USER`, `ROLE_MERCHANT`, `ROLE_ADMIN`) and Object-Level Principal Ownership.
- **Transaction Integrity:** Database isolation using `@Transactional(isolation = Isolation.READ_COMMITTED)` paired with Pessimistic Write Locking (`LockModeType.PESSIMISTIC_WRITE`) on Wallet balance entities to prevent race conditions and double-spending.
- **Idempotency & Replay Protection:** Client-submitted `Idempotency-Key` headers stored in an append-only unique constraint table with SHA-256 request payload hashing and timestamp window enforcement. Duplicate submissions return the cached response without re-executing state mutation.
- **Tampering Countermeasures:** Zero trust in client-provided balances, payment states, or sender IDs. All business state is derived strictly from the authenticated security context and database truth.
- **Audit Logging:** Dedicated, append-only `AuditLog` entity capturing actor ID, event type, resource ID, IP address, status, and timestamp. Secrets, credit card numbers, and tokens are scrubbed prior to persistence.
- **Container Hardening:** Minimal multi-stage base images (`eclipse-temurin:21-jre-alpine` / `nginx:alpine`), dedicated non-root users (`UID 10001`), read-only root filesystems where applicable, dropped capabilities.

## 2. Supported Versions
| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## 3. Reporting a Vulnerability
Security vulnerabilities should be reported directly to the security lead:
- **Contact:** sathvikvalivety
- **Academic Environment:** 24CYS401 Secure Software Engineering Laboratory
- **SLA:** Vulnerability triage occurs within 24 hours.

## 4. Secrets Management Policy
- **No Hard-coded Secrets:** API keys, passwords, private keys, and JWT secrets must NEVER be committed to source control.
- **Environment Isolation:** Local configurations use `.env` files which are strictly excluded by `.gitignore`. Template variables are tracked in `.env.example`.
- **Kubernetes Secrets:** Production credentials are injected via Kubernetes `Secret` resources (`k8s/secret.yaml`).
- **Static Analysis Enforcement:** SonarQube SAST scans and git hooks inspect all changes for hard-coded credentials prior to promotion.
