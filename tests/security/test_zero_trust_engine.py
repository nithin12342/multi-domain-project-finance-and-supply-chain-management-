
import sys
import os
import pytest
from datetime import datetime, timedelta
# Add the project root to the Python path
sys.path.insert(0, r'c:\Users\thela\OneDrive\Desktop\personal projets\multi domain supply chain and finance project\supplychain-finance-platform')

from security.advanced.zero_trust_architecture import (
    ZeroTrustEngine,
    AccessRequest,
    UserContext,
    ThreatLevel,
)

@pytest.fixture
def zt_engine():
    """Fixture for a ZeroTrustEngine instance."""
    return ZeroTrustEngine()

@pytest.fixture
def registered_user_and_device(zt_engine):
    """Fixture to register a user and device."""
    user_id = "test_user"
    device_id = "test_device"
    zt_engine.register_user(user_id, {"email": "test@example.com", "role": "admin", "mfa_enabled": True})
    zt_engine.register_device(device_id, {
        "user_id": user_id,
        "device_type": "laptop",
        "os": "Windows 10",
        "antivirus_installed": True,
        "encryption_enabled": True,
        "os_updated": True,
        "screen_lock_enabled": True,
        "expected_locations": [(10.0, 20.0)]
    })
    return zt_engine, user_id, device_id

def test_initialization(zt_engine):
    """Test that the ZeroTrustEngine initializes correctly."""
    assert zt_engine is not None
    assert zt_engine.quantum_crypto is not None
    assert zt_engine.homomorphic_enc is not None
    assert zt_engine.zk_proof is not None
    assert zt_engine.behavioral_analytics is not None
    assert zt_engine.threat_intelligence is not None
    assert zt_engine.soar_engine is not None

def test_user_and_device_registration(registered_user_and_device):
    """Test that a user and device can be registered."""
    zt_engine, user_id, device_id = registered_user_and_device
    assert user_id in zt_engine.user_registry
    assert device_id in zt_engine.device_registry
    assert zt_engine.user_registry[user_id]["email"] == "test@example.com"
    assert zt_engine.device_registry[device_id]["os"] == "Windows 10"

def create_access_request(user_id, device_id, location, totp_code=None):
    """Helper function to create an access request."""
    user_context = UserContext(
        user_id=user_id,
        device_id=device_id,
        source_ip="192.168.1.1",
        location=location,
        network="test_network",
        time_of_access=datetime.now(),
        behavior_profile={},
        risk_factors=[],
        trust_score=0.0,
        totp_code=totp_code,
    )
    return AccessRequest(
        request_id="test_req",
        user_id=user_id,
        resource="test_resource",
        action="read",
        context=user_context,
        timestamp=datetime.now(),
        session_id="test_session",
    )

def test_evaluate_access_request_trusted(registered_user_and_device):
    """Test a simple, trusted access request."""
    zt_engine, user_id, device_id = registered_user_and_device
    # Generate a valid TOTP code
    totp_code = zt_engine.get_totp_uri(user_id)
    
    request = create_access_request(user_id, device_id, (10.0, 20.0), totp_code)
    
    # Mock MFA verification to return True
    zt_engine._verify_mfa = lambda user_id, context: True
    
    result = zt_engine.evaluate_access_request(request)
    
    assert result["decision"]["action"] == "allow"
    assert result["risk_score"] < 0.3

def test_evaluate_access_request_untrusted_device(registered_user_and_device):
    """Test an access request from an untrusted device."""
    zt_engine, user_id, device_id = registered_user_and_device
    request = create_access_request(user_id, "untrusted_device", (10.0, 20.0))
    
    result = zt_engine.evaluate_access_request(request)
    
    assert result["decision"]["action"] in ["deny", "challenge"]
    assert result["risk_score"] > 0.5

def test_evaluate_access_request_suspicious_location(registered_user_and_device):
    """Test an access request from a suspicious location."""
    zt_engine, user_id, device_id = registered_user_and_device
    request = create_access_request(user_id, device_id, (99.0, 99.0)) # Far from expected location
    
    result = zt_engine.evaluate_access_request(request)
    
    assert result["decision"]["action"] in ["deny", "challenge"]
    assert result["risk_score"] > 0.5

def test_mfa_verification(registered_user_and_device):
    """Test the MFA verification logic."""
    zt_engine, user_id, device_id = registered_user_and_device
    
    # No TOTP code provided
    assert not zt_engine._verify_mfa(user_id, UserContext(user_id=user_id, device_id=device_id, source_ip="127.0.0.1", location=(0,0), network="", time_of_access=datetime.now(), behavior_profile={}, risk_factors=[], trust_score=0.0))
    
    # Invalid TOTP code
    assert not zt_engine._verify_mfa(user_id, UserContext(user_id=user_id, device_id=device_id, source_ip="127.0.0.1", location=(0,0), network="", time_of_access=datetime.now(), behavior_profile={}, risk_factors=[], trust_score=0.0, totp_code="123456"))

def test_threat_intelligence(zt_engine):
    """Test the threat intelligence system."""
    zt_engine.threat_intelligence.ioc_database["1.2.3.4"] = {
        "type": "ip",
        "threat_level": "high",
        "description": "Known malicious IP",
    }
    
    result = zt_engine.threat_intelligence.check_ioc("1.2.3.4", "ip")
    assert result["is_ioc"]
    assert result["threat_level"] == "high"
    
    result = zt_engine.threat_intelligence.check_ioc("5.6.7.8", "ip")
    assert not result["is_ioc"]

def test_behavioral_analytics(zt_engine):
    """Test the behavioral analytics engine."""
    user_id = "behavior_test_user"
    
    # Add some baseline behavior
    for i in range(10):
        zt_engine.behavioral_analytics.update_user_profile(user_id, {
            "login_time": datetime(2023, 1, 1, 9 + i % 2, 0, 0), # Logins around 9-10 AM
            "location": (30.0, 40.0),
            "session_duration": 60,
        })
    
    # This should not be an anomaly
    normal_behavior = {
        "login_time": datetime(2023, 1, 2, 9, 30, 0),
        "location": (30.1, 40.1),
        "session_duration": 65,
    }
    result = zt_engine.behavioral_analytics.detect_anomalies(user_id, normal_behavior)
    assert not result["anomaly_detected"]
    
    # This should be an anomaly
    anomalous_behavior = {
        "login_time": datetime(2023, 1, 2, 23, 0, 0), # Late night login
        "location": (80.0, 80.0), # Far away
        "session_duration": 500,
    }
    result = zt_engine.behavioral_analytics.detect_anomalies(user_id, anomalous_behavior)
    assert result["anomaly_detected"]

def test_soar_playbook_execution(zt_engine):
    """Test the execution of a SOAR playbook."""
    incident_data = {
        "source_ip": "10.20.30.40",
        "device_id": "compromised_device",
        "user_id": "compromised_user",
        "incident_id": "incident-123",
    }
    
    result = zt_engine.soar_engine.execute_playbook("high_risk_incident", incident_data)
    
    assert result["overall_success"]
    assert len(result["results"]) == 4
    assert result["results"][0]["action"] == "send_alert"
    assert result["results"][1]["action"] == "block_ip"
    assert result["results"][2]["action"] == "collect_forensics"
    assert result["results"][3]["action"] == "escalate_incident"
