# Ice Cream ERP

Welcome to the Ice Cream ERP! This project is a comprehensive Enterprise Resource Planning (ERP) system designed specifically for managing ice cream stores. It provides tools for managing inventory, sales, employees, and store performance while also automating key tasks such as report generation and notifications.

---

## Features

### Core Features
- **Inventory Management**: Track and manage inventory levels for ice cream flavors, cones, toppings, and other supplies.
- **Sales Management**: Record sales transactions and generate daily/weekly/monthly sales reports.
- **Employee Management**: Manage employee schedules, payroll, and performance metrics.
- **Store Performance Tracking**: Monitor KPIs for individual stores or multiple locations.

### Technical Features
- **Built with Django**: A robust backend framework for secure and scalable operations.
- **Dockerized Environment**: Containerized deployment using Docker for consistency and reliability.
- **RabbitMQ Integration**: Message broker for asynchronous task handling.
- **Discord Webhook Notifications**: Send daily/weekly reports and alerts directly to the store owner's Discord channel.

---

## Prerequisites

- **Docker**: Ensure Docker is installed on your system. [Download Docker](https://www.docker.com/get-started)
- **Docker Compose**: Install Docker Compose. [Install Docker Compose](https://docs.docker.com/compose/install/)
- **Python 3.9+**: Required for any additional customizations.
- **Discord Webhook URL**: Set up a webhook on your Discord server to enable notifications.

---

## Installation and Setup

### 1. Clone the Repository
```bash
$ git clone https://github.com/TihomirGalov/ice_cream_erp.git
$ cd ice-cream-erp
```

### 2. Configure Environment Variables
Copy the example `.env` file and update it with your settings:
```bash
$ cp .env.example .env
```
Update the following fields in the `.env` file:
- `DJANGO_SECRET_KEY`
- `RABBITMQ_USER`
- `RABBITMQ_PASS`
- `RABBITMQ_HOST`
- `RABBITMQ_QUEUE`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `DISCORD_WEBHOOK_URL`: Your Discord webhook URL.

### 3. Build and Start Docker Containers
Run the following commands to set up and launch the Docker environment:
```bash
$ docker-compose build
$ docker-compose up -d
```

### 4. Run Migrations
Apply database migrations:
```bash
$ docker-compose exec web python manage.py migrate
```

### 5. Create a Superuser
Create an admin user for the ERP system:
```bash
$ docker-compose exec web python manage.py createsuperuser
```

### 6. Access the Application
Visit `http://localhost:8000` in your web browser and log in with your superuser credentials.

---

## Usage

### Sending Reports to Discord
The system automatically generates and sends store performance reports to the configured Discord webhook. Reports can be sent for daily, weekly, or monthly dispatch.

### Asynchronous Task Management
RabbitMQ is used for handling tasks such as sending reports and managing notifications.

---

## Development

### Adding Dependencies
Add Python dependencies using `pip`:
```bash
$ docker-compose exec web pip install <package-name>
```
Update the `requirements.txt` file:
```bash
$ docker-compose exec web pip freeze > requirements.txt
```

---

## Deployment

### Production Build
For a production-ready deployment, ensure you:
- Use a production database (e.g., PostgreSQL).
- Configure HTTPS using a reverse proxy (e.g., NGINX).
- Set `DEBUG=False` in the `.env` file.

---

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. Ensure your code is linted and tested before submitting.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

Special thanks to the contributors and the open-source community for their support and inspiration in building this project.

