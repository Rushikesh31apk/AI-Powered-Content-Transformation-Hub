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

app = Flask(__name__)
# Explicitly use 0.0.0.0 for all environments
app.config['SERVER_NAME'] = None # Ensure no host filtering
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'static/uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# ═══════════════════════════════════════════════
# EMAIL CONFIGURATION
# ═══════════════════════════════════════════════
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'narawaderushikesh18@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'nkziakqypimfhlzo')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'])

mail = Mail(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static/audio', exist_ok=True)

# ─────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────
def init_db():
    db_path = os.environ.get('DATABASE_URL', 'database.db')
    if db_path.startswith('sqlite:///'):
        db_path = db_path.replace('sqlite:///', '')
    
    conn = sqlite3.connect(db_path)
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
    db_path = os.environ.get('DATABASE_URL', 'database.db')
    if db_path.startswith('sqlite:///'):
        db_path = db_path.replace('sqlite:///', '')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/health')
def health():
    return "ok", 200

# Original logic follows...

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(email, otp, purpose):
    try:
        msg = Message('AI Hub', recipients=[email])
        msg.body = f'Your code: {otp}'
        mail.send(msg)
        return True
    except: return False

def save_otp(email, otp, purpose):
    conn = get_db()
    conn.execute('INSERT INTO otps (email, otp, purpose, expires_at) VALUES (?, ?, ?, ?)',
                (email, otp, purpose, datetime.now() + timedelta(minutes=10)))
    conn.commit(); conn.close()

def verify_otp(email, otp, purpose):
    conn = get_db()
    otp_record = conn.execute('SELECT * FROM otps WHERE email=? AND otp=? AND purpose=? AND is_used=0 AND expires_at>?',
                             (email, otp, purpose, datetime.now())).fetchone()
    if otp_record:
        conn.execute('UPDATE otps SET is_used=1 WHERE id=?', (otp_record['id'],))
        conn.commit(); conn.close(); return True
    conn.close(); return False

def cleanup_expired_otps():
    conn = get_db(); conn.execute('DELETE FROM otps WHERE expires_at < ?', (datetime.now(),)); conn.commit(); conn.close()

def generate_summary(text, num_sentences=None, method='lsa'):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    corpus = parser.document
    if len(corpus.sentences) <= 3: return text
    summarizers = {'lsa': LsaSummarizer(), 'textrank': TextRankSummarizer(), 'lexrank': LexRankSummarizer()}
    summarizer = summarizers.get(method, LsaSummarizer())
    return ' '.join(str(s) for s in summarizer(corpus, num_sentences or 3))

def cleanup_old_audio_files(keep_count=20):
    try:
        files = [(f'static/audio/{f}', os.path.getmtime(f'static/audio/{f}')) for f in os.listdir('static/audio') if f.endswith('.mp3')]
        files.sort(key=lambda x: x[1], reverse=True)
        for f, _ in files[keep_count:]: os.remove(f)
    except: pass

def convert_to_wav(p):
    try:
        w = p.rsplit('.', 1)[0] + '.wav'
        AudioSegment.from_file(p).export(w, format='wav')
        return w
    except: return None

def extract_text_from_image(p):
    try: return pytesseract.image_to_string(Image.open(p)).strip() or "No text"
    except: return "Error"

@app.route('/')
def index():
    if 'user_id' in session: return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed = generate_password_hash(request.form['password'])
        try:
            conn = get_db()
            conn.execute('INSERT INTO users (name, email, password, role, profile_image, is_verified) VALUES (?, ?, ?, ?, ?, 0)',
                        (request.form['name'], request.form['email'], hashed, request.form.get('role', 'Free'), None))
            conn.commit(); conn.close()
            otp = generate_otp(); save_otp(request.form['email'], otp, 'verification')
            send_otp_email(request.form['email'], otp, 'verification')
            session['pending_verification_email'] = request.form['email']
            return redirect(url_for('verify_email'))
        except: flash('Error')
    return render_template('register.html')

@app.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    if 'pending_verification_email' not in session: return redirect(url_for('register'))
    if request.method == 'POST':
        if verify_otp(session['pending_verification_email'], request.form['otp'], 'verification'):
            conn = get_db(); conn.execute('UPDATE users SET is_verified = 1 WHERE email = ?', (session['pending_verification_email'],))
            conn.commit(); conn.close()
            session.pop('pending_verification_email')
            return redirect(url_for('login'))
    return render_template('verify_email.html', email=session['pending_verification_email'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = get_db(); user = conn.execute('SELECT * FROM users WHERE email = ?', (request.form['email'],)).fetchone(); conn.close()
        if user and check_password_hash(user['password'], request.form['password']):
            if user['is_verified'] == 0:
                session['pending_verification_email'] = user['email']
                return redirect(url_for('verify_email'))
            session.update({'user_id': user['id'], 'user_name': user['name'], 'user_role': user['role']})
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/summarize', methods=['GET', 'POST'])
def summarize():
    if 'user_id' not in session: return redirect(url_for('login'))
    summary = None
    if request.method == 'POST': summary = generate_summary(request.form.get('text', ''))
    return render_template('summarize.html', summary=summary)

@app.route('/tts', methods=['GET', 'POST'])
def tts():
    if 'user_id' not in session: return redirect(url_for('login'))
    audio_file = None
    if request.method == 'POST':
        text = request.form.get('text', '')
        if text:
            f = f"tts_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
            gTTS(text=text).save(f'static/audio/{f}')
            audio_file = f; cleanup_old_audio_files()
    return render_template('tts.html', audio_file=audio_file)

@app.route('/stt', methods=['GET', 'POST'])
def stt():
    if 'user_id' not in session: return redirect(url_for('login'))
    text = None
    if request.method == 'POST' and 'audio_file' in request.files:
        p = f"static/uploads/{secure_filename(request.files['audio_file'].filename)}"
        request.files['audio_file'].save(p)
        w = p if p.endswith('.wav') else convert_to_wav(p)
        if w:
            r = sr.Recognizer()
            with sr.AudioFile(w) as s: text = r.recognize_google(r.record(s))
            os.remove(p); 
            if w != p: os.remove(w)
    return render_template('stt.html', extracted_text=text)

@app.route('/ocr', methods=['GET', 'POST'])
def ocr():
    if 'user_id' not in session: return redirect(url_for('login'))
    text = None
    if request.method == 'POST' and 'image_file' in request.files:
        p = f"static/uploads/{secure_filename(request.files['image_file'].filename)}"
        request.files['image_file'].save(p)
        text = extract_text_from_image(p); os.remove(p)
    return render_template('ocr.html', extracted_text=text)

@app.route('/profile')
def profile():
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = get_db(); user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone(); conn.close()
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout(): session.clear(); return redirect(url_for('login'))

@app.before_request
def before_request():
    if random.random() < 0.01: cleanup_expired_otps()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
