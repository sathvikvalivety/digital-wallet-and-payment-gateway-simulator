# Digital Wallet and Payment Gateway Simulator (DWPG)
**Course:** 24CYS401 Secure Software Engineering End Semester Laboratory Examination  
**Author / Candidate:** sathvikvalivety  
**Academic Environment:** Ubuntu Linux  
**Status:** Fully Implemented, Tested, Hardened, Containerized & Validated  

---

## 1. Project Overview
The **Digital Wallet and Payment Gateway Simulator (DWPG)** is an enterprise-grade, defense-in-depth financial simulation platform engineered strictly to satisfy all 16 phases of the Secure Software Engineering lifecycle. 

> **NOTICE:** This system is a **SIMULATOR**. It does **NOT** process real fiat currency and does **NOT** integrate with real banking clearing houses (e.g., SWIFT, ACH, NPCI). All account balances, transactions, and merchant settlements are purely simulated using secure atomic computational ledgers.

The application addresses critical financial cybersecurity threat vectors including:
- **Replay Attacks** (RFC 7231 Idempotency Key validation, Nonces, Server-side cache validation)
- **Double Spending & Race Conditions** (Pessimistic Write Locking `@Lock(LockModeType.PESSIMISTIC_WRITE)`, atomic transactional boundaries)
- **Transaction Tampering & Parameter Pollution** (Cryptographic signing, server-side truth enforcement)
- **Broken Object Level Authorization (BOLA / IDOR)** (Spring Security `@PreAuthorize`, Principal verification)
- **Non-Repudiation & Audit Logging** (Append-only immutable audit trail capturing 12 security-critical event types)

---

## 2. Layered Architecture
```
                  +----------------------------------------------+
                  |         React 18 + Vite Web Client           |
                  |     (TailwindCSS, Formik, Axios, DOMPurify)  |
                  +----------------------+-----------------------+
                                         | HTTPS / REST (JSON)
                                         v
                  +----------------------------------------------+
                  |      Spring Boot API Gateway & Filter        |
                  |  - JwtAuthenticationFilter                   |
                  |  - RateLimiting / SecurityHeadersFilter      |
                  |  - GlobalExceptionHandler                    |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------------------------------+
                  |     Role-Based Access Control (RBAC)         |
                  |    USER  |  MERCHANT  |  ADMIN               |
                  +----------------------+-----------------------+
                                         |
            +----------------------------+----------------------------+
            |                            |                            |
            v                            v                            v
     +--------------+             +--------------+             +--------------+
     | Wallet Svc   |             | Payment Svc  |             | Merchant Svc |
     | - Balance    |             | - Atomic FSM |             | - Api Keys   |
     | - Concurrency|             | - Idempotency|             | - Settlement |
     +--------------+             +--------------+             +--------------+
            |                            |                            |
            +----------------------------+----------------------------+
                                         |
            +----------------------------+----------------------------+
            |                                                         |
            v                                                         v
     +--------------+                                          +--------------+
     | Refund Svc   |                                          | Audit Svc    |
     | - State Valid|                                          | - Immutable  |
     +--------------+                                          +--------------+
                                         |
                                         v
                  +----------------------------------------------+
                  |        Data Access Layer (Spring JPA)        |
                  | - Pessimistic Locking & ACID Boundaries      |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------------------------------+
                  |          MariaDB Persistence Store           |
                  +----------------------------------------------+
```

---

## 3. Technology Stack
- **Backend Runtime:** Java 21 LTS (Eclipse Temurin)
- **Backend Framework:** Spring Boot 3.3.4, Spring Security 6, Spring Data JPA, Hibernate, JJWT 0.12.5, H2 / MariaDB
- **Build System:** Apache Maven 3.9.6
- **Database:** MariaDB 11.4 / Hibernate Dialect (ACID transactions, Row-level Locking)
- **Frontend:** React 18, Vite, Axios, Lucide Icons, Modern CSS
- **Containerization:** Docker (Multi-stage build, non-root user), Docker Compose v2
- **Orchestration:** Kubernetes / Minikube manifests (ConfigMaps, Secrets, Resource Quotas, Security Contexts)
- **Static Analysis & SAST:** SonarQube LTS Community
- **Testing:** JUnit 5, MockMvc, Testcontainers / H2 In-Memory DB, Concurrency Multi-Threaded Stress Tests, Fuzzing Suite
- **Issue Tracking & Agile:** Atlassian Jira Cloud (`DWPG` Project, Scrum Board, 2 Sprints, Burndown, Velocity)
- **Documentation:** Microsoft Word `.docx` (Full 63-section Report), draw.io diagrams (`.drawio` + `.png`), Markdown

---

## 4. Quick Start & Execution Commands

### Prerequisites
- Java 21 (`java -version`)
- Maven 3.9+ (`mvn -version`)
- Node.js 18+ & npm (`node -v`)
- Docker & Docker Compose (`docker compose version`)

### 1. Build and Run Backend
```bash
# Navigate to backend directory
cd backend

# Run automated test suite (Unit, Integration, Concurrency, Rollback, Fuzzing)
mvn clean test

# Run application locally
mvn spring-boot:run
```

### 2. Build and Run Frontend
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 3. Run Entire Stack in Docker Compose
```bash
# From repository root
docker compose up --build -d

# Check running services
docker compose ps
```

### 4. Deploy to Kubernetes / Minikube
```bash
# Apply namespace, configmap, secrets and services
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/database-deployment.yaml
kubectl apply -f k8s/database-service.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml

# Verify pods
kubectl get pods -n dwpg
```

---

## 5. Security & Exam Phase Documentation Index

All documentation deliverables for all 16 phases of the Secure Software Engineering examination are organized in `docs/`:

| Phase | Phase Title & Marks | Primary Documentation Deliverables | Implementation Status |
|:---:|---|---|:---:|
| **01** | **Agile Development** [2M] | [`docs/01-agile/`](file:///home/sathvik/sse_project_lab_exam/docs/01-agile/) (Manifesto, Refactoring, Limitations) | **COMPLETE** |
| **02** | **Requirements Engineering** [4M] | [`docs/02-requirements/`](file:///home/sathvik/sse_project_lab_exam/docs/02-requirements/) (SRS, FR/NFR, CIA Classification) | **COMPLETE** |
| **03** | **UML Modeling** [4M] | [`docs/03-uml/`](file:///home/sathvik/sse_project_lab_exam/docs/03-uml/) (Use Cases, Sequence, Analysis Models) | **COMPLETE** |
| **04** | **Data Flow Modeling** [4M] | [`docs/04-data-flow/`](file:///home/sathvik/sse_project_lab_exam/docs/04-data-flow/) (DFD 0/1, ER Diagram, Trust Boundaries) | **COMPLETE** |
| **05** | **Architecture Design** [4M] | [`docs/05-architecture/`](file:///home/sathvik/sse_project_lab_exam/docs/05-architecture/) (Layered Arch, Components, Design Patterns) | **COMPLETE** |
| **06** | **UI/UX Design** [3M] | [`docs/06-ui/`](file:///home/sathvik/sse_project_lab_exam/docs/06-ui/) (Wireframes, Defense-in-Depth UI Rationale) | **COMPLETE** |
| **07** | **Security Engineering** [4M] | [`docs/07-security/`](file:///home/sathvik/sse_project_lab_exam/docs/07-security/) (STRIDE Threat Model, CIA Matrix, Threat Flows) | **COMPLETE** |
| **08** | **Attack Trees** [3M] | [`docs/08-attack-tree/`](file:///home/sathvik/sse_project_lab_exam/docs/08-attack-tree/) (Attack Tree Probes, Refined Controls) | **COMPLETE** |
| **09** | **Product Backlog** [3M] | [`docs/09-backlog/`](file:///home/sathvik/sse_project_lab_exam/docs/09-backlog/) (Jira Stories, Acceptance Criteria) | **COMPLETE** |
| **10** | **Sprint Metrics** [3M] | [`docs/10-sprint-metrics/`](file:///home/sathvik/sse_project_lab_exam/docs/10-sprint-metrics/) (Burndown, Velocity, Scrum Retrospectives) | **COMPLETE** |
| **11** | **Secure Build Environment** [4M] | [`docs/11-secure-build/`](file:///home/sathvik/sse_project_lab_exam/docs/11-secure-build/) (SonarQube SAST Report, Quality Gate OK) | **COMPLETE** |
| **12** | **Secure Coding & Refactoring** [5M] | [`docs/12-secure-coding/`](file:///home/sathvik/sse_project_lab_exam/docs/12-secure-coding/) (Vulnerability Remediation, Before/After) | **COMPLETE** |
| **13** | **Containerized Development** [7M] | [**Phase 13 Specification**](file:///home/sathvik/sse_project_lab_exam/docs/13-docker-kubernetes/PHASE-13-CONTAINERIZATION.md) (`backend/Dockerfile`, `frontend/Dockerfile`, `k8s/*.yaml`, non-root, PSS Restricted) | **COMPLETE** |
| **14** | **CI/CD & Security Testing** [7M] | [**Phase 14 Specification**](file:///home/sathvik/sse_project_lab_exam/docs/14-cicd-testing/PHASE-14-CICD-TESTING.md) (`.github/workflows/ci.yml`, 36 Tests, Fuzzing, DEF-001/002) | **COMPLETE** |
| **15** | **Hardening & Deployment** [5M] | [**Phase 15 Specification**](file:///home/sathvik/sse_project_lab_exam/docs/15-hardening/PHASE-15-HARDENING-DEPLOYMENT.md) (12 Event Types, 5 Alerts, Pre-flight Checklist) | **COMPLETE** |
| **16** | **Final Capstone Report** [5M] | [`docs/final/`](file:///home/sathvik/sse_project_lab_exam/docs/final/) (`Digital_Wallet_Payment_Gateway_Secure_Software_Engineering_Final_Report.docx` & `.pdf`, Traceability Matrix) | **COMPLETE** |
