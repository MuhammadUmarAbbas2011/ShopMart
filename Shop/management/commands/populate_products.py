import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Shop.models import Stores, Products

fake = Faker()

class Command(BaseCommand):
    help = "Generate 200 dummy products"

    def handle(self, *args, **kwargs):
        # Ensure at least one user exists
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR("No users found! Create a user first."))
            return

        # Get or create stores for the user
        stores = list(Stores.objects.filter(by_user=user))
        if not stores:
            for _ in range(5):  # Create 5 stores
                store = Stores.objects.create(
                    by_user=user,
                    category=random.choice([c[0] for c in Stores.CATEGORY_CHOICES])
                )
                stores.append(store)

        products = []
        images = [
            "Shop/static/brand-logo.png", 
            "Shop/static/bg-register.jpg", 
            "Shop/static/bg-login.jpg", 

        ]
        
        for _ in range(200):  # Generate 2000 products
            store = random.choice(stores)
            category = random.choice(Stores.CATEGORY_CHOICES)[0]

            product = Products(
                store=store,
                name=fake.word().capitalize(),
                description=fake.sentence(),
                price=round(random.uniform(5.0, 500.0), 2),
                image=random.choice(images),  # Randomly choose an image path
                category=category
            )
            products.append(product)

        # Bulk create products
        Products.objects.bulk_create(products)
        self.stdout.write(self.style.SUCCESS("Successfully added 200 dummy products!"))
