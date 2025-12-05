# Sticky Notes Application

A complete Django web application for managing sticky notes with full CRUD (Create, Read, Update, Delete) functionality. This application demonstrates Django MVT (Model-View-Template) architecture with function-based views, form validation, and comprehensive testing.

## Features

- ✅ Create new sticky notes with title and content
- ✅ View all notes in a list with preview
- ✅ View individual note details
- ✅ Edit existing notes
- ✅ Delete notes with confirmation
- ✅ Beautiful and responsive user interface
- ✅ Success messages for user feedback
- ✅ Admin interface for note management
- ✅ Comprehensive unit tests
- ✅ Custom note manager with recent notes query

## Technologies Used

- Python 3.8+
- Django 4.2.7
- SQLite (development database)
- PostgreSQL support (production via dj-database-url)
- HTML5/CSS3
- WhiteNoise (static file serving)
- Gunicorn (production server)

## Project Structure

This project follows Django's MVT (Model-View-Template) architecture:

```
upwork_project/
├── sticky_notes/          # Django project configuration
│   ├── manage.py
│   ├── sticky_notes/     # Project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── notes/            # Main application
│       ├── migrations/   # Database migrations
│       ├── static/       # Static files (CSS)
│       ├── templates/    # HTML templates
│       ├── models.py     # Note model
│       ├── views.py      # View functions
│       ├── forms.py      # Form definitions
│       ├── urls.py       # URL routing
│       ├── admin.py      # Admin configuration
│       └── tests.py      # Unit tests
├── requirements.txt
├── README.md
├── .gitignore
├── MANUAL_TESTING_CHECKLIST.md
└── PROJECT_STRUCTURE.txt
```

## Installation Instructions

### Prerequisites

- Python 3.8 or higher installed
- pip package manager
- Git (for cloning the repository)

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone [your-repo-url]
   cd upwork_project
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Mac/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Open your browser and navigate to:**
   - Main application: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## Usage

### Creating a Note

1. Click the "Create New Note" button on the home page or navigate to `/note/create/`
2. Fill in the title and content fields
3. Click "Save Note"
4. You'll be redirected to the notes list with a success message

### Viewing Notes

- **List View:** Navigate to the home page (`/`) to see all notes
- **Detail View:** Click "View" on any note card or navigate to `/note/<id>/` to see full note details

### Editing a Note

1. Navigate to a note's detail page
2. Click the "Edit" button
3. Modify the title and/or content
4. Click "Save Note"
5. You'll be redirected to the note detail page with updated content

### Deleting a Note

1. Navigate to a note's detail page
2. Click the "Delete" button
3. Confirm deletion on the confirmation page
4. The note will be permanently deleted and you'll be redirected to the notes list

## Running Tests

To run the comprehensive unit tests:

```bash
python manage.py test notes
```

Or to run tests with verbose output:

```bash
python manage.py test notes --verbosity=2
```

The test suite includes:
- **Model Tests:** Note creation, field validation, timestamps, ordering
- **View Tests:** All CRUD operations, templates, redirects, error handling
- **Form Tests:** Form validation, field widgets, save functionality
- **URL Tests:** URL pattern resolution and reverse lookup
- **Integration Tests:** Complete workflows and navigation

## URLs

| URL Pattern | View | Description |
|------------|------|-------------|
| `/` | `note_list` | Display all notes |
| `/note/create/` | `note_create` | Create a new note |
| `/note/<id>/` | `note_detail` | View note details |
| `/note/<id>/update/` | `note_update` | Update a note |
| `/note/<id>/delete/` | `note_delete` | Delete a note |
| `/admin/` | Admin interface | Django admin panel |

## Model

The `Note` model has the following fields:

- `title` (CharField, max_length=255) - Required
- `content` (TextField) - Note content
- `created_at` (DateTimeField, auto_now_add=True) - Creation timestamp
- `updated_at` (DateTimeField, auto_now=True) - Last update timestamp

**Custom Features:**
- Custom `NoteManager` with `get_recent()` method
- Default ordering by `updated_at` descending (most recent first)

## Design Documentation

See the `design_diagrams/` folder for:
- Use Case Diagram - Shows user interactions
- Sequence Diagram - Shows request-response flow
- Class Diagram - Shows model relationships

## Testing

### Unit Tests

Comprehensive unit tests are located in `notes/tests.py` covering:
- Model functionality and constraints
- View responses and redirects
- Form validation
- URL routing
- Integration workflows

### Manual Testing

See `MANUAL_TESTING_CHECKLIST.md` for a complete manual testing guide.

## Code Standards

- ✅ Follows PEP 8 style guide
- ✅ Uses Django best practices
- ✅ Function-based views (FBV)
- ✅ Django MVT architecture
- ✅ Proper template inheritance
- ✅ Static file management
- ✅ CSRF protection enabled
- ✅ Form validation
- ✅ Error handling with `get_object_or_404`
- ✅ Success messages via Django messages framework

## Contributing

This is an educational project. If you'd like to contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is open source and available for educational purposes.

## Author

[Your Name]

## Acknowledgments

- Django Documentation
- Django Community
