# Preprocessing script for StudyChat dataset.
# This script cleans and prepares the data for model training.
#
# Usage:
# python scripts/preprocess_studychat.py

import pandas as pd
import numpy as np
import json
import ast
import os


def load_data(path='data/raw/studychat.csv'):
    # Load raw StudyChat data.
    print("Loading raw data...")
    df = pd.read_csv(path)
    print(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    return df


def extract_label(label_str):
    # Extract label from llm_label JSON string.
    try:
        if isinstance(label_str, str):
            label_dict = json.loads(label_str)
            return label_dict.get('label', None)
        return None
    except Exception:
        try:
            label_dict = ast.literal_eval(label_str)
            return label_dict.get('label', None)
        except Exception:
            return None


def map_to_meta_category(label):
    # Map granular label to meta-category.
    if pd.isna(label):
        return 'Other'
    label = str(label).lower()
    if 'writing_requests' in label:
        return 'Writing'
    if 'conceptual_questions' in label:
        return 'Conceptual'
    if 'contextual_questions' in label:
        return 'Contextual'
    if 'provide_context' in label:
        return 'Providing Context'
    if 'verification' in label:
        return 'Verification'
    return 'Other'


def parse_messages(msg_str):
    # Parse messages JSON string.
    try:
        if isinstance(msg_str, str):
            return json.loads(msg_str)
        return msg_str
    except Exception:
        try:
            return ast.literal_eval(msg_str)
        except Exception:
            return None


def engineer_features(df):
    # Create new features.
    print("Engineering features...")
    df['prompt_length'] = df['prompt'].str.len()
    df['prompt_word_count'] = df['prompt'].str.split().str.len()
    df['response_length'] = df['response'].str.len()

    df['parsed_messages'] = df['messages'].apply(parse_messages)
    df['num_turns'] = df['parsed_messages'].apply(
        lambda x: len(x) if isinstance(x, list) else 0
    )
    return df


def clean_data(df):
    # Clean the dataset.
    print("Cleaning data...")

    # Extract target
    df['label'] = df['llm_label'].apply(extract_label)

    # Group into meta-categories
    df['meta_category'] = df['label'].apply(map_to_meta_category)

    # Feature engineering
    df = engineer_features(df)

    # Select final columns
    columns_to_keep = [
        'prompt', 'response', 'topic', 'meta_category',
        'prompt_length', 'prompt_word_count', 'response_length',
        'num_turns', 'chatId', 'userId', 'semester'
    ]

    df_cleaned = df[columns_to_keep].copy()
    df_cleaned = df_cleaned.rename(columns={
        'meta_category': 'label',
        'chatId': 'chat_id',
        'userId': 'user_id'
    })

    return df_cleaned


def save_data(df, path='data/processed/studychat_cleaned.csv'):
    # Save cleaned data.
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} rows to {path}")


def main():
    # Main preprocessing pipeline.
    print("=" * 60)
    print("STUDYCHAT PREPROCESSING PIPELINE")
    print("=" * 60)

    # Load
    df = load_data()

    # Clean
    df_cleaned = clean_data(df)

    # Save
    save_data(df_cleaned)

    # Summary
    print("\n" + "=" * 60)
    print("PREPROCESSING SUMMARY")
    print("=" * 60)
    print(f"Original rows: {len(df)}")
    print(f"Cleaned rows: {len(df_cleaned)}")
    print(f"Final columns: {list(df_cleaned.columns)}")
    print("\nTarget distribution:")
    print(df_cleaned['label'].value_counts())
    print("\nPreprocessing complete!")


if __name__ == "__main__":
    main()