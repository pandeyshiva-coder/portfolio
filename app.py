"""
Portfolio Website - Shiva Pandey
Flask-based multi-page portfolio web application
Developed during Python Development Internship at StaxTech
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import re
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'staxtech_portfolio_2026'

# Path to store contact messages
MESSAGES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'messages.json')


def save_message(name, email, subject, message):
    """Save contact form message to messages.json."""
    # Load existing messages
    messages = []
    if os.path.exists(MESSAGES_FILE):
        try:
            with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
                messages = json.load(f)
        except (json.JSONDecodeError, IOError):
            messages = []

    # Add new message
    messages.append({
        'id': len(messages) + 1,
        'name': name,
        'email': email,
        'subject': subject,
        'message': message,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

    # Save to file
    with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, indent=4, ensure_ascii=False)


# Email Configuration
EMAIL_ADDRESS = 'pandeyshiva1105@gmail.com'
EMAIL_APP_PASSWORD = 'kevjcuflhpeearch'


def send_email_notification(name, email, subject, message):
    """Send email notification when a contact form is submitted."""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        msg['Subject'] = f'Portfolio Contact: {subject}'

        body = f"""🔔 New Message from Portfolio Website!

━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Name:    {name}
📧 Email:   {email}
📋 Subject: {subject}
━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 Message:
{message}

━━━━━━━━━━━━━━━━━━━━━━━━━━
🕐 Received: {datetime.now().strftime('%d %b %Y, %I:%M %p')}
📌 Reply to: {email}
"""

        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f'Email sending failed: {e}')
        return False

# ============================================================
# Portfolio Data - Dynamic Content
# ============================================================

PROFILE = {
    'name': 'Shiva Pandey',
    'title': 'Python Developer',
    'tagline': 'Building scalable web applications with clean, efficient code.',
    'about': (
        'I am a passionate Python Developer and B.Sc. IT student with hands-on experience '
        'in backend development, web framework architecture, and full-stack application design. '
        'I completed a 120-hour Python Development Internship at StaxTech, where I developed '
        'portfolio-based web applications using modern Python frameworks.'
    ),
    'email': 'pandeyshiva1105@gmail.com',
    'github': 'https://github.com/pandeyshiva-coder',
    'location': 'India',
    'education': 'B.Sc. IT',
    'internship_company': 'StaxTech',
    'internship_duration': '27 Dec 2025 – 25 Jan 2026',
    'internship_hours': '120 Hours',
}

SKILLS = {
    'technical': [
        {'name': 'Python', 'level': 90, 'icon': '🐍'},
        {'name': 'Flask / Django', 'level': 80, 'icon': '🌐'},
        {'name': 'HTML & CSS', 'level': 85, 'icon': '🎨'},
        {'name': 'JavaScript', 'level': 70, 'icon': '⚡'},
        {'name': 'SQL & Database', 'level': 75, 'icon': '🗄️'},
        {'name': 'Git & GitHub', 'level': 78, 'icon': '📂'},
        {'name': 'REST APIs', 'level': 72, 'icon': '🔗'},
        {'name': 'Data Structures', 'level': 80, 'icon': '📊'},
    ],
    'professional': [
        {'name': 'Problem Solving', 'level': 88, 'icon': '🧠'},
        {'name': 'Time Management', 'level': 85, 'icon': '⏱️'},
        {'name': 'Debugging', 'level': 82, 'icon': '🔍'},
        {'name': 'Code Documentation', 'level': 78, 'icon': '📝'},
        {'name': 'Team Collaboration', 'level': 80, 'icon': '🤝'},
        {'name': 'Adaptability', 'level': 85, 'icon': '🔄'},
    ]
}

PROJECTS = [
    {
        'id': 1,
        'title': 'Portfolio Website - Core Version',
        'description': (
            'A structured multi-page web application built using Flask with dynamic template '
            'rendering, modular backend architecture, and organized project directory structure.'
        ),
        'tech': ['Python', 'Flask', 'HTML', 'CSS', 'JavaScript'],
        'features': [
            'Structured routing and URL mapping',
            'Dynamic template rendering',
            'Frontend-backend integration',
            'Modular backend architecture',
        ],
        'category': 'Web Development',
        'icon': '🌐',
        'color': '#6C63FF',
    },
    {
        'id': 2,
        'title': 'Portfolio Website - Advanced Version',
        'description': (
            'Enhanced portfolio application with server-side validation, dynamic content '
            'rendering, exception handling, and deployment-ready architecture.'
        ),
        'tech': ['Python', 'Flask', 'Jinja2', 'CSS3', 'JavaScript'],
        'features': [
            'Server-side form handling & validation',
            'Template inheritance',
            'Exception handling for runtime stability',
            'Optimized modular code organization',
        ],
        'category': 'Web Development',
        'icon': '🚀',
        'color': '#FF6584',
    },
    {
        'id': 3,
        'title': 'Hangman Game',
        'description': (
            'Interactive word-guessing game implementing logic building, flow control, '
            'and user interaction through Python programming.'
        ),
        'tech': ['Python', 'Random Module', 'Logic Design'],
        'features': [
            'Word generation with random module',
            'Interactive gameplay loop',
            'Score tracking system',
            'Input validation',
        ],
        'category': 'Game Development',
        'icon': '🎮',
        'color': '#00C9A7',
    },
    {
        'id': 4,
        'title': 'Stock Portfolio Tracker',
        'description': (
            'Data structuring and file handling application for tracking stock portfolios '
            'with persistent storage and analysis capabilities.'
        ),
        'tech': ['Python', 'CSV', 'File I/O', 'Data Structures'],
        'features': [
            'Portfolio data management',
            'File-based persistence',
            'Data analysis and reporting',
            'Structured data handling',
        ],
        'category': 'Data Application',
        'icon': '📈',
        'color': '#FFA726',
    },
    {
        'id': 5,
        'title': 'Task Automation Script',
        'description': (
            'System-level automation tool utilizing os and shutil modules for '
            'file management and automated task execution.'
        ),
        'tech': ['Python', 'os Module', 'shutil', 'Automation'],
        'features': [
            'Automated file operations',
            'Directory management',
            'Batch processing',
            'System-level scripting',
        ],
        'category': 'Automation',
        'icon': '⚙️',
        'color': '#AB47BC',
    },
    {
        'id': 6,
        'title': 'Rule-Based Chatbot',
        'description': (
            'Interactive chatbot system built using conditional logic, pattern matching, '
            'and regular expressions for natural language interaction.'
        ),
        'tech': ['Python', 'Regex', 'NLP Basics', 'Logic Design'],
        'features': [
            'Pattern-based response system',
            'Regular expression matching',
            'Conversation flow management',
            'Extensible rule engine',
        ],
        'category': 'AI / NLP',
        'icon': '🤖',
        'color': '#29B6F6',
    },
]

EXPERIENCE_TIMELINE = [
    {
        'week': 'Week 1',
        'title': 'Core Structure Development',
        'hours': 30,
        'tasks': [
            'Designed overall website layout and navigation',
            'Created backend routing architecture',
            'Implemented dynamic HTML templates',
            'Integrated CSS and JavaScript for UI',
        ],
    },
    {
        'week': 'Week 2',
        'title': 'Dynamic Enhancement',
        'hours': 30,
        'tasks': [
            'Dynamic project rendering',
            'Contact form processing & validation',
            'Template inheritance implementation',
            'Server-side input validation',
        ],
    },
    {
        'week': 'Week 3',
        'title': 'Performance Optimization',
        'hours': 30,
        'tasks': [
            'Code refactoring and optimization',
            'Strengthening exception handling',
            'Cross-page navigation testing',
            'Deployment configuration setup',
        ],
    },
    {
        'week': 'Week 4',
        'title': 'Finalization & Deployment',
        'hours': 30,
        'tasks': [
            'Backend logic refactoring for modularity',
            'Template rendering optimization',
            'Structured form validation',
            'Final testing and debugging',
        ],
    },
]

# ============================================================
# Routes
# ============================================================

@app.route('/')
def home():
    """Home page - Hero section with introduction."""
    return render_template('index.html', profile=PROFILE, projects=PROJECTS[:3])


@app.route('/about')
def about():
    """About page - Personal info, education, internship details."""
    return render_template('about.html', profile=PROFILE, timeline=EXPERIENCE_TIMELINE)


@app.route('/skills')
def skills():
    """Skills page - Technical and professional skills showcase."""
    return render_template('skills.html', profile=PROFILE, skills=SKILLS)


@app.route('/projects')
def projects():
    """Projects page - All portfolio projects."""
    return render_template('projects.html', profile=PROFILE, projects=PROJECTS)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page - Form with server-side validation."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        # Server-side validation
        errors = []

        if not name:
            errors.append('Name is required.')
        elif len(name) < 2:
            errors.append('Name must be at least 2 characters.')

        if not email:
            errors.append('Email is required.')
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append('Please enter a valid email address.')

        if not subject:
            errors.append('Subject is required.')

        if not message:
            errors.append('Message is required.')
        elif len(message) < 10:
            errors.append('Message must be at least 10 characters.')

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('contact.html', profile=PROFILE,
                                   form_data={'name': name, 'email': email,
                                              'subject': subject, 'message': message})

        # Save message to JSON file
        save_message(name, email, subject, message)

        # Send email notification
        send_email_notification(name, email, subject, message)

        # Success
        flash('Thank you for your message! I will get back to you soon.', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html', profile=PROFILE, form_data={})


@app.route('/messages')
def messages():
    """Messages page - View all received contact messages."""
    all_messages = []
    if os.path.exists(MESSAGES_FILE):
        try:
            with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
                all_messages = json.load(f)
        except (json.JSONDecodeError, IOError):
            all_messages = []
    return render_template('messages.html', profile=PROFILE, messages=all_messages)


@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 error page."""
    return render_template('404.html', profile=PROFILE), 404


@app.errorhandler(500)
def internal_error(e):
    """Custom 500 error page."""
    return render_template('500.html', profile=PROFILE), 500


@app.context_processor
def inject_year():
    """Inject current year into all templates."""
    return {'current_year': datetime.now().year}


# ============================================================
# Run Application
# ============================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
