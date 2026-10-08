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

## 5. Security & Exam Phase Documentation
All documentation deliverables for Phases 1 through 16 are organized in `docs/`:
- `docs/01-agile/` - Agile approach, Manifesto mapping, Refactoring opportunities, Agile limitations
- `docs/02-requirements/` - SRS document, requirements traceability, CIA classification
- `docs/03-uml/` - Use case diagrams, specifications, sequence/analysis models
- `docs/04-data-flow/` - DFD Level 0, Level 1, ER diagram, Trust boundaries
- `docs/05-architecture/` - Layered architecture, Component diagram, Design patterns
- `docs/06-ui/` - Wireframes and design rationale
- `docs/07-security/` - STRIDE threat model, Asset/CIA matrix, Information flow, Vulnerabilities
- `docs/08-attack-tree/` - Attack tree, Refined security architecture
- `docs/09-backlog/` - User stories, Acceptance criteria, Jira backlog export
- `docs/10-sprint-metrics/` - Sprint 1 & 2 reviews, Burndown, Velocity, Defect carry-over tracking
- `docs/11-secure-build/` - Secure build checklist, SonarQube SAST report
- `docs/12-secure-coding/` - Vulnerability before/after code refactoring analysis
- `docs/13-docker-kubernetes/` - Container hardening, Kubernetes security manifests
- `docs/14-cicd-testing/` - GitHub Actions pipeline, Automated test reports, Fuzzing results
- `docs/15-hardening/` - Production hardening checklist, Logging & monitoring plan
- `docs/final/` - Comprehensive End Semester Final Report (`Secure_Software_Engineering_Final_Report.docx`)
