# Spire API Documentation

## Base URL
`http://localhost:8000/api/`

## Authentication
Most endpoints support both authenticated and unauthenticated access. Authenticated users have additional features:
- Create boards and posts
- Like and save content
- Get personalized recommendations
- Track behavior

To authenticate, use the Django REST Framework browsable API at `/api-auth/login/`

## Endpoints

### Users API (`/api/`)

#### List Users
```http
GET /api/users/
```
Returns a paginated list of all users.

**Response:**
```json
{
  "count": 10,
  "next": "http://localhost:8000/api/users/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "bio": "Coffee lover and design enthusiast",
      "profile_picture": "/media/profile_pics/john.jpg",
      "favorite_categories": ["minimalist", "modern"],
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Get User Details
```http
GET /api/users/{id}/
```

#### User Behavior
```http
GET /api/behavior/
POST /api/behavior/
```
Track user interactions. Requires authentication.

**POST Body:**
```json
{
  "interaction_type": "save",
  "content_type": "post",
  "content_id": 123,
  "tags": ["minimalist", "cozy"]
}
```

---

### Content API (`/api/content/`)

#### Posts

##### List Posts
```http
GET /api/content/posts/
```
Returns all posts with pagination.

##### Create Post
```http
POST /api/content/posts/
```
Requires authentication.

**Body (multipart/form-data):**
```json
{
  "title": "My Cozy Corner",
  "description": "Love this aesthetic",
  "content_type": "image",
  "image": <file>,
  "tags": ["cozy", "minimalist"],
  "mood": "peaceful",
  "aesthetic": "minimalist"
}
```

##### Like Post
```http
POST /api/content/posts/{id}/like/
```
Like a specific post. Requires authentication.

##### Unlike Post
```http
POST /api/content/posts/{id}/unlike/
```
Remove like from a post. Requires authentication.

#### Boards

##### List Boards
```http
GET /api/content/boards/
```
Returns public boards and authenticated user's private boards.

##### Create Board
```http
POST /api/content/boards/
```
Requires authentication.

**Body:**
```json
{
  "title": "Minimalist Spaces",
  "description": "Clean, simple interiors",
  "is_private": false,
  "tags": ["minimalist", "modern"]
}
```

##### Add Post to Board
```http
POST /api/content/boards/{id}/add_post/
```
**Body:**
```json
{
  "post_id": 123
}
```

---

### Places API (`/api/places/`)

#### Places

##### List Places
```http
GET /api/places/places/
```
Returns all active places with pagination.

**Response:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "The Minimalist Cafe",
      "description": "A serene coffee shop...",
      "place_type": "cafe",
      "address": "123 Oak Street",
      "city": "Brooklyn",
      "state": "NY",
      "country": "USA",
      "latitude": null,
      "longitude": null,
      "phone": "(555) 123-4567",
      "website": "https://minimalistcafe.example",
      "instagram": "@minimalistcafe",
      "cover_image": null,
      "aesthetic_tags": ["minimalist", "modern", "clean"],
      "mood_tags": ["peaceful", "focused"],
      "features": ["free wifi", "natural light"],
      "views_count": 0,
      "saves_count": 0,
      "is_active": true,
      "verified": false,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

##### Get Place Details
```http
GET /api/places/places/{id}/
```
Automatically increments view count.

##### Save Place
```http
POST /api/places/places/{id}/save_place/
```
Save a place for later. Requires authentication.

**Body (optional):**
```json
{
  "notes": "Want to visit for brunch"
}
```

#### Events

##### List Events
```http
GET /api/places/events/
```
Returns all active upcoming events.

##### Get Event Details
```http
GET /api/places/events/{id}/
```
Automatically increments view count.

#### Saved Places

##### List User's Saved Places
```http
GET /api/places/saved/
```
Returns authenticated user's saved places.

---

### Recommendations API (`/api/recommendations/`)

#### Get Recommendations
```http
GET /api/recommendations/recommendations/
```
Returns personalized place recommendations. Requires authentication.

**Response:**
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "user": "johndoe",
      "place": {
        "id": 1,
        "name": "The Minimalist Cafe",
        ...
      },
      "score": 85.5,
      "match_reasons": ["aesthetic match", "similar saved content"],
      "viewed": false,
      "dismissed": false,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Mark Recommendation as Viewed
```http
POST /api/recommendations/recommendations/{id}/mark_viewed/
```

#### Dismiss Recommendation
```http
POST /api/recommendations/recommendations/{id}/dismiss/
```

#### Submit Feedback
```http
POST /api/recommendations/feedback/
```
**Body:**
```json
{
  "recommendation": 1,
  "feedback_type": "interested"
}
```

Feedback types: `interested`, `not_interested`, `visited`, `saved`

---

## Filtering & Pagination

All list endpoints support pagination:
- `?page=2` - Get page 2
- `?page_size=50` - Change page size (max 100)

---

## Admin Interface

Access the admin interface at `/admin/` to manage:
- Users and user behavior
- Posts and boards
- Places and events
- Recommendations

Create a superuser:
```bash
python manage.py createsuperuser
```

---

## Sample Data

Populate the database with sample places and events:
```bash
python manage.py populate_sample_data
```

---

## Error Responses

All error responses follow this format:
```json
{
  "detail": "Error message here"
}
```

Or for validation errors:
```json
{
  "field_name": ["Error message for this field"]
}
```

Common HTTP status codes:
- `200 OK` - Success
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error
