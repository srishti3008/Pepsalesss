
# PEPSales-srishti-notification

## Overview
A notification service that sends alerts to users via Email, SMS, and In-App channels.

---

## Functionality

- *Trigger Notifications*: POST /notifications API endpoint to initiate notifications.
- *Fetch User Notifications*: GET /users/{user_id}/notifications to retrieve a user’s notification history.
- Notification methods supported: *Email, **SMS, and **In-App*.
- *RabbitMQ* handles asynchronous message delivery.
- Implements automatic retries for failed delivery attempts.

---

## Technology Used

- *FastAPI* for RESTful APIs
- *PostgreSQL* with *SQLAlchemy* for database operations
- *Celery* for background task management using *RabbitMQ*
- *Docker & Docker Compose* for containerization and orchestration