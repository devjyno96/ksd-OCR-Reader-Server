# Create domain resource file

```shell
nano ocr-domain.json
```

```json
[
  {
    "domain_description": "1. 발달력 및 신체성장",
    "domain_name": "Development & Physical growth",
    "secret_key": "END_POINT_SECRET_KEY",
    "APIGW_Invoke_url": "APIGW_Invoke_url",
    "category": "DP",
    "domain_keyword_list": [
      "keyword"
    ]
  },
  {
    "domain_description": "2. 혈액 검사",
    "domain_name": "Medical checkup",
    "secret_key": "END_POINT_SECRET_KEY",
    "APIGW_Invoke_url": "APIGW_Invoke_url",
    "category": "MC",
    "domain_keyword_list": [
      "keyword"
    ]
  },
  {
    "domain_description": "3. 발달 및 지능검사",
    "domain_name": "Development & Intelligence test",
    "secret_key": "END_POINT_SECRET_KEY",
    "APIGW_Invoke_url": "APIGW_Invoke_url",
    "category": "DI",
    "domain_keyword_list": [
      "keyword"
    ]
  },
  {
    "domain_description": "4. 사회성 및 자폐검사",
    "domain_name": "Sociality & Autism tests",
    "secret_key": "END_POINT_SECRET_KEY",
    "APIGW_Invoke_url": "APIGW_Invoke_url",
    "category": "SA",
    "domain_keyword_list": [
      "keyword"
    ]
  },
  {
    "domain_description": "5. 언어 및 신경인지검사",
    "domain_name": "Language test",
    "secret_key": "END_POINT_SECRET_KEY",
    "APIGW_Invoke_url": "APIGW_Invoke_url",
    "category": "LR",
    "domain_keyword_list": [
      "keyword"
    ]
  },
  {
    "domain_description": "6. 기질 및 성격검사",
    "domain_name": "Temperament & Personality & Emotional state",
    "secret_key": "END_POINT_SECRET_KEY",
    "APIGW_Invoke_url": "APIGW_Invoke_url",
    "category": "TC",
    "domain_keyword_list": [
      "keyword"
    ]
  },
  {
    "domain_description": "7. 주의력 및 기질 및 학습검사",
    "domain_name": "Attention & Neurocognition & Learning tests",
    "secret_key": "END_POINT_SECRET_KEY",
    "APIGW_Invoke_url": "APIGW_Invoke_url",
    "category": "AL",
    "domain_keyword_list": [
      "keyword"
    ]
  }
]
```