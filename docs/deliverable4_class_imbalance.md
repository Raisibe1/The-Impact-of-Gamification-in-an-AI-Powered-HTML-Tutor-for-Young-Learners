# Class Imbalance Report — StudyChat

## Class Distribution (After Grouping)

| Meta-Category | Count | Percentage |
| :--- | :--- | :--- |
| (fill in from your script output) | | |

## Imbalance Analysis

| Metric | Value |
| :--- | :--- |
| Total classes | 5 |
| Majority class | (fill in) |
| Minority class | (fill in) |
| Imbalance ratio | (fill in):1 |

## Was There Imbalance?

- Yes/No: Yes
- Severity: Moderate

## How Was It Handled?

**Method selected:** Class weights

**Why this method:**
- Works well with text classification (transformers)
- No data loss (unlike undersampling)
- No synthetic data (unlike SMOTE)
- Supported by scikit-learn and Hugging Face transformers

## Code

```python
from sklearn.utils.class_weight import compute_class_weight

class_weights = compute_class_weight(
    'balanced',
    classes=np.unique(y_train),
    y=y_train
)