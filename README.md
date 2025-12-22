# Spire - Lifestyle Discovery Application

Spire is a lifestyle discovery application that blends visual inspiration with real-world recommendations. Similar to Pinterest, users can upload photos and videos, create boards, and save content that reflects their personal style, interests, and mood. Unlike Pinterest, Spire does not prioritize shopping ads. Instead, it uses user behavior to recommend real places and social experiences — such as restaurants, pop-up shops, events, and outings — that match the user's saved aesthetic.

## Features

### Core Features
- **User Profiles**: Custom user authentication with profile pictures, bios, and preferences
- **Content Sharing**: Upload photos and videos, similar to Pinterest
- **Boards**: Create and organize collections of content by theme or mood
- **Save & Like**: Save content to boards and like posts
- **Visual Discovery**: Browse content by aesthetic, mood, and tags

### Discovery & Recommendations
- **Place Recommendations**: Discover real-world locations (restaurants, cafes, galleries, etc.)
- **Event Discovery**: Find pop-ups, exhibitions, workshops, and festivals
- **Personalized Suggestions**: Algorithm-based recommendations matching your aesthetic
- **Behavior Tracking**: Smart recommendations based on your interactions
- **No Shopping Ads**: Focus on genuine lifestyle experiences, not commercial advertising

## Technology Stack

- **Backend**: Django 6.0 + Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production)
- **Media Storage**: Local storage (development) / Cloud storage (production)
- **API**: RESTful API with full CRUD operations

## Installation

### Prerequisites
- Python 3.12+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Jazz1990D/Passion-Project-Spire.git
cd Passion-Project-Spire
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser (for admin access):
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000/`

## API Endpoints

### Users
- `GET /api/users/` - List all users
- `GET /api/users/{id}/` - Get user details
- `GET /api/behavior/` - Get current user's behavior history

### Content
- `GET /api/content/posts/` - List all posts
- `POST /api/content/posts/` - Create a new post
- `POST /api/content/posts/{id}/like/` - Like a post
- `GET /api/content/boards/` - List boards
- `POST /api/content/boards/` - Create a board
- `POST /api/content/boards/{id}/add_post/` - Add post to board

### Places
- `GET /api/places/places/` - List all places
- `GET /api/places/places/{id}/` - Get place details
- `POST /api/places/places/{id}/save_place/` - Save a place
- `GET /api/places/events/` - List upcoming events
- `GET /api/places/saved/` - Get user's saved places

### Recommendations
- `GET /api/recommendations/recommendations/` - Get personalized recommendations
- `POST /api/recommendations/recommendations/{id}/mark_viewed/` - Mark as viewed
- `POST /api/recommendations/recommendations/{id}/dismiss/` - Dismiss recommendation
- `POST /api/recommendations/feedback/` - Submit feedback

## Admin Interface

Access the Django admin interface at `http://localhost:8000/admin/` using your superuser credentials.

## Data Models

### User Models
- **User**: Custom user with profile and preferences
- **UserBehavior**: Track user interactions for recommendations

### Content Models
- **Board**: Collections of posts organized by theme
- **Post**: User-uploaded photos/videos with metadata
- **BoardPost**: Link posts to boards (many-to-many)
- **Like**: Track post likes

### Places Models
- **Place**: Real-world locations with aesthetic tags
- **Event**: Time-limited events and experiences
- **SavedPlace**: User-saved places

### Recommendation Models
- **UserRecommendation**: Personalized place suggestions
- **RecommendationFeedback**: User feedback on recommendations

## Contributing

This is a passion project. Contributions are welcome! Please feel free to submit pull requests.

## License

See LICENSE file for details.

## Project Vision

Spire bridges the gap between inspiration and action, helping users move from "I love this vibe" to "Here's where you can go." By understanding your aesthetic preferences through the content you save and engage with, Spire curates real-world experiences that match your personal style and interests.
