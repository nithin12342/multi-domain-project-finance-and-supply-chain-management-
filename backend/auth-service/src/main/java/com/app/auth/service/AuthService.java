package com.app.auth.service;

import com.app.auth.controller.RegisterRequest;
import com.app.auth.model.User;
import com.app.auth.model.UserRole;
import com.app.auth.repository.UserRepository;
import com.app.auth.security.JwtTokenProvider;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Autowired
    private JwtTokenProvider jwtTokenProvider;

    @Autowired
    private AuthenticationManager authenticationManager;

    public String authenticate(String email, String password) {
        // Authenticate user and generate token
        try {
            User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("User not found"));
            
            if (!passwordEncoder.matches(password, user.getPassword())) {
                throw new RuntimeException("Invalid credentials");
            }

            return jwtTokenProvider.generateToken(user);
        } catch (Exception e) {
            throw new RuntimeException("Authentication failed: " + e.getMessage());
        }
    }

    public User registerUser(RegisterRequest request) {
        // Check if user exists
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new RuntimeException("Email already registered");
        }

        // Create new user
        User user = new User();
        user.setEmail(request.getEmail());
        user.setPassword(passwordEncoder.encode(request.getPassword()));
        user.setName(request.getName());
        user.setRole(UserRole.USER);

        return userRepository.save(user);
    }

    public User getCurrentUser(String token) {
        String userId = jwtTokenProvider.getUserIdFromToken(token);
        return userRepository.findById(userId)
            .orElseThrow(() -> new RuntimeException("User not found"));
    }

    public void logout(String token) {
        // Invalidate token
        jwtTokenProvider.invalidateToken(token);
    }
}
