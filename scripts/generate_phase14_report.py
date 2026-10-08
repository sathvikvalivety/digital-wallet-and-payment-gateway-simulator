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
    run_title = p_title.add_run("PHASE 14: CI/CD AND SECURITY TESTING SPECIFICATION\nDEVSECOPS PIPELINE & AUTOMATED QUALITY GATES")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(20)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(30, 58, 138)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("Automated Build, Test, SAST, DAST, Trivy Container Scanning & K8s IaC Governance\nCourse: 24CYS401 Secure Software Engineering | Academic Year 2026")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(10.5)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_paragraph()

    # Meta Table
    table = doc.add_table(rows=5, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta = [
        ("Pipeline System", "GitHub Actions DevSecOps Workflow (.github/workflows/ci.yml)"),
        ("SAST & SCA Engines", "SonarQube 9.9 LTS, JaCoCo Coverage Agent, OWASP Ruleset"),
        ("Container Vulnerability Scanner", "Aqua Security Trivy (CRITICAL & HIGH Severity Gate)"),
        ("IaC Linter", "Kubeconform (Kubernetes v1.28+ Schema Validation)"),
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
    doc.add_heading("1. Executive DevSecOps Pipeline Strategy", level=1)
    doc.add_paragraph(
        "Modern secure software engineering requires embedding automated security validations directly into the software "
        "delivery pipeline (Shift-Left Security). Rather than treating security as an afterthought or manual pre-release gate, "
        "the DWPG project implements a multi-stage GitHub Actions CI/CD workflow that executes on every push and pull request. "
        "Builds failing security thresholds are blocked automatically, preventing vulnerable code or container images from "
        "reaching production."
    )

    # Section 2
    doc.add_heading("2. Six-Stage Automated DevSecOps Pipeline Architecture", level=1)
    doc.add_paragraph(
        "The pipeline is structured into six sequential and parallel security jobs:"
    )

    stages = [
        ("Stage 1: Unit & Concurrency Testing", "backend-test-and-sast", "Executes 25 JUnit 5 test cases including 10-thread parallel race-condition stress testing and 12 boundary input fuzzing probes. All tests must pass with 0 failures."),
        ("Stage 2: Code Coverage Enforcement", "jacoco-maven-plugin", "Measures branch and statement coverage. Fails if coverage drops below 60%. Current measured coverage: 62.6%."),
        ("Stage 3: Static Application Security Testing", "SonarQube SAST", "Performs deep semantic AST scanning for OWASP Top 10 vulnerabilities, CWE compliance, hardcoded secrets, and code smells. Enforces Quality Gate = OK."),
        ("Stage 4: Frontend Static Verification", "frontend-build-and-lint", "Validates React 18 / Vite syntax, builds optimized static bundles, and verifies zero bundling or module resolution errors."),
        ("Stage 5: Container Image Vulnerability Scan", "aquasecurity/trivy-action", "Packages hardened Docker images and executes Trivy scanning on Alpine JRE and Nginx layers, checking for unpatched CVEs in OS libraries."),
        ("Stage 6: Kubernetes Manifest IaC Linting", "kubeconform", "Performs schema-level validation against Kubernetes v1.28 API specifications for all 11 manifests in k8s/, ensuring Pod Security Standards compliance.")
    ]

    t_stages = doc.add_table(rows=7, cols=3)
    t_stages.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_hdr = t_stages.rows[0]
    for i, h in enumerate(["Pipeline Stage", "Automated Tooling", "Security Validation Objective"]):
        s_hdr.cells[i].paragraphs[0].add_run(h).font.bold = True
        set_cell_background(s_hdr.cells[i], "1E3A8A")
        s_hdr.cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    for idx, (stg, tool, obj) in enumerate(stages, start=1):
        row = t_stages.rows[idx]
        row.cells[0].paragraphs[0].add_run(stg).font.bold = True
        row.cells[0].paragraphs[0].runs[0].font.size = Pt(8.5)
        row.cells[1].paragraphs[0].add_run(tool).font.size = Pt(8.5)
        row.cells[2].paragraphs[0].add_run(obj).font.size = Pt(8.5)
        bg = "F8FAFC" if idx % 2 == 1 else "FFFFFF"
        for c in row.cells:
            set_cell_background(c, bg)

    doc.add_paragraph()

    # Section 3
    doc.add_heading("3. Automated Quality Gate Policy Matrix", level=1)
    doc.add_paragraph(
        "The following policy rules determine whether a pull request is accepted or rejected by the CI/CD engine:"
    )

    t_rules = doc.add_table(rows=7, cols=4)
    t_rules.alignment = WD_TABLE_ALIGNMENT.CENTER
    r_hdr = t_rules.rows[0]
    for i, h in enumerate(["Security Metric", "Allowed Maximum", "Observed Baseline", "Pipeline Action"]):
        r_hdr.cells[i].paragraphs[0].add_run(h).font.bold = True
        set_cell_background(r_hdr.cells[i], "334155")
        r_hdr.cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    rules_data = [
        ("Blocker / Critical Vulnerabilities", "0 Allowed", "0 (Verified)", "FAIL Pipeline if > 0"),
        ("Unreviewed Security Hotspots", "0 Allowed", "0 (Verified)", "FAIL Pipeline if > 0"),
        ("Automated Test Failures", "0 Allowed", "0 of 25 Failed", "FAIL Pipeline if > 0"),
        ("Code Coverage Threshold", ">= 60.0%", "62.6%", "FAIL Pipeline if < 60%"),
        ("Duplicated Code Density", "< 3.0%", "0.0%", "FAIL Pipeline if >= 3%"),
        ("Trivy CRITICAL Container CVEs", "0 Allowed", "0 Unfixed", "FAIL Pipeline if > 0")
    ]

    for idx, (m, a, o, p) in enumerate(rules_data, start=1):
        row = t_rules.rows[idx]
        row.cells[0].paragraphs[0].add_run(m).font.bold = True
        row.cells[0].paragraphs[0].runs[0].font.size = Pt(8.5)
        row.cells[1].paragraphs[0].add_run(a).font.size = Pt(8.5)
        row.cells[2].paragraphs[0].add_run(o).font.size = Pt(8.5)
        row.cells[3].paragraphs[0].add_run(p).font.size = Pt(8.5)
        bg = "F8FAFC" if idx % 2 == 1 else "FFFFFF"
        for c in row.cells:
            set_cell_background(c, bg)

    doc.add_paragraph()

    # Section 4
    doc.add_heading("4. Branch Protection & Governance Policies", level=1)
    doc.add_paragraph(
        "To protect the integrity of the production codebase, GitHub repository branch protection rules enforce:\n"
        "1. Mandatory Pull Requests: Direct pushes to 'main' are restricted; all changes require an approved pull request.\n"
        "2. Mandatory Status Checks: The 'backend-test-and-sast', 'frontend-build-and-lint', and 'container-security-scan' "
        "jobs must complete successfully before any PR can be merged.\n"
        "3. Linear History: Merge commits are prohibited in favor of fast-forward squashes or rebased commits to preserve clean auditability.\n"
        "4. Secret Scanning & Push Protection: Commits containing unencrypted tokens, credentials, or private keys are rejected at push time."
    )

    doc.save("docs/14-cicd/cicd-pipeline.docx")
    print("Report written to docs/14-cicd/cicd-pipeline.docx")

if __name__ == "__main__":
    create_report()
