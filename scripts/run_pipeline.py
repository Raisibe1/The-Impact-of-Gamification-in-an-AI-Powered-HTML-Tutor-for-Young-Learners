# Master pipeline script for all datasets.
# This script runs preprocessing for StudyChat, ASSISTments, EdNet, and ConvoLearn.
#
# Usage:
#     python scripts/run_pipeline.py

import os
import sys
import time
import pandas as pd

# Import preprocessing functions
from preprocess_studychat import load_data as load_studychat, clean_data as clean_studychat, save_data as save_studychat


def print_header(title):
    # Print a formatted header.
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def check_data_exists():
    # Check if raw data files exist.
    print_header("STEP 1: CHECKING RAW DATA")
    
    required_files = {
        'StudyChat': 'data/raw/studychat.csv',
        'ASSISTments': 'data/raw/assistments.csv',
        'ConvoLearn': 'data/raw/convolearn.csv',
        'EdNet-KT3': 'data/raw/KT3/',
    }
    
    all_present = True
    for name, path in required_files.items():
        if os.path.exists(path):
            print(f"  [OK] {name}: {path}")
        else:
            print(f"  [MISSING] {name}: {path}")
            all_present = False
    
    if not all_present:
        print("\n  [WARNING] Some files are missing.")
        print("  Download from Google Drive link in README.md")
        print("  Continuing with available datasets...")
    
    return all_present


def run_studychat_pipeline():
    # Run StudyChat preprocessing.
    print_header("STEP 2: STUDYCHAT PREPROCESSING")
    
    if not os.path.exists('data/raw/studychat.csv'):
        print("  [SKIPPED] studychat.csv not found")
        return None
    
    start = time.time()
    
    df = load_studychat('data/raw/studychat.csv')
    df_cleaned = clean_studychat(df)
    save_studychat(df_cleaned, 'data/processed/studychat_cleaned.csv')
    
    elapsed = time.time() - start
    print(f"\n  [DONE] Completed in {elapsed:.2f} seconds")
    print(f"  Rows: {len(df_cleaned)}")
    print(f"  Classes: {df_cleaned['label'].nunique()}")
    
    return df_cleaned


def run_assistments_pipeline():
    # Run ASSISTments preprocessing.
    print_header("STEP 3: ASSISTMENTS PREPROCESSING")
    
    if not os.path.exists('data/raw/assistments.csv'):
        print("  [SKIPPED] assistments.csv not found")
        return None
    
    start = time.time()
    
    print("  Loading raw data...")
    df = pd.read_csv('data/raw/assistments.csv')
    print(f"  Loaded {len(df)} rows")
    
    # Basic cleaning
    df_cleaned = df.dropna()
    print(f"  After dropping NA: {len(df_cleaned)} rows")
    
    # Save
    os.makedirs('data/processed', exist_ok=True)
    df_cleaned.to_csv('data/processed/assistments_cleaned.csv', index=False)
    print(f"  Saved to data/processed/assistments_cleaned.csv")
    
    elapsed = time.time() - start
    print(f"\n  [DONE] Completed in {elapsed:.2f} seconds")
    
    return df_cleaned


def run_convolearn_pipeline():
    # Run ConvoLearn preprocessing.
    print_header("STEP 4: CONVOLEARN PREPROCESSING")
    
    if not os.path.exists('data/raw/convolearn.csv'):
        print("  [SKIPPED] convolearn.csv not found")
        return None
    
    start = time.time()
    
    print("  Loading raw data...")
    df = pd.read_csv('data/raw/convolearn.csv')
    print(f"  Loaded {len(df)} rows")
    
    # Save as-is for now (team will process further)
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv('data/processed/convolearn_cleaned.csv', index=False)
    print(f"  Saved to data/processed/convolearn_cleaned.csv")
    
    elapsed = time.time() - start
    print(f"\n  [DONE] Completed in {elapsed:.2f} seconds")
    
    return df


def run_ednet_pipeline():
    # Check EdNet data (large - just verify).
    print_header("STEP 5: EDNET-KT3 VERIFICATION")
    
    ednet_path = 'data/raw/KT3/'
    if not os.path.exists(ednet_path):
        print("  [SKIPPED] KT3 folder not found")
        return None
    
    files = os.listdir(ednet_path)
    print(f"  Found {len(files)} student files")
    print(f"  Sample files: {files[:5]}")
    
    # Load one file to verify structure
    if files:
        sample = pd.read_csv(os.path.join(ednet_path, files[0]))
        print(f"\n  Sample file structure:")
        print(f"  Columns: {list(sample.columns)}")
        print(f"  Rows in sample: {len(sample)}")
    
    print("\n  [DONE] EdNet verified (no preprocessing needed at this stage)")
    
    return None


def print_summary(results):
    # Print final summary.
    print_header("PIPELINE SUMMARY")
    
    print("\n  Datasets processed:")
    for name, df in results.items():
        if df is not None:
            print(f"    [OK] {name}: {len(df)} rows")
        else:
            print(f"    [SKIPPED] {name}")
    
    print("\n  Output folder: data/processed/")
    print("  Pipeline complete!")
    print("\n  Next steps:")
    print("    1. Model training (ML Engineer)")
    print("    2. Model evaluation (ML Engineer)")
    print("    3. Backend integration (Backend Developer)")


def main():
    # Main pipeline function.
    print("\n" + "=" * 60)
    print("  MASTER DATA PIPELINE")
    print("  AI-Powered HTML Tutor Project")
    print("=" * 60)
    
    start_time = time.time()
    
    # Step 1: Check data
    check_data_exists()
    
    # Step 2-5: Run each dataset pipeline
    results = {}
    results['StudyChat'] = run_studychat_pipeline()
    results['ASSISTments'] = run_assistments_pipeline()
    results['ConvoLearn'] = run_convolearn_pipeline()
    results['EdNet-KT3'] = run_ednet_pipeline()
    
    # Summary
    print_summary(results)
    
    total_time = time.time() - start_time
    print(f"\n  Total pipeline time: {total_time:.2f} seconds")


if __name__ == "__main__":
    main()