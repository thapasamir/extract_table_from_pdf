# PDF Table Extractor

## Project Overview

This is a Flask-based microservice for extracting tables from PDF files asynchronously using Celery and Redis for task management.

## Features

- Upload PDF files via REST API
- Asynchronous table extraction
- Task tracking and status reporting
- Supports multi-page PDF processing
- Generates CSV files for extracted tables

## Technology Stack

- Python 3.9
- Flask
- Flask-RESTX
- Celery
- Redis
- Tabula-py

## Prerequisites

- Python 3.9+
- Docker
- Docker Compose

## Installation

### Using Docker Compose

1. Clone the repository
2. Create a `.env` file with necessary configurations
3. Run the following command:

```bash
docker-compose up --build
```

### API Endpoints

- **POST /pdf/upload**: Upload a PDF file for processing
  - Returns a unique task ID
- **GET /pdf/status/<task_id>**: Check processing status
  - Returns task status and generated CSV files

## Example Usage

### Upload PDF
```bash
curl -F "file=@document.pdf" http://localhost:5000/pdf/upload
```

### Check Status
```bash
curl http://localhost:5000/pdf/status/<task_id>
```

## Configuration

Key configuration parameters are managed in `app/core/config.py`:
- Upload folder
- Celery settings
- Redis connection

## Error Handling

- Validates file type (PDF only)
- Generates error logs for failed processing
- Provides detailed status responses

## Scaling

The application uses Celery with Redis for:
- Distributed task processing
- Horizontal scalability
- Background job management

## Dependencies

All dependencies are listed in `requirements.txt`. Key libraries:
- Flask-RESTX for API
- Tabula-py for PDF table extraction
- Celery for task queuing
- Redis as message broker
