# your_app/management/commands/create_users.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from market.models import Product  # Import your Product model

class Command(BaseCommand):
    help = 'Create superuser and staff user with necessary permissions'

    def handle(self, *args, **kwargs):
        # Create Superuser
        User.objects.create_superuser('superuser', 'superuser@example.com', 'password')

        # Create Staff User
        staff_user = User.objects.create_user('staffuser', 'staffuser@example.com', 'password')
        staff_user.is_staff = True  # Mark the user as staff
        staff_user.save()

        # Assign Permissions to Staff User (Assuming 'change_product' permission is required)
        product_content_type = ContentType.objects.get_for_model(Product)
        change_product_permission = Permission.objects.get(
            codename='change_product', content_type=product_content_type
        )
        staff_user.user_permissions.add(change_product_permission)
