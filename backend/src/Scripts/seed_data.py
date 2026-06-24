import asyncio
import random
from faker import Faker

from sqlalchemy import delete

from src.infrastructure.database.session import AsyncSessionLocal

from src.domain.entities.customer import Customer
from src.domain.entities.product import Product
from src.domain.entities.sale import Sale
from src.domain.entities.supplier import Supplier
from src.domain.entities.department import Department
from src.domain.entities.employee import Employee


fake = Faker()


async def seed_database():

    async with AsyncSessionLocal() as db:

        print("Cleaning existing data...")

        await db.execute(delete(Sale))
        await db.execute(delete(Employee))
        await db.execute(delete(Product))
        await db.execute(delete(Customer))
        await db.execute(delete(Supplier))
        await db.execute(delete(Department))

        await db.commit()

        # --------------------------------------------------
        # Customers
        # --------------------------------------------------

        customers = []

        print("Creating customers...")

        for _ in range(50):

            customer = Customer(
                name=fake.name(),
                email=fake.unique.email(),
                city=fake.city(),
                country=fake.country(),
            )

            db.add(customer)
            customers.append(customer)

        await db.flush()

        # --------------------------------------------------
        # Suppliers
        # --------------------------------------------------

        suppliers = []

        print("Creating suppliers...")

        for _ in range(20):

            supplier = Supplier(
                supplier_name=fake.company(),
                country=fake.country(),
            )

            db.add(supplier)
            suppliers.append(supplier)

        await db.flush()

        # --------------------------------------------------
        # Departments
        # --------------------------------------------------

        departments = []

        department_names = [
            "Sales",
            "Marketing",
            "Finance",
            "Operations",
            "IT",
            "HR",
            "Support",
            "Analytics",
            "Procurement",
            "Management",
        ]

        print("Creating departments...")

        for name in department_names:

            department = Department(
                department_name=name
            )

            db.add(department)
            departments.append(department)

        await db.flush()

        # --------------------------------------------------
        # Employees
        # --------------------------------------------------

        employees = []

        print("Creating employees...")

        for _ in range(25):

            employee = Employee(
                name=fake.name(),
                salary=round(
                    random.uniform(
                        30000,
                        150000,
                    ),
                    2,
                ),
                department_id=random.choice(
                    departments
                ).id,
            )

            db.add(employee)
            employees.append(employee)

        await db.flush()

        # --------------------------------------------------
        # Products
        # --------------------------------------------------

        categories = [
            "Electronics",
            "Accessories",
            "Software",
            "Furniture",
            "Books",
        ]

        products = []

        print("Creating products...")

        for _ in range(30):

            product = Product(
                product_name=fake.word().title(),
                category=random.choice(
                    categories
                ),
                price=round(
                    random.uniform(
                        10,
                        2000,
                    ),
                    2,
                ),
            )

            db.add(product)
            products.append(product)

        await db.flush()

        # --------------------------------------------------
        # Sales
        # --------------------------------------------------

        print("Creating sales...")

        for _ in range(500):

            customer = random.choice(
                customers
            )

            product = random.choice(
                products
            )

            quantity = random.randint(
                1,
                10,
            )

            sale = Sale(
                customer_id=customer.id,
                product_id=product.id,
                quantity=quantity,
                sale_amount=round(
                    quantity
                    * float(product.price),
                    2,
                ),
            )

            db.add(sale)

        await db.commit()

        print()
        print("Database seeded successfully!")
        print("Customers  : 50")
        print("Products   : 30")
        print("Suppliers  : 20")
        print("Departments: 10")
        print("Employees  : 25")
        print("Sales      : 500")


if __name__ == "__main__":

    asyncio.run(
        seed_database()
    )