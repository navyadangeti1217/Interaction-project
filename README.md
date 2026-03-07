# Student Doubt Sharing Platform

A modern web application for students to share and answer academic doubts/questions.

## 🚀 Features

- **User Authentication**: Register and login with email
- **Post Questions**: Ask academic doubts/questions
- **Answer System**: Provide answers to posted questions
- **Modern UI**: Clean, responsive interface with cards and animations
- **Session Management**: Secure user sessions

## 🛠️ Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript (ES6)
- **Templating**: Jinja2

## 📁 Project Structure

```
INTERACTION/
├── app.py                 # Flask application
├── doubts.db             # SQLite database (ignored)
├── templates/            # HTML templates
│   ├── login.html
│   ├── register.html
│   ├── index.html
│   ├── post.html
│   └── doubt.html
└── static/               # Static assets
    ├── style.css
    └── script.js
```

## 🏃‍♂️ Running the Application

1. **Install Dependencies**:
   ```bash
   pip install flask
   ```

2. **Run the App**:
   ```bash
   python app.py
   ```

3. **Open Browser**:
   Navigate to `http://127.0.0.1:5000`

## 📝 Usage

1. **Register**: Create an account with your email
2. **Login**: Use your email to log in
3. **Post Questions**: Click "Ask Question" to post doubts
4. **Answer Questions**: Click "View Answers" on any question to respond
5. **Logout**: Use the logout button in the navbar

## 🔒 Database Schema

- **users**: id, email (unique), password
- **doubts**: id, username, question, created_at
- **answers**: id, doubt_id, username, answer, created_at

## 🎨 UI Features

- Responsive design with CSS Grid and Flexbox
- Modern card-based layout
- Form validation and error handling
- Interactive elements with JavaScript
- Gradient backgrounds and smooth animations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

Built with ❤️ for students, by students.