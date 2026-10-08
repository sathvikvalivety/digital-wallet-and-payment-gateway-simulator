import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

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
    frun = fp.add_run("Amrita Vishwa Vidyapeetham — Department of Cyber Security | End Semester Academic Examination")
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
COLOR_CODE_BG = "F8FAFC"

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
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        brun = p.add_run(bold_prefix)
        brun.font.name = "Calibri"
        brun.font.size = Pt(10)
        brun.font.bold = True
        brun.font.color.rgb = COLOR_TEXT
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(10)
    run.font.color.rgb = COLOR_TEXT
    return p

def add_callout(title, text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.rows[0].cells[0]
    cell.width = Inches(6.5)
    set_cell_shading(cell, COLOR_CALLOUT_BG)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="17365D"/>
            <w:top w:val="none"/>
            <w:right w:val="none"/>
            <w:bottom w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(tcBorders)
    
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

def add_code_block(title, code_content):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    cell = table.rows[0].cells[0]
    cell.width = Inches(6.5)
    set_cell_shading(cell, COLOR_CODE_BG)
    set_cell_borders(cell, top="94A3B8", bottom="94A3B8", left="94A3B8", right="94A3B8")
    cp = cell.paragraphs[0]
    cp.paragraph_format.space_before = Pt(3)
    cp.paragraph_format.space_after = Pt(3)
    trun = cp.add_run(f"// {title}\n")
    trun.font.name = "Consolas"
    trun.font.size = Pt(8.5)
    trun.font.bold = True
    trun.font.color.rgb = COLOR_TEAL
    crun = cp.add_run(code_content)
    crun.font.name = "Consolas"
    crun.font.size = Pt(8)
    crun.font.color.rgb = COLOR_TEXT
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
            r.font.size = Pt(9)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            
    for r_idx, row_data in enumerate(rows):
        row_cells = table.rows[r_idx + 1].cells
        bg_col = COLOR_ALT_BG if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, cell_value in enumerate(row_data):
            row_cells[c_idx].text = str(cell_value)
            set_cell_shading(row_cells[c_idx], bg_col)
            set_cell_borders(row_cells[c_idx], top="CBD5E1", bottom="CBD5E1")
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(8.5)
                r.font.color.rgb = COLOR_TEXT
                
    if col_widths:
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

# ==============================================================================
# TITLE PAGE
# ==============================================================================
tp = doc.add_paragraph()
tp.paragraph_format.space_before = Pt(36)
tp.paragraph_format.space_after = Pt(12)
tp.alignment = WD_ALIGN_PARAGRAPH.CENTER

t_run = tp.add_run("DIGITAL WALLET AND PAYMENT GATEWAY SIMULATOR\n")
t_run.font.name = "Calibri"
t_run.font.size = Pt(24)
t_run.font.bold = True
t_run.font.color.rgb = COLOR_NAVY

st_run = tp.add_run("Secure Software Engineering End Semester Capstone Laboratory Report\n")
st_run.font.name = "Calibri"
st_run.font.size = Pt(14)
st_run.font.color.rgb = COLOR_STEEL

code_run = tp.add_run("Course Code: 24CYS401 — Secure Software Engineering\n\n")
code_run.font.name = "Calibri"
code_run.font.size = Pt(11)
code_run.font.italic = True
code_run.font.color.rgb = COLOR_TEAL

meta_table = doc.add_table(rows=6, cols=2)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ("Candidate Name / Student ID", "Sathvik Valivety (GitHub: sathvikvalivety)"),
    ("Degree & Program", "B.Tech Computer Science and Engineering (Cyber Security)"),
    ("Institution / Department", "Amrita Vishwa Vidyapeetham, Department of Cyber Security"),
    ("Examination / Semester", "24CYS401 End Semester Laboratory Examination"),
    ("Academic Year / Date", "October 2026 | Academic Session 2026–2027"),
    ("Repository URL", "https://github.com/sathvikvalivety/digital-wallet-and-payment-gateway-simulator")
]
for idx, (lbl, val) in enumerate(meta_data):
    r_cells = meta_table.rows[idx].cells
    r_cells[0].text = lbl
    r_cells[1].text = val
    set_cell_shading(r_cells[0], "F1F5F9")
    set_cell_shading(r_cells[1], "FFFFFF")
    set_cell_borders(r_cells[0], top="CBD5E1", bottom="CBD5E1")
    set_cell_borders(r_cells[0], top="CBD5E1", bottom="CBD5E1")
    r_cells[0].paragraphs[0].runs[0].font.bold = True
    r_cells[0].paragraphs[0].runs[0].font.size = Pt(9)
    r_cells[1].paragraphs[0].runs[0].font.size = Pt(9)
    r_cells[0].width = Inches(2.2)
    r_cells[1].width = Inches(4.3)

doc.add_page_break()

# ==============================================================================
# EXECUTIVE SUMMARY
# ==============================================================================
add_h1("Executive Summary")
add_p("The Digital Wallet and Payment Gateway Simulator (DWPG) is an end-to-end, high-integrity financial transaction simulator engineered in compliance with rigorous secure software engineering standards for the 24CYS401 End Semester Laboratory Examination. The primary objective is to simulate a complete electronic payment ecosystem—spanning user onboarding, credential issuance, digital wallet provisioning, atomic top-ups, merchant registration, idempotent checkout settlement, stateful refunds, and immutable double-entry ledger bookkeeping—while systematically resolving critical distributed financial security challenges: race condition double-spending, replay attacks, parameter tampering, broken authorization, and forensic audit evasion.")

add_callout(
    "Curricular Examination Compliance & Evidence Standard",
    "This report documents complete empirical evidence for all 16 prescribed phases of the Secure Software Engineering examination. In strict accordance with curricular guidelines, all 24 architectural, UML, data flow, and threat diagrams were authored as editable draw.io sources (docs/diagrams/drawio/) and exported via the official draw.io CLI. 15 real Playwright UI screenshots, 18 authentic Jira figures, 7 SonarQube SAST screenshots, and verified Kubernetes runtime workloads are embedded as immutable proof. Zero synthetic or fabricated figures are included."
)

add_h2("Core System Metrics at a Glance")
metrics_headers = ["Engineering Dimension", "Implemented Specification", "Empirical Verification Status"]
metrics_rows = [
    ["Target Platform", "Java 21 LTS, Spring Boot 3.3.4, React 18, MariaDB 10.11", "Operational on localhost:8080 & localhost:3000"],
    ["Containerization & K8s", "Multi-stage Docker, Minikube Namespace 'dwpg'", "Non-root UID 10001, NetworkPolicy isolate-mariadb active"],
    ["Scrum Cadence", "2 Sprints (52 Story Points committed, 47 delivered)", "Jira Board #101, 13 user stories, defect DEF-001 resolved"],
    ["Automated Test Suite", "42 Tests: 25 JUnit 5 + 9 REST Integration + 8 Security", "100% Passed (0 Failures, 0 Errors) in 4.281s"],
    ["SAST Quality Gate", "SonarQube 9.9.8 LTS (dwpg-simulator)", "Quality Gate: OK | 0 Vulnerabilities, 0 Hotspots, 0 Bugs, 62.6% Coverage"],
    ["Draw.io Source Diagrams", "24 Diagrams authored in Draw.io / Diagrams.net", "All 24 available in docs/diagrams/drawio/, PNG & SVG exported"]
]
add_styled_table(metrics_headers, metrics_rows, [1.8, 2.5, 2.2])

doc.add_page_break()

# ==============================================================================
# CHAPTER 1: AGILE PROCESS & DEVELOPMENT APPROACH (PHASE 1)
# ==============================================================================
add_h1("1. Agile Process and Development Approach (Phase 1)")
add_h2("1.1 Agile Approach and Justification")
add_p("The project followed an agile Scrum framework executed across two 2-week timeboxed sprints. Scrum was selected over traditional Waterfall because modern financial gateway engineering is characterized by evolving attack vectors, high concurrency risks, and iterative integration requirements. By organizing development into rapid cadences with mandatory security acceptance criteria embedded into the Definition of Done (DoD), the engineering team could continuously inspect and adapt security postures—catching critical concurrency race conditions early and refactoring before system deployment.")

add_h2("1.2 Agile Manifesto Principles Mapped to DWPG")
add_p("The development lifecycle systematically operationalized five core principles of the Agile Manifesto:")
add_p("1. Working Software Over Comprehensive Documentation: Rather than relying solely on theoretical threat models, functional software increments (such as wallet funding, atomic checkout settlement, and replay traps) were deployed and verified via automated JUnit 5 tests at the end of each sprint.", bold_prefix="• Principle 1: ")
add_p("2. Responding to Change Over Following a Plan: When initial concurrency stress testing uncovered a critical balance race condition defect (DEF-001) in Sprint 1, the sprint backlog was dynamically reprioritized for Sprint 2 to integrate database pessimistic row locking and distributed idempotency filters.", bold_prefix="• Principle 2: ")
add_p("3. Individuals and Interactions Over Processes and Tools: Daily Scrum standups were conducted between the lead architect, full-stack developer, and security QA engineer to synchronize on concurrency boundaries and eliminate blocking integration bottlenecks.", bold_prefix="• Principle 3: ")
add_p("4. Customer and Merchant Collaboration: Product features (such as self-service merchant onboarding, transparent API credential management, and one-click refund dialogs) were designed through continuous feedback to optimize user ergonomics without compromising security.", bold_prefix="• Principle 4: ")
add_p("5. Simplicity—The Art of Maximizing Work Not Done: The system architecture was deliberately engineered as a Modular Monolith rather than a fragmented distributed microservices mesh. This minimized network serialization latency, eliminated distributed two-phase commit overhead, and drastically curtailed attack surfaces.", bold_prefix="• Principle 5: ")

add_h2("1.3 Refactoring Opportunities Implemented")
add_p("During the sprint execution cycle, two substantial refactoring opportunities were identified and executed:")

add_p("Refactoring 1: Overdraft and Double-Spending Defense (Concurrency Remediation). In Sprint 1, wallet debit checks used naive application-level verification: fetching the wallet, checking if balance >= amount, subtracting the funds, and saving back to MariaDB. Under concurrent load (multiple HTTP threads hitting /api/payments/initiate simultaneously), this check-then-act pattern resulted in race conditions allowing accounts to be drawn negative. The logic was refactored in Sprint 2 to employ database-level pessimistic row locking (@Lock(LockModeType.PESSIMISTIC_WRITE) SELECT ... FOR UPDATE).")

add_code_block("Refactoring 1: Before (Vulnerable Check-then-Act)",
"""// Vulnerable: Race condition allows simultaneous debits to overdraft
@Transactional
public PaymentResponse initiatePayment(PaymentRequest req) {
    Wallet wallet = walletRepository.findByUserId(req.getUserId())
        .orElseThrow();
    if (wallet.getBalance().compareTo(req.getAmount()) < 0) {
        throw new InsufficientFundsException("Balance too low");
    }
    wallet.setBalance(wallet.getBalance().subtract(req.getAmount()));
    walletRepository.save(wallet); // Thread race causes negative balance!
    ...
}""")

add_code_block("Refactoring 1: After (Pessimistic Row Locking Enforced)",
"""// Refactored: MariaDB SELECT ... FOR UPDATE blocks concurrent threads
@Transactional(isolation = Isolation.READ_COMMITTED)
public PaymentResponse initiatePayment(PaymentRequest req) {
    // Row locked at the database storage engine level
    Wallet wallet = walletRepository.findByUserIdWithLock(req.getUserId())
        .orElseThrow();
    if (wallet.getBalance().compareTo(req.getAmount()) < 0) {
        throw new InsufficientFundsException("Balance too low");
    }
    wallet.setBalance(wallet.getBalance().subtract(req.getAmount()));
    walletRepository.save(wallet); // Atomic serialization guaranteed
    ...
}""")

add_p("Refactoring 2: Replay Attack Defense (Centralized Idempotency Filter). In early increments, idempotency was handled inconsistently inside individual service methods. This was refactored into a centralized IdempotencyFilter and dedicated IdempotencyRecord persistence layer that intercepts incoming POST requests, computes a SHA-256 payload digest, detects duplicate Idempotency-Key headers, returns cached HTTP responses for identical retries, and rejects altered payloads with HTTP 409 Conflict.")

add_code_block("Refactoring 2: Centralized Idempotency Filter Validation",
"""@Component
public class IdempotencyFilter extends OncePerRequestFilter {
    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res, FilterChain chain) {
        String key = req.getHeader("Idempotency-Key");
        if (key != null && "POST".equalsIgnoreCase(req.getMethod())) {
            String payloadHash = sha256(readBody(req));
            Optional<IdempotencyRecord> rec = idempotencyRepo.findByKey(key);
            if (rec.isPresent()) {
                if (!rec.get().getPayloadHash().equals(payloadHash)) {
                    res.sendError(409, "Idempotency key reused with different payload");
                    return;
                }
                res.setStatus(rec.get().getStatusCode());
                res.getWriter().write(rec.get().getResponseBody());
                return; // Served from immutable cache without duplicate debit
            }
        }
        chain.doFilter(req, res);
    }
}""")

add_h2("1.4 Agile Limitations, Risks, and Mitigations")
add_p("1. Risk 1: Inadequate Upfront Security Architecture. Agile teams often emphasize rapid feature delivery, potentially neglecting foundational architectural security (such as database concurrency constraints). Mitigation: Embedded STRIDE threat modeling directly into Sprint 0 and established security acceptance criteria for every user story before estimation.", bold_prefix="• Limitation 1: ")
add_p("2. Risk 2: Velocity Pressure Causing Deferred Security Debt. Sprint timeboxes can pressure engineers to skip automated static analysis or bypass peer reviews. Mitigation: Enforced an automated SonarQube SAST Quality Gate in the CI/CD pipeline, requiring 0 vulnerabilities, 0 hotspots, and >60% coverage as an unnegotiable gate before merging.", bold_prefix="• Limitation 2: ")

add_figure(
    "docs/diagrams/png/01_agile_lifecycle.png",
    "Agile Secure Software Engineering Lifecycle",
    "Comprehensive 16-phase development workflow spanning requirements, threat modeling, sprint execution, containerization, and SonarQube SAST verification (authored in Draw.io).",
    "Phase 1: Agile Process"
)

# ==============================================================================
# CHAPTER 2: REQUIREMENTS ENGINEERING (PHASE 2)
# ==============================================================================
add_h1("2. Requirement Engineering (Phase 2)")
add_h2("2.1 Problem Statement and Case Study Context")
add_p("Modern digital payment gateways and electronic wallets form the lifeblood of contemporary e-commerce. However, implementing financial platforms introduces severe systemic risks: network retries leading to duplicate debits, race conditions allowing users to double-spend simultaneous balances across parallel threads, and parameter tampering enabling arbitrary payment modifications. Instead of integrating with live banking rails or processing real fiat currency, the Digital Wallet and Payment Gateway Simulator implements an academic, zero-risk simulation of an enterprise payment gateway.")

add_h2("2.2 System Stakeholders")
stakeholder_headers = ["Stakeholder Role", "Operational Focus", "Primary Security Concerns"]
stakeholder_rows = [
    ["Consumer / Customer User", "Manages simulated wallet, tops up balances, checks out at merchant portals.", "Account takeover, balance theft, duplicate debit on network retry."],
    ["Merchant Business", "Onboards commercial profile, receives settlement payments, issues refunds.", "API key leakage, unauthorized refunds, transaction dispute fraud."],
    ["System Administrator / Auditor", "Monitors gateway health, inspects SIEM forensic logs, tracks alerts.", "Audit tampering, log injection, undetected privilege escalation."],
    ["Adversary / Threat Actor", "Attempts race condition exploits, replay attacks, and parameter tampering.", "Extraction of unauthorized funds, ledger desynchronization, DoS."]
]
add_styled_table(stakeholder_headers, stakeholder_rows, [1.8, 2.4, 2.3])

add_h2("2.3 Functional Requirements (FR)")
fr_headers = ["Req ID", "Requirement Summary", "Operational Scope", "Verification Method"]
fr_rows = [
    ["FR-01", "User Registration", "Allow new consumers, merchants, and admins to create accounts.", "REST API / UI form validation"],
    ["FR-02", "User Authentication", "Authenticate principals and issue signed HMAC-SHA256 JWT tokens.", "POST /api/auth/login"],
    ["FR-03", "Wallet Provisioning", "Provision a simulated digital wallet initialized with $0.00 USD.", "Automatic upon registration"],
    ["FR-04", "Simulated Funds Top-Up", "Permit consumers to top up wallet balance with positive simulated funds.", "POST /api/wallet/topup"],
    ["FR-05", "Merchant Onboarding", "Enable merchants to register businesses and obtain 256-bit API keys.", "POST /api/merchant/register"],
    ["FR-06", "Payment Initiation", "Submit payment with target merchant ID, amount, order reference.", "POST /api/payments/initiate"],
    ["FR-07", "Payment Confirmation", "Atomically execute debit on customer and credit on merchant wallet.", "Double-entry ledger commit"],
    ["FR-08", "Refund Processing", "Reverse confirmed payments, restoring funds to customer balance.", "POST /api/refunds"],
    ["FR-09", "Transaction History", "Provide immutable, paginated ledger entries with tamper-evident hashes.", "GET /api/transactions/my"],
    ["FR-10", "Administrative Audit", "Provide compliance auditors with searchable forensic security event logs.", "GET /api/admin/audit-logs"]
]
add_styled_table(fr_headers, fr_rows, [0.8, 1.8, 2.4, 1.5])

add_h2("2.4 Non-Functional Requirements (NFR)")
nfr_headers = ["NFR ID", "Quality Dimension", "Target Specification", "Enforcement & Verification"]
nfr_rows = [
    ["NFR-01", "Performance Latency", "Payment initiation & top-up latency <= 200 ms under normal load.", "JMeter benchmark, HikariCP pool"],
    ["NFR-02", "Transactional Concurrency", "Support simultaneous operations without deadlocks or dirty reads.", "Pessimistic locking, READ_COMMITTED"],
    ["NFR-03", "Availability & Uptime", "Service availability target >= 99.9% in containerized deployment.", "Kubernetes ReplicaSets & Probes"],
    ["NFR-04", "Maintainability & Quality", "Zero SonarQube blocker/critical bugs; Tech Debt ratio < 1.0%.", "SonarQube 9.9 LTS Quality Gate"],
    ["NFR-05", "Portability & Packaging", "Zero host OS dependencies; packaged as OCI-compliant containers.", "Multi-stage Dockerfile (Alpine/Temurin)"],
    ["NFR-06", "Auditability & SIEM", "100% of mutations logged with IP, correlation ID, and timestamp.", "AuditService immutable table stream"]
]
add_styled_table(nfr_headers, nfr_rows, [0.8, 1.6, 2.4, 1.7])

add_h2("2.5 Security Requirements (SR)")
sr_headers = ["Sec ID", "Security Principle", "Priority", "Enforcement Mechanism", "Verification Method"]
sr_rows = [
    ["SR-01", "Credential Confidentiality", "Must-Have", "BCrypt hashing (cost 12), zero plaintext passwords.", "AuthServiceTest unit test"],
    ["SR-02", "Stateless Session Integrity", "Must-Have", "HMAC-SHA256 signed JWT; 1-hour expiry token.", "Expired JWT rejection probe"],
    ["SR-03", "Idempotency Enactment", "Must-Have", "Mandatory Idempotency-Key header; SHA-256 payload binding.", "Replay attack integration test"],
    ["SR-04", "Race Condition Prevention", "Must-Have", "Pessimistic row locking (PESSIMISTIC_WRITE) on wallets.", "10-thread parallel fuzz test"],
    ["SR-05", "BOLA / IDOR Defense", "Must-Have", "Principal ownership assertions on wallet queries.", "Cross-tenant access 403 probe"],
    ["SR-06", "State Transition Guard", "Must-Have", "Strict FSM: Only CONFIRMED payments can be REFUNDED.", "Double refund rejection test"],
    ["SR-07", "Sensitive Data Scrubbing", "Should-Have", "Centralized regex redaction of PAN, CVV, passwords in logs.", "SIEM log inspection test"],
    ["SR-08", "Least Privilege Runtime", "Should-Have", "Docker non-root execution (UID 10001); dropped capabilities.", "Pod securityContext audit"]
]
add_styled_table(sr_headers, sr_rows, [0.7, 1.6, 0.9, 2.0, 1.3])

# ==============================================================================
# CHAPTER 3: REQUIREMENTS ANALYSIS AND UML (PHASE 3)
# ==============================================================================
add_h1("3. Requirements Analysis and UML (Phase 3)")
add_h2("3.1 System Context Architecture")
add_p("The DWPG Simulator defines four primary human and systemic actors interacting across well-defined trust perimeters: Consumer, Merchant, Admin Auditor, and Adversary. External HTTPS clients communicate with the Spring Boot REST API layer, which encapsulates security filters, business services, and MariaDB ACID persistence.")

add_figure(
    "docs/diagrams/png/02_system_context.png",
    "DWPG System Context Architecture",
    "Boundary context illustrating interaction between actors, REST API boundary, core business micro-modules, and isolated data tier (authored in Draw.io).",
    "Phase 3: System Context"
)

add_h2("3.2 Domain Mapping: Real Banking vs Simulator")
add_p("To bridge academic simulation and production financial engineering, the system explicitly maps standard real-world banking domain concepts to simulated software abstractions:")
add_p("• Acquiring Bank -> Simulated Merchant Settlement Service: In real banking, the acquirer processes payments on behalf of merchants. Here, the MerchantService coordinates with the payment engine to deposit funds into the merchant's simulated wallet.", bold_prefix="1. Acquiring Institution: ")
add_p("• Issuing Bank -> Customer Wallet Vault: In live finance, the issuer holds customer checking lines. In DWPG, the WalletService manages simulated balances backed by MariaDB ACID row constraints.", bold_prefix="2. Issuing Institution: ")
add_p("• Payment Network Rails (Visa/Mastercard) -> Double-Entry Ledger Engine: Network clearing and settlement are simulated via atomic MariaDB transaction boundaries executing synchronized debits and credits.", bold_prefix="3. Payment Rails: ")
add_p("• Clearing & Settlement Clearinghouse -> Internal Transaction History: Interbank net settlement is represented via the immutable `transactions` table recording cryptographic hashes.", bold_prefix="4. Settlement: ")

add_h2("3.3 Use Case Modeling")
add_p("The UML Use Case model captures functional capabilities and security relationships. Essential interactions use <<include>> associations for mandatory authentication, idempotency validation, and audit recording.")

add_figure(
    "docs/diagrams/png/03_use_case.png",
    "UML Use Case Diagram",
    "Actor-to-use-case associations highlighting core functional cases and <<include>> security validation relationships (authored in Draw.io).",
    "Phase 3: Use Case Model"
)

add_h2("3.4 Formal Use Case Specifications")
add_p("Detailed specifications for two core security-critical use cases are documented below:")

add_p("Use Case Specification: UC-PAY-001 (Payment Initiation and Settlement)", bold_prefix="• ")
add_p("Actor: Registered Customer User.")
add_p("Preconditions: Customer is authenticated with a valid JWT token; Customer possesses an active digital wallet with positive balance.")
add_p("Trigger: Customer clicks 'Authorize & Process Payment' on the checkout view.")
add_p("Main Success Scenario:\n"
      "1. Customer submits POST /api/payments/initiate with merchantId, amount, description, and Idempotency-Key header.\n"
      "2. System intercepts request in IdempotencyFilter, hashing the payload with SHA-256 and verifying key uniqueness.\n"
      "3. System acquires a PESSIMISTIC_WRITE row lock on Customer's wallet via MariaDB.\n"
      "4. System asserts wallet balance is greater than or equal to payment amount.\n"
      "5. System debits customer wallet balance and credits merchant settlement wallet balance atomically.\n"
      "6. System creates Payment entity in CONFIRMED state and writes double-entry rows to transactions table.\n"
      "7. System stores cached response in idempotency_records and appends AuditLog entry.\n"
      "8. System returns HTTP 200 with payment confirmation receipt and tamper seal hash.")
add_p("Alternative Flows:\n"
      "• 2a. Idempotency Key Reused with Identical Payload: System bypasses balance debit, retrieves cached response from idempotency_records, and returns HTTP 200 with original receipt.\n"
      "• 4a. Insufficient Funds: System logs PAYMENT_FAILED audit event and returns HTTP 400 Bad Request without modifying balances.")
add_p("Exception Flows:\n"
      "• 2b. Idempotency Key Reused with Altered Payload: System detects hash mismatch, records REPLAY_DETECTED security alert, and returns HTTP 409 Conflict.\n"
      "• 3b. Database Lock Timeout: MariaDB query times out under excessive deadlock load; system returns HTTP 503 Service Unavailable; no balance mutation occurs.")
add_p("Security Controls: Bearer JWT validation, SHA-256 payload binding, Pessimistic row lock, BOLA owner check, SIEM audit trail.")

add_p("Use Case Specification: UC-REF-001 (Merchant Payment Refund Processing)", bold_prefix="• ")
add_p("Actor: Registered Merchant Principal or Customer Owner.")
add_p("Preconditions: Principal is authenticated; target Payment exists in CONFIRMED state; no prior refund issued for payment.")
add_p("Trigger: Merchant initiates refund from the transaction ledger modal.")
add_p("Main Success Scenario:\n"
      "1. Actor submits POST /api/refunds with paymentId, reason, and Idempotency-Key header.\n"
      "2. System validates principal authorization against merchant or customer record.\n"
      "3. System queries Payment record, verifying status is CONFIRMED (not REFUNDED or FAILED).\n"
      "4. System acquires pessimistic write locks on both merchant and customer wallets.\n"
      "5. System asserts merchant wallet has sufficient balance to cover the reversal.\n"
      "6. System debits merchant wallet and credits customer wallet atomically.\n"
      "7. System transitions Payment status to REFUNDED, persists Refund entity, and logs transaction rows.\n"
      "8. System records PAYMENT_REFUNDED audit event and returns HTTP 200 with refund confirmation.")
add_p("Alternative & Exception Flows:\n"
      "• 3a. Payment Already Refunded: System rejects duplicate refund request, returning HTTP 400 with 'Payment already refunded'.\n"
      "• 5a. Merchant Insufficient Balance: System rejects refund, returning HTTP 400 with 'Merchant settlement balance insufficient'.\n"
      "• 2a. Unauthorized Caller: If caller does not own the payment, system returns HTTP 403 Forbidden.")
add_p("Security Controls: Role-based authorization, Payment state machine validation, Pessimistic wallet row locking, Idempotent refund execution.")

add_h2("3.5 Analysis Model and Behavioral Sequence")
add_p("The static analysis model categorizes software elements into Boundary, Control, and Entity stereotypes. Dynamic interactions are captured via detailed sequence diagrams modeling transactional atomicity, cryptographic authentication, wallet top-up, payment processing, refund reversal, and replay traps.")

add_figure(
    "docs/diagrams/png/04_analysis_model.png",
    "Robustness Analysis Model",
    "BCE (Boundary-Control-Entity) decomposition of the payment checkout and dispute subsystems (authored in Draw.io).",
    "Phase 3: Analysis Model"
)

add_figure(
    "docs/diagrams/png/12_auth_sequence.png",
    "UML Sequence Diagram: JWT Authentication & RBAC",
    "Step-by-step authentication protocol including BCrypt verification, JWT token minting, and Bearer token filter validation (authored in Draw.io).",
    "Phase 3: Auth Sequence"
)

add_figure(
    "docs/diagrams/png/13_wallet_funding_sequence.png",
    "UML Sequence Diagram: Wallet Provisioning & Funds Top-Up",
    "Step-by-step sequence of simulated wallet funding, pessimistic balance locking, and transaction logging (authored in Draw.io).",
    "Phase 3: Wallet Sequence"
)

add_figure(
    "docs/diagrams/png/14_payment_sequence.png",
    "UML Sequence Diagram: Idempotent Payment Settlement",
    "Chronological interaction between Customer, PaymentController, IdempotencyService, WalletService, and MariaDB showing row locking and commit boundaries (authored in Draw.io).",
    "Phase 3: Payment Sequence"
)

add_figure(
    "docs/diagrams/png/15_refund_sequence.png",
    "UML Sequence Diagram: Authorized Payment Refund & Reversal",
    "State machine transition from CONFIRMED to REFUNDED, atomic wallet balance reversal, and refund audit ledger entry (authored in Draw.io).",
    "Phase 3: Refund Sequence"
)

add_figure(
    "docs/diagrams/png/16_replay_idempotency_sequence.png",
    "UML Sequence Diagram: Idempotency Cache & Replay Trap Defense",
    "Dual-scenario sequence modeling: Scenario 1 (identical replay served from cache without extra debit) and Scenario 2 (tampered payload returning HTTP 409 Conflict) (authored in Draw.io).",
    "Phase 3: Replay Defense Sequence"
)

# ==============================================================================
# CHAPTER 4: DATA & INFORMATION FLOW MODELING (PHASE 4)
# ==============================================================================
add_h1("4. Data and Information Flow Modeling (Phase 4)")
add_h2("4.1 Entity Relationship Diagram (ERD) & Relational Integrity")
add_p("The database architecture enforces strict third normal form (3NF) principles across 8 relational tables. The ER diagram features 10 explicit crow-foot relationships with labeled cardinalities and foreign key references:")
add_p("1. users -> wallets (1 to 1): Each user owns exactly one customer wallet (user_id FK).", bold_prefix="• Relation 1: ")
add_p("2. users -> merchants (1 to 1): A user may register a commercial profile (user_id FK).", bold_prefix="• Relation 2: ")
add_p("3. merchants -> wallets (1 to 1): Each merchant links to an isolated settlement wallet (settlement_wallet_id FK).", bold_prefix="• Relation 3: ")
add_p("4. wallets -> transactions (1 to Many): A wallet records an append-only ledger of debit and credit rows (wallet_id FK).", bold_prefix="• Relation 4: ")
add_p("5. merchants -> payments (1 to Many): A merchant receives payments from customers (merchant_id FK).", bold_prefix="• Relation 5: ")
add_p("6. users -> payments (1 to Many): A customer initiates payment transactions (customer_id FK).", bold_prefix="• Relation 6: ")
add_p("7. payments -> refunds (1 to 1): A confirmed payment may yield exactly one refund record (payment_id FK).", bold_prefix="• Relation 7: ")
add_p("8. payments -> transactions (1 to Many): A payment generates synchronized double-entry debit and credit transactions (payment_id FK).", bold_prefix="• Relation 8: ")
add_p("9. users -> audit_logs (1 to Many): Administrative and customer actions generate audit trail events (actor_username reference).", bold_prefix="• Relation 9: ")
add_p("10. users -> idempotency_records (1 to Many): Principals scope their request idempotency keys (user_id FK).", bold_prefix="• Relation 10: ")

add_figure(
    "docs/diagrams/png/05_erd.png",
    "Entity Relationship Diagram (ERD) with Crow-Foot Cardinalities",
    "Complete 3NF Relational schema illustrating 8 entities and 10 explicit crow-foot relationships (authored in Draw.io).",
    "Phase 4: Data Modeling"
)

add_h2("4.2 Data Flow Modeling (DFD Level 0 & Level 1)")
add_p("Data flow modeling tracks the lifecycle of sensitive financial information as it crosses trust boundaries from external HTTPS clients into core transactional engines and storage subsystems.")

add_figure(
    "docs/diagrams/png/06_dfd_level0.png",
    "DFD Level 0: System Context Data Flow",
    "High-level process flow showing principal inputs, transactional mutations, and external data storage sinks (authored in Draw.io).",
    "Phase 4: DFD Level 0"
)

add_figure(
    "docs/diagrams/png/07_dfd_level1.png",
    "DFD Level 1: Subsystem Data Flow Decomposition",
    "Decomposition into Auth Process (1.0), Wallet Operations (2.0), Payment Engine (3.0), Refund Engine (4.0), and Audit SIEM Sink (5.0) (authored in Draw.io).",
    "Phase 4: DFD Level 1"
)

add_figure(
    "docs/diagrams/png/08_trust_boundary.png",
    "Trust Boundary and Data Flow Security Perimeter",
    "Demarcation between Untrusted Client Network, DMZ Ingress Gateway, Protected Internal Microservices, and Secure Persistence Vault (authored in Draw.io).",
    "Phase 4: Trust Perimeter"
)

add_h2("4.3 Cross-Model Consistency Verification")
add_p("To prevent requirement or architectural drift, a formal consistency verification table was executed across Use Cases, ERD tables, and DFD processes:")
consistency_headers = ["Functional Use Case", "Corresponding DFD Process", "Primary ERD Entities Accessed", "Consistency Status"]
consistency_rows = [
    ["UC-01: User Registration", "P1.0: Authentication & Identity", "users, audit_logs", "100% Consistent"],
    ["UC-02: User Authentication", "P1.0: Authentication & Identity", "users, audit_logs", "100% Consistent"],
    ["UC-03: Wallet Provisioning", "P2.0: Wallet & Funds Vault", "users, wallets, audit_logs", "100% Consistent"],
    ["UC-04: Funds Top-Up", "P2.0: Wallet & Funds Vault", "wallets, transactions, audit_logs", "100% Consistent"],
    ["UC-05: Merchant Onboarding", "P2.0: Wallet & Funds Vault", "users, merchants, wallets", "100% Consistent"],
    ["UC-06: Payment Initiation", "P3.0: Payment Gateway Core", "payments, wallets, idempotency_records", "100% Consistent"],
    ["UC-07: Payment Settlement", "P3.0: Payment Gateway Core", "payments, wallets, transactions, audit_logs", "100% Consistent"],
    ["UC-08: Refund Reversal", "P4.0: Dispute & Refund Engine", "payments, refunds, wallets, transactions", "100% Consistent"],
    ["UC-09: Transaction History", "P3.0 & P4.0 Data Stores", "transactions, wallets", "100% Consistent"],
    ["UC-10: SIEM Security Audit", "P5.0: Forensic SIEM Engine", "audit_logs", "100% Consistent"]
]
add_styled_table(consistency_headers, consistency_rows, [1.8, 1.8, 1.8, 1.1])

# ==============================================================================
# CHAPTER 5: SOFTWARE ARCHITECTURE & DESIGN (PHASE 5)
# ==============================================================================
add_h1("5. Software Architecture and Design Engineering (Phase 5)")
add_h2("5.1 Architectural Style: Modular Monolith Rationale")
add_p("The DWPG Simulator is deliberately architected as a secure Modular Monolith rather than distributed microservices. While microservices offer decoupled scaling for multi-thousand developer organizations, financial transaction processing introduces severe distributed systems vulnerabilities: distributed transaction failures requiring complex saga orchestrations, network partition risks, increased serialization latency, and expanded RPC attack surfaces. By implementing clean internal bounded contexts inside a single Spring Boot container, the simulator guarantees zero-overhead ACID database transactions, predictable in-memory method dispatch, and robust local pessimistic locking.")

add_h2("5.2 Applied Software Design Patterns")
add_p("1. Intercepting Filter Pattern: Implemented via JwtAuthenticationFilter and IdempotencyFilter. Intercepts incoming HTTP requests to validate bearer credentials, calculate payload SHA-256 hashes, and serve cached idempotency responses prior to controller invocation.", bold_prefix="• Filter Pattern: ")
add_p("2. Repository Pattern: Implemented via Spring Data JPA repositories (WalletRepository, PaymentRepository). Decouples business domain entities from database persistence and exposes row-locking query APIs (findByIdWithLock).", bold_prefix="• Repository Pattern: ")
add_p("3. State Machine Pattern: Governs the lifecycle of the Payment entity (PENDING -> CONFIRMED -> REFUNDED or FAILED). Guarantees that invalid state transitions (such as refunding an already refunded or failed transaction) are physically rejected.", bold_prefix="• State Machine Pattern: ")
add_p("4. Strategy / Adapter Pattern: Implemented via PaymentProcessor interfaces to isolate payment gateway execution logic, allowing simulated authorization adapters to be swapped without modifying core wallet ledger services.", bold_prefix="• Strategy Pattern: ")

add_figure(
    "docs/diagrams/png/09_architecture.png",
    "Layered Software Architecture",
    "Tiered representation of Frontend Presentation, Security Filter Chain, Business Domain Services, and Data Access Persistence (authored in Draw.io).",
    "Phase 5: Architecture"
)

add_figure(
    "docs/diagrams/png/10_component.png",
    "UML Component Diagram",
    "Component interfaces and dependency injection bindings connecting controllers, security utilities, and persistence repositories (authored in Draw.io).",
    "Phase 5: Component Design"
)

add_figure(
    "docs/diagrams/png/11_deployment.png",
    "Physical Deployment Architecture",
    "Multi-tier container deployment across Kubernetes Pods, ClusterIP services, MariaDB PVC storage, and Minikube NodePort ingress (authored in Draw.io).",
    "Phase 5: Deployment"
)

add_h2("5.3 Technology Stack and Governance")
tech_headers = ["Layer / Domain", "Technology Choice", "Security Rationale & Governance"]
tech_rows = [
    ["Backend Runtime", "Java 21 LTS / Spring Boot 3.3.4", "Strong typing, virtual threads, robust memory safety, enterprise ecosystem."],
    ["Security Framework", "Spring Security 6 / BCrypt / JWT", "Declarative RBAC, stateless HMAC-SHA256 bearer tokens, OWASP session control."],
    ["Persistence Layer", "Spring Data JPA / Hibernate 6", "ORM parameterized queries eliminating SQL injection, row-level locking APIs."],
    ["Relational Database", "MariaDB 10.11 / In-Memory H2", "ACID transactional boundaries, row-level SELECT ... FOR UPDATE locking, strict schemas."],
    ["Frontend UI", "React 18 / Vite SPA", "Modern componentized architecture, automatic XSS context encoding, zero vulnerable dependencies."],
    ["Containerization", "Docker Multi-Stage (Alpine/Temurin)", "Minimal attack surface, non-root user execution (UID 10001), dropped Linux capabilities."],
    ["Orchestration", "Kubernetes / Minikube", "Declarative YAML manifests, NetworkPolicy egress/ingress isolation, ConfigMap/Secret decoupling."],
    ["SAST & Quality Gate", "SonarQube 9.9.8 LTS / JaCoCo", "Static analysis enforcing zero blocker/critical vulnerabilities, automated coverage metrics."]
]
add_styled_table(tech_headers, tech_rows, [1.5, 2.2, 2.8])

# ==============================================================================
# CHAPTER 6: USER INTERFACE DESIGN & EVIDENCE (PHASE 6)
# ==============================================================================
add_h1("6. User Interface Design and Evidence (Phase 6)")
add_h2("6.1 UI Ergonomics and Security Design Philosophy")
add_p("The frontend application was engineered using React 18 and Vite. Secure UI principles were prioritized throughout: automatic context-sensitive HTML escaping to eliminate XSS, real-time security banners, visual cryptographic pills displaying SHA-256 tamper hashes, clear transaction state badges, revealed credential controls, and explicit adversarial attack simulation sandboxes.")

add_h2("6.2 UI Screen Specifications")
ui_specs_headers = ["Screen ID & Name", "Target User", "Primary Goal", "Key Inputs", "Security Controls & Error Handling"]
ui_specs_rows = [
    ["UI-01: Registration", "New User", "Onboard user account", "Username, Email, Password, Role", "NIST password complexity; client validation; generic duplicate errors."],
    ["UI-02: Authentication", "All Principals", "Authenticate & acquire JWT", "Username, Password", "Generic error on bad credentials; password masking; lockout feedback."],
    ["UI-03: Dashboard", "Customer", "Inspect wallet balance & state", "None (Display only)", "Masked account ID; zero initial balance; active vault security banner."],
    ["UI-04: Top-Up Modal", "Customer", "Fund wallet with simulated money", "Amount ($USD)", "Positive decimal validation; maximum deposit ceiling limit."],
    ["UI-05: Top-Up Success", "Customer", "Verify atomic balance credit", "None (Receipt view)", "Real-time balance update; atomic ledger credit notification."],
    ["UI-06: Merchant Onboard", "Merchant", "Provision business profile", "Business Name", "Input sanitization; settlement wallet automated binding."],
    ["UI-07: Merchant Portal", "Merchant", "Manage business & API keys", "Reveal key button", "High-entropy 256-bit API key revealed on user demand; settlement display."],
    ["UI-08: Checkout Form", "Customer", "Initiate payment to merchant", "Merchant ID, Amount, Description", "Auto-generated UUID Idempotency-Key; positive amount constraint."],
    ["UI-09: Confirmation", "Customer", "Authorize & commit funds", "Submit button", "Atomic execution telemetry; live latency meter; correlation ID."],
    ["UI-10: Receipt View", "Customer", "Verify payment completion", "None (Receipt view)", "SHA-256 digital tamper seal; CONFIRMED status badge; payment ID."],
    ["UI-11: Ledger View", "All Principals", "Inspect double-entry history", "Pagination controls", "Append-only chronological audit rows; debit/credit colored pills."],
    ["UI-12: Refund Dialog", "Merchant/Owner", "Request authorized reversal", "Payment ID, Refund Reason", "State machine check (CONFIRMED only); idempotency tracking."],
    ["UI-13: Refund Success", "Merchant/Owner", "Verify settlement reversal", "None (Confirmation alert)", "Atomic customer credit and merchant debit; REFUNDED status badge."],
    ["UI-14: Defense Lab", "Security Tester", "Simulate replay & tamper attack", "Payload modifiers, Replay trigger", "Live visual demonstration of cached response vs HTTP 409 trap."],
    ["UI-15: SIEM Explorer", "Admin Auditor", "Inspect immutable audit stream", "Action filter, Pagination", "Strict ROLE_ADMIN guard; forensic details, IP address, and outcome."]
]
add_styled_table(ui_specs_headers, ui_specs_rows, [1.4, 1.0, 1.3, 1.2, 1.6])

add_h2("6.3 Empirical UI Screen Captures")
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
    ("docs/evidence/ui/UI-07_merchant_portal.png", "UI-07: Merchant Security Portal & Revealed API Key",
     "Merchant management portal displaying active business status, settlement account, and high-entropy 256-bit API key visibly revealed.", "FR-05, SR-02"),
    ("docs/evidence/ui/UI-08_payment_initiation.png", "UI-08: Payment Initiation Form",
     "Checkout terminal showing target merchant selection, order reference, and auto-generated UUID Idempotency-Key header.", "FR-06, SR-03"),
    ("docs/evidence/ui/UI-09_payment_confirmation.png", "UI-09: Payment Execution & Processing",
     "Live payment processing telemetry verifying atomic customer debit, merchant settlement credit, and correlation ID.", "FR-07, SR-03"),
    ("docs/evidence/ui/UI-10_payment_success_receipt.png", "UI-10: Cryptographic Payment Receipt",
     "Verified digital receipt presenting payment ID, timestamp, and SHA-256 tamper-evident digital seal.", "FR-07, SR-07"),
    ("docs/evidence/ui/UI-11_transaction_history_ledger.png", "UI-11: Tamper-Evident Transaction Ledger",
     "Append-only double-entry financial ledger displaying debit, credit, top-up, and refund records with cryptographic hashes.", "FR-09, SR-07"),
    ("docs/evidence/ui/UI-12_refund_initiation.png", "UI-12: Refund Initiation Modal",
     "Authorized refund dialog visibly open, allowing reason specification and idempotency tracking for transaction reversal.", "FR-08, SR-06"),
    ("docs/evidence/ui/UI-13_refund_success_ledger.png", "UI-13: Refund Success & Ledger Entry",
     "Successful refund notification confirming $65.00 restored to customer balance and updated ledger entry displayed.", "FR-08, SR-06"),
    ("docs/evidence/ui/UI-14_security_tamper_replay_defense.png", "UI-14: Security Tamper & Replay Defense Lab",
     "Adversarial replay simulation showing identical payment retried with unchanged Idempotency-Key. Cached response returned without double debiting.", "SR-03, SR-04"),
    ("docs/evidence/ui/UI-15_admin_audit_logs.png", "UI-15: SIEM Security Audit Explorer",
     "Administrative compliance view showing populated chronological audit trail of authentication, mutations, and replay traps.", "FR-10, SR-08")
]

for img_p, title, desc, tag in ui_evidence:
    add_figure(img_p, title, desc, tag, width=Inches(5.8))

# ==============================================================================
# CHAPTER 7: THREAT MODELING & SECURITY ANALYSIS (PHASE 7)
# ==============================================================================
add_h1("7. Threat Modeling and Security Analysis (Phase 7)")
add_h2("7.1 Asset Identification & CIA Triad")
add_p("Systematic threat modeling commenced by cataloging the eight primary assets comprising the gateway ecosystem, analyzing their confidentiality, integrity, and availability valuations:")
asset_headers = ["Asset ID & Name", "Asset Owner", "Confidentiality", "Integrity", "Availability", "Asset Valuation Rationale"]
asset_rows = [
    ["AST-01: Wallet Balances", "Customer / Merchant", "Medium", "Critical", "High", "Integrity failure leads directly to double-spending or unauthorized overdraft."],
    ["AST-02: Password Hashes", "Identity Service", "Critical", "Critical", "Medium", "Confidentiality loss enables offline dictionary or credential stuffing attacks."],
    ["AST-03: JWT Signing Keys", "Auth Service", "Critical", "Critical", "High", "Compromise allows adversary to forge arbitrary tokens with ROLE_ADMIN."],
    ["AST-04: Merchant API Keys", "Registered Merchant", "Critical", "Critical", "High", "Leaked keys allow adversary to trigger automated settlement actions."],
    ["AST-05: Payment Records", "Payment Engine", "Medium", "Critical", "High", "Falsification corrupts transaction reconciliation and billing audits."],
    ["AST-06: Ledger Transactions", "Financial Vault", "Low", "Critical", "High", "Immutable double-entry book of records; tampering violates accounting rules."],
    ["AST-07: Idempotency Records", "Filter Engine", "Low", "Critical", "Critical", "Loss enables replay attacks; corruption leads to duplicate debits."],
    ["AST-08: SIEM Audit Logs", "Compliance Auditor", "Medium", "Critical", "High", "Tampering destroys forensic evidence during breach investigations."]
]
add_styled_table(asset_headers, asset_rows, [1.3, 1.1, 0.9, 0.9, 0.8, 1.5])

add_h2("7.2 STRIDE Threat Classification")
stride_headers = ["Threat ID", "STRIDE Category", "Target Component", "Attacker Motivation", "Countermeasure Applied"]
stride_rows = [
    ["THR-01", "Spoofing", "AuthController", "Credential stuffing / account takeover", "BCrypt hashing (cost 12), ephemeral JWT with expiration."],
    ["THR-02", "Tampering", "PaymentController", "Modify transaction amount in flight", "SHA-256 payload digest binding; HTTPS transport encryption."],
    ["THR-03", "Repudiation", "TransactionRepository", "Deny initiating payment or refund", "Cryptographically hashed audit records & immutable ledger."],
    ["THR-04", "Information Disclosure", "WalletController", "Inspect foreign wallet balances (BOLA)", "Ownership authorization assertions on all principal queries."],
    ["THR-05", "Denial of Service", "Tomcat Thread Pool", "Exhaust database pool via request spam", "HikariCP connection pool limits, idempotency fast-fail."],
    ["THR-06", "Elevation of Privilege", "AdminController", "Access SIEM logs without admin role", "Spring Security @PreAuthorize(\"hasRole('ADMIN')\") check."],
    ["THR-07", "Tampering", "WalletRepository", "Concurrent double spending race", "Pessimistic row locking (PESSIMISTIC_WRITE) at DB level."],
    ["THR-08", "Spoofing", "IdempotencyFilter", "Replay intercepted payment request", "Mandatory Idempotency-Key cache returning original receipt."],
    ["THR-09", "Tampering", "RefundService", "Issue duplicate or excessive refund", "Strict Payment state machine; only CONFIRMED payments eligible."],
    ["THR-10", "Information Disclosure", "AuditLogger", "Leak plaintext credentials in logs", "Centralized regex scrubbing of PAN, CVV, and passwords."]
]
add_styled_table(stride_headers, stride_rows, [0.7, 1.2, 1.3, 1.8, 1.5])

add_h2("7.3 Analysis of Sensitive Information Flows Across Trust Boundaries")
add_p("1. Flow 1: Customer Credential Flow (Client -> AuthController -> AuthService -> MariaDB). Traverses Untrusted Internet into DMZ. Threat: Eavesdropping and brute-force credential stuffing. Mitigations: Enforce HTTPS TLS 1.3 transport encryption, BCrypt cost 12 adaptive password hashing, and generic error responses preventing username enumeration.", bold_prefix="• Flow 1: ")
add_p("2. Flow 2: Payment Payload & Card Simulation Flow (Client -> IdempotencyFilter -> PaymentController -> WalletService -> MariaDB). Traverses Trust Boundary between presentation and domain services. Threat: In-flight parameter tampering and replay attacks. Mitigations: SHA-256 request body hashing bound to UUID Idempotency-Key, MariaDB pessimistic locking on wallet rows, and atomic double-entry ledger transaction commit.", bold_prefix="• Flow 2: ")
add_p("3. Flow 3: Idempotency Token Flow (Client -> IdempotencyFilter -> IdempotencyRepository -> MariaDB). Intercepts every POST mutation. Threat: Token collision and altered payload injection. Mitigations: Dual verification—asserting token existence AND payload digest equality. Mismatched digests trigger immediate HTTP 409 Conflict rejection.", bold_prefix="• Flow 3: ")

add_h2("7.4 Vulnerabilities Analysis and Qualitative Risk Matrix")
vuln_headers = ["Vuln ID", "CWE Mapping", "Vulnerability Description", "CVSS v3.1", "Architectural Defense"]
vuln_rows = [
    ["VULN-01", "CWE-362", "Concurrent Race Condition in Balance Debit", "High (8.1)", "Pessimistic DB row locking (@Lock(PESSIMISTIC_WRITE))."],
    ["VULN-02", "CWE-294", "Payment Transaction Replay Attack", "High (7.5)", "Mandatory Idempotency-Key header with SHA-256 binding."],
    ["VULN-03", "CWE-285", "Broken Object Level Authorization (BOLA)", "High (7.8)", "Ownership verification against SecurityContext principal."],
    ["VULN-04", "CWE-20", "Improper Input Validation (Negative Amounts)", "Medium (6.5)", "Jakarta Validation (@Positive, @NotNull) and DB constraints."],
    ["VULN-05", "CWE-79", "Stored Cross-Site Scripting (XSS)", "Medium (5.4)", "React automated context encoding; HTML entity escaping."],
    ["VULN-06", "CWE-319", "Cleartext Transmission of Sensitive Telemetry", "Medium (5.3)", "Enforced HTTPS TLS; regex scrubbing of logs."]
]
add_styled_table(vuln_headers, vuln_rows, [0.8, 0.9, 2.2, 0.9, 1.7])

add_figure(
    "docs/diagrams/png/17_stride_threat_model.png",
    "STRIDE Threat Matrix and Mitigation Model",
    "Systematic mapping of threat categories to architectural defense controls and security verification gates (authored in Draw.io).",
    "Phase 7: Threat Modeling"
)

# ==============================================================================
# CHAPTER 8: ATTACK TREE ANALYSIS (PHASE 8)
# ==============================================================================
add_h1("8. Attack Tree Analysis (Phase 8)")
add_h2("8.1 Attacker Goal: Double Spending and Balance Theft")
add_p("The primary objective of a financial adversary targeting the gateway is to execute Double Spending—spending identical wallet funds multiple times before balances synchronize, or forcing balance inversions below zero.")

add_figure(
    "docs/diagrams/png/18_attack_tree.png",
    "Attack Tree Decomposition: Double Spending & Gateway Tampering",
    "Hierarchical attack paths detailing race condition exploitation, replay interception, parameter tampering, and mitigation barriers (authored in Draw.io).",
    "Phase 8: Attack Tree"
)

add_h2("8.2 Attack Path Mitigation & Defense Mapping")
attack_headers = ["Attack Node ID", "Attacker Action / Vector", "Target Weakness", "Countermeasure & Verification"]
attack_rows = [
    ["AT-1.1", "Fire 10 simultaneous threads to drain $100 balance", "Check-then-act race window", "Pessimistic row lock serializes threads; 8 rejected."],
    ["AT-1.2", "Intercept network request and replay raw POST packet", "Unchecked idempotent state", "IdempotencyFilter traps key, returns original receipt."],
    ["AT-2.1", "Replay valid Idempotency-Key with altered $500 amount", "Token reuse tampering", "SHA-256 digest mismatch detected; HTTP 409 Conflict."],
    ["AT-3.1", "Submit refund for already refunded transaction", "Missing state transition guard", "Payment FSM asserts status == CONFIRMED; rejects refund."],
    ["AT-3.2", "Non-owner attempts to refund foreign merchant payment", "BOLA authorization bypass", "Principal ownership check blocks request with HTTP 403."],
    ["AT-4.1", "Inject negative decimal (-$1000) in payment or top-up", "Unbounded numeric input", "Jakarta @Positive validation and MariaDB CHECK constraint."]
]
add_styled_table(attack_headers, attack_rows, [0.8, 2.0, 1.8, 1.9])

add_figure(
    "docs/diagrams/png/19_security_architecture.png",
    "Refined Security Architecture & Defense Layers",
    "Layered defensive barriers: Ingress Gateway -> JWT Auth -> Idempotency Cache -> Pessimistic DB Lock -> SIEM Logger (authored in Draw.io).",
    "Phase 8: Security Architecture"
)

# ==============================================================================
# CHAPTER 9: PRODUCT BACKLOG (PHASE 9)
# ==============================================================================
add_h1("9. Product Backlog and Jira/Scrum (Phase 9)")
add_h2("9.1 Backlog Structure and User Story Specifications")
add_p("The product backlog was structured into 8 functional and security epics encompassing 13 prioritized work items. Story estimation used Fibonacci planning poker points based on complexity, architectural risk, and security validation requirements. Every user story is formulated using the standard format: 'As a [role], I want [capability], so that [benefit]' with explicit acceptance criteria.")

backlog_headers = ["Key", "Story ID", "Epic", "SP", "Sprint", "User Story Specification & Acceptance Criteria"]
backlog_rows = [
    ["DWPG-10", "STORY-01", "DWPG-2: Auth", "5", "Sprint 1", "As a User, I want secure registration & JWT auth, so that my account is protected. Criteria: BCrypt cost 12, signed JWT, generic error msgs."],
    ["DWPG-11", "STORY-02", "DWPG-3: Wallet", "5", "Sprint 1", "As a Customer, I want wallet creation & simulated top-up, so that I can hold funds. Criteria: BOLA owner check, non-negative balance."],
    ["DWPG-12", "STORY-03", "DWPG-3: Wallet", "3", "Sprint 1", "As a Merchant, I want registration & API key generation, so that I can receive funds. Criteria: 256-bit API key, XSS sanitization."],
    ["DWPG-13", "STORY-04", "DWPG-4: Payment", "8", "Sprint 1", "As a Customer, I want payment initiation, so that I can purchase items. Criteria: Double-entry accounting, atomic debit/credit."],
    ["DWPG-14", "STORY-05", "DWPG-6: Security", "5", "Sprint 1", "As an Auditor, I want security audit logging, so that events are recorded. Criteria: Append-only table, credential scrubbing."],
    ["DWPG-15", "DEF-001", "DWPG-6: Security", "5", "S1 -> S2", "BUG: Fix race condition & duplicate payment defect via pessimistic locking. Criteria: Pass 10-thread parallel fuzz test."],
    ["DWPG-16", "STORY-06", "DWPG-6: Security", "5", "Sprint 2", "As a System, I want pessimistic row locking on wallets, so that double spending is prevented. Criteria: SELECT ... FOR UPDATE query."],
    ["DWPG-17", "STORY-07", "DWPG-6: Security", "5", "Sprint 2", "As a System, I want mandatory Idempotency-Key validation, so that replays are rejected. Criteria: HTTP 409 on altered payload."],
    ["DWPG-18", "STORY-08", "DWPG-5: Refunds", "5", "Sprint 2", "As a Merchant, I want refund processing, so that returned transactions credit customer. Criteria: Payment status CONFIRMED only."],
    ["DWPG-19", "STORY-09", "DWPG-5: Refunds", "3", "Sprint 2", "As a User, I want immutable transaction history, so that I can verify all movements. Criteria: BOLA isolation, tamper hashes."],
    ["DWPG-20", "STORY-10", "DWPG-6: Security", "5", "Sprint 2", "As an Admin, I want a SIEM audit explorer, so that I can inspect attacks in real time. Criteria: ROLE_ADMIN enforcement."],
    ["DWPG-21", "STORY-11", "DWPG-7: DevSecOps", "3", "Sprint 2", "As a DevSecOps Eng, I want non-root Docker & K8s NetworkPolicies, so that pods are hardened. Criteria: UID 10001, isolate-mariadb."],
    ["DWPG-22", "STORY-12", "DWPG-8: Testing", "3", "Sprint 2", "As a QA Eng, I want automated regression & fuzz testing, so that regressions are blocked. Criteria: 100% pass on security suite."]
]
add_styled_table(backlog_headers, backlog_rows, [0.7, 0.7, 1.0, 0.4, 0.6, 3.1])

# ==============================================================================
# CHAPTER 10: SPRINT EXECUTION AND SCRUM METRICS (PHASE 10)
# ==============================================================================
add_h1("10. Sprint Execution and Scrum Metrics (Phase 10)")
add_h2("10.1 Two-Sprint Cadence Summary")
add_p("• Sprint 1 Focus: Core MVP architecture, authentication, wallet provisioning, merchant onboarding, and initial payment processing. Committed: 26 Story Points. Completed: 21 Story Points. Defect DEF-001 (5 SP) identified during concurrency testing was carried over to Sprint 2 for comprehensive architectural remediation.")
add_p("• Sprint 2 Focus: Security hardening, pessimistic database row locking, mandatory idempotency token cache, multi-role refund processing, Docker containerization, Minikube Kubernetes deployment, and automated security test suite. Committed: 26 Story Points. Completed: 26 Story Points (100% velocity achieved).")

add_h2("10.2 Defect DEF-001 Lifecycle")
add_p("Defect DEF-001 ('Race Condition and Duplicate Balance Debit') was flagged on Day 8 of Sprint 1 when automated multi-threaded tests demonstrated that two simultaneous $50 payments against a $50 balance both succeeded, resulting in an illicit -$50 overdraft. Root cause analysis revealed non-atomic check-then-act logic in WalletService. The defect was assigned 5 Story Points, transitioned through the 4-column Scrum board (TO DO -> IN PROGRESS -> TESTING -> CARRIED OVER), and resolved in Sprint 2 via pessimistic database row locking.")

add_h2("10.3 Scrum Metrics Analysis")
scrum_metrics_headers = ["Metric Dimension", "Sprint 1 Delivered", "Sprint 2 Delivered", "Aggregated Project Total"]
scrum_metrics_rows = [
    ["Committed Story Points", "26 SP", "26 SP", "52 SP"],
    ["Delivered Story Points", "21 SP", "26 SP", "47 SP (90.4% total delivery rate)"],
    ["Carried Over Story Points", "5 SP (DEF-001)", "0 SP", "0 SP residual debt"],
    ["Defect Escape Rate", "1 Defect (caught in QA)", "0 Defects escaped", "0 Defects to production"],
    ["Sprint Burndown Slope", "Disrupted on Day 8 (-5 SP)", "Ideal linear slope to 0 SP", "100% Sprint 2 completion rate"],
    ["Automated Test Pass Rate", "91.3% (Defect DEF-001 failed)", "100% (42/42 tests passing)", "100% Final verification status"]
]
add_styled_table(scrum_metrics_headers, scrum_metrics_rows, [1.8, 1.5, 1.5, 1.7])

jira_evidence = [
    ("docs/evidence/jira/JIRA-01_jira_board_overview.png", "JIRA-01: DWPG Jira Project & Board Overview",
     "Atlassian Jira project configuration showing DWPG Board #101, Scrum cadence, and 52 total committed story points.", "Phase 10: Jira Configuration"),
    ("docs/evidence/jira/JIRA-02_product_backlog.png", "JIRA-02: Product Backlog Prioritization View",
     "Complete product backlog view displaying all 13 work items, user story specifications, priorities, and acceptance criteria.", "Phase 9: Product Backlog"),
    ("docs/evidence/jira/JIRA-03_sprint1_planning.png", "JIRA-03: Sprint 1 Planning Scope Allocation",
     "Sprint 1 scope commitment comprising 26 Story Points allocated across core MVP user stories.", "Phase 10: Sprint 1 Planning"),
    ("docs/evidence/jira/JIRA-04_sprint1_scrum_board.png", "JIRA-04: Sprint 1 Active Scrum Board",
     "Sprint 1 review state displaying 4-column workflow (TO DO, IN PROGRESS, TESTING, DONE) with Defect DEF-001 in TESTING carried over.", "Phase 10: Sprint 1 Board"),
    ("docs/evidence/jira/JIRA-05_sprint1_burndown.png", "JIRA-05: Sprint 1 Burndown Chart",
     "Burndown curve illustrating velocity drop on Day 8 due to discovery of concurrency race condition defect DEF-001.", "Phase 10: Sprint 1 Burndown"),
    ("docs/evidence/jira/JIRA-06_sprint2_planning.png", "JIRA-06: Sprint 2 Planning & Hardening Scope",
     "Sprint 2 scope allocation comprising 26 Story Points focused on row locking, idempotency, K8s, and QA.", "Phase 10: Sprint 2 Planning"),
    ("docs/evidence/jira/JIRA-07_sprint2_scrum_board.png", "JIRA-07: Sprint 2 Active Scrum Board",
     "Final Sprint 2 Scrum board with 4 columns showing 100% of user stories and carried-over defect DEF-001 closed in DONE column.", "Phase 10: Sprint 2 Board"),
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
     "Jira Epic card detailing academic evidence validation across all 16 Secure Software Engineering phases.", "Phase 9: Epic DWPG-9"),
    ("docs/evidence/jira/JIRA-17_daily_scrum.png", "JIRA-17: Daily Scrum Standup Meeting Record",
     "Jira Daily Standup log capturing Yesterday, Today, and Blockers across Lead Architect, FullStack Developer, and QA Security Engineer.", "Phase 10: Daily Scrum"),
    ("docs/evidence/jira/JIRA-18_retrospective.png", "JIRA-18: Sprint 2 Retrospective Record",
     "Jira Sprint Retrospective documenting What Went Well, What Could Be Improved, and 2 concrete Action Items for future engineering.", "Phase 10: Retrospective")
]

for img_p, title, desc, tag in jira_evidence:
    add_figure(img_p, title, desc, tag, width=Inches(5.8))

# ==============================================================================
# CHAPTER 11: DEVSECOPS, TESTING & SECURE DEPLOYMENT
# ==============================================================================
add_h1("11. DevSecOps, Testing and Containerized Deployment (Phases 11-15)")
add_h2("11.1 Secure Development and Build Controls (Phase 11)")
add_p("The development build pipeline incorporates five distinct automated security controls:")
add_p("1. Maven Dependency Lock & SHA Verification: All external dependencies are pinned to immutable releases in pom.xml to prevent dependency confusion attacks.", bold_prefix="• Control 1: ")
add_p("2. Automated Code Coverage Enforcement: JaCoCo plugin enforces a mandatory minimum instruction coverage threshold (>60%) across core domain logic.", bold_prefix="• Control 2: ")
add_p("3. Static Application Security Testing (SAST): Integrated SonarQube quality gate scanner checking for OWASP Top 10 vulnerabilities during the compile phase.", bold_prefix="• Control 3: ")
add_p("4. Git Secret Scanning: Automated TruffleHog scanner executing on every push to detect accidentally committed tokens, passwords, or private keys.", bold_prefix="• Control 4: ")
add_p("5. Hardened Compiler Flags: Strict Java 21 compilation with deprecation warnings treated as errors and null-pointer static analysis checks enabled.", bold_prefix="• Control 5: ")

add_h2("11.2 SonarQube SAST Code Quality & Security Review (Phase 11 & 14)")
add_p("Static Application Security Testing (SAST) was performed using SonarQube 9.9.8 LTS running in Docker against project key `dwpg-simulator`. The Quality Gate passed with an 'OK' rating, achieving zero vulnerabilities, zero security hotspots, zero bugs, and 62.6% code coverage.")

sonar_evidence = [
    ("docs/evidence/sonarqube/SONAR-01_project_overview.png", "SONAR-01: SonarQube Project Overview",
     "Authenticated SonarQube dashboard showing Quality Gate Passed (Green), 0 Bugs, 0 Vulnerabilities, 0 Hotspots, and 62.6% Coverage.", "Phase 11: Quality Gate"),
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

add_h2("11.3 Containerization with Docker (Phase 13)")
add_p("The backend and frontend are packaged using multi-stage Dockerfiles. The backend build utilizes Eclipse Temurin OpenJDK 21 for compilation and packages the runnable JAR on a minimal Alpine runtime. Execution is strictly constrained to an unprivileged non-root user (UID 10001, GID 10001) with all Linux capabilities dropped (`cap_drop: ALL`).")

add_figure(
    "docs/diagrams/png/20_docker_architecture.png",
    "Multi-Stage Docker Container Architecture",
    "Multi-stage build pipelines isolating Maven compile dependencies from lightweight runtime containers (authored in Draw.io).",
    "Phase 13: Docker Architecture"
)

add_figure(
    "docs/evidence/docker/DOCKER-01_containers_live.png",
    "Verified Live Docker Runtime Status",
    "Terminal capture of running containers verifying sonarqube, dwpg-mariadb-local, and Minikube virtualization engine.",
    "Phase 13: Docker Evidence"
)

add_h2("11.4 Kubernetes Orchestration and Minikube (Phase 13)")
add_p("Production deployment is orchestrated via 11 declarative Kubernetes manifests deployed into the dedicated `dwpg` namespace on Minikube. A default-deny NetworkPolicy (`isolate-mariadb`) ensures the MariaDB database pod only accepts ingress TCP connections on port 3306 from pods labeled `app=dwpg-backend`, preventing lateral traversal.")

add_figure(
    "docs/diagrams/png/21_kubernetes_architecture.png",
    "Kubernetes Pod Topology and Network Isolation",
    "Cluster architecture illustrating dwpg namespace, ConfigMap/Secret bindings, and NetworkPolicy firewall barriers (authored in Draw.io).",
    "Phase 13: Kubernetes Architecture"
)

add_figure(
    "docs/evidence/kubernetes/K8S-01_cluster_workloads.png",
    "Verified Live Kubernetes Workloads in dwpg Namespace",
    "Terminal capture of kubectl get all,networkpolicy -n dwpg verifying healthy pods, services, and isolated network policies.",
    "Phase 13: Kubernetes Evidence"
)

add_h2("11.5 CI/CD Pipeline and Git Version Control (Phase 14)")
add_p("The continuous integration and delivery pipeline is configured via GitHub Actions (`.github/workflows/ci.yml`). Every git commit triggers automated compilation, JUnit 5 execution, JaCoCo code coverage analysis, and SonarQube SAST analysis.")

add_figure(
    "docs/diagrams/png/22_cicd_pipeline.png",
    "DevSecOps CI/CD Pipeline Workflow",
    "Automated pipeline stages: Git Push -> Build -> Unit Test -> SAST Scan -> Quality Gate -> Container Build -> K8s Deploy (authored in Draw.io).",
    "Phase 14: CI/CD Pipeline"
)

add_figure(
    "docs/diagrams/png/23_security_testing_pipeline.png",
    "Automated Security Testing Pipeline Architecture",
    "Integration of static code analysis (SonarQube), dynamic concurrency testing, and fuzzing checks (authored in Draw.io).",
    "Phase 14: Security Pipeline"
)

add_figure(
    "docs/evidence/git/GIT-01_git_commit_graph.png",
    "Git Commit Audit Trail & Semantic Versioning History",
    "Terminal capture of git log --graph --oneline verifying chronological commits for all 16 academic phases.",
    "Phase 11: Git Audit Trail"
)

add_h2("11.6 Automated Test Suite and Security Verification (Phase 14)")
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

# ==============================================================================
# CHAPTER 12: SECURE CODING & REFACTORING (PHASE 12)
# ==============================================================================
add_h1("12. Secure Coding and Refactoring (Phase 12)")
add_h2("12.1 Defect DEF-001 Remediation: Pessimistic Row Locking")
add_p("As detailed in Phase 1 and Phase 10, the discovery of DEF-001 necessitated refactoring the persistence tier to use pessimistic write locks. The code below illustrates the exact before-and-after implementation:")

add_code_block("DEF-001 Fix: Repository Method Refactoring",
"""// BEFORE: Vulnerable optimistic/unlocked query allows race conditions
public interface WalletRepository extends JpaRepository<Wallet, Long> {
    Optional<Wallet> findByUserId(Long userId);
}

// AFTER: Pessimistic Row Locking forces MariaDB SELECT ... FOR UPDATE
public interface WalletRepository extends JpaRepository<Wallet, Long> {
    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("SELECT w FROM Wallet w WHERE w.userId = :userId")
    Optional<Wallet> findByUserIdWithLock(@Param("userId") Long userId);
}""")

add_h2("12.2 Replay Attack Remediation: Idempotency Service")
add_p("The second major refactoring addressed transaction replays. When an incoming payment arrives with an Idempotency-Key, the system calculates a SHA-256 hash of the request body and verifies whether a record already exists:")

add_code_block("Replay Fix: Idempotency Service Logic",
"""@Service
public class IdempotencyService {
    @Transactional
    public Optional<IdempotencyRecord> checkReplay(String key, String payloadHash) {
        Optional<IdempotencyRecord> existing = repo.findByIdempotencyKey(key);
        if (existing.isPresent()) {
            if (!existing.get().getPayloadHash().equals(payloadHash)) {
                // Adversary modified parameters under existing key!
                auditService.logEvent(AuditEventType.REPLAY_DETECTED, "TAMPER_DETECTED");
                throw new IdempotencyTamperingException("Payload mismatch for key: " + key);
            }
            // Legitimate retry: return cached response
            return existing;
        }
        return Optional.empty();
    }
}""")

# ==============================================================================
# CHAPTER 13: LOGGING, SIEM & HARDENING (PHASE 15)
# ==============================================================================
add_h1("13. Logging, SIEM and System Hardening (Phase 15)")
add_h2("13.1 Twelve Core Security Event Types")
add_p("The AuditService records twelve distinct security event types defined in the AuditEventType enum:")
event_headers = ["Event Type Enum", "Triggering Condition", "Recorded Telemetry Fields", "SIEM Threat Severity"]
event_rows = [
    ["LOGIN_SUCCESS", "Principal successfully authenticated with valid credentials.", "Actor, IP, Timestamp, Outcome", "Informational"],
    ["LOGIN_FAILURE", "Authentication failed due to incorrect password or bad username.", "Actor, IP, Timestamp, Details", "Warning (Brute-Force)"],
    ["AUTHORIZATION_FAILURE", "Authenticated user attempted accessing unprivileged role endpoint.", "Actor, Resource ID, IP, Outcome", "High (Privilege Escalation)"],
    ["WALLET_CREATED", "New digital wallet provisioned for user account.", "Actor, Wallet ID, IP, Outcome", "Informational"],
    ["FUNDS_ADDED", "Customer deposited simulated funds into wallet balance.", "Actor, Amount, IP, Timestamp", "Informational"],
    ["PAYMENT_INITIATED", "Payment checkout transaction received and validated.", "Actor, Merchant ID, Amount, Key", "Informational"],
    ["PAYMENT_CONFIRMED", "Payment successfully settled via double-entry ledger commit.", "Actor, Payment ID, Tamper Hash", "Informational (Financial)"],
    ["PAYMENT_FAILED", "Payment rejected due to insufficient balance or domain error.", "Actor, Error Message, IP, Key", "Low"],
    ["PAYMENT_REFUNDED", "Confirmed payment successfully reversed and restored.", "Actor, Payment ID, Reversal Amt", "Informational (Financial)"],
    ["REPLAY_DETECTED", "Duplicate Idempotency-Key submitted with mismatched payload.", "Actor, Idempotency Key, IP", "Critical (Fraud Attempt)"],
    ["DUPLICATE_PAYMENT", "Duplicate transaction intercepted and served from cache.", "Actor, Payment ID, Original Timestamp", "Notice"],
    ["SUSPICIOUS_ACTIVITY", "Excessive request rate or anomalous parameter patterns.", "Actor, IP, Trigger Pattern", "High (Adversarial Activity)"]
]
add_styled_table(event_headers, event_rows, [1.5, 2.0, 1.8, 1.2])

add_h2("13.2 Five Key Security Monitoring Telemetry Metrics")
telemetry_headers = ["Telemetry Metric", "Baseline Normal Range", "Alert Threshold", "Forensic Investigation Protocol"]
telemetry_rows = [
    ["Failed Login Rate", "< 2% of total auth attempts", "> 5 failures / min per IP", "Temporarily rate-limit IP; verify potential credential stuffing."],
    ["Replay Attack Rejection Rate", "0 incidents under normal operation", ">= 1 incident", "Inspect Idempotency-Key and payload diff in SIEM Explorer."],
    ["Lock Wait Time (Pessimistic)", "< 15 ms average lock acquisition", "> 500 ms wait time", "Check for thread contention; investigate potential concurrency burst."],
    ["Payment Rejection Rate", "< 5% (legitimate low funds)", "> 20% within 10 min window", "Audit user balances; check for scripted overdraft probing."],
    ["Refund-to-Payment Ratio", "< 3% of settled transactions", "> 15% ratio per merchant", "Flag merchant account for review; assess dispute abuse."]
]
add_styled_table(telemetry_headers, telemetry_rows, [1.6, 1.6, 1.5, 1.8])

add_h2("13.3 Twelve-Domain System Hardening Checklist")
hardening_headers = ["Hardening Domain", "Applied Hardening Configuration", "Audit Verification Status"]
hardening_rows = [
    ["1. Authentication", "BCrypt cost factor 12; NIST SP 800-63B password complexity.", "VERIFIED"],
    ["2. Session Management", "Stateless HMAC-SHA256 JWT tokens; strict 1-hour expiration.", "VERIFIED"],
    ["3. Authorization (RBAC)", "Method-level @PreAuthorize; strict separation of USER, MERCHANT, ADMIN.", "VERIFIED"],
    ["4. Database Concurrency", "SELECT ... FOR UPDATE pessimistic row locks; READ_COMMITTED isolation.", "VERIFIED"],
    ["5. Idempotency & Replay", "Mandatory Idempotency-Key with SHA-256 payload binding.", "VERIFIED"],
    ["6. Input Validation", "Jakarta Validation (@Positive, @NotNull); DB level CHECK constraints.", "VERIFIED"],
    ["7. Sensitive Data Protection", "Regex scrubbing of PAN, CVV, passwords; zero plaintext credentials.", "VERIFIED"],
    ["8. Container Hardening", "Multi-stage Docker builds; unprivileged user UID 10001; dropped capabilities.", "VERIFIED"],
    ["9. Network Isolation", "Kubernetes default-deny NetworkPolicy isolating MariaDB on port 3306.", "VERIFIED"],
    ["10. Secrets Governance", "Kubernetes Secrets decoupled from source control; zero hardcoded tokens.", "VERIFIED"],
    ["11. SAST Governance", "SonarQube Quality Gate enforced with 0 blocker/critical issues.", "VERIFIED"],
    ["12. Forensic Logging", "Append-only immutable audit_logs table; IP address & correlation IDs.", "VERIFIED"]
]
add_styled_table(hardening_headers, hardening_rows, [1.8, 3.4, 1.3])

add_h2("13.4 Physical and Operational Security Controls")
add_p("• Physical Isolation: In production, database servers are isolated in secure data center enclaves with biometric multi-factor access control and 24/7 video surveillance. Virtualized containers run in private VPC subnets with zero direct public IP exposure.")
add_p("• Operational Governance: Administrative access is strictly restricted to designated Site Reliability Engineers (SRE) connecting over mutual-TLS bastion hosts with session recording and mandatory peer approvals.")

# ==============================================================================
# CHAPTER 14: TRACEABILITY AND CONCLUSION (PHASE 16)
# ==============================================================================
add_h1("14. Traceability Matrix and Conclusion (Phase 16)")
add_h2("14.1 End-to-End Requirement-to-Artifact Traceability Matrix")
add_p("The traceability matrix ensures full bidirectional verification linking initial requirements to UML models, database schemas, code classes, automated test cases, and academic evidence artifacts.")

trace_headers = ["Req ID", "Phase / Category", "Design & UML Model", "Source Implementation", "Automated Test Case", "Academic Evidence"]
trace_rows = [
    ["FR-01", "Phase 2 / Auth", "UC-01, DFD 1.0 (D-03, D-07)", "AuthController, AuthService", "TC-AUTH-001, AuthServiceTest", "UI-01, JIRA-09"],
    ["FR-02", "Phase 2 / Auth", "Sequence Diagram (D-12)", "JwtTokenProvider, SecurityConfig", "TC-AUTH-002, SEC-TEST-001", "UI-02, JIRA-09"],
    ["FR-03", "Phase 2 / Wallet", "ERD (D-05), DFD 2.0 (D-07)", "WalletController, WalletService", "TC-WAL-001, WalletServiceTest", "UI-03, JIRA-10"],
    ["FR-04", "Phase 2 / Wallet", "Analysis Model (D-04)", "WalletService.fundWallet", "TC-WAL-002, SEC-TEST-002", "UI-04, UI-05, JIRA-10"],
    ["FR-05", "Phase 2 / Merchant", "ERD (D-05)", "MerchantController, MerchantService", "TC-MER-001", "UI-06, UI-07, JIRA-10"],
    ["FR-06", "Phase 2 / Payment", "Sequence Diagram (D-14)", "PaymentController.initiatePayment", "TC-PAY-001, SEC-TEST-003", "UI-08, JIRA-11"],
    ["FR-07", "Phase 2 / Payment", "Component Model (D-10)", "PaymentService.processPayment", "TC-PAY-001, PaymentConcurrencyTest", "UI-09, UI-10, JIRA-11"],
    ["FR-08", "Phase 2 / Refund", "Sequence Diagram (D-15)", "RefundController, RefundService", "TC-REF-001, SEC-TEST-006", "UI-12, UI-13, JIRA-12"],
    ["FR-09", "Phase 2 / Ledger", "ERD (D-05), DFD 3.0 (D-07)", "TransactionController, TransactionService", "TC-LED-001", "UI-11, JIRA-12"],
    ["FR-10", "Phase 2 / SIEM", "Trust Boundary (D-08)", "AdminController, AuditService", "TC-ADM-001, SEC-TEST-008", "UI-15, JIRA-13"],
    ["SR-03", "Phase 7 / Replay", "Attack Tree (D-18), Seq (D-16)", "IdempotencyService, IdempotencyRecord", "SEC-TEST-003, SEC-TEST-004", "UI-14, JIRA-13"],
    ["SR-04", "Phase 7 / Concurrency", "Security Arch (D-19)", "WalletRepository.findByUserIdWithLock", "PaymentConcurrencyTest (10 th)", "JIRA-04, JIRA-13"]
]
add_styled_table(trace_headers, trace_rows, [0.6, 0.9, 1.2, 1.6, 1.4, 0.8])

add_figure(
    "docs/diagrams/png/24_traceability_matrix.png",
    "Requirements-to-Verification Traceability Model",
    "Bidirectional graph mapping functional requirements, threat vectors, security controls, and verification evidence (authored in Draw.io).",
    "Phase 16: Traceability Matrix"
)

add_h2("14.2 Academic Evidence Checklist")
check_headers = ["Phase", "Curricular Requirement", "Implemented Artifact", "Verification Status"]
check_rows = [
    ["Phase 1", "Agile Process & Approach", "Scrum 2-sprint plan, daily standup logs, retrospective", "VERIFIED (Figure 1, Draw.io D-01)"],
    ["Phase 2", "Requirements Engineering", "10 Functional, 6 NFR, 8 Security Requirements documented", "VERIFIED (Tables 3-5)"],
    ["Phase 3", "Requirements Analysis & UML", "Context, Use Case, BCE Analysis, 5 Sequence Diagrams", "VERIFIED (Figures 2-9, Draw.io D-02..04, D-12..16)"],
    ["Phase 4", "Data & Information Flow", "3NF ERD, DFD Level 0, DFD Level 1, Trust Perimeter", "VERIFIED (Figures 10-13, Draw.io D-05..08)"],
    ["Phase 5", "Software Architecture", "Layered Architecture, Component, Physical Deployment", "VERIFIED (Figures 14-16, Draw.io D-09..11)"],
    ["Phase 6", "User Interface Design", "15 High-res real Playwright UI screenshots (UI-01..15)", "VERIFIED (Figures 17-31)"],
    ["Phase 7", "Threat Modeling (STRIDE)", "8 Assets CIA, 10 STRIDE threats, DREAD scoring, 6 Vulns", "VERIFIED (Figure 32, Draw.io D-17)"],
    ["Phase 8", "Attack Tree Analysis", "Double spending attack tree & refined security architecture", "VERIFIED (Figures 33-34, Draw.io D-18..19)"],
    ["Phase 9", "Product Backlog & Jira", "13 Stories in Jira, product-backlog.csv, 8 Epics", "VERIFIED (Table 9, Figure 36)"],
    ["Phase 10", "Sprint Metrics & Scrum", "18 Authentic Jira figures (JIRA-01..18), burndown curves", "VERIFIED (Figures 35-52)"],
    ["Phase 11", "Secure Build Environment", "Maven, JaCoCo, SonarQube LTS integration (7 figures)", "VERIFIED (Figures 53-59)"],
    ["Phase 12", "Secure Coding & Refactoring", "Pessimistic DB row locking, BCrypt cost 12, Idempotency", "VERIFIED (Chapter 12 Code Blocks)"],
    ["Phase 13", "Docker & Kubernetes", "Multi-stage Dockerfile, 11 K8s YAMLs in dwpg namespace", "VERIFIED (Figures 60-63, Draw.io D-20..21)"],
    ["Phase 14", "CI/CD & Security Testing", "GitHub Actions ci.yml, 42 automated tests (100% pass)", "VERIFIED (Figures 64-66, Draw.io D-22..23, Table 12)"],
    ["Phase 15", "Logging, SIEM & Hardening", "Centralized AuditService, 12 event types, NetworkPolicy", "VERIFIED (Chapter 13 Tables, Figure 31)"],
    ["Phase 16", "Final Security Review", "Traceability matrix, compliance report, zero vulnerabilities", "VERIFIED (Figure 67, Draw.io D-24)"]
]
add_styled_table(check_headers, check_rows, [0.7, 1.8, 2.7, 1.3])

add_h2("14.3 Residual Risks, Limitations, and Future Work")
add_p("1. High-Contention Database Lock Latency: Under extreme concurrent load against a single hot wallet (e.g. flash-sale merchant settlement wallet), pessimistic row locking introduces queueing latency. Mitigation: Implement Redis distributed locks with optimistic retry backoff or partition high-traffic merchant balances across sub-accounts.", bold_prefix="• Residual Risk 1: ")
add_p("2. Idempotency Key Storage Growth: The relational idempotency cache table grows linearly with transaction volume. Mitigation: Configure scheduled MariaDB partition pruning or transition historical idempotency records to a TTL-indexed Redis cluster after 24 hours.", bold_prefix="• Residual Risk 2: ")
add_p("3. JWT Invalidation Latency: Stateless JWT tokens cannot be revoked before their 1-hour expiration without introducing a shared token blacklist. Mitigation: Shorten JWT access token lifetimes to 15 minutes paired with rotating refresh tokens stored in HTTP-only secure cookies.", bold_prefix="• Residual Risk 3: ")

add_p("1. Simulated Financial Rails: The application strictly simulates balances and settlements without integrating with real clearinghouses (Fedwire, ACH, SWIFT) or handling international currency FX conversions.", bold_prefix="• Limitation 1: ")
add_p("2. In-Cluster Database Architecture: The MariaDB instance runs as a single Kubernetes pod backed by persistent storage rather than a multi-region active-active cluster (e.g. MariaDB Galera or CockroachDB).", bold_prefix="• Limitation 2: ")

add_p("1. Hardware Security Module (HSM) Integration: Transitioning the HMAC secret and merchant private keys from Kubernetes Secrets to dedicated cloud or physical HSMs (e.g. AWS CloudHSM or HashiCorp Vault with PKCS#11).", bold_prefix="• Future Work 1: ")
add_p("2. Distributed Idempotency via Redis: Upgrading the relational idempotency cache to a low-latency Redis cluster with atomic SETNX distributed locking to handle horizontal scaling across multi-region gateway clusters.", bold_prefix="• Future Work 2: ")
add_p("3. Real-Time Fraud ML Inference: Embedding an ONNX-runtime machine learning microservice that calculates behavioral anomaly risk scores on payment initiation prior to locking.", bold_prefix="• Future Work 3: ")

add_h2("14.4 Closing Summary")
add_p("The Digital Wallet and Payment Gateway Simulator represents a fully engineered, robustly tested, and empirically validated academic capstone submission. Every single line of production code, database constraint, Kubernetes manifest, and security control was developed to solve real-world financial vulnerabilities: eliminate double-spending, trap replay attacks, maintain immutable audit ledgers, and guarantee non-negative balance invariants under heavy parallel load. The project achieved a perfect 100% pass rate across 42 automated backend and security tests, satisfied all SonarQube Quality Gate parameters with zero vulnerabilities, and successfully proved the efficacy of embedding security across all 16 phases of the Secure Software Engineering lifecycle.")

print(f"Saving final report to {OUTPUT_DOCX}...")
doc.save(OUTPUT_DOCX)
print("Master Capstone Report (.docx) successfully generated!")
