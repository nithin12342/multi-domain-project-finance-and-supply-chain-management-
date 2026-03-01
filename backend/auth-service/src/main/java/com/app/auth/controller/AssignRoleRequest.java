package com.app.auth.controller;

import com.app.auth.model.UserRole;

public class AssignRoleRequest {
    private String userId;
    private UserRole role;

    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public UserRole getRole() {
        return role;
    }

    public void setRole(UserRole role) {
        this.role = role;
    }
}
