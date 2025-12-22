from django.core.management.base import BaseCommand
from places.models import Place, Event
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Populate the database with sample places and events'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample places...')
        
        # Sample places
        places_data = [
            {
                'name': 'The Minimalist Cafe',
                'description': 'A serene coffee shop with clean lines, natural light, and artisanal brews. Perfect for quiet work sessions or contemplative afternoons.',
                'place_type': 'cafe',
                'address': '123 Oak Street',
                'city': 'Brooklyn',
                'state': 'NY',
                'country': 'USA',
                'phone': '(555) 123-4567',
                'website': 'https://minimalistcafe.example',
                'instagram': '@minimalistcafe',
                'aesthetic_tags': ['minimalist', 'modern', 'clean', 'bright'],
                'mood_tags': ['peaceful', 'focused', 'calming'],
                'features': ['free wifi', 'natural light', 'vegan options', 'outdoor seating']
            },
            {
                'name': 'Velvet Underground Bar',
                'description': 'Dark, moody cocktail bar with vintage decor and live jazz on weekends. An intimate space for evening conversations.',
                'place_type': 'bar',
                'address': '456 Bourbon Lane',
                'city': 'New Orleans',
                'state': 'LA',
                'country': 'USA',
                'phone': '(555) 987-6543',
                'website': 'https://velvetunderground.example',
                'instagram': '@velvetundergroundbar',
                'aesthetic_tags': ['vintage', 'dark', 'cozy', 'romantic'],
                'mood_tags': ['intimate', 'sophisticated', 'romantic'],
                'features': ['live music', 'craft cocktails', 'dim lighting', 'speakeasy vibe']
            },
            {
                'name': 'Sunflower Garden Bistro',
                'description': 'Farm-to-table restaurant with a sunny patio filled with plants. Fresh, seasonal menu in a cheerful atmosphere.',
                'place_type': 'restaurant',
                'address': '789 Garden Way',
                'city': 'Portland',
                'state': 'OR',
                'country': 'USA',
                'phone': '(555) 246-8135',
                'website': 'https://sunflowerbistro.example',
                'instagram': '@sunflowerbistro',
                'aesthetic_tags': ['botanical', 'bright', 'natural', 'fresh'],
                'mood_tags': ['cheerful', 'healthy', 'energizing'],
                'features': ['outdoor seating', 'farm-to-table', 'vegetarian options', 'brunch']
            },
            {
                'name': 'Industrial Arts Gallery',
                'description': 'Contemporary art space in a converted warehouse. Rotating exhibitions featuring emerging artists and bold installations.',
                'place_type': 'gallery',
                'address': '321 Factory Street',
                'city': 'Los Angeles',
                'state': 'CA',
                'country': 'USA',
                'phone': '(555) 369-2580',
                'website': 'https://industrialartsgallery.example',
                'instagram': '@industrialarts',
                'aesthetic_tags': ['industrial', 'contemporary', 'raw', 'bold'],
                'mood_tags': ['inspiring', 'edgy', 'creative'],
                'features': ['rotating exhibitions', 'artist talks', 'warehouse space', 'installations']
            },
            {
                'name': 'Cozy Corner Bookstore',
                'description': 'Independent bookshop with comfortable reading nooks, rare finds, and a welcoming community atmosphere.',
                'place_type': 'bookstore',
                'address': '567 Literary Lane',
                'city': 'Seattle',
                'state': 'WA',
                'country': 'USA',
                'phone': '(555) 741-8520',
                'website': 'https://cozycornerbooks.example',
                'instagram': '@cozycornerbooks',
                'aesthetic_tags': ['cozy', 'vintage', 'warm', 'inviting'],
                'mood_tags': ['comforting', 'nostalgic', 'peaceful'],
                'features': ['reading nooks', 'rare books', 'local authors', 'book clubs']
            }
        ]
        
        created_places = []
        for place_data in places_data:
            place, created = Place.objects.get_or_create(
                name=place_data['name'],
                defaults=place_data
            )
            if created:
                created_places.append(place)
                self.stdout.write(self.style.SUCCESS(f'Created place: {place.name}'))
        
        self.stdout.write('Creating sample events...')
        
        # Sample events
        today = date.today()
        events_data = [
            {
                'title': 'Sunset Rooftop Sessions',
                'description': 'Live acoustic music as the sun sets over the city. Bring a blanket and enjoy local musicians.',
                'event_type': 'concert',
                'place': created_places[1] if created_places else None,
                'location_name': 'Rooftop Terrace',
                'address': '456 Bourbon Lane, Rooftop',
                'city': 'New Orleans',
                'start_date': today + timedelta(days=7),
                'start_time': '18:00',
                'price_info': 'Free entry, donations welcome',
                'aesthetic_tags': ['casual', 'outdoor', 'bohemian'],
                'mood_tags': ['relaxed', 'social', 'joyful']
            },
            {
                'title': 'Abstract Dreams Exhibition',
                'description': 'Opening reception for new abstract expressionist works by local emerging artists.',
                'event_type': 'exhibition',
                'place': created_places[3] if len(created_places) > 3 else None,
                'location_name': 'Main Gallery',
                'address': '321 Factory Street',
                'city': 'Los Angeles',
                'start_date': today + timedelta(days=3),
                'end_date': today + timedelta(days=45),
                'start_time': '19:00',
                'price_info': 'Free',
                'aesthetic_tags': ['contemporary', 'artistic', 'bold'],
                'mood_tags': ['inspiring', 'thought-provoking', 'creative']
            },
            {
                'title': 'Sunday Farmers Market',
                'description': 'Weekly market featuring local produce, artisanal foods, and handmade crafts.',
                'event_type': 'market',
                'location_name': 'Central Park Square',
                'address': '100 Park Avenue',
                'city': 'Portland',
                'start_date': today + timedelta(days=5),
                'start_time': '09:00',
                'price_info': 'Free entry',
                'aesthetic_tags': ['natural', 'community', 'fresh'],
                'mood_tags': ['lively', 'friendly', 'wholesome']
            }
        ]
        
        for event_data in events_data:
            event, created = Event.objects.get_or_create(
                title=event_data['title'],
                defaults=event_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created event: {event.title}'))
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
