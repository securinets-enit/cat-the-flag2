from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages
import sqlite3

app = Flask(__name__)
app.secret_key = 'secure-session-key-2024-@flki666969'


def init_db():
    """Initialize the database with user data"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       username
                       TEXT
                       UNIQUE
                       NOT
                       NULL,
                       password
                       TEXT
                       NOT
                       NULL,
                       email
                       TEXT,
                       full_name
                       TEXT
                   )
                   ''')

    # Add sample users
    sample_users = [
        ('admin', 'Admin123!rourou', 'admin@company.com', 'SecurinetsEnit{b5a1cfc34b9f1b0a5c8e6a7c3b9d1e2a}'),
        ('john.doe', 'Welcome123!@', 'john.doe@company.com', 'John Doe'),
        ('sarah.connor', 'Terminator2adimosllooo', 'sarah.connor@company.com', 'Sarah Connor'),
        ('michael.scott', 'WorldsBestBosshahahhaf', 'michael.scott@company.com', 'Michael Scott')
    ]

    for username, password, email, full_name in sample_users:
        cursor.execute("INSERT OR IGNORE INTO users (username, password, email, full_name) VALUES (?, ?, ?, ?)",
                       (username, password, email, full_name))

    conn.commit()
    conn.close()


def authenticate_user(username, password):
    """Authentication function with intentional vulnerability"""
    conn = None
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # VULNERABLE: Direct string concatenation in SQL query
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

        cursor.execute(query)
        user = cursor.fetchone()

        if user:
            return True, user
        else:
            return False, None

    except Exception as e:
        return False, None
    finally:
        if conn:
            conn.close()


@app.route('/')
def index():
    if 'user' in session:
        user = session['user']
        is_admin = user['username'] == 'admin'
        flag_html = '''
        <div class="bg-gradient-to-r from-purple-500 to-blue-500 rounded-xl p-6 mb-6 text-white text-center">
            <h2 class="text-2xl font-bold mb-2"><i class="fas fa-flag mr-2"></i>Congratulations!</h2>
            <p class="text-lg">You found the flag:</p>
            <code class="bg-black bg-opacity-30 px-4 py-2 rounded-lg font-mono text-xl mt-2 inline-block">{flag}</code>
        </div>
        '''.format(flag=user['full_name']) if is_admin else ''
        return f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Dashboard - Secure Portal</title>
                <script src="https://cdn.tailwindcss.com"></script>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            </head>
            <body class="bg-gray-50 min-h-screen">
                <nav class="bg-white shadow-sm border-b">
                    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div class="flex justify-between h-16">
                            <div class="flex items-center">
                                <i class="fas fa-shield-alt text-blue-600 text-xl mr-3"></i>
                                <span class="text-xl font-semibold text-gray-900">SecurePortal</span>
                            </div>
                            <div class="flex items-center space-x-4">
                                <span class="text-gray-700">Welcome, {user['full_name']}</span>
                                <a href="/logout" class="bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded-lg text-gray-700 transition duration-200">
                                    <i class="fas fa-sign-out-alt mr-2"></i>Sign Out
                                </a>
                            </div>
                        </div>
                    </div>
                </nav>

                <div class="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
                    {flag_html}
                    <div class="bg-white rounded-xl shadow-sm border p-6 mb-6">
                        <div class="flex items-center mb-6">
                            <div class="bg-blue-100 p-3 rounded-full">
                                <i class="fas fa-user-circle text-blue-600 text-2xl"></i>
                            </div>
                            <div class="ml-4">
                                <h2 class="text-2xl font-bold text-gray-900">{user['full_name']}</h2>
                                <p class="text-gray-600">{user['email']}</p>
                            </div>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div class="bg-blue-50 rounded-lg p-4 border border-blue-100">
                                <div class="flex items-center">
                                    <i class="fas fa-user text-blue-600 text-lg mr-3"></i>
                                    <h3 class="font-semibold text-gray-900">Username</h3>
                                </div>
                                <p class="mt-2 text-gray-700">{user['username']}</p>
                            </div>

                            <div class="bg-green-50 rounded-lg p-4 border border-green-100">
                                <div class="flex items-center">
                                    <i class="fas fa-envelope text-green-600 text-lg mr-3"></i>
                                    <h3 class="font-semibold text-gray-900">Email Address</h3>
                                </div>
                                <p class="mt-2 text-gray-700">{user['email']}</p>
                            </div>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div class="bg-white rounded-xl shadow-sm border p-6 text-center hover:shadow-md transition duration-200">
                            <i class="fas fa-chart-bar text-purple-600 text-3xl mb-4"></i>
                            <h3 class="font-semibold text-gray-900 mb-2">Analytics</h3>
                            <p class="text-gray-600 text-sm">View usage statistics and reports</p>
                        </div>

                        <div class="bg-white rounded-xl shadow-sm border p-6 text-center hover:shadow-md transition duration-200">
                            <i class="fas fa-cog text-gray-600 text-3xl mb-4"></i>
                            <h3 class="font-semibold text-gray-900 mb-2">Settings</h3>
                            <p class="text-gray-600 text-sm">Manage your account preferences</p>
                        </div>

                        <div class="bg-white rounded-xl shadow-sm border p-6 text-center hover:shadow-md transition duration-200">
                            <i class="fas fa-bell text-yellow-600 text-3xl mb-4"></i>
                            <h3 class="font-semibold text-gray-900 mb-2">Notifications</h3>
                            <p class="text-gray-600 text-sm">Check your latest alerts</p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
        '''
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        success, user = authenticate_user(username, password)

        if success:
            session['user'] = {
                'id': user[0],
                'username': user[1],
                'email': user[3],
                'full_name': user[4]
            }
            flash('Login successful! Welcome back.', 'success')
            return redirect(url_for('index'))
        else:
            flash('The username or password you entered is incorrect. Please try again.', 'error')

    # Handle flashed messages for GET request
    messages_html = ''
    for category, message in get_flashed_messages(with_categories=True):
        if category == 'success':
            class_name = 'bg-green-50 text-green-700 border border-green-200'
            icon = 'fa-check-circle'
        elif category == 'error':
            class_name = 'bg-red-50 text-red-700 border border-red-200'
            icon = 'fa-exclamation-circle'
        elif category == 'info':
            class_name = 'bg-blue-50 text-blue-700 border border-blue-200'
            icon = 'fa-info-circle'
        else:
            class_name = 'bg-gray-50 text-gray-700 border border-gray-200'
            icon = 'fa-circle-info'

        messages_html += f'''
        <div class="mb-6 p-4 rounded-lg {class_name}">
            <div class="flex items-center">
                <i class="fas {icon} mr-2"></i>
                {message}
            </div>
        </div>
        '''

    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sign In - Secure Portal</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    </head>
    <body class="bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen flex items-center justify-center p-4">
        <div class="max-w-md w-full">
            <div class="bg-white rounded-2xl shadow-xl p-8">
                <div class="text-center mb-8">
                    <div class="flex justify-center mb-4">
                        <div class="bg-blue-600 p-3 rounded-xl">
                            <i class="fas fa-shield-alt text-white text-2xl"></i>
                        </div>
                    </div>
                    <h1 class="text-3xl font-bold text-gray-900 mb-2">Welcome Back</h1>
                    <p class="text-gray-600">Sign in to access your secure portal</p>
                </div>

                {messages_html}

                <form method="post" class="space-y-6">
                    <div>
                        <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
                            <i class="fas fa-user mr-2 text-gray-400"></i>Username
                        </label>
                        <input type="text" id="username" name="username" required 
                               class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200"
                               placeholder="Enter your username">
                    </div>

                    <div>
                        <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
                            <i class="fas fa-lock mr-2 text-gray-400"></i>Password
                        </label>
                        <input type="password" id="password" name="password" required 
                               class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200"
                               placeholder="Enter your password">
                    </div>

                    <div class="flex items-center justify-between">
                        <div class="flex items-center">
                            <input type="checkbox" id="remember" class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500">
                            <label for="remember" class="ml-2 text-sm text-gray-600">Remember me</label>
                        </div>
                        <a href="#" class="text-sm text-blue-600 hover:text-blue-500 transition duration-200">Forgot password?</a>
                    </div>

                    <button type="submit" 
                            class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-lg transition duration-200 transform hover:scale-105">
                        <i class="fas fa-sign-in-alt mr-2"></i>Sign In
                    </button>
                </form>

                <div class="mt-8 pt-6 border-t border-gray-200">
                    <p class="text-center text-gray-600 text-sm">
                        Don't have an account? 
                        <a href="#" class="text-blue-600 hover:text-blue-500 font-semibold transition duration-200">Contact administrator</a>
                    </p>
                </div>
            </div>

            <div class="text-center mt-6">
                <p class="text-gray-500 text-sm">
                    &copy; 2024 SecurePortal. All rights reserved.
                </p>
            </div>
        </div>
    </body>
    </html>
    '''


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been successfully signed out.', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='0.0.0.0', port=8004)