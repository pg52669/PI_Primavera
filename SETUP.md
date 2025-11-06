# Events System Backend - Setup Guide

## Quick Start with Docker

### Prerequisites

- Docker
- Docker Compose

### Running the Full Stack

```bash
docker compose up
```

This single command starts:

- 🎨 **Frontend** at `http://localhost:5173`
- 🔧 **Backend API** at `http://localhost:5001`
- 🗄️ **PostgreSQL** database at `localhost:5432`

### Stop the services

```bash
docker compose down
```

### Rebuild after changes

```bash
docker compose up --build
```

## Project Structure

The docker-compose.yml orchestrates three services:

- **frontend**: React + Vite app (from `../PI_Primavera_Frontend`)
- **backend**: Python Flask API (from current directory)
- **postgres**: PostgreSQL 16 database

## API Endpoints

### 1. Create Event

**Endpoint:** `POST http://localhost:5000/event`

**Payload:**

```json
{
  "name": "Event Name",
  "description": "Event Description",
  "date": "15-11-2025" // (dd-MM-yyyy)
}
```

**Example with curl:**

```bash
curl -X POST http://localhost:5001/event \
  -H "Content-Type: application/json" \
  -d '{"name":"Tech Conference","description":"Annual tech conference","date":"15-11-2025"}'
```

### 2. Delete Event

**Endpoint:** `DELETE http://localhost:5000/event`

**Payload:**

```json
{
  "id": 1
}
```

**Example with curl:**

```bash
curl -X DELETE http://localhost:5001/event \
  -H "Content-Type: application/json" \
  -d '{"id":1}'
```

### 3. Get Events

**Endpoint:** `GET http://localhost:5000/events`

**Payload (optional filters):**

```json
{
  "name": "Tech",
  "date": "15-11-2025" // (dd-MM-yyyy)
}
```

**Example with curl:**

```bash
# Get all events
curl -X GET http://localhost:5001/events

# Get events with filters
curl -X GET http://localhost:5001/events \
  -H "Content-Type: application/json" \
  -d '{"name":"Tech"}'
```

### Health Check

**Endpoint:** `GET http://localhost:5001/health`

## Notes

- Currently using in-memory storage (data will be lost on restart)
- Database tables will be created in a future update
- The PostgreSQL container is ready for when you implement database integration
