import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
import xgboost as xgb
import joblib
import json
from datetime import datetime

def generate_comprehensive_training_data():
    """Generate large, diverse training dataset"""
    print(" Generating comprehensive training dataset...")
    from generate_training_data import generate_training_data
    base_data = generate_training_data()
    additional_risky = []
    additional_safe = []
    breach_patterns = [
        #Capital one 
        {
            'open_cidr_0_0_0_0': 1, 'iam_wildcard_action': 1, 'iam_wildcard_resource': 1,
            's3_public_acl': 1, 's3_encryption_disabled': 1, 'cloudtrail_not_enabled': 1,
            'vpc_flow_logs_disabled': 1, 'guardduty_not_enabled': 1
        },
        #Uber 
        {
            'secrets_in_environment_vars': 1, 'open_ssh_port_22': 1, 
            'mfa_not_enabled': 1, 'access_logging_disabled': 1,
            'alarm_missing_for_changes': 1
        },
        #Tesla
        {
            's3_public_acl': 1, 's3_encryption_disabled': 1, 's3_versioning_disabled': 1,
            's3_lifecycle_policy_missing': 1, 's3_mfa_delete_disabled': 1
        },
        #MongoDB ransomware 
        {
            'rds_publicly_accessible': 1, 'open_database_port_3306': 1,
            'rds_storage_unencrypted': 1, 'backup_vault_unencrypted': 1,
            'default_sg_in_use': 1
        }
    ]

    for pattern in breach_patterns:
        for _ in range(20): 
            variation = pattern.copy()
            for key in variation:
                if np.random.random() < 0.2:  
                    variation[key] = 0
            for i in range(1, 51):
                feature_name = f'feature_{i}'
                if feature_name not in variation:
                    variation[feature_name] = 0
            variation['label'] = 'risky'
            additional_risky.append(variation)
    safe_patterns = [
        {
            's3_public_acl': 0, 's3_encryption_disabled': 0, 's3_versioning_disabled': 0,
            's3_block_public_access_disabled': 0, 's3_lifecycle_policy_missing': 0,
            'kms_key_rotation_disabled': 0, 'cloudtrail_not_enabled': 0
        },
        {
            'rds_publicly_accessible': 0, 'rds_storage_unencrypted': 0,
            'vpc_flow_logs_disabled': 0, 'guardduty_not_enabled': 0,
            'security_hub_not_enabled': 0
        },
        {
            'iam_wildcard_action': 0, 'iam_wildcard_resource': 0,
            'iam_inline_user_policy': 0, 'mfa_not_enabled': 0,
            'password_policy_weak': 0, 'cross_account_access_unrestricted': 0
        }
    ]
    for pattern in safe_patterns:
        for _ in range(30):  
            variation = pattern.copy()
            for i in range(1, 51):
                feature_name = f'feature_{i}'
                if feature_name not in variation:
                    variation[feature_name] = 0
            variation['label'] = 'safe'
            additional_safe.append(variation)
    all_data = base_data + additional_risky + additional_safe
    print(f" Generated {len(all_data)} training examples")
    print(f"   - Risky: {sum(1 for d in all_data if d['label'] == 'risky')}")
    print(f"   - Safe: {sum(1 for d in all_data if d['label'] == 'safe')}")
    return pd.DataFrame(all_data)

