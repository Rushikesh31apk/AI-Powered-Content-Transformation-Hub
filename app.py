# ─────────────────────────────────────────────
# COMPLETE INSTALLATION GUIDE
# ─────────────────────────────────────────────
# Run these commands ONCE in your terminal:
#
#   pip install flask werkzeug sumy nltk gtts speechrecognition pydub pytesseract pillow flask-mail
#   python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
#
# IMPORTANT: Also install these external tools:
#   
#   1. FFmpeg (for audio processing):
#      Windows: Download from https://ffmpeg.org/download.html
#      Mac: brew install ffmpeg
#      Linux: sudo apt-get install ffmpeg
#
#   2. Tesseract OCR (for text extraction from images):
#      Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
#      Mac: brew install tesseract
#      Linux: sudo apt-get install tesseract-ocr
#
# Then run your app:
#   python app.py
# ─────────────────────────────────────────────

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
import sqlite3
from datetime import datetime, timedelta
import os
import hashlib
import random
import string

# ─── Summarization imports ───
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# ─── Text-to-Speech imports ───
from gtts import gTTS

# ─── Speech-to-Text imports ───
import speech_recognition as sr
from pydub import AudioSegment

# ─── OCR imports ───
import pytesseract
from PIL import Image

# Update this path for Windows users
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# ═══════════════════════════════════════════════
# EMAIL CONFIGURATION
# ═══════════════════════════════════════════════
# IMPORTANT: Update these with your email credentials
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'narawaderushikesh18@gmail.com'  # ← CHANGE THIS
app.config['MAIL_PASSWORD'] = 'nkziakqypimfhlzo'      # ← CHANGE THIS (use App Password for Gmail)
app.config['MAIL_DEFAULT_SENDER'] = 'narawaderushikesh18@gmail.com'  # ← CHANGE THIS

mail = Mail(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static/audio', exist_ok=True)

# ─────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'Free User',
            profile_image TEXT,
            is_verified INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # OTP table for verification and password reset
    c.execute('''
        CREATE TABLE IF NOT EXISTS otps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            otp TEXT NOT NULL,
            purpose TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            is_used INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# ─────────────────────────────────────────────
# OTP HELPER FUNCTIONS
# ─────────────────────────────────────────────
def generate_otp(length=6):
    """Generate a random OTP"""
    return ''.join(random.choices(string.digits, k=length))


def send_otp_email(email, otp, purpose):
    """Send OTP via email with HTML template"""
    try:
        if purpose == 'verification':
            subject = '🔐 Email Verification - AI Hub'
            
            # Read HTML template
            with open('email_verification_template.html', 'r', encoding='utf-8') as f:
                html_template = f.read()
            
            # Replace placeholder with actual OTP
            html_body = html_template.replace('{{OTP}}', otp)
            
            # Plain text fallback
            text_body = f'''
AI Hub - Email Verification

Thank you for registering with AI Hub!

Your verification code is: {otp}

This code will expire in 10 minutes.

If you didn't create an account, please ignore this email.

Best regards,
AI Hub Team
            '''
            
        elif purpose == 'password_reset':
            subject = '🔑 Password Reset - AI Hub'
            
            # Read HTML template
            with open('password_reset_template.html', 'r', encoding='utf-8') as f:
                html_template = f.read()
            
            # Replace placeholder with actual OTP
            html_body = html_template.replace('{{OTP}}', otp)
            
            # Plain text fallback
            text_body = f'''
AI Hub - Password Reset Request

You requested to reset your password for AI Hub.

Your password reset code is: {otp}

This code will expire in 10 minutes.

If you didn't request this, please ignore this email.

Best regards,
AI Hub Team
            '''
        else:
            return False
        
        msg = Message(subject, recipients=[email])
        msg.body = text_body
        msg.html = html_body
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False


def save_otp(email, otp, purpose):
    """Save OTP to database"""
    conn = get_db()
    expires_at = datetime.now() + timedelta(minutes=10)
    conn.execute(
        'INSERT INTO otps (email, otp, purpose, expires_at) VALUES (?, ?, ?, ?)',
        (email, otp, purpose, expires_at)
    )
    conn.commit()
    conn.close()


def verify_otp(email, otp, purpose):
    """Verify OTP"""
    conn = get_db()
    otp_record = conn.execute(
        '''SELECT * FROM otps 
           WHERE email = ? AND otp = ? AND purpose = ? AND is_used = 0 
           AND expires_at > ? 
           ORDER BY created_at DESC LIMIT 1''',
        (email, otp, purpose, datetime.now())
    ).fetchone()
    
    if otp_record:
        # Mark OTP as used
        conn.execute('UPDATE otps SET is_used = 1 WHERE id = ?', (otp_record['id'],))
        conn.commit()
        conn.close()
        return True
    
    conn.close()
    return False


def cleanup_expired_otps():
    """Clean up expired OTPs (run periodically)"""
    conn = get_db()
    conn.execute('DELETE FROM otps WHERE expires_at < ?', (datetime.now(),))
    conn.commit()
    conn.close()


# ─────────────────────────────────────────────
# SUMMARIZATION HELPER
# ─────────────────────────────────────────────
def generate_summary(text, num_sentences=None, method='lsa'):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    corpus = parser.document
    total_sentences = len(corpus.sentences)

    if total_sentences <= 3:
        return text.strip()

    if num_sentences is None:
        if total_sentences <= 5:
            num_sentences = 2
        elif total_sentences <= 10:
            num_sentences = 3
        elif total_sentences <= 20:
            num_sentences = 4
        else:
            num_sentences = max(3, total_sentences // 4)

    summarizers = {
        'lsa':       LsaSummarizer(),
        'textrank':  TextRankSummarizer(),
        'lexrank':   LexRankSummarizer(),
    }
    summarizer = summarizers.get(method, LsaSummarizer())

    summary_sentences = summarizer(corpus, num_sentences)
    summary = ' '.join(str(s) for s in summary_sentences)
    return summary if summary.strip() else text.strip()


# ─────────────────────────────────────────────
# TTS CLEANUP HELPER
# ─────────────────────────────────────────────
def cleanup_old_audio_files(keep_count=20):
    try:
        audio_dir = 'static/audio'
        if not os.path.exists(audio_dir):
            return
        
        files = []
        for filename in os.listdir(audio_dir):
            if filename.startswith('tts_') and filename.endswith('.mp3'):
                filepath = os.path.join(audio_dir, filename)
                files.append((filepath, os.path.getmtime(filepath)))
        
        files.sort(key=lambda x: x[1], reverse=True)
        
        for filepath, _ in files[keep_count:]:
            try:
                os.remove(filepath)
            except:
                pass
    except Exception as e:
        print(f"Cleanup error: {e}")


# ─────────────────────────────────────────────
# STT HELPER - Convert audio to WAV format
# ─────────────────────────────────────────────
def convert_to_wav(input_path):
    """Convert any audio format to WAV for speech recognition"""
    try:
        audio = AudioSegment.from_file(input_path)
        wav_path = input_path.rsplit('.', 1)[0] + '.wav'
        audio.export(wav_path, format='wav')
        return wav_path
    except Exception as e:
        print(f"Audio conversion error: {e}")
        return None


# ─────────────────────────────────────────────
# OCR HELPER - Extract text from image
# ─────────────────────────────────────────────
def extract_text_from_image(image_path):
    """Extract text from image using Tesseract OCR"""
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='eng')
        text = text.strip()
        
        if not text:
            return "No text found in the image. Please try with a clearer image containing text."
        
        return text
        
    except pytesseract.TesseractNotFoundError:
        return "ERROR: Tesseract is not installed or not found in PATH. Please install Tesseract OCR."
    except Exception as e:
        print(f"OCR Error: {e}")
        return f"ERROR: Could not process image: {str(e)}"


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')


# ─────────────────────────────────────────────
# AUTHENTICATION ROUTES
# ─────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name     = request.form['name']
        email    = request.form['email']
        password = request.form['password']
        role     = request.form.get('role', 'Free User')

        profile_image = None
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                ts = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f"{ts}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                profile_image = filename

        hashed = generate_password_hash(password)
        try:
            conn = get_db()
            conn.execute(
                'INSERT INTO users (name, email, password, role, profile_image, is_verified) VALUES (?, ?, ?, ?, ?, ?)',
                (name, email, hashed, role, profile_image, 0)
            )
            conn.commit()
            conn.close()
            
            # Generate and send OTP
            otp = generate_otp()
            save_otp(email, otp, 'verification')
            
            if send_otp_email(email, otp, 'verification'):
                session['pending_verification_email'] = email
                flash('Registration successful! Please check your email for verification code.', 'success')
                return redirect(url_for('verify_email'))
            else:
                flash('Registration successful but email sending failed. Please contact support.', 'warning')
                return redirect(url_for('login'))
                
        except sqlite3.IntegrityError:
            flash('Email already exists!', 'error')

    return render_template('register.html')


@app.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    if 'pending_verification_email' not in session:
        flash('No pending verification found.', 'error')
        return redirect(url_for('register'))
    
    email = session['pending_verification_email']
    
    if request.method == 'POST':
        otp = request.form.get('otp', '').strip()
        
        if verify_otp(email, otp, 'verification'):
            # Mark user as verified
            conn = get_db()
            conn.execute('UPDATE users SET is_verified = 1 WHERE email = ?', (email,))
            conn.commit()
            conn.close()
            
            session.pop('pending_verification_email', None)
            flash('Email verified successfully! You can now login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Invalid or expired OTP. Please try again.', 'error')
    
    return render_template('verify_email.html', email=email)


@app.route('/resend-otp')
def resend_otp():
    if 'pending_verification_email' not in session:
        flash('No pending verification found.', 'error')
        return redirect(url_for('register'))
    
    email = session['pending_verification_email']
    otp = generate_otp()
    save_otp(email, otp, 'verification')
    
    if send_otp_email(email, otp, 'verification'):
        flash('New OTP sent to your email!', 'success')
    else:
        flash('Failed to send OTP. Please try again.', 'error')
    
    return redirect(url_for('verify_email'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']

        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            # Check if is_verified column exists and user is verified
            try:
                is_verified = user['is_verified']
            except (KeyError, IndexError):
                # Column doesn't exist, treat as verified (for backward compatibility)
                is_verified = 1
            
            if is_verified == 0:
                flash('Please verify your email before logging in.', 'error')
                session['pending_verification_email'] = email
                return redirect(url_for('verify_email'))
            
            session['user_id']       = user['id']
            session['user_name']     = user['name']
            session['user_email']    = user['email']
            session['user_role']     = user['role']
            try:
                session['profile_image'] = user['profile_image']
            except (KeyError, IndexError):
                session['profile_image'] = None
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'error')

    return render_template('login.html')


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user:
            # Generate and send OTP
            otp = generate_otp()
            save_otp(email, otp, 'password_reset')
            
            if send_otp_email(email, otp, 'password_reset'):
                session['reset_password_email'] = email
                flash('Password reset code sent to your email!', 'success')
                return redirect(url_for('reset_password'))
            else:
                flash('Failed to send reset code. Please try again.', 'error')
        else:
            # Don't reveal if email exists or not for security
            flash('If the email exists, a reset code has been sent.', 'info')
    
    return render_template('forgot_password.html')


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if 'reset_password_email' not in session:
        flash('Please request a password reset first.', 'error')
        return redirect(url_for('forgot_password'))
    
    email = session['reset_password_email']
    
    if request.method == 'POST':
        otp = request.form.get('otp', '').strip()
        new_password = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        if new_password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('reset_password.html', email=email)
        
        if len(new_password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
            return render_template('reset_password.html', email=email)
        
        if verify_otp(email, otp, 'password_reset'):
            # Update password
            hashed = generate_password_hash(new_password)
            conn = get_db()
            conn.execute('UPDATE users SET password = ? WHERE email = ?', (hashed, email))
            conn.commit()
            conn.close()
            
            session.pop('reset_password_email', None)
            flash('Password reset successful! You can now login with your new password.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Invalid or expired OTP. Please try again.', 'error')
    
    return render_template('reset_password.html', email=email)


@app.route('/resend-reset-otp')
def resend_reset_otp():
    if 'reset_password_email' not in session:
        flash('Please request a password reset first.', 'error')
        return redirect(url_for('forgot_password'))
    
    email = session['reset_password_email']
    otp = generate_otp()
    save_otp(email, otp, 'password_reset')
    
    if send_otp_email(email, otp, 'password_reset'):
        flash('New reset code sent to your email!', 'success')
    else:
        flash('Failed to send reset code. Please try again.', 'error')
    
    return redirect(url_for('reset_password'))


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))


# ─────────────────────────────────────────────
# DASHBOARD & FEATURES
# ─────────────────────────────────────────────
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')


@app.route('/summarize', methods=['GET', 'POST'])
def summarize():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    summary       = None
    original_text = None

    if request.method == 'POST':
        original_text = request.form.get('text', '').strip()

        if original_text:
            word_count = len(original_text.split())
            if word_count < 80:
                method = 'textrank'
            elif word_count < 300:
                method = 'lsa'
            else:
                method = 'lexrank'

            summary = generate_summary(original_text, method=method)

    return render_template('summarize.html',
                           summary=summary,
                           original_text=original_text)


@app.route('/tts', methods=['GET', 'POST'])
def tts():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    audio_file = None
    input_text = None
    voice_name = None
    
    if request.method == 'POST':
        input_text = request.form.get('text', '').strip()
        voice = request.form.get('voice', 'en')
        
        if input_text:
            if len(input_text) > 5000:
                flash('Text too long! Maximum 5000 characters.', 'error')
                return render_template('tts.html', 
                                     input_text=input_text,
                                     audio_file=None,
                                     voice_name=None)
            
            voice_map = {
                'en':    {'lang': 'en', 'tld': 'com',   'name': 'English (US) - Female'},
                'en-uk': {'lang': 'en', 'tld': 'co.uk', 'name': 'English (UK) - Male'},
                'en-au': {'lang': 'en', 'tld': 'com.au','name': 'English (AU) - Female'},
                'en-in': {'lang': 'en', 'tld': 'co.in', 'name': 'English (IN) - Female'},
            }
            
            if voice != 'en' and session.get('user_role') != 'Paid User':
                flash('Premium voices require a Paid account!', 'error')
                voice = 'en'
            
            voice_config = voice_map.get(voice, voice_map['en'])
            voice_name = voice_config['name']
            
            try:
                text_hash = hashlib.md5(input_text.encode()).hexdigest()[:12]
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f"tts_{timestamp}_{text_hash}.mp3"
                filepath = os.path.join('static/audio', filename)
                
                tts_obj = gTTS(text=input_text, 
                              lang=voice_config['lang'], 
                              tld=voice_config['tld'],
                              slow=False)
                
                tts_obj.save(filepath)
                audio_file = filename
                
                cleanup_old_audio_files()
                
            except Exception as e:
                flash(f'Error generating audio: {str(e)}', 'error')
                print(f"TTS Error: {e}")
    
    return render_template('tts.html', 
                         audio_file=audio_file,
                         input_text=input_text,
                         voice_name=voice_name)


@app.route('/stt', methods=['GET', 'POST'])
def stt():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    extracted_text = None
    
    if request.method == 'POST' and 'audio_file' in request.files:
        file = request.files['audio_file']
        
        if file and file.filename:
            try:
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f"stt_{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                wav_path = filepath
                if not filepath.lower().endswith('.wav'):
                    wav_path = convert_to_wav(filepath)
                    if not wav_path:
                        flash('Error converting audio file. Please try a different format.', 'error')
                        return render_template('stt.html', extracted_text=None)
                
                recognizer = sr.Recognizer()
                
                with sr.AudioFile(wav_path) as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio_data = recognizer.record(source)
                    extracted_text = recognizer.recognize_google(audio_data)
                
                try:
                    os.remove(filepath)
                    if wav_path != filepath:
                        os.remove(wav_path)
                except:
                    pass
                
            except sr.UnknownValueError:
                flash('Could not understand audio. Please try with clearer speech.', 'error')
            except sr.RequestError as e:
                flash(f'Speech recognition service error: {str(e)}', 'error')
            except Exception as e:
                flash(f'Error processing audio: {str(e)}', 'error')
                print(f"STT Error: {e}")
    
    return render_template('stt.html', extracted_text=extracted_text)


@app.route('/ocr', methods=['GET', 'POST'])
def ocr():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    extracted_text = None
    
    if request.method == 'POST' and 'image_file' in request.files:
        file = request.files['image_file']
        
        if file and file.filename:
            try:
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f"ocr_{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                extracted_text = extract_text_from_image(filepath)
                
                try:
                    os.remove(filepath)
                except:
                    pass
                
            except Exception as e:
                flash(f'Error processing image: {str(e)}', 'error')
                print(f"OCR Error: {e}")
    
    return render_template('ocr.html', extracted_text=extracted_text)


@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    return render_template('profile.html', user=user)


@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    new_password = request.form.get('new_password', '').strip()
    
    if not name or not email:
        flash('Name and email are required!', 'error')
        return redirect(url_for('profile'))
    
    try:
        conn = get_db()
        
        existing = conn.execute(
            'SELECT id FROM users WHERE email = ? AND id != ?', 
            (email, session['user_id'])
        ).fetchone()
        
        if existing:
            flash('Email already in use by another account!', 'error')
            conn.close()
            return redirect(url_for('profile'))
        
        if new_password:
            hashed = generate_password_hash(new_password)
            conn.execute(
                'UPDATE users SET name = ?, email = ?, password = ? WHERE id = ?',
                (name, email, hashed, session['user_id'])
            )
        else:
            conn.execute(
                'UPDATE users SET name = ?, email = ? WHERE id = ?',
                (name, email, session['user_id'])
            )
        
        conn.commit()
        conn.close()
        
        session['user_name'] = name
        session['user_email'] = email
        
        flash('Profile updated successfully!', 'success')
        
    except Exception as e:
        flash(f'Error updating profile: {str(e)}', 'error')
        print(f"Profile update error: {e}")
    
    return redirect(url_for('profile'))


# ─────────────────────────────────────────────
# PERIODIC CLEANUP
# ─────────────────────────────────────────────
@app.before_request
def before_request():
    """Clean up expired OTPs before each request"""
    if random.random() < 0.01:  # 1% chance to run cleanup
        cleanup_expired_otps()


# ─────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)