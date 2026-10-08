# Phase 13: Containerized Development — Docker and Kubernetes [7 Marks]

**Course:** 24CYS401 Secure Software Engineering  
**Project:** Digital Wallet and Payment Gateway Simulator (DWPG)  
**Author / Candidate:** Sathvik Valivety  
**Academic Environment:** Ubuntu Linux, Docker Compose v2, Minikube Kubernetes v1.34  
**Evaluation Marks:** 7 Marks  
**Status:** FULLY IMPLEMENTED, HARDENED & VERIFIED LIVE  

---

## Executive Summary

Phase 13 establishes a production-grade, hardened containerization and orchestration environment for the DWPG Simulator. All application tiers—the Spring Boot 3.3.4 backend API, the React 18 / Vite unprivileged Nginx frontend, the MariaDB 11.4 relational database, and the SonarQube LTS security platform—are fully containerized and orchestrated via both **Docker Compose** and **Kubernetes (Minikube)**.

---

## 1. Application Containerization & Dockerfiles

### 1.1 Backend Containerization (`backend/Dockerfile`)
The backend microservice utilizes a hardened Alpine-based Java 21 runtime:

```dockerfile
FROM eclipse-temurin:21-jre-alpine AS runtime

LABEL maintainer="sathvikvalivety" \
      project="dwpg-simulator" \
      security.hardened="true"

# Create unprivileged system group and user (UID/GID 10001)
RUN addgroup -g 10001 -S appgroup && \
    adduser -u 10001 -S appuser -G appgroup

WORKDIR /app

# Copy runnable fat JAR with proper ownership
COPY --chown=appuser:appgroup target/dwpg-simulator-1.0.0.jar /app/dwpg-simulator.jar

# Enforce least privilege execution
USER 10001:10001

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1

ENTRYPOINT ["java", \
  "-XX:+UseContainerSupport", \
  "-XX:MaxRAMPercentage=75.0", \
  "-Djava.security.egd=file:/dev/./urandom", \
  "-jar", "/app/dwpg-simulator.jar"]
```

### 1.2 Frontend Containerization (`frontend/Dockerfile`)
The frontend SPA is served by an unprivileged Nginx web server:

```dockerfile
FROM nginxinc/nginx-unprivileged:alpine AS runtime

LABEL maintainer="sathvikvalivety" \
      project="dwpg-simulator-frontend" \
      security.hardened="true"

COPY dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:3000/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
```

### 1.3 Multi-Container Orchestration (`docker-compose.yml`)
The entire application topology is orchestrated with service health dependencies:
- **`dwpg-mariadb`**: MariaDB 11.4 with healthcheck ping (`mariadb-admin ping`).
- **`dwpg-backend`**: Depends on MariaDB (`condition: service_healthy`), exposed on port `8080`.
- **`dwpg-frontend`**: Depends on Backend (`condition: service_healthy`), exposed on port `3000`.
- **`dwpg-network`**: Isolated bridge network preventing unauthorized external routing.
- **`mariadb_data`**: Named persistent volume guaranteeing ACID transaction data persistence.

---

## 2. Container Security Practices Applied (Rubric: At least 4 practices)

The DWPG container architecture applies **five** core container security controls:

| # | Security Practice | Technical Implementation in DWPG | Security Justification & CWE Defense |
|---|---|---|---|
| **1** | **Minimal Base Image** | `eclipse-temurin:21-jre-alpine` (compressed **129 MB**) and `nginxinc/nginx-unprivileged:alpine` (**25.9 MB**). No compilers, debuggers, or package managers remain in the runtime image. | Eliminates unnecessary binaries (curl, gcc, python) reducing CVE attack surface. Complies with CIS Benchmark §4.3. |
| **2** | **Non-Root Execution** | Explicitly executes under dedicated unprivileged users: `USER 10001:10001` (`appuser`) for Backend; `USER 101:101` (`nginx`) for Frontend. | Prevents container breakout privilege escalation to host root (CWE-250: Execution with Unnecessary Privileges). |
| **3** | **Controlled & Unprivileged Ports** | Backend binds exclusively to port `8080`; Frontend binds to port `3000`. Privileged ports (`< 1024`) are strictly disallowed. | Mitigates port spoofing and eliminates the requirement for `CAP_NET_BIND_SERVICE`. |
| **4** | **Secret Handling & Environmental Decoupling** | Zero secrets, private keys, or passwords exist in image layers. `.dockerignore` excludes `.env`, `*.key`, and credential files. Credentials (`JWT_SECRET`, `MARIADB_PASSWORD`) are injected at runtime via environment variables and Kubernetes Secrets. | Prevents credential leaks in public registries (CWE-798: Use of Hard-coded Credentials). |
| **5** | **Container Resource Bounds & Entropy Tuning** | Configured `-XX:+UseContainerSupport`, `-XX:MaxRAMPercentage=75.0`, and mapped entropy to `-Djava.security.egd=file:/dev/./urandom`. Built-in Docker `HEALTHCHECK` probes prevent zombie container accumulation. | Mitigates Denial of Service (DoS) from JVM out-of-memory crashes and cryptographic PRNG exhaustion. |

---

## 3. Kubernetes Deployment and Service Architecture

A complete 11-manifest production suite is implemented in the `k8s/` directory and deployed on Minikube under the isolated `dwpg` namespace:

```
k8s/
├── 00-namespace.yaml          # Dedicated dwpg namespace with PSS Restricted enforcement
├── 01-configmap.yaml          # Non-sensitive runtime properties (JDBC URL, profiles)
├── 02-secret.yaml             # Base64-sealed DB credentials and JWT HMAC-SHA256 signing key
├── 03-mariadb-pvc.yaml        # 5Gi ReadWriteOnce PersistentVolumeClaim
├── 04-mariadb-deployment.yaml # MariaDB 11.4 Stateful Pod Deployment
├── 05-mariadb-service.yaml    # Internal ClusterIP service on port 3306
├── 06-backend-deployment.yaml # 2-replica High-Availability Spring Boot Deployment
├── 07-backend-service.yaml    # ClusterIP service on port 8080 (dwpg-backend-service & backend)
├── 08-frontend-deployment.yaml# 2-replica Unprivileged Nginx Deployment
├── 09-frontend-service.yaml   # NodePort service exposing UI externally on port 30080
└── 10-networkpolicy.yaml      # Zero-Trust network segmentation rules
```

---

## 4. Kubernetes Security Controls Applied (Rubric: At least 2 controls)

The deployment implements **four** robust Kubernetes security controls:

### Control 1: Pod Security Standards (PSS) & Namespace Isolation
The `dwpg` namespace (`k8s/00-namespace.yaml`) enforces the official Kubernetes **Restricted Pod Security Standard**:
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: dwpg
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

### Control 2: Non-Root Security Context & Privilege De-escalation
In `k8s/06-backend-deployment.yaml`, the pod specification enforces non-root execution and drops all Linux capabilities:
```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 10001
    runAsGroup: 10001
    fsGroup: 10001
  containers:
    - name: backend
      securityContext:
        allowPrivilegeEscalation: false
        capabilities:
          drop:
            - ALL
```

### Control 3: Strict CPU & Memory Resource Quotas
Both backend and frontend pods enforce CPU and memory request/limit quotas to prevent resource starvation:
```yaml
resources:
  requests:
    cpu: 300m
    memory: 512Mi
  limits:
    cpu: 1000m
    memory: 1Gi
```

### Control 4: Zero-Trust Network Segmentation (`k8s/10-networkpolicy.yaml`)
Two microsegmentation policies isolate network traffic at Layer 3/4:
1. **`isolate-mariadb`**: Restricts incoming TCP traffic on port `3306` **strictly** to pods carrying label `app: dwpg-backend`. The frontend and foreign pods cannot establish direct socket connections to MariaDB.
2. **`backend-network-policy`**: Restricts incoming TCP traffic on port `8080` strictly to pods carrying label `app: dwpg-frontend`.

---

## 5. Empirical Live Deployment Evidence

### 5.1 Docker Compose Live Verification
```text
$ docker compose ps
NAME            IMAGE                           STATUS                  PORTS
dwpg-backend    sse_project_lab_exam-backend    Up (healthy)            0.0.0.0:8080->8080/tcp
dwpg-frontend   sse_project_lab_exam-frontend   Up (healthy)            0.0.0.0:3000->3000/tcp
dwpg-mariadb    mariadb:11.4                    Up (healthy)            3306/tcp
sonarqube       sonarqube:lts-community         Up                      0.0.0.0:9000->9000/tcp
```

### 5.2 Kubernetes (Minikube) Cluster Live Verification
```text
$ kubectl get all -n dwpg
NAME                                READY   STATUS    RESTARTS   AGE
pod/dwpg-backend-5dc65f7b58-4kstq   1/1     Running   0          3m
pod/dwpg-backend-7cd4d58cb9-2phww   1/1     Running   0          3m
pod/dwpg-frontend-dd9cc6c-25ck6     1/1     Running   0          3m
pod/dwpg-frontend-dd9cc6c-86n9q     1/1     Running   0          3m
pod/dwpg-mariadb-764985446-q6kqp    1/1     Running   0          3h

NAME                            TYPE        CLUSTER-IP       PORT(S)          AGE
service/backend                 ClusterIP   10.107.97.72     8080/TCP         3m
service/dwpg-backend-service    ClusterIP   10.110.48.46     8080/TCP         3h
service/dwpg-frontend-service   NodePort    10.111.214.148   3000:30080/TCP   3h
service/dwpg-mariadb-service    ClusterIP   10.96.193.236    3306/TCP         3h

NAME                            READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/dwpg-backend    2/2     2            2           3h
deployment.apps/dwpg-frontend   2/2     2            2           3h
deployment.apps/dwpg-mariadb    1/1     1            1           3h
```

### 5.3 Health & Liveness Probe Proof
Backend readiness and liveness endpoints verify Spring Boot Actuator health status:
```bash
$ curl -s http://localhost:8080/actuator/health
{"status":"UP","components":{"db":{"status":"UP","details":{"database":"MariaDB","validationQuery":"isValid()"}},"diskSpace":{"status":"UP"},"ping":{"status":"UP"}}}
```

---

## Conclusion
Phase 13 is fully satisfied. The application is containerized with non-root security principles, minimal base images, and zero hardcoded secrets. It runs under Kubernetes with 2-replica high availability, PSS Restricted profile enforcement, strict resource boundaries, and zero-trust network policy isolation.
