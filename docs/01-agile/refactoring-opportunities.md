# Refactoring Opportunities in Secure Payment Processing

This document identifies two concrete, production-grade refactoring opportunities in the Digital Wallet and Payment Gateway Simulator (DWPG), demonstrating how architectural and code refactorings improve both security and maintainability.

---

## Refactoring Opportunity 1: Non-Atomic Wallet Balance Updates to Pessimistic Database Locking

### Context
In an initial naive implementation, checking a sender's wallet balance and deducting the amount are executed in separate standard JPA read and write operations. Under concurrent transaction execution (e.g., rapid parallel API requests), a Time-of-Check to Time-of-Use (TOCTOU) race condition allows double spending.

### BEFORE (Vulnerable Naive Implementation)
```java
// Naive implementation prone to Race Conditions / Double Spending
@Transactional
public PaymentResponse processPayment(PaymentRequest request) {
    Wallet senderWallet = walletRepository.findById(request.getSenderWalletId())
        .orElseThrow(() -> new ResourceNotFoundException("Wallet not found"));

    // Check balance (Time-of-Check)
    if (senderWallet.getBalance().compareTo(request.getAmount()) < 0) {
        throw new InsufficientFundsException("Insufficient balance");
    }

    // SIMULATED LATENCY / NETWORK DELAY (Window of Vulnerability)
    simulateNetworkDelay();

    // Deduct and Save (Time-of-Use)
    senderWallet.setBalance(senderWallet.getBalance().subtract(request.getAmount()));
    walletRepository.save(senderWallet);

    Payment payment = new Payment(senderWallet, request.getMerchantId(), request.getAmount(), PaymentStatus.CONFIRMED);
    return paymentRepository.save(payment).toResponse();
}
```

### AFTER (Refactored Secure Implementation)
```java
// Secure refactored implementation with Pessimistic Write Locking & Strict Validation
@Transactional(isolation = Isolation.READ_COMMITTED)
public PaymentResponse processPayment(PaymentRequest request, String authenticatedUsername) {
    // 1. Lock wallet row exclusively in MariaDB (SELECT ... FOR UPDATE)
    Wallet senderWallet = walletRepository.findByIdForUpdate(request.getSenderWalletId())
        .orElseThrow(() -> new ResourceNotFoundException("Wallet not found"));

    // 2. Validate Ownership against authenticated principal (BOLA prevention)
    if (!senderWallet.getUser().getUsername().equals(authenticatedUsername)) {
        throw new AccessDeniedException("Unauthorized access to foreign wallet");
    }

    // 3. Strict positive balance and sufficiency checks
    if (request.getAmount().compareTo(BigDecimal.ZERO) <= 0) {
        throw new InvalidAmountException("Payment amount must be positive");
    }
    if (senderWallet.getBalance().compareTo(request.getAmount()) < 0) {
        throw new InsufficientFundsException("Insufficient funds available");
    }

    // 4. Atomic balance deduction
    senderWallet.debit(request.getAmount());
    walletRepository.save(senderWallet);

    // 5. Merchant balance credit (with lock)
    Wallet merchantWallet = walletRepository.findByMerchantIdForUpdate(request.getMerchantId())
        .orElseThrow(() -> new ResourceNotFoundException("Merchant wallet not found"));
    merchantWallet.credit(request.getAmount());
    walletRepository.save(merchantWallet);

    // 6. Record transaction and audit
    Payment payment = Payment.builder()
        .senderWallet(senderWallet)
        .merchantWallet(merchantWallet)
        .amount(request.getAmount())
        .status(PaymentStatus.CONFIRMED)
        .build();
    paymentRepository.save(payment);
    auditService.logEvent(AuditEventType.PAYMENT_CONFIRMED, payment.getId(), authenticatedUsername, "SUCCESS");

    return payment.toResponse();
}
```

### Why It Is Better
- **Atomicity & Isolation:** The refactored version uses `LockModeType.PESSIMISTIC_WRITE` on the wallet entity, forcing the database engine to acquire an exclusive row lock (`SELECT ... FOR UPDATE`). Concurrent requests targeting the same wallet are serialized at the database boundary.
- **Security Improvement:** Eliminates the Double-Spending vulnerability (CWE-362 / TOCTOU). Prevents negative balances regardless of concurrent request volume. Enforces ownership verification to thwart Broken Object Level Authorization (OWASP API1:2023).
- **Maintainability Improvement:** Encapsulates domain invariants (`debit()`, `credit()`) inside the `Wallet` aggregate root rather than mutating state directly in procedural service code.

---

## Refactoring Opportunity 2: Ad-Hoc Request Validation to Centralized Idempotency Filter/Service

### Context
Initially, duplicate request detection was handled haphazardly within individual service methods or omitted entirely. Network retries and client replay attacks caused duplicate charges.

### BEFORE (Ad-Hoc / Absent Idempotency)
```java
// Payment controller directly processing payments without idempotency enforcement
@PostMapping("/pay")
public ResponseEntity<PaymentResponse> initiatePayment(@RequestBody PaymentRequest request) {
    // No idempotency key validation
    // If the network times out and client retries, a duplicate payment is created!
    PaymentResponse response = paymentService.processPayment(request);
    return ResponseEntity.ok(response);
}
```

### AFTER (Refactored Unified Idempotency Service)
```java
// Centralized Idempotency enforcement pattern with SHA-256 payload binding
@Transactional
public PaymentResponse processIdempotentPayment(String idempotencyKey, PaymentRequest request, String username) {
    if (idempotencyKey == null || idempotencyKey.trim().isEmpty()) {
        throw new MissingHeaderException("Idempotency-Key header is mandatory for payment transactions");
    }

    String requestHash = cryptographicService.computeSha256(request.toString());

    Optional<IdempotencyRecord> existingRecord = idempotencyRepository.findByKeyForUpdate(idempotencyKey);
    if (existingRecord.isPresent()) {
        IdempotencyRecord record = existingRecord.get();
        // Check payload tampering: if same key is reused with different parameters, reject as replay/tamper!
        if (!record.getRequestHash().equals(requestHash)) {
            auditService.logSecurityAlert(AuditEventType.REPLAY_DETECTED, idempotencyKey, username, "TAMPERED_PAYLOAD");
            throw new IdempotencyTamperingException("Idempotency key reused with mismatched request parameters");
        }
        // Return existing cached response without repeating debit
        auditService.logEvent(AuditEventType.DUPLICATE_PAYMENT, record.getResourceId(), username, "IDEMPOTENT_REPLAY_RETURNED");
        return jsonSerializer.deserialize(record.getResponseBody(), PaymentResponse.class);
    }

    // Process new payment atomically
    PaymentResponse response = paymentService.executePayment(request, username);

    // Save idempotency record with cached serialized response
    IdempotencyRecord newRecord = IdempotencyRecord.builder()
        .idempotencyKey(idempotencyKey)
        .requestHash(requestHash)
        .resourceId(response.getPaymentId())
        .responseBody(jsonSerializer.serialize(response))
        .createdAt(Instant.now())
        .build();
    idempotencyRepository.save(newRecord);

    return response;
}
```

### Why It Is Better
- **Deterministic Replay Handling:** Complies with IETF RFC Draft specification for Idempotency-Key HTTP headers. Guarantees that network retries return identical results without repeated financial mutations.
- **Security Improvement:** Thwarts Replay Attacks (CWE-294) and Parameter Tampering. If an attacker intercepts and resubmits a valid idempotency key with altered amounts or destinations, the hash mismatch immediately triggers an alert and halts processing.
- **Maintainability Improvement:** Centralizes idempotency semantics into a reusable service architecture, isolating transaction execution from deduplication caching logic.
