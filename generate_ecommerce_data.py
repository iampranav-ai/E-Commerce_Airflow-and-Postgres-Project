from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from faker import Faker 
import random
import uuid

# Initialize Faker
fake = Faker()

# Define categories and subcategories
categories = {
    'Electronics': ['Smartphones', 'Laptops', 'Tablets', 'Cameras', 'Audio'],
    'Clothing': ['Men\'s', 'Women\'s', 'Children\'s', 'Accessories', 'Footwear'],
    'Home & Garden': ['Furniture', 'Decor', 'Kitchen', 'Bedding', 'Gardening'],
    'Sports & Outdoors': ['Fitness', 'Camping', 'Cycling', 'Team Sports', 'Water Sports'],
    'Books': ['Fiction', 'Non-fiction', 'Educational', 'Comics', 'Magazines']
}

# Function to generate fake e-commerce data
def generate_ecommerce_data():
    category = random.choice(list(categories.keys()))
    subcategory = random.choice(categories[category])
    
    return (
        str(uuid.uuid4()),
        str(uuid.uuid4()),
        str(uuid.uuid4()),
        category,
        subcategory,
        fake.word(),
        random.randint(1, 10),
        round(random.uniform(10, 1000), 2),
        fake.date_time_this_year(),
        random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Cash on Delivery'])
    )

# Function to generate and insert data in batches
def generate_and_insert_data():
    postgres_hook = PostgresHook(postgres_conn_id='airflow_connection')
    batch_size = 10000
    total_records = 1000000

    for i in range(0, total_records, batch_size):
        batch = [generate_ecommerce_data() for _ in range(batch_size)]
        postgres_hook.insert_rows('E_Commerce_Big_Data', batch, 
                                  target_fields=['transaction_id', 'customer_id', 'product_id', 'category', 'subcategory',
                                                 'product_name', 'quantity', 'price', 'transaction_date', 'payment_method'])
        print(f"Inserted {i + batch_size} records")

# Default DAG arguments
default_args = {
    'owner': 'pranavVerma',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 20),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
dag = DAG(
    'generate_ecommerce_data',
    default_args=default_args,
    description='A DAG to generate fake e-commerce data and store in PostgreSQL',
    schedule="@once",
    catchup=False,
    tags=['ecommerce', 'faker', 'postgres'],
)

# Task to create the table
create_table_task = PostgresOperator(
    task_id='create_table',
    postgres_conn_id='airflow_connection',
    sql="""
    CREATE TABLE IF NOT EXISTS E_Commerce_Big_Data (
        id SERIAL PRIMARY KEY,
        transaction_id UUID,
        customer_id UUID,
        product_id UUID,
        category VARCHAR(100),
        subcategory VARCHAR(100),
        product_name VARCHAR(200),
        quantity INTEGER,
        price DECIMAL(10, 2),
        transaction_date TIMESTAMP,
        payment_method VARCHAR(50)
    );
    """,
    dag=dag,
)

# Task to generate and insert data
generate_and_insert_task = PythonOperator(
    task_id='generate_and_insert_data',
    python_callable=generate_and_insert_data,
    dag=dag,
)

# Set task dependencies
create_table_task >> generate_and_insert_task