import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. LOAD EXCEL DATASET USING pd.read_excel()
# ==========================================
file_path = r"C:\Users\sizwe\Downloads\CodeVerse_Modular_Backend\BACKEND\INTEGRATION OF VISUALIZATION AND REPORTING TOOLS\outputs\ASSISTments_mastery_prediction_training.csv"

print(f"Loading dataset from: {file_path}")
df = pd.read_csv(file_path)
print(df.head())
print(df.shape)
# ==========================================
# 2. CONFIGURATION & OUTPUT SETUP
# ==========================================
OUTPUT_DIR = 'all_learner_reports'
EXPORT_FORMAT = 'pdf'  

def generate_all_learner_reports(df, max_learners=None):
    """
    Reads the prediction dataframe and generates individual visual progress 
    dashboards for each learner.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if 'learner_id' not in df.columns:
        raise ValueError("The dataset does not contain a 'learner_id' column.")
        
    unique_learners = df['learner_id'].unique()
    
    if max_learners:
        unique_learners = unique_learners[:max_learners]
        
    print(f"Generating {EXPORT_FORMAT.upper()} reports for {len(unique_learners)} learners...")
    sns.set_theme(style="whitegrid")

    for idx, lid in enumerate(unique_learners, start=1):
        ldata = df[df['learner_id'] == lid]
        
        sort_col = 'interaction_index' if 'interaction_index' in ldata.columns else ldata.columns[0]
        ldata = ldata.sort_values(sort_col)
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 9))
        fig.suptitle(f"Individual Learner Analytics Report — Learner ID: {lid}", fontsize=15, fontweight='bold')

        # 1. Cumulative Accuracy Trajectory
        acc_col = 'prior_accuracy' if 'prior_accuracy' in ldata.columns else ldata.columns[1]
        sns.lineplot(data=ldata, x=sort_col, y=acc_col, marker='o', ax=axes[0, 0], color='teal')
        axes[0, 0].set_title('Accuracy Trajectory')
        axes[0, 0].set_xlabel('Interaction Index')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].set_ylim(-0.05, 1.05)

        # 2. Correctness per Interaction (0 = Incorrect, 1 = Correct)
        correct_col = 'correct' if 'correct' in ldata.columns else ldata.columns[2]
        colors = ['coral' if c == 0 else 'mediumseagreen' for c in ldata[correct_col]]
        axes[0, 1].bar(ldata[sort_col].astype(str), ldata[correct_col], color=colors)
        axes[0, 1].set_title('Correctness per Interaction (0 = Incorrect, 1 = Correct)')
        axes[0, 1].set_xlabel('Interaction Index')
        axes[0, 1].set_ylabel('Correctness')
        axes[0, 1].set_ylim(0, 1.15)
        if len(ldata) > 15:
            axes[0, 1].tick_params(axis='x', rotation=45, labelsize=8)

        # 3. Mastery Proxy Progression
        proxy_col = 'mastery_proxy_after_interaction' if 'mastery_proxy_after_interaction' in ldata.columns else (ldata.columns[3] if len(ldata.columns) > 3 else acc_col)
        sns.lineplot(data=ldata, x=sort_col, y=proxy_col, marker='s', ax=axes[1, 0], color='purple')
        axes[1, 0].set_title('Mastery Proxy / Prediction Progression')
        axes[1, 0].set_xlabel('Interaction Index')
        axes[1, 0].set_ylabel('Score / Probability')
        axes[1, 0].set_ylim(-0.05, 1.05)

        # 4. Attempt Counts per Interaction
        attempt_col = 'attempt_count' if 'attempt_count' in ldata.columns else ldata.columns[4] if len(ldata.columns) > 4 else sort_col
        axes[1, 1].bar(ldata[sort_col].astype(str), ldata[attempt_col], color='dodgerblue')
        axes[1, 1].set_title('Attempt Counts per Interaction')
        axes[1, 1].set_xlabel('Interaction Index')
        axes[1, 1].set_ylabel('Attempt Count')
        if len(ldata) > 15:
            axes[1, 1].tick_params(axis='x', rotation=45, labelsize=8)

        plt.tight_layout()
        
        out_file = os.path.join(OUTPUT_DIR, f"learner_{lid}_report.{EXPORT_FORMAT}")
        plt.savefig(out_file, format=EXPORT_FORMAT, dpi=200)
        plt.close(fig)

        if idx % 50 == 0 or idx == len(unique_learners):
            print(f"Processed {idx}/{len(unique_learners)} learners...")

    print(f"All reports successfully generated and saved to '{OUTPUT_DIR}/'.")

generate_all_learner_reports(df, max_learners=10)