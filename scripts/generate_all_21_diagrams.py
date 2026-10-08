import os
from PIL import Image, ImageDraw, ImageFont

FONT_TITLE = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
FONT_SUBTITLE = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
FONT_HEADER = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
FONT_BODY = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
FONT_BOLD = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
FONT_CODE = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 11)
FONT_SMALL = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)

def create_base_canvas(title, subtitle):
    w, h = 1400, 800
    img = Image.new("RGB", (w, h), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    # Header Banner
    draw.rectangle([0, 0, w, 70], fill="#1E293B")
    draw.rectangle([0, 68, w, 72], fill="#2563EB")
    draw.text((30, 15), title, fill="#FFFFFF", font=FONT_TITLE)
    draw.text((30, 45), subtitle, fill="#94A3B8", font=FONT_SUBTITLE)
    
    # Footer
    draw.rectangle([0, h - 35, w, h], fill="#F1F5F9")
    draw.line([0, h - 35, w, h - 35], fill="#E2E8F0", width=1)
    draw.text((30, h - 25), "24CYS401 Secure Software Engineering | Digital Wallet & Payment Gateway Simulator", fill="#64748B", font=FONT_SMALL)
    draw.text((w - 280, h - 25), "Lead Architect: Sathvik Valivety", fill="#64748B", font=FONT_SMALL)
    return img, draw

def draw_card(draw, box, title, lines=[], fill="#FFFFFF", outline="#CBD5E1", header_fill="#F1F5F9", badge=None):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=fill, outline=outline, width=2)
    # Card header
    draw.rounded_rectangle([x0, y0, x1, y0 + 32], radius=6, fill=header_fill)
    draw.text((x0 + 12, y0 + 8), title, fill="#0F172A", font=FONT_HEADER)
    if badge:
        bw = len(badge) * 7 + 14
        draw.rounded_rectangle([x1 - bw - 10, y0 + 6, x1 - 10, y0 + 26], radius=4, fill="#2563EB")
        draw.text((x1 - bw - 3, y0 + 9), badge, fill="#FFFFFF", font=FONT_SMALL)
    
    cur_y = y0 + 44
    for line in lines:
        if isinstance(line, tuple):
            prefix, text, col = line
            draw.text((x0 + 12, cur_y), prefix, fill=col, font=FONT_BOLD)
            draw.text((x0 + 12 + len(prefix) * 8, cur_y), text, fill="#334155", font=FONT_BODY)
        else:
            draw.text((x0 + 12, cur_y), line, fill="#475569", font=FONT_BODY)
        cur_y += 20

def draw_arrow(draw, start, end, label=None, color="#2563EB", width=2):
    x0, y0 = start
    x1, y1 = end
    draw.line([x0, y0, x1, y1], fill=color, width=width)
    # Simple arrowhead
    if x1 > x0:
        draw.polygon([(x1, y1), (x1 - 10, y1 - 5), (x1 - 10, y1 + 5)], fill=color)
    elif x1 < x0:
        draw.polygon([(x1, y1), (x1 + 10, y1 - 5), (x1 + 10, y1 + 5)], fill=color)
    elif y1 > y0:
        draw.polygon([(x1, y1), (x1 - 5, y1 - 10), (x1 + 5, y1 - 10)], fill=color)
    elif y1 < y0:
        draw.polygon([(x1, y1), (x1 - 5, y1 + 10), (x1 + 5, y1 + 10)], fill=color)
    
    if label:
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        draw.rectangle([mx - len(label)*3 - 4, my - 9, mx + len(label)*3 + 4, my + 9], fill="#FFFFFF", outline=color)
        draw.text((mx - len(label)*3, my - 7), label, fill=color, font=FONT_SMALL)

os.makedirs("docs/diagrams", exist_ok=True)
print("Generating 21 High-Resolution Architecture & Security Diagrams...")

# 01_agile_lifecycle
img, draw = create_base_canvas("Figure 1 — Security-Driven Agile Scrum Lifecycle", "Phase 1: Iterative 2-Sprint Cadence with Embedded Threat Gates")
draw_card(draw, [50, 120, 280, 480], "Sprint Planning", [
    "• Threat Modeling (STRIDE)", "• Security User Stories", "• Story Point Estimation", "• Definition of Done (DoD)", "• Carry-Over Risk Triage"
], header_fill="#DBEAFE", badge="INIT")
draw_card(draw, [320, 120, 560, 480], "Sprint Execution", [
    "• Daily Security Scrums", "• TDD / Pair Programming", "• Concurrency Safeguards", "• Pessimistic Row Locking", "• Striped User Locks"
], header_fill="#FEF3C7", badge="DEV")
draw_card(draw, [600, 120, 840, 480], "DevSecOps Gates", [
    "• JUnit 5 (25 Tests)", "• Concurrency Stress Test", "• SonarQube SAST (0 Vuln)", "• Trivy Container Scan", "• Kubeconform IaC Check"
], header_fill="#FEE2E2", badge="GATE")
draw_card(draw, [880, 120, 1120, 480], "Sprint Review", [
    "• Working Software Demo", "• Idempotency Replay Demo", "• Defect DEF-001 Retest", "• Jira Velocity Analysis", "• Stakeholder Sign-Off"
], header_fill="#DCFCE7", badge="REVIEW")
draw_card(draw, [1160, 120, 1360, 480], "Retrospective", [
    "• Root-Cause Analysis", "• Process Optimization", "• Carried-Over Defect Log", "• Continuous Learning"
], header_fill="#F3E8FF", badge="RETRO")
draw_arrow(draw, (280, 300), (320, 300), "Commit")
draw_arrow(draw, (560, 300), (600, 300), "CI/CD")
draw_arrow(draw, (840, 300), (880, 300), "Validate")
draw_arrow(draw, (1120, 300), (1160, 300), "Reflect")
draw_arrow(draw, (1260, 480), (1260, 600))
draw.line([1260, 600, 160, 600], fill="#2563EB", width=2)
draw_arrow(draw, (160, 600), (160, 480), "Sprint 2 Feedback Loop")
img.save("docs/diagrams/01_agile_lifecycle.png")

# 02_system_context
img, draw = create_base_canvas("Figure 2 — Digital Wallet & Payment Gateway System Context", "Phase 1: High-Level System Context & Boundary Decomposition")
draw_card(draw, [60, 220, 300, 420], "Consumer User", ["• Registers Account", "• Authenticates via JWT", "• Views Wallet Balance", "• Initiates Payments", "• Requests Refunds"], header_fill="#DBEAFE", badge="ACTOR")
draw_card(draw, [60, 480, 300, 680], "Merchant Business", ["• Registers Business", "• Obtains 256-bit API Key", "• Accepts Consumer Payments", "• Inspects Settlements"], header_fill="#FEF3C7", badge="ACTOR")
draw_card(draw, [450, 180, 950, 700], "DWPG Simulator System Boundary", [
    ("CORE: ", "Spring Boot 3.3.4 + Java 21 Engine", "#1E3A8A"),
    ("AUTH: ", "Stateless JWT + BCrypt (Cost 12)", "#1E3A8A"),
    ("VAULT: ", "Pessimistic Locking + ACID Balance", "#16A34A"),
    ("IDEMP: ", "SHA-256 Digest Replay Filter", "#2563EB"),
    ("LEDGER: ", "Tamper-Evident SHA-256 Transaction Chain", "#7C3AED"),
    ("SIEM: ", "Immutable Audit Log with PII Scrub", "#DC2626"),
    ("API: ", "RESTful JSON / OpenAPI 3.0", "#0891B2")
], fill="#F8FAFC", header_fill="#E2E8F0", badge="TARGET")
draw_card(draw, [1100, 220, 1340, 420], "MariaDB Persistence", ["• Relational Schema", "• Row-Level Lock Queue", "• Foreign Key Invariants", "• ACID Compliance"], header_fill="#DCFCE7", badge="DB")
draw_card(draw, [1100, 480, 1340, 680], "Security Auditor", ["• Queries Security Logs", "• Inspects SIEM Alerts", "• Verifies Tamper Hashes", "• Enforces Compliance"], header_fill="#FEE2E2", badge="ADMIN")
draw_arrow(draw, (300, 320), (450, 320), "HTTPS / JWT")
draw_arrow(draw, (300, 580), (450, 580), "API Key / HTTPS")
draw_arrow(draw, (950, 320), (1100, 320), "JDBC / Pool")
draw_arrow(draw, (1100, 580), (950, 580), "Admin Audit")
img.save("docs/diagrams/02_system_context.png")

# 03_use_case
img, draw = create_base_canvas("Figure 3 — Digital Wallet & Payment Gateway UML Use Case Model", "Phase 3: Actor Roles, Primary Scenarios and Security Constraints")
draw_card(draw, [60, 180, 260, 380], "Actor: Consumer", ["• UC-REG: Register", "• UC-AUTH: Sign In", "• UC-WAL: Fund Wallet", "• UC-PAY: Make Payment", "• UC-REF: Request Refund"], header_fill="#DBEAFE")
draw_card(draw, [60, 440, 260, 640], "Actor: Merchant", ["• UC-MER: Register Merchant", "• UC-KEY: API Key Mgmt", "• UC-TXN: View Sales"], header_fill="#FEF3C7")
draw_card(draw, [360, 140, 940, 720], "System Use Cases (DWPG Simulator)", [
    ("UC-01 ", "User Registration & Argon2/BCrypt Hashing", "#2563EB"),
    ("UC-02 ", "JWT Authentication & Session Management", "#2563EB"),
    ("UC-03 ", "Wallet Provisioning with 0.00 Balance Invariant", "#16A34A"),
    ("UC-04 ", "Simulated Funds Top-Up (ACID Boundary)", "#16A34A"),
    ("UC-05 ", "Merchant Profile Registration & 256-bit Key", "#D97706"),
    ("UC-06 ", "Payment Initiation with Mandatory Idempotency-Key", "#DC2626"),
    ("UC-07 ", "Payment Confirmation & One-Way State Transition", "#DC2626"),
    ("UC-08 ", "Refund Processing with Anti-Double Refund Guard", "#7C3AED"),
    ("UC-09 ", "Tamper-Evident Transaction Ledger History", "#7C3AED"),
    ("UC-10 ", "Admin Security Audit Explorer & SIEM Alert Stream", "#BE123C")
], fill="#FFFFFF", header_fill="#E2E8F0")
draw_card(draw, [1040, 280, 1320, 500], "Actor: Compliance Auditor", ["• UC-ADM: Query Audit Logs", "• UC-ALT: Review Replay Alerts", "• UC-VER: Verify Hash Integrity"], header_fill="#FEE2E2")
draw_arrow(draw, (260, 280), (360, 280), "Executes")
draw_arrow(draw, (260, 540), (360, 540), "Executes")
draw_arrow(draw, (1040, 390), (940, 390), "Audits")
img.save("docs/diagrams/03_use_case.png")

# 04_analysis_model
img, draw = create_base_canvas("Figure 4 — Scenario-Based Analysis Model (Boundary-Control-Entity)", "Phase 3: Formal BCE Object Decomposition of Critical Payment Transaction")
draw_card(draw, [60, 180, 360, 680], "Boundary Objects", [
    ("UI: ", "PaymentView.jsx", "#2563EB"),
    ("CTR: ", "PaymentController.java", "#2563EB"),
    ("FLT: ", "JwtAuthenticationFilter.java", "#2563EB"),
    ("EXC: ", "GlobalExceptionHandler.java", "#DC2626"),
    ("DTO: ", "PaymentRequest.java", "#64748B"),
    ("DTO: ", "PaymentResponse.java", "#64748B")
], header_fill="#DBEAFE", badge="BOUNDARY")
draw_card(draw, [440, 180, 840, 680], "Control Objects", [
    ("SRV: ", "PaymentService.java", "#16A34A"),
    ("SRV: ", "WalletService.java", "#16A34A"),
    ("SRV: ", "IdempotencyService.java", "#16A34A"),
    ("SRV: ", "AuditService.java", "#16A34A"),
    ("LCK: ", "ConcurrentHashMap (User Locks)", "#D97706"),
    ("TXN: ", "TransactionTemplate (ACID)", "#D97706")
], header_fill="#DCFCE7", badge="CONTROL")
draw_card(draw, [920, 180, 1320, 680], "Entity Objects", [
    ("ENT: ", "User.java", "#7C3AED"),
    ("ENT: ", "Wallet.java (@Lock PESSIMISTIC)", "#7C3AED"),
    ("ENT: ", "Payment.java (INITIATED->CONFIRMED)", "#7C3AED"),
    ("ENT: ", "Transaction.java (SHA-256 Hash)", "#7C3AED"),
    ("ENT: ", "IdempotencyRecord.java", "#7C3AED"),
    ("ENT: ", "AuditLog.java (Immutable)", "#7C3AED")
], header_fill="#F3E8FF", badge="ENTITY")
draw_arrow(draw, (360, 360), (440, 360), "Invokes")
draw_arrow(draw, (840, 360), (920, 360), "Persists")
img.save("docs/diagrams/04_analysis_model.png")

# 05_erd
img, draw = create_base_canvas("Figure 5 — Relational Database Schema & Entity Relationship Model", "Phase 4: Tables, Constraints, Primary Keys, Foreign Keys and Cardinalities")
draw_card(draw, [50, 120, 320, 420], "users", [
    ("PK ", "id: BIGINT AUTO_INCREMENT", "#DC2626"),
    ("UQ ", "username: VARCHAR(50)", "#2563EB"),
    ("UQ ", "email: VARCHAR(100)", "#2563EB"),
    ("   ", "password_hash: VARCHAR(255)", "#64748B"),
    ("   ", "role: VARCHAR(20)", "#16A34A"),
    ("   ", "created_at: TIMESTAMP", "#64748B")
], header_fill="#DBEAFE")
draw_card(draw, [380, 120, 680, 420], "wallets", [
    ("PK ", "id: BIGINT AUTO_INCREMENT", "#DC2626"),
    ("FK ", "user_id: BIGINT (NOT NULL)", "#7C3AED"),
    ("UQ ", "account_number: VARCHAR(24)", "#2563EB"),
    ("   ", "balance: DECIMAL(19,4)", "#16A34A"),
    ("   ", "currency: VARCHAR(3)", "#64748B"),
    ("   ", "status: VARCHAR(20)", "#64748B")
], header_fill="#DCFCE7")
draw_card(draw, [740, 120, 1040, 420], "merchants", [
    ("PK ", "id: BIGINT AUTO_INCREMENT", "#DC2626"),
    ("FK ", "user_id: BIGINT (NOT NULL)", "#7C3AED"),
    ("   ", "business_name: VARCHAR(100)", "#2563EB"),
    ("UQ ", "api_key: VARCHAR(64)", "#D97706"),
    ("   ", "status: VARCHAR(20)", "#64748B")
], header_fill="#FEF3C7")
draw_card(draw, [1080, 120, 1350, 420], "idempotency_records", [
    ("PK ", "id: BIGINT AUTO_INCREMENT", "#DC2626"),
    ("UQ ", "idempotency_key: VARCHAR(128)", "#2563EB"),
    ("   ", "request_hash: VARCHAR(64)", "#D97706"),
    ("   ", "resource_id: BIGINT", "#64748B"),
    ("   ", "response_body: LONGTEXT", "#64748B"),
    ("   ", "status_code: INT", "#64748B")
], header_fill="#FEE2E2")
draw_card(draw, [200, 460, 560, 740], "payments", [
    ("PK ", "id: BIGINT AUTO_INCREMENT", "#DC2626"),
    ("FK ", "wallet_id: BIGINT", "#7C3AED"),
    ("FK ", "merchant_id: BIGINT", "#7C3AED"),
    ("   ", "amount: DECIMAL(19,4)", "#16A34A"),
    ("   ", "status: VARCHAR(20)", "#D97706"),
    ("   ", "correlation_id: VARCHAR(64)", "#2563EB"),
    ("   ", "tamper_hash: VARCHAR(64)", "#7C3AED")
], header_fill="#F3E8FF")
draw_card(draw, [620, 460, 960, 740], "transactions", [
    ("PK ", "id: BIGINT AUTO_INCREMENT", "#DC2626"),
    ("FK ", "wallet_id: BIGINT", "#7C3AED"),
    ("   ", "type: VARCHAR(20)", "#2563EB"),
    ("   ", "amount: DECIMAL(19,4)", "#16A34A"),
    ("   ", "balance_after: DECIMAL(19,4)", "#16A34A"),
    ("   ", "status: VARCHAR(20)", "#64748B"),
    ("   ", "tamper_hash: VARCHAR(64)", "#7C3AED")
], header_fill="#E0F2FE")
draw_card(draw, [1000, 460, 1350, 740], "audit_logs", [
    ("PK ", "id: BIGINT AUTO_INCREMENT", "#DC2626"),
    ("   ", "event_type: VARCHAR(50)", "#DC2626"),
    ("   ", "actor_username: VARCHAR(50)", "#2563EB"),
    ("   ", "resource_id: BIGINT", "#64748B"),
    ("   ", "outcome: VARCHAR(20)", "#16A34A"),
    ("   ", "ip_address: VARCHAR(45)", "#64748B"),
    ("   ", "details: VARCHAR(1000)", "#64748B")
], header_fill="#FFE4E6")
draw_arrow(draw, (320, 250), (380, 250), "1:1")
draw_arrow(draw, (320, 350), (740, 350), "1:1")
draw_arrow(draw, (530, 420), (380, 460), "1:N")
draw_arrow(draw, (530, 420), (790, 460), "1:N")
img.save("docs/diagrams/05_erd.png")

# 06_dfd_level0
img, draw = create_base_canvas("Figure 6 — Level 0 Data Flow Diagram (Context Model)", "Phase 4: External Entities, Core Process Boundary, and Primary Data Flows")
draw_card(draw, [60, 280, 320, 520], "Consumer Client", [
    "• Registration Data", "• Login Credentials", "• Top-Up Requests", "• Payment Requests", "• Refund Requests"
], header_fill="#DBEAFE", badge="ENTITY")
draw_card(draw, [480, 200, 920, 600], "Process 0: DWPG Simulator Engine", [
    ("CORE: ", "Spring Boot REST Service", "#1E3A8A"),
    ("SECURITY: ", "JWT Bearer Token Filter", "#2563EB"),
    ("ROUTING: ", "Idempotency & Replay Guard", "#DC2626"),
    ("MUTATION: ", "ACID Balance Locking", "#16A34A"),
    ("AUDIT: ", "SIEM Security Logging", "#7C3AED")
], fill="#FFFFFF", header_fill="#DCFCE7", badge="P-0")
draw_card(draw, [1080, 180, 1340, 380], "Merchant System", [
    "• Merchant Registration", "• API Key Validation", "• Webhook Callbacks", "• Settlement Telemetry"
], header_fill="#FEF3C7", badge="ENTITY")
draw_card(draw, [1080, 440, 1340, 640], "Compliance Auditor", [
    "• Audit Query Requests", "• Security Event Logs", "• Tamper Verification", "• SIEM Alert Notifications"
], header_fill="#FEE2E2", badge="ENTITY")
draw_arrow(draw, (320, 350), (480, 350), "Credentials / Orders")
draw_arrow(draw, (480, 450), (320, 450), "Tokens / Receipts")
draw_arrow(draw, (920, 280), (1080, 280), "Order Notifications")
draw_arrow(draw, (1080, 540), (920, 540), "Audit Requests")
draw_arrow(draw, (920, 580), (1080, 580), "Security Logs")
img.save("docs/diagrams/06_dfd_level0.png")

# 07_dfd_level1
img, draw = create_base_canvas("Figure 7 — Level 1 Data Flow Diagram (Operational Decomposition)", "Phase 4: Detailed Processes, Internal Data Stores, and Information Pipelines")
draw_card(draw, [40, 120, 260, 260], "P1: Authentication", ["• BCrypt Hashing", "• JWT Token Issuance", "• Failed Login Throttling"], header_fill="#DBEAFE")
draw_card(draw, [40, 320, 260, 460], "P2: Wallet Service", ["• Provision Wallet", "• Top-Up Balance", "• Non-Negative Invariant"], header_fill="#DCFCE7")
draw_card(draw, [40, 520, 260, 660], "P3: Merchant Service", ["• Onboard Business", "• Generate 256-bit Key", "• Role Verification"], header_fill="#FEF3C7")
draw_card(draw, [400, 220, 720, 560], "P4: Payment & Replay Guard", [
    ("4.1 ", "Extract Idempotency-Key Header", "#2563EB"),
    ("4.2 ", "Compute SHA-256 Payload Hash", "#2563EB"),
    ("4.3 ", "Check Existing Idempotency Record", "#DC2626"),
    ("4.4 ", "Acquire JVM Striped Lock", "#D97706"),
    ("4.5 ", "Execute SELECT FOR UPDATE", "#16A34A"),
    ("4.6 ", "Debit Wallet & Credit Merchant", "#16A34A"),
    ("4.7 ", "Generate Tamper-Evident Receipt", "#7C3AED")
], header_fill="#FEE2E2")
draw_card(draw, [840, 120, 1080, 260], "D1: Users & Wallets", ["• Credential Hashes", "• Atomic Balances", "• Account Numbers"], header_fill="#F1F5F9")
draw_card(draw, [840, 320, 1080, 460], "D2: Idempotency Cache", ["• SHA-256 Request Hashes", "• Cached Responses", "• HTTP Status Codes"], header_fill="#F1F5F9")
draw_card(draw, [840, 520, 1080, 660], "D3: Payments & Ledger", ["• Payment Records", "• Transaction Ledger", "• SHA-256 State Hashes"], header_fill="#F1F5F9")
draw_card(draw, [1140, 320, 1360, 460], "P5: SIEM Audit Logger", ["• Scrub Sensitive Data", "• Redact PAN / Passwords", "• Append to Audit Table"], header_fill="#F3E8FF")
draw_arrow(draw, (260, 390), (400, 390), "Debit Request")
draw_arrow(draw, (720, 200), (840, 200), "Lock & Update")
draw_arrow(draw, (720, 390), (840, 390), "Check / Store")
draw_arrow(draw, (720, 580), (840, 580), "Append Ledger")
draw_arrow(draw, (720, 440), (1140, 400), "Security Event")
img.save("docs/diagrams/07_dfd_level1.png")

# 08_trust_boundary
img, draw = create_base_canvas("Figure 8 — System Trust Boundaries & Threat Surface Mapping", "Phase 4: Threat Surface Demarcation Across Untrusted, DMZ and Protected Tiers")
# Draw zones
draw.rectangle([40, 120, 340, 720], fill="#FEF2F2", outline="#DC2626", width=2)
draw.text((60, 135), "ZONE 1: Untrusted Public Network", fill="#DC2626", font=FONT_HEADER)
draw_card(draw, [60, 180, 320, 380], "Web Browser / Client", ["• React 18 SPA", "• Untrusted User Input", "• Stored JWT Token", "• Browser LocalStorage"], header_fill="#FEE2E2")
draw_card(draw, [60, 440, 320, 640], "External Adversary", ["• Man-in-the-Middle (MitM)", "• Replay Attack Dispatches", "• Parameter Tampering", "• Automated Fuzzing Bots"], header_fill="#FEE2E2")

draw.rectangle([380, 120, 800, 720], fill="#FEFCE8", outline="#CA8A04", width=2)
draw.text((400, 135), "ZONE 2: DMZ & Application Gateway", fill="#CA8A04", font=FONT_HEADER)
draw_card(draw, [400, 180, 780, 420], "Reverse Proxy & Web Server", [
    "• Nginx Unprivileged (UID 101)", "• TLS / HTTPS Termination", "• Security Headers (CSP, XSS, XFO)", "• Rate Limiting & Reverse Proxy"
], header_fill="#FEF3C7")
draw_card(draw, [400, 460, 780, 680], "Spring Security Perimeter", [
    "• JwtAuthenticationFilter", "• BCrypt Password Validator", "• Idempotency Header Guard", "• Global Exception Handler"
], header_fill="#FEF3C7")

draw.rectangle([840, 120, 1360, 720], fill="#F0FDF4", outline="#16A34A", width=2)
draw.text((860, 135), "ZONE 3: Protected Core & Vault", fill="#16A34A", font=FONT_HEADER)
draw_card(draw, [860, 180, 1340, 420], "Core Business Microservices", [
    "• PaymentService (Striped Locks)", "• WalletService (Ownership BOLA Guard)", "• RefundService (Single Refund Guard)", "• AuditService (PII Scrubber)"
], header_fill="#DCFCE7")
draw_card(draw, [860, 460, 1340, 680], "MariaDB Transaction Vault", [
    "• NetworkPolicy Port 3306 Restricted", "• SELECT FOR UPDATE Row Locks", "• Foreign Key Constraints", "• Non-root User (dwpg_user)"
], header_fill="#DCFCE7")
draw_arrow(draw, (320, 280), (400, 280), "TB-1: TLS 1.3")
draw_arrow(draw, (780, 280), (860, 280), "TB-2: Authenticated")
draw_arrow(draw, (1100, 420), (1100, 460), "TB-3: Encrypted JDBC")
img.save("docs/diagrams/08_trust_boundary.png")

# 09_architecture
img, draw = create_base_canvas("Figure 9 — Layered Secure Architecture Model", "Phase 5: Four-Tier Secure Architecture with Defense-in-Depth Enforcements")
draw_card(draw, [50, 120, 330, 720], "1. Presentation Layer", [
    ("TECH: ", "React 18 + Vite 5.4", "#2563EB"),
    ("VIEWS: ", "LoginView, RegisterView", "#64748B"),
    (" ", "WalletView, PaymentView", "#64748B"),
    (" ", "TransactionLedgerView", "#64748B"),
    (" ", "MerchantView, AdminAuditView", "#64748B"),
    ("SEC: ", "XSS Content Sanitization", "#16A34A"),
    ("SEC: ", "Automatic UUIDv4 Idempotency", "#16A34A"),
    ("SEC: ", "Interactive Replay Test Lab", "#D97706")
], header_fill="#DBEAFE")
draw_card(draw, [380, 120, 670, 720], "2. API & Security Layer", [
    ("TECH: ", "Spring Security 6.3", "#2563EB"),
    ("AUTH: ", "JwtAuthenticationFilter", "#16A34A"),
    ("ROLE: ", "@PreAuthorize(USER/MERCH/ADM)", "#16A34A"),
    ("CORS: ", "Restricted Origins & Methods", "#16A34A"),
    ("VAL: ", "Jakarta Validation (Size/Pattern)", "#16A34A"),
    ("EXC: ", "GlobalExceptionHandler", "#DC2626"),
    ("ACT: ", "Hardened Spring Actuator", "#D97706")
], header_fill="#DCFCE7")
draw_card(draw, [720, 120, 1010, 720], "3. Business Service Layer", [
    ("TECH: ", "Java 21 Virtual Threads & JPA", "#2563EB"),
    ("SRV: ", "PaymentService (ACID Engine)", "#16A34A"),
    ("SRV: ", "WalletService (Invariant Guard)", "#16A34A"),
    ("SRV: ", "IdempotencyService (SHA-256)", "#16A34A"),
    ("SRV: ", "RefundService (Anti-Double)", "#16A34A"),
    ("SRV: ", "AuditService (PII Scrubber)", "#DC2626"),
    ("LCK: ", "ConcurrentHashMap Striping", "#D97706")
], header_fill="#FEF3C7")
draw_card(draw, [1060, 120, 1350, 720], "4. Persistence Layer", [
    ("TECH: ", "Spring Data JPA + MariaDB 11.4", "#2563EB"),
    ("LOCK: ", "PESSIMISTIC_WRITE Lock Mode", "#DC2626"),
    ("POOL: ", "HikariCP (Max 30, Timeout 30s)", "#16A34A"),
    ("ACID: ", "REPEATABLE_READ Isolation", "#16A34A"),
    ("HASH: ", "SHA-256 Ledger State Chain", "#7C3AED"),
    ("USER: ", "Unprivileged dwpg_user", "#16A34A")
], header_fill="#F3E8FF")
draw_arrow(draw, (330, 400), (380, 400), "REST / JSON")
draw_arrow(draw, (670, 400), (720, 400), "Service Call")
draw_arrow(draw, (1010, 400), (1060, 400), "Repository")
img.save("docs/diagrams/09_architecture.png")

# 10_component
img, draw = create_base_canvas("Figure 10 — Detailed Software Component & Interface Diagram", "Phase 5: High-Cohesion Component Topology and Interaction Interfaces")
draw_card(draw, [50, 140, 440, 400], "Auth & Identity Component", [
    "• AuthController.java", "• AuthService.java", "• JwtTokenProvider.java", "• UserRepository.java",
    "• Interfaces: /api/auth/register, /api/auth/login"
], header_fill="#DBEAFE")
draw_card(draw, [50, 450, 440, 720], "Wallet & Vault Component", [
    "• WalletController.java", "• WalletService.java", "• WalletRepository.java",
    "• Interfaces: /api/wallet, /api/wallet/topup",
    "• Locks: findByUserIdForUpdate() [PESSIMISTIC_WRITE]"
], header_fill="#DCFCE7")
draw_card(draw, [490, 140, 910, 720], "Payment & Idempotency Component", [
    ("CTR: ", "PaymentController.java", "#2563EB"),
    ("SRV: ", "PaymentService.java", "#16A34A"),
    ("IDM: ", "IdempotencyService.java", "#DC2626"),
    ("REF: ", "RefundService.java", "#D97706"),
    ("TXN: ", "TransactionService.java", "#7C3AED"),
    ("LOG: ", "AuditService.java", "#BE123C"),
    (" ", "Interfaces: POST /api/payments/initiate", "#64748B"),
    (" ", "Interfaces: POST /api/refunds", "#64748B"),
    (" ", "Interfaces: GET /api/transactions/my", "#64748B")
], header_fill="#FEE2E2")
draw_card(draw, [960, 140, 1350, 400], "Merchant Management Component", [
    "• MerchantController.java", "• MerchantService.java", "• MerchantRepository.java",
    "• Interfaces: /api/merchant/register, /api/merchant/me"
], header_fill="#FEF3C7")
draw_card(draw, [960, 450, 1350, 720], "Audit & Compliance Component", [
    "• AdminController.java", "• AuditService.java", "• AuditLogRepository.java",
    "• Interfaces: /api/admin/audit-logs", "• Security Alert Evaluation Stream"
], header_fill="#FFE4E6")
draw_arrow(draw, (440, 270), (490, 270))
draw_arrow(draw, (440, 580), (490, 580))
draw_arrow(draw, (910, 270), (960, 270))
draw_arrow(draw, (910, 580), (960, 580))
img.save("docs/diagrams/10_component.png")

# 11_deployment
img, draw = create_base_canvas("Figure 11 — Physical Deployment Architecture & Network Topology", "Phase 5: Multi-Tier Containerized Pod Deployment with Isolation Safeguards")
draw_card(draw, [50, 160, 320, 660], "Client Ingress Tier", [
    ("HOST: ", "User Browser Client", "#1E3A8A"),
    ("PORT: ", "Host Port 3000 / NodePort 30080", "#2563EB"),
    ("PROT: ", "HTTPS / TLS 1.3", "#16A34A"),
    ("DNS: ", "wallet.simulator.local", "#64748B"),
    ("LB: ", "Ingress / Reverse Proxy", "#D97706")
], header_fill="#DBEAFE")
draw_card(draw, [380, 160, 800, 660], "Application Pod Tier (Kubernetes)", [
    ("POD: ", "dwpg-frontend-deployment (2 Replicas)", "#2563EB"),
    ("USR: ", "UID 101 (nginx-unprivileged)", "#16A34A"),
    ("POD: ", "dwpg-backend-deployment (2 Replicas)", "#2563EB"),
    ("USR: ", "UID 10001 (appuser: Alpine JRE 21)", "#16A34A"),
    ("RAM: ", "Requests 512Mi, Limits 1Gi", "#64748B"),
    ("PRB: ", "Liveness & Readiness /actuator/health", "#16A34A"),
    ("SEC: ", "PSS Restricted (drop ALL capabilities)", "#DC2626")
], header_fill="#DCFCE7")
draw_card(draw, [860, 160, 1350, 660], "Data Persistence Tier (Isolated)", [
    ("POD: ", "dwpg-mariadb-deployment (Stateful)", "#1E3A8A"),
    ("SVC: ", "dwpg-mariadb-service:3306 (ClusterIP)", "#2563EB"),
    ("PVC: ", "mariadb-pvc (5Gi ReadWriteOnce)", "#64748B"),
    ("POL: ", "NetworkPolicy (Default Deny Ingress)", "#DC2626"),
    ("RULE: ", "Permits TCP 3306 ONLY from dwpg-backend", "#16A34A"),
    ("ENC: ", "TLS in-flight transport encryption", "#16A34A")
], header_fill="#F3E8FF")
draw_arrow(draw, (320, 410), (380, 410), "HTTP :3000")
draw_arrow(draw, (800, 410), (860, 410), "ClusterIP :3306")
img.save("docs/diagrams/11_deployment.png")

# 12_payment_sequence
img, draw = create_base_canvas("Figure 12 — Payment Transaction Lifecycle Sequence Diagram", "Phase 5: End-to-End Payment Execution with Idempotency and Locking")
draw_card(draw, [50, 140, 200, 220], "User / SPA", ["Client Actor"], header_fill="#DBEAFE")
draw_card(draw, [250, 140, 400, 220], "API Controller", ["REST Boundary"], header_fill="#DBEAFE")
draw_card(draw, [450, 140, 620, 220], "Idempotency", ["Replay Guard"], header_fill="#FEE2E2")
draw_card(draw, [670, 140, 840, 220], "PaymentService", ["Striped Lock"], header_fill="#DCFCE7")
draw_card(draw, [890, 140, 1060, 220], "WalletRepository", ["Row Lock Mode"], header_fill="#FEF3C7")
draw_card(draw, [1110, 140, 1350, 220], "AuditService", ["SIEM Vault"], header_fill="#FFE4E6")

# Sequence lines
for x in [125, 325, 535, 755, 975, 1230]:
    draw.line([x, 220, x, 720], fill="#CBD5E1", width=1)

y = 260
draw_arrow(draw, (125, y), (325, y), "1. POST /payments/initiate [Idempotency-Key]"); y += 50
draw_arrow(draw, (325, y), (535, y), "2. checkIdempotency(key, hash)"); y += 50
draw_arrow(draw, (535, y), (325, y), "3. Key is NEW -> Continue"); y += 50
draw_arrow(draw, (325, y), (755, y), "4. processPayment(req, user)"); y += 50
draw_arrow(draw, (755, y), (975, y), "5. findByUserIdForUpdate(uid) [SELECT FOR UPDATE]"); y += 50
draw_arrow(draw, (975, y), (755, y), "6. Returns Locked Wallet Record"); y += 50
draw_arrow(draw, (755, y), (755, y + 25), "7. wallet.debit(amount)"); y += 40
draw_arrow(draw, (755, y), (1230, y), "8. logEvent(PAYMENT_CONFIRMED)"); y += 50
draw_arrow(draw, (755, y), (535, y), "9. saveIdempotencyRecord(key, res)"); y += 50
draw_arrow(draw, (755, y), (325, y), "10. PaymentResponse (CONFIRMED)"); y += 40
draw_arrow(draw, (325, y), (125, y), "11. HTTP 200 OK + Tamper Hash")
img.save("docs/diagrams/12_payment_sequence.png")

# 13_auth_sequence
img, draw = create_base_canvas("Figure 13 — Authentication & JWT Session Issuance Sequence Diagram", "Phase 5: Secure Registration, BCrypt Verification and Role Authorization")
draw_card(draw, [50, 140, 220, 220], "Client Browser", ["User / SPA"], header_fill="#DBEAFE")
draw_card(draw, [280, 140, 480, 220], "SecurityConfig", ["Filter Chain"], header_fill="#DCFCE7")
draw_card(draw, [540, 140, 760, 220], "AuthService", ["Auth Logic"], header_fill="#FEF3C7")
draw_card(draw, [820, 140, 1040, 220], "UserRepository", ["Database"], header_fill="#F3E8FF")
draw_card(draw, [1100, 140, 1340, 220], "JwtTokenProvider", ["Crypto Engine"], header_fill="#DBEAFE")

for x in [135, 380, 650, 930, 1220]:
    draw.line([x, 220, x, 720], fill="#CBD5E1", width=1)

y = 260
draw_arrow(draw, (135, y), (380, y), "1. POST /api/auth/register (username, pass)"); y += 60
draw_arrow(draw, (380, y), (650, y), "2. registerUser(req)"); y += 60
draw_arrow(draw, (650, y), (930, y), "3. BCrypt.hashpw(pass, salt12) -> save()"); y += 60
draw_arrow(draw, (930, y), (135, y), "4. HTTP 201 Created"); y += 70
draw_arrow(draw, (135, y), (380, y), "5. POST /api/auth/login (username, pass)"); y += 60
draw_arrow(draw, (380, y), (650, y), "6. authenticate(credentials)"); y += 60
draw_arrow(draw, (650, y), (1220, y), "7. generateToken(username, role)"); y += 60
draw_arrow(draw, (1220, y), (650, y), "8. Returns Signed 256-bit JWT"); y += 60
draw_arrow(draw, (650, y), (135, y), "9. HTTP 200 OK (Bearer JWT Token)")
img.save("docs/diagrams/13_auth_sequence.png")

# 14_threat_model
img, draw = create_base_canvas("Figure 14 — STRIDE Threat Model Decomposition & Controls", "Phase 7: Systematic Threat Identification and Architectural Mitigations")
stride_cards = [
    ("Spoofing (S)", ["• Impersonating Alice", "• Forging JWT tokens", "• Brute-force passwords"], "BCrypt Cost 12 + HMAC-SHA256 Secret", [50, 140, 450, 400], "#DBEAFE"),
    ("Tampering (T)", ["• Altering payment amount", "• Inverting balance in transit", "• Modifying merchant ID"], "SHA-256 Tamper Hash + Server-Side Derivation", [490, 140, 890, 400], "#DCFCE7"),
    ("Repudiation (R)", ["• Denying payment creation", "• Claiming refund not processed", "• False dispute claims"], "Immutable Audit Trail + Correlation IDs", [930, 140, 1340, 400], "#FEF3C7"),
    ("Info Disclosure (I)", ["• Leaking card PAN in logs", "• Stack traces in error body", "• Sniffing plain HTTP traffic"], "Regex Scrubbing + Suppressed Stacktraces", [50, 440, 450, 710], "#FEE2E2"),
    ("Denial of Service (D)", ["• Flooding checkout requests", "• Database lock starvation", "• Hikari connection exhaustion"], "Striped JVM Locks + Hikari 30 Pool + cgroups", [490, 440, 890, 710], "#F3E8FF"),
    ("Elevation of Privilege (E)", ["• BOLA reading foreign wallet", "• Regular user executing admin", "• Merchant modifying ledger"], "Spring @PreAuthorize + Principal Ownership Check", [930, 440, 1340, 710], "#FFE4E6")
]
for title, threats, control, box, header_col in stride_cards:
    lines = threats + [("DEFENSE: ", control, "#16A34A")]
    draw_card(draw, box, title, lines, header_fill=header_col)
img.save("docs/diagrams/14_threat_model.png")

# 15_attack_tree
img, draw = create_base_canvas("Figure 15 — Hierarchical Attack Tree: Exhaust Funds & Double Spending", "Phase 8: Quantitative Path Analysis and Defensive Countermeasure Mapping")
draw_card(draw, [400, 110, 1000, 200], "ROOT GOAL: Drain Wallet Funds via Double-Spending or Replay", [
    ("IMPACT: ", "CRITICAL | Severity: High | Asset: Financial Balance", "#DC2626")
], header_fill="#FEE2E2", badge="GOAL")

draw_card(draw, [50, 260, 440, 500], "Branch 1: Race Condition", [
    "• Parallel checkout threads",
    "• Read-then-write collision",
    "• Exploits non-locking queries",
    ("RISK: ", "Cost: Low | Skill: Med", "#D97706"),
    ("CONTROL: ", "MariaDB PESSIMISTIC_WRITE", "#16A34A"),
    ("TEST: ", "PaymentConcurrencyTest (10 th)", "#2563EB")
], header_fill="#DBEAFE")

draw_card(draw, [500, 260, 890, 500], "Branch 2: Replay Attack", [
    "• Packet re-transmission",
    "• Re-submitting payment POST",
    "• Exploits non-idempotent API",
    ("RISK: ", "Cost: Low | Skill: Low", "#D97706"),
    ("CONTROL: ", "Idempotency-Key + SHA-256", "#16A34A"),
    ("TEST: ", "PaymentSecurityIntegrationTest", "#2563EB")
], header_fill="#FEF3C7")

draw_card(draw, [950, 260, 1350, 500], "Branch 3: Payload Tampering", [
    "• Intercept checkout packet",
    "• Modify recipient merchant",
    "• Change debit amount to $0.01",
    ("RISK: ", "Cost: Med | Skill: High", "#D97706"),
    ("CONTROL: ", "SHA-256 Hash Tamper Seal", "#16A34A"),
    ("TEST: ", "PaymentInputFuzzingTest", "#2563EB")
], header_fill="#F3E8FF")

draw_card(draw, [250, 560, 1150, 720], "Integrated Defensive Architecture Verification", [
    ("VERIFICATION: ", "PaymentConcurrencyTest verified 10 parallel threads -> Exactly 2 debits succeeded ($100), 8 denied.", "#16A34A"),
    ("VERIFICATION: ", "Idempotent duplicate returns cached HTTP 200 receipt without secondary balance deduction.", "#16A34A"),
    ("VERIFICATION: ", "Tampered payload with reused Idempotency-Key triggers REPLAY_DETECTED audit event & HTTP 400 rejection.", "#16A34A")
], header_fill="#DCFCE7", badge="PROVEN")

draw_arrow(draw, (700, 200), (245, 260), "OR")
draw_arrow(draw, (700, 200), (695, 260), "OR")
draw_arrow(draw, (700, 200), (1150, 260), "OR")
draw_arrow(draw, (245, 500), (450, 560))
draw_arrow(draw, (695, 500), (700, 560))
draw_arrow(draw, (1150, 500), (950, 560))
img.save("docs/diagrams/15_attack_tree.png")

# 16_security_architecture
img, draw = create_base_canvas("Figure 16 — Refined Security Architecture & Defense Matrix", "Phase 8: Multi-Layered Hardening Controls and Safeguards")
layers = [
    ("Perimeter Security", ["• Nginx Reverse Proxy (UID 101)", "• CSP, X-Frame-Options, XSS Headers", "• Rate Limiting & TLS Termination"], [50, 140, 340, 700], "#DBEAFE"),
    ("Identity & Access", ["• BCrypt Hashing (Cost 12)", "• HMAC-SHA256 256-bit JWT", "• Spring @PreAuthorize RBAC", "• BOLA Ownership Validation"], [380, 140, 680, 700], "#DCFCE7"),
    ("Transaction Engine", ["• Mandatory Idempotency-Key", "• SHA-256 Request Payload Hash", "• Striped JVM Reentrant Locks", "• MariaDB PESSIMISTIC_WRITE"], [720, 140, 1020, 700], "#FEF3C7"),
    ("Audit & Monitoring", ["• Immutable audit_logs Table", "• Automated PCI-DSS Regex Scrub", "• Correlation ID Distributed Trace", "• SIEM Threat Alert Stream"], [1060, 140, 1350, 700], "#FFE4E6")
]
for title, items, box, header_col in layers:
    draw_card(draw, box, title, items, header_fill=header_col)
img.save("docs/diagrams/16_security_architecture.png")

# 17_docker
img, draw = create_base_canvas("Figure 17 — Hardened Multi-Stage Container Architecture", "Phase 13: Docker Build Stages, Distroless/Alpine Base and User Sandboxing")
draw_card(draw, [50, 140, 440, 680], "Backend Dockerfile (Alpine JRE 21)", [
    ("STAGE 1: ", "Maven 3.9 + Temurin JDK 21 Builder", "#2563EB"),
    ("STAGE 2: ", "eclipse-temurin:21-jre-alpine Runtime", "#2563EB"),
    ("USER: ", "UID 10001 : GID 10001 (appuser)", "#16A34A"),
    ("PORT: ", "Exposed: 8080 (http-api)", "#64748B"),
    ("JVM: ", "-XX:+UseContainerSupport", "#D97706"),
    ("JVM: ", "-XX:MaxRAMPercentage=75.0", "#D97706"),
    ("ENTROPY: ", "-Djava.security.egd=/dev/urandom", "#16A34A"),
    ("HEALTH: ", "wget spider /actuator/health", "#16A34A"),
    ("SIZE: ", "129 MB Compressed", "#7C3AED")
], header_fill="#DBEAFE", badge="BACKEND")

draw_card(draw, [490, 140, 890, 680], "Frontend Dockerfile (Unprivileged Nginx)", [
    ("STAGE 1: ", "Node 22 Alpine (Vite Builder)", "#2563EB"),
    ("STAGE 2: ", "nginxinc/nginx-unprivileged:alpine", "#2563EB"),
    ("USER: ", "UID 101 : GID 101 (nginx)", "#16A34A"),
    ("PORT: ", "Exposed: 3000 (http-ui)", "#64748B"),
    ("HEADERS: ", "Content-Security-Policy", "#16A34A"),
    ("HEADERS: ", "X-Frame-Options: SAMEORIGIN", "#16A34A"),
    ("HEADERS: ", "X-Content-Type-Options: nosniff", "#16A34A"),
    ("PROXY: ", "Reverse Proxy /api/ to backend:8080", "#2563EB"),
    ("SIZE: ", "25.9 MB Compressed", "#7C3AED")
], header_fill="#FEF3C7", badge="FRONTEND")

draw_card(draw, [940, 140, 1350, 680], "Docker Compose Multi-Container Fabric", [
    ("NETWORK: ", "dwpg-network (Isolated Bridge)", "#2563EB"),
    ("VOLUME: ", "mariadb_data (Persistent)", "#64748B"),
    ("DB: ", "mariadb:11.4 with healthcheck", "#16A34A"),
    ("DEP: ", "backend depends_on: mariadb healthy", "#D97706"),
    ("DEP: ", "frontend depends_on: backend healthy", "#D97706"),
    ("SECRETS: ", "Injected via .env (never committed)", "#16A34A")
], header_fill="#DCFCE7", badge="COMPOSE")
img.save("docs/diagrams/17_docker.png")

# 18_kubernetes
img, draw = create_base_canvas("Figure 18 — Production Kubernetes Manifest & Pod Security Standard", "Phase 13: Namespaces, Restricted Pod Security Standards & Zero-Trust Policies")
draw_card(draw, [50, 140, 440, 680], "dwpg Namespace Resources", [
    ("NS: ", "00-namespace.yaml (dwpg)", "#2563EB"),
    ("CFG: ", "01-configmap.yaml (JDBC/Profile)", "#64748B"),
    ("SEC: ", "02-secret.yaml (MariaDB Pass/JWT)", "#DC2626"),
    ("PVC: ", "03-mariadb-pvc.yaml (5Gi RWO)", "#64748B"),
    ("DEP: ", "04-mariadb-deployment.yaml", "#2563EB"),
    ("SVC: ", "05-mariadb-service.yaml (ClusterIP)", "#2563EB")
], header_fill="#DBEAFE")
draw_card(draw, [490, 140, 910, 680], "Application Pods (PSS Restricted)", [
    ("DEP: ", "06-backend-deployment.yaml (2 Replicas)", "#2563EB"),
    ("SEC: ", "runAsNonRoot: true, runAsUser: 10001", "#16A34A"),
    ("SEC: ", "allowPrivilegeEscalation: false", "#16A34A"),
    ("SEC: ", "capabilities: drop: ['ALL']", "#16A34A"),
    ("SVC: ", "07-backend-service.yaml (ClusterIP)", "#2563EB"),
    ("DEP: ", "08-frontend-deployment.yaml (2 Replicas)", "#2563EB"),
    ("SVC: ", "09-frontend-service.yaml (NodePort :30080)", "#2563EB")
], header_fill="#DCFCE7")
draw_card(draw, [960, 140, 1350, 680], "10-networkpolicy.yaml (Zero-Trust)", [
    ("RULE 1: ", "Default Deny Ingress on MariaDB", "#DC2626"),
    ("RULE 2: ", "Allow Port 3306 ONLY from dwpg-backend", "#16A34A"),
    ("RULE 3: ", "Allow Port 8080 from dwpg-frontend", "#16A34A"),
    ("RULE 4: ", "Allow Port 3000 Ingress from external", "#2563EB"),
    ("RESULT: ", "Zero Lateral Movement from compromised UI", "#16A34A")
], header_fill="#FEE2E2")
img.save("docs/diagrams/18_kubernetes.png")

# 19_cicd
img, draw = create_base_canvas("Figure 19 — GitHub Actions DevSecOps CI/CD Workflow", "Phase 14: Six-Stage Automated Quality & Security Gate Pipeline (.github/workflows/ci.yml)")
stages = [
    ("Stage 1: Build & Test", ["• Checkout Source", "• JDK 21 Temurin Setup", "• mvn clean test", "• 25/25 Tests Passing"], [50, 160, 240, 640], "#DBEAFE"),
    ("Stage 2: JaCoCo Coverage", ["• Upload Coverage XML", "• Threshold >= 60%", "• Actual: 62.6%", "• Fail on Coverage Drop"], [270, 160, 460, 640], "#DCFCE7"),
    ("Stage 3: SonarQube SAST", ["• AST Deep Scan", "• OWASP Top 10 Rules", "• Quality Gate: OK", "• 0 Blocker/Criticals"], [490, 160, 680, 640], "#FEF3C7"),
    ("Stage 4: Frontend Lint", ["• Node 22 Setup", "• npm ci install", "• npm run build", "• Zero Bundling Errors"], [710, 160, 900, 640], "#F3E8FF"),
    ("Stage 5: Trivy Scan", ["• Build Docker Images", "• aquasecurity/trivy", "• Scan Alpine JRE & Nginx", "• Gate: 0 Critical CVEs"], [930, 160, 1120, 640], "#FEE2E2"),
    ("Stage 6: K8s IaC Lint", ["• Kubeconform Setup", "• Strict Schema Check", "• Validate 11 Manifests", "• PSS Compliance Check"], [1150, 160, 1350, 640], "#FFE4E6")
]
for title, items, box, header_col in stages:
    draw_card(draw, box, title, items, header_fill=header_col)
    if box[2] < 1300:
        draw_arrow(draw, (box[2], 380), (box[2] + 30, 380))
img.save("docs/diagrams/19_cicd.png")

# 20_security_pipeline
img, draw = create_base_canvas("Figure 20 — Continuous Security Testing Architecture", "Phase 14: Multi-Dimensional Security Verification Matrix")
draw_card(draw, [50, 140, 440, 400], "SAST: Static Security Analysis", [
    "• SonarQube Server 9.9 LTS", "• JavaSensor (68 files indexed)", "• Rule java:S6437 (Hardcoded Secrets)", "• Result: 0 Vulnerabilities, 0 Bugs"
], header_fill="#DBEAFE")
draw_card(draw, [50, 440, 440, 700], "DAST / Boundary Fuzzing", [
    "• PaymentInputFuzzingTest.java", "• 12 Boundary Vectors (Negative, NaN, Overflow)", "• SQL Injection Parameterized JPA Immunity", "• Result: 100% Pass Rate"
], header_fill="#DCFCE7")
draw_card(draw, [490, 140, 910, 700], "Concurrency & Race Stress Testing", [
    ("SUITE: ", "PaymentConcurrencyTest.java", "#2563EB"),
    ("THREADS: ", "10 Simultaneous Parallel Executions", "#DC2626"),
    ("BALANCE: ", "$100.00 Wallet Initial State", "#16A34A"),
    ("DEMAND: ", "10 x $50.00 = $500.00 Total Attempted", "#DC2626"),
    ("RESULT: ", "Exactly 2 Succeeded (2 x $50 = $100)", "#16A34A"),
    ("DENIED: ", "Exactly 8 Failed (InsufficientFundsException)", "#16A34A"),
    ("FINAL: ", "Wallet Balance = $0.00 (Zero Double Spending)", "#16A34A"),
    ("DEADLOCK: ", "0 Deadlocks Observed (Hikari Pool Size 30)", "#16A34A")
], header_fill="#FEF3C7", badge="PROVEN")
draw_card(draw, [960, 140, 1350, 400], "SCA: Container Vulnerability Scanning", [
    "• Aqua Security Trivy Scan", "• Minimal Alpine JRE Base", "• Scans OS libraries & JAR dependencies", "• Result: 0 Unpatched Critical CVEs"
], header_fill="#FEE2E2")
draw_card(draw, [960, 440, 1350, 700], "IaC: Kubernetes Policy Enforcement", [
    "• Kubeconform Strict Validation", "• Pod Security Standard (Restricted)", "• Default-Deny NetworkPolicy", "• Result: 11 / 11 Manifests Compliant"
], header_fill="#F3E8FF")
img.save("docs/diagrams/20_security_pipeline.png")

# 21_traceability
img, draw = create_base_canvas("Figure 21 — Bidirectional Requirements Traceability Flow", "Phase 16: Complete Traceability Chain from Requirements to Empirical Evidence")
chain_boxes = [
    ("Requirement", "FR-006 & SEC-006", "Pessimistic Locking & Idempotency", [50, 180, 240, 360], "#DBEAFE"),
    ("UML Model", "UC-PAY-001", "Payment Initiation Specification", [270, 180, 460, 360], "#DCFCE7"),
    ("Threat Model", "STRIDE / Tree", "Branch 1: Race Condition & Double Spend", [490, 180, 680, 360], "#FEF3C7"),
    ("Jira Backlog", "DEF-001 / DWPG-19", "Sprint 2 Concurrency Hardening Story", [710, 180, 900, 360], "#FEE2E2"),
    ("Source Code", "PaymentService.java", "findByUserIdForUpdate() [PESSIMISTIC_WRITE]", [930, 180, 1120, 360], "#F3E8FF"),
    ("Verification", "ConcurrencyTest", "10 Threads Stress -> Zero Double Spend", [1150, 180, 1350, 360], "#DCFCE7")
]
for title, code, desc, box, header_col in chain_boxes:
    draw_card(draw, box, title, [code, desc], header_fill=header_col)
    if box[2] < 1300:
        draw_arrow(draw, (box[2], 270), (box[2] + 30, 270))

draw_card(draw, [150, 450, 1250, 680], "Master Traceability Coverage Matrix Summary", [
    ("FUNCTIONAL: ", "12 / 12 Requirements (FR-001..12) Mapped to Source, Tests & Verification Artifacts", "#16A34A"),
    ("NON-FUNCTIONAL: ", "6 / 6 Requirements (NFR-001..06) Mapped to Performance, ACID, Container & PSS Standards", "#16A34A"),
    ("SECURITY: ", "10 / 10 Security Requirements (SEC-001..10) Verified via Concurrency, Fuzzing & SAST Scans", "#16A34A"),
    ("JIRA STORIES: ", "8 Epics, 13 User Stories Closed Across Sprint 1 & Sprint 2 on Jira Cloud DWPG Board", "#16A34A"),
    ("CERTIFICATION: ", "Complete Bidirectional Spreadsheet Preserved in docs/final/traceability-matrix.xlsx", "#1E3A8A")
], header_fill="#E0F2FE", badge="100% COVERAGE")
img.save("docs/diagrams/21_traceability.png")

print("All 21 diagrams generated successfully in docs/diagrams/!")
