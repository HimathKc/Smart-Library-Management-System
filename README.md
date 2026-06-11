# Smart Library Management System

A Flask + MySQL web application for managing a library's books and members. It includes login access, an admin dashboard, book management, member management, and a clean responsive interface.

## Features

- Admin login system
- Dashboard with library statistics
- Add and view books
- Add and view members
- Category, publisher, and author database structure
- Responsive UI with light/dark theme toggle
- MySQL database integration

## Technologies Used

- Python
- Flask
- MySQL
- HTML
- CSS
- JavaScript

## Project Structure

```text
Smart Library Management System/
├── app.py
├── database.sql
├── requirements.txt
├── .env.example
├── .gitignore
├── static/
│   ├── script.js
│   └── styles.css
└── templates/
    ├── _sidebar.html
    ├── add_book.html
    ├── add_member.html
    ├── books.html
    ├── dashboard.html
    ├── login.html
    ├── members.html
    └── user_dashboard.html
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/smart-library-management-system.git
cd smart-library-management-system
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the MySQL database

Open MySQL Workbench, create a new SQL tab, paste the contents of `database.sql`, and run it.

Or run this command:

```bash
mysql -u root -p < database.sql
```

### 5. Configure environment variables

Create a `.env` file using `.env.example` as a guide:

```env
SECRET_KEY=your-secret-key
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=library_system_db
```

The app also works with default values, but setting environment variables is safer for GitHub because your real database password should never be committed.

### 6. Run the app

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Demo Login

```text
Username: admin
Password: admin123
```

## Notes

This project is built for coursework and learning purposes. For production use, passwords should be hashed instead of stored as plain text.

## Author

Himath Chandrasena
