# Project Overview

This is a Django-based code evaluation and assignment management system. It provides a platform where teachers can create subjects and assignments, and students can upload or edit their code online. The system runs automated tests to grade student submissions, and provides a built-in plagiarism checking module to help detect code similarity among submissions.

## Features

- **User Authentication**: Students and teachers can register and log in. Teacher accounts are handled via the `is_teacher` check.
- **Subject & Assignment Management**: Teachers can create and delete subjects and assignments, each with customizable deadlines, maximum points, and maximum number of uploads.
- **File Upload & Code Editor**: Students can upload `.py` files, or open an online editor with Ace Editor for direct code editing.
- **Automated Testing**:
  - Each assignment has a corresponding Python test file (e.g., `DSA1_tests.py`), automatically executed to produce pass/fail results and assign a grade.
- **Plagiarism Detection**:
  - Multiple methods for measuring code similarity (e.g., difflib, tokenization, AST, n-grams, winnowing).
  - A teacher can compare code across all submissions for a given assignment.
- **Grades Overview**:
  - Students can see their best grades across all assignments.
- **Document Storage**:
  - Uploaded files are stored under a structured path: `<username>/<subject>/<assignment_number>/...`.

## Requirements

- **Python 3.8+**  
- **Django 4.x**  
- **Bootstrap 5** (optional for styling, loaded via CDN)  
- **Ace Editor** (loaded via CDN for the browser-based code editor)  
- **SQLite** (default database, can be changed in settings)  

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/SMARTcla/CVUT_Bachelor_Thesis/
cd CVUT_Bachelor_Thesis
```

2. **Set up a virtual environment (optional but recommended):**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Apply migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Run the development server:**
```bash
python manage.py runserver
```

6. **Access the application:**
```bash
Open http://127.0.0.1:8000/ in your web browser.
```

## Configuration

- **Environment Variables**: Specify your database and other sensitive configurations via `.env` or environment variables.
- **Database Settings**: Update `DATABASES` in `settings.py` to connect to your chosen database (e.g., PostgreSQL, MySQL, SQLite).
- **Antiplagiarism Parameters**: Adjust thresholds or settings related to plagiarism detection (e.g., similarity cutoffs for difflib/tokenize/AST/n-grams/Winnowing).

**Example `.env`**
```bash
DEBUG=True
SECRET_KEY="mkononenko-secret"
DATABASE_URL="postgres://user:password@localhost:5432/upload"
```

**Development Server:**

```bash
python manage.py runserver
```

**Docker**

Build the Docker image:

```bash
docker build -t CVUT_Bachelor_Thesis .
```

Run the container:

```bash
docker run -p 8000:8000 CVUT_Bachelor_Thesis
```

**Use your preferred deployment method**

Ensure the .env file or environment variables are properly set on your production server.

Usage

1. Student Flow:

- Register or log in.
- Navigate to a course and upload code solutions to assignments.
- View test results and grades.

2. Teacher Flow:

- Log in as a teacher or admin (superuser).
- Create or manage subjects and assignments.
- View submissions, run tests, and see grades.
- Initiate plagiarism checks (Difflib, Tokenize, AST, n-Grams, Winnowing).


## Testing

### Unit Tests:

```bash
python manage.py test
```

This command runs all Django unit tests, including any tests for plagiarism modules.

### Integration Tests:

TO DO

## Contributing

TO DO

Create a Feature Branch:

```bash
git checkout -b feature/your-feature
```

Commit Changes:

```bash
git commit -m "Add your descriptive commit message"
```

Push to Your Branch:

```bash
git push origin feature/your-feature
```

Submit a Pull Request:

Open a PR from your fork into the main repository’s main or develop branch.

## Documentation

- **Extended Docs**: [Extended Documentation](https://docs.google.com/document/d/1nRsoA4HdOebU5PG1ruUs25b6isW5TrEzwRv1daRllMg/edit?tab=t.0).