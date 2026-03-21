# TerraSecure Production Model v1.0.0

- **Version:** 1.0.0
- **Build Date:** 2026-03-21T13:11:48.912980
- **Model Type:** XGBoost
- **Training Samples:** 265
- **Features:** 50

- **Accuracy:** 84.91%
- **Precision:** 94.74%
- **Recall:** 72.00%
- **F1-Score:** 0.8182

- **False Positive Rate:** 3.57% (Target: <10%)
- **False Negative Rate:** 28.00% (Target: <5%)

 FAILED
1. s3_block_public_access_disabled (0.0677)
2. mfa_not_enabled (0.0659)
3. open_database_port_5432 (0.0640)
4. s3_encryption_disabled (0.0637)
5. secrets_in_environment_vars (0.0612)
6. s3_public_acl (0.0569)
7. s3_versioning_disabled (0.0566)
8. ecr_image_scan_disabled (0.0555)
9. s3_lifecycle_policy_missing (0.0468)
10. open_ssh_port_22 (0.0422)
