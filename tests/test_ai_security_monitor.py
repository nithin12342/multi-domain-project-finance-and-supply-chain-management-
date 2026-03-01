"""
Test suite for AI-Driven Security Monitoring System
"""

import unittest
import sys
import os
import tempfile
from datetime import datetime, timedelta

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from security.ai_driven.ai_security_monitor import (
    AIThreatDetector,
    BehavioralAnalyzer,
    ThreatIntelligenceProcessor,
    AISecurityMonitor,
    SecurityEvent,
    ThreatLevel,
    ThreatIndicator,
    ThreatType
)

class TestAIThreatDetector(unittest.TestCase):
    """Test cases for AI Threat Detector"""

    def setUp(self):
        """Set up test fixtures"""
        self.threat_detector = AIThreatDetector()
    
    def test_initialization(self):
        """Test initialization of threat detector"""
        self.assertIsNotNone(self.threat_detector.isolation_forest)
        self.assertIsNotNone(self.threat_detector.random_forest)
        self.assertIsNotNone(self.threat_detector.scaler)
    
    def test_score_to_threat_level(self):
        """Test conversion of scores to threat levels"""
        self.assertEqual(
            self.threat_detector._score_to_threat_level(0.9),
            ThreatLevel.CRITICAL
        )
        self.assertEqual(
            self.threat_detector._score_to_threat_level(0.7),
            ThreatLevel.HIGH
        )
        self.assertEqual(
            self.threat_detector._score_to_threat_level(0.5),
            ThreatLevel.MEDIUM
        )
        self.assertEqual(
            self.threat_detector._score_to_threat_level(0.2),
            ThreatLevel.LOW
        )

class TestBehavioralAnalyzer(unittest.TestCase):
    """Test cases for Behavioral Analyzer"""

    def setUp(self):
        """Set up test fixtures"""
        self.behavioral_analyzer = BehavioralAnalyzer()
    
    def test_user_profile_creation(self):
        """Test user profile creation"""
        user_id = "test_user"
        behavior_data = {
            "login_time": datetime.now(),
            "accessed_resources": ["dashboard", "reports"],
            "data_volume": 1000,
            "location": (40.7128, -74.0060),
            "device_id": "device_123",
            "session_duration": 1800
        }
        
        self.behavioral_analyzer.update_user_profile(user_id, behavior_data)
        
        self.assertIn(user_id, self.behavioral_analyzer.user_profiles)
        profile = self.behavioral_analyzer.user_profiles[user_id]
        self.assertIn("login_times", profile)
        self.assertIn("access_patterns", profile)
        self.assertIn("data_access_volume", profile)
    
    def test_behavioral_anomaly_detection(self):
        """Test behavioral anomaly detection"""
        user_id = "test_user"
        
        # Create baseline behavior
        for i in range(5):
            self.behavioral_analyzer.update_user_profile(user_id, {
                "login_time": datetime.now() - timedelta(hours=9 + i),  # Normal login time
                "location": (40.7128, -74.0060),  # New York
                "data_volume": 1000 + (i * 100),
                "device_id": "device_123"
            })
        
        # Test normal behavior
        normal_behavior = {
            "login_time": datetime.now().replace(hour=10),
            "location": (40.7128, -74.0060),
            "data_volume": 1200,
            "device_id": "device_123"
        }
        
        result = self.behavioral_analyzer.detect_behavioral_anomalies(user_id, normal_behavior)
        self.assertIsInstance(result, dict)
        
        # Test anomalous behavior
        anomalous_behavior = {
            "login_time": datetime.now().replace(hour=3),  # Unusual hour
            "location": (34.0522, -118.2437),  # Different location (LA)
            "data_volume": 5000,  # Much higher data volume
            "device_id": "unknown_device"
        }
        
        result = self.behavioral_analyzer.detect_behavioral_anomalies(user_id, anomalous_behavior)
        self.assertTrue(result['anomaly_detected'])

class TestThreatIntelligenceProcessor(unittest.TestCase):
    """Test cases for Threat Intelligence Processor"""

    def setUp(self):
        """Set up test fixtures"""
        self.threat_intel_processor = ThreatIntelligenceProcessor()
    
    def test_add_threat_indicator(self):
        """Test adding threat indicator"""
        indicator = ThreatIndicator(
            indicator_id="test_ioc",
            timestamp=datetime.now(),
            indicator_type="ip",
            value="192.168.1.100",
            confidence=0.8,
            threat_type=ThreatType.MALWARE,
            source="test_feed",
            metadata={"description": "Test indicator"}
        )
        
        self.threat_intel_processor.add_threat_indicator(indicator)
        
        self.assertIn("test_ioc", self.threat_intel_processor.threat_indicators)
        self.assertIn("192.168.1.100", self.threat_intel_processor.ioc_database)
    
    def test_correlate_indicators(self):
        """Test correlating indicators with security events"""
        # Add test indicator
        indicator = ThreatIndicator(
            indicator_id="test_ioc",
            timestamp=datetime.now(),
            indicator_type="ip",
            value="192.168.1.100",
            confidence=0.9,
            threat_type=ThreatType.DATA_EXFILTRATION,
            source="test_feed",
            metadata={"description": "Malicious IP"}
        )
        self.threat_intel_processor.add_threat_indicator(indicator)
        
        # Create security event with matching IP
        event = SecurityEvent(
            event_id="test_event",
            timestamp=datetime.now(),
            event_type="suspicious_request",
            severity=ThreatLevel.MEDIUM,
            source_ip="192.168.1.100",  # Matching IP
            user_id="test_user",
            resource="test_resource",
            action="access",
            result="attempted",
            metadata={},
            risk_score=0.5
        )
        
        matches = self.threat_intel_processor.correlate_indicators(event)
        
        self.assertIsInstance(matches, list)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]['type'], 'ip_match')
        self.assertEqual(matches[0]['threat_type'], 'data_exfiltration')

class TestAISecurityMonitor(unittest.TestCase):
    """Test cases for AI Security Monitor"""

    def setUp(self):
        """Set up test fixtures"""
        self.ai_monitor = AISecurityMonitor()
    
    def test_initialization(self):
        """Test initialization of AI security monitor"""
        self.assertIsNotNone(self.ai_monitor.threat_detector)
        self.assertIsNotNone(self.ai_monitor.behavioral_analyzer)
        self.assertIsNotNone(self.ai_monitor.threat_intel_processor)
    
    def test_process_security_event(self):
        """Test processing of security event"""
        event = SecurityEvent(
            event_id="test_event",
            timestamp=datetime.now(),
            event_type="failed_login",
            severity=ThreatLevel.MEDIUM,
            source_ip="192.168.1.100",
            user_id="test_user",
            resource="admin_panel",
            action="login",
            result="failed",
            metadata={
                "attempt_count": 5,
                "location": (40.7128, -74.0060)
            },
            risk_score=0.6
        )
        
        result = self.ai_monitor.process_security_event(event)
        
        self.assertIsInstance(result, dict)
        self.assertIn('event_id', result)
        self.assertIn('risk_score', result)
        self.assertIn('threat_level', result)
        self.assertIn('anomalies_detected', result)
        self.assertIn('alert_generated', result)
    
    def test_risk_to_threat_level(self):
        """Test conversion of risk scores to threat levels"""
        self.assertEqual(
            self.ai_monitor._risk_to_threat_level(0.9),
            ThreatLevel.CRITICAL
        )
        self.assertEqual(
            self.ai_monitor._risk_to_threat_level(0.7),
            ThreatLevel.HIGH
        )
        self.assertEqual(
            self.ai_monitor._risk_to_threat_level(0.5),
            ThreatLevel.MEDIUM
        )
        self.assertEqual(
            self.ai_monitor._risk_to_threat_level(0.2),
            ThreatLevel.LOW
        )

if __name__ == '__main__':
    unittest.main()