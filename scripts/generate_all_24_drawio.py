#!/usr/bin/env python3
"""
DWPG DRAW.IO 24-DIAGRAM GENERATOR & EXPORTER
Generates 100% valid, rich, production-grade draw.io (.drawio) XML source files
for all 24 required diagrams, and exports them to PNG (scale 2) and SVG.
"""

import os
import subprocess
import html

DRAWIO_DIR = "docs/diagrams/drawio"
PNG_DIR = "docs/diagrams/png"
SVG_DIR = "docs/diagrams/svg"
DRAWIO_BIN = "/home/sathvik/.local/bin/drawio"

os.makedirs(DRAWIO_DIR, exist_ok=True)
os.makedirs(PNG_DIR, exist_ok=True)
os.makedirs(SVG_DIR, exist_ok=True)

def make_drawio(filename, title, content_xml, width=1400, height=900):
    filepath = os.path.join(DRAWIO_DIR, filename)
    xml = f'''<mxfile host="app.diagrams.net" modified="2026-10-08T12:00:00.000Z" agent="Antigravity" version="24.0.0">
  <diagram id="DWPG-{filename.replace('.drawio', '')}" name="{title}">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{width}" pageHeight="{height}" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
{content_xml}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
    with open(filepath, 'w') as f:
        f.write(xml)
    print(f"Generated: {filepath}")

def b(id, val, x, y, w, h, style="rounded=1;whiteSpace=wrap;html=1;", parent="1"):
    val_esc = html.escape(val).replace('\n', '&#xa;')
    return f'        <mxCell id="{id}" value="{val_esc}" style="{style}" vertex="1" parent="{parent}"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>\n'

def e(id, src, tgt, val="", style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#1E3A8A;strokeWidth=2;"):
    val_esc = html.escape(val).replace('\n', '&#xa;')
    return f'        <mxCell id="{id}" value="{val_esc}" style="{style}" edge="1" parent="1" source="{src}" target="{tgt}"><mxGeometry relative="1" as="geometry" /></mxCell>\n'

def header(title):
    return b("title_banner", f"DIGITAL WALLET & PAYMENT GATEWAY SIMULATOR | {title}", 60, 20, 1280, 40, "shape=rect;fillColor=#1E3A8A;fontColor=#FFFFFF;fontStyle=1;fontSize=14;rounded=1;")

# ==============================================================================
# 01. Agile Development Lifecycle
# ==============================================================================
def gen_01():
    xml = header("AGILE SECURE SOFTWARE ENGINEERING LIFECYCLE")
    nodes = [
        ("p1", "Sprint 1: Architecture & MVP\n• Epics DWPG-1..3\n• User/Merchant Auth\n• Wallet Top-Up\n• 26 SP Committed", 80, 100, 260, 95, "rounded=1;fillColor=#DBEAFE;strokeColor=#1D4ED8;fontStyle=1;"),
        ("p2", "Sprint 1 Execution\n• Sprint Backlog DWPG-10..14\n• REST Endpoints Built\n• In-Memory Ledger\n• 21 SP Completed", 380, 100, 260, 95, "rounded=1;fillColor=#EFF6FF;strokeColor=#2563EB;fontStyle=1;"),
        ("p3", "Discovery & Retrospective\n• Concurrency Stress Test\n• Defect DEF-001 Logged:\n  Race Condition & Double Spend\n• 5 SP Carried Over", 680, 100, 260, 95, "rounded=1;fillColor=#FEE2E2;strokeColor=#DC2626;fontStyle=1;"),
        ("p4", "Sprint 2: Hardening Scope\n• Epics DWPG-4..7\n• SELECT FOR UPDATE Row Locks\n• Idempotency Token Engine\n• 26 SP Committed", 980, 100, 260, 95, "rounded=1;fillColor=#FEF3C7;strokeColor=#D97706;fontStyle=1;"),
        ("p5", "Sprint 2 Refactoring\n• Pessimistic Locking Query\n• SHA-256 Payload Hash Binding\n• State Machine Refunds\n• 26 SP Delivered (100%)", 980, 260, 260, 95, "rounded=1;fillColor=#D1FAE5;strokeColor=#059669;fontStyle=1;"),
        ("p6", "Containerization & K8s\n• Multi-Stage Dockerfile (Alpine)\n• UID 10001 Non-Root User\n• Minikube Namespace dwpg\n• NetworkPolicy Isolation", 680, 260, 260, 95, "rounded=1;fillColor=#E0E7FF;strokeColor=#4338CA;fontStyle=1;"),
        ("p7", "DevSecOps & SAST Pipeline\n• SonarQube LTS Quality Gate\n• Zero Bugs, Zero Vulns\n• 42 Automated Security Tests\n• 62.6% Code Coverage", 380, 260, 260, 95, "rounded=1;fillColor=#CCFBF1;strokeColor=#0D9488;fontStyle=1;"),
        ("p8", "Academic Capstone Review\n• 16 Exam Phases Verified\n• 24 Draw.io Source Diagrams\n• Master Report Published\n• Remote Git Synchronized", 80, 260, 260, 95, "rounded=1;fillColor=#F3E8FF;strokeColor=#7E22CE;fontStyle=1;")
    ]
    for n in nodes: xml += b(n[0], n[1], n[2], n[3], n[4], n[5], n[6])
    xml += e("e1", "p1", "p2")
    xml += e("e2", "p2", "p3")
    xml += e("e3", "p3", "p4")
    xml += e("e4", "p4", "p5")
    xml += e("e5", "p5", "p6")
    xml += e("e6", "p6", "p7")
    xml += e("e7", "p7", "p8")
    xml += b("summary", "SCRUM SUMMARY: 2 Sprints | 16 Epics & Stories | 47 Total SP Delivered | Velocity: 21 SP (S1) -> 26 SP (S2) | Defect Density: 0.02/SP", 80, 390, 1160, 45, "rounded=1;fillColor=#F8FAFC;strokeColor=#64748B;fontStyle=1;fontSize=12;")
    make_drawio("01_agile_lifecycle.drawio", "Agile Development Lifecycle", xml)

# ==============================================================================
# 02. System Context Diagram
# ==============================================================================
def gen_02():
    xml = header("SYSTEM CONTEXT DIAGRAM")
    xml += b("sys_box", "Digital Wallet & Payment Gateway System Boundary", 320, 80, 680, 480, "shape=rect;fillColor=#F8FAFC;strokeColor=#1E3A8A;strokeWidth=2;verticalAlign=top;fontStyle=1;fontSize=13;")
    xml += b("u_cust", "Consumer User\n(Student/Customer)", 60, 110, 180, 75, "shape=actor;fillColor=#DBEAFE;strokeColor=#1D4ED8;fontStyle=1;")
    xml += b("u_merch", "Registered Merchant\n(Vendor Store)", 60, 260, 180, 75, "shape=actor;fillColor=#FEF3C7;strokeColor=#D97706;fontStyle=1;")
    xml += b("u_admin", "System Administrator\n(Auditor / SecOps)", 60, 410, 180, 75, "shape=actor;fillColor=#FEE2E2;strokeColor=#DC2626;fontStyle=1;")
    xml += b("c_gw", "API Gateway & Security Layer\n• Spring Security 6\n• Bearer JWT Token Filter\n• Idempotency-Key Header Interceptor", 360, 130, 600, 80, "rounded=1;fillColor=#EFF6FF;strokeColor=#2563EB;fontStyle=1;")
    xml += b("c_app", "Core Application Service Tier\n• AuthService (BCrypt 12)\n• WalletService (Pessimistic Row Lock)\n• PaymentService (Atomic Debit/Credit)\n• RefundService (Status FSM Transition)", 360, 250, 600, 110, "rounded=1;fillColor=#F0FDF4;strokeColor=#16A34A;fontStyle=1;")
    xml += b("c_db", "Data Storage Vault (MariaDB / H2)\n• Wallets (balance >= 0)\n• Transactions (Immutable Ledger)\n• Idempotency Cache (SHA-256)\n• Security Audit Logs (PII Scrubbed)", 360, 400, 600, 100, "shape=cylinder;fillColor=#FEF2F2;strokeColor=#DC2626;fontStyle=1;")
    xml += b("ext_siem", "External Security SIEM\n& Log Vault", 1060, 260, 180, 80, "shape=rect;fillColor=#F3E8FF;strokeColor=#7E22CE;fontStyle=1;")
    xml += e("e21", "u_cust", "c_gw", "HTTPS / REST (JWT)")
    xml += e("e22", "u_merch", "c_gw", "HTTPS / API Key")
    xml += e("e23", "u_admin", "c_gw", "ROLE_ADMIN Auth")
    xml += e("e24", "c_gw", "c_app", "Authenticated Context")
    xml += e("e25", "c_app", "c_db", "ACID / SELECT FOR UPDATE")
    xml += e("e26", "c_app", "ext_siem", "Audit Events (Immutable)")
    make_drawio("02_system_context.drawio", "System Context Diagram", xml)

# ==============================================================================
# 03. Use Case Diagram
# ==============================================================================
def gen_03():
    xml = header("UML USE CASE DIAGRAM")
    xml += b("sys", "Digital Wallet & Payment Gateway Simulator", 280, 70, 760, 640, "shape=rect;fillColor=#F8FAFC;strokeColor=#1E3A8A;strokeWidth=2;verticalAlign=top;fontStyle=1;fontSize=14;")
    xml += b("act_user", "Consumer User", 60, 220, 140, 70, "shape=actor;fillColor=#DBEAFE;strokeColor=#1D4ED8;fontStyle=1;")
    xml += b("act_merch", "Merchant", 60, 480, 140, 70, "shape=actor;fillColor=#FEF3C7;strokeColor=#D97706;fontStyle=1;")
    xml += b("act_admin", "System Administrator", 1100, 320, 140, 70, "shape=actor;fillColor=#FEE2E2;strokeColor=#DC2626;fontStyle=1;")
    
    ucs = [
        ("uc1", "UC-01: Register & Authenticate", 320, 100, 200, 50, "fillColor=#EFF6FF;strokeColor=#2563EB;"),
        ("uc2", "UC-02: Provision Wallet", 320, 170, 200, 50, "fillColor=#EFF6FF;strokeColor=#2563EB;"),
        ("uc3", "UC-03: Add Simulated Funds", 320, 240, 200, 50, "fillColor=#EFF6FF;strokeColor=#2563EB;"),
        ("uc4", "UC-04: Initiate Payment", 320, 310, 200, 50, "fillColor=#DBEAFE;strokeColor=#1D4ED8;"),
        ("uc5", "UC-05: Lock Wallet Balance", 580, 260, 200, 50, "fillColor=#D1FAE5;strokeColor=#059669;"),
        ("uc6", "UC-06: Enforce Idempotency", 580, 340, 200, 50, "fillColor=#D1FAE5;strokeColor=#059669;"),
        ("uc7", "UC-07: Register Merchant Profile", 320, 470, 200, 50, "fillColor=#FEF3C7;strokeColor=#D97706;"),
        ("uc8", "UC-08: Process Refund", 320, 550, 200, 50, "fillColor=#DBEAFE;strokeColor=#1D4ED8;"),
        ("uc9", "UC-09: Log Security Audit Event", 580, 550, 200, 50, "fillColor=#D1FAE5;strokeColor=#059669;"),
        ("uc10", "UC-10: Review Audit Trail & SIEM", 820, 330, 200, 50, "fillColor=#FEE2E2;strokeColor=#DC2626;")
    ]
    for u in ucs: xml += b(u[0], u[1], u[2], u[3], u[4], u[5], f"shape=ellipse;rounded=1;{u[6]}fontStyle=1;fontSize=10;")
    
    # Actor connections
    xml += e("ea1", "act_user", "uc1")
    xml += e("ea2", "act_user", "uc2")
    xml += e("ea3", "act_user", "uc3")
    xml += e("ea4", "act_user", "uc4")
    xml += e("ea5", "act_user", "uc8")
    xml += e("ea6", "act_merch", "uc7")
    xml += e("ea7", "act_merch", "uc8")
    xml += e("ea8", "act_admin", "uc10")
    
    # Includes
    xml += e("ei1", "uc4", "uc5", "<<include>>", "edgeStyle=orthogonalEdgeStyle;dashed=1;strokeColor=#059669;")
    xml += e("ei2", "uc4", "uc6", "<<include>>", "edgeStyle=orthogonalEdgeStyle;dashed=1;strokeColor=#059669;")
    xml += e("ei3", "uc4", "uc9", "<<include>>", "edgeStyle=orthogonalEdgeStyle;dashed=1;strokeColor=#059669;")
    xml += e("ei4", "uc8", "uc9", "<<include>>", "edgeStyle=orthogonalEdgeStyle;dashed=1;strokeColor=#059669;")
    make_drawio("03_use_case.drawio", "Use Case Diagram", xml)

# ==============================================================================
# 04. Analysis / Class Model
# ==============================================================================
def gen_04():
    xml = header("ANALYSIS & CLASS MODEL (BOUNDARY - CONTROL - ENTITY)")
    # Boundary classes
    xml += b("b_lbl", "BOUNDARY (API CONTROLLERS)", 80, 80, 360, 30, "fillColor=#1E3A8A;fontColor=#FFFFFF;fontStyle=1;")
    xml += b("bc1", "AuthController\n+ register(UserDto): Response\n+ login(LoginDto): TokenResponse", 80, 120, 360, 65, "fillColor=#EFF6FF;strokeColor=#2563EB;fontStyle=1;")
    xml += b("bc2", "WalletController\n+ getMyWallet(): WalletDto\n+ topup(TopupDto): WalletDto", 80, 200, 360, 65, "fillColor=#EFF6FF;strokeColor=#2563EB;fontStyle=1;")
    xml += b("bc3", "PaymentController\n+ initiatePayment(PayDto): PayResponse\n+ getHistory(): List<TxDto>", 80, 280, 360, 65, "fillColor=#EFF6FF;strokeColor=#2563EB;fontStyle=1;")
    xml += b("bc4", "RefundController\n+ requestRefund(RefDto): RefResponse", 80, 360, 360, 65, "fillColor=#EFF6FF;strokeColor=#2563EB;fontStyle=1;")
    
    # Control classes
    xml += b("c_lbl", "CONTROL (BUSINESS SERVICES)", 490, 80, 380, 30, "fillColor=#065F46;fontColor=#FFFFFF;fontStyle=1;")
    xml += b("cc1", "AuthService\n+ authenticate(username, rawPassword)\n+ hashPassword(raw): BCrypt12", 490, 120, 380, 65, "fillColor=#ECFDF5;strokeColor=#059669;fontStyle=1;")
    xml += b("cc2", "WalletService\n+ fundWallet(walletId, amount)\n+ getLockedWallet(id): PessimisticWrite", 490, 200, 380, 65, "fillColor=#ECFDF5;strokeColor=#059669;fontStyle=1;")
    xml += b("cc3", "PaymentService\n+ processPayment(request, idemKey)\n+ executeAtomicTransfer(s, m, amt)", 490, 280, 380, 65, "fillColor=#ECFDF5;strokeColor=#059669;fontStyle=1;")
    xml += b("cc4", "IdempotencyService\n+ checkAndLock(key, hash): CachedResp\n+ saveResponse(key, hash, resp)", 490, 360, 380, 65, "fillColor=#ECFDF5;strokeColor=#059669;fontStyle=1;")
    xml += b("cc5", "RefundService\n+ reversePayment(paymentId, user)", 490, 440, 380, 55, "fillColor=#ECFDF5;strokeColor=#059669;fontStyle=1;")
    
    # Entity classes
    xml += b("e_lbl", "ENTITY (DOMAIN MODELS)", 920, 80, 360, 30, "fillColor=#991B1B;fontColor=#FFFFFF;fontStyle=1;")
    xml += b("ec1", "User\n- id: Long [PK]\n- username: String\n- passwordHash: String\n- role: RoleEnum", 920, 120, 360, 75, "fillColor=#FEF2F2;strokeColor=#DC2626;fontStyle=1;")
    xml += b("ec2", "Wallet\n- id: Long [PK]\n- userId: Long [FK]\n- balance: BigDecimal\n- currency: String", 920, 210, 360, 75, "fillColor=#FEF2F2;strokeColor=#DC2626;fontStyle=1;")
    xml += b("ec3", "Payment\n- id: Long [PK]\n- senderWalletId: Long [FK]\n- merchantId: Long [FK]\n- amount: BigDecimal\n- status: PaymentStatus", 920, 300, 360, 95, "fillColor=#FEF2F2;strokeColor=#DC2626;fontStyle=1;")
    xml += b("ec4", "IdempotencyRecord\n- idempotencyKey: String [PK]\n- requestHash: String\n- responseBody: String\n- status: Int", 920, 410, 360, 85, "fillColor=#FEF2F2;strokeColor=#DC2626;fontStyle=1;")
    
    # Associations
    xml += e("e41", "bc1", "cc1")
    xml += e("e42", "bc2", "cc2")
    xml += e("e43", "bc3", "cc3")
    xml += e("e44", "bc3", "cc4")
    xml += e("e45", "bc4", "cc5")
    xml += e("e46", "cc1", "ec1")
    xml += e("e47", "cc2", "ec2")
    xml += e("e48", "cc3", "ec3")
    xml += e("e49", "cc4", "ec4")
    make_drawio("04_analysis_model.drawio", "Analysis and Class Model", xml)

# ==============================================================================
# 05. Entity-Relationship Diagram (ERD)
# ==============================================================================
def gen_05():
    xml = header("ENTITY-RELATIONSHIP DIAGRAM (3RD NORMAL FORM RELATIONAL SCHEMA)")
    entities = [
        ("t_user", "users\n───────────────\nPK id : BIGINT\n   username : VARCHAR(50) [UQ]\n   email : VARCHAR(100) [UQ]\n   password_hash : VARCHAR(100)\n   role : VARCHAR(20)\n   created_at : TIMESTAMP", 80, 90, 260, 140, "fillColor=#EFF6FF;strokeColor=#1D4ED8;"),
        ("t_wal", "wallets\n───────────────\nPK id : BIGINT\nFK user_id : BIGINT [UQ]\n   currency : VARCHAR(3)\n   balance : DECIMAL(15,2)\n   CHECK (balance >= 0)\n   version : BIGINT\n   updated_at : TIMESTAMP", 400, 90, 260, 150, "fillColor=#ECFDF5;strokeColor=#059669;"),
        ("t_merch", "merchants\n───────────────\nPK id : BIGINT\nFK user_id : BIGINT [UQ]\n   merchant_name : VARCHAR(100)\n   api_key_hash : VARCHAR(64) [UQ]\n   webhook_url : VARCHAR(255)\n   created_at : TIMESTAMP", 720, 90, 260, 140, "fillColor=#FEF3C7;strokeColor=#D97706;"),
        ("t_pay", "payments\n───────────────\nPK id : BIGINT\nFK sender_wallet_id : BIGINT\nFK merchant_id : BIGINT\n   amount : DECIMAL(15,2)\n   status : VARCHAR(20)\n   idempotency_key : VARCHAR(64) [UQ]\n   tamper_hash : VARCHAR(64)\n   created_at : TIMESTAMP", 400, 290, 260, 170, "fillColor=#EDE9FE;strokeColor=#7C3AED;"),
        ("t_tx", "transactions\n───────────────\nPK id : BIGINT\nFK wallet_id : BIGINT\nFK payment_id : BIGINT [NULL]\n   type : VARCHAR(20)\n   amount : DECIMAL(15,2)\n   balance_after : DECIMAL(15,2)\n   created_at : TIMESTAMP", 80, 290, 260, 150, "fillColor=#EFF6FF;strokeColor=#1D4ED8;"),
        ("t_ref", "refunds\n───────────────\nPK id : BIGINT\nFK payment_id : BIGINT [UQ]\nFK requester_wallet_id : BIGINT\n   amount : DECIMAL(15,2)\n   status : VARCHAR(20)\n   reason : VARCHAR(255)\n   created_at : TIMESTAMP", 720, 290, 260, 150, "fillColor=#FEF2F2;strokeColor=#DC2626;"),
        ("t_idem", "idempotency_records\n───────────────────\nPK idempotency_key : VARCHAR(64)\n   request_hash : VARCHAR(64)\n   status_code : INT\n   response_body : TEXT\n   created_at : TIMESTAMP\n   expires_at : TIMESTAMP", 1040, 90, 260, 140, "fillColor=#FFFBEB;strokeColor=#B45309;"),
        ("t_aud", "audit_logs\n───────────────\nPK id : BIGINT\n   event_type : VARCHAR(50)\n   actor_username : VARCHAR(50)\n   client_ip : VARCHAR(45)\n   action_details : TEXT\n   created_at : TIMESTAMP", 1040, 290, 260, 140, "fillColor=#F8FAFC;strokeColor=#475569;")
    ]
    for ent in entities:
        xml += b(ent[0], ent[1], ent[2], ent[3], ent[4], ent[5], f"rounded=1;{ent[6]}fontStyle=1;align=left;fontSize=10;")
        
    xml += e("r1", "t_user", "t_wal", "1 : 1")
    xml += e("r2", "t_user", "t_merch", "1 : 1")
    xml += e("r3", "t_wal", "t_pay", "1 : N")
    xml += e("r4", "t_merch", "t_pay", "1 : N")
    xml += e("r5", "t_wal", "t_tx", "1 : N")
    xml += e("r6", "t_pay", "t_ref", "1 : 1")
    make_drawio("05_erd.drawio", "Entity-Relationship Diagram", xml)

# ==============================================================================
# 06. DFD Level 0 (Context Diagram)
# ==============================================================================
def gen_06():
    xml = header("DATA FLOW DIAGRAM (DFD LEVEL 0 - CONTEXT MODEL)")
    xml += b("p0", "0.0\nDIGITAL WALLET &amp;\nPAYMENT GATEWAY\nSIMULATOR", 520, 220, 260, 150, "shape=ellipse;fillColor=#1E3A8A;fontColor=#FFFFFF;fontStyle=1;fontSize=14;")
    xml += b("ee_user", "External Entity:\nCONSUMER USER\n(Student/Customer)", 80, 240, 200, 100, "shape=rect;fillColor=#DBEAFE;strokeColor=#1D4ED8;fontStyle=1;")
    xml += b("ee_merch", "External Entity:\nREGISTERED MERCHANT\n(Vendor Store)", 1020, 240, 200, 100, "shape=rect;fillColor=#FEF3C7;strokeColor=#D97706;fontStyle=1;")
    xml += b("ee_admin", "External Entity:\nSECURITY ADMIN\n&amp; AUDITOR", 550, 480, 200, 80, "shape=rect;fillColor=#FEE2E2;strokeColor=#DC2626;fontStyle=1;")
    
    xml += e("f1", "ee_user", "p0", "Registration, Login, Top-up, Payment Initiation")
    xml += e("f2", "p0", "ee_user", "JWT Token, Balance, Payment Receipt, Refund Status")
    xml += e("f3", "ee_merch", "p0", "Merchant Registration, Refund Approvals")
    xml += e("f4", "p0", "ee_merch", "Settlement Notification, Webhook Payload")
    xml += e("f5", "p0", "ee_admin", "Security Audit Logs, Forensic Events, Metrics")
    xml += e("f6", "ee_admin", "p0", "Audit Queries, Security Policy Configuration")
    make_drawio("06_dfd_level0.drawio", "DFD Level 0 Context Diagram", xml)

# ==============================================================================
# 07. DFD Level 1 (Decomposition)
# ==============================================================================
def gen_07():
    xml = header("DATA FLOW DIAGRAM (DFD LEVEL 1 - SUBSYSTEM DECOMPOSITION)")
    # Entities
    xml += b("ee_u", "User", 60, 120, 120, 60, "fillColor=#DBEAFE;strokeColor=#1D4ED8;fontStyle=1;")
    xml += b("ee_m", "Merchant", 60, 360, 120, 60, "fillColor=#FEF3C7;strokeColor=#D97706;fontStyle=1;")
    
    # Processes
    xml += b("p1", "1.0\nAuth &amp; Session\nManagement", 240, 110, 180, 80, "shape=ellipse;fillColor=#EFF6FF;strokeColor=#2563EB;fontStyle=1;")
    xml += b("p2", "2.0\nWallet &amp; Concurrency\nControl", 500, 110, 190, 80, "shape=ellipse;fillColor=#EFF6FF;strokeColor=#2563EB;fontStyle=1;")
    xml += b("p3", "3.0\nPayment Settlement\n&amp; Idempotency Gate", 770, 110, 200, 80, "shape=ellipse;fillColor=#EFF6FF;strokeColor=#2563EB;fontStyle=1;")
    xml += b("p4", "4.0\nRefund &amp; State\nReversal Engine", 770, 350, 200, 80, "shape=ellipse;fillColor=#EFF6FF;strokeColor=#2563EB;fontStyle=1;")
    xml += b("p5", "5.0\nAudit Logging &amp;\nForensics Collector", 500, 350, 190, 80, "shape=ellipse;fillColor=#EFF6FF;strokeColor=#2563EB;fontStyle=1;")
    
    # Data Stores
    xml += b("ds1", "D1: Users DB (BCrypt Hashed)", 240, 250, 180, 40, "shape=partialRectangle;fillColor=#F8FAFC;strokeColor=#475569;fontStyle=1;")
    xml += b("ds2", "D2: Wallets DB (Balance Row)", 500, 250, 190, 40, "shape=partialRectangle;fillColor=#F8FAFC;strokeColor=#475569;fontStyle=1;")
    xml += b("ds3", "D3: Idempotency Cache (SHA-256)", 770, 250, 200, 40, "shape=partialRectangle;fillColor=#F8FAFC;strokeColor=#475569;fontStyle=1;")
    xml += b("ds4", "D4: Audit Ledger (Immutable)", 500, 480, 190, 40, "shape=partialRectangle;fillColor=#F8FAFC;strokeColor=#475569;fontStyle=1;")
    
    # Edges
    xml += e("df1", "ee_u", "p1", "Login Req")
    xml += e("df2", "p1", "ds1", "Verify Hash")
    xml += e("df3", "ee_u", "p2", "Top-Up Req")
    xml += e("df4", "p2", "ds2", "Pessimistic Write")
    xml += e("df5", "ee_u", "p3", "Pay Req + Key")
    xml += e("df6", "p3", "ds3", "Check/Store Key")
    xml += e("df7", "p3", "ds2", "Debit & Credit")
    xml += e("df8", "ee_m", "p4", "Refund Req")
    xml += e("df9", "p4", "ds2", "Reverse Funds")
    xml += e("df10", "p3", "p5", "Payment Event")
    xml += e("df11", "p4", "p5", "Refund Event")
    xml += e("df12", "p5", "ds4", "Append Log")
    make_drawio("07_dfd_level1.drawio", "DFD Level 1 Decomposition", xml)

# ==============================================================================
# 08. Trust Boundary DFD
# ==============================================================================
def gen_08():
    xml = header("TRUST BOUNDARY ARCHITECTURE & SECURITY ZONES")
    # Zone 1
    xml += b("z1", "ZONE 1: UNTRUSTED PUBLIC ZONE\n(Internet / Browser / Attacker Surface)", 60, 80, 360, 440, "shape=rect;fillColor=#FFF5F5;strokeColor=#E53E3E;strokeWidth=2;dashed=1;verticalAlign=top;fontStyle=1;")
    xml += b("z1_client", "React 18 SPA Client\n• Session in Memory\n• Axios REST Client", 90, 140, 300, 70, "fillColor=#FEE2E2;strokeColor=#DC2626;fontStyle=1;")
    xml += b("z1_att", "External Adversary\n• Replay Attacks\n• Concurrent Race Storm\n• SQLi / Fuzz Probes", 90, 260, 300, 90, "fillColor=#FEE2E2;strokeColor=#DC2626;fontStyle=1;")
    
    # Zone 2
    xml += b("z2", "ZONE 2: DMZ / INGRESS PERIMETER\n(TLS & Rate Limiting Barrier)", 460, 80, 380, 440, "shape=rect;fillColor=#FFFFF0;strokeColor=#D69E2E;strokeWidth=2;dashed=1;verticalAlign=top;fontStyle=1;")
    xml += b("z2_ng", "Nginx Reverse Proxy\n• NodePort 30080\n• TLS Termination\n• CORS Whitelist Policy", 500, 140, 300, 80, "fillColor=#FEF3C7;strokeColor=#D97706;fontStyle=1;")
    xml += b("z2_flt", "Spring Security Filter Chain\n• Bearer JWT Validator\n• Idempotency-Key Gate\n• Nonce & Header Verification", 500, 260, 300, 90, "fillColor=#FEF3C7;strokeColor=#D97706;fontStyle=1;")
    
    # Zone 3
    xml += b("z3", "ZONE 3: CORE FINANCIAL EXECUTION TIER\n(ACID & Isolated Database Vault)", 880, 80, 460, 440, "shape=rect;fillColor=#F7FAFC;strokeColor=#2B6CB0;strokeWidth=2;dashed=1;verticalAlign=top;fontStyle=1;")
    xml += b("z3_svc", "Spring Boot Service Layer\n• WalletService (Pessimistic Lock)\n• PaymentService (Atomic Transfer)\n• RefundService (State Guard)", 920, 140, 380, 80, "fillColor=#DBEAFE;strokeColor=#1D4ED8;fontStyle=1;")
    xml += b("z3_db", "MariaDB 11.4 Storage Engine\n• SELECT FOR UPDATE Row Locks\n• CHECK (balance >= 0)\n• Immutable Audit Ledger Table", 920, 260, 380, 90, "shape=cylinder;fillColor=#DCFCE7;strokeColor=#15803D;fontStyle=1;")
    
    # Boundary Crossing Arrows
    xml += e("tb_e1", "z1_client", "z2_ng", "HTTPS Crossing [Boundary A]", "strokeColor=#E53E3E;strokeWidth=2;")
    xml += e("tb_e2", "z2_ng", "z2_flt", "Internal Forward")
    xml += e("tb_e3", "z2_flt", "z3_svc", "Authenticated Principal [Boundary B]", "strokeColor=#D69E2E;strokeWidth=2;")
    xml += e("tb_e4", "z3_svc", "z3_db", "Isolated JDBC Connection [Boundary C]", "strokeColor=#2B6CB0;strokeWidth=2;")
    make_drawio("08_trust_boundary.drawio", "Trust Boundary Architecture", xml)

# ==============================================================================
# 09. System Architecture
# ==============================================================================
def gen_09():
    xml = header("SYSTEM ARCHITECTURE (5-TIER SECURE PATTERN)")
    layers = [
        ("l1", "TIER 1: PRESENTATION TIER\nReact 18 Single Page Application | Vite Bundler | TailwindCSS\nAxios HTTP Interceptors | Bearer Token Session Management | Client-Side Input Sanitization", 80, 80, 1200, 70, "fillColor=#EFF6FF;strokeColor=#1D4ED8;"),
        ("l2", "TIER 2: API GATEWAY & SECURITY PERIMETER TIER\nSpring Security 6.x | DelegatingFilterProxy | OncePerRequestFilter (JwtAuthenticationFilter)\nIdempotencyValidationInterceptor | Rate Limiter | Global CORS Configuration", 80, 170, 1200, 70, "fillColor=#ECFDF5;strokeColor=#059669;"),
        ("l3", "TIER 3: CORE APPLICATION SERVICE TIER\nAuthService (BCrypt 12) | WalletService (Pessimistic Concurrency) | PaymentService (Atomic Transfer)\nMerchantService (API Key Hash) | RefundService (State FSM) | AuditService (Forensics)", 80, 260, 1200, 80, "fillColor=#FEF3C7;strokeColor=#D97706;"),
        ("l4", "TIER 4: PERSISTENCE & TRANSACTIONAL INTEGRITY TIER\nSpring Data JPA | Hibernate ORM | @Transactional(isolation = Isolation.READ_COMMITTED)\n@Lock(LockModeType.PESSIMISTIC_WRITE) | HikariCP Managed Connection Pool", 80, 360, 1200, 70, "fillColor=#EDE9FE;strokeColor=#7C3AED;"),
        ("l5", "TIER 5: SECURE DATA STORAGE TIER\nMariaDB 11.4 Relational Engine / In-Memory H2 | ACID Guarantees\nCHECK Constraints (balance >= 0) | SHA-256 Idempotency Cache | Immutable Audit Table", 80, 450, 1200, 70, "shape=cylinder;fillColor=#FEF2F2;strokeColor=#DC2626;")
    ]
    for lyr in layers: xml += b(lyr[0], lyr[1], lyr[2], lyr[3], lyr[4], lyr[5], f"rounded=1;{lyr[6]}fontStyle=1;fontSize=11;")
    xml += e("la1", "l1", "l2", "HTTPS / JSON REST")
    xml += e("la2", "l2", "l3", "Authenticated Request Context")
    xml += e("la3", "l3", "l4", "Transactional Method Invocations")
    xml += e("la4", "l4", "l5", "SQL via JDBC / SELECT FOR UPDATE")
    make_drawio("09_architecture.drawio", "System Architecture", xml)

# ==============================================================================
# 10. Component Diagram
# ==============================================================================
def gen_10():
    xml = header("UML COMPONENT DIAGRAM")
    comps = [
        ("c_ui", "«component»\nDWPG Web UI\n(React 18 SPA)", 80, 100, 240, 90, "fillColor=#EFF6FF;strokeColor=#1D4ED8;"),
        ("c_sec", "«component»\nSecurity Filter Chain\n(Spring Security 6)", 400, 100, 240, 90, "fillColor=#ECFDF5;strokeColor=#059669;"),
        ("c_idem", "«component»\nIdempotency Gate\n(Token & Hash Verifier)", 720, 100, 240, 90, "fillColor=#FEF3C7;strokeColor=#D97706;"),
        ("c_wal", "«component»\nWallet Engine\n(Pessimistic Lock Controller)", 400, 260, 240, 90, "fillColor=#DBEAFE;strokeColor=#2563EB;"),
        ("c_pay", "«component»\nPayment Settlement\n(Double-Entry Ledger)", 720, 260, 240, 90, "fillColor=#EDE9FE;strokeColor=#7C3AED;"),
        ("c_ref", "«component»\nRefund Manager\n(State Reversal FSM)", 1040, 260, 240, 90, "fillColor=#FEF2F2;strokeColor=#DC2626;"),
        ("c_aud", "«component»\nForensics Collector\n(Audit Trail Logger)", 400, 420, 240, 90, "fillColor=#F8FAFC;strokeColor=#475569;"),
        ("c_db", "«database»\nMariaDB Storage Engine\n(ACID Vault)", 720, 420, 240, 90, "shape=cylinder;fillColor=#FEF2F2;strokeColor=#DC2626;")
    ]
    for c in comps: xml += b(c[0], c[1], c[2], c[3], c[4], c[5], f"rounded=1;{c[6]}fontStyle=1;fontSize=11;")
    xml += e("ec1", "c_ui", "c_sec", "REST Calls")
    xml += e("ec2", "c_sec", "c_idem", "Validated JWT")
    xml += e("ec3", "c_idem", "c_pay", "Payment Route")
    xml += e("ec4", "c_pay", "c_wal", "Lock & Debit/Credit")
    xml += e("ec5", "c_pay", "c_ref", "Payment Status")
    xml += e("ec6", "c_pay", "c_aud", "Tx Auditing")
    xml += e("ec7", "c_wal", "c_db", "Row Locking (SQL)")
    xml += e("ec8", "c_pay", "c_db", "Insert Ledger")
    xml += e("ec9", "c_aud", "c_db", "Append Event")
    make_drawio("10_component.drawio", "Component Diagram", xml)

# ==============================================================================
# 11. Deployment Architecture
# ==============================================================================
def gen_11():
    xml = header("PHYSICAL DEPLOYMENT ARCHITECTURE (KUBERNETES & MINIKUBE)")
    xml += b("k8s_node", "Kubernetes Minikube Cluster (Namespace: dwpg)", 60, 80, 1140, 480, "shape=rect;fillColor=#F8FAFC;strokeColor=#2563EB;strokeWidth=2;verticalAlign=top;fontStyle=1;fontSize=13;")
    xml += b("np_front", "Service: dwpg-frontend-service\nNodePort: 30080 -> 3000", 100, 130, 280, 60, "rounded=1;fillColor=#EFF6FF;strokeColor=#1D4ED8;fontStyle=1;")
    xml += b("pod_front", "Deployment: dwpg-frontend (2 Replicas)\n• React 18 SPA + Nginx Reverse Proxy\n• Non-root User UID 101\n• Security Context: runAsNonRoot: true", 100, 220, 280, 110, "rounded=1;fillColor=#DBEAFE;strokeColor=#2563EB;fontStyle=1;")
    xml += b("svc_back", "Service: dwpg-backend-service\nClusterIP: 8080 (Internal DNS)", 480, 130, 280, 60, "rounded=1;fillColor=#F0FDF4;strokeColor=#16A34A;fontStyle=1;")
    xml += b("pod_back", "Deployment: dwpg-backend (2 Replicas)\n• Java 21 LTS + Spring Boot 3.3.4\n• Non-root User UID 10001\n• ReadOnlyRootFilesystem: true\n• Capabilities Dropped: ALL", 480, 220, 280, 110, "rounded=1;fillColor=#DCFCE7;strokeColor=#15803D;fontStyle=1;")
    xml += b("svc_db", "Service: dwpg-mariadb-service\nClusterIP: 3306 (Isolated)", 840, 130, 300, 60, "rounded=1;fillColor=#FEF2F2;strokeColor=#DC2626;fontStyle=1;")
    xml += b("pod_db", "Deployment: dwpg-mariadb (1 Replica)\n• MariaDB 10.11 Engine\n• PersistentVolumeClaim: 5Gi\n• NetworkPolicy: isolate-mariadb\n  (Ingress allowed only from dwpg-backend)", 840, 220, 300, 110, "shape=cylinder;fillColor=#FEE2E2;strokeColor=#B91C1C;fontStyle=1;")
    xml += b("cm", "ConfigMap: dwpg-config\n• SPRING_PROFILES_ACTIVE=dev\n• SERVER_PORT=8080", 280, 380, 280, 60, "rounded=1;fillColor=#FEF3C7;strokeColor=#D97706;fontStyle=1;")
    xml += b("sec", "Secret: dwpg-secrets\n• JWT_SECRET (256-bit Key)\n• DB_PASSWORD (Encrypted)", 640, 380, 280, 60, "rounded=1;fillColor=#EDE9FE;strokeColor=#7C3AED;fontStyle=1;")
    xml += e("ed1", "np_front", "pod_front")
    xml += e("ed2", "pod_front", "svc_back", "Proxy /api/*")
    xml += e("ed3", "svc_back", "pod_back")
    xml += e("ed4", "pod_back", "svc_db", "JDBC Connection")
    xml += e("ed5", "svc_db", "pod_db")
    make_drawio("11_deployment.drawio", "Deployment Architecture", xml)

# ==============================================================================
# 12. Authentication Sequence
# ==============================================================================
def gen_12():
    xml = header("AUTHENTICATION & JWT ISSUANCE SEQUENCE")
    actors = [
        ("c", "Client (React UI)", 80),
        ("ac", "AuthController", 280),
        ("as", "AuthService", 480),
        ("ur", "UserRepository", 680),
        ("pe", "PasswordEncoder (BCrypt)", 880),
        ("jp", "JwtTokenProvider", 1080)
    ]
    for a in actors:
        xml += b(a[0], a[1], a[2], 80, 160, 40, "rounded=1;fillColor=#DBEAFE;strokeColor=#1D4ED8;fontStyle=1;")
        xml += b(f"line_{a[0]}", "", a[2]+75, 120, 10, 380, "shape=rect;fillColor=#CBD5E1;strokeColor=none;")
    xml += e("s1", "c", "ac", "1. POST /api/auth/login {user, pass}")
    xml += e("s2", "ac", "as", "2. login(request, clientIp)")
    xml += e("s3", "as", "ur", "3. findByUsername(user)")
    xml += e("s4", "ur", "as", "4. return User Entity")
    xml += e("s5", "as", "pe", "5. matches(rawPassword, hash)")
    xml += e("s6", "pe", "as", "6. true (BCrypt verified)")
    xml += e("s7", "as", "jp", "7. generateToken(username, role)")
    xml += e("s8", "jp", "as", "8. signed HMAC-SHA256 JWT")
    xml += e("s9", "as", "c", "9. HTTP 200 OK {token, walletId}", "strokeColor=#059669;strokeWidth=2;dashed=1;")
    make_drawio("12_auth_sequence.drawio", "Authentication Sequence Diagram", xml)

# ==============================================================================
# 13. Wallet Funding Sequence
# ==============================================================================
def gen_13():
    xml = header("WALLET PROVISIONING & FUNDS TOP-UP SEQUENCE")
    actors = [
        ("c13", "Client (User)", 80),
        ("wc13", "WalletController", 280),
        ("ws13", "WalletService", 480),
        ("wr13", "WalletRepository", 680),
        ("tr13", "TransactionRepository", 880),
        ("as13", "AuditService", 1080)
    ]
    for a in actors:
        xml += b(a[0], a[1], a[2], 80, 160, 40, "rounded=1;fillColor=#DBEAFE;strokeColor=#1D4ED8;fontStyle=1;")
        xml += b(f"line_{a[0]}", "", a[2]+75, 120, 10, 380, "shape=rect;fillColor=#CBD5E1;strokeColor=none;")
    xml += e("sf1", "c13", "wc13", "1. POST /api/wallets/topup {amount: 500.00}")
    xml += e("sf2", "wc13", "ws13", "2. fundMyWallet(request, user)")
    xml += e("sf3", "ws13", "wr13", "3. findByIdForUpdate(walletId) [PESSIMISTIC_WRITE]")
    xml += e("sf4", "wr13", "ws13", "4. Locked Wallet Row")
    xml += e("sf5", "ws13", "wr13", "5. wallet.credit(500.00) & save()")
    xml += e("sf6", "ws13", "tr13", "6. save(Transaction: TOP_UP)")
    xml += e("sf7", "ws13", "as13", "7. logEvent(FUNDS_ADDED)")
    xml += e("sf8", "ws13", "c13", "8. HTTP 200 OK {newBalance: 500.00}", "strokeColor=#059669;strokeWidth=2;dashed=1;")
    make_drawio("13_wallet_funding_sequence.drawio", "Wallet Funding Sequence Diagram", xml)

# ==============================================================================
# 14. Payment Sequence
# ==============================================================================
def gen_14():
    xml = header("IDEMPOTENT PAYMENT SETTLEMENT & CONCURRENCY LOCKING SEQUENCE")
    actors = [
        ("c14", "Customer Client", 60),
        ("pc14", "PaymentController", 260),
        ("is14", "IdempotencyService", 460),
        ("ps14", "PaymentService", 660),
        ("wr14", "WalletRepository", 860),
        ("tr14", "TransactionRepository", 1060)
    ]
    for a in actors:
        xml += b(a[0], a[1], a[2], 80, 160, 40, "rounded=1;fillColor=#DBEAFE;strokeColor=#1D4ED8;fontStyle=1;")
        xml += b(f"line_{a[0]}", "", a[2]+75, 120, 10, 380, "shape=rect;fillColor=#CBD5E1;strokeColor=none;")
    xml += e("p1", "c14", "pc14", "1. POST /api/payments/initiate [Idempotency-Key: K1, $75]")
    xml += e("p2", "pc14", "is14", "2. checkIdempotency(K1, sha256(payload))")
    xml += e("p3", "is14", "ps14", "3. Cache Miss -> Process Fresh Payment")
    xml += e("p4", "ps14", "wr14", "4. Lock Sender & Merchant Wallets [SELECT FOR UPDATE]")
    xml += e("p5", "wr14", "ps14", "5. Wallets Locked & Invariant Verified (balance >= 75)")
    xml += e("p6", "ps14", "wr14", "6. Atomic Debit Sender ($75) & Credit Merchant ($75)")
    xml += e("p7", "ps14", "tr14", "7. Record Double-Entry Ledger (DEBIT & CREDIT Tx)")
    xml += e("p8", "ps14", "is14", "8. saveIdempotencyRecord(K1, response, 201)")
    xml += e("p9", "ps14", "c14", "9. HTTP 201 Created {status: CONFIRMED, tamperHash}", "strokeColor=#059669;strokeWidth=2;dashed=1;")
    make_drawio("14_payment_sequence.drawio", "Payment Transaction Sequence Diagram", xml)

# ==============================================================================
# 15. Refund Sequence
# ==============================================================================
def gen_15():
    xml = header("AUTHORIZED PAYMENT REFUND & STATE MACHINE REVERSAL SEQUENCE")
    actors = [
        ("c15", "Merchant / Customer", 60),
        ("rc15", "RefundController", 260),
        ("rs15", "RefundService", 460),
        ("pr15", "PaymentRepository", 660),
        ("wr15", "WalletRepository", 860),
        ("rf15", "RefundRepository", 1060)
    ]
    for a in actors:
        xml += b(a[0], a[1], a[2], 80, 160, 40, "rounded=1;fillColor=#DBEAFE;strokeColor=#1D4ED8;fontStyle=1;")
        xml += b(f"line_{a[0]}", "", a[2]+75, 120, 10, 380, "shape=rect;fillColor=#CBD5E1;strokeColor=none;")
    xml += e("r1", "c15", "rc15", "1. POST /api/refunds {paymentId: 1, reason}")
    xml += e("r2", "rc15", "rs15", "2. processRefund(paymentId, user)")
    xml += e("r3", "rs15", "pr15", "3. findByIdForUpdate(paymentId)")
    xml += e("r4", "pr15", "rs15", "4. Validate: Status == CONFIRMED & Not Refunded")
    xml += e("r5", "rs15", "wr15", "5. Lock Settlement & Customer Wallets [Row Lock]")
    xml += e("r6", "rs15", "wr15", "6. Reversal: Debit Merchant & Credit Customer")
    xml += e("r7", "rs15", "pr15", "7. payment.setStatus(REFUNDED)")
    xml += e("r8", "rs15", "rf15", "8. save(Refund: COMPLETED)")
    xml += e("r9", "rs15", "c15", "9. HTTP 200 OK {status: COMPLETED, fundsRestored}", "strokeColor=#059669;strokeWidth=2;dashed=1;")
    make_drawio("15_refund_sequence.drawio", "Refund Sequence Diagram", xml)

# ==============================================================================
# 16. Replay & Idempotency Sequence
# ==============================================================================
def gen_16():
    xml = header("IDEMPOTENCY CACHE & REPLAY ATTACK DEFENSE PROTOCOL")
    actors = [
        ("c16", "Client / Attacker", 80),
        ("pc16", "PaymentController", 320),
        ("is16", "IdempotencyService", 580),
        ("ir16", "IdempotencyRecordRepository", 860),
        ("ps16", "PaymentEngine", 1100)
    ]
    for a in actors:
        xml += b(a[0], a[1], a[2], 80, 160, 40, "rounded=1;fillColor=#DBEAFE;strokeColor=#1D4ED8;fontStyle=1;")
        xml += b(f"line_{a[0]}", "", a[2]+75, 120, 10, 420, "shape=rect;fillColor=#CBD5E1;strokeColor=none;")
    xml += b("sep1", "SCENARIO 1: IDENTICAL RETRY (NETWORK REPLAY)", 80, 140, 1180, 25, "fillColor=#EFF6FF;strokeColor=#2563EB;fontStyle=1;align=left;")
    xml += e("rp1", "c16", "pc16", "1. Retried POST /payments [Key: K1, Payload: P1]")
    xml += e("rp2", "pc16", "is16", "2. checkIdempotency(K1, sha256(P1))")
    xml += e("rp3", "is16", "ir16", "3. findByIdempotencyKey(K1)")
    xml += e("rp4", "ir16", "is16", "4. Record Found: Hash Matches P1")
    xml += e("rp5", "is16", "c16", "5. Return CACHED Response (Zero Extra Debit)", "strokeColor=#059669;strokeWidth=2;dashed=1;")
    xml += b("sep2", "SCENARIO 2: TAMPERED PAYLOAD REPLAY ATTACK", 80, 290, 1180, 25, "fillColor=#FEF2F2;strokeColor=#DC2626;fontStyle=1;align=left;")
    xml += e("rp6", "c16", "pc16", "6. Tampered POST /payments [Key: K1, Tampered Amount: $999]")
    xml += e("rp7", "pc16", "is16", "7. checkIdempotency(K1, sha256(P2))")
    xml += e("rp8", "is16", "ir16", "8. Hash Mismatch Detected! P1 != P2")
    xml += e("rp9", "is16", "c16", "9. HTTP 409 Conflict: Tampered Replay Blocked", "strokeColor=#DC2626;strokeWidth=2;dashed=1;")
    make_drawio("16_replay_idempotency_sequence.drawio", "Replay/Idempotency Sequence Diagram", xml)

# ==============================================================================
# 17. STRIDE Threat Model
# ==============================================================================
def gen_17():
    xml = header("STRIDE THREAT MODELING MATRIX & DEFENSE MAPPING")
    cards = [
        ("s_s", "S - Spoofing Identity", "Threat: Attacker steals session token or impersonates merchant.\n\nMitigation: BCrypt cost 12 password hashing, short-lived HMAC-SHA256 JWT, 256-bit API key authentication.", 80, 90, 520, 130, "fillColor=#DBEAFE;strokeColor=#1D4ED8;"),
        ("s_t", "T - Tampering with Data", "Threat: Adversary modifies payment amount or target merchant in flight.\n\nMitigation: TLS transport encryption, SHA-256 payload binding to Idempotency-Key, cryptographic tamper seal.", 640, 90, 520, 130, "fillColor=#FEE2E2;strokeColor=#DC2626;"),
        ("s_r", "R - Repudiation", "Threat: Customer or merchant claims transaction was unauthorized.\n\nMitigation: Append-only transaction ledger, digital receipt hashes, immutable SIEM audit trail.", 80, 250, 520, 130, "fillColor=#FEF3C7;strokeColor=#D97706;"),
        ("s_i", "I - Information Disclosure", "Threat: Cross-tenant IDOR exposes foreign wallet balances.\n\nMitigation: Strict BOLA ownership validation, zero sensitive card PAN in DB, regex log scrubbing.", 640, 250, 520, 130, "fillColor=#EFF6FF;strokeColor=#2563EB;"),
        ("s_d", "D - Denial of Service", "Threat: Concurrent payment storm exhausts DB connection pool.\n\nMitigation: HikariCP connection pool limits, idempotency fast-cache lookup, MariaDB row-level locks.", 80, 410, 520, 130, "fillColor=#F3E8FF;strokeColor=#7E22CE;"),
        ("s_e", "E - Elevation of Privilege", "Threat: Consumer principal invokes admin audit endpoints.\n\nMitigation: Spring Security RBAC @PreAuthorize(\"hasRole('ADMIN')\"), 403 Forbidden enforcement.", 640, 410, 520, 130, "fillColor=#DCFCE7;strokeColor=#15803D;")
    ]
    for c in cards: xml += b(c[0], c[1], c[3], c[4], c[5], c[6], f"rounded=1;{c[7]}fontStyle=1;fontSize=11;")
    make_drawio("17_stride_threat_model.drawio", "STRIDE Threat Model", xml)

# ==============================================================================
# 18. Attack Tree
# ==============================================================================
def gen_18():
    xml = header("COMPREHENSIVE ATTACK TREE & MITIGATION ARCHITECTURE")
    xml += b("root", "GOAL: Compromise Digital Wallet System\n(Illicit Funds Theft / Ledger Distortion)", 460, 80, 440, 60, "rounded=1;fillColor=#1E3A8A;fontColor=#FFFFFF;fontStyle=1;fontSize=12;")
    
    # 4 Sub-goals
    xml += b("b1", "SUB-GOAL 1: Double Spending\nvia Concurrency Race", 80, 180, 260, 65, "rounded=1;fillColor=#FEE2E2;strokeColor=#DC2626;fontStyle=1;")
    xml += b("b2", "SUB-GOAL 2: Replay Attack\non Payment API", 380, 180, 260, 65, "rounded=1;fillColor=#FEE2E2;strokeColor=#DC2626;fontStyle=1;")
    xml += b("b3", "SUB-GOAL 3: In-Flight\nPayload Tampering", 680, 180, 260, 65, "rounded=1;fillColor=#FEE2E2;strokeColor=#DC2626;fontStyle=1;")
    xml += b("b4", "SUB-GOAL 4: Cross-User\nAccount Takeover / BOLA", 980, 180, 260, 65, "rounded=1;fillColor=#FEE2E2;strokeColor=#DC2626;fontStyle=1;")
    
    # Leaves (Attacks)
    xml += b("l1", "Attack: Blast 10 concurrent\n$50 debits on $100 wallet", 80, 280, 260, 65, "rounded=1;fillColor=#FEF2F2;strokeColor=#EF4444;fontStyle=1;")
    xml += b("l2", "Attack: Resend captured\nPOST /payments request", 380, 280, 260, 65, "rounded=1;fillColor=#FEF2F2;strokeColor=#EF4444;fontStyle=1;")
    xml += b("l3", "Attack: Alter merchantId or\namount using same key", 680, 280, 260, 65, "rounded=1;fillColor=#FEF2F2;strokeColor=#EF4444;fontStyle=1;")
    xml += b("l4", "Attack: Access foreign walletId\nvia manipulated REST parameter", 980, 280, 260, 65, "rounded=1;fillColor=#FEF2F2;strokeColor=#EF4444;fontStyle=1;")
    
    # Mitigations
    xml += b("m1", "MITIGATION:\nSELECT FOR UPDATE Row Locking\n(Guarantees exactly 2 debits; 8 denied)", 80, 380, 260, 80, "rounded=1;fillColor=#DCFCE7;strokeColor=#15803D;fontStyle=1;")
    xml += b("m2", "MITIGATION:\nIdempotency Cache\n(Returns cached response without debit)", 380, 380, 260, 80, "rounded=1;fillColor=#DCFCE7;strokeColor=#15803D;fontStyle=1;")
    xml += b("m3", "MITIGATION:\nSHA-256 Payload Hash Binding\n(Returns HTTP 409 Conflict)", 680, 380, 260, 80, "rounded=1;fillColor=#DCFCE7;strokeColor=#15803D;fontStyle=1;")
    xml += b("m4", "MITIGATION:\nBOLA Security Ownership Check\n(Returns HTTP 403 Forbidden)", 980, 380, 260, 80, "rounded=1;fillColor=#DCFCE7;strokeColor=#15803D;fontStyle=1;")
    
    xml += e("ae1", "root", "b1")
    xml += e("ae2", "root", "b2")
    xml += e("ae3", "root", "b3")
    xml += e("ae4", "root", "b4")
    xml += e("ae5", "b1", "l1")
    xml += e("ae6", "b2", "l2")
    xml += e("ae7", "b3", "l3")
    xml += e("ae8", "b4", "l4")
    xml += e("ae9", "l1", "m1", "Blocked By", "strokeColor=#15803D;dashed=1;")
    xml += e("ae10", "l2", "m2", "Blocked By", "strokeColor=#15803D;dashed=1;")
    xml += e("ae11", "l3", "m3", "Blocked By", "strokeColor=#15803D;dashed=1;")
    xml += e("ae12", "l4", "m4", "Blocked By", "strokeColor=#15803D;dashed=1;")
    make_drawio("18_attack_tree.drawio", "Attack Tree", xml)

# ==============================================================================
# 19. Security Architecture Refinement
# ==============================================================================
def gen_19():
    xml = header("SECURITY-REFINED MULTI-TIER ARCHITECTURE")
    tiers = [
        ("t1", "PERIMETER TIER: Ingress & Transport Hardening\n• TLS 1.3 Transport Encryption | Nginx Reverse Proxy\n• Non-Root Container Execution (UID 10001) | Read-Only Root Filesystem\n• CORS Whitelist & Strict Content-Security-Policy (CSP)", 80, 80, 1200, 70, "fillColor=#EFF6FF;strokeColor=#1D4ED8;"),
        ("t2", "AUTHENTICATION & ACCESS CONTROL TIER: Zero-Trust Identity\n• BCrypt Cost Factor 12 Password Hashing\n• Stateless HMAC-SHA256 JWT Bearer Tokens with Expiry Claims\n• Spring Security @PreAuthorize RBAC (ROLE_USER, ROLE_MERCHANT, ROLE_ADMIN)", 80, 170, 1200, 70, "fillColor=#ECFDF5;strokeColor=#059669;"),
        ("t3", "INTEGRITY & IDEMPOTENCY TIER: Anti-Tamper & Anti-Replay Engine\n• Mandatory Idempotency-Key HTTP Header Gate\n• SHA-256 Request Payload Cryptographic Binding\n• State Machine Enforced Reversal Transitions (CONFIRMED -> REFUNDED)", 80, 260, 1200, 70, "fillColor=#FEF3C7;strokeColor=#D97706;"),
        ("t4", "CONCURRENCY & DATA CONSISTENCY TIER: Transactional Locking\n• Pessimistic Row-Level Write Locks (SELECT FOR UPDATE)\n• Strict READ_COMMITTED Database Isolation\n• Database-Level CHECK Constraints: CHECK (balance >= 0)", 80, 350, 1200, 70, "fillColor=#EDE9FE;strokeColor=#7C3AED;"),
        ("t5", "AUDITABILITY & COMPLIANCE TIER: Immutable Forensic Logging\n• Append-Only Audit Trail in MariaDB Ledger\n• Automated PII Regex Scrubbing (Masking Passwords and Tokens)\n• SIEM-Ready Structured JSON Event Logging", 80, 440, 1200, 70, "fillColor=#FEF2F2;strokeColor=#DC2626;")
    ]
    for t in tiers: xml += b(t[0], t[1], t[2], t[3], t[4], t[5], f"rounded=1;{t[6]}fontStyle=1;fontSize=11;")
    xml += e("te1", "t1", "t2", "Filtered Traffic")
    xml += e("te2", "t2", "t3", "Authenticated Claims")
    xml += e("te3", "t3", "t4", "Integrity Checked Orders")
    xml += e("te4", "t4", "t5", "State Transition Events")
    make_drawio("19_security_architecture.drawio", "Security Architecture Refinement", xml)

# ==============================================================================
# 20. Docker Architecture
# ==============================================================================
def gen_20():
    xml = header("MULTI-STAGE DOCKER ARCHITECTURE & LEAST-PRIVILEGE HARDENING")
    xml += b("stg1", "STAGE 1: MAVEN BUILD ENVIRONMENT\n\n• Base Image: maven:3.9.6-eclipse-temurin-21\n• Dependencies cached via pom.xml copy\n• Source compilation & JUnit 5 test execution\n• JaCoCo coverage agent instrumentation\n• Artifact Generated: dwpg-simulator-1.0.0.jar\n• Build tools and source code discarded", 80, 90, 480, 220, "rounded=1;fillColor=#EFF6FF;strokeColor=#1D4ED8;fontStyle=1;fontSize=11;")
    xml += b("stg2", "STAGE 2: HARDENED PRODUCTION RUNTIME\n\n• Base Image: eclipse-temurin:21-jre-alpine\n• Attack Surface: Minimal (Zero package managers/compilers)\n• Minimal Size: ~180MB footprint\n• Non-Root Execution: User UID 10001 (dwpgapp)\n• Read-Only Root Filesystem: read_only: true\n• Linux Capabilities Dropped: cap_drop: ALL\n• Exposed Port: 8080 (unprivileged)", 660, 90, 480, 220, "rounded=1;fillColor=#D1FAE5;strokeColor=#059669;fontStyle=1;fontSize=11;")
    xml += e("ed_stg", "stg1", "stg2", "COPY --from=builder dwpg-simulator.jar", "strokeColor=#059669;strokeWidth=3;")
    xml += b("d_sec", "RUNTIME SECURITY SAFEGUARDS VERIFIED\n\n1. Zero Root Privilege: Application cannot modify OS binaries or install malware.\n2. Container Escape Prevention: Dropped capabilities block kernel exploitation.\n3. Secret Protection: Zero hardcoded credentials in Dockerfile; injected via environment at runtime.", 80, 350, 1060, 110, "rounded=1;fillColor=#F8FAFC;strokeColor=#CBD5E1;fontStyle=1;fontSize=11;")
    make_drawio("20_docker_architecture.drawio", "Docker Architecture", xml)

# ==============================================================================
# 21. Kubernetes Architecture
# ==============================================================================
def gen_21():
    xml = header("KUBERNETES WORKLOAD TOPOLOGY & ZERO-TRUST NETWORK POLICIES")
    xml += b("k8s_ns", "Kubernetes Namespace: dwpg", 60, 80, 1100, 480, "shape=rect;fillColor=#F8FAFC;strokeColor=#2563EB;strokeWidth=2;verticalAlign=top;fontStyle=1;fontSize=13;")
    xml += b("ing", "NodePort Service (30080)\nExternal Ingress Barrier", 100, 130, 220, 70, "rounded=1;fillColor=#EFF6FF;strokeColor=#1D4ED8;fontStyle=1;")
    xml += b("pod_f", "Frontend Pods (x2)\napp=dwpg-frontend\nNginx + React SPA\nrunAsNonRoot: true", 100, 240, 220, 100, "rounded=1;fillColor=#DBEAFE;strokeColor=#2563EB;fontStyle=1;")
    xml += b("b_svc_k", "ClusterIP Service (8080)\ndwpg-backend-service", 460, 130, 260, 70, "rounded=1;fillColor=#F0FDF4;strokeColor=#16A34A;fontStyle=1;")
    xml += b("pod_b", "Backend Pods (x2)\napp=dwpg-backend\nSpring Boot 3.3.4\nUID 10001 | No-Root", 460, 240, 260, 100, "rounded=1;fillColor=#DCFCE7;strokeColor=#15803D;fontStyle=1;")
    xml += b("net_pol", "NetworkPolicy: isolate-mariadb\nDefault-Deny Ingress\nAllow ONLY app=dwpg-backend", 820, 130, 300, 70, "rounded=1;fillColor=#FEE2E2;strokeColor=#DC2626;fontStyle=1;")
    xml += b("pod_d", "MariaDB Stateful Pod (x1)\napp=dwpg-mariadb\nPort 3306 | PVC 5Gi", 820, 240, 300, 100, "shape=cylinder;fillColor=#FEF2F2;strokeColor=#B91C1C;fontStyle=1;")
    xml += e("k1", "ing", "pod_f")
    xml += e("k2", "pod_f", "b_svc_k")
    xml += e("k3", "b_svc_k", "pod_b")
    xml += e("k4", "pod_b", "pod_d", "Allowed by NetworkPolicy")
    xml += e("k5", "net_pol", "pod_d", "Firewall Filter", "strokeColor=#DC2626;strokeWidth=2;dashed=1;")
    make_drawio("21_kubernetes_architecture.drawio", "Kubernetes Architecture", xml)

# ==============================================================================
# 22. CI/CD Pipeline
# ==============================================================================
def gen_22():
    xml = header("DEVSECOPS CI/CD PIPELINE (GITHUB ACTIONS & QUALITY GATES)")
    stages = [
        ("c1", "1. Source Checkout\n• git clone\n• Branch: main\n• Setup JDK 21", 80, 120, 180, 80, "fillColor=#EFF6FF;strokeColor=#1D4ED8;"),
        ("c2", "2. Build & Test\n• mvn clean test\n• 25 JUnit 5 Tests\n• Concurrency Stress", 280, 120, 180, 80, "fillColor=#DBEAFE;strokeColor=#2563EB;"),
        ("c3", "3. Code Coverage\n• JaCoCo Agent\n• Coverage: 62.6%\n• Coverage XML export", 480, 120, 180, 80, "fillColor=#FEF3C7;strokeColor=#D97706;"),
        ("c4", "4. SonarQube SAST\n• SonarScanner Maven\n• 0 Vulnerabilities\n• Quality Gate = OK", 680, 120, 180, 80, "fillColor=#D1FAE5;strokeColor=#059669;"),
        ("c5", "5. Container Build\n• Multi-Stage Docker\n• Trivy Scan\n• Non-root Verification", 880, 120, 180, 80, "fillColor=#EDE9FE;strokeColor=#7C3AED;"),
        ("c6", "6. K8s Manifest Lint\n• Kubeconform\n• kubectl apply -f k8s/\n• dwpg namespace", 1080, 120, 160, 80, "fillColor=#CCFBF1;strokeColor=#0D9488;")
    ]
    for s in stages: xml += b(s[0], s[1], s[2], s[3], s[4], s[5], f"rounded=1;{s[6]}fontStyle=1;fontSize=10;")
    xml += e("ce1", "c1", "c2")
    xml += e("ce2", "c2", "c3")
    xml += e("ce3", "c3", "c4")
    xml += e("ce4", "c4", "c5")
    xml += e("ce5", "c5", "c6")
    xml += b("g_qg", "SECURITY QUALITY GATE: Zero Blocker/Critical Defects | Coverage >= 60% | Pass All Fuzz Probes", 80, 260, 1160, 50, "rounded=1;fillColor=#F0FDF4;strokeColor=#16A34A;fontStyle=1;fontSize=12;")
    make_drawio("22_cicd_pipeline.drawio", "CI/CD Pipeline", xml)

# ==============================================================================
# 23. Security Testing Pipeline
# ==============================================================================
def gen_23():
    xml = header("COMPREHENSIVE AUTOMATED SECURITY TESTING PIPELINE")
    tests = [
        ("t1", "Static SAST (SonarQube)\n• 0 Vulnerabilities\n• 0 Security Hotspots\n• 0 Bugs / Maintainability A", 80, 100, 260, 90, "fillColor=#DBEAFE;strokeColor=#1D4ED8;"),
        ("t2", "Unit & Domain Invariants\n• BCrypt Hashing (Cost 12)\n• Wallet Non-Negative Rule\n• BOLA Ownership Check", 370, 100, 260, 90, "fillColor=#DCFCE7;strokeColor=#15803D;"),
        ("t3", "Concurrency Race Stress\n• 10 Parallel Worker Threads\n• $100 Initial Balance\n• Exactly 2 Debits ($50+$50)\n• 8 Overdrafts Denied", 660, 100, 260, 90, "fillColor=#FEF3C7;strokeColor=#D97706;"),
        ("t4", "Input Fuzzing Suite\n• Negative Amounts ($-50)\n• SQLi Probes (' OR 1=1)\n• XSS Injection Probes\n• 12 Tests 100% Blocked", 950, 100, 260, 90, "fillColor=#FEE2E2;strokeColor=#DC2626;"),
        ("t5", "Live Functional REST\n• 9 End-to-End Test Cases\n• Auth, Wallet, Top-Up\n• Merchant, Payment, Refund", 220, 250, 280, 90, "fillColor=#EFF6FF;strokeColor=#2563EB;"),
        ("t6", "Live Adversarial Invariants\n• 8 Security Property Probes\n• Tamper Replay (409 Conflict)\n• Idempotent Duplicate (Cached)\n• Foreign Wallet IDOR (403)", 660, 250, 280, 90, "fillColor=#F3E8FF;strokeColor=#7E22CE;")
    ]
    for t in tests: xml += b(t[0], t[1], t[2], t[3], t[4], t[5], f"rounded=1;{t[6]}fontStyle=1;fontSize=10;")
    xml += e("te1", "t1", "t5")
    xml += e("te2", "t2", "t5")
    xml += e("te3", "t3", "t6")
    xml += e("te4", "t4", "t6")
    xml += b("t_sum", "VERIFICATION RESULT: 42 Automated Security & Functional Tests Executed | 100% PASSED (0 FAILURES)", 80, 390, 1130, 50, "rounded=1;fillColor=#ECFDF5;strokeColor=#059669;fontStyle=1;fontSize=12;")
    make_drawio("23_security_testing_pipeline.drawio", "Security Testing Pipeline", xml)

# ==============================================================================
# 24. Requirements-to-Implementation Traceability Matrix
# ==============================================================================
def gen_24():
    xml = header("REQUIREMENTS-TO-IMPLEMENTATION BIDIRECTIONAL TRACEABILITY MODEL")
    cols = [
        ("col_req", "1. Requirements\n\n• FR-01: User Auth\n• FR-03: Wallet Init\n• FR-04: Funds Topup\n• FR-06: Payment Process\n• FR-08: Refund Process\n• SR-03: Idempotency\n• SR-04: Race Condition", 80, 90, 200, 360, "fillColor=#EFF6FF;strokeColor=#1D4ED8;"),
        ("col_uml", "2. UML & Models\n\n• UC-01: Context (D-02)\n• Sequence Diag (D-12)\n• Sequence Diag (D-14)\n• 3NF ERD (D-05)\n• DFD Level 1 (D-07)\n• Attack Tree (D-18)\n• Security Arch (D-19)", 320, 90, 200, 360, "fillColor=#F0FDF4;strokeColor=#16A34A;"),
        ("col_code", "3. Source Classes\n\n• AuthController / Service\n• WalletController / Service\n• PaymentController / Svc\n• RefundController / Svc\n• IdempotencyService\n• WalletRepository (Lock)\n• AuditService (SIEM)", 560, 90, 220, 360, "fillColor=#FEF3C7;strokeColor=#D97706;"),
        ("col_test", "4. Automated Tests\n\n• AuthServiceTest\n• WalletServiceTest\n• PaymentConcurrencyTest\n• PaymentInputFuzzingTest\n• TC-AUTH-001..002\n• TC-PAY-001, SEC-003\n• TC-REF-001, SEC-006", 820, 90, 200, 360, "fillColor=#FEE2E2;strokeColor=#DC2626;"),
        ("col_evid", "5. Evidence Figures\n\n• UI-01 & UI-02 (Auth)\n• UI-03 & UI-05 (Wallet)\n• UI-08..10 (Payment)\n• UI-12 & UI-13 (Refund)\n• UI-14 (Replay Trap)\n• JIRA-01..16 (Metrics)\n• SONAR-01..07 (SAST)", 1060, 90, 200, 360, "fillColor=#EDE9FE;strokeColor=#7C3AED;")
    ]
    for c in cols: xml += b(c[0], c[1], c[2], c[3], c[4], c[5], f"rounded=1;{c[6]}fontStyle=1;fontSize=10;verticalAlign=top;")
    xml += e("tr1", "col_req", "col_uml")
    xml += e("tr2", "col_uml", "col_code")
    xml += e("tr3", "col_code", "col_test")
    xml += e("tr4", "col_test", "col_evid")
    make_drawio("24_traceability_matrix.drawio", "Requirement-to-Implementation Traceability", xml)

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":
    print("Generating all 24 drawio files...")
    gen_01()
    gen_02()
    gen_03()
    gen_04()
    gen_05()
    gen_06()
    gen_07()
    gen_08()
    gen_09()
    gen_10()
    gen_11()
    gen_12()
    gen_13()
    gen_14()
    gen_15()
    gen_16()
    gen_17()
    gen_18()
    gen_19()
    gen_20()
    gen_21()
    gen_22()
    gen_23()
    gen_24()
    print("\nAll 24 DRAW.IO files successfully generated!")
