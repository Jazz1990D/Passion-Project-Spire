"""
Recommendation engine for Spire.
Matches users with places based on their aesthetic preferences and behavior.
"""
from collections import Counter
from django.db.models import Count, Q
from places.models import Place
from content.models import Post, Board, BoardPost
from users.models import UserBehavior
from .models import UserRecommendation


def generate_recommendations_for_user(user, limit=20):
    """
    Generate personalized place recommendations based on user behavior and preferences.
    
    This is a basic recommendation algorithm that:
    1. Analyzes user's saved posts and boards for aesthetic/mood tags
    2. Finds places with matching tags
    3. Scores places based on tag overlap
    4. Returns top recommendations
    """
    
    # Get user's aesthetic preferences from their posts and boards
    user_posts = Post.objects.filter(user=user)
    user_boards = Board.objects.filter(user=user)
    
    # Collect all tags from user's content
    aesthetic_tags = []
    mood_tags = []
    
    # From posts
    for post in user_posts:
        if post.tags:
            aesthetic_tags.extend(post.tags)
        if post.mood:
            mood_tags.append(post.mood)
        if post.aesthetic:
            aesthetic_tags.append(post.aesthetic)
    
    # From boards
    for board in user_boards:
        if board.tags:
            aesthetic_tags.extend(board.tags)
    
    # Get user's recent interactions
    recent_behaviors = UserBehavior.objects.filter(user=user).order_by('-timestamp')[:50]
    for behavior in recent_behaviors:
        if behavior.tags:
            aesthetic_tags.extend(behavior.tags)
    
    # Count tag frequencies
    aesthetic_counter = Counter(aesthetic_tags)
    mood_counter = Counter(mood_tags)
    
    # Get user's favorite categories
    if user.favorite_categories:
        aesthetic_counter.update(user.favorite_categories)
    
    if not aesthetic_counter and not mood_counter:
        # No data to base recommendations on, return popular places
        places = Place.objects.filter(is_active=True).order_by('-views_count')[:limit]
        for place in places:
            UserRecommendation.objects.get_or_create(
                user=user,
                place=place,
                defaults={
                    'score': 50.0,
                    'match_reasons': ['popular place'],
                }
            )
        return
    
    # Find matching places
    all_places = Place.objects.filter(is_active=True)
    recommendations = []
    
    for place in all_places:
        # Skip if already recommended and not dismissed
        if UserRecommendation.objects.filter(user=user, place=place, dismissed=False).exists():
            continue
        
        score = 0
        match_reasons = []
        
        # Score based on aesthetic tag matches
        if place.aesthetic_tags:
            for tag in place.aesthetic_tags:
                if tag in aesthetic_counter:
                    weight = aesthetic_counter[tag]
                    score += weight * 10
                    if 'aesthetic match' not in match_reasons:
                        match_reasons.append('aesthetic match')
        
        # Score based on mood tag matches
        if place.mood_tags:
            for tag in place.mood_tags:
                if tag in mood_counter:
                    weight = mood_counter[tag]
                    score += weight * 8
                    if 'mood match' not in match_reasons:
                        match_reasons.append('mood match')
        
        # Boost for verified places
        if place.verified:
            score += 5
            match_reasons.append('verified place')
        
        # Boost for places with high saves
        if place.saves_count > 10:
            score += 3
            match_reasons.append('popular with users')
        
        if score > 0:
            recommendations.append({
                'place': place,
                'score': min(score, 100),  # Cap at 100
                'match_reasons': match_reasons,
            })
    
    # Sort by score and take top recommendations
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    recommendations = recommendations[:limit]
    
    # Save recommendations
    for rec in recommendations:
        UserRecommendation.objects.get_or_create(
            user=user,
            place=rec['place'],
            defaults={
                'score': rec['score'],
                'match_reasons': rec['match_reasons'],
            }
        )
    
    return len(recommendations)


def update_user_preferences(user):
    """
    Update user's favorite_categories based on their behavior.
    This should be called periodically or after significant interactions.
    """
    # Get user's recent posts and boards
    user_posts = Post.objects.filter(user=user)
    user_boards = Board.objects.filter(user=user)
    
    all_tags = []
    
    # Collect tags
    for post in user_posts:
        if post.tags:
            all_tags.extend(post.tags)
        if post.aesthetic:
            all_tags.append(post.aesthetic)
    
    for board in user_boards:
        if board.tags:
            all_tags.extend(board.tags)
    
    # Count and get top 5 categories
    tag_counter = Counter(all_tags)
    top_categories = [tag for tag, count in tag_counter.most_common(5)]
    
    # Update user's favorite categories
    user.favorite_categories = top_categories
    user.save()
    
    return top_categories
