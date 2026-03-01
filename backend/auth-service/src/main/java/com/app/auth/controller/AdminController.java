package com.app.auth.controller;

import com.app.auth.model.User;
import com.app.auth.service.AdminService;
import com.app.common.dto.ApiResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/admin")
@PreAuthorize("hasRole('ADMIN')")
public class AdminController {

    @Autowired
    private AdminService adminService;

    @GetMapping("/users")
    public ResponseEntity<?> getAllUsers() {
        List<User> users = adminService.getAllUsers();
        return ResponseEntity.ok(new ApiResponse<>(users, "All users retrieved"));
    }

    @PostMapping("/roles/assign")
    public ResponseEntity<?> assignRole(@RequestBody AssignRoleRequest request) {
        adminService.assignRole(request.getUserId(), request.getRole());
        return ResponseEntity.ok(new ApiResponse<>(null, "Role assigned successfully"));
    }
}
