# School Management System

## Project Title
School Management System

## Description
A comprehensive desktop application designed to manage school operations efficiently. It allows administrators to manage students, teachers, track attendance, handle fee payments, and view overall reports.

## Features
- **Authentication**: Secure admin login.
- **Student Management**: Add, view, update, and delete student records.
- **Teacher Management**: Add, view, update, and delete teacher records.
- **Attendance Tracking**: Mark and view student attendance.
- **Fee Management**: Add and track student fee payments.
- **Dashboard/Reports**: Overview of total students, teachers, and fees collected.

## Technologies Used
- Python 3
- Tkinter (GUI)
- MySQL (Database)
- `mysql-connector-python`
- `pytest` (Testing)

## How to Run Project
1. **Clone the repository**:
   ```bash
   git clone <your-repository-url>
   cd <repository-directory>
   ```
2. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Database Setup**:
   Ensure you have MySQL installed and running. By default, the app expects root user with password `your_password`. You can change this in `app/utils/db.py`.
   Run the database setup script to create the database and tables:
   ```bash
   python setup_db.py
   ```
4. **Run the Application**:
   ```bash
   python app/main.py
   ```
   **Admin Login:** Username: `admin`, Password: `adminpassword` (created by the setup script).

## Git & GitHub Collaboration
The local repository has been initialized with the following branches: `main`, `feature-login`, `feature-student`, `feature-teacher`.

To add a collaborator and push to GitHub:
1. Create an empty repository on GitHub.
2. Link the local repository to GitHub:
   ```bash
   git remote add origin <your-github-repo-url>
   ```
3. Push the branches:
   ```bash
   git push -u origin main
   git push -u origin feature-login
   git push -u origin feature-student
   git push -u origin feature-teacher
   ```
4. On GitHub, go to **Settings** > **Collaborators** and click **Add people**. Search for `shah7008` and add them to the repository.
