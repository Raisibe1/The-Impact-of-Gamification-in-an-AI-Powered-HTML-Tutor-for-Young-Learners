\# Before/After Data Summary — StudyChat



\## Before Preprocessing



| Metric | Value |

| :--- | :--- |

| Rows | 16,851 |

| Columns | 13 |

| Missing values | (fill in) |

| Duplicates | (fill in) |

| Target classes | 15+ |

| Target encoding | JSON string |



\## After Preprocessing



| Metric | Value |

| :--- | :--- |

| Rows | 16,851 |

| Columns | 11 |

| Missing values | 0 |

| Duplicates | 0 |

| Target classes | 5 |

| Target encoding | String labels |



\## Changes Made



| Action | Details |

| :--- | :--- |

| Columns removed | timestamp, chatTitle, llm\_label, messages, interactionCount, chatStartTime, chatTotalInteractionCount |

| Features created | prompt\_length, prompt\_word\_count, response\_length, num\_turns, label |

| Target variable | Extracted from llm\_label JSON, grouped into 5 meta-categories |



\## Final Columns



| Column | Type | Purpose |

| :--- | :--- | :--- |

| prompt | Text | Input feature |

| response | Text | Reference output |

| topic | Categorical | Context |

| label | Categorical | TARGET variable |

| prompt\_length | Numerical | Feature |

| prompt\_word\_count | Numerical | Feature |

| response\_length | Numerical | Feature |

| num\_turns | Numerical | Feature |

| chat\_id | String | Identifier |

| user\_id | String | Identifier |

| semester | Categorical | Context |

