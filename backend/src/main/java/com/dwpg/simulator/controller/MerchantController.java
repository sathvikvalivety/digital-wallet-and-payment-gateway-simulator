package com.dwpg.simulator.controller;

import com.dwpg.simulator.dto.MerchantRequest;
import com.dwpg.simulator.dto.MerchantResponse;
import com.dwpg.simulator.security.SecurityUtils;
import com.dwpg.simulator.service.MerchantService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/merchants")
public class MerchantController {

    private final MerchantService merchantService;

    public MerchantController(MerchantService merchantService) {
        this.merchantService = merchantService;
    }

    @PostMapping
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<MerchantResponse> registerMerchant(@Valid @RequestBody MerchantRequest request) {
        String username = SecurityUtils.getCurrentUsername();
        MerchantResponse response = merchantService.registerMerchant(request, username);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping("/me")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<MerchantResponse> getMyMerchantProfile() {
        String username = SecurityUtils.getCurrentUsername();
        return ResponseEntity.ok(merchantService.getMerchantByUsername(username));
    }

    @GetMapping("/{id}")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<MerchantResponse> getMerchantById(@PathVariable("id") Long id) {
        return ResponseEntity.ok(merchantService.getMerchantById(id));
    }
}
