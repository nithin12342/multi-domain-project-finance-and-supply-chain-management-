package com.app.auth.controller;

import com.app.auth.model.User;
import com.app.auth.service.AuthService;
import com.app.common.dto.ApiResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    private AuthService authService;

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginRequest request) {
        String token = authService.authenticate(request.getEmail(), request.getPassword());
        return ResponseEntity.ok(new ApiResponse<>(token, "Login successful"));
    }

    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody RegisterRequest request) {
        User user = authService.registerUser(request);
        return ResponseEntity.ok(new ApiResponse<>(user, "User registered successfully"));
    }

    @GetMapping("/user")
    public ResponseEntity<?> getCurrentUser(@RequestHeader("Authorization") String token) {
        User user = authService.getCurrentUser(token);
        return ResponseEntity.ok(new ApiResponse<>(user, "User details retrieved"));
    }

    @PostMapping("/logout")
    public ResponseEntity<?> logout(@RequestHeader("Authorization") String token) {
        authService.logout(token);
        return ResponseEntity.ok(new ApiResponse<>(null, "Logged out successfully"));
    }
}
