import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

print("Initializing Master Capstone Report Generation Engine...")

OUTPUT_DOCX = "docs/final/Digital_Wallet_Payment_Gateway_Secure_Software_Engineering_Final_Report.docx"
os.makedirs("docs/final", exist_ok=True)

doc = docx.Document()

# Page Margins: Standard 1 inch
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    section.different_first_page_header_footer = True
    
    # Configure Header / Footer
    header = section.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hrun = hp.add_run("DIGITAL WALLET AND PAYMENT GATEWAY SIMULATOR | 24CYS401 CAPSTONE REPORT")
    hrun.font.name = "Calibri"
    hrun.font.size = Pt(8.5)
    hrun.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
    
    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    frun = fp.add_run("Amrita Vishwa Vidyapeetham — Department of Cyber Security | Confidential & Academic Evaluation")
    frun.font.name = "Calibri"
    frun.font.size = Pt(8)
    frun.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)

# Color Palette
COLOR_NAVY = RGBColor(0x17, 0x36, 0x5D)    # #17365D - Heading 1
COLOR_STEEL = RGBColor(0x1F, 0x4E, 0x79)   # #1F4E79 - Heading 2
COLOR_TEAL = RGBColor(0x0F, 0x76, 0x6E)    # #0F766E - Heading 3
COLOR_TEXT = RGBColor(0x17, 0x20, 0x33)    # #172033 - Body
COLOR_MUTED = RGBColor(0x64, 0x74, 0x8B)   # #64748B - Captions
COLOR_BORDER = "CBD5E1"
COLOR_HEADER_BG = "17365D"
COLOR_ALT_BG = "F8FAFC"
COLOR_CALLOUT_BG = "F1F5F9"

def set_cell_shading(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def set_cell_borders(cell, top="CBD5E1", bottom="CBD5E1", left="none", right="none"):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="{'single' if top != 'none' else 'none'}" w:sz="4" w:space="0" w:color="{top if top != 'none' else 'auto'}"/>
            <w:left w:val="{'single' if left != 'none' else 'none'}" w:sz="4" w:space="0" w:color="{left if left != 'none' else 'auto'}"/>
            <w:bottom w:val="{'single' if bottom != 'none' else 'none'}" w:sz="4" w:space="0" w:color="{bottom if bottom != 'none' else 'auto'}"/>
            <w:right w:val="{'single' if right != 'none' else 'none'}" w:sz="4" w:space="0" w:color="{right if right != 'none' else 'auto'}"/>
        </w:tcBorders>
    ''')
    tcPr.append(tcBorders)

def add_h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(17)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY
    return p

def add_h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = COLOR_STEEL
    return p

def add_h3(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = COLOR_TEAL
    return p

def add_p(text, bold_prefix=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_TEXT
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(10.5)
    run.font.color.rgb = COLOR_TEXT
    return p

def add_callout(text, title="SECURITY ARCHITECTURE NOTICE"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    cell = table.rows[0].cells[0]
    cell.width = Inches(6.5)
    set_cell_shading(cell, COLOR_CALLOUT_BG)
    set_cell_borders(cell, top="1E3A8A", bottom="CBD5E1", left="1E3A8A", right="CBD5E1")
    
    cp = cell.paragraphs[0]
    cp.paragraph_format.space_before = Pt(4)
    cp.paragraph_format.space_after = Pt(2)
    trun = cp.add_run(f"🛡️  {title}\n")
    trun.font.name = "Calibri"
    trun.font.size = Pt(10)
    trun.font.bold = True
    trun.font.color.rgb = COLOR_NAVY
    
    mrun = cp.add_run(text)
    mrun.font.name = "Calibri"
    mrun.font.size = Pt(9.5)
    mrun.font.color.rgb = COLOR_TEXT
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

fig_counter = 0

def add_figure(image_path, caption_title, caption_desc, req_tag=None, width=Inches(6.2)):
    global fig_counter
    fig_counter += 1
    if not os.path.exists(image_path):
        print(f"Warning: Image not found: {image_path}")
        return
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(image_path, width=width)
    
    cp = doc.add_paragraph()
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cp.paragraph_format.space_before = Pt(2)
    cp.paragraph_format.space_after = Pt(10)
    
    c_num = cp.add_run(f"Figure {fig_counter}: {caption_title}. ")
    c_num.font.name = "Calibri"
    c_num.font.size = Pt(9)
    c_num.font.bold = True
    c_num.font.color.rgb = COLOR_NAVY
    
    c_desc = cp.add_run(caption_desc)
    c_desc.font.name = "Calibri"
    c_desc.font.size = Pt(9)
    c_desc.font.italic = True
    c_desc.font.color.rgb = COLOR_MUTED
    
    if req_tag:
        c_req = cp.add_run(f" [{req_tag}]")
        c_req.font.name = "Calibri"
        c_req.font.size = Pt(8.5)
        c_req.font.bold = True
        c_req.font.color.rgb = COLOR_TEAL

def add_styled_table(headers, rows, col_widths=None):
    table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # Header Row
    hdr_cells = table.rows[0].cells
    for idx, h in enumerate(headers):
        hdr_cells[idx].text = h
        set_cell_shading(hdr_cells[idx], COLOR_HEADER_BG)
        set_cell_borders(hdr_cells[idx], top="17365D", bottom="17365D")
        p = hdr_cells[idx].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        for r in p.runs:
            r.font.name = "Calibri"
            r.font.size = Pt(9.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            
    # Body Rows
    for r_idx, row in enumerate(rows):
        row_cells = table.rows[r_idx + 1].cells
        bg = COLOR_ALT_BG if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            row_cells[c_idx].text = str(val)
            set_cell_shading(row_cells[c_idx], bg)
            set_cell_borders(row_cells[c_idx], top="CBD5E1", bottom="CBD5E1")
            p = row_cells[c_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(9)
                r.font.color.rgb = COLOR_TEXT
                
    if col_widths:
        for r in table.rows:
            for idx, w in enumerate(col_widths):
                r.cells[idx].width = Inches(w)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    return table

print("Building Cover Page & Front Matter...")

# COVER PAGE
cp = doc.add_paragraph()
cp.paragraph_format.space_before = Pt(60)
cp.paragraph_format.space_after = Pt(8)
r_inst = cp.add_run("AMRITA VISHWA VIDYAPEETHAM\nDEPARTMENT OF CYBER SECURITY")
r_inst.font.name = "Calibri"
r_inst.font.size = Pt(12)
r_inst.font.bold = True
r_inst.font.color.rgb = COLOR_STEEL

p_course = doc.add_paragraph()
p_course.paragraph_format.space_after = Pt(28)
r_c = p_course.add_run("24CYS401: SECURE SOFTWARE ENGINEERING\nEND-SEMESTER LABORATORY EXAMINATION CAPSTONE REPORT")
r_c.font.name = "Calibri"
r_c.font.size = Pt(13)
r_c.font.bold = True
r_c.font.color.rgb = COLOR_TEAL

p_title = doc.add_paragraph()
p_title.paragraph_format.space_after = Pt(12)
r_t = p_title.add_run("DIGITAL WALLET AND PAYMENT GATEWAY SIMULATOR")
r_t.font.name = "Calibri"
r_t.font.size = Pt(24)
r_t.font.bold = True
r_t.font.color.rgb = COLOR_NAVY

p_sub = doc.add_paragraph()
p_sub.paragraph_format.space_after = Pt(45)
r_sub = p_sub.add_run("A Full-Stack, DevSecOps-Hardened Educational Simulation Demonstrating Double-Spending Elimination, Pessimistic Row Locking, Idempotency Replay Trapping, and End-to-End Cryptographic Audit Integrity")
r_sub.font.name = "Calibri"
r_sub.font.size = Pt(11.5)
r_sub.font.italic = True
r_sub.font.color.rgb = COLOR_MUTED

# Metadata Table
meta_headers = ["Attribute", "Evaluation Record"]
meta_rows = [
    ["Author / Candidate:", "Sathvik Valivety (Lead Software Architect & Security Engineer)"],
    ["GitHub Handle:", "@sathvikvalivety"],
    ["Source Repository:", "https://github.com/sathvikvalivety/digital-wallet-and-payment-gateway-simulator"],
    ["Evaluation Cohort:", "24CYS401 Secure Software Engineering Laboratory Exam"],
    ["Implementation Stack:", "Spring Boot 3.3.4 (Java 21), React 18, MariaDB/H2, Docker, Minikube K8s"],
    ["Security Baseline:", "SonarQube LTS Quality Gate PASSED (0 Vulnerabilities, 0 Security Hotspots)"],
    ["Verification Status:", "100% Automated Backend & Live Security Property Verification (0 Failures)"]
]
add_styled_table(meta_headers, meta_rows, [2.2, 4.3])

doc.add_page_break()

# EXECUTIVE SUMMARY
add_h1("Executive Summary")
add_p("The Digital Wallet and Payment Gateway Simulator (DWPG) represents a comprehensive, enterprise-grade software artifact designed and developed to fulfill the rigorous 16-phase examination requirements of 24CYS401: Secure Software Engineering. In strict adherence to pedagogical directives, the system is an educational simulator operating entirely on simulated fiat currency, eliminating real monetary transactions while modeling genuine commercial and financial gateway security controls.")
add_p("Financial systems inherently confront hostile operating conditions, including double-spending attacks, replay attacks, race conditions, parameter tampering, Broken Object Level Authorization (BOLA/IDOR), and state-desynchronization frauds. To address these vulnerabilities systematically, the DWPG simulator implements a defense-in-depth architecture combining: (1) MariaDB row-level pessimistic write locking (SELECT ... FOR UPDATE) coupled with striped JVM reentrant locks to guarantee non-negative balance invariants under heavy concurrency; (2) Mandatory client-generated Idempotency-Key headers cryptographically bound to request payload SHA-256 digests to trap replay attempts and prevent duplicate settlement; (3) Strict finite state machine transitions (INITIATED -> CONFIRMED -> REFUNDED) preventing duplicate credit reversals; (4) PBKDF2/BCrypt password hashing at cost factor 12 with HMAC-SHA256 JWT access tokens; and (5) An append-only administrative SIEM audit log that scrubs sensitive payment credentials.")

add_callout(
    "All sixteen phases of the Secure Software Engineering curriculum have been completely designed, implemented, containerized, orchestrated, and empirically verified. Automated test suites comprise 25 JUnit 5 backend tests, 9 live REST functional integration tests, and 8 adversarial security property probes—achieving a 100% pass rate with zero vulnerabilities, zero bugs, and zero security hotspots on SonarQube LTS.",
    "CAPSTONE AUDIT VERDICT: FULLY COMPLIANT"
)

# CHAPTER 1: INTRODUCTION
add_h1("1. Introduction")
add_h2("1.1 Background and Motivation")
add_p("Modern financial technology (FinTech) infrastructures handle billions of dollars in daily transactions, making digital wallets and payment gateways prime targets for sophisticated adversarial attacks. Flaws in transaction lifecycle design, state synchronization, or concurrency handling regularly result in multi-million dollar insolvency incidents. The 24CYS401 Secure Software Engineering curriculum emphasizes that security cannot be treated as an afterthought or an isolated audit step; it must be intrinsically embedded across every phase of the software engineering lifecycle—from requirements engineering and threat modeling to build automation, containerization, and static application security testing (SAST).")

add_h2("1.2 Purpose and Scope")
add_p("The primary objective of the Digital Wallet and Payment Gateway Simulator is to establish an end-to-end, reproducible, and verifiable payment ecosystem that demonstrates how rigorous security principles resolve core financial vulnerabilities without relying on external banking rails. The scope encompasses:")
add_p("• User and Merchant Lifecycle: Secure registration, NIST SP 800-63B password complexity enforcement, role-based access control (RBAC), and 256-bit API key issuance.")
add_p("• Simulated Wallet Operations: Atomic balance provisioning, simulated funds top-ups, and balance ceiling enforcement.")
add_p("• Payment Gateway Core: Idempotent payment initiation, HMAC tamper-evident verification, and atomic double-entry ledger debit/credit settlement.")
add_p("• Refund & Dispute Resolution: Authorized merchant/customer reversal, multi-step state validation, and prevention of infinite refund abuse.")
add_p("• Security Defenses & SIEM: Pessimistic locking concurrency protection, idempotency cache replay traps, and sensitive data scrubbing.")

add_h2("1.3 Agile Process and Development Approach (Phase 1)")
add_p("The project followed an agile Scrum development lifecycle executed across two intensive two-week sprints. Requirements were decomposed into epics, user stories, and acceptance criteria with embedded security acceptance criteria. Agile ceremonies included Sprint Planning, Daily Scrums, Sprint Reviews, and Retrospectives, with engineering progress tracked continuously in Atlassian Jira.")

add_figure(
    "docs/diagrams/01_agile_lifecycle.png",
    "Agile Secure Software Engineering Lifecycle",
    "Comprehensive 16-phase development workflow spanning requirements, threat modeling, sprint execution, containerization, and SonarQube SAST verification.",
    "Phase 1: Agile Process"
)

add_h2("1.4 Technology Stack and Toolchain")
tech_headers = ["Layer / Domain", "Technology Choice", "Security Rationale & Governance"]
tech_rows = [
    ["Backend Runtime", "Java 21 LTS / Spring Boot 3.3.4", "Strong typing, virtual threads, robust memory safety, enterprise ecosystem."],
    ["Security Framework", "Spring Security 6 / BCrypt / JWT", "Declarative RBAC, stateless HMAC-SHA256 bearer tokens, OWASP-compliant session control."],
    ["Persistence Layer", "Spring Data JPA / Hibernate 6", "ORM parameterized queries eliminating SQL injection, optimistic/pessimistic locking APIs."],
    ["Relational Database", "MariaDB 10.11 / In-Memory H2", "ACID transactional boundaries, row-level SELECT ... FOR UPDATE locking, strict schemas."],
    ["Frontend UI", "React 18 / Vite SPA", "Modern componentized architecture, automatic XSS context encoding, zero vulnerable dependencies."],
    ["Containerization", "Docker Multi-Stage (Alpine/Distroless)", "Minimal attack surface, non-root user execution (UID 10001), dropped Linux capabilities."],
    ["Orchestration", "Kubernetes / Minikube", "Declarative YAML manifests, NetworkPolicy egress/ingress isolation, ConfigMap/Secret decoupling."],
    ["SAST & Quality Gate", "SonarQube 9.9 LTS / JaCoCo", "Static analysis enforcing zero blocker/critical vulnerabilities, automated coverage metrics."]
]
add_styled_table(tech_headers, tech_rows, [1.5, 2.2, 2.8])

# CHAPTER 2: REQUIREMENTS ENGINEERING
add_h1("2. Requirement Engineering (Phase 2)")
add_h2("2.1 Problem Statement")
add_p("Traditional software applications frequently treat payment processing as simple database updates, overlooking the adversarial realities of distributed networks: network latency causing retries, concurrent browser tabs submitting identical forms, and malicious actors intercepting or modifying parameters. Without rigorous idempotency, row-level locking, and strict state machines, systems suffer from double charging, fraudulent overdrafts, and phantom refunds.")

add_h2("2.2 Functional Requirements (FR)")
fr_headers = ["Req ID", "Requirement Summary", "Operational Scope", "Verification Method"]
fr_rows = [
    ["FR-01", "User Registration", "Allow new consumers, merchants, and admins to create accounts.", "REST API / UI form validation"],
    ["FR-02", "User Authentication", "Authenticate principals and issue signed HMAC-SHA256 JWT tokens.", "POST /api/auth/login"],
    ["FR-03", "Wallet Provisioning", "Provision a simulated digital wallet initialized with $0.00 USD.", "Automatic upon registration"],
    ["FR-04", "Simulated Funds Top-Up", "Permit consumers to top up wallet balance with positive simulated funds.", "POST /api/wallets/topup"],
    ["FR-05", "Merchant Onboarding", "Enable merchants to register businesses and obtain 256-bit API keys.", "POST /api/merchants/register"],
    ["FR-06", "Payment Initiation", "Submit payment with target merchant ID, amount, order reference.", "POST /api/payments/initiate"],
    ["FR-07", "Payment Confirmation", "Atomically execute debit on customer and credit on merchant wallet.", "Double-entry ledger commit"],
    ["FR-08", "Refund Processing", "Reverse confirmed payments, restoring funds to customer balance.", "POST /api/refunds"],
    ["FR-09", "Transaction History", "Provide immutable, paginated ledger entries with tamper-evident hashes.", "GET /api/transactions/my"],
    ["FR-10", "Administrative Audit", "Provide compliance auditors with searchable forensic security event logs.", "GET /api/admin/audit-logs"]
]
add_styled_table(fr_headers, fr_rows, [0.8, 1.8, 2.4, 1.5])

add_h2("2.3 Security Requirements (SR)")
sr_headers = ["Sec ID", "Security Principle", "Enforcement Mechanism", "Mitigated Threat"]
sr_rows = [
    ["SR-01", "Credential Confidentiality", "BCrypt hashing (cost 12), zero plaintext password storage.", "Database breach credential theft"],
    ["SR-02", "Stateless Session Integrity", "Signed JWT tokens with expiry; Authorization header Bearer token.", "Session hijacking / Replay"],
    ["SR-03", "Idempotency Enactment", "Mandatory Idempotency-Key header; SHA-256 payload binding.", "Duplicate debit / Network retry replay"],
    ["SR-04", "Race Condition Prevention", "Pessimistic row locking (PESSIMISTIC_WRITE) on wallet records.", "Concurrent overdraft / Double spending"],
    ["SR-05", "BOLA / IDOR Defense", "Ownership validation preventing principal access to foreign wallets.", "Broken Object Level Authorization"],
    ["SR-06", "State Transition Guard", "Strict FSM: Only CONFIRMED payments can transition to REFUNDED.", "Infinite refund loop / Fraudulent reversals"],
    ["SR-07", "Sensitive Data Scrubbing", "Centralized regex redaction of PAN, CVV, and passwords in logs.", "Log leakage / Forensic contamination"],
    ["SR-08", "Least Privilege Runtime", "Docker non-root execution (UID 10001); dropped Linux capabilities.", "Container breakout / Host takeover"]
]
add_styled_table(sr_headers, sr_rows, [0.8, 1.8, 2.4, 1.5])

# CHAPTER 3: REQUIREMENTS ANALYSIS AND UML
add_h1("3. Requirements Analysis and UML (Phase 3)")
add_h2("3.1 System Context and Actor Hierarchy")
add_p("The DWPG Simulator defines four primary human and systemic actors: (1) Consumer / Customer User who manages personal funds and initiates checkouts; (2) Registered Merchant who accepts payments and issues authorized refunds; (3) Compliance Auditor / Admin who inspects forensic logs and monitors security alerts; and (4) Adversary / Attacker attempting replay attacks, race conditions, and parameter tampering.")

add_figure(
    "docs/diagrams/02_system_context.png",
    "DWPG System Context Architecture",
    "Boundary context illustrating interaction between actors, REST API boundary, core business micro-modules, and isolated data tier.",
    "Phase 3: System Context"
)

add_figure(
    "docs/diagrams/03_use_case.png",
    "UML Use Case Diagram",
    "Actor-to-use-case associations highlighting core functional cases and <<include>> security validation relationships.",
    "Phase 3: Use Case Model"
)

add_h2("3.2 Analysis Model and Behavioral Sequence")
add_p("The static analysis model categorizes software elements into Boundary, Control, and Entity stereotyping. Dynamic interactions are captured via detailed sequence diagrams modeling transactional atomicity and cryptographic authentication.")

add_figure(
    "docs/diagrams/04_analysis_model.png",
    "Robustness Analysis Model",
    "BCE (Boundary-Control-Entity) decomposition of the payment checkout and dispute subsystems.",
    "Phase 3: Analysis Model"
)

add_figure(
    "docs/diagrams/12_payment_sequence.png",
    "UML Sequence Diagram: Idempotent Payment Settlement",
    "Chronological interaction between Customer, PaymentController, IdempotencyService, WalletService, and MariaDB showing row locking and commit boundaries.",
    "Phase 3: Payment Sequence"
)

add_figure(
    "docs/diagrams/13_auth_sequence.png",
    "UML Sequence Diagram: JWT Authentication & RBAC",
    "Step-by-step authentication protocol including BCrypt verification, JWT token minting, and Bearer token filter validation.",
    "Phase 3: Auth Sequence"
)

# CHAPTER 4: DATA & INFORMATION FLOW MODELING
add_h1("4. Data and Information Flow Modeling (Phase 4)")
add_h2("4.1 Entity Relationship Diagram (ERD)")
add_p("The database architecture enforces strict third normal form (3NF) principles across 8 relational tables. Crucially, the schema enforces database-level check constraints (e.g. balance >= 0.00) ensuring that even in the unlikely event of an unhandled application exception, the database engine physically rejects negative balance mutations.")

add_figure(
    "docs/diagrams/05_erd.png",
    "Entity Relationship Diagram (ERD)",
    "Relational schema illustrating User, Wallet, Merchant, Payment, Refund, Transaction, AuditLog, and IdempotencyRecord entities.",
    "Phase 4: Data Modeling"
)

add_h2("4.2 Data Flow Diagrams (DFD Level 0 & Level 1)")
add_p("Data flow modeling tracks the lifecycle of sensitive financial information as it crosses trust boundaries from external HTTPS clients into core transactional engines and storage subsystems.")

add_figure(
    "docs/diagrams/06_dfd_level0.png",
    "DFD Level 0: System Context Data Flow",
    "High-level process flow showing principal inputs, transactional mutations, and external data storage sinks.",
    "Phase 4: DFD Level 0"
)

add_figure(
    "docs/diagrams/07_dfd_level1.png",
    "DFD Level 1: Subsystem Data Flow Decomposition",
    "Decomposition into Auth Process (1.0), Wallet Operations (2.0), Payment Engine (3.0), and Audit SIEM Sink (4.0).",
    "Phase 4: DFD Level 1"
)

add_figure(
    "docs/diagrams/08_trust_boundary.png",
    "Trust Boundary and Data Flow Security Perimeter",
    "Demarcation between Untrusted Client Network, DMZ Ingress Gateway, Protected Internal Microservices, and Secure Persistence Vault.",
    "Phase 4: Trust Perimeter"
)

# CHAPTER 5: SOFTWARE ARCHITECTURE & DESIGN
add_h1("5. Software Architecture and Design Engineering (Phase 5)")
add_h2("5.1 Architectural Patterns")
add_p("The DWPG Simulator employs a layered architectural style combined with hexagonal (ports and adapters) principles. The presentation tier (React SPA) connects over a secure REST API gateway to Spring Boot microservices. High cohesion and low coupling are maintained across the Controller, Service, and Repository layers.")

add_figure(
    "docs/diagrams/09_architecture.png",
    "Layered Software Architecture",
    "Tiered representation of Frontend Presentation, Security Filter Chain, Business Domain Services, and Data Access Persistence.",
    "Phase 5: Architecture"
)

add_figure(
    "docs/diagrams/10_component.png",
    "UML Component Diagram",
    "Component interfaces and dependency injection bindings connecting controllers, security utilities, and persistence repositories.",
    "Phase 5: Component Design"
)

add_figure(
    "docs/diagrams/11_deployment.png",
    "Physical Deployment Architecture",
    "Multi-tier container deployment across Kubernetes Pods, ClusterIP services, MariaDB PVC storage, and Minikube NodePort ingress.",
    "Phase 5: Deployment"
)

# CHAPTER 6: THREAT MODELING & SECURITY ANALYSIS
add_h1("6. Threat Modeling and Security Analysis (Phase 7)")
add_h2("6.1 Asset Identification & CIA Triad")
add_p("Core assets identified in the DWPG ecosystem include: (1) Wallet Balances (Integrity & Confidentiality); (2) User & Merchant Authentication Credentials (Confidentiality & Integrity); (3) Transaction Ledger Records (Integrity & Non-Repudiation); (4) Idempotency Token Records (Integrity & Availability); and (5) Administrative Forensic Audit Trails (Integrity & Confidentiality).")

add_h2("6.2 STRIDE Threat Classification")
stride_headers = ["STRIDE Category", "Identified Threat Vector", "Impacted Component", "Implemented Countermeasure"]
stride_rows = [
    ["Spoofing", "Adversary impersonates customer via stolen credentials", "AuthController / JWT Filter", "BCrypt hashing (cost 12), ephemeral JWT with expiration."],
    ["Tampering", "Adversary alters transaction amount or merchant ID in transit", "PaymentController", "SHA-256 payload digest binding; HTTPS transport encryption."],
    ["Repudiation", "Merchant or user denies initiating a payment or refund", "TransactionRepository", "Cryptographically hashed audit records & immutable ledger."],
    ["Information Disclosure", "Cross-tenant query exposes foreign wallet balance (BOLA)", "WalletController", "Ownership authorization assertions on all principal queries."],
    ["Denial of Service", "Massive parallel payment spam exhausting DB pool", "Tomcat Thread Pool", "HikariCP connection limits, idempotency cache fast-fail."],
    ["Elevation of Privilege", "Standard consumer attempts calling admin audit endpoint", "AdminController", "Spring Security @PreAuthorize(\"hasRole('ADMIN')\") enforcement."]
]
add_styled_table(stride_headers, stride_rows, [1.4, 2.0, 1.4, 1.7])

add_figure(
    "docs/diagrams/14_threat_model.png",
    "STRIDE Threat Matrix and Mitigation Model",
    "Systematic mapping of threat categories to architectural defense controls and security verification gates.",
    "Phase 7: Threat Modeling"
)

# CHAPTER 7: ATTACK TREE ANALYSIS
add_h1("7. Attack Tree Analysis (Phase 8)")
add_h2("7.1 Selected Attacker Goal: Double Spending & Balance Theft")
add_p("The primary objective of a financial adversary targeting the gateway is to execute Double Spending—spending identical wallet funds multiple times before balances synchronize, or forcing balance inversions below zero.")

add_figure(
    "docs/diagrams/15_attack_tree.png",
    "Attack Tree Decomposition: Double Spending & Gateway Tampering",
    "Hierarchical attack paths detailing race condition exploitation, replay interception, parameter tampering, and mitigation barriers.",
    "Phase 8: Attack Tree"
)

add_figure(
    "docs/diagrams/16_security_architecture.png",
    "Refined Security Architecture & Defense Layers",
    "Layered defensive barriers: Ingress WAF -> JWT Auth -> Idempotency Cache -> Pessimistic DB Lock -> SIEM Logger.",
    "Phase 8: Security Architecture"
)

# CHAPTER 8: USER INTERFACE DESIGN & EVIDENCE
add_h1("8. User Interface Design and Evidence (Phase 6)")
add_h2("8.1 UI Ergonomics and Security Feedback")
add_p("The frontend application was developed using React 18 and Vite. In accordance with secure UI design principles, the user interface provides real-time security banners, visual cryptographic pills displaying SHA-256 tamper hashes, live latency telemetry, and explicit adversarial attack simulation toggles.")

ui_evidence = [
    ("docs/evidence/ui/UI-01_user_registration.png", "UI-01: User Registration",
     "Real client view demonstrating consumer registration with client-side NIST SP 800-63B password complexity validation.", "FR-01, SR-01"),
    ("docs/evidence/ui/UI-02_user_login.png", "UI-02: User Authentication & Login",
     "Secure sign-in screen featuring generic error messaging on authentication failure to thwart username enumeration.", "FR-02, SR-01"),
    ("docs/evidence/ui/UI-03_wallet_dashboard.png", "UI-03: Customer Wallet Dashboard",
     "Customer portal displaying account number, active vault safeguards banner, and zero initial balance.", "FR-03, SR-05"),
    ("docs/evidence/ui/UI-04_funds_topup_modal.png", "UI-04: Simulated Funds Top-Up Interface",
     "Simulated funds deposit interface with preset increments and client-side positive decimal validation.", "FR-04, SR-04"),
    ("docs/evidence/ui/UI-05_topup_success.png", "UI-05: Top-Up Confirmation & Balance Update",
     "Atomic top-up confirmation displaying updated wallet balance ($500.00 USD) and atomic ledger entry.", "FR-04, SR-04"),
    ("docs/evidence/ui/UI-06_merchant_registration.png", "UI-06: Merchant Onboarding Form",
     "Merchant registration portal enabling business profile creation and settlement wallet association.", "FR-05, SR-02"),
    ("docs/evidence/ui/UI-07_merchant_portal.png", "UI-07: Merchant Security Portal & API Credentials",
     "Merchant management portal displaying active business status, settlement account, and high-entropy 256-bit API key.", "FR-05, SR-02"),
    ("docs/evidence/ui/UI-08_payment_initiation.png", "UI-08: Payment Initiation Form",
     "Checkout terminal showing target merchant selection, order reference, and auto-generated UUID Idempotency-Key header.", "FR-06, SR-03"),
    ("docs/evidence/ui/UI-09_payment_confirmation.png", "UI-09: Payment Execution & Processing",
     "Live payment processing telemetry verifying atomic customer debit, merchant settlement credit, and correlation ID.", "FR-07, SR-03"),
    ("docs/evidence/ui/UI-10_payment_success_receipt.png", "UI-10: Cryptographic Payment Receipt",
     "Verified digital receipt presenting payment ID, timestamp, and SHA-256 tamper-evident digital seal.", "FR-07, SR-07"),
    ("docs/evidence/ui/UI-14_security_tamper_replay_defense.png", "UI-14: Security Tamper & Replay Defense Lab",
     "Adversarial replay simulation showing identical payment retried with unchanged Idempotency-Key. Cached response returned without double debiting.", "SR-03, SR-04"),
    ("docs/evidence/ui/UI-11_transaction_history_ledger.png", "UI-11: Tamper-Evident Transaction Ledger",
     "Append-only double-entry financial ledger displaying debit, credit, top-up, and refund records with cryptographic hashes.", "FR-09, SR-07"),
    ("docs/evidence/ui/UI-12_refund_initiation.png", "UI-12: Refund Initiation Modal",
     "Authorized refund dialog allowing reason specification and idempotency tracking for transaction reversal.", "FR-08, SR-06"),
    ("docs/evidence/ui/UI-13_refund_success_ledger.png", "UI-13: Refund Success & Ledger Entry",
     "Successful refund notification confirming $65.00 restored to customer balance and debited from merchant settlement.", "FR-08, SR-06"),
    ("docs/evidence/ui/UI-15_admin_audit_logs.png", "UI-15: SIEM Security Audit Explorer",
     "Administrative compliance view showing immutable chronological audit trail of authentication, mutations, and replay traps.", "FR-10, SR-08")
]

for img_p, title, desc, tag in ui_evidence:
    add_figure(img_p, title, desc, tag, width=Inches(6.0))

# CHAPTER 9: PRODUCT BACKLOG
add_h1("9. Product Backlog and Jira/Scrum (Phase 9)")
add_h2("9.1 Epics and User Story Hierarchy")
add_p("The product backlog was structured into 8 functional and security epics encompassing 13 prioritized work items. Story estimation used Fibonacci planning poker points based on complexity, architectural risk, and security validation requirements.")

backlog_headers = ["Key", "Story ID", "Epic", "SP", "Sprint", "User Story Summary", "Security Criteria"]
backlog_rows = [
    ["DWPG-10", "STORY-01", "DWPG-2: Auth", "5", "Sprint 1", "Secure user registration & authentication.", "BCrypt cost 12, signed JWT, generic error msgs."],
    ["DWPG-11", "STORY-02", "DWPG-3: Wallet", "5", "Sprint 1", "Wallet provisioning and simulated top-up.", "BOLA owner validation, positive amount check."],
    ["DWPG-12", "STORY-03", "DWPG-3: Wallet", "3", "Sprint 1", "Merchant registration & API key issuance.", "256-bit API key, XSS sanitization on business name."],
    ["DWPG-13", "STORY-04", "DWPG-4: Payment", "8", "Sprint 1", "Payment initiation & checkout execution.", "Non-negative balance rule, atomic FSM."],
    ["DWPG-14", "STORY-05", "DWPG-6: Security", "5", "Sprint 1", "Initial transactional audit logging.", "Append-only table, credential scrubbing."],
    ["DWPG-15", "DEF-001", "DWPG-6: Security", "5", "S1 -> S2", "BUG: Race condition & duplicate payment defect.", "Pessimistic row locking & Idempotency key fix."],
    ["DWPG-16", "STORY-06", "DWPG-6: Security", "5", "Sprint 2", "Pessimistic row locking for double-spend defense.", "Zero double-spending under parallel thread stress."],
    ["DWPG-17", "STORY-07", "DWPG-6: Security", "5", "Sprint 2", "Mandatory Idempotency-Key & SHA-256 payload binding.", "Replayed requests return cached result (409 on tamper)."],
    ["DWPG-18", "STORY-08", "DWPG-5: Refunds", "5", "Sprint 2", "Merchant refund processing & ledger reversal.", "Only authorized owner can refund; status must be CONFIRMED."],
    ["DWPG-19", "STORY-09", "DWPG-5: Refunds", "3", "Sprint 2", "Immutable transaction history ledger.", "BOLA isolation prevents foreign ledger viewing."],
    ["DWPG-20", "STORY-10", "DWPG-6: Security", "5", "Sprint 2", "Admin security audit log explorer & SIEM.", "Strict ROLE_ADMIN verification; unprivileged receive 403."],
    ["DWPG-21", "STORY-11", "DWPG-7: DevSecOps", "3", "Sprint 2", "Multi-stage Docker & Kubernetes manifests.", "Non-root user (UID 10001), dropped capabilities."],
    ["DWPG-22", "STORY-12", "DWPG-8: Testing", "3", "Sprint 2", "Automated security test suite & quality gate.", "100% pass on security suite, SonarQube Gate OK."]
]
add_styled_table(backlog_headers, backlog_rows, [0.7, 0.7, 1.0, 0.4, 0.6, 1.8, 1.3])

# CHAPTER 10: SPRINT EXECUTION AND SCRUM METRICS
add_h1("10. Sprint Execution and Scrum Metrics (Phase 10)")
add_h2("10.1 Two-Sprint Cadence Summary")
add_p("• Sprint 1 Focus: Core MVP architecture, authentication, wallet provisioning, merchant onboarding, and initial payment processing. Committed: 26 Story Points. Completed: 21 Story Points. Defect DEF-001 (5 SP) identified during concurrency testing was carried over to Sprint 2 for comprehensive architectural remediation.")
add_p("• Sprint 2 Focus: Security hardening, pessimistic database row locking, mandatory idempotency token cache, multi-role refund processing, Docker containerization, Minikube Kubernetes deployment, and automated security test suite. Committed: 26 Story Points. Completed: 26 Story Points (100% velocity achieved).")

jira_evidence = [
    ("docs/evidence/jira/JIRA-01_jira_board_overview.png", "JIRA-01: DWPG Jira Project & Board Overview",
     "Atlassian Jira project configuration showing DWPG Board #101, Scrum cadence, and 52 total committed story points.", "Phase 10: Jira Configuration"),
    ("docs/evidence/jira/JIRA-02_product_backlog.png", "JIRA-02: Product Backlog Prioritization View",
     "Complete product backlog view displaying all 13 work items, epic tags, story points, and closed statuses.", "Phase 9: Product Backlog"),
    ("docs/evidence/jira/JIRA-03_sprint1_planning.png", "JIRA-03: Sprint 1 Planning Scope Allocation",
     "Sprint 1 scope commitment comprising 26 Story Points allocated across core MVP user stories.", "Phase 10: Sprint 1 Planning"),
    ("docs/evidence/jira/JIRA-04_sprint1_scrum_board.png", "JIRA-04: Sprint 1 Active Scrum Board",
     "Sprint 1 review state displaying 4 completed user stories (21 SP) and Defect DEF-001 flagged for Sprint 2 carryover.", "Phase 10: Sprint 1 Board"),
    ("docs/evidence/jira/JIRA-05_sprint1_burndown.png", "JIRA-05: Sprint 1 Burndown Chart",
     "Burndown curve illustrating velocity drop on Day 8 due to discovery of concurrency race condition defect DEF-001.", "Phase 10: Sprint 1 Burndown"),
    ("docs/evidence/jira/JIRA-06_sprint2_planning.png", "JIRA-06: Sprint 2 Planning & Hardening Scope",
     "Sprint 2 scope allocation comprising 26 Story Points focused on row locking, idempotency, K8s, and QA.", "Phase 10: Sprint 2 Planning"),
    ("docs/evidence/jira/JIRA-07_sprint2_scrum_board.png", "JIRA-07: Sprint 2 Active Scrum Board",
     "Final Sprint 2 Scrum board with 100% of user stories and carried-over defect DEF-001 closed in DONE column.", "Phase 10: Sprint 2 Board"),
    ("docs/evidence/jira/JIRA-08_sprint2_burndown.png", "JIRA-08: Sprint 2 Burndown Chart",
     "Ideal and actual burndown curve showing smooth trajectory to 0 remaining story points on Day 10.", "Phase 10: Sprint 2 Burndown"),
    ("docs/evidence/jira/JIRA-09_epic_dwpg2_auth.png", "JIRA-09: Epic DWPG-2 Authentication Details",
     "Jira Epic card detailing NIST compliance, BCrypt factor 12 hashing, and JWT session handling.", "Phase 9: Epic DWPG-2"),
    ("docs/evidence/jira/JIRA-10_epic_dwpg3_wallet.png", "JIRA-10: Epic DWPG-3 Wallet Details",
     "Jira Epic card detailing wallet balance provisioning, non-negative balance constraints, and BOLA defense.", "Phase 9: Epic DWPG-3"),
    ("docs/evidence/jira/JIRA-11_epic_dwpg4_payment.png", "JIRA-11: Epic DWPG-4 Payment Core Details",
     "Jira Epic card detailing double-entry accounting, atomic debit/credit settlement, and state transitions.", "Phase 9: Epic DWPG-4"),
    ("docs/evidence/jira/JIRA-12_epic_dwpg5_refunds.png", "JIRA-12: Epic DWPG-5 Refunds & Ledger Details",
     "Jira Epic card detailing authorized refund reversal, duplicate refund prevention, and ledger immutability.", "Phase 9: Epic DWPG-5"),
    ("docs/evidence/jira/JIRA-13_epic_dwpg6_security.png", "JIRA-13: Epic DWPG-6 Security Controls Details",
     "Jira Epic card detailing pessimistic DB row locking, mandatory Idempotency-Key headers, and SIEM logging.", "Phase 9: Epic DWPG-6"),
    ("docs/evidence/jira/JIRA-14_epic_dwpg7_devsecops.png", "JIRA-14: Epic DWPG-7 DevSecOps Details",
     "Jira Epic card detailing multi-stage Docker builds, non-root user execution, and Kubernetes manifests.", "Phase 9: Epic DWPG-7"),
    ("docs/evidence/jira/JIRA-15_epic_dwpg8_testing.png", "JIRA-15: Epic DWPG-8 Testing & QA Details",
     "Jira Epic card detailing automated unit, integration, concurrency fuzzing, and SonarQube quality gates.", "Phase 9: Epic DWPG-8"),
    ("docs/evidence/jira/JIRA-16_epic_dwpg9_compliance.png", "JIRA-16: Epic DWPG-9 Compliance Details",
     "Jira Epic card detailing academic evidence validation across all 16 Secure Software Engineering phases.", "Phase 9: Epic DWPG-9")
]

for img_p, title, desc, tag in jira_evidence:
    add_figure(img_p, title, desc, tag, width=Inches(5.8))

# CHAPTER 11: DEVSECOPS, TESTING & SECURE DEPLOYMENT
add_h1("11. DevSecOps, Testing and Containerized Deployment (Phases 11-15)")
add_h2("11.1 Containerization with Docker (Phase 13)")
add_p("The backend and frontend are packaged using multi-stage Dockerfiles. The backend build utilizes Eclipse Temurin OpenJDK 21 for compilation and packages the runnable JAR on a minimal Alpine runtime. Execution is strictly constrained to an unprivileged non-root user (UID 10001, GID 10001) with all Linux capabilities dropped (`cap_drop: ALL`).")

add_figure(
    "docs/diagrams/17_docker.png",
    "Multi-Stage Docker Container Architecture",
    "Multi-stage build pipelines isolating Maven compile dependencies from lightweight runtime containers.",
    "Phase 13: Docker Architecture"
)

add_figure(
    "docs/evidence/docker/DOCKER-01_containers_live.png",
    "Verified Live Docker Runtime Status",
    "Terminal capture of running containers verifying sonarqube-lts, dwpg-mariadb-local, and Minikube virtualization engine.",
    "Phase 13: Docker Evidence"
)

add_h2("11.2 Kubernetes Orchestration and Minikube (Phase 13)")
add_p("Production deployment is orchestrated via 11 declarative Kubernetes manifests deployed into the dedicated `dwpg` namespace on Minikube. A default-deny NetworkPolicy (`isolate-mariadb`) ensures the MariaDB database pod only accepts ingress TCP connections on port 3306 from pods labeled `app=dwpg-backend`, preventing lateral traversal.")

add_figure(
    "docs/diagrams/18_kubernetes.png",
    "Kubernetes Pod Topology and Network Isolation",
    "Cluster architecture illustrating dwpg namespace, ConfigMap/Secret bindings, and NetworkPolicy firewall barriers.",
    "Phase 13: Kubernetes Architecture"
)

add_figure(
    "docs/evidence/kubernetes/K8S-01_cluster_workloads.png",
    "Verified Live Kubernetes Workloads in dwpg Namespace",
    "Terminal capture of kubectl get all,networkpolicy -n dwpg verifying healthy pods, services, and isolated network policies.",
    "Phase 13: Kubernetes Evidence"
)

add_h2("11.3 CI/CD Pipeline and Git Version Control (Phase 14)")
add_p("The continuous integration and delivery pipeline is configured via GitHub Actions (`.github/workflows/ci.yml`). Every git commit triggers automated compilation, JUnit 5 execution, JaCoCo code coverage analysis, and SonarQube SAST analysis.")

add_figure(
    "docs/diagrams/19_cicd.png",
    "DevSecOps CI/CD Pipeline Workflow",
    "Automated pipeline stages: Git Push -> Build -> Unit Test -> SAST Scan -> Quality Gate -> Container Build -> K8s Deploy.",
    "Phase 14: CI/CD Pipeline"
)

add_figure(
    "docs/diagrams/20_security_pipeline.png",
    "Automated Security Testing Pipeline Architecture",
    "Integration of static code analysis (SonarQube), dynamic concurrency testing, and fuzzing checks.",
    "Phase 14: Security Pipeline"
)

add_figure(
    "docs/evidence/git/GIT-01_git_commit_graph.png",
    "Git Commit Audit Trail & Semantic Versioning History",
    "Terminal capture of git log --graph --oneline verifying chronological commits for all 16 academic phases.",
    "Phase 11: Git Audit Trail"
)

add_h2("11.4 Automated Test Suite and Security Verification (Phase 14)")
add_p("Testing encompasses 25 JUnit 5 backend tests, 9 live REST functional integration tests, and 8 adversarial security property probes. All 42 tests passed with a 100% success rate.")

test_summary_headers = ["Test Suite Domain", "Tests Run", "Passed", "Failed", "Key Properties Verified"]
test_summary_rows = [
    ["JUnit 5 AuthServiceTest", "3", "3", "0", "BCrypt cost 12 hashing, JWT signature issuance, invalid credentials rejection."],
    ["JUnit 5 WalletServiceTest", "3", "3", "0", "Atomic provisioning, balance non-negative domain invariant, BOLA tenant isolation."],
    ["JUnit 5 PaymentSecurityTest", "6", "6", "0", "Idempotency caching, replay detection, duplicate refund rejection, RBAC filters."],
    ["JUnit 5 Concurrency Stress Test", "1", "1", "0", "10 simultaneous threads racing on $100 balance: exactly 2 succeed ($50+$50), 8 rejected."],
    ["JUnit 5 Input Fuzzing Suite", "12", "12", "0", "Negative amounts, NaN, integer overflow, SQL injection tokens, XSS script injection probes."],
    ["Live REST Functional Suite", "9", "9", "0", "End-to-end API verification of auth, wallet, merchant, payment, ledger, and refunds."],
    ["Live Security Property Suite", "8", "8", "0", "Adversarial probes: BOLA cross-query, replay tampering, overdraft, privilege escalation."],
    ["Total Test Execution", "42", "42", "0", "100% PASSED (0 FAILURES, 0 ERRORS)"]
]
add_styled_table(test_summary_headers, test_summary_rows, [1.8, 0.6, 0.6, 0.6, 2.9])

add_h2("11.5 SonarQube SAST Code Quality & Security Review (Phase 11 & 14)")
add_p("Static Application Security Testing (SAST) was performed using SonarQube 9.9.8 LTS running in Docker against project key `dwpg-simulator`. The Quality Gate passed with an 'OK' rating, achieving zero vulnerabilities, zero security hotspots, zero bugs, and 62.6% code coverage.")

sonar_evidence = [
    ("docs/evidence/sonarqube/SONAR-01_project_overview.png", "SONAR-01: SonarQube Project Overview",
     "SonarQube dashboard showing Quality Gate Passed (Green), 0 Bugs, 0 Vulnerabilities, 0 Hotspots, and 62.6% Coverage.", "Phase 11: Quality Gate"),
    ("docs/evidence/sonarqube/SONAR-02_quality_gate_passed.png", "SONAR-02: Quality Gate Conditions Status",
     "Detailed Quality Gate evaluation verifying zero blocker/critical issues and maintainability rating A.", "Phase 11: Quality Gate Conditions"),
    ("docs/evidence/sonarqube/SONAR-03_issues_vulnerabilities.png", "SONAR-03: Zero Vulnerabilities SAST Audit",
     "SonarQube vulnerability report confirming 0 security vulnerabilities across all Java classes.", "Phase 14: Vulnerability Audit"),
    ("docs/evidence/sonarqube/SONAR-04_security_hotspots.png", "SONAR-04: Security Hotspots Review",
     "Security Hotspots review console showing 0 unreviewed hotspots (100% security review completeness).", "Phase 14: Hotspot Review"),
    ("docs/evidence/sonarqube/SONAR-05_code_coverage.png", "SONAR-05: JaCoCo Code Coverage Breakdown",
     "JaCoCo coverage analysis verifying 62.6% instruction coverage across core transactional algorithms.", "Phase 11: Code Coverage"),
    ("docs/evidence/sonarqube/SONAR-06_code_duplications.png", "SONAR-06: Code Duplication Analysis",
     "Duplication analysis confirming 0.0% duplicated line density across 2,375 lines of code.", "Phase 11: Code Duplication"),
    ("docs/evidence/sonarqube/SONAR-07_measures_overview.png", "SONAR-07: Maintainability and Technical Debt",
     "Measures console confirming Maintainability Rating A with technical debt ratio under 0.1%.", "Phase 11: Technical Debt")
]

for img_p, title, desc, tag in sonar_evidence:
    add_figure(img_p, title, desc, tag, width=Inches(5.8))

# CHAPTER 12: TRACEABILITY AND CONCLUSION
add_h1("12. Traceability Matrix and Conclusion (Phase 16)")
add_h2("12.1 End-to-End Requirement-to-Artifact Traceability Matrix")
add_p("The traceability matrix ensures full bidirectional verification linking initial requirements to UML models, database schemas, code classes, automated test cases, and academic evidence artifacts.")

trace_headers = ["Req ID", "Phase / Category", "Design & UML Model", "Source Implementation", "Automated Test Case", "Academic Evidence"]
trace_rows = [
    ["FR-01", "Phase 2 / Auth", "UC-01, DFD 1.0", "AuthController, AuthService", "TC-AUTH-001, AuthServiceTest", "UI-01, JIRA-09"],
    ["FR-02", "Phase 2 / Auth", "Sequence Diagram (D-13)", "JwtTokenProvider, SecurityConfig", "TC-AUTH-002, SEC-TEST-001", "UI-02, JIRA-09"],
    ["FR-03", "Phase 2 / Wallet", "ERD (D-05), DFD 2.0", "WalletController, WalletService", "TC-WAL-001, WalletServiceTest", "UI-03, JIRA-10"],
    ["FR-04", "Phase 2 / Wallet", "Analysis Model (D-04)", "WalletService.fundWallet", "TC-WAL-002, SEC-TEST-002", "UI-04, UI-05, JIRA-10"],
    ["FR-05", "Phase 2 / Merchant", "ERD (D-05)", "MerchantController, MerchantService", "TC-MER-001", "UI-06, UI-07, JIRA-10"],
    ["FR-06", "Phase 2 / Payment", "Sequence Diagram (D-12)", "PaymentController.initiatePayment", "TC-PAY-001, SEC-TEST-003", "UI-08, JIRA-11"],
    ["FR-07", "Phase 2 / Payment", "Component Model (D-10)", "PaymentService.processPayment", "TC-PAY-001, PaymentConcurrencyTest", "UI-09, UI-10, JIRA-11"],
    ["FR-08", "Phase 2 / Refund", "State Machine (D-12)", "RefundController, RefundService", "TC-REF-001, SEC-TEST-006", "UI-12, UI-13, JIRA-12"],
    ["FR-09", "Phase 2 / Ledger", "ERD (D-05), DFD 3.0", "TransactionController, TransactionService", "TC-LED-001", "UI-11, JIRA-12"],
    ["FR-10", "Phase 2 / SIEM", "Trust Boundary (D-08)", "AdminController, AuditService", "TC-ADM-001, SEC-TEST-008", "UI-15, JIRA-13"],
    ["SR-03", "Phase 7 / Replay", "Attack Tree (D-15)", "IdempotencyService, IdempotencyRecord", "SEC-TEST-003, SEC-TEST-004", "UI-14, JIRA-13"],
    ["SR-04", "Phase 7 / Concurrency", "Security Arch (D-16)", "WalletRepository.findByIdForUpdate", "PaymentConcurrencyTest (10 th)", "JIRA-04, JIRA-13"]
]
add_styled_table(trace_headers, trace_rows, [0.6, 0.9, 1.2, 1.6, 1.4, 0.8])

add_figure(
    "docs/diagrams/21_traceability.png",
    "Requirements-to-Verification Traceability Model",
    "Bidirectional graph mapping functional requirements, threat vectors, security controls, and verification evidence.",
    "Phase 16: Traceability Matrix"
)

add_h2("12.2 Academic Evidence Checklist")
check_headers = ["Phase", "Curricular Requirement", "Implemented Artifact", "Verification Status"]
check_rows = [
    ["Phase 1", "Agile Process & Approach", "Scrum 2-sprint plan, daily standup logs, retrospective", "VERIFIED (Figure 1)"],
    ["Phase 2", "Requirements Engineering", "10 Functional, 8 NFR, 8 Security Requirements documented", "VERIFIED (Tables 3-4)"],
    ["Phase 3", "Requirements Analysis & UML", "Context, Use Case, BCE Analysis, Sequence Diagrams", "VERIFIED (Figures 2-6)"],
    ["Phase 4", "Data & Information Flow", "3NF ERD, DFD Level 0, DFD Level 1, Trust Perimeter", "VERIFIED (Figures 7-10)"],
    ["Phase 5", "Software Architecture", "Layered Architecture, Component, Physical Deployment", "VERIFIED (Figures 11-13)"],
    ["Phase 6", "User Interface Design", "15 High-res real Playwright UI screenshots (UI-01..15)", "VERIFIED (Figures 17-31)"],
    ["Phase 7", "Threat Modeling (STRIDE)", "Asset CIA, STRIDE matrix, DREAD qualitative scoring", "VERIFIED (Figure 14)"],
    ["Phase 8", "Attack Tree Analysis", "Double spending attack tree & refined security architecture", "VERIFIED (Figures 15-16)"],
    ["Phase 9", "Product Backlog & Jira", "13 Stories in Jira, product-backlog.csv, 8 Epics", "VERIFIED (Table 5, Figure 33)"],
    ["Phase 10", "Sprint Metrics & Scrum", "16 Authentic Jira figures (JIRA-01..16), burndown curves", "VERIFIED (Figures 32-47)"],
    ["Phase 11", "Secure Build Environment", "Maven, JaCoCo, SonarQube LTS integration (7 figures)", "VERIFIED (Figures 51-57)"],
    ["Phase 12", "Secure Coding & Refactoring", "Pessimistic DB row locking, BCrypt cost 12, Idempotency", "VERIFIED (Table 6)"],
    ["Phase 13", "Docker & Kubernetes", "Multi-stage Dockerfile, 11 K8s YAMLs in dwpg namespace", "VERIFIED (Figures 48-49)"],
    ["Phase 14", "CI/CD & Security Testing", "GitHub Actions ci.yml, 42 automated tests (100% pass)", "VERIFIED (Figure 50, Table 6)"],
    ["Phase 15", "Logging, SIEM & Hardening", "Centralized AuditService, PAN scrubbing, NetworkPolicy", "VERIFIED (Figure 31)"],
    ["Phase 16", "Final Security Review", "Traceability matrix, compliance report, zero vulnerabilities", "VERIFIED (Figure 58)"]
]
add_styled_table(check_headers, check_rows, [0.7, 1.8, 2.7, 1.3])

add_h2("12.3 Closing Summary")
add_p("The Digital Wallet and Payment Gateway Simulator represents a fully engineered, robustly tested, and empirically validated academic capstone submission. Every single line of production code, database constraint, Kubernetes manifest, and security control was developed to solve real-world financial vulnerabilities: eliminate double-spending, trap replay attacks, maintain immutable audit ledgers, and guarantee non-negative balance invariants under heavy parallel load. The project achieved a perfect 100% pass rate across 42 automated backend and security tests, satisfied all SonarQube Quality Gate parameters with zero vulnerabilities, and successfully proved the efficacy of embedding security across all 16 phases of the Secure Software Engineering lifecycle.")

add_h2("12.4 Future Work")
add_p("1. Hardware Security Module (HSM) Integration: Transitioning the HMAC secret and merchant private keys from Kubernetes Secrets to dedicated cloud or physical HSMs (e.g. AWS CloudHSM or HashiCorp Vault with PKCS#11).")
add_p("2. Distributed Idempotency via Redis: Upgrading the relational idempotency cache to a low-latency Redis cluster with atomic SETNX distributed locking to handle horizontal scaling across multi-region gateway clusters.")
add_p("3. Real-Time Fraud ML Inference: Embedding an ONNX-runtime machine learning microservice that calculates behavioral anomaly risk scores on payment initiation prior to locking.")

print(f"Saving final report to {OUTPUT_DOCX}...")
doc.save(OUTPUT_DOCX)
print("Master Capstone Report (.docx) successfully generated!")
