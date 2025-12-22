from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from recommendations.recommendation_engine import generate_recommendations_for_user

User = get_user_model()


class Command(BaseCommand):
    help = 'Generate recommendations for all users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            help='Generate recommendations for a specific user (username)',
        )

    def handle(self, *args, **options):
        if options['user']:
            try:
                user = User.objects.get(username=options['user'])
                self.stdout.write(f'Generating recommendations for {user.username}...')
                count = generate_recommendations_for_user(user)
                self.stdout.write(self.style.SUCCESS(f'Generated {count} recommendations for {user.username}'))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User {options["user"]} not found'))
        else:
            self.stdout.write('Generating recommendations for all users...')
            users = User.objects.all()
            total = 0
            for user in users:
                try:
                    count = generate_recommendations_for_user(user)
                    total += count
                    self.stdout.write(f'Generated {count} recommendations for {user.username}')
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Error for {user.username}: {str(e)}'))
            
            self.stdout.write(self.style.SUCCESS(f'Generated {total} total recommendations'))
