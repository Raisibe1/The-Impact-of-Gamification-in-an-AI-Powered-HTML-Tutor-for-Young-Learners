\# Data Pipeline Diagram — StudyChat



\## Pipeline Overview



┌─────────────────────────────────────────────────────────┐

│ STUDYCHAT DATA PIPELINE │

└─────────────────────────────────────────────────────────┘



┌─────────────┐ ┌─────────────┐ ┌─────────────┐

│ RAW DATA │────▶│ CLEANING │────▶│ FEATURES │

│ │ │ │ │ │

│ studychat │ │ Extract │ │ prompt\_len │

│ .csv │ │ target │ │ num\_turns │

│ │ │ Group │ │ word\_count │

│ 16,851 rows │ │ categories │ │ │

└─────────────┘ └─────────────┘ └─────────────┘

│

▼

┌─────────────┐ ┌─────────────┐ ┌─────────────┐

│ MODEL │◀────│ SPLIT │◀────│ PROCESSED │

│ TRAINING │ │ │ │ DATA │

│ │ │ Train 70% │ │ │

│ Classifier │ │ Val 15% │ │ studychat │

│ │ │ Test 15% │ │ \_cleaned │

└─────────────┘ └─────────────┘ └─────────────┘

