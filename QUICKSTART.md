# Quick Start Guide for Spire

This guide will help you get Spire up and running in minutes.

## Prerequisites
- Python 3.12+ installed
- pip package manager

## Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/Jazz1990D/Passion-Project-Spire.git
cd Passion-Project-Spire
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Apply database migrations**
```bash
python manage.py migrate
```

4. **Create an admin user**
```bash
python manage.py createsuperuser
```
Follow the prompts to create your admin account.

5. **Load sample data (optional)**
```bash
python manage.py populate_sample_data
```
This will create sample places and events to explore.

6. **Start the development server**
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000/`

## Quick Tour

### Admin Interface
Visit `http://localhost:8000/admin/` and log in with your superuser credentials.

From here you can:
- Manage users
- Create and edit posts and boards
- Add places and events
- View recommendations and user behavior

### API Endpoints

#### Browse the API
Visit `http://localhost:8000/api/` to see available endpoints through the browsable API.

#### Key Endpoints to Try:

**Places:**
```bash
# List all places
curl http://localhost:8000/api/places/places/

# Get a specific place
curl http://localhost:8000/api/places/places/1/
```

**Events:**
```bash
# List all events
curl http://localhost:8000/api/places/events/
```

**Posts:**
```bash
# List all posts
curl http://localhost:8000/api/content/posts/
```

**Boards:**
```bash
# List all boards
curl http://localhost:8000/api/content/boards/
```

## Creating Content

### Via Admin Interface
1. Go to `http://localhost:8000/admin/`
2. Navigate to "Content" section
3. Click "Posts" > "Add post"
4. Fill in the details and upload an image
5. Save

### Via API (requires authentication)
1. Go to `http://localhost:8000/api-auth/login/`
2. Log in with your credentials
3. Go to `http://localhost:8000/api/content/posts/`
4. Use the HTML form at the bottom to create a post

## Generating Recommendations

Once you have users and they've created some content:

```bash
# Generate recommendations for all users
python manage.py generate_recommendations

# Generate for a specific user
python manage.py generate_recommendations --user johndoe
```

## Next Steps

### Explore the API
Full API documentation is available in `API_DOCS.md`

### Customize
- Modify models in `*/models.py` files
- Adjust recommendation logic in `recommendations/recommendation_engine.py`
- Customize admin views in `*/admin.py` files

### Production Deployment
For production deployment:
1. Set `DEBUG = False` in settings.py
2. Configure a production database (PostgreSQL recommended)
3. Set up proper media file storage (AWS S3, etc.)
4. Configure `ALLOWED_HOSTS` in settings.py
5. Use a production server (gunicorn + nginx)
6. Set up HTTPS

## Common Commands

```bash
# Make migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data
python manage.py populate_sample_data

# Generate recommendations
python manage.py generate_recommendations

# Run development server
python manage.py runserver

# Check for issues
python manage.py check
```

## Troubleshooting

**Issue: "No module named django"**
- Solution: Make sure you've installed dependencies: `pip install -r requirements.txt`

**Issue: "Table doesn't exist"**
- Solution: Run migrations: `python manage.py migrate`

**Issue: "No such table: users_user"**
- Solution: The custom user model requires migrations. Run: `python manage.py migrate`

**Issue: Can't create posts via API**
- Solution: Make sure you're logged in. Go to `/api-auth/login/` first.

## Support

For issues or questions, please open an issue on GitHub.

## Happy Building! 🚀

Start exploring, create some content, add places, and watch Spire recommend experiences that match your aesthetic!
