# TerraSecure Production Model v1.0.0

- **Version:** 1.0.0
- **Build Date:** 2026-03-09T20:03:11.290802
- **Model Type:** XGBoost
- **Training Samples:** 265
- **Features:** 50

- **Accuracy:** 92.45%
- **Precision:** 88.89%
- **Recall:** 96.00%
- **F1-Score:** 0.9231

- **False Positive Rate:** 10.71% (Target: <10%)
- **False Negative Rate:** 4.00% (Target: <5%)

 PASSED
1. open_database_port_3306 (0.1217)
2. api_gateway_no_waf (0.0919)
3. rds_storage_unencrypted (0.0880)
4. vpc_flow_logs_disabled (0.0839)
5. s3_encryption_disabled (0.0786)
6. lambda_env_vars_unencrypted (0.0615)
7. rds_publicly_accessible (0.0505)
8. iam_wildcard_resource (0.0447)
9. secrets_in_environment_vars (0.0430)
10. mfa_not_enabled (0.0430)
