"""
Test suite for Zero Trust Security Architecture
"""

import unittest
import tempfile
import os
import json
from datetime import datetime
from security.advanced.zero_trust_architecture import (
    ZeroTrustEngine, 
    AccessRequest, 
    UserContext,
    SecurityEvent,
    ThreatLevel,
    AccessDecision
)

class TestZeroTrustEngine(unittest.TestCase):
    """Test cases for Zero Trust Engine"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary config file
        self.temp_config = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        config_content = """
general:
  log_level: DEBUG

iam:
  mfa:
    required_for_admins: true
    totp_issuer: TestIssuer

device_trust:
  compliance:
    antivirus_required: true
    encryption_required: true

threat_intelligence:
  feeds: []
"""
        self.temp_config.write(config_content)
        self.temp_config.close()
        
        # Initialize the Zero Trust Engine
        self.zt_engine = ZeroTrustEngine(self.temp_config.name)
        
        # Register a test user
        self.zt_engine.register_user('test_user', {
            'email': 'test@example.com',
            'role': 'admin',
            'mfa_enabled': True
        })
        
        # Register a test device
        self.zt_engine.register_device('test_device', {
            'user_id': 'test_user',
            'device_type': 'laptop',
            'os': 'Linux',
            'antivirus_installed': True,
            'encryption_enabled': True,
            'os_updated': True,
            'screen_lock_enabled': True
        })

    def tearDown(self):
        """Tear down test fixtures"""
        os.unlink(self.temp_config.name)

    def test_user_registration(self):
        """Test user registration"""
        self.assertIn('test_user', self.zt_engine.user_registry)
        user = self.zt_engine.user_registry['test_user']
        self.assertEqual(user['email'], 'test@example.com')
        self.assertEqual(user['role'], 'admin')

    def test_device_registration(self):
        """Test device registration"""
        self.assertIn('test_device', self.zt_engine.device_registry)
        device = self.zt_engine.device_registry['test_device']
        self.assertEqual(device['user_id'], 'test_user')
        self.assertEqual(device['device_type'], 'laptop')

    def test_totp_uri_generation(self):
        """Test TOTP URI generation"""
        uri = self.zt_engine.get_totp_uri('test_user')
        self.assertIsNotNone(uri)
        self.assertIn('otpauth://totp/', uri)
        self.assertIn('TestIssuer', uri)

    def test_access_request_evaluation(self):
        """Test access request evaluation"""
        # Generate a TOTP code for testing
        user = self.zt_engine.user_registry['test_user']
        totp_code = pyotp.TOTP(user['totp_secret']).now()
        
        # Create access request
        user_context = UserContext(
            user_id='test_user',
            device_id='test_device',
            source_ip='192.168.1.100',
            location=(40.7128, -74.0060),
            network='corporate_wifi',
            time_of_access=datetime.now(),
            behavior_profile={},
            risk_factors=[],
            trust_score=0.8,
            totp_code=totp_code
        )
        
        access_request = AccessRequest(
            request_id='test_request',
            user_id='test_user',
            resource='sensitive_data',
            action='read',
            context=user_context,
            timestamp=datetime.now(),
            session_id='test_session'
        )
        
        # Evaluate access request
        result = self.zt_engine.evaluate_access_request(access_request)
        
        # Assertions
        self.assertIn('decision', result)
        self.assertIn('risk_score', result)
        self.assertIsInstance(result['risk_score'], float)
        self.assertTrue(0.0 <= result['risk_score'] <= 1.0)

    def test_quantum_resistant_crypto(self):
        """Test quantum-resistant cryptography"""
        qr_crypto = self.zt_engine.quantum_crypto
        
        # Test key generation
        private_key, public_key = qr_crypto.generate_quantum_resistant_keypair('dilithium')
        self.assertIsInstance(private_key, bytes)
        self.assertIsInstance(public_key, bytes)
        
        # Test signing
        message = b"Test message"
        signature = qr_crypto._dilithium_sign(message, private_key)
        self.assertIsInstance(signature, bytes)

    def test_homomorphic_encryption(self):
        """Test homomorphic encryption"""
        hom_enc = self.zt_engine.homomorphic_enc
        
        # Test encryption/decryption
        plaintext = 42
        ciphertext = hom_enc.encrypt(plaintext)
        decrypted = hom_enc.decrypt(ciphertext)
        self.assertEqual(plaintext, decrypted)
        
        # Test homomorphic addition
        plaintext1, plaintext2 = 15, 25
        ciphertext1 = hom_enc.encrypt(plaintext1)
        ciphertext2 = hom_enc.encrypt(plaintext2)
        result_cipher = hom_enc.add_encrypted(ciphertext1, ciphertext2)
        result_plain = hom_enc.decrypt(result_cipher)
        self.assertEqual(plaintext1 + plaintext2, result_plain)

    def test_zero_knowledge_proof(self):
        """Test zero-knowledge proof system"""
        zk_proof = self.zt_engine.zk_proof
        
        # Test proof generation and verification
        secret = "test_secret"
        statement = "I know the secret"
        proof = zk_proof.generate_proof(secret, statement)
        self.assertIsInstance(proof, dict)
        
        # Test proof verification
        is_valid = zk_proof.verify_proof(proof)
        self.assertTrue(is_valid)

    def test_behavioral_analytics(self):
        """Test behavioral analytics"""
        behavior_analytics = self.zt_engine.behavioral_analytics
        
        # Test user profile update
        behavior_analytics.update_user_profile('test_user', {
            'login_time': datetime.now(),
            'location': (40.7128, -74.0060),
            'session_duration': 300
        })
        
        self.assertIn('test_user', behavior_analytics.user_profiles)
        
        # Test anomaly detection
        current_behavior = {
            'login_time': datetime.now(),
            'location': (40.7128, -74.0060),
            'session_duration': 300
        }
        
        result = behavior_analytics.detect_anomalies('test_user', current_behavior)
        self.assertIsInstance(result, dict)
        self.assertIn('anomaly_detected', result)

class TestSecurityComponents(unittest.TestCase):
    """Test cases for security components"""

    def test_security_event_creation(self):
        """Test security event creation"""
        event = SecurityEvent(
            event_id='test_event',
            timestamp=datetime.now(),
            event_type='access_request',
            severity=ThreatLevel.MEDIUM,
            source_ip='192.168.1.100',
            user_id='test_user',
            resource='test_resource',
            action='read',
            result='allowed',
            metadata={},
            risk_score=0.5
        )
        
        self.assertEqual(event.event_id, 'test_event')
        self.assertEqual(event.event_type, 'access_request')
        self.assertEqual(event.severity, ThreatLevel.MEDIUM)

    def test_threat_level_enum(self):
        """Test threat level enumeration"""
        self.assertEqual(ThreatLevel.LOW.value, 'low')
        self.assertEqual(ThreatLevel.MEDIUM.value, 'medium')
        self.assertEqual(ThreatLevel.HIGH.value, 'high')
        self.assertEqual(ThreatLevel.CRITICAL.value, 'critical')

    def test_access_decision_enum(self):
        """Test access decision enumeration"""
        self.assertEqual(AccessDecision.ALLOW.value, 'allow')
        self.assertEqual(AccessDecision.DENY.value, 'deny')
        self.assertEqual(AccessDecision.CHALLENGE.value, 'challenge')
        self.assertEqual(AccessDecision.REVIEW.value, 'review')

if __name__ == '__main__':
    unittest.main()