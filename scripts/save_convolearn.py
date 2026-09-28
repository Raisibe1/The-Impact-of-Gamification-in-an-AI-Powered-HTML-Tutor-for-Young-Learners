from datasets import load_dataset
import pandas as pd
import os

# Create directory if it doesn't exist
os.makedirs('data/raw', exist_ok=True)

print(" Loading ConvoLearn from Hugging Face...")
dataset = load_dataset("masharma/convolearn", split="train")

print(f" Loaded {len(dataset)} conversations!")

# Convert to pandas DataFrame
df = pd.DataFrame(dataset)

# Save to CSV
output_path = 'data/raw/convolearn.csv'
df.to_csv(output_path, index=False)

print(f" Saved to {output_path}")
print(f"File size: {os.path.getsize(output_path) / 1024:.2f} KB")
