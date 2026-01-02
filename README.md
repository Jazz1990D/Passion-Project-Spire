:clipboard: data-model/DATA_DICTIONARY.md


markdown
# Data Dictionary

Complete field-by-field reference for SPIRE database.

## USERS Table
User profiles (no password/authentication fields)

| Field | Type | Nullable | Indexed | Description |
|-------|------|----------|---------|-------------|
| user_id | UUID | NO | YES | Primary key - unique user ID |
| username | VARCHAR(100) | NO | YES | Display name (must be unique) |
| email | VARCHAR(255) | NO | YES | Email address (optional but unique if provided) |
| profile_pic | VARCHAR(500) | YES | NO | URL to profile picture in S3 |
| bio | TEXT | YES | NO | Short bio (max 500 chars) |
| location | VARCHAR(255) | YES | NO | City/region (e.g., "New York, NY") |
| favorite_aesthetics | JSONB | YES | NO | Array of preferred aesthetics: ["minimalist", "luxury"] |
| preferences | JSONB | YES | NO | User settings: {radius: 5, categories: ["restaurant"]} |
| is_active | BOOLEAN | NO | NO | Account status (default: true) |
| created_at | TIMESTAMP | NO | NO | Account creation date |
| updated_at | TIMESTAMP | NO | NO | Last profile update |

**Example Row:**
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "sarah_aesthetic",
  "email": "sarah@example.com",
  "profile_pic": "https://s3.amazonaws.com/.../profile.jpg",
  "bio": "Coffee lover, minimalist vibes, NYC explorer",
  "location": "New York, NY",
  "favorite_aesthetics": ["minimalist", "cafe", "sustainable"],
  "preferences": {
    "radius_miles": 5,
    "categories": ["restaurant", "cafe", "pop-up"],
    "notifications_enabled": true
  },
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-12-20T14:45:00Z"
}
```

---

## BOARDS Table
Collections of pins organized by theme/mood

| Field | Type | Nullable | Indexed | Description |
|-------|------|----------|---------|-------------|
| board_id | UUID | NO | YES | Primary key |
| user_id | UUID | NO | YES | Owner (FK → users) |
| title | VARCHAR(200) | NO | NO | Board name (e.g., "Date Night Spots") |
| description | TEXT | YES | NO | Board description |
| mood_tags | JSONB | YES | NO | Tags: ["romantic", "cozy", "dinner"] |
| color_palette | JSONB | YES | NO | Dominant colors: {primary: "#FF0000", secondary: "#00FF00"} |
| thumbnail_url | VARCHAR(500) | YES | NO | Board cover image URL |
| is_public | BOOLEAN | NO | NO | Public/private (default: false) |
| view_count | INTEGER | NO | NO | Total views (default: 0) |
| save_count | INTEGER | NO | NO | How many times saved (default: 0) |
| created_at | TIMESTAMP | NO | YES | Creation date |
| updated_at | TIMESTAMP | NO | NO | Last update |

**Example Row:**
```json
{
  "board_id": "660e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Minimalist Brunch Spots",
  "description": "Finding the perfect minimalist brunch experience",
  "mood_tags": ["brunch", "minimalist", "casual", "coffee"],
  "color_palette": {
    "primary": "#F5F5F5",
    "secondary": "#8B8680",
    "accent": "#D4AF37"
  },
  "thumbnail_url": "https://s3.amazonaws.com/.../board-cover.jpg",
  "is_public": true,
  "view_count": 245,
  "save_count": 32,
  "created_at": "2024-11-01T09:00:00Z",
  "updated_at": "2024-12-20T14:30:00Z"
}
```

---

## PINS Table
Individual images/videos saved to boards

| Field | Type | Nullable | Indexed | Description |
|-------|------|----------|---------|-------------|
| pin_id | UUID | NO | YES | Primary key |
| board_id | UUID | NO | YES | Parent board (FK → boards) |
| user_id | UUID | NO | YES | Creator (FK → users) |
| media_url | VARCHAR(500) | NO | NO | URL to image/video in S3 |
| media_type | VARCHAR(20) | NO | NO | "image" or "video" |
| caption | TEXT | YES | NO | User's description |
| mood_tags | JSONB | YES | NO | Tags: ["aesthetic", "minimal", "natural-light"] |
| color_palette | JSONB | YES | NO | Extracted dominant colors |
| visual_features | JSONB | YES | NO | AI-extracted features: {style: "minimalist", brightness: 0.8} |
| source_url | VARCHAR(500) | YES | NO | Original source if imported from URL |
| like_count | INTEGER | NO | NO | Total likes (default: 0) |
| created_at | TIMESTAMP | NO | YES | When pin was saved |

**Example Row:**
```json
{
  "pin_id": "770e8400-e29b-41d4-a716-446655440002",
  "board_id": "660e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "media_url": "https://s3.amazonaws.com/.../pin_001.jpg",
  "media_type": "image",
  "caption": "Love the natural light and simple plating here",
  "mood_tags": ["natural-light", "minimalist", "clean-lines", "neutral-tones"],
  "color_palette": {
    "dominant": ["#F5F5F5", "#D4AF37", "#8B8680"],
    "brightness": 0.85
  },
  "visual_features": {
    "style": "minimalist",
    "aesthetic": "cafe",
    "main_subjects": ["food", "table", "natural-light"],
    "color_temperature": "warm"
  },
  "source_url": "https://example.com/pin",
  "like_count": 12,
  "created_at": "2024-11-15T14:22:00Z"
}
```

---

## EVENTS Table
Real-world experiences (restaurants, events, pop-ups, shops)

| Field | Type | Nullable | Indexed | Description |
|-------|------|----------|---------|-------------|
| event_id | UUID | NO | YES | Primary key |
| title | VARCHAR(255) | NO | NO | Event/venue name |
| category | VARCHAR(50) | NO | YES | Type: "restaurant", "cafe", "event", "pop-up", "shop" |
| description | TEXT | YES | NO | What is this experience? |
| address | VARCHAR(500) | YES | NO | Full street address |
| location | POINT | NO | YES | Geo coordinates (latitude, longitude) |
| city | VARCHAR(100) | NO | YES | City name for filtering |
| phone | VARCHAR(20) | YES | NO | Contact phone |
| website | VARCHAR(500) | YES | NO | Website URL |
| image_url | VARCHAR(500) | YES | NO | Main photo URL |
| images | JSONB | YES | NO | Array of image URLs |
| hours | JSONB | YES | NO | Operating hours by day |
| rating | FLOAT | YES | NO | Star rating (0-5, nullable if new) |
| review_count | INTEGER | YES | NO | Number of reviews |
| price_range | VARCHAR(10) | YES | NO | "$", "$$", "$$$", "$$$$" |
| mood_tags | JSONB | YES | NO | Extracted tags: ["romantic", "casual", "trendy"] |
| visual_features | JSONB | YES | NO | AI features matching pins |
| is_trending | BOOLEAN | NO | NO | Trending flag (default: false) |
| source | VARCHAR(50) | NO | NO | Data source: "manual", "google_places", "eventbrite" |
| source_id | VARCHAR(255) | YES | NO | External API ID (for syncing) |
| created_at | TIMESTAMP | NO | YES | When added to SPIRE |
| updated_at | TIMESTAMP | NO | NO | Last sync/update |

**Example Row:**
```json
{
  "event_id": "880e8400-e29b-41d4-a716-446655440003",
  "title": "The Minimal Brunch",
  "category": "restaurant",
  "description": "Minimalist cafe focusing on locally-sourced ingredients and sustainable practices",
  "address": "123 Main St, New York, NY 10001",
  "location": {
    "type": "Point",
    "coordinates": [-74.0060, 40.7128]
  },
  "city": "New York",
  "phone": "(212) 555-0123",
  "website": "https://minimalbrunch.com",
  "image_url": "https://images.example.com/minimal-brunch.jpg",
  "hours": {
    "monday": "8:00-17:00",
    "tuesday": "8:00-17:00",
    "saturday": "9:00-18:00",
    "sunday": "9:00-17:00"
  },
  "rating": 4.8,
  "review_count": 245,
  "price_range": "$$$",
  "mood_tags": ["brunch", "minimalist", "sustainable", "casual", "coffee"],
  "visual_features": {
    "aesthetic": "minimalist",
    "colors": ["#F5F5F5", "#D4AF37"],
    "atmosphere": "calm",
    "lighting": "natural"
  },
  "is_trending": true,
  "source": "google_places",
  "source_id": "ChIJ...",
  "created_at": "2024-10-01T12:00:00Z",
  "updated_at": "2024-12-20T09:30:00Z"
}
```

---

## RECOMMENDATIONS Table
AI-generated experience suggestions

| Field | Type | Nullable | Indexed | Description |
|-------|------|----------|---------|-------------|
| recommendation_id | UUID | NO | YES | Primary key |
| user_id | UUID | NO | YES | Recommended-to user (FK → users) |
| event_id | UUID | NO | YES | Recommended event (FK → events) |
| score | FLOAT | NO | YES | Relevance score (0.0 to 1.0) |
| reason | VARCHAR(255) | YES | NO | Why recommended (e.g., "Matches your minimalist aesthetic") |
| matching_tags | JSONB | YES | NO | Tags that matched: ["minimalist", "natural-light"] |
| distance_miles | FLOAT | YES | NO | How far away (if location provided) |
| created_at | TIMESTAMP | NO | YES | When generated |
| clicked | BOOLEAN | NO | NO | User clicked on it? (default: false) |
| saved | BOOLEAN | NO | NO | User saved it? (default: false) |

**Example Row:**
```json
{
  "recommendation_id": "990e8400-e29b-41d4-a716-446655440004",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "event_id": "880e8400-e29b-41d4-a716-446655440003",
  "score": 0.92,
  "reason": "Matches your minimalist brunch aesthetic",
  "matching_tags": ["minimalist", "brunch", "casual", "natural-light"],
  "distance_miles": 2.3,
  "created_at": "2024-12-20T14:00:00Z",
  "clicked": true,
  "saved": true
}
```

---

## INTERACTIONS Table
User behavior data for recommendation training

| Field | Type | Nullable | Indexed | Description |
|-------|------|----------|---------|-------------|
| interaction_id | UUID | NO | YES | Primary key |
| user_id | UUID | NO | YES | User (FK → users) |
| pin_id | UUID | YES | YES | Pin interacted with (FK → pins) |
| event_id | UUID | YES | YES | Event interacted with (FK → events) |
| action | VARCHAR(50) | NO | YES | "save", "like", "view", "click", "share" |
| duration_seconds | INTEGER | YES | NO | How long viewed (null if save/like) |
| timestamp | TIMESTAMP | NO | YES | When action occurred |

**Example Rows:**
```json
[
  {
    "interaction_id": "aa0e8400-e29b-41d4-a716-446655440005",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "pin_id": "770e8400-e29b-41d4-a716-446655440002",
    "event_id": null,
    "action": "save",
    "duration_seconds": null,
    "timestamp": "2024-12-15T10:30:00Z"
  },
  {
    "interaction_id": "bb0e8400-e29b-41d4-a716-446655440006",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "pin_id": null,
    "event_id": "880e8400-e29b-41d4-a716-446655440003",
    "action": "click",
    "duration_seconds": 45,
    "timestamp": "2024-12-20T14:05:00Z"
  }
]
```

---

## Database Statistics

| Table | Est. Rows | Growth Rate | Key Index |
|-------|-----------|------------|-----------|
| users | 10,000 | 100/day | user_id, email |
| boards | 50,000 | 500/day | user_id, is_public |
| pins | 500,000 | 5,000/day | board_id, user_id |
| events | 5,000 | 50/day | location, city |
| interactions | 2,000,000 | 10,000/day | user_id, action |
| recommendations | 1,000,000 | 100,000/day | user_id, score |

---

## Field Constraints & Validation

### Users
- `username` - 3-100 chars, alphanumeric + underscore
- `email` - Valid email format
- `bio` - Max 500 chars

### Boards
- `title` - 1-200 chars, required
- `mood_tags` - Array of strings, max 10 tags

### Pins
- `media_url` - Valid S3 URL
- `mood_tags` - Array of strings, max 15 tags
- `visual_features` - JSON object with AI data

### Events
- `category` - Must be one of: restaurant, cafe, event, pop-up, shop
- `location` - Valid GeoJSON point
- `rating` - Float between 0 and 5
- `price_range` - One of: "$", "$$", "$$$", "$$$$"

### Recommendations
- `score` - Float between 0.0 and 1.0
- `reason` - Max 255 chars

### Interactions
- `action` - One of: save, like, view, click, share
- `duration_seconds` - Null for save/like, > 0 for view
