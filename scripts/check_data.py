import os

def check_data():
    """Check if raw data exists and provide instructions."""
    raw_dir = 'data/raw/'
    
    required = [ 'convolearn.csv', 'studychat.csv', 'assistments.csv']
    missing = []
    
    for item in required:
        if not os.path.exists(os.path.join(raw_dir, item)):
            missing.append(item)
    
    if missing:
        print(" Missing raw data files/folders:")
        for item in missing:
            print(f"   - {item}")
        print("\n Download from Google Drive:")
        print("   https://drive.google.com/drive/folders/1m1XdbMPcJKMS7myBaH5byA77xEnmgzMn?usp=sharing")
        print(f"   Extract/move files to: {raw_dir}")
        return False
    else:
        print(" All raw data found!")
        return True

if __name__ == "__main__":
    check_data()