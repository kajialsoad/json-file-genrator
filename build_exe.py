#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Script for Gmail OAuth Client JSON Generator
.exe ফাইল তৈরি করার জন্য বিল্ড স্ক্রিপ্ট
"""

import os
import sys
import subprocess
import shutil
import time
import psutil
from pathlib import Path

def kill_running_processes():
    """চলমান Gmail_OAuth_Generator.exe প্রসেস বন্ধ করা"""
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] and 'Gmail_OAuth_Generator' in proc.info['name']:
                print(f"🔄 চলমান প্রসেস বন্ধ করা হচ্ছে: {proc.info['name']} (PID: {proc.info['pid']})")
                try:
                    proc.terminate()
                    proc.wait(timeout=5)
                    print(f"✅ প্রসেস সফলভাবে বন্ধ হয়েছে")
                except (psutil.NoSuchProcess, psutil.TimeoutExpired):
                    try:
                        proc.kill()
                        print(f"✅ প্রসেস জোরপূর্বক বন্ধ করা হয়েছে")
                    except psutil.NoSuchProcess:
                        pass
    except Exception as e:
        print(f"⚠️ প্রসেস বন্ধ করতে সমস্যা: {e}")

def safe_remove_file(file_path, max_retries=3, delay=1):
    """নিরাপদে ফাইল মুছে ফেলা retry logic সহ"""
    for attempt in range(max_retries):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except PermissionError:
            if attempt < max_retries - 1:
                print(f"⚠️ ফাইল locked, {delay} সেকেন্ড অপেক্ষা করা হচ্ছে... (চেষ্টা {attempt + 1}/{max_retries})")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                print(f"❌ ফাইল মুছতে পারছি না: {file_path}")
                print(f"💡 সমাধান: ম্যানুয়ালি Gmail_OAuth_Generator.exe বন্ধ করুন এবং আবার চেষ্টা করুন")
                return False
        except Exception as e:
            print(f"❌ ফাইল মুছতে সমস্যা: {e}")
            return False
    return True

def safe_remove_directory(dir_path, max_retries=3, delay=1):
    """নিরাপদে ডিরেক্টরি মুছে ফেলা retry logic সহ"""
    for attempt in range(max_retries):
        try:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
                return True
        except PermissionError as e:
            if attempt < max_retries - 1:
                print(f"⚠️ ডিরেক্টরি locked, {delay} সেকেন্ড অপেক্ষা করা হচ্ছে... (চেষ্টা {attempt + 1}/{max_retries})")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                print(f"❌ ডিরেক্টরি মুছতে পারছি না: {dir_path}")
                print(f"💡 সমাধান: সকল Gmail_OAuth_Generator প্রসেস বন্ধ করুন এবং আবার চেষ্টা করুন")
                return False
        except Exception as e:
            print(f"❌ ডিরেক্টরি মুছতে সমস্যা: {e}")
            return False
    return True

def clean_build_dirs():
    """পুরানো build এবং dist ডিরেক্টরি পরিষ্কার করা"""
    # প্রথমে চলমান প্রসেস বন্ধ করা
    print("🔍 চলমান Gmail_OAuth_Generator প্রসেস খোঁজা হচ্ছে...")
    kill_running_processes()
    
    # কিছুক্ষণ অপেক্ষা করা
    time.sleep(2)
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"পরিষ্কার করা হচ্ছে: {dir_name}")
            if not safe_remove_directory(dir_name):
                print(f"❌ {dir_name} ডিরেক্টরি পরিষ্কার করতে ব্যর্থ")
                return False
            
    # Remove .spec files
    for spec_file in Path('.').glob('*.spec'):
        print(f"মুছে ফেলা হচ্ছে: {spec_file}")
        if not safe_remove_file(str(spec_file)):
            print(f"❌ {spec_file} ফাইল মুছতে ব্যর্থ")
            return False
    
    return True

def install_requirements():
    """প্রয়োজনীয় packages ইনস্টল করা"""
    print("প্রয়োজনীয় packages ইনস্টল করা হচ্ছে...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True, text=True)
        print("✅ সকল packages সফলভাবে ইনস্টল হয়েছে")
    except subprocess.CalledProcessError as e:
        print(f"❌ Package ইনস্টলেশনে সমস্যা: {e}")
        print(f"Error output: {e.stderr}")
        return False
    return True

def build_executable():
    """PyInstaller দিয়ে .exe ফাইল তৈরি করা"""
    print(".exe ফাইল তৈরি করা হচ্ছে...")
    
    # PyInstaller command with Windows 7 compatibility
    cmd = [
        'pyinstaller',
        '--onefile',                    # Single executable file
        '--noconsole',                  # No console window
        '--name=Gmail_OAuth_Generator', # Executable name
        '--icon=icon.ico',             # Icon (if exists)
        '--add-data=output;output',    # Include output directory
        '--hidden-import=selenium',     # Ensure selenium is included
        '--hidden-import=tkinter',      # Ensure tkinter is included
        '--hidden-import=_tkinter',     # Ensure _tkinter is included
        '--hidden-import=pymsgbox',     # Ensure pymsgbox is included
        '--noupx',                     # Disable UPX for Windows 7 compatibility
        '--target-architecture=x86_64', # Specify architecture
        'main.py'
    ]
    
    # Remove icon parameter if icon file doesn't exist
    if not os.path.exists('icon.ico'):
        cmd = [arg for arg in cmd if not arg.startswith('--icon')]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ .exe ফাইল সফলভাবে তৈরি হয়েছে")
        print(f"ফাইলের অবস্থান: dist/Gmail_OAuth_Generator.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ .exe তৈরিতে সমস্যা: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ PyInstaller পাওয়া যায়নি। প্রথমে ইনস্টল করুন: pip install pyinstaller")
        return False

def copy_additional_files():
    """অতিরিক্ত ফাইল dist ফোল্ডারে কপি করা"""
    print("অতিরিক্ত ফাইল কপি করা হচ্ছে...")
    
    files_to_copy = [
        'README.md',
        'accounts.txt',
        'requirements.txt'
    ]
    
    dist_dir = Path('dist')
    if not dist_dir.exists():
        dist_dir.mkdir()
    
    for file_name in files_to_copy:
        if os.path.exists(file_name):
            shutil.copy2(file_name, dist_dir / file_name)
            print(f"✅ কপি করা হয়েছে: {file_name}")
    
    # Create output directory in dist
    output_dir = dist_dir / 'output'
    if not output_dir.exists():
        output_dir.mkdir()
        print("✅ output ডিরেক্টরি তৈরি করা হয়েছে")

def main():
    """মূল বিল্ড প্রক্রিয়া"""
    print("=" * 50)
    print("Gmail OAuth Client JSON Generator")
    print(".exe Build Script")
    print("=" * 50)
    
    # Step 1: Clean previous builds
    print("\n1️⃣ পুরানো build ফাইল পরিষ্কার করা হচ্ছে...")
    if not clean_build_dirs():
        print("❌ Build প্রক্রিয়া বন্ধ করা হলো - ফাইল পরিষ্কার করতে ব্যর্থ")
        print("💡 সমাধান: Gmail_OAuth_Generator.exe বন্ধ করুন এবং আবার চেষ্টা করুন")
        return False
    
    # Step 2: Install requirements
    print("\n2️⃣ Dependencies ইনস্টল করা হচ্ছে...")
    if not install_requirements():
        print("❌ Build প্রক্রিয়া বন্ধ করা হলো")
        return False
    
    # Step 3: Build executable
    print("\n3️⃣ .exe ফাইল তৈরি করা হচ্ছে...")
    if not build_executable():
        print("❌ Build প্রক্রিয়া বন্ধ করা হলো")
        return False
    
    # Step 4: Copy additional files
    print("\n4️⃣ অতিরিক্ত ফাইল কপি করা হচ্ছে...")
    copy_additional_files()
    
    print("\n" + "=" * 50)
    print("🎉 Build সফলভাবে সম্পন্ন হয়েছে!")
    print("📁 ফাইলের অবস্থান: dist/Gmail_OAuth_Generator.exe")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)