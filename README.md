# E-Commerce Data Generation and Analysis Project

This project demonstrates the generation of fake e-commerce data using Apache Airflow and its storage in a PostgreSQL database. It uses Docker for easy setup and deployment of the required services.

## Project Structure

- `dags/generate_ecommerce_data.py`: Airflow DAG for generating and inserting fake e-commerce data
- `docker-compose.yaml`: Docker Compose file for setting up the project environment

## DAG: generate_ecommerce_data.py

This DAG generates fake e-commerce data and stores it in a PostgreSQL database. Here are its key components:

1. **Data Generation**: Uses the Faker library to create realistic e-commerce data, including transaction IDs, customer IDs, product details, and payment information.
2. **Database Insertion**: Inserts the generated data into a PostgreSQL database in batches for efficient processing.
3. **Scheduling**: Set to run once (`@once`) but can be modified for recurring execution.

The DAG consists of two main tasks:
- `create_table_task`: Creates the necessary table in the PostgreSQL database.
- `generate_and_insert_task`: Generates the fake data and inserts it into the database.

## Docker Setup (docker-compose.yaml)

The `docker-compose.yaml` file sets up the following services:

- **Apache Airflow**: Includes Webserver, Scheduler, Worker, and Triggerer
- **PostgreSQL**: Main database for Airflow and our e-commerce data
- **Redis**: Message broker for Airflow's Celery Executor
- **pgAdmin**: Web-based PostgreSQL admin tool

Note: Redis Insight is included in the compose file but can be ignored for now.

To start the project:

1. Ensure Docker and Docker Compose are installed on your system.
2. Navigate to the project directory.
3. Run `docker-compose up -d` to start all services.
4. Access Airflow web interface at `http://localhost:8080` (default credentials: airflow/airflow).

## Project Screenshots

Docker
![image](https://github.com/user-attachments/assets/86ba17b4-d9ff-4308-8557-b19a91b7a86c)

Airflow DAG
![image](https://github.com/user-attachments/assets/0ec556a6-9edb-4017-8def-a65f443009a6)

pgAdmin Database
![image](https://github.com/user-attachments/assets/7e3dea8b-cd7f-4443-b50b-4c9628f5e730)


## Components Used

- Apache Airflow
- PostgreSQL
- Redis
- Docker & Docker Compose
- Faker (Python library)
- pgAdmin

## Future Enhancements

- Implement data analysis tasks using the generated e-commerce data
- Create visualizations using tools like Grafana or Superset
- Extend the data model to include more e-commerce-specific information

Feel free to contribute to this project by submitting pull requests or opening issues for any bugs or feature requests.
