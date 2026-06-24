import asyncio
import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.session import AsyncSessionLocal
from src.domain.entities.customer import Customer
from src.domain.entities.product import Product
from src.domain.entities.order import Order
from src.domain.entities.order_item import OrderItem
from src.domain.entities.payment import Payment
from src.domain.entities.sale import Sale

fake = Faker()
Faker.seed(42)
random.seed(42)

# List of realistic products by category
PRODUCT_TEMPLATES = {
    "Electronics": [
        ("Flagship Laptop", 1299.99),
        ("Smartphone 5G", 799.99),
        ("Wireless Headphones", 149.99),
        ("Smart Watch Active", 249.99),
        ("High-Res Tablet", 499.99),
        ("Bluetooth Speaker Portable", 89.99),
    ],
    "Clothing": [
        ("Classic Denim Jeans", 59.99),
        ("Organic Cotton T-Shirt", 24.99),
        ("Waterproof Winter Jacket", 129.99),
        ("Comfy Fleece Hoodie", 49.99),
        ("Running Sneakers", 89.99),
        ("Bamboo Fiber Socks 6-Pack", 19.99),
    ],
    "Home & Kitchen": [
        ("Drip Coffee Maker", 79.99),
        ("High-Speed Blender", 99.99),
        ("4-Slice Retro Toaster", 39.99),
        ("Digital Air Fryer", 119.99),
        ("Robot Vacuum Cleaner", 299.99),
        ("Ceramic Dinnerware Set", 89.99),
    ],
    "Books": [
        ("Sci-Fi Bestseller Novel", 14.99),
        ("Inspiring Biography", 19.99),
        ("Mystery Thriller Novel", 12.99),
        ("World Cuisine Cookbook", 29.99),
        ("Ancient History Book", 24.99),
        ("Personal Finance Guide", 22.99),
    ],
    "Sports & Outdoors": [
        ("Non-Slip Yoga Mat", 29.99),
        ("Adjustable Dumbbells Set", 199.99),
        ("Insulated Water Bottle", 24.99),
        ("Ergonomic Hiking Backpack", 79.99),
        ("4-Person Camping Tent", 149.99),
        ("Trail Running Shoes", 99.99),
    ]
}


async def seed_data():
    async with AsyncSessionLocal() as session:
        print("Cleaning up existing database records...")
        await session.execute(
            text(
                "TRUNCATE TABLE sales, payments, order_items, orders, customers, products RESTART IDENTITY CASCADE;"
            )
        )
        await session.commit()

        print("Generating 50 Customers...")
        customers = []
        for _ in range(50):
            signup_date = datetime.now() - timedelta(days=random.randint(180, 365))
            c = Customer(
                name=fake.name(),
                email=fake.unique.email(),
                city=fake.city(),
                country=fake.country(),
                signup_date=signup_date,
            )
            session.add(c)
            customers.append(c)

        print("Generating 30 Products...")
        products = []
        product_keys = list(PRODUCT_TEMPLATES.keys())
        for i in range(30):
            # Select a category cyclically or randomly, then pick a template
            category = product_keys[i % len(product_keys)]
            templates = PRODUCT_TEMPLATES[category]
            template_name, base_price = templates[i % len(templates)]
            
            # Add minor name variation to get 30 unique products
            product_name = f"{template_name} v{1 + (i // len(templates))}"
            p = Product(
                product_name=product_name,
                category=category,
                price=base_price,
            )
            session.add(p)
            products.append(p)

        # Flush to DB to retrieve generated IDs for foreign keys
        await session.flush()

        print("Generating 200 Orders, Order Items, and Payments...")
        for _ in range(200):
            customer = random.choice(customers)
            # Order date must be after customer signup date
            days_since_signup = (datetime.now() - customer.signup_date).days
            order_date = customer.signup_date + timedelta(
                days=random.randint(0, max(0, days_since_signup - 1))
            )
            
            status = random.choices(
                ["Completed", "Pending", "Cancelled"], 
                weights=[80, 15, 5], 
                k=1
            )[0]
            
            order = Order(
                customer_id=customer.id,
                status=status,
                order_date=order_date,
            )
            session.add(order)
            await session.flush()  # Retrieve order ID

            # Generate 1 to 4 items for this order
            order_total = 0.0
            chosen_products = random.sample(products, k=random.randint(1, 4))
            for prod in chosen_products:
                qty = random.randint(1, 3)
                item_total = qty * prod.price
                order_total += item_total
                
                item = OrderItem(
                    order_id=order.id,
                    product_id=prod.id,
                    quantity=qty,
                    unit_price=prod.price,
                )
                session.add(item)

            # Generate payment for non-cancelled orders
            if status != "Cancelled":
                payment_method = random.choices(
                    ["Credit Card", "PayPal", "Bank Transfer"],
                    weights=[60, 25, 15],
                    k=1
                )[0]
                
                pay = Payment(
                    order_id=order.id,
                    payment_method=payment_method,
                    amount=round(order_total, 2),
                    payment_date=order_date + timedelta(minutes=random.randint(5, 1440)),
                )
                session.add(pay)

        print("Generating 500 Sales...")
        for _ in range(500):
            customer = random.choice(customers)
            product = random.choice(products)
            
            # Sale date after customer signup
            days_since_signup = (datetime.now() - customer.signup_date).days
            sale_date = customer.signup_date + timedelta(
                days=random.randint(0, max(0, days_since_signup - 1))
            )
            
            qty = random.randint(1, 5)
            sale_amount = round(qty * product.price, 2)
            
            sale = Sale(
                customer_id=customer.id,
                product_id=product.id,
                quantity=qty,
                sale_amount=sale_amount,
                sale_date=sale_date,
            )
            session.add(sale)

        await session.commit()
        print("Database seeded successfully with all entities!")


if __name__ == "__main__":
    asyncio.run(seed_data())
