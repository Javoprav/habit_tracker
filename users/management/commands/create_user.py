from django.core.management import BaseCommand
from users.models import User, UserRoles


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='user@user1.com',
            is_staff=False,
            is_superuser=False,
            is_active=True,
            role=UserRoles.MEMBER,
        )
        user.set_password('123')
        user.save()

        moder = User.objects.create(
            email='moder@moder1.com',
            is_staff=True,
            is_superuser=False,
            is_active=True,
            role=UserRoles.MODERATOR,
        )
        moder.set_password('123')
        moder.save()
