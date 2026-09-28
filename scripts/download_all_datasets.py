from datasets import load_dataset
import os

print("=" * 60)
print(" DOWNLOADING ALL DATASETS")
print("=" * 60)

# 1. ConvoLearn (Smallest - Fastest)
print("\n Downloading ConvoLearn...")
try:
    convolearn = load_dataset("masharma/convolearn", split="train")
    print(f" ConvoLearn: {len(convolearn)} conversations")
except Exception as e:
    print(f" ConvoLearn error: {e}")

# 2. StudyChat
print("\ Downloading StudyChat...")
try:
    studychat = load_dataset("wmcnicho/StudyChat", split="train")
    print(f" StudyChat: {len(studychat)} conversations")
except Exception as e:
    print(f" StudyChat error: {e}")

# 3. ASSISTments (Large)
print("\n Downloading ASSISTments...")
try:
    assistments = load_dataset("assistments/2009-2010", split="train", streaming=True)
    # Get a sample to verify
    sample = next(iter(assistments))
    print(f" ASSISTments: Loaded successfully (streaming mode)")
    print(f"   Sample keys: {sample.keys()}")
except Exception as e:
    print(f" ASSISTments error: {e}")

# 4. EdNet (Largest - Takes time)
print("\n Downloading EdNet...")
try:
    ednet = load_dataset("ednet/ednet", split="train", streaming=True)
    sample = next(iter(ednet))
    print(f" EdNet: Loaded successfully (streaming mode)")
    print(f"   Sample keys: {sample.keys()}")
except Exception as e:
    print(f" EdNet error: {e}")

print("\n" + "=" * 60)
print("Download process complete!")
print("=" * 60)