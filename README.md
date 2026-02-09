# 🤖 AI-Powered Content Transformation Hub

<div align="center">

![AI Hub Banner](./docs/images/banner.png)

### Transform Your Content with Cutting-Edge AI Technology

[![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Sumy](https://img.shields.io/badge/Sumy-Text%20Summarization-FFD700?style=for-the-badge)](https://pypi.org/project/sumy/)
[![gTTS](https://img.shields.io/badge/gTTS-Text%20to%20Speech-34A853?style=for-the-badge&logo=google)](https://pypi.org/project/gTTS/)
[![SpeechRecognition](https://img.shields.io/badge/SpeechRecognition-Audio%20Processing-FF6F00?style=for-the-badge)](https://pypi.org/project/SpeechRecognition/)
[![Pytesseract](https://img.shields.io/badge/Pytesseract-OCR-000000?style=for-the-badge)](https://pypi.org/project/pytesseract/)
[![Werkzeug](https://img.shields.io/badge/Werkzeug-Security-CC0000?style=for-the-badge)](https://werkzeug.palletsprojects.com/)

[Features](#-key-features) • [Installation](#-installation--setup) • [Usage](#-usage-guide) • [Screenshots](#-project-screenshots) • [Documentation](#-documentation)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Project Screenshots](#-project-screenshots)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Usage Guide](#-usage-guide)
- [Database Schema](#-database-schema)
- [API Endpoints](#-api-endpoints)
- [Customization](#-customization)
- [Security Features](#-security-features)
- [Troubleshooting](#-troubleshooting)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 🌟 Overview

**AI Hub** is a modern, full-stack web application that leverages cutting-edge artificial intelligence to provide powerful content transformation tools. Built with Flask and featuring a sleek, responsive UI, this platform offers four core AI-powered features designed to enhance productivity and accessibility.

### 🎯 Mission

To democratize access to AI-powered content transformation tools, making advanced technology accessible to students, professionals, and content creators worldwide.

### 🏆 Why AI Hub?

- ✅ **All-in-One Platform**: Four powerful AI tools in a single application
- ✅ **User-Friendly Interface**: Clean, modern design with intuitive navigation
- ✅ **Secure & Reliable**: Enterprise-grade security with encrypted passwords
- ✅ **Free & Premium Tiers**: Flexible pricing for different user needs
- ✅ **Open Source**: Learn, modify, and contribute to the codebase

---

## ✨ Key Features

### 🔐 1. Authentication & User Management

<div align="center">

![Authentication System](./docs/images/01-login-page.png)
*Secure login interface with modern design*

</div>

- **User Registration** with profile image upload
- **Secure Login** with password hashing (Werkzeug)
- **Email Verification** system (ready for integration)
- **Password Reset** functionality
- **Session Management** for secure access
- **Role-Based Access Control** (Free/Paid users)
- **Profile Management** with editable user information

---

### 📝 2. Text Summarization

<div align="center">

![Text Summarization](./docs/images/02-summarization.png)
*AI-powered text summarization interface*

</div>

Transform lengthy documents into concise, meaningful summaries using advanced NLP algorithms.

**Features:**
- Intelligent sentence extraction
- Adjustable summary length
- Support for multiple text formats
- Copy-to-clipboard functionality
- Real-time processing

**Use Cases:**
- Research paper summaries
- Article condensation
- Meeting notes compression
- Report executive summaries

---

### 🔊 3. Text-to-Speech (TTS)

<div align="center">

![Text to Speech](./docs/images/03-text-to-speech.png)
*Convert text to natural-sounding audio*

</div>

Convert any text into high-quality, downloadable audio files with multiple voice options.

**Features:**
- Multiple voice selections
- Premium voices for paid users
- Downloadable MP3 audio files
- Adjustable speech rate
- Language support

**Use Cases:**
- Audiobook creation
- Accessibility tools
- Podcast generation
- Language learning

---

### 🎙️ 4. Speech-to-Text (STT)

<div align="center">

![Speech to Text](./docs/images/04-speech-to-text.png)
*Accurate audio transcription system*

</div>

Upload audio files and convert speech into accurate, editable text transcriptions.

**Features:**
- Multi-format audio support (MP3, WAV, M4A)
- Automatic WAV conversion
- High accuracy transcription
- Editable text output
- Copy & export functionality

**Use Cases:**
- Meeting transcriptions
- Interview documentation
- Lecture notes
- Podcast subtitles

---

### 🖼️ 5. Optical Character Recognition (OCR)

<div align="center">

![OCR System](./docs/images/05-ocr.png)
*Extract text from images with precision*

</div>

Upload images and extract readable text using advanced Tesseract OCR technology.

**Features:**
- Image-to-text conversion
- Support for JPG, PNG, PDF
- Clear text extraction
- Editable output
- Multi-language support (expandable)

**Use Cases:**
- Document digitization
- Business card scanning
- Receipt processing
- Handwritten note conversion

---

### 📊 6. User Dashboard

<div align="center">

![Dashboard](./docs/images/06-dashboard.png)
*Centralized control panel for all AI tools*

</div>

A clean, responsive dashboard providing quick access to all features and account management.

**Features:**
- Activity overview
- Quick access cards
- Usage statistics
- Profile shortcuts
- Responsive design

---

## 📸 Project Screenshots

### Landing Page & Authentication

<div align="center">

| Landing Page | Registration |
|:---:|:---:|
| ![Landing](./docs/images/07-landing-page.png) | ![Register](./docs/images/08-registration.png) |

| Password Reset | Email Verification |
|:---:|:---:|
| ![Reset](./docs/images/09-password-reset.png) | ![Verify](./docs/images/10-email-verification.png) |

</div>

### Core Features

<div align="center">

| Summarization Tool | TTS Interface |
|:---:|:---:|
| ![Summary](./docs/images/11-summarize-demo.png) | ![TTS](./docs/images/12-tts-demo.png) |

| STT Processing | OCR Extraction |
|:---:|:---:|
| ![STT](./docs/images/13-stt-demo.png) | ![OCR](./docs/images/14-ocr-demo.png) |

</div>

### User Experience

<div align="center">

| User Profile | Premium Upgrade |
|:---:|:---:|
| ![Profile](./docs/images/15-user-profile.png) | ![Upgrade](./docs/images/16-premium-upgrade.png) |

</div>

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 2.3+
- **Database**: SQLite3
- **Security**: Werkzeug (Password Hashing)
- **Session Management**: Flask-Session

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **JavaScript**: Interactive functionality
- **Bootstrap 5.3**: Responsive framework
- **Font Awesome**: Icon library

### AI & Machine Learning
- **Text Summarization**: Sumy (LSA Algorithm)
- **Text-to-Speech**: gTTS (Google Text-to-Speech)
- **Speech-to-Text**: SpeechRecognition
- **OCR**: Pytesseract (Tesseract-OCR)

### Additional Libraries
- **Pillow**: Image processing
- **pydub**: Audio manipulation
- **NLTK**: Natural language processing
- **email-validator**: Email validation

---

## 📁 Project Structure

```
ai_hub_project/
│
├── 📄 app.py                              # Main Flask application
├── 📄 database.db                         # SQLite database (auto-created)
├── 📄 README.md                           # Project documentation
├── 📄 requirements.txt                    # Python dependencies
├── 📄 .gitignore                          # Git ignore rules
│
├── 📂 templates/                          # HTML Templates
│   ├── 🏠 index.html                      # Landing page
│   ├── 🔐 register.html                   # User registration
│   ├── 🔑 login.html                      # User login
│   ├── ✉️  verify_email.html              # Email verification
│   ├── 🔒 forgot_password.html            # Password recovery
│   ├── 🔓 reset_password.html             # Password reset
│   ├── 📊 dashboard.html                  # User dashboard
│   ├── 👤 profile.html                    # User profile
│   ├── 📝 summarize.html                  # Text summarization
│   ├── 🔊 tts.html                        # Text-to-speech
│   ├── 🎙️ stt.html                        # Speech-to-text
│   └── 🖼️ ocr.html                        # OCR tool
│
├── 📂 static/                             # Static assets
│   ├── 📂 css/
│   │   └── style.css                      # Custom styles
│   ├── 📂 js/
│   │   └── main.js                        # JavaScript functions
│   ├── 📂 images/
│   │   ├── logo.png                       # Application logo
│   │   └── background.jpg                 # Background images
│   ├── 📂 uploads/                        # User uploads (auto-created)
│   │   └── profiles/                      # Profile images
│   └── 📂 audio/                          # Generated audio (auto-created)
│       └── tts/                           # TTS audio files
│
├── 📂 docs/                               # Documentation
│   ├── 📂 images/                         # Screenshot images
│   │   ├── 01-login-page.png
│   │   ├── 02-summarization.png
│   │   ├── ... (16 images total)
│   │   └── 16-premium-upgrade.png
│   └── API.md                             # API documentation
│
└── 📂 utils/                              # Utility modules
    ├── auth.py                            # Authentication helpers
    ├── ai_processors.py                   # AI processing functions
    └── validators.py                      # Input validators
```

---

## 🚀 Installation & Setup

### Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.7+** ([Download](https://www.python.org/downloads/))
- **pip** (Python package manager)
- **Git** (optional, for cloning)

### Step 1: Clone or Download the Repository

```bash
# Option 1: Clone with Git
git clone https://github.com/yourusername/ai-hub.git
cd ai-hub

# Option 2: Download ZIP and extract
# Then navigate to the extracted folder
cd ai-hub-main
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
```
Flask==2.3.0
Werkzeug==2.3.0
Pillow==10.0.0
sumy==0.11.0
nltk==3.8.1
gTTS==2.3.2
SpeechRecognition==3.10.0
pytesseract==0.3.10
pydub==0.25.1
email-validator==2.0.0
```

### Step 4: Install Tesseract OCR (for OCR feature)

**Windows:**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install and add to PATH

**macOS:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

### Step 5: Download NLTK Data (for Summarization)

```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### Step 6: Create Required Directories

```bash
mkdir -p static/uploads static/audio docs/images
```

### Step 7: Configure Application

Edit `app.py` and update:
```python
# Change this in production!
app.secret_key = 'your-super-secret-key-change-in-production'

# Optional: Configure upload settings
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
```

### Step 8: Run the Application

```bash
python app.py
```

**Success!** The application should now be running at:
```
🌐 http://127.0.0.1:5000/
```

### Step 9: Create First Account

1. Navigate to `http://127.0.0.1:5000/`
2. Click "Get Started" or "Register"
3. Fill in your details
4. Start using AI Hub!

---

## 📱 Usage Guide

### 1️⃣ Registration & Login

**Register a New Account:**
1. Click "Get Started" or "Register"
2. Fill in the registration form:
   - Full Name
   - Email Address
   - Password (min. 8 characters)
   - User Role (Free/Paid)
   - Profile Picture (optional)
3. Click "Create Account"
4. Login with your credentials

**Login:**
1. Enter your email and password
2. Click "Sign In"
3. You'll be redirected to the dashboard

---

### 2️⃣ Text Summarization

**Steps:**
1. Navigate to **Dashboard → Summarize** or use navbar
2. Paste your long text in the input area
3. (Optional) Adjust summary length
4. Click **"Generate Summary"**
5. View the condensed summary
6. Click **"Copy Summary"** to copy to clipboard

**Tips:**
- Works best with articles, reports, and documents
- Minimum 3 sentences required
- Longer texts produce better summaries

---

### 3️⃣ Text-to-Speech

**Steps:**
1. Go to **Dashboard → Text to Speech**
2. Enter or paste your text
3. Select a voice option:
   - **Free Users**: 2 standard voices
   - **Paid Users**: 6 premium voices
4. Click **"Convert to Audio"**
5. Listen to preview or download MP3 file

**Voice Options:**
- English (US) - Male/Female
- English (UK) - Male/Female
- English (AU) - Male/Female (Premium)
- English (IN) - Male/Female (Premium)

---

### 4️⃣ Speech-to-Text

**Steps:**
1. Navigate to **Dashboard → Speech to Text**
2. Click **"Choose File"** and select audio file
3. Supported formats: MP3, WAV, M4A, FLAC
4. Click **"Convert to Text"**
5. Wait for processing (depends on file size)
6. View transcribed text
7. Edit, copy, or download as needed

**Best Practices:**
- Use clear audio with minimal background noise
- Ensure proper microphone quality
- Avoid overlapping speakers

---

### 5️⃣ Optical Character Recognition

**Steps:**
1. Go to **Dashboard → OCR**
2. Upload an image (JPG, PNG, PDF)
3. Click **"Extract Text"**
4. View extracted text
5. Edit or copy the results

**Tips:**
- Use high-quality, clear images
- Ensure good lighting and contrast
- Works best with printed text
- Avoid handwritten notes for better accuracy

---

### 6️⃣ Profile Management

**View Profile:**
1. Click your name in the navbar
2. Select "Profile"
3. View account information and statistics

**Edit Profile:**
1. Go to Profile page
2. Click **"Edit Profile"**
3. Update name, email, or password
4. Click **"Save Changes"**

**Change Profile Picture:**
1. Click camera icon on avatar
2. Upload new image
3. Image auto-saves

---

## 🗄️ Database Schema

### Users Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'Free User',
    profile_image TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Fields:**
- `id`: Unique user identifier
- `name`: User's full name
- `email`: Unique email address
- `password`: Hashed password (Werkzeug)
- `role`: Account type (Free User / Paid User)
- `profile_image`: Filename of profile picture
- `created_at`: Account creation timestamp
- `updated_at`: Last modification timestamp

---

## 🔗 API Endpoints

### Authentication Routes

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Landing page | No |
| GET/POST | `/register` | User registration | No |
| GET/POST | `/login` | User login | No |
| GET | `/logout` | User logout | Yes |
| GET/POST | `/forgot-password` | Password recovery | No |
| GET/POST | `/reset-password/<token>` | Reset password | No |

### Feature Routes

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/dashboard` | User dashboard | Yes |
| GET | `/profile` | User profile | Yes |
| POST | `/update-profile` | Update profile | Yes |
| GET/POST | `/summarize` | Text summarization | Yes |
| GET/POST | `/tts` | Text-to-speech | Yes |
| GET/POST | `/stt` | Speech-to-text | Yes |
| GET/POST | `/ocr` | OCR processing | Yes |

---

## 🎨 Customization

### Change Color Scheme

Edit `static/css/style.css`:

```css
:root {
    /* Primary Colors */
    --primary-yellow: #FFC107;
    --primary-orange: #FF9800;
    
    /* Background Colors */
    --dark-bg: #0a0a0a;
    --card-bg: #1a1a1a;
    --section-bg: #141414;
    
    /* Text Colors */
    --text-primary: #f0f0f0;
    --text-secondary: #aaa;
    --text-muted: #666;
}
```

### Modify Application Settings

In `app.py`:

```python
# Application Configuration
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['AUDIO_FOLDER'] = 'static/audio'

# Session Configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
```

### Add New AI Models

Replace placeholder functions in `app.py`:

```python
# Example: Integrate OpenAI GPT for better summarization
from openai import OpenAI

@app.route('/summarize', methods=['POST'])
def summarize_text():
    text = request.form['text']
    
    # Use OpenAI API
    client = OpenAI(api_key='your-api-key')
    response = client.completions.create(
        model="gpt-3.5-turbo",
        prompt=f"Summarize this text: {text}",
        max_tokens=150
    )
    
    summary = response.choices[0].text
    return jsonify({'summary': summary})
```

---

## 🔐 Security Features

### Implemented Security Measures

1. **Password Hashing**
   - Werkzeug's `generate_password_hash()`
   - SHA-256 encryption
   - Salt generation for each password

2. **Session Management**
   - Secure cookie-based sessions
   - Session timeout after inactivity
   - CSRF protection

3. **Input Validation**
   - Email format validation
   - Password strength requirements
   - File type verification
   - SQL injection prevention

4. **File Upload Security**
   - Allowed file extensions whitelist
   - File size limitations (16MB)
   - Secure filename generation
   - Path traversal prevention

5. **Authentication Guards**
   - Login required decorators
   - Role-based access control
   - Session verification

### Security Best Practices

**For Production Deployment:**

```python
# Generate secure secret key
import secrets
app.secret_key = secrets.token_hex(32)

# Enable HTTPS only
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Add security headers
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

---

## 🐛 Troubleshooting

### Common Issues & Solutions

#### 1. Database Error

**Error:** `sqlite3.OperationalError: unable to open database file`

**Solution:**
```bash
# Delete existing database and restart
rm database.db
python app.py
```

#### 2. Import Errors

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

#### 3. Upload Folder Not Found

**Error:** `FileNotFoundError: [Errno 2] No such file or directory: 'static/uploads'`

**Solution:**
```bash
# Create required directories
mkdir -p static/uploads static/audio
```

#### 4. Template Not Found

**Error:** `jinja2.exceptions.TemplateNotFound: index.html`

**Solution:**
```bash
# Ensure templates are in correct folder
ls templates/
# Should show all HTML files
```

#### 5. Tesseract Not Found (OCR Error)

**Error:** `TesseractNotFoundError`

**Solution:**
```bash
# Install Tesseract OCR
# Windows: Download from GitHub
# macOS: brew install tesseract
# Linux: sudo apt-get install tesseract-ocr

# Then set path in app.py
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

#### 6. Audio Conversion Error (STT)

**Error:** `FileNotFoundError: [WinError 2] The system cannot find the file specified`

**Solution:**
```bash
# Install FFmpeg
# Windows: Download from ffmpeg.org
# macOS: brew install ffmpeg
# Linux: sudo apt-get install ffmpeg
```

#### 7. NLTK Data Not Found

**Error:** `LookupError: Resource punkt not found`

**Solution:**
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

---

## 🚀 Future Enhancements

### Planned Features

#### Short-term (Q2 2026)
- [ ] Email verification system (SMTP integration)
- [ ] Real-time collaboration on documents
- [ ] Export summaries as PDF/DOCX
- [ ] Advanced voice customization (pitch, speed)
- [ ] Multi-language support for all features
- [ ] Dark/Light theme toggle
- [ ] Mobile app (React Native)

#### Mid-term (Q3-Q4 2026)
- [ ] Payment gateway integration (Stripe/PayPal)
- [ ] API access for developers
- [ ] Batch processing for multiple files
- [ ] Cloud storage integration (Google Drive, Dropbox)
- [ ] Advanced analytics dashboard
- [ ] Team collaboration features
- [ ] Custom AI model training

#### Long-term (2027)
- [ ] AI chatbot assistant
- [ ] Video-to-text transcription
- [ ] Real-time translation
- [ ] Voice cloning technology
- [ ] Advanced OCR with handwriting recognition
- [ ] Browser extension
- [ ] Desktop application (Electron)

### Suggested Improvements

**AI Models:**
- Integrate OpenAI GPT-4 for summarization
- Use ElevenLabs for premium TTS voices
- Implement Whisper AI for better STT accuracy
- Add Google Vision API for enhanced OCR

**UI/UX:**
- Add drag-and-drop file uploads
- Implement progressive web app (PWA)
- Add keyboard shortcuts
- Create onboarding tutorial
- Add tooltips and help guides

**Performance:**
- Implement Redis caching
- Add background job processing (Celery)
- Optimize database queries
- Add CDN for static assets
- Implement lazy loading

---

## 👥 Contributing

We welcome contributions from the community! Here's how you can help:

### How to Contribute

1. **Fork the Repository**
   ```bash
   git clone https://github.com/yourusername/ai-hub.git
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```

3. **Make Your Changes**
   - Write clean, commented code
   - Follow existing code style
   - Test your changes thoroughly

4. **Commit Your Changes**
   ```bash
   git commit -m "Add some AmazingFeature"
   ```

5. **Push to Branch**
   ```bash
   git push origin feature/AmazingFeature
   ```

6. **Open a Pull Request**
   - Describe your changes
   - Reference any related issues
   - Wait for review

### Contribution Guidelines

- Follow PEP 8 style guide for Python
- Write meaningful commit messages
- Add comments for complex logic
- Update documentation as needed
- Test before submitting PR

### Code of Conduct

- Be respectful and inclusive
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Rutika Pardhi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

### Special Thanks

- **Savitribai Phule Pune University** - Academic guidance and support
- **Flask Community** - Excellent framework and documentation
- **Open Source Contributors** - For amazing libraries and tools
- **Beta Testers** - For valuable feedback and bug reports

### Technologies & Libraries

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Bootstrap](https://getbootstrap.com/) - UI components
- [Font Awesome](https://fontawesome.com/) - Icons
- [gTTS](https://pypi.org/project/gTTS/) - Text-to-speech
- [Pytesseract](https://github.com/madmaze/pytesseract) - OCR engine
- [Sumy](https://github.com/miso-belica/sumy) - Text summarization
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) - Audio processing

### Inspiration

This project was inspired by the need for accessible AI tools for students and researchers, combining multiple AI capabilities into a single, user-friendly platform.

---

## 📞 Contact & Support

### Developer Information

**Rutika Pardhi**
- 🎓 Student at Savitribai Phule Pune University
- 📧 Email: rutika.pardhi@example.com
- 💼 LinkedIn: [Rutika Pardhi](https://linkedin.com/in/rutikapardhi)
- 🐱 GitHub: [@rutikapardhi](https://github.com/rutikapardhi)

### Project Links

- **Repository**: https://github.com/rutikapardhi/ai-hub
- **Issues**: https://github.com/rutikapardhi/ai-hub/issues
- **Documentation**: https://github.com/rutikapardhi/ai-hub/wiki
- **Changelog**: https://github.com/rutikapardhi/ai-hub/releases

### Get Help

- 📖 Check the [Documentation](https://github.com/rutikapardhi/ai-hub/wiki)
- 🐛 Report bugs via [GitHub Issues](https://github.com/rutikapardhi/ai-hub/issues)
- 💬 Join our [Discord Community](https://discord.gg/aihub)
- 📧 Email: support@aihub.edu

---

## 🌟 Star History

If you find this project helpful, please consider giving it a ⭐ on GitHub!

[![Star History Chart](https://api.star-history.com/svg?repos=rutikapardhi/ai-hub&type=Date)](https://star-history.com/#rutikapardhi/ai-hub&Date)

---

<div align="center">

### Made with ❤️ by Rushikesh Narawade

**AI Hub** - Transforming Content, Empowering Innovation

© 2026 AI-Powered Content Transformation Hub | All Rights Reserved

[⬆ Back to Top](#-ai-powered-content-transformation-hub)

</div>
