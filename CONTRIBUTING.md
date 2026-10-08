# Contributing to Digital Wallet and Payment Gateway Simulator (DWPG)

Thank you for contributing to the DWPG Secure Software Engineering project.

## Development Workflow & Branching Strategy
We adhere to GitFlow adapted for DevSecOps:
- `main`: Production-ready code, tagged with releases.
- `develop`: Integration branch for sprint deliverables.
- `feature/<name>`: New functional features branched off `develop`.
- `security/<name>`: Security hardening, threat mitigations, and SAST fixes.
- `fix/<name>`: Defect repairs and regression fixes.

## Commit Message Convention
All commit messages must follow Conventional Commits:
- `feat(scope): ...`
- `fix(scope): ...`
- `security(scope): ...`
- `test(scope): ...`
- `docs(scope): ...`
- `refactor(scope): ...`
- `chore(scope): ...`

## Security Requirements Before Pull Request / Commit
1. Verify no secrets are committed (`git grep -i "secret\|password\|token"`).
2. Execute full automated test suite (`mvn clean test`).
3. Ensure SonarQube SAST scan passes with Zero Security Hotspots and Zero Vulnerabilities.
4. Verify Docker container builds cleanly without root privileges.
