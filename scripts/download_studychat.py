from datasets import load_dataset
import pandas as pd
import os

# Create directory if it doesn't exist
os.makedirs('data/raw', exist_ok=True)

print(" Downloading StudyChat dataset...")
print(" This may take a few minutes...")

try:
    # Load the dataset
    dataset = load_dataset("wmcnicho/StudyChat", split="train")
    
    print(f"Loaded {len(dataset)} conversations!")
    
    # Convert to pandas DataFrame
    df = pd.DataFrame(dataset)
    
    # Save to CSV
    output_path = 'data/raw/studychat.csv'
    df.to_csv(output_path, index=False)
    
    print(f" Saved to {output_path}")
    print(f" File size: {os.path.getsize(output_path) / 1024:.2f} KB")
    
except Exception as e:
    print(f" Error: {e}")
    print("\n Troubleshooting tips:")
    print("1. Make sure you logged in: huggingface-cli login")
    print("2. Make sure you accepted the terms on Hugging Face")
    print("3. Check your internet connection")