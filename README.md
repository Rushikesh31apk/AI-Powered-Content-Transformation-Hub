# AI-Powered-Content-Transformation-Hub

# AI-Powered Content Transformation Hub

A modern web application for AI-powered content transformation with features like text summarization, text-to-speech, speech-to-text, and OCR.

## 🎓 Academic Project
**University:** Savitribai Phule Pune University  
**Tech Stack:** Python Flask, SQLite, Bootstrap 5  
**Theme:** Modern Yellow & Black Premium UI

## ✨ Features

1. **User Authentication**
   - Register with email and password
   - Secure login system
   - Profile image upload
   - Free and Paid user roles

2. **AI Features**
   - **Text Summarization**: Transform long texts into concise summaries
   - **Text to Speech**: Convert text into audio
   - **Speech to Text**: Transcribe audio files to text
   - **OCR**: Extract text from images

3. **User Dashboard**
   - Clean, modern interface
   - Feature cards with hover animations
   - Profile management
   - Role-based access

## 📁 Project Structure

```
ai_hub_project/
│
├── app.py                 # Main Flask application
├── database.db           # SQLite database (auto-created)
├── README.md             # This file
│
├── templates/            # HTML templates
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── summarize.html
│   ├── tts.html
│   ├── stt.html
│   ├── ocr.html
│   └── profile.html
│
└── static/              # Static files
    ├── css/
    │   └── style.css    # Custom styles
    ├── js/
    │   └── main.js      # JavaScript functions
    ├── images/          # Static images
    └── uploads/         # User uploaded files
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install flask
pip install werkzeug
```

### Step 2: Create Project Structure

Create the following folder structure:

```
ai_hub_project/
├── app.py
├── templates/
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── uploads/
```

### Step 3: Copy Files

1. Copy `app.py` to the root directory
2. Copy all HTML files to `templates/` folder
3. Copy `style.css` to `static/css/` folder
4. Copy `main.js` to `static/js/` folder

### Step 4: Run the Application

```bash
python app.py
```

The application will start at: `http://127.0.0.1:5000/`

## 📝 Usage Guide

### 1. Register an Account
- Go to `http://127.0.0.1:5000/`
- Click on "Register here"
- Fill in your details:
  - Full Name
  - Email
  - Password
  - Role (Free User / Paid User)
  - Profile Image (optional)
- Click "Register"

### 2. Login
- Enter your email and password
- Click "Login"
- You'll be redirected to the dashboard

### 3. Use Features

**Text Summarization:**
- Click on "Summarization" from navbar or dashboard
- Paste your long text
- Click "Generate Summary"
- View the summarized text

**Text to Speech:**
- Click on "Text to Speech"
- Enter your text
- Select voice (Premium voices for paid users)
- Click "Convert to Audio"

**Speech to Text:**
- Click on "Speech to Text"
- Upload an audio file
- Click "Convert to Text"
- View and copy the transcribed text

**OCR:**
- Click on "OCR"
- Upload an image
- Click "Extract Text"
- View and copy the extracted text

### 4. Profile Management
- Click on your name in the navbar
- Select "Profile" from dropdown
- View your account details
- Upgrade to premium (UI only)

## 🎨 UI Features

- **Color Scheme**: Yellow (#f5c518) and Black (#0f0f0f)
- **Responsive Design**: Works on all devices
- **Smooth Animations**: Hover effects and transitions
- **Modern Cards**: Rounded corners with yellow borders
- **Clean Layout**: Easy to navigate
- **Bootstrap Icons**: Professional icon set

## 🔐 Security Features

- Password hashing using werkzeug
- Session-based authentication
- Secure file uploads
- SQL injection prevention

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'Free User',
    profile_image TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## 🛠️ Customization

### Change Secret Key
In `app.py`, update:
```python
app.secret_key = 'your-secret-key-change-this-in-production'
```

### Change Colors
In `static/css/style.css`, modify:
```css
:root {
    --primary-yellow: #f5c518;
    --dark-bg: #0f0f0f;
    --card-bg: #1a1a1a;
}
```

### Add Real AI APIs
The current implementation uses placeholder logic. To add real AI features:

1. **For TTS**: Use Google Cloud TTS, Amazon Polly, or gTTS
2. **For STT**: Use Google Cloud Speech-to-Text or Assembly AI
3. **For OCR**: Use Tesseract, Google Vision API, or Azure Computer Vision
4. **For Summarization**: Use OpenAI API, Hugging Face, or custom models

## 📌 Important Notes

1. **Database**: `database.db` is created automatically on first run
2. **Uploads**: Profile images are stored in `static/uploads/`
3. **File Size**: Max upload size is 16MB
4. **AI Features**: Currently use placeholder logic for demonstration
5. **Production**: Change secret key and add proper security measures

## 🐛 Troubleshooting

**Issue: Database error**
- Delete `database.db` and restart the application

**Issue: Import errors**
- Make sure all dependencies are installed: `pip install flask werkzeug`

**Issue: Upload folder not found**
- Create `static/uploads/` folder manually

**Issue: Template not found**
- Check that all HTML files are in the `templates/` folder

## 📚 Future Enhancements

- [ ] Implement real AI APIs
- [ ] Add payment integration for premium users
- [ ] Email verification
- [ ] Password reset functionality
- [ ] Usage analytics
- [ ] File history
- [ ] Export features
- [ ] Multi-language support

## 👨‍💻 Development

This project is designed for college submissions and learning purposes. The code is:
- Well-commented
- Easy to understand
- Beginner-friendly
- Ready for demonstrations

## 📄 License

This project is created for educational purposes.

## 🤝 Support

For any issues or questions, please refer to:
- Flask documentation: https://flask.palletsprojects.com/
- Bootstrap documentation: https://getbootstrap.com/
- SQLite documentation: https://www.sqlite.org/

---

**Created with ❤️ for Savitribai Phule Pune University**
