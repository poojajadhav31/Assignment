import threading
import random
import time
from django.core.management.base import BaseCommand
from users_app.models import User
from orders_app.models import Order
from products_app.models import Product
from django.db import transaction

class Command(BaseCommand):
    help = "Simulate simultaneous inserts in multiple databases"

    def insert_users(self):
        users = [User(name=f'User{i}', email=f'user{i}@example.com') for i in range(10)]
        User.objects.bulk_create(users)
        print("Inserted 10 users.")

    def insert_products(self):
        products = [Product(name=f'Product{i}', price=random.uniform(10, 100)) for i in range(10)]
        Product.objects.bulk_create(products)
        print("Inserted 10 products.")

    def insert_orders(self):
        users = User.objects.all()
        products = Product.objects.all()

        if not users or not products:
            print("No users or products available. Run user and product insertions first.")
            return

        orders = [
            Order(user_id=random.choice(users).id, product_id=random.choice(products).id, quantity=random.randint(1, 5))
            for _ in range(10)
        ]
        Order.objects.bulk_create(orders)
        print("Inserted 10 orders.")

    def handle(self, *args, **kwargs):
        start_time = time.time()

        threads = [
            threading.Thread(target=self.insert_users),
            threading.Thread(target=self.insert_products),
            threading.Thread(target=self.insert_orders)
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        end_time = time.time()
        print(f"Simultaneous insertions completed in {end_time - start_time:.2f} seconds.")

        # Fetch and display results
        self.show_results()

    def show_results(self):
        print("\n=== Users ===")
        for user in User.objects.all():
            print(user.id, user.name, user.email)

        print("\n=== Products ===")
        for product in Product.objects.all():
            print(product.id, product.name, product.price)

        print("\n=== Orders ===")
        for order in Order.objects.all():
            print(order.id, order.user_id, order.product_id, order.quantity)
