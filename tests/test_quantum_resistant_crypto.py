"""
Test suite for Quantum-Resistant Cryptography System
"""

import unittest
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from security.quantum_resistant.pq_crypto import (
    QuantumResistantCryptoSuite,
    CRYSTALSDilithium,
    CRYSTALSKyber,
    SPHINCSPlus,
    NTRUEncrypt,
    QuantumResistantCryptoError
)

class TestCRYSTALSDilithium(unittest.TestCase):
    """Test cases for CRYSTALS-Dilithium"""

    def setUp(self):
        """Set up test fixtures"""
        self.dilithium = CRYSTALSDilithium(security_level=2)
    
    def test_initialization(self):
        """Test initialization"""
        self.assertEqual(self.dilithium.security_level, 2)
        self.assertIn('n', self.dilithium.params)
        self.assertIn('q', self.dilithium.params)
    
    def test_keypair_generation(self):
        """Test key pair generation"""
        private_key, public_key = self.dilithium.generate_keypair()
        self.assertIsInstance(private_key, bytes)
        self.assertIsInstance(public_key, bytes)
        self.assertEqual(len(private_key), 64)
        self.assertEqual(len(public_key), 32)
    
    def test_signing_and_verification(self):
        """Test signing and verification"""
        private_key, public_key = self.dilithium.generate_keypair()
        message = b"Test message for Dilithium"
        
        # Sign message
        signature = self.dilithium.sign(message, private_key)
        self.assertIsInstance(signature, bytes)
        
        # Verify signature
        is_valid = self.dilithium.verify(message, signature, public_key)
        self.assertTrue(is_valid)
        
        # Verify with wrong message
        is_valid_wrong = self.dilithium.verify(b"Wrong message", signature, public_key)
        self.assertFalse(is_valid_wrong)
        
        # Verify with wrong public key
        _, wrong_public_key = self.dilithium.generate_keypair()
        is_valid_wrong_key = self.dilithium.verify(message, signature, wrong_public_key)
        self.assertFalse(is_valid_wrong_key)

class TestCRYSTALSKyber(unittest.TestCase):
    """Test cases for CRYSTALS-Kyber"""

    def setUp(self):
        """Set up test fixtures"""
        self.kyber = CRYSTALSKyber(security_level=2)
    
    def test_initialization(self):
        """Test initialization"""
        self.assertEqual(self.kyber.security_level, 2)
        self.assertIn('k', self.kyber.params)
        self.assertIn('eta1', self.kyber.params)
    
    def test_keypair_generation(self):
        """Test key pair generation"""
        private_key, public_key = self.kyber.generate_keypair()
        self.assertIsInstance(private_key, bytes)
        self.assertIsInstance(public_key, bytes)
        self.assertEqual(len(private_key), 32)
        self.assertEqual(len(public_key), 32)
    
    def test_encapsulation_and_decapsulation(self):
        """Test encapsulation and decapsulation"""
        private_key, public_key = self.kyber.generate_keypair()
        
        # Encapsulate key
        ciphertext, shared_secret = self.kyber.encapsulate(public_key)
        self.assertIsInstance(ciphertext, bytes)
        self.assertIsInstance(shared_secret, bytes)
        
        # Decapsulate key
        recovered_secret = self.kyber.decapsulate(ciphertext, private_key)
        self.assertIsInstance(recovered_secret, bytes)
        self.assertEqual(shared_secret, recovered_secret)

class TestSPHINCSPlus(unittest.TestCase):
    """Test cases for SPHINCS+"""

    def setUp(self):
        """Set up test fixtures"""
        self.sphincs = SPHINCSPlus(security_level=2)
    
    def test_initialization(self):
        """Test initialization"""
        self.assertEqual(self.sphincs.security_level, 2)
        self.assertIn('n', self.sphincs.params)
        self.assertIn('h', self.sphincs.params)
    
    def test_keypair_generation(self):
        """Test key pair generation"""
        private_key, public_key = self.sphincs.generate_keypair()
        self.assertIsInstance(private_key, bytes)
        self.assertIsInstance(public_key, bytes)
        self.assertEqual(len(private_key), 64)
        self.assertEqual(len(public_key), 32)
    
    def test_signing_and_verification(self):
        """Test signing and verification"""
        private_key, public_key = self.sphincs.generate_keypair()
        message = b"Test message for SPHINCS+"
        
        # Sign message
        signature = self.sphincs.sign(message, private_key)
        self.assertIsInstance(signature, bytes)
        
        # Verify signature
        is_valid = self.sphincs.verify(message, signature, public_key)
        self.assertTrue(is_valid)
        
        # Verify with wrong message
        is_valid_wrong = self.sphincs.verify(b"Wrong message", signature, public_key)
        self.assertFalse(is_valid_wrong)

class TestNTRUEncrypt(unittest.TestCase):
    """Test cases for NTRUEncrypt"""

    def setUp(self):
        """Set up test fixtures"""
        self.ntru = NTRUEncrypt(security_level=2)
    
    def test_initialization(self):
        """Test initialization"""
        self.assertEqual(self.ntru.security_level, 2)
        self.assertIn('N', self.ntru.params)
        self.assertIn('p', self.ntru.params)
    
    def test_keypair_generation(self):
        """Test key pair generation"""
        private_key, public_key = self.ntru.generate_keypair()
        self.assertIsInstance(private_key, bytes)
        self.assertIsInstance(public_key, bytes)
        self.assertEqual(len(private_key), 32)
        self.assertEqual(len(public_key), 32)
    
    def test_encryption_and_decryption(self):
        """Test encryption and decryption"""
        private_key, public_key = self.ntru.generate_keypair()
        message = b"Test message for NTRUEncrypt"
        
        # Encrypt message
        ciphertext = self.ntru.encrypt(message, public_key)
        self.assertIsInstance(ciphertext, bytes)
        self.assertGreater(len(ciphertext), len(message))
        
        # Decrypt message
        decrypted_message = self.ntru.decrypt(ciphertext, private_key)
        self.assertIsInstance(decrypted_message, bytes)
        self.assertEqual(message, decrypted_message)

class TestQuantumResistantCryptoSuite(unittest.TestCase):
    """Test cases for QuantumResistantCryptoSuite"""

    def setUp(self):
        """Set up test fixtures"""
        self.pq_crypto = QuantumResistantCryptoSuite(default_algorithm='dilithium', security_level=2)
    
    def test_initialization(self):
        """Test initialization"""
        self.assertEqual(self.pq_crypto.default_algorithm, 'dilithium')
        self.assertEqual(self.pq_crypto.security_level, 2)
        self.assertIn('dilithium', self.pq_crypto.algorithms)
        self.assertIn('kyber', self.pq_crypto.algorithms)
    
    def test_generate_keypair(self):
        """Test key pair generation"""
        # Test with default algorithm
        private_key, public_key = self.pq_crypto.generate_keypair()
        self.assertIsInstance(private_key, bytes)
        self.assertIsInstance(public_key, bytes)
        
        # Test with specific algorithm
        private_key, public_key = self.pq_crypto.generate_keypair('kyber')
        self.assertIsInstance(private_key, bytes)
        self.assertIsInstance(public_key, bytes)
        
        # Test with unsupported algorithm
        with self.assertRaises(QuantumResistantCryptoError):
            self.pq_crypto.generate_keypair('unsupported')
    
    def test_signing_and_verification(self):
        """Test signing and verification through the suite"""
        private_key, public_key = self.pq_crypto.generate_keypair('dilithium')
        message = b"Test message through crypto suite"
        
        # Sign message
        signature = self.pq_crypto.sign(message, private_key, 'dilithium')
        self.assertIsInstance(signature, bytes)
        
        # Verify signature
        is_valid = self.pq_crypto.verify(message, signature, public_key, 'dilithium')
        self.assertTrue(is_valid)
        
        # Test with unsupported algorithm for signing
        with self.assertRaises(QuantumResistantCryptoError):
            self.pq_crypto.sign(message, private_key, 'unsupported')
    
    def test_encapsulation_and_decapsulation(self):
        """Test encapsulation and decapsulation through the suite"""
        private_key, public_key = self.pq_crypto.generate_keypair('kyber')
        
        # Encapsulate key
        ciphertext, shared_secret = self.pq_crypto.encapsulate(public_key, 'kyber')
        self.assertIsInstance(ciphertext, bytes)
        self.assertIsInstance(shared_secret, bytes)
        
        # Decapsulate key
        recovered_secret = self.pq_crypto.decapsulate(ciphertext, private_key, 'kyber')
        self.assertIsInstance(recovered_secret, bytes)
        self.assertEqual(shared_secret, recovered_secret)
        
        # Test with unsupported algorithm for encapsulation
        with self.assertRaises(QuantumResistantCryptoError):
            self.pq_crypto.encapsulate(public_key, 'unsupported')
    
    def test_encryption_and_decryption(self):
        """Test encryption and decryption through the suite"""
        private_key, public_key = self.pq_crypto.generate_keypair('ntru')
        message = b"Test message through crypto suite"
        
        # Encrypt message
        ciphertext = self.pq_crypto.encrypt(message, public_key, 'ntru')
        self.assertIsInstance(ciphertext, bytes)
        
        # Decrypt message
        decrypted_message = self.pq_crypto.decrypt(ciphertext, private_key, 'ntru')
        self.assertIsInstance(decrypted_message, bytes)
        self.assertEqual(message, decrypted_message)
        
        # Test with unsupported algorithm for encryption
        with self.assertRaises(QuantumResistantCryptoError):
            self.pq_crypto.encrypt(message, public_key, 'unsupported')

if __name__ == '__main__':
    unittest.main()