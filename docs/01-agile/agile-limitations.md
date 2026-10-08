# Agile Limitations and Risks in Security-Critical Financial Software

While Agile methodologies (Scrum, XP) offer rapid iteration and customer responsiveness, pure Agile frameworks present inherent risks when applied to security-critical domains such as digital wallets and payment gateways. This document examines two primary risks and their engineering mitigations within the DWPG architecture.

---

## Risk 1: Over-Prioritization of Velocity Leading to Security Debt ("Security as an Afterthought")

### Nature of the Risk
In standard Agile Scrum, sprint velocity is measured by functional story points delivered to the customer ("Working software is the primary measure of progress"). Security controls (such as threat modeling, cryptographic verification, pessimistic concurrency locks, and rate limiting) are often invisible to end users and do not produce overt UI features. Consequently, product owners may deprioritize non-functional security requirements in favor of visual features, introducing severe architectural flaws like race conditions and double-spending vulnerabilities into production.

### Real-World Consequence in Financial Gateways
A team rushing to release "Instant Wallet Top-up" may use basic non-locking ORM updates. The feature works perfectly in single-user demo environments, but collapses under real-world concurrency, causing fraudulent double-spending and massive simulated balance leaks.

### Engineering Mitigations in DWPG
1. **Security-Integrated Definition of Done (DoD):** A user story cannot transition to "DONE" unless it satisfies explicit Security Acceptance Criteria, achieves clean SonarQube SAST analysis (0 vulnerabilities), and passes automated negative concurrency test suites.
2. **Dedicated Security Epics & Spikes:** Security is allocated dedicated backlog capacity. In DWPG, `EPIC-06 (Security & Audit)` and `EPIC-07 (DevSecOps)` receive committed story points alongside functional epics.
3. **Automated Continuous Verification in CI/CD:** High-risk checks (e.g., automated thread concurrency tests and secret scanning) execute in every build pipeline, halting promotion if a security regression is detected.

---

## Risk 2: Incremental Architectural Degradation ("Architecture by Emergence" Failing Cryptographic & Transactional Invariants)

### Nature of the Risk
Agile emphasizes "emergent architecture" where designs evolve organically through small iterations without upfront heavy architecture design. However, financial transaction systems rely on strict foundational invariants:
- Distributed ACID transaction boundaries
- Cryptographic key management lifecycles
- Immutable audit log non-repudiation
- Row-level database isolation

Attempting to retrofit transactional consistency or immutable audit hashing into an existing loosely-coupled codebase often requires complete architectural rewrites and introduces brittle edge cases.

### Real-World Consequence in Financial Gateways
If database schemas are designed incrementally without foreign key constraints, unique idempotency constraints, or pessimistic lock indexes, retrofitting concurrency controls after thousands of lines of service code are written becomes error-prone and invites data corruption.

### Engineering Mitigations in DWPG
1. **Upfront Foundational Architecture & Threat Modeling (Phases 1–8):** Prior to sprint execution, a rigorous Architectural Spike defines trust boundaries, STRIDE threat models, normalized database models, and transaction state machines.
2. **Hard Database Constraints & Invariants:** Enforcing checks at the schema layer (e.g., `CHECK (balance >= 0)`, unique `idempotency_key` constraint) ensures that even if application logic suffers an edge-case regression, the database strictly prevents invalid states.
3. **XP Collective Code Ownership & Security Pair Programming:** High-risk transaction modules (e.g., `PaymentService`, `RefundService`) require strict code review and automated integration tests before merge.
