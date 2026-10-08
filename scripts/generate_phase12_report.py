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
    run_title = p_title.add_run("PHASE 12: SECURE CODING AND REFACTORING EVIDENCE\nDEFECT REMEDIATION & ARCHITECTURAL HARDENING")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(20)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(30, 58, 138)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("Formal Evidence of Concurrency Protection, Idempotency Safeguards & Defensive Engineering\nCourse: 24CYS401 Secure Software Engineering | Academic Year 2026")
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
        ("Defect Identifiers", "DEF-001 (Double Spending / Race Condition), SEC-004 (Replay Attack)"),
        ("Remediation Strategy", "Pessimistic Row-Locking + JVM Striped Synchronization + SHA-256 Idempotency Cache"),
        ("Automated Test Suite", "JUnit 5 + Spring Boot Test (25 Tests: Concurrency, Fuzzing, BOLA, Idempotency)"),
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
    doc.add_heading("1. Executive Technical Summary", level=1)
    doc.add_paragraph(
        "During Sprint 1 of the development lifecycle, defect DEF-001 was identified during multi-threaded stress testing: "
        "when multiple concurrent HTTP payment requests were dispatched simultaneously against the same wallet, race conditions "
        "allowed concurrent reads of identical balance snapshots before debit mutations could be committed. "
        "This resulted in either double-spending anomalies or unhandled optimistic locking exceptions (StaleObjectStateException). "
        "Phase 12 documents the secure coding refactoring and defense-in-depth architecture implemented to guarantee 100% "
        "financial transaction integrity."
    )

    # Section 2
    doc.add_heading("2. Defect DEF-001: Race Condition & Double-Spending Remediation", level=1)
    doc.add_paragraph(
        "Vulnerability Profile:\n"
        "• CWE Identifier: CWE-362 (Concurrent Execution using Shared Resource with Improper Synchronization - 'Race Condition')\n"
        "• OWASP Top 10: A04:2021 - Insecure Design\n"
        "• Threat Impact: A malicious actor could execute simultaneous parallel checkout requests exceeding their available balance, "
        "artificially creating funds out of nothing and causing insolvency."
    )

    doc.add_heading("Flawed Implementation (Before Refactoring):", level=2)
    doc.add_paragraph(
        "In the initial prototype, WalletService performed simple non-locked entity lookups, followed by memory subtraction and save. "
        "Even when Hibernate @Version optimistic locking was tried, concurrent collisions threw raw unchecked exceptions that crashed "
        "caller transactions rather than cleanly serializing debit operations:"
    )

    before_code = """// VULNERABLE PROTOTYPE: Non-locked read-then-write pattern
@Transactional
public PaymentResponse processPayment(PaymentRequest req, String username) {
    // 1. Unlocked read - multiple threads read balance = $100 simultaneously
    Wallet wallet = walletRepository.findByUserUsername(username).orElseThrow();
    
    // 2. Both threads evaluate ($100 >= $50) as TRUE!
    if (wallet.getBalance().compareTo(req.getAmount()) < 0) {
        throw new InsufficientFundsException("Insufficient funds");
    }
    
    // 3. Both threads deduct $50 and write balance = $50 (Double Spend!)
    wallet.setBalance(wallet.getBalance().subtract(req.getAmount()));
    walletRepository.save(wallet);
    ...
}"""
    add_code_block(doc, before_code)

    doc.add_heading("Hardened Implementation (After Refactoring - Defense in Depth):", level=2)
    doc.add_paragraph(
        "To achieve enterprise-grade resilience, a two-tier defense-in-depth model was architected:\n"
        "1. Database Row-Level Pessimistic Locking: The WalletRepository method findByUserIdForUpdate() applies "
        "@Lock(LockModeType.PESSIMISTIC_WRITE) generating 'SELECT ... FOR UPDATE' in MariaDB. Any concurrent database transaction "
        "targeting the same wallet is placed in a locked queue until the active transaction completes.\n"
        "2. Striped JVM Synchronization: To prevent thread pool starvation and database lock contention under high load, "
        "PaymentService implements a ConcurrentHashMap of lock objects striped per user identity. Threads for the same user serialize "
        "before entering the transaction boundary, while distinct users execute fully in parallel."
    )

    after_code = """// HARDENED ARCHITECTURE: Striped User Lock + Pessimistic Row Lock
public PaymentResponse processPayment(PaymentRequest request, String username, 
                                      String idempotencyKey, String clientIp) {
    // Tier 1: JVM-level striped reentrant synchronization per user
    Object userLock = userLocks.computeIfAbsent(username, k -> new Object());
    synchronized (userLock) {
        // Tier 2: Managed TransactionTemplate boundary
        return transactionTemplate.execute(status -> {
            // Tier 3: Database row-level pessimistic write lock (SELECT FOR UPDATE)
            Wallet wallet = walletRepository.findByUserIdForUpdate(user.getId())
                    .orElseThrow(() -> new ResourceNotFoundException("Wallet not found"));

            // Strict domain invariant debit evaluation
            wallet.debit(request.getAmount());
            walletRepository.save(wallet);
            ...
        });
    }
}"""
    add_code_block(doc, after_code)

    doc.add_heading("Automated Concurrency Stress Test Evidence:", level=2)
    doc.add_paragraph(
        "The concurrency protection was verified via 'PaymentConcurrencyTest.java':\n"
        "• Test Scenario: Wallet initialized with exactly $100.00. 10 parallel threads simultaneously submit $50.00 debit requests.\n"
        "• Mathematical Verification: Exactly 2 requests must succeed (2 x $50 = $100); exactly 8 requests must fail with "
        "InsufficientFundsException; final wallet balance must be exactly $0.00.\n"
        "• Test Execution Result: PASSED (10 parallel threads, 2 successful debits, 8 rejections, 0 double spends, 0 deadlocks)."
    )

    doc.add_paragraph()

    # Section 3
    doc.add_heading("3. Case Study: Idempotency & Replay Attack Defense (SEC-004, SEC-005)", level=1)
    doc.add_paragraph(
        "Vulnerability Profile:\n"
        "• CWE Identifier: CWE-294 (Authentication Bypass by Capture-replay) / CWE-799 (Improper Control of Interaction Frequency)\n"
        "• Threat Scenario: Network timeouts or attacker packet capture replaying valid payment requests to trigger unauthorized duplicate debits."
    )

    doc.add_heading("Architectural Solution: IdempotencyService", level=2)
    doc.add_paragraph(
        "All mutating payment and refund endpoints mandate the 'Idempotency-Key' HTTP header. "
        "The system hashes the request payload (amount, merchant ID, description) using SHA-256 and records the execution result:\n"
        "1. First Request: Key not present in database -> Transaction executes atomically -> Response cached in IdempotencyRecord.\n"
        "2. Identical Duplicate (Replay): Key present + Hash matches -> Mutation bypassed -> Cached HTTP response returned instantly.\n"
        "3. Tampered Replay: Key present + Hash mismatch -> Attack flagged -> REPLAY_DETECTED event logged -> HTTP 400 rejected."
    )

    idemp_code = """// Idempotency Validation & Tamper Verification
Optional<IdempotencyRecord> existingOpt = idempotencyRecordRepository.findByIdempotencyKey(key);
if (existingOpt.isPresent()) {
    IdempotencyRecord existing = existingOpt.get();
    if (!existing.getRequestHash().equals(currentPayloadSha256)) {
        // Payload modified with reused key -> Flag Tamper & Reject
        auditService.logEvent(AuditEventType.REPLAY_DETECTED, existing.getResourceId(), 
                              username, "FAILED", "Replay/Tampering attempt detected", clientIp);
        throw new IdempotencyException("Idempotency key reused with modified parameters. Replay rejected.");
    }
    // Identical duplicate -> Return cached response safely
    auditService.logEvent(AuditEventType.DUPLICATE_PAYMENT, existing.getResourceId(),
                          username, "SUCCESS", "Idempotent duplicate returned from cache", clientIp);
    return Optional.of(existing);
}"""
    add_code_block(doc, idemp_code)

    doc.add_heading("Automated Idempotency Test Evidence:", level=2)
    doc.add_paragraph(
        "Verified via 'PaymentSecurityIntegrationTest.java':\n"
        "• Test 1: testIdempotentPaymentRequestReturnsCachedResponse() -> Replayed request returns identical HTTP 200 and payment ID.\n"
        "• Test 2: testReplayAttackWithModifiedPayloadRejected() -> Tampered payload with reused key returns HTTP 400 error."
    )

    doc.add_paragraph()

    # Section 4
    doc.add_heading("4. Case Study: Broken Object Level Authorization (BOLA / IDOR) Defense", level=1)
    doc.add_paragraph(
        "Vulnerability Profile: CWE-639 (Authorization Bypass Through User-Controlled Key) / OWASP API Security Top 10 API1:2023.\n"
        "Threat Scenario: A logged-in attacker modifies the wallet ID parameter in the URL from /api/wallet/10 to /api/wallet/11 "
        "to inspect another user's balance and transaction history."
    )

    doc.add_paragraph(
        "Secure Coding Control: WalletService and TransactionService strictly enforce ownership validation by cross-referencing "
        "the authenticated SecurityContext username against the resource owner's username:"
    )

    bola_code = """@Transactional(readOnly = true)
public Wallet getWalletById(Long walletId, String authenticatedUsername) {
    Wallet wallet = walletRepository.findById(walletId)
            .orElseThrow(() -> new ResourceNotFoundException("Wallet not found: " + walletId));
    
    // BOLA / IDOR Defense Check
    if (!wallet.getUser().getUsername().equals(authenticatedUsername)) {
        auditService.logEvent(AuditEventType.AUTHORIZATION_FAILURE, walletId, authenticatedUsername, 
                              "FAILED", "BOLA Violation: Attempted unauthorized read of foreign wallet");
        throw new UnauthorizedAccessException("Forbidden: You do not own wallet ID " + walletId);
    }
    return wallet;
}"""
    add_code_block(doc, bola_code)

    doc.add_paragraph()

    # Section 5
    doc.add_heading("5. Case Study: Boundary Input Fuzzing & Injection Robustness", level=1)
    doc.add_paragraph(
        "Verified via 'PaymentInputFuzzingTest.java' across 12 adversarial boundary attack vectors:\n"
        "• Negative amounts (-100.00, -0.01) -> HTTP 400 Rejected\n"
        "• Zero amount (0.00) -> HTTP 400 Rejected\n"
        "• Overflow amounts (10,000,000.00) -> HTTP 400 Rejected\n"
        "• Fractional sub-cent precision (10.005) -> HTTP 400 Rejected\n"
        "• SQL Injection payloads (\"' OR '1'='1\") -> Parameterized JPA Query Safe\n"
        "• Cross-Site Scripting payloads (\"<script>alert(1)</script>\") -> Escaped & Redacted Safe\n"
        "• Null and empty Idempotency-Key headers -> HTTP 400 Rejected"
    )

    doc.add_paragraph()

    # Section 6
    doc.add_heading("6. Refactoring Summary Matrix", level=1)
    t_summary = doc.add_table(rows=5, cols=4)
    t_summary.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_hdr = t_summary.rows[0]
    for i, h in enumerate(["Security Dimension", "Pre-Refactoring State", "Post-Refactoring Architecture", "Verification Proof"]):
        s_hdr.cells[i].paragraphs[0].add_run(h).font.bold = True
        set_cell_background(s_hdr.cells[i], "1E3A8A")
        s_hdr.cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    refactors = [
        ("Concurrency / Double-Spending", "Unlocked JPA Read/Write", "JVM Striped Lock + MariaDB PESSIMISTIC_WRITE", "PaymentConcurrencyTest (10 Threads)"),
        ("Replay Attacks", "No request uniqueness check", "SHA-256 Digest + Idempotency-Key Cache", "PaymentSecurityIntegrationTest"),
        ("Tenant Isolation (BOLA)", "Implicit URL trust", "Explicit SecurityContext Ownership Check", "WalletServiceTest (BOLA Suite)"),
        ("Input Validation", "Ad-hoc checks", "Jakarta Bean Validation + Fuzzing Tests", "PaymentInputFuzzingTest (12 Vectors)")
    ]

    for idx, (dim, pre, post, proof) in enumerate(refactors, start=1):
        row = t_summary.rows[idx]
        row.cells[0].paragraphs[0].add_run(dim).font.bold = True
        row.cells[0].paragraphs[0].runs[0].font.size = Pt(8.5)
        row.cells[1].paragraphs[0].add_run(pre).font.size = Pt(8.5)
        row.cells[2].paragraphs[0].add_run(post).font.size = Pt(8.5)
        row.cells[3].paragraphs[0].add_run(proof).font.size = Pt(8.5)
        bg = "F8FAFC" if idx % 2 == 1 else "FFFFFF"
        for c in row.cells:
            set_cell_background(c, bg)

    doc.save("docs/12-secure-coding/refactoring-evidence.docx")
    print("Report written to docs/12-secure-coding/refactoring-evidence.docx")

if __name__ == "__main__":
    create_report()
