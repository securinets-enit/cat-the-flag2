#!/usr/bin/env python3
"""
Challenge 1: The Postcard from the Zodiac - Solution Script
This script demonstrates the solution steps for verification purposes.
"""

import subprocess
import os

def run_command(command, description):
    """Run a command and return the result"""
    print(f"\n🔍 {description}")
    print(f"Command: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            print("✅ Success!")
            if result.stdout:
                print("Output:")
                print(result.stdout)
        else:
            print("❌ Failed!")
            if result.stderr:
                print("Error:")
                print(result.stderr)
        return result.returncode == 0
    except (subprocess.SubprocessError, OSError) as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🎯 Challenge 1: The Postcard from the Zodiac - Solution Verification")
    print("=" * 70)
    
    # Check if the postcard file exists
    if not os.path.exists("challenge1_postcard.jpg"):
        print("❌ Error: challenge1_postcard.jpg not found!")
        print("Please place the challenge file in the same directory as this script.")
        return
    
    print("📁 Files found:")
    print(f"  - challenge1_postcard.jpg ({os.path.getsize('challenge1_postcard.jpg')} bytes)")
    
    # Step 1: Extract metadata
    print("\n" + "="*50)
    print("STEP 1: Metadata Analysis")
    print("="*50)
    
    success = run_command("exiftool challenge1_postcard.jpg", "Extracting metadata from postcard")
    
    if not success:
        print("❌ Metadata extraction failed. Make sure exiftool is installed.")
        return
    
    # Step 2: Extract hidden content with steghide
    print("\n" + "="*50)
    print("STEP 2: Steganography Extraction")
    print("="*50)
    
    # Check if steghide is available
    steghide_check = subprocess.run("which steghide", shell=True, capture_output=True, check=False)
    if steghide_check.returncode != 0:
        print("❌ Steghide not found. Please install it first:")
        print("   sudo apt-get install steghide")
        return
    
    # Extract the hidden file
    success = run_command(
        'steghide extract -sf challenge1_postcard.jpg -p "Tr4cK_Th3_Tr41l"',
        "Extracting hidden content with password 'Tr4cK_Th3_Tr41l'"
    )
    
    if not success:
        print("❌ Steganography extraction failed.")
        return
    
    # Step 3: Check extracted file
    print("\n" + "="*50)
    print("STEP 3: Analyzing Extracted Content")
    print("="*50)
    
    if os.path.exists("Zodiac.jpg"):
        print("✅ Hidden file extracted successfully!")
        print(f"  - Zodiac.jpg ({os.path.getsize('Zodiac.jpg')} bytes)")
        
        # Extract metadata from the hidden image
        run_command("exiftool Zodiac.jpg", "Extracting metadata from hidden image")
        
        print("\n🎉 Challenge completed!")
        print("The hidden image contains the flag and a clue for the next challenge.")
        print("Check the metadata of Zodiac.jpg for the pastebin link!")
        
    else:
        print("❌ Hidden file not found after extraction.")
        return

if __name__ == "__main__":
    main() 