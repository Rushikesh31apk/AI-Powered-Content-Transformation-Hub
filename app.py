# ─────────────────────────────────────────────
# COMPLETE INSTALLATION GUIDE
# ─────────────────────────────────────────────
# Run these commands ONCE in your terminal:
#
#   pip install flask werkzeug sumy nltk gtts speechrecognition pydub pytesseract pillow
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
import sqlite3
from datetime import datetime
import os
import hashlib

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
app.secret_key = 'your-secret-key-change-this-in-production'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static/audio', exist_ok=True)

# ═══════════════════════════════════════════════
# WINDOWS USERS: Update these paths if needed
# ═══════════════════════════════════════════════
# Uncomment and update the path to your Tesseract installation
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# ─────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'Free User',
            profile_image TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
        # Open image with PIL
        img = Image.open(image_path)
        
        # Perform OCR
        text = pytesseract.image_to_string(img, lang='eng')
        
        # Clean up the text
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

# ── Auth ──
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
                'INSERT INTO users (name, email, password, role, profile_image) VALUES (?, ?, ?, ?, ?)',
                (name, email, hashed, role, profile_image)
            )
            conn.commit(); conn.close()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already exists!', 'error')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']

        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id']       = user['id']
            session['user_name']     = user['name']
            session['user_email']    = user['email']
            session['user_role']     = user['role']
            session['profile_image'] = user['profile_image']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))


# ── Pages ──
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')


# ─────────────────────────────────────────────
# SUMMARIZE (fully working)
# ─────────────────────────────────────────────
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


# ─────────────────────────────────────────────
# TEXT TO SPEECH (fully working)
# ─────────────────────────────────────────────
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


# ─────────────────────────────────────────────
# SPEECH TO TEXT (fully working)
# ─────────────────────────────────────────────
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


# ─────────────────────────────────────────────
# OCR (fully working)
# ─────────────────────────────────────────────
@app.route('/ocr', methods=['GET', 'POST'])
def ocr():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    extracted_text = None
    
    if request.method == 'POST' and 'image_file' in request.files:
        file = request.files['image_file']
        
        if file and file.filename:
            try:
                # Save uploaded image
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f"ocr_{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Extract text from image
                extracted_text = extract_text_from_image(filepath)
                
                # Clean up uploaded file
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


# ─────────────────────────────────────────────
# UPDATE PROFILE (fully working)
# ─────────────────────────────────────────────
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
        
        # Check if email is already taken by another user
        existing = conn.execute(
            'SELECT id FROM users WHERE email = ? AND id != ?', 
            (email, session['user_id'])
        ).fetchone()
        
        if existing:
            flash('Email already in use by another account!', 'error')
            conn.close()
            return redirect(url_for('profile'))
        
        # Update profile
        if new_password:
            # Update with new password
            hashed = generate_password_hash(new_password)
            conn.execute(
                'UPDATE users SET name = ?, email = ?, password = ? WHERE id = ?',
                (name, email, hashed, session['user_id'])
            )
        else:
            # Update without changing password
            conn.execute(
                'UPDATE users SET name = ?, email = ? WHERE id = ?',
                (name, email, session['user_id'])
            )
        
        conn.commit()
        conn.close()
        
        # Update session
        session['user_name'] = name
        session['user_email'] = email
        
        flash('Profile updated successfully!', 'success')
        
    except Exception as e:
        flash(f'Error updating profile: {str(e)}', 'error')
        print(f"Profile update error: {e}")
    
    return redirect(url_for('profile'))


# ─────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)

# ─────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'Free User',
            profile_image TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
        # Load audio file
        audio = AudioSegment.from_file(input_path)
        
        # Export as WAV
        wav_path = input_path.rsplit('.', 1)[0] + '.wav'
        audio.export(wav_path, format='wav')
        
        return wav_path
    except Exception as e:
        print(f"Audio conversion error: {e}")
        return None


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

# ── Auth ──
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
                'INSERT INTO users (name, email, password, role, profile_image) VALUES (?, ?, ?, ?, ?)',
                (name, email, hashed, role, profile_image)
            )
            conn.commit(); conn.close()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already exists!', 'error')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']

        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id']       = user['id']
            session['user_name']     = user['name']
            session['user_email']    = user['email']
            session['user_role']     = user['role']
            session['profile_image'] = user['profile_image']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))


# ── Pages ──
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')


# ─────────────────────────────────────────────
# SUMMARIZE (fully working)
# ─────────────────────────────────────────────
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


# ─────────────────────────────────────────────
# TEXT TO SPEECH (fully working)
# ─────────────────────────────────────────────
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


# ─────────────────────────────────────────────
# SPEECH TO TEXT (fully working)
# ─────────────────────────────────────────────
@app.route('/stt', methods=['GET', 'POST'])
def stt():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    extracted_text = None
    
    if request.method == 'POST' and 'audio_file' in request.files:
        file = request.files['audio_file']
        
        if file and file.filename:
            try:
                # Save uploaded file
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f"stt_{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Convert to WAV if needed
                wav_path = filepath
                if not filepath.lower().endswith('.wav'):
                    wav_path = convert_to_wav(filepath)
                    if not wav_path:
                        flash('Error converting audio file. Please try a different format.', 'error')
                        return render_template('stt.html', extracted_text=None)
                
                # Perform speech recognition
                recognizer = sr.Recognizer()
                
                with sr.AudioFile(wav_path) as source:
                    # Adjust for ambient noise
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    
                    # Record audio
                    audio_data = recognizer.record(source)
                    
                    # Recognize speech using Google Speech Recognition
                    extracted_text = recognizer.recognize_google(audio_data)
                
                # Clean up temporary files
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


# ── Other feature stubs ──
@app.route('/ocr', methods=['GET', 'POST'])
def ocr():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    extracted_text = None
    if request.method == 'POST' and 'image_file' in request.files:
        file = request.files['image_file']
        if file and file.filename:
            extracted_text = "This is placeholder OCR output. In production this would use Tesseract or a cloud OCR API."
    return render_template('ocr.html', extracted_text=extracted_text)


@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    return render_template('profile.html', user=user)


# ─────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)