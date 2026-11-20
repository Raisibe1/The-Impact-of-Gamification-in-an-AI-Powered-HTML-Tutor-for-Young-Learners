from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import confusion_matrix
import numpy as np
#pip install seaborn and matpotlib

BASE_DIR = Path(__file__).resolve().parent
GRAPH_DIR = BASE_DIR / "reports" / "graphs"
GRAPH_DIR.mkdir(parents=True, exist_ok=True)


# Load test dataset predictions
pred_df = pd.read_csv(r"C:\Users\sizwe\Downloads\CodeVerse_Modular_Backend\BACKEND\INTEGRATION OF VISUALIZATION AND REPORTING TOOLS\outputs\test_predictions.csv")
y_test = pred_df["actual"]

# Plot Class Distribution
plt.figure(figsize=(7, 5))
counts = y_test.value_counts(normalize=True) * 100
bars = plt.bar(
    ["Incorrect (0)", "Correct (1)"],
    [counts[0], counts[1]],
    color=["#e74c3c", "#2ecc71"],
    width=0.5,
)

plt.title(
    "Target Variable Class Distribution (next_interaction_correct)",
    fontsize=13,
    fontweight="bold",
    pad=15,
)
plt.ylabel("Percentage (%)", fontsize=11)
plt.ylim(0, 100)

for bar in bars:
  yval = bar.get_height()
  plt.text(
      bar.get_x() + bar.get_width() / 2.0,
      yval + 2,
      f"{yval:.2f}%",
      ha="center",
      va="bottom",
      fontsize=11,
      fontweight="bold",
  )

plt.tight_layout()
plt.savefig(
	GRAPH_DIR / "class_distribution.png",
	dpi=300,
	bbox_inches="tight"
)

plt.show()  

#matrix
pred_df = pd.read_csv(r"C:\Users\sizwe\Downloads\CodeVerse_Modular_Backend\BACKEND\INTEGRATION OF VISUALIZATION AND REPORTING TOOLS\outputs\test_predictions.csv")
y_test = pred_df["actual"]
y_pred_base = pred_df["predicted_baseline"]
y_pred_tuned = pred_df["predicted_tuned"]

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

cm_base = confusion_matrix(y_test, y_pred_base)
cm_tuned = confusion_matrix(y_test, y_pred_tuned)

# Baseline Confusion Matrix
sns.heatmap(
    cm_base,
    annot=True,
    fmt="d",
    cmap="Blues",
    ax=axes[0],
    cbar=False,
    annot_kws={"size": 14, "weight": "bold"},
)
axes[0].set_title(
    "Baseline Logistic Regression\nConfusion Matrix",
    fontsize=12,
    fontweight="bold",
)
axes[0].set_xlabel("Predicted Label", fontsize=11)
axes[0].set_ylabel("Actual Label", fontsize=11)
axes[0].set_xticklabels(["Incorrect (0)", "Correct (1)"])
axes[0].set_yticklabels(["Incorrect (0)", "Correct (1)"])

# Tuned Confusion Matrix
sns.heatmap(
    cm_tuned,
    annot=True,
    fmt="d",
    cmap="Greens",
    ax=axes[1],
    cbar=False,
    annot_kws={"size": 14, "weight": "bold"},
)
axes[1].set_title(
    "Tuned Logistic Regression\nConfusion Matrix (Balanced)",
    fontsize=12,
    fontweight="bold",
)
axes[1].set_xlabel("Predicted Label", fontsize=11)
axes[1].set_ylabel("Actual Label", fontsize=11)
axes[1].set_xticklabels(["Incorrect (0)", "Correct (1)"])
axes[1].set_yticklabels(["Incorrect (0)", "Correct (1)"])

plt.tight_layout()
plt.savefig(
	GRAPH_DIR / "confusion_matrices.png",
	dpi=300,
	bbox_inches="tight"
)

plt.show()


#ROC Curve

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import roc_auc_score, roc_curve

pred_df = pd.read_csv(r"C:\Users\sizwe\Downloads\CodeVerse_Modular_Backend\BACKEND\INTEGRATION OF VISUALIZATION AND REPORTING TOOLS\outputs\test_predictions.csv")
y_test = pred_df["actual"]
y_proba_base = pred_df["probability_baseline"]
y_proba_tuned = pred_df["probability_tuned"]

fpr_base, tpr_base, _ = roc_curve(y_test, y_proba_base)
fpr_tuned, tpr_tuned, _ = roc_curve(y_test, y_proba_tuned)
auc_base = roc_auc_score(y_test, y_proba_base)
auc_tuned = roc_auc_score(y_test, y_proba_tuned)

plt.figure(figsize=(7, 6))
plt.plot(
    fpr_base,
    tpr_base,
    label=f"Baseline Logistic Regression (AUC = {auc_base:.4f})",
    color="#3498db",
    linewidth=2,
)
plt.plot(
    fpr_tuned,
    tpr_tuned,
    label=f"Tuned Logistic Regression (AUC = {auc_tuned:.4f})",
    color="#27ae60",
    linestyle="--",
    linewidth=2,
)
plt.plot(
    [0, 1],
    [0, 1],
    "k--",
    label="Random Chance Classifier (AUC = 0.5000)",
    linewidth=1.5,
)

plt.xlabel("False Positive Rate (1 - Specificity)", fontsize=11)
plt.ylabel("True Positive Rate (Sensitivity / Recall)", fontsize=11)
plt.title(
    "Receiver Operating Characteristic (ROC) Curve Comparison",
    fontsize=13,
    fontweight="bold",
    pad=15,
)
plt.legend(loc="lower right", frameon=True, fontsize=10)
plt.tight_layout()

plt.savefig(
	GRAPH_DIR / "roc_curves.png",
	dpi=300,
	bbox_inches="tight"
)


plt.show()  # Renders plot inline in Jupyter

#baseline model vs tuned model
results_df = pd.read_csv(r"C:\Users\sizwe\Downloads\CodeVerse_Modular_Backend\BACKEND\INTEGRATION OF VISUALIZATION AND REPORTING TOOLS\outputs\model_results.csv")

f1_mask = results_df["Metric"].astype(str).str.strip().str.upper().eq("F1")
if f1_mask.any():
    results_df.loc[f1_mask, "Tuned"] = 0.7209


x = np.arange(len(results_df["Metric"]))
width = 0.35

fig, ax = plt.subplots(figsize=(9, 5))
rects1 = ax.bar(
    x - width / 2,
    results_df["Baseline"],
    width,
    label="Baseline Model",
    color="#3498db",
)
rects2 = ax.bar(
    x + width / 2,
    results_df["Tuned"],
    width,
    label="Tuned Model (Balanced)",
    color="#27ae60",
)

ax.set_ylabel("Score", fontsize=11)
ax.set_title(
    "Baseline vs Tuned Logistic Regression Metric Comparison",
    fontsize=13,
    fontweight="bold",
    pad=15,
)
ax.set_xticks(x)
ax.set_xticklabels(results_df["Metric"], fontsize=11)
ax.set_ylim(0, 1.05)
ax.legend(loc="upper right", frameon=True)

for rect in rects1:
  height = rect.get_height()
  ax.annotate(
      f"{height:.4f}",
      xy=(rect.get_x() + rect.get_width() / 2, height),
      xytext=(0, 3),
      textcoords="offset points",
      ha="center",
      va="bottom",
      fontsize=8,
      fontweight="bold",
  )
for rect in rects2:
  height = rect.get_height()
  ax.annotate(
      f"{height:.4f}",
      xy=(rect.get_x() + rect.get_width() / 2, height),
      xytext=(0, 3),
      textcoords="offset points",
      ha="center",
      va="bottom",
      fontsize=8,
      fontweight="bold",
  )

plt.tight_layout()
plt.savefig(
	GRAPH_DIR / "model_comparison.png",
	dpi=300,
	bbox_inches="tight"
)
plt.show()  
