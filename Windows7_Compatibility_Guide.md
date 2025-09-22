# Windows 7 Compatibility Guide
# উইন্ডোজ ৭ সামঞ্জস্য গাইড

## সমস্যা (Problem)
আপনি যখন Windows 7 এ Gmail OAuth Generator চালানোর চেষ্টা করেন, তখন এই error দেখতে পান:
```
The program can't start because api-ms-win-core-path-l1-1-0.dll is missing from your computer.
```

## কারণ (Cause)
এই সমস্যাটি হয় কারণ:
- আধুনিক Python versions এবং PyInstaller Windows 7 এর সাথে সরাসরি compatible নয়
- api-ms-win-core-path-l1-1-0.dll একটি Windows API যা Windows 8+ এ আছে কিন্তু Windows 7 এ নেই
- UPX compression Windows 7 এ সমস্যা সৃষ্টি করে

## সমাধান (Solutions)

### ১. নতুন Compatible Build তৈরি করুন
আমি আপনার জন্য PyInstaller configuration update করেছি। এখন নতুন build তৈরি করুন:

```bash
python build_exe.py
```

### ২. Manual PyInstaller Command (যদি build script কাজ না করে)
```bash
pyinstaller --onefile --noconsole --noupx --target-architecture=x86_64 --exclude-module=_tkinter --exclude-module=tkinter.dnd --name=Gmail_OAuth_Generator main.py
```

### ৩. Python Version Downgrade (যদি এখনও সমস্যা হয়)
Windows 7 এর জন্য Python 3.8 বা তার নিচের version ব্যবহার করুন:
- Python 3.8.10 (সর্বোচ্চ recommended)
- Python 3.7.9

### ৪. Alternative Solution - Portable Python
1. Portable Python 3.8 download করুন
2. সেই Python দিয়ে application build করুন
3. Dependencies manually copy করুন

## Updated Configuration

### PyInstaller Spec File Changes:
- `upx=False` - UPX compression disable
- `target_arch='x86_64'` - Architecture specify
- Compatibility options added

### Build Script Changes:
- `--noupx` flag added
- `--target-architecture=x86_64` specified
- `--compatibility-mode` enabled
- Problematic modules excluded

## Testing on Different Windows Versions

### Windows 7:
- ✅ Should work with new build
- ⚠️ May need Visual C++ Redistributable 2015-2019

### Windows 8/8.1:
- ✅ Should work perfectly

### Windows 10/11:
- ✅ Will work without issues

## Additional Requirements for Windows 7

1. **Microsoft Visual C++ Redistributable**:
   - Download এবং install করুন: vc_redist.x64.exe
   - Link: https://aka.ms/vs/17/release/vc_redist.x64.exe

2. **Windows Updates**:
   - Windows 7 SP1 installed থাকতে হবে
   - Latest Windows updates install করুন

3. **.NET Framework**:
   - .NET Framework 4.7.2 বা তার উপরে

## Troubleshooting

### যদি এখনও error আসে:
1. Antivirus disable করে দেখুন
2. Administrator হিসেবে run করুন
3. Compatibility mode এ run করুন (Windows 8 compatibility)
4. Windows Defender বা অন্য security software check করুন

### Log File Check:
যদি application crash হয়, এই locations এ log file দেখুন:
- `%TEMP%\Gmail_OAuth_Generator.log`
- Application directory তে error.log

## Contact
যদি এখনও সমস্যা হয়, তাহলে:
1. Windows version check করুন: `winver`
2. Python version check করুন: `python --version`
3. Error message এর screenshot নিন
4. System specifications share করুন

---

**Note**: Windows 7 support Microsoft officially বন্ধ করে দিয়েছে। Security এবং performance এর জন্য Windows 10 বা 11 এ upgrade করার পরামর্শ দেওয়া হচ্ছে।