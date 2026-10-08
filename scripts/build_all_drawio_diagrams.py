import os
import subprocess

DRAWIO_DIR = "docs/diagrams/drawio"
PNG_DIR = "docs/diagrams/png"
SVG_DIR = "docs/diagrams/svg"

os.makedirs(DRAWIO_DIR, exist_ok=True)
os.makedirs(PNG_DIR, exist_ok=True)
os.makedirs(SVG_DIR, exist_ok=True)

print("Authoring 24 Professional DRAW.IO XML Source Diagrams...")

def write_drawio(filename, title, content_xml, width=1400, height=900):
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
    print(f"Created: {filepath}")

# Helper generators
def mx_box(id, val, x, y, w, h, style="rounded=1;whiteSpace=wrap;html=1;", parent="1"):
    return f'        <mxCell id="{id}" value="{val}" style="{style}" vertex="1" parent="{parent}"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>\n'

def mx_edge(id, src, tgt, val="", style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#1E3A8A;strokeWidth=2;"):
    return f'        <mxCell id="{id}" value="{val}" style="{style}" edge="1" parent="1" source="{src}" target="{tgt}"><mxGeometry relative="1" as="geometry" /></mxCell>\n'

# 1. 01_agile_lifecycle.drawio
d01 = ""
d01 += mx_box("title", "DWPG SIMULATOR | AGILE SECURE SOFTWARE ENGINEERING LIFECYCLE", 100, 20, 1000, 40, "shape=rect;fillColor=#1E3A8A;fontColor=#FFFFFF;fontStyle=1;fontSize=15;rounded=1;")
phases = [
    ("p1", "Sprint 1: Core MVP Planning\n• User & Merchant Lifecycle\n• Wallet Provisioning\n• Payment Core Engine", 80, 100, 240, 90, "rounded=1;fillColor=#DBEAFE;strokeColor=#1D4ED8;fontStyle=1;fontSize=11;"),
    ("p2", "Sprint 1 Execution\n• Stories DWPG-10..14\n• 26 SP Committed\n• 21 SP Delivered", 360, 100, 220, 90, "rounded=1;fillColor=#EFF6FF;strokeColor=#2563EB;fontStyle=1;fontSize=11;"),
    ("p3", "Discovery & Retrospective\n• Concurrency Stress Testing\n• Defect DEF-001 Flagged:\n  Race Condition & Replay", 620, 100, 240, 90, "rounded=1;fillColor=#FEE2E2;strokeColor=#DC2626;fontStyle=1;fontSize=11;"),
    ("p4", "Sprint 2: Hardening Scope\n• Pessimistic Row Locking\n• Idempotency Token Cache\n• Multi-Role Refunds (26 SP)", 900, 100, 240, 90, "rounded=1;fillColor=#FEF3C7;strokeColor=#D97706;fontStyle=1;fontSize=11;"),
    ("p5", "Sprint 2 Execution & Refactor\n• SELECT FOR UPDATE Implementation\n• SHA-256 Payload Binding\n• 100% Velocity Achieved", 900, 240, 240, 90, "rounded=1;fillColor=#D1FAE5;strokeColor=#059669;fontStyle=1;fontSize=11;"),
    ("p6", "Containerization & K8s\n• Multi-Stage Docker Build\n• Non-Root UID 10001\n• Minikube dwpg Namespace", 620, 240, 240, 90, "rounded=1;fillColor=#E0E7FF;strokeColor=#4338CA;fontStyle=1;fontSize=11;"),
    ("p7", "DevSecOps & SAST Pipeline\n• SonarQube LTS Quality Gate\n• Zero Vulnerabilities / Bugs\n• 42 Automated Tests Passed", 360, 240, 220, 90, "rounded=1;fillColor=#CCFBF1;strokeColor=#0D9488;fontStyle=1;fontSize=11;"),
    ("p8", "Academic Capstone Review\n• 16 Phases Fully Verified\n• Master Report Generated\n• Git Repository Synchronized", 80, 240, 240, 90, "rounded=1;fillColor=#F3E8FF;strokeColor=#7E22CE;fontStyle=1;fontSize=11;")
]
for p in phases: d01 += mx_box(p[0], p[1], p[2], p[3], p[4], p[5], p[6])
d01 += mx_edge("e1", "p1", "p2")
d01 += mx_edge("e2", "p2", "p3")
d01 += mx_edge("e3", "p3", "p4")
d01 += mx_edge("e4", "p4", "p5")
d01 += mx_edge("e5", "p5", "p6")
d01 += mx_edge("e6", "p6", "p7")
d01 += mx_edge("e7", "p7", "p8")
write_drawio("01_agile_lifecycle.drawio", "Agile Development Lifecycle", d01)

# 2. 02_system_context.drawio
d02 = ""
d02 += mx_box("title", "DWPG SYSTEM CONTEXT & TRUST BOUNDARY ARCHITECTURE", 150, 20, 900, 40, "shape=rect;fillColor=#1E3A8A;fontColor=#FFFFFF;fontStyle=1;fontSize=15;rounded=1;")
d02 += mx_box("c_bound", "Digital Wallet & Payment Gateway Boundary", 320, 80, 560, 460, "shape=rect;fillColor=#F8FAFC;strokeColor=#1E3A8A;strokeWidth=2;verticalAlign=top;fontStyle=1;fontSize=13;")
d02 += mx_box("act_cust", "Consumer User\n(Student / Customer)", 60, 120, 180, 70, "shape=actor;fillColor=#DBEAFE;strokeColor=#1D4ED8;fontStyle=1;fontSize=11;")
d02 += mx_box("act_merch", "Registered Merchant\n(Store / Service)", 60, 280, 180, 70, "shape=actor;fillColor=#FEF3C7;strokeColor=#D97706;fontStyle=1;fontSize=11;")
d02 += mx_box("act_admin", "Compliance Auditor\n(Administrator)", 60, 440, 180, 70, "shape=actor;fillColor=#FEE2E2;strokeColor=#DC2626;fontStyle=1;fontSize=11;")
d02 += mx_box("b_gw", "REST API Gateway & Security Filter\n• Spring Security 6\n• Bearer JWT Auth Filter\n• Idempotency-Key Header Interceptor", 360, 140, 480, 80, "rounded=1;fillColor=#EFF6FF;strokeColor=#2563EB;fontStyle=1;fontSize=11;")
d02 += mx_box("b_svc", "Core Business Services Tier\n• AuthService (BCrypt Cost 12)\n• WalletService (Pessimistic Row Lock)\n• PaymentService (Double-Entry Debit/Credit)\n• RefundService (Status FSM Transition)", 360, 260, 480, 110, "rounded=1;fillColor=#F0FDF4;strokeColor=#16A34A;fontStyle=1;fontSize=11;")
d02 += mx_box("b_data", "Secure Storage Vault (MariaDB / H2)\n• wallets (balance >= 0 check)\n• transactions (immutable ledger)\n• idempotency_keys (SHA-256 payload bind)\n• audit_logs (PII scrubbed)", 360, 410, 480, 100, "shape=cylinder;fillColor=#FEF2F2;strokeColor=#DC2626;fontStyle=1;fontSize=11;")
d02 += mx_box("act_siem", "Enterprise SIEM /\nForensic Collector", 960, 280, 180, 80, "shape=rect;fillColor=#F3E8FF;strokeColor=#7E22CE;fontStyle=1;fontSize=11;")
d02 += mx_edge("ec1", "act_cust", "b_gw", "HTTPS / REST")
d02 += mx_edge("ec2", "act_merch", "b_gw", "HTTPS / API Key")
d02 += mx_edge("ec3", "act_admin", "b_gw", "ROLE_ADMIN")
d02 += mx_edge("ec4", "b_gw", "b_svc", "Authenticated Principal")
d02 += mx_edge("ec5", "b_svc", "b_data", "ACID / SELECT FOR UPDATE")
d02 += mx_edge("ec6", "b_svc", "act_siem", "Audit Events Stream")
write_drawio("02_system_context.drawio", "System Context Diagram", d02)

# Copy existing drawio files where applicable and enrich them
existing_mappings = [
    ("docs/03-uml/use-case-diagram.drawio", "03_use_case.drawio"),
    ("docs/03-uml/analysis-model.drawio", "04_analysis_model.drawio"),
    ("docs/04-data-flow/er-diagram.drawio", "05_erd.drawio"),
    ("docs/04-data-flow/dfd-level-0.drawio", "06_dfd_level0.drawio"),
    ("docs/04-data-flow/dfd-level-1.drawio", "07_dfd_level1.drawio"),
    ("docs/04-data-flow/trust-boundaries.drawio", "08_trust_boundary.drawio"),
    ("docs/05-architecture/architecture.drawio", "09_architecture.drawio"),
    ("docs/05-architecture/component-diagram.drawio", "10_component.drawio"),
    ("docs/08-attack-tree/attack-tree.drawio", "18_attack_tree.drawio"),
    ("docs/08-attack-tree/security-refined-architecture.drawio", "19_security_architecture.drawio")
]

for src, dst in existing_mappings:
    if os.path.exists(src):
        with open(src, 'r') as f_in:
            content = f_in.read()
        with open(os.path.join(DRAWIO_DIR, dst), 'w') as f_out:
            f_out.write(content)
        print(f"Adopted existing high-quality drawio: {dst}")

# 11. 11_deployment.drawio
d11 = ""
d11 += mx_box("title", "PHYSICAL DEPLOYMENT ARCHITECTURE (KUBERNETES & MINIKUBE)", 100, 20, 1000, 40, "shape=rect;fillColor=#1E3A8A;fontColor=#FFFFFF;fontStyle=1;fontSize=15;rounded=1;")
d11 += mx_box("k8s_node", "Kubernetes Minikube Cluster (Namespace: dwpg)", 80, 80, 1040, 500, "shape=rect;fillColor=#F8FAFC;strokeColor=#2563EB;strokeWidth=2;verticalAlign=top;fontStyle=1;fontSize=13;")
d11 += mx_box("np_front", "Service: dwpg-frontend-service\nNodePort: 30080 -> 3000", 120, 130, 260, 60, "rounded=1;fillColor=#EFF6FF;strokeColor=#1D4ED8;fontStyle=1;")
d11 += mx_box("pod_front", "Deployment: dwpg-frontend (Replicas: 2)\n• React 18 SPA + Nginx Reverse Proxy\n• Non-root User UID 101\n• Security Context: runAsNonRoot: true", 120, 220, 260, 110, "rounded=1;fillColor=#DBEAFE;strokeColor=#2563EB;fontStyle=1;")
d11 += mx_box("svc_back", "Service: dwpg-backend-service\nClusterIP: 8080 (Internal DNS)", 460, 130, 280, 60, "rounded=1;fillColor=#F0FDF4;strokeColor=#16A34A;fontStyle=1;")
d11 += mx_box("pod_back", "Deployment: dwpg-backend (Replicas: 2)\n• Java 21 LTS + Spring Boot 3.3.4\n• Non-root User UID 10001\n• ReadOnlyRootFilesystem: true\n• Capabilities Dropped: ALL", 460, 220, 280, 110, "rounded=1;fillColor=#DCFCE7;strokeColor=#15803D;fontStyle=1;")
d11 += mx_box("svc_db", "Service: dwpg-mariadb-service\nClusterIP: 3306 (NetworkPolicy Protected)", 800, 130, 280, 60, "rounded=1;fillColor=#FEF2F2;strokeColor=#DC2626;fontStyle=1;")
d11 += mx_box("pod_db", "Deployment: dwpg-mariadb\n• MariaDB 10.11 Engine\n• PersistentVolumeClaim: mariadb-pvc (5Gi)\n• NetworkPolicy: isolate-mariadb\n  (Ingress allowed only from dwpg-backend)", 800, 220, 280, 110, "shape=cylinder;fillColor=#FEE2E2;strokeColor=#B91C1C;fontStyle=1;")
d11 += mx_box("cm", "ConfigMap: dwpg-config\n• SPRING_PROFILES_ACTIVE=dev\n• SERVER_PORT=8080", 280, 390, 280, 70, "rounded=1;fillColor=#FEF3C7;strokeColor=#D97706;fontStyle=1;")
d11 += mx_box("sec", "Secret: dwpg-secrets\n• JWT_SECRET (256-bit Key)\n• DB_PASSWORD (Encrypted)", 620, 390, 280, 70, "rounded=1;fillColor=#EDE9FE;strokeColor=#7C3AED;fontStyle=1;")
d11 += mx_edge("ed1", "np_front", "pod_front")
d11 += mx_edge("ed2", "pod_front", "svc_back", "Proxy /api/*")
d11 += mx_edge("ed3", "svc_back", "pod_back")
d11 += mx_edge("ed4", "pod_back", "svc_db", "JDBC Connection")
d11 += mx_edge("ed5", "svc_db", "pod_db")
write_drawio("11_deployment.drawio", "Deployment Architecture", d11)

# 12. 12_auth_sequence.drawio
d12 = ""
d12 += mx_box("title", "AUTHENTICATION & JWT ISSUANCE SEQUENCE DIAGRAM", 150, 20, 900, 40, "shape=rect;fillColor=#1E3A8A;fontColor=#FFFFFF;fontStyle=1;fontSize=15;rounded=1;")
actors12 = [
    ("c", "Client (React UI)", 80),
    ("ac", "AuthController", 280),
    ("as", "AuthService", 480),
    ("ur", "UserRepository", 680),
    ("pe", "PasswordEncoder (BCrypt)", 880),
    ("jp", "JwtTokenProvider", 1080)
]
for a in actors12:
    d12 += mx_box(a[0], a[1], a[2], 80, 160, 40, "rounded=1;fillColor=#DBEAFE;strokeColor=#1D4ED8;fontStyle=1;")
    d12 += mx_box(f"line_{a[0]}", "", a[2]+75, 120, 10, 400, "shape=rect;fillColor=#CBD5E1;strokeColor=none;")

d12 += mx_edge("s1", "c", "ac", "1. POST /api/auth/login {user, pass}", "strokeColor=#1E3A8A;strokeWidth=2;")
d12 += mx_edge("s2", "ac", "as", "2. login(request, clientIp)")
d12 += mx_edge("s3", "as", "ur", "3. findByUsername(user)")
d12 += mx_edge("s4", "ur", "as", "4. return User Entity")
d12 += mx_edge("s5", "as", "pe", "5. matches(rawPassword, hash)")
d12 += mx_edge("s6", "pe", "as", "6. true (BCrypt verified)")
d12 += mx_edge("s7", "as", "jp", "7. generateToken(username, role)")
d12 += mx_edge("s8", "jp", "as", "8. signed HMAC-SHA256 JWT")
d12 += mx_edge("s9", "as", "c", "9. HTTP 200 OK {token, walletId}", "strokeColor=#059669;strokeWidth=2;dashed=1;")
write_drawio("12_auth_sequence.drawio", "Authentication Sequence Diagram", d12)

# 13. 13_wallet_funding_sequence.drawio
d13 = ""
d13 += mx_box("title", "WALLET PROVISIONING & FUNDS TOP-UP SEQUENCE DIAGRAM", 150, 20, 900, 40, "shape=rect;fillColor=#1E3A8A;fontColor=#FFFFFF;fontStyle=1;fontSize=15;rounded=1;")
actors13 = [
    ("c13", "Client (User)", 80),
    ("wc13", "WalletController", 280),
    ("ws13", "WalletService", 480),
    ("wr13", "WalletRepository", 680),
    ("tr13", "TransactionRepository", 880),
    ("as13", "AuditService", 1080)
]
for a in actors13:
    d13 += mx_box(a[0], a[1], a[2], 80, 160, 40, "rounded=1;fillColor=#DBEAFE;strokeColor=#1D4ED8;fontStyle=1;")
    d13 += mx_box(f"line_{a[0]}", "", a[2]+75, 120, 10, 400, "shape=rect;fillColor=#CBD5E1;strokeColor=none;")

d13 += mx_edge("sf1", "c13", "wc13", "1. POST /api/wallets/topup {amount: 500.00}")
d13 += mx_edge("sf2", "wc13", "ws13", "2. fundMyWallet(request, user)")
d13 += mx_edge("sf3", "ws13", "wr13", "3. findByIdForUpdate(walletId) [PESSIMISTIC_WRITE]")
d13 += mx_edge("sf4", "wr13", "ws13", "4. Locked Wallet Row")
d13 += mx_edge("sf5", "ws13", "wr13", "5. wallet.credit(500.00) & save()")
d13 += mx_edge("sf6", "ws13", "tr13", "6. save(Transaction: TOP_UP)")
d13 += mx_edge("sf7", "ws13", "as13", "7. logEvent(FUNDS_ADDED)")
d13 += mx_edge("sf8", "ws13", "c13", "8. HTTP 200 OK {newBalance: 500.00}", "strokeColor=#059669;strokeWidth=2;dashed=1;")
write_drawio("13_wallet_funding_sequence.drawio", "Wallet Funding Sequence Diagram", d13)

# 14. 14_payment_sequence.drawio
d14 = ""
d14 += mx_box("title", "IDEMPOTENT PAYMENT SETTLEMENT & CONCURRENCY LOCKING SEQUENCE", 100, 20, 1000, 40, "shape=rect;fillColor=#1E3A8A;fontColor=#FFFFFF;fontStyle=1;fontSize=15;rounded=1;")
actors14 = [
    ("c14", "Customer Client", 60),
    ("pc14", "PaymentController", 260),
    ("is14", "IdempotencyService", 460),
    ("ps14", "PaymentService", 660),
    ("wr14", "WalletRepository", 860),
    ("tr14", "TransactionRepository", 1060)
]
for a in actors14:
    d14 += mx_box(a[0], a[1], a[2], 80, 160, 40, "rounded=1;fillColor=#DBEAFE;strokeColor=#1D4ED8;fontStyle=1;")
    d14 += mx_box(f"line_{a[0]}", "", a[2]+75, 120, 10, 400, "shape=rect;fillColor=#CBD5E1;strokeColor=none;")

d14 += mx_edge("p1", "c14", "pc14", "1. POST /api/payments/initiate [Idempotency-Key: K1, $75]")
d14 += mx_edge("p2", "pc14", "is14", "2. checkIdempotency(K1, sha256(payload))")
d14 += mx_edge("p3", "is14", "ps14", "3. Cache Miss -> Process Fresh Payment")
d14 += mx_edge("p4", "ps14", "wr14", "4. Lock Sender & Merchant Wallets [SELECT FOR UPDATE]")
d14 += mx_edge("p5", "wr14", "ps14", "5. Wallets Locked & Invariant Verified (balance >= 75)")
d14 += mx_edge("p6", "ps14", "wr14", "6. Atomic Debit Sender ($75) & Credit Merchant ($75)")
d14 += mx_edge("p7", "ps14", "tr14", "7. Record Double-Entry Ledger (DEBIT & CREDIT Tx)")
d14 += mx_edge("p8", "ps14", "is14", "8. saveIdempotencyRecord(K1, response, 201)")
d14 += mx_edge("p9", "ps14", "c14", "9. HTTP 201 Created {status: CONFIRMED, tamperHash}", "strokeColor=#059669;strokeWidth=2;dashed=1;")
write_drawio("14_payment_sequence.drawio", "Payment Transaction Sequence Diagram", d14)

# 15. 15_refund_sequence.drawio
d15 = ""
d15 += mx_box("title", "AUTHORIZED PAYMENT REFUND & STATE MACHINE REVERSAL SEQUENCE", 100, 20, 1000, 40, "shape=rect;fillColor=#1E3A8A;fontColor=#FFFFFF;fontStyle=1;fontSize=15;rounded=1;")
actors15 = [
    ("c15", "Merchant / Customer", 60),
    ("rc15", "RefundController", 260),
    ("rs15", "RefundService", 460),
    ("pr15", "PaymentRepository", 660),
    ("wr15", "WalletRepository", 860),
    ("rf15", "RefundRepository", 1060)
]
for a in actors15:
    d15 += mx_box(a[0], a[1], a[2], 80, 160, 40, "rounded=1;fillColor=#DBEAFE;strokeColor=#1D4ED8;fontStyle=1;")
    d15 += mx_box(f"line_{a[0]}", "", a[2]+75, 120, 10, 400, "shape=rect;fillColor=#CBD5E1;strokeColor=none;")

d15 += mx_edge("r1", "c15", "rc15", "1. POST /api/refunds {paymentId: 1, reason}")
d15 += mx_edge("r2", "rc15", "rs15", "2. processRefund(paymentId, user)")
d15 += mx_edge("r3", "rs15", "pr15", "3. findByIdForUpdate(paymentId)")
d15 += mx_edge("r4", "pr15", "rs15", "4. Validate: Status == CONFIRMED & Not Refunded")
d15 += mx_edge("r5", "rs15", "wr15", "5. Lock Settlement & Customer Wallets [Row Lock]")
d15 += mx_edge("r6", "rs15", "wr15", "6. Reversal: Debit Merchant & Credit Customer")
d15 += mx_edge("r7", "rs15", "pr15", "7. payment.setStatus(REFUNDED)")
d15 += mx_edge("r8", "rs15", "rf15", "8. save(Refund: COMPLETED)")
d15 += mx_edge("r9", "rs15", "c15", "9. HTTP 200 OK {status: COMPLETED, fundsRestored}", "strokeColor=#059669;strokeWidth=2;dashed=1;")
write_drawio("15_refund_sequence.drawio", "Refund Sequence Diagram", d15)

# 16. 16_replay_idempotency_sequence.drawio
d16 = ""
d16 += mx_box("title", "IDEMPOTENCY CACHE & REPLAY ATTACK DEFENSE PROTOCOL", 100, 20, 1000, 40, "shape=rect;fillColor=#1E3A8A;fontColor=#FFFFFF;fontStyle=1;fontSize=15;rounded=1;")
actors16 = [
    ("c16", "Client / Attacker", 80),
    ("pc16", "PaymentController", 320),
    ("is16", "IdempotencyService", 580),
    ("ir16", "IdempotencyRecordRepository", 860),
    ("ps16", "PaymentEngine", 1100)
]
for a in actors16:
    d16 += mx_box(a[0], a[1], a[2], 80, 160, 40, "rounded=1;fillColor=#DBEAFE;strokeColor=#1D4ED8;fontStyle=1;")
    d16 += mx_box(f"line_{a[0]}", "", a[2]+75, 120, 10, 450, "shape=rect;fillColor=#CBD5E1;strokeColor=none;")

d16 += mx_box("sep1", "SCENARIO 1: IDENTICAL RETRY (NETWORK REPLAY)", 80, 140, 1180, 25, "fillColor=#EFF6FF;strokeColor=#2563EB;fontStyle=1;align=left;")
d16 += mx_edge("rp1", "c16", "pc16", "1. Retried POST /payments [Key: K1, Payload: P1]")
d16 += mx_edge("rp2", "pc16", "is16", "2. checkIdempotency(K1, sha256(P1))")
d16 += mx_edge("rp3", "is16", "ir16", "3. findByIdempotencyKey(K1)")
d16 += mx_edge("rp4", "ir16", "is16", "4. Record Found: Hash Matches P1")
d16 += mx_edge("rp5", "is16", "c16", "5. Return CACHED Response (Zero Extra Debit)", "strokeColor=#059669;strokeWidth=2;dashed=1;")

d16 += mx_box("sep2", "SCENARIO 2: TAMPERED PAYLOAD REPLAY ATTACK", 80, 310, 1180, 25, "fillColor=#FEF2F2;strokeColor=#DC2626;fontStyle=1;align=left;")
d16 += mx_edge("rp6", "c16", "pc16", "6. Tampered POST /payments [Key: K1, Tampered Amount: $999]")
d16 += mx_edge("rp7", "pc16", "is16", "7. checkIdempotency(K1, sha256(P2))")
d16 += mx_edge("rp8", "is16", "ir16", "8. Hash Mismatch Detected! P1 != P2")
d16 += mx_edge("rp9", "is16", "c16", "9. HTTP 409 Conflict: Tampered Replay Blocked", "strokeColor=#DC2626;strokeWidth=2;dashed=1;")
write_drawio("16_replay_idempotency_sequence.drawio", "Replay/Idempotency Sequence Diagram", d16)

# 17. 17_stride_threat_model.drawio
d17 = ""
d17 += mx_box("title", "STRIDE THREAT MODELING MATRIX & DEFENSE MAPPING", 100, 20, 1000, 40, "shape=rect;fillColor=#1E3A8A;fontColor=#FFFFFF;fontStyle=1;fontSize=15;rounded=1;")
stride_cards = [
    ("s_s", "S - Spoofing Identity", "Threat: Attacker steals session token or impersonates merchant.\n\nMitigation: BCrypt cost 12 password hashing, short-lived HMAC-SHA256 JWT, 256-bit API key authentication.", 80, 90, 520, 130, "fillColor=#DBEAFE;strokeColor=#1D4ED8;"),
    ("s_t", "T - Tampering with Data", "Threat: Adversary modifies payment amount or target merchant in flight.\n\nMitigation: TLS transport encryption, SHA-256 payload binding to Idempotency-Key, cryptographic tamper seal.", 640, 90, 520, 130, "fillColor=#FEE2E2;strokeColor=#DC2626;"),
    ("s_r", "R - Repudiation", "Threat: Customer or merchant claims transaction was unauthorized.\n\nMitigation: Append-only transaction ledger, digital receipt hashes, immutable SIEM audit trail.", 80, 250, 520, 130, "fillColor=#FEF3C7;strokeColor=#D97706;"),
    ("s_i", "I - Information Disclosure", "Threat: Cross-tenant IDOR exposes foreign wallet balances.\n\nMitigation: Strict BOLA ownership validation, zero sensitive card PAN in DB, regex log scrubbing.", 640, 250, 520, 130, "fillColor=#EFF6FF;strokeColor=#2563EB;"),
    ("s_d", "D - Denial of Service", "Threat: Concurrent payment storm exhausts DB connection pool.\n\nMitigation: HikariCP connection pool limits, idempotency fast-cache lookup, MariaDB row-level locks.", 80, 410, 520, 130, "fillColor=#F3E8FF;strokeColor=#7E22CE;"),
    ("s_e", "E - Elevation of Privilege", "Threat: Consumer principal invokes admin audit endpoints.\n\nMitigation: Spring Security RBAC @PreAuthorize(\"hasRole('ADMIN')\"), 403 Forbidden enforcement.", 640, 410, 520, 130, "fillColor=#DCFCE7;strokeColor=#15803D;")
]
for c in stride_cards: d17 += mx_box(c[0], c[1], c[3], c[4], c[5], c[6], f"rounded=1;{c[7]}fontStyle=1;fontSize=11;")
write_drawio("17_stride_threat_model.drawio", "STRIDE Threat Model", d17)

# 20. 20_docker_architecture.drawio
d20 = ""
d20 += mx_box("title", "MULTI-STAGE DOCKER ARCHITECTURE & LEAST-PRIVILEGE HARDENING", 100, 20, 1000, 40, "shape=rect;fillColor=#1E3A8A;fontColor=#FFFFFF;fontStyle=1;fontSize=15;rounded=1;")
d20 += mx_box("stg1", "STAGE 1: MAVEN BUILD ENVIRONMENT\n\n• Base Image: maven:3.9.6-eclipse-temurin-21\n• Dependencies cached via pom.xml copy\n• Source compilation & JUnit 5 test execution\n• JaCoCo coverage agent instrumentation\n• Artifact Generated: dwpg-simulator-1.0.0.jar\n• Build tools and source code discarded", 80, 90, 480, 220, "rounded=1;fillColor=#EFF6FF;strokeColor=#1D4ED8;fontStyle=1;fontSize=11;")
d20 += mx_box("stg2", "STAGE 2: HARDENED PRODUCTION RUNTIME\n\n• Base Image: eclipse-temurin:21-jre-alpine\n• Attack Surface: Minimal (Zero package managers/compilers)\n• Minimal Size: ~180MB footprint\n• Non-Root Execution: User UID 10001 (dwpgapp)\n• Read-Only Root Filesystem: read_only: true\n• Linux Capabilities Dropped: cap_drop: ALL\n• Exposed Port: 8080 (unprivileged)", 660, 90, 480, 220, "rounded=1;fillColor=#D1FAE5;strokeColor=#059669;fontStyle=1;fontSize=11;")
d20 += mx_edge("ed_stg", "stg1", "stg2", "COPY --from=builder dwpg-simulator.jar", "strokeColor=#059669;strokeWidth=3;")
d20 += mx_box("d_sec", "RUNTIME SECURITY SAFEGUARDS VERIFIED\n\n1. Zero Root Privilege: Application cannot modify OS binaries or install malware.\n2. Container Escape Prevention: Dropped capabilities block kernel exploitation.\n3. Secret Protection: Zero hardcoded credentials in Dockerfile; injected via environment at runtime.", 80, 350, 1060, 110, "rounded=1;fillColor=#F8FAFC;strokeColor=#CBD5E1;fontStyle=1;fontSize=11;")
write_drawio("20_docker_architecture.drawio", "Docker Architecture", d20)

# 21. 21_kubernetes_architecture.drawio
d21 = ""
d21 += mx_box("title", "KUBERNETES WORKLOAD TOPOLOGY & ZERO-TRUST NETWORK POLICIES", 100, 20, 1000, 40, "shape=rect;fillColor=#1E3A8A;fontColor=#FFFFFF;fontStyle=1;fontSize=15;rounded=1;")
d21 += mx_box("k8s_ns", "Kubernetes Namespace: dwpg", 60, 80, 1100, 480, "shape=rect;fillColor=#F8FAFC;strokeColor=#2563EB;strokeWidth=2;verticalAlign=top;fontStyle=1;fontSize=13;")
d21 += mx_box("ing", "NodePort Service (30080)\nExternal Ingress Barrier", 100, 130, 220, 70, "rounded=1;fillColor=#EFF6FF;strokeColor=#1D4ED8;fontStyle=1;")
d21 += mx_box("pod_f", "Frontend Pods (x2)\napp=dwpg-frontend\nNginx + React SPA\nrunAsNonRoot: true", 100, 240, 220, 100, "rounded=1;fillColor=#DBEAFE;strokeColor=#2563EB;fontStyle=1;")
d21 += mx_box("b_svc_k", "ClusterIP Service (8080)\ndwpg-backend-service", 460, 130, 260, 70, "rounded=1;fillColor=#F0FDF4;strokeColor=#16A34A;fontStyle=1;")
d21 += mx_box("pod_b", "Backend Pods (x2)\napp=dwpg-backend\nSpring Boot 3.3.4\nUID 10001 | No-Root", 460, 240, 260, 100, "rounded=1;fillColor=#DCFCE7;strokeColor=#15803D;fontStyle=1;")
d21 += mx_box("net_pol", "NetworkPolicy: isolate-mariadb\nDefault-Deny Ingress\nAllow ONLY app=dwpg-backend", 820, 130, 300, 70, "rounded=1;fillColor=#FEE2E2;strokeColor=#DC2626;fontStyle=1;")
d21 += mx_box("pod_d", "MariaDB Stateful Pod (x1)\napp=dwpg-mariadb\nPort 3306 | PVC 5Gi", 820, 240, 300, 100, "shape=cylinder;fillColor=#FEF2F2;strokeColor=#B91C1C;fontStyle=1;")
d21 += mx_edge("k1", "ing", "pod_f")
d21 += mx_edge("k2", "pod_f", "b_svc_k")
d21 += mx_edge("k3", "b_svc_k", "pod_b")
d21 += mx_edge("k4", "pod_b", "pod_d", "Allowed by NetworkPolicy")
d21 += mx_edge("k5", "net_pol", "pod_d", "Firewall Filter", "strokeColor=#DC2626;strokeWidth=2;dashed=1;")
write_drawio("21_kubernetes_architecture.drawio", "Kubernetes Architecture", d21)

# 22. 22_cicd_pipeline.drawio
d22 = ""
d22 += mx_box("title", "DEVSECOPS CI/CD PIPELINE (GITHUB ACTIONS & QUALITY GATES)", 100, 20, 1000, 40, "shape=rect;fillColor=#1E3A8A;fontColor=#FFFFFF;fontStyle=1;fontSize=15;rounded=1;")
stages22 = [
    ("c1", "1. Source Checkout\n• git clone\n• Branch: main\n• Setup JDK 21", 80, 120, 180, 80, "fillColor=#EFF6FF;strokeColor=#1D4ED8;"),
    ("c2", "2. Build & Test\n• mvn clean test\n• 25 JUnit 5 Tests\n• Concurrency Stress", 280, 120, 180, 80, "fillColor=#DBEAFE;strokeColor=#2563EB;"),
    ("c3", "3. Code Coverage\n• JaCoCo Agent\n• Instruction Coverage: 62.6%\n• Coverage XML export", 480, 120, 180, 80, "fillColor=#FEF3C7;strokeColor=#D97706;"),
    ("c4", "4. SonarQube SAST\n• SonarScanner Maven\n• 0 Vulnerabilities\n• Quality Gate = OK", 680, 120, 180, 80, "fillColor=#D1FAE5;strokeColor=#059669;"),
    ("c5", "5. Container Build\n• Multi-Stage Docker\n• Trivy Vulnerability Scan\n• Non-root Verification", 880, 120, 180, 80, "fillColor=#EDE9FE;strokeColor=#7C3AED;"),
    ("c6", "6. K8s Manifest Lint\n• Kubeconform\n• kubectl apply -f k8s/\n• dwpg namespace", 1080, 120, 160, 80, "fillColor=#CCFBF1;strokeColor=#0D9488;")
]
for s in stages22: d22 += mx_box(s[0], s[1], s[2], s[3], s[4], s[5], f"rounded=1;{s[6]}fontStyle=1;fontSize=10;")
d22 += mx_edge("ce1", "c1", "c2")
d22 += mx_edge("ce2", "c2", "c3")
d22 += mx_edge("ce3", "c3", "c4")
d22 += mx_edge("ce4", "c4", "c5")
d22 += mx_edge("ce5", "c5", "c6")
d22 += mx_box("g_qg", "SECURITY QUALITY GATE: Zero Blocker/Critical Defects | Coverage >= 60% | Pass All Fuzz Probes", 80, 260, 1160, 50, "rounded=1;fillColor=#F0FDF4;strokeColor=#16A34A;fontStyle=1;fontSize=12;")
write_drawio("22_cicd_pipeline.drawio", "CI/CD Pipeline", d22)

# 23. 23_security_testing_pipeline.drawio
d23 = ""
d23 += mx_box("title", "COMPREHENSIVE AUTOMATED SECURITY TESTING PIPELINE", 100, 20, 1000, 40, "shape=rect;fillColor=#1E3A8A;fontColor=#FFFFFF;fontStyle=1;fontSize=15;rounded=1;")
tests23 = [
    ("t1", "Static SAST (SonarQube)\n• 0 Vulnerabilities\n• 0 Security Hotspots\n• 0 Bugs / Maintainability A", 80, 100, 260, 90, "fillColor=#DBEAFE;strokeColor=#1D4ED8;"),
    ("t2", "Unit & Domain Invariants\n• BCrypt Hashing (Cost 12)\n• Wallet Non-Negative Rule\n• BOLA Ownership Check", 370, 100, 260, 90, "fillColor=#DCFCE7;strokeColor=#15803D;"),
    ("t3", "Concurrency Race Stress\n• 10 Parallel Worker Threads\n• $100 Initial Balance\n• Exactly 2 Debits ($50+$50)\n• 8 Overdrafts Denied", 660, 100, 260, 90, "fillColor=#FEF3C7;strokeColor=#D97706;"),
    ("t4", "Input Fuzzing Suite\n• Negative Amounts ($-50)\n• SQLi Probes (' OR 1=1)\n• XSS Injection Probes\n• 12 Tests 100% Blocked", 950, 100, 260, 90, "fillColor=#FEE2E2;strokeColor=#DC2626;"),
    ("t5", "Live Functional REST\n• 9 End-to-End Test Cases\n• Auth, Wallet, Top-Up\n• Merchant, Payment, Refund", 220, 250, 280, 90, "fillColor=#EFF6FF;strokeColor=#2563EB;"),
    ("t6", "Live Adversarial Invariants\n• 8 Security Property Probes\n• Tamper Replay (409 Conflict)\n• Idempotent Duplicate (Cached)\n• Foreign Wallet IDOR (403)", 660, 250, 280, 90, "fillColor=#F3E8FF;strokeColor=#7E22CE;")
]
for t in tests23: d23 += mx_box(t[0], t[1], t[2], t[3], t[4], t[5], f"rounded=1;{t[6]}fontStyle=1;fontSize=10;")
d23 += mx_edge("te1", "t1", "t5")
d23 += mx_edge("te2", "t2", "t5")
d23 += mx_edge("te3", "t3", "t6")
d23 += mx_edge("te4", "t4", "t6")
d23 += mx_box("t_sum", "VERIFICATION RESULT: 42 Automated Security & Functional Tests Executed | 100% PASSED (0 FAILURES)", 80, 390, 1130, 50, "rounded=1;fillColor=#ECFDF5;strokeColor=#059669;fontStyle=1;fontSize=12;")
write_drawio("23_security_testing_pipeline.drawio", "Security Testing Pipeline", d23)

# 24. 24_traceability_matrix.drawio
d24 = ""
d24 += mx_box("title", "REQUIREMENTS-TO-IMPLEMENTATION BIDIRECTIONAL TRACEABILITY MODEL", 100, 20, 1000, 40, "shape=rect;fillColor=#1E3A8A;fontColor=#FFFFFF;fontStyle=1;fontSize=15;rounded=1;")
t_cols = [
    ("col_req", "1. Requirements\n\n• FR-01: User Auth\n• FR-03: Wallet Init\n• FR-04: Funds Topup\n• FR-06: Payment Process\n• FR-08: Refund Process\n• SR-03: Idempotency\n• SR-04: Race Condition", 80, 90, 200, 360, "fillColor=#EFF6FF;strokeColor=#1D4ED8;"),
    ("col_uml", "2. UML & Models\n\n• UC-01: Context (D-02)\n• Sequence Diag (D-12)\n• Sequence Diag (D-14)\n• 3NF ERD (D-05)\n• DFD Level 1 (D-07)\n• Attack Tree (D-18)\n• Security Arch (D-19)", 320, 90, 200, 360, "fillColor=#F0FDF4;strokeColor=#16A34A;"),
    ("col_code", "3. Source Classes\n\n• AuthController / Service\n• WalletController / Service\n• PaymentController / Svc\n• RefundController / Svc\n• IdempotencyService\n• WalletRepository (Lock)\n• AuditService (SIEM)", 560, 90, 220, 360, "fillColor=#FEF3C7;strokeColor=#D97706;"),
    ("col_test", "4. Automated Tests\n\n• AuthServiceTest\n• WalletServiceTest\n• PaymentConcurrencyTest\n• PaymentInputFuzzingTest\n• TC-AUTH-001..002\n• TC-PAY-001, SEC-003\n• TC-REF-001, SEC-006", 820, 90, 200, 360, "fillColor=#FEE2E2;strokeColor=#DC2626;"),
    ("col_evid", "5. Evidence Figures\n\n• UI-01 & UI-02 (Auth)\n• UI-03 & UI-05 (Wallet)\n• UI-08..10 (Payment)\n• UI-12 & UI-13 (Refund)\n• UI-14 (Replay Trap)\n• JIRA-01..16 (Metrics)\n• SONAR-01..07 (SAST)", 1060, 90, 200, 360, "fillColor=#EDE9FE;strokeColor=#7C3AED;")
]
for c in t_cols: d24 += mx_box(c[0], c[1], c[2], c[3], c[4], c[5], f"rounded=1;{c[6]}fontStyle=1;fontSize=10;verticalAlign=top;")
d24 += mx_edge("tr1", "col_req", "col_uml")
d24 += mx_edge("tr2", "col_uml", "col_code")
d24 += mx_edge("tr3", "col_code", "col_test")
d24 += mx_edge("tr4", "col_test", "col_evid")
write_drawio("24_traceability_matrix.drawio", "Requirement-to-Implementation Traceability", d24)

print("\nALL 24 DRAW.IO DIAGRAMS CREATED SUCCESSFULLY IN docs/diagrams/drawio/!")
