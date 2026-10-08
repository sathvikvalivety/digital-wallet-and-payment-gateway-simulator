import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import datetime

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tbl.rows[0].cells[0]
    c.width = Inches(6.5)
    set_cell_background(c, "F1F5F9")
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(code_text)
    run.font.name = "Courier New"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph()

def create_report():
    doc = docx.Document()

    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("PHASE 13: CONTAINERIZED DEVELOPMENT AND ORCHESTRATION\nDOCKER & KUBERNETES SECURITY SPECIFICATION")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(20)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(30, 58, 138)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("Hardened Multi-Stage Containers, Pod Security Standards & Zero-Trust Network Segmentation\nCourse: 24CYS401 Secure Software Engineering | Academic Year 2026")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(10.5)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_paragraph()

    # Meta Table
    table = doc.add_table(rows=5, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta = [
        ("Project System", "Digital Wallet and Payment Gateway Simulator (DWPG)"),
        ("Container Runtimes", "Docker Engine 24+ / containerd, Kubernetes / Minikube v1.39"),
        ("Base Images", "eclipse-temurin:21-jre-alpine (Backend), nginxinc/nginx-unprivileged:alpine (Frontend)"),
        ("Security Compliance", "Kubernetes Pod Security Standard (Restricted Profile), CIS Docker Benchmark"),
        ("Lead DevSecOps Engineer", "Sathvik Valivety (GitHub: sathvikvalivety)")
    ]
    for idx, (k, v) in enumerate(meta):
        r = table.rows[idx]
        r.cells[0].width = Inches(2.2)
        r.cells[1].width = Inches(4.3)
        set_cell_background(r.cells[0], "F1F5F9")
        set_cell_background(r.cells[1], "FFFFFF")
        r.cells[0].paragraphs[0].add_run(k).font.bold = True
        r.cells[0].paragraphs[0].runs[0].font.size = Pt(9.5)
        r.cells[1].paragraphs[0].add_run(v).font.size = Pt(9.5)

    doc.add_page_break()

    # Section 1
    doc.add_heading("1. Executive Containerization Strategy", level=1)
    doc.add_paragraph(
        "Containerization provides deterministic, reproducible runtime environments while isolating application services. "
        "In enterprise financial applications, containers represent a critical security boundary. "
        "Phase 13 details the complete containerization architecture for the DWPG Simulator, incorporating non-root execution, "
        "minimal attack surface base images, multi-container Docker Compose orchestration, and Kubernetes Pod Security Standards."
    )

    # Section 2
    doc.add_heading("2. Hardened Multi-Stage Dockerfile Architecture", level=1)
    doc.add_paragraph(
        "Both backend and frontend services implement strict multi-stage builds and security hardening controls:"
    )

    doc.add_heading("Backend Dockerfile Security Controls (backend/Dockerfile):", level=2)
    doc.add_paragraph(
        "1. Minimal Base Image: Built upon Alpine Linux with Eclipse Temurin JRE 21, stripping development compilers, headers, and package tools from the runtime.\n"
        "2. Unprivileged Execution: Explicitly creates system group 'appgroup' and user 'appuser' (UID 10001 / GID 10001). Root access is strictly prohibited.\n"
        "3. Container Memory Management: Configured with -XX:+UseContainerSupport and -XX:MaxRAMPercentage=75.0 to prevent cgroup out-of-memory kernel kills.\n"
        "4. Cryptographic Entropy: Forces -Djava.security.egd=file:/dev/./urandom ensuring non-blocking cryptographic random generation for JWT and token signing.\n"
        "5. Automated Healthcheck: Actuator endpoint /actuator/health is polled every 30s using wget spider mode."
    )

    backend_docker = """FROM eclipse-temurin:21-jre-alpine AS runtime
RUN addgroup -g 10001 -S appgroup && \\
    adduser -u 10001 -S appuser -G appgroup
WORKDIR /app
COPY --chown=appuser:appgroup target/dwpg-simulator-1.0.0.jar /app/dwpg-simulator.jar
USER 10001:10001
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \\
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1
ENTRYPOINT ["java", "-XX:+UseContainerSupport", "-XX:MaxRAMPercentage=75.0", \\
            "-Djava.security.egd=file:/dev/./urandom", "-jar", "/app/dwpg-simulator.jar"]"""
    add_code_block(doc, backend_docker)

    doc.add_heading("Frontend Dockerfile Security Controls (frontend/Dockerfile):", level=2)
    doc.add_paragraph(
        "1. Unprivileged Web Server: Built on 'nginxinc/nginx-unprivileged:alpine' running as UID 101 ('nginx') on port 3000.\n"
        "2. Defense-in-Depth HTTP Headers: Injected directly at the Nginx reverse-proxy layer:\n"
        "   - X-Frame-Options: SAMEORIGIN (prevents clickjacking attacks)\n"
        "   - X-Content-Type-Options: nosniff (prevents MIME sniffing)\n"
        "   - Content-Security-Policy: default-src 'self' (mitigates XSS injection)\n"
        "   - Referrer-Policy: strict-origin-when-cross-origin (prevents token leakage)\n"
        "3. Internal Network Proxying: Nginx forwards /api/ requests to the backend container over internal Docker DNS."
    )

    doc.add_paragraph()

    # Section 3
    doc.add_heading("3. Multi-Container Orchestration with Docker Compose", level=1)
    doc.add_paragraph(
        "The docker-compose.yml manifest configures a full 3-tier topology with health-checked dependency ordering:"
    )

    t_dc = doc.add_table(rows=4, cols=4)
    t_dc.alignment = WD_TABLE_ALIGNMENT.CENTER
    dc_hdr = t_dc.rows[0]
    for i, h in enumerate(["Service", "Image / Build", "Exposed Ports", "Security & Health Configuration"]):
        dc_hdr.cells[i].paragraphs[0].add_run(h).font.bold = True
        set_cell_background(dc_hdr.cells[i], "1E3A8A")
        dc_hdr.cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    dc_data = [
        ("mariadb", "mariadb:11.4", "Internal 3306", "Persistent volume mariadb_data, mariadb-admin ping healthcheck, credentials from .env"),
        ("backend", "dwpg-backend:1.0.0", "Host 8080", "Depends on mariadb healthy, runs as UID 10001, Spring Actuator healthcheck"),
        ("frontend", "dwpg-frontend:1.0.0", "Host 3000", "Depends on backend healthy, runs as UID 101, unprivileged Nginx reverse proxy")
    ]
    for idx, (svc, img, prt, sec) in enumerate(dc_data, start=1):
        row = t_dc.rows[idx]
        row.cells[0].paragraphs[0].add_run(svc).font.bold = True
        row.cells[0].paragraphs[0].runs[0].font.size = Pt(8.5)
        row.cells[1].paragraphs[0].add_run(img).font.size = Pt(8.5)
        row.cells[2].paragraphs[0].add_run(prt).font.size = Pt(8.5)
        row.cells[3].paragraphs[0].add_run(sec).font.size = Pt(8.5)
        bg = "F8FAFC" if idx % 2 == 1 else "FFFFFF"
        for c in row.cells:
            set_cell_background(c, bg)

    doc.add_paragraph()

    # Section 4
    doc.add_heading("4. Production Kubernetes Architecture (k8s/)", level=1)
    doc.add_paragraph(
        "The Kubernetes deployment architecture implements enterprise security controls across 11 manifests in the 'dwpg' namespace:"
    )

    k8s_manifests = [
        ("00-namespace.yaml", "Namespace Isolation", "Creates isolated 'dwpg' tenant namespace with 24CYS401 governance labels."),
        ("01-configmap.yaml", "Configuration Management", "Stores non-confidential configuration (JDBC URL, Hibernate DDL, JWT expiration)."),
        ("02-secret.yaml", "Sensitive Secret Storage", "Stores credentials (MariaDB password, root password, 256-bit JWT secret)."),
        ("03-mariadb-pvc.yaml", "Storage Persistence", "Allocates 5Gi ReadWriteOnce persistent storage volume for MariaDB transactional data."),
        ("04-mariadb-deployment.yaml", "Database Controller", "Deploys MariaDB pod with CPU/memory limits, readiness/liveness health probes."),
        ("05-mariadb-service.yaml", "Internal Database Service", "ClusterIP service binding MariaDB port 3306 inside cluster DNS."),
        ("06-backend-deployment.yaml", "API Tier Controller", "Hardened 2-replica deployment enforcing PSS Restricted: runAsNonRoot, UID 10001, drop ALL capabilities."),
        ("07-backend-service.yaml", "Internal API Service", "ClusterIP service routing traffic across healthy backend replica pods on port 8080."),
        ("08-frontend-deployment.yaml", "UI Tier Controller", "2-replica deployment running unprivileged Nginx (UID 101) with CPU/memory quotas."),
        ("09-frontend-service.yaml", "External Ingress Service", "NodePort service exposing frontend on port 30080 for client browser access."),
        ("10-networkpolicy.yaml", "Zero-Trust Network Isolation", "Default-deny ingress on MariaDB; exclusively permits TCP 3306 ingress from dwpg-backend pods.")
    ]

    t_k8s = doc.add_table(rows=12, cols=3)
    t_k8s.alignment = WD_TABLE_ALIGNMENT.CENTER
    k_hdr = t_k8s.rows[0]
    for i, h in enumerate(["Manifest File", "Resource Type", "Security Specification"]):
        k_hdr.cells[i].paragraphs[0].add_run(h).font.bold = True
        set_cell_background(k_hdr.cells[i], "1E3A8A")
        k_hdr.cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    for idx, (mfile, rtype, spec) in enumerate(k8s_manifests, start=1):
        row = t_k8s.rows[idx]
        row.cells[0].paragraphs[0].add_run(mfile).font.bold = True
        row.cells[0].paragraphs[0].runs[0].font.size = Pt(8.5)
        row.cells[1].paragraphs[0].add_run(rtype).font.size = Pt(8.5)
        row.cells[2].paragraphs[0].add_run(spec).font.size = Pt(8.5)
        bg = "F8FAFC" if idx % 2 == 1 else "FFFFFF"
        for c in row.cells:
            set_cell_background(c, bg)

    doc.add_paragraph()

    # Section 5
    doc.add_heading("5. Container & Pod Threat Mitigation Matrix", level=1)
    t_threat = doc.add_table(rows=5, cols=3)
    t_threat.alignment = WD_TABLE_ALIGNMENT.CENTER
    th_hdr = t_threat.rows[0]
    for i, h in enumerate(["Threat Vector", "Impact Severity", "Engineered Defensive Control"]):
        th_hdr.cells[i].paragraphs[0].add_run(h).font.bold = True
        set_cell_background(th_hdr.cells[i], "334155")
        th_hdr.cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    threat_data = [
        ("Container Escape / Host Takeover", "CRITICAL", "runAsNonRoot: true, runAsUser: 10001, allowPrivilegeEscalation: false, capabilities drop: ['ALL']."),
        ("Pod-to-Pod Lateral Movement", "HIGH", "k8s NetworkPolicy isolates MariaDB port 3306 strictly to backend pods; frontend cannot communicate with database directly."),
        ("Denial of Service (Resource Exhaustion)", "HIGH", "Strict CPU (1000m) and Memory (1Gi) requests and limits enforce fair resource sharing under cgroups."),
        ("Secret Leakage in Revision Control", "HIGH", "Zero secrets committed to Git repository; managed via Kubernetes Secrets and .env / .env.example abstraction.")
    ]

    for idx, (vec, sev, ctl) in enumerate(threat_data, start=1):
        row = t_threat.rows[idx]
        row.cells[0].paragraphs[0].add_run(vec).font.bold = True
        row.cells[0].paragraphs[0].runs[0].font.size = Pt(8.5)
        row.cells[1].paragraphs[0].add_run(sev).font.size = Pt(8.5)
        row.cells[2].paragraphs[0].add_run(ctl).font.size = Pt(8.5)
        bg = "F8FAFC" if idx % 2 == 1 else "FFFFFF"
        for c in row.cells:
            set_cell_background(c, bg)

    doc.save("docs/13-containers/containerization-report.docx")
    print("Report written to docs/13-containers/containerization-report.docx")

if __name__ == "__main__":
    create_report()
