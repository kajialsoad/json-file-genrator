# Gmail OAuth Client JSON Generator
## স্বয়ংক্রিয় জিমেইল OAuth ক্লায়েন্ট জেনারেটর

### প্রজেক্ট বিবরণ
এই অ্যাপ্লিকেশনটি একটি Python ডেস্কটপ অ্যাপ্লিকেশন যা ব্যবহারকারীর কাছ থেকে ইমেল এবং পাসওয়ার্ড নিয়ে স্বয়ংক্রিয়ভাবে Gmail OAuth ক্লায়েন্ট তৈরি করে এবং JSON ফাইল হিসেবে আউটপুট দেয়।

### বৈশিষ্ট্যসমূহ
- 🖥️ **Tkinter GUI**: সহজ এবং ব্যবহারকারী-বান্ধব ইন্টারফেস
- 🤖 **Selenium Automation**: Google Cloud Console এর সাথে স্বয়ংক্রিয় ইন্টারঅ্যাকশন
- 📁 **Batch Processing**: একসাথে একাধিক অ্যাকাউন্ট প্রক্রিয়া করা
- 📊 **Progress Tracking**: রিয়েল-টাইম অগ্রগতি প্রদর্শন
- 📄 **JSON Output**: OAuth credentials JSON ফরম্যাটে সংরক্ষণ
- 🔒 **Error Handling**: ত্রুটি বার্তা এবং ব্যতিক্রম পরিচালনা

### প্রয়োজনীয়তা
- Python 3.9 বা তার উপরে
- Google Chrome ব্রাউজার
- ইন্টারনেট সংযোগ

### ইনস্টলেশন

1. **Repository clone করুন:**
   ```bash
   git clone <repository-url>
   cd gmail-oauth-client-generator
   ```

2. **Dependencies ইনস্টল করুন:**
   ```bash
   pip install -r requirements.txt
   ```

3. **অ্যাপ্লিকেশন চালান:**
   ```bash
   python main.py
   ```

### ব্যবহারের নির্দেশনা

#### 1. অ্যাকাউন্ট ফাইল প্রস্তুত করুন
`accounts.txt` ফাইলে আপনার Gmail অ্যাকাউন্টগুলো নিম্নলিখিত ফরম্যাটে যোগ করুন:
```
email1@gmail.com:password1
email2@gmail.com:password2
email3@gmail.com:password3
```

#### 2. অ্যাপ্লিকেশন চালান
- `python main.py` কমান্ড দিয়ে অ্যাপ্লিকেশন চালু করুন
- "Browse" বাটন চেপে আপনার accounts.txt ফাইল নির্বাচন করুন
- "Generate JSON Files" বাটন চাপুন

#### 3. আউটপুট দেখুন
- প্রক্রিয়া সম্পন্ন হলে `output/` ফোল্ডারে JSON ফাইলগুলো পাবেন
- প্রতিটি অ্যাকাউন্টের জন্য আলাদা JSON ফাইল তৈরি হবে

### ফাইল স্ট্রাকচার
```
gmail-oauth-client-generator/
├── main.py                 # মূল অ্যাপ্লিকেশন ফাইল
├── requirements.txt        # Python dependencies
├── accounts.txt           # ইনপুট অ্যাকাউন্ট ফাইল (স্যাম্পল)
├── output/                # Generated JSON ফাইলের ফোল্ডার
├── README.md              # এই ফাইল
└── .gitignore            # Git ignore ফাইল
```

### JSON আউটপুট ফরম্যাট
```json
{
  "email": "user@gmail.com",
  "password": "userpassword",
  "client_id": "generated_client_id",
  "client_secret": "generated_client_secret",
  "redirect_uris": ["http://localhost:8080/callback"],
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "project_id": "gmail-oauth-project",
  "created_at": "2024-01-01 12:00:00"
}
```

### .exe ফাইল তৈরি করা

PyInstaller ব্যবহার করে standalone .exe ফাইল তৈরি করতে:

```bash
pyinstaller --onefile --noconsole --name="Gmail_OAuth_Generator" main.py
```

তৈরি হওয়া .exe ফাইল `dist/` ফোল্ডারে পাবেন।

### সতর্কতা ⚠️

1. **নিরাপত্তা**: আপনার Gmail পাসওয়ার্ড সুরক্ষিত রাখুন
2. **Google নীতি**: Google এর Terms of Service মেনে চলুন
3. **2FA**: যদি 2-Factor Authentication চালু থাকে, App Password ব্যবহার করুন
4. **Rate Limiting**: অতিরিক্ত দ্রুত অনুরোধ এড়িয়ে চলুন

### সমস্যা সমাধান

#### সাধারণ সমস্যা:
1. **ChromeDriver Error**: Chrome ব্রাউজার আপডেট করুন
2. **Login Failed**: ইমেল/পাসওয়ার্ড যাচাই করুন
3. **Permission Denied**: অ্যাপটি Administrator হিসেবে চালান

### অবদান
এই প্রজেক্টে অবদান রাখতে চাইলে:
1. Fork করুন
2. Feature branch তৈরি করুন
3. Changes commit করুন
4. Pull request পাঠান

### লাইসেন্স
এই প্রজেক্টটি MIT লাইসেন্সের অধীনে প্রকাশিত।

### যোগাযোগ
কোনো প্রশ্ন বা সহায়তার জন্য issue তৈরি করুন।

---
**বিঃদ্রঃ**: এই অ্যাপ্লিকেশনটি শিক্ষামূলক উদ্দেশ্যে তৈরি। ব্যবহারের আগে Google এর নীতিমালা পড়ুন।