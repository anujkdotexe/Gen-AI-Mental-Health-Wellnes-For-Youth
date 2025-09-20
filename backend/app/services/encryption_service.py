"""
Data Encryption Service for MindSpark AI
Provides comprehensive data encryption and decryption for sensitive user data
"""
import base64
import os
import json
from typing import Dict, Any, Optional, Union, List
from datetime import datetime, timedelta
from cryptography.fernet import Fernet, MultiFernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import secrets


class EncryptionService:
    """Service for data encryption and decryption"""
    
    def __init__(self):
        # Generate master encryption key (in production, store securely)
        self.master_key = Fernet.generate_key()
        self.fernet = Fernet(self.master_key)
        
        # Generate RSA key pair for asymmetric encryption
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()
        
        # Encryption metadata storage
        self.encryption_metadata = {}
        
    def encrypt_sensitive_data(self, data: Union[str, Dict[str, Any]], encryption_type: str = "symmetric") -> Dict[str, str]:
        """Encrypt sensitive data with optional encryption type"""
        try:
            # Convert data to string if needed
            if isinstance(data, dict):
                data_string = json.dumps(data, separators=(',', ':'))
            else:
                data_string = str(data)
            
            data_bytes = data_string.encode('utf-8')
            
            if encryption_type == "symmetric":
                encrypted_data = self.fernet.encrypt(data_bytes)
                encryption_key = self.master_key.decode('utf-8')
            elif encryption_type == "asymmetric":
                encrypted_data = self.public_key.encrypt(
                    data_bytes,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                encryption_key = "rsa_public_key"
            else:
                raise ValueError(f"Unsupported encryption type: {encryption_type}")
            
            # Create metadata
            encryption_id = secrets.token_hex(16)
            metadata = {
                'encryption_id': encryption_id,
                'encrypted_data': base64.b64encode(encrypted_data).decode('utf-8'),
                'encryption_type': encryption_type,
                'encryption_algorithm': 'Fernet' if encryption_type == 'symmetric' else 'RSA-OAEP',
                'created_at': datetime.now().isoformat(),
                'data_size': len(data_bytes)
            }
            
            # Store metadata
            self.encryption_metadata[encryption_id] = {
                'metadata': metadata,
                'encryption_key': encryption_key
            }
            
            return metadata
            
        except Exception as e:
            raise Exception(f"Encryption failed: {str(e)}")
    
    def decrypt_sensitive_data(self, encryption_id: str) -> Union[str, Dict[str, Any]]:
        """Decrypt data using encryption ID"""
        try:
            if encryption_id not in self.encryption_metadata:
                raise ValueError(f"Encryption ID not found: {encryption_id}")
            
            stored_data = self.encryption_metadata[encryption_id]
            metadata = stored_data['metadata']
            
            # Decode encrypted data
            encrypted_data = base64.b64decode(metadata['encrypted_data'])
            
            if metadata['encryption_type'] == 'symmetric':
                decrypted_bytes = self.fernet.decrypt(encrypted_data)
            elif metadata['encryption_type'] == 'asymmetric':
                decrypted_bytes = self.private_key.decrypt(
                    encrypted_data,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
            else:
                raise ValueError(f"Unsupported encryption type: {metadata['encryption_type']}")
            
            # Convert back to original format
            decrypted_string = decrypted_bytes.decode('utf-8')
            
            # Try to parse as JSON
            try:
                return json.loads(decrypted_string)
            except json.JSONDecodeError:
                return decrypted_string
                
        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")
    
    def encrypt_mood_data(self, user_id: str, mood_data: Dict[str, Any]) -> str:
        """Encrypt mood data specifically"""
        # Add user context to mood data
        enhanced_data = {
            'user_id': user_id,
            'mood_data': mood_data,
            'data_type': 'mood_entry',
            'encrypted_at': datetime.now().isoformat()
        }
        
        result = self.encrypt_sensitive_data(enhanced_data, "symmetric")
        return result['encryption_id']
    
    def decrypt_mood_data(self, encryption_id: str) -> Dict[str, Any]:
        """Decrypt mood data"""
        decrypted_data = self.decrypt_sensitive_data(encryption_id)
        if isinstance(decrypted_data, dict) and 'mood_data' in decrypted_data:
            return decrypted_data['mood_data']
        raise ValueError("Invalid mood data format")
    
    def encrypt_journal_entry(self, user_id: str, journal_data: Dict[str, Any]) -> str:
        """Encrypt journal entry"""
        enhanced_data = {
            'user_id': user_id,
            'journal_data': journal_data,
            'data_type': 'journal_entry',
            'encrypted_at': datetime.now().isoformat()
        }
        
        result = self.encrypt_sensitive_data(enhanced_data, "symmetric")
        return result['encryption_id']
    
    def decrypt_journal_entry(self, encryption_id: str) -> Dict[str, Any]:
        """Decrypt journal entry"""
        decrypted_data = self.decrypt_sensitive_data(encryption_id)
        if isinstance(decrypted_data, dict) and 'journal_data' in decrypted_data:
            return decrypted_data['journal_data']
        raise ValueError("Invalid journal data format")
    
    def encrypt_conversation(self, user_id: str, conversation_data: Dict[str, Any]) -> str:
        """Encrypt AI conversation data"""
        enhanced_data = {
            'user_id': user_id,
            'conversation_data': conversation_data,
            'data_type': 'conversation',
            'encrypted_at': datetime.now().isoformat()
        }
        
        result = self.encrypt_sensitive_data(enhanced_data, "asymmetric")  # Use stronger encryption for conversations
        return result['encryption_id']
    
    def decrypt_conversation(self, encryption_id: str) -> Dict[str, Any]:
        """Decrypt AI conversation data"""
        decrypted_data = self.decrypt_sensitive_data(encryption_id)
        if isinstance(decrypted_data, dict) and 'conversation_data' in decrypted_data:
            return decrypted_data['conversation_data']
        raise ValueError("Invalid conversation data format")
    
    def encrypt_user_credentials(self, credentials: Dict[str, Any]) -> str:
        """Encrypt user credentials with strongest security"""
        result = self.encrypt_sensitive_data(credentials, "asymmetric")
        return result['encryption_id']
    
    def decrypt_user_credentials(self, encryption_id: str) -> Dict[str, Any]:
        """Decrypt user credentials"""
        decrypted_data = self.decrypt_sensitive_data(encryption_id)
        if isinstance(decrypted_data, dict):
            return decrypted_data
        raise ValueError("Invalid credentials data format")
    
    def generate_field_encryption_key(self, field_name: str, user_id: str) -> str:
        """Generate specific encryption key for database field"""
        # Create deterministic key based on field and user
        key_material = f"{field_name}_{user_id}_{self.master_key.decode('utf-8')}".encode('utf-8')
        
        # Use PBKDF2 for key derivation
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'mindspark_salt',  # In production, use random salt per user
            iterations=100000
        )
        
        derived_key = base64.urlsafe_b64encode(kdf.derive(key_material))
        return derived_key.decode('utf-8')
    
    def encrypt_database_field(self, value: str, field_name: str, user_id: str) -> str:
        """Encrypt individual database field"""
        field_key = self.generate_field_encryption_key(field_name, user_id)
        field_fernet = Fernet(field_key.encode('utf-8'))
        
        encrypted_value = field_fernet.encrypt(value.encode('utf-8'))
        return base64.b64encode(encrypted_value).decode('utf-8')
    
    def decrypt_database_field(self, encrypted_value: str, field_name: str, user_id: str) -> str:
        """Decrypt individual database field"""
        field_key = self.generate_field_encryption_key(field_name, user_id)
        field_fernet = Fernet(field_key.encode('utf-8'))
        
        encrypted_bytes = base64.b64decode(encrypted_value)
        decrypted_bytes = field_fernet.decrypt(encrypted_bytes)
        return decrypted_bytes.decode('utf-8')
    
    def bulk_encrypt_data(self, data_list: List[Dict[str, Any]], encryption_type: str = "symmetric") -> List[str]:
        """Encrypt multiple data items"""
        encryption_ids = []
        for data in data_list:
            result = self.encrypt_sensitive_data(data, encryption_type)
            encryption_ids.append(result['encryption_id'])
        return encryption_ids
    
    def bulk_decrypt_data(self, encryption_ids: List[str]) -> List[Union[str, Dict[str, Any]]]:
        """Decrypt multiple data items"""
        decrypted_data = []
        for encryption_id in encryption_ids:
            try:
                data = self.decrypt_sensitive_data(encryption_id)
                decrypted_data.append(data)
            except Exception as e:
                decrypted_data.append({'error': str(e)})
        return decrypted_data
    
    def get_encryption_stats(self) -> Dict[str, Any]:
        """Get encryption service statistics"""
        total_encrypted = len(self.encryption_metadata)
        
        type_counts = {}
        algorithm_counts = {}
        
        for data in self.encryption_metadata.values():
            metadata = data['metadata']
            enc_type = metadata['encryption_type']
            algorithm = metadata['encryption_algorithm']
            
            type_counts[enc_type] = type_counts.get(enc_type, 0) + 1
            algorithm_counts[algorithm] = algorithm_counts.get(algorithm, 0) + 1
        
        return {
            'total_encrypted_items': total_encrypted,
            'encryption_types': type_counts,
            'algorithms': algorithm_counts,
            'master_key_created': datetime.now().isoformat(),  # Simulated
            'encryption_service_status': 'active'
        }
    
    def rotate_encryption_keys(self) -> Dict[str, str]:
        """Rotate encryption keys (simplified version)"""
        # Generate new master key
        new_master_key = Fernet.generate_key()
        old_master_key = self.master_key
        
        # In production, this would re-encrypt all data with new key
        # For now, just update the key
        self.master_key = new_master_key
        self.fernet = Fernet(self.master_key)
        
        return {
            'status': 'success',
            'old_key_id': base64.b64encode(old_master_key[:8]).decode('utf-8'),
            'new_key_id': base64.b64encode(new_master_key[:8]).decode('utf-8'),
            'rotated_at': datetime.now().isoformat()
        }


# Global encryption service instance
encryption_service = EncryptionService()