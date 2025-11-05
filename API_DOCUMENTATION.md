# Events System API Documentation

## Base URL

`http://localhost:5001`

## Table of Contents

1. [Events Endpoints](#events-endpoints)
2. [Users Endpoints](#users-endpoints)
3. [Organisations Endpoints](#organisations-endpoints)
4. [Location Endpoints](#location-endpoints)
5. [Event Interest Endpoints](#event-interest-endpoints)

---

## Events Endpoints

### 1. Create Event

**Endpoint:** `POST /event`

**Description:** Create a new event. Event names must be unique.

**Request Body (JSON):**

```json
{
  "name": "Tech Conference",
  "description": "Annual tech conference",
  "date": "15-11-2025",
  "organisation_id": 1
}
```

**Fields:**

- `name` (required): Unique name of the event
- `description` (required): Description of the event
- `date` (required): Date in dd-MM-yyyy format
- `organisation_id` (optional): ID of the organisation hosting the event

**Response (201 Created):**

```json
{
  "message": "Event created successfully",
  "event": {
    "id": 1,
    "name": "Tech Conference",
    "description": "Annual tech conference",
    "date": "15-11-2025",
    "organisation_id": 1,
    "interested_count": 0
  }
}
```

**Error Responses:**

- `400`: Missing required fields or invalid date format
- `404`: Organisation not found
- `409`: Event with this name already exists

**Example with curl:**

```bash
curl -X POST http://localhost:5001/event \
  -H "Content-Type: application/json" \
  -d '{"name":"Tech Conference","description":"Annual tech conference","date":"15-11-2025","organisation_id":1}'
```

---

### 2. Delete Event

**Endpoint:** `DELETE /event`

**Description:** Delete an event by ID.

**Request Body (JSON):**

```json
{
  "id": 1
}
```

**Response (200 OK):**

```json
{
  "message": "Event deleted successfully"
}
```

**Error Responses:**

- `400`: Missing required field
- `404`: Event not found

**Example with curl:**

```bash
curl -X DELETE http://localhost:5001/event \
  -H "Content-Type: application/json" \
  -d '{"id":1}'
```

---

### 3. Get Events

**Endpoint:** `GET /events`

**Description:** Get all events with optional filters.

**Query Parameters (optional):**

- `name`: Filter by event name (partial match)
- `date`: Filter by exact date (dd-MM-yyyy format)

**Response (200 OK):**

```json
{
  "events": [
    {
      "id": 1,
      "name": "Tech Conference",
      "description": "Annual tech conference",
      "date": "15-11-2025",
      "organisation_id": 1,
      "interested_count": 5
    }
  ],
  "count": 1
}
```

**Example with curl:**

```bash
# Get all events
curl -X GET http://localhost:5001/events

# Get events with filters
curl -X GET "http://localhost:5001/events?name=Tech"
```

---

## Users Endpoints

### 4. Create User

**Endpoint:** `POST /user`

**Description:** Create a new user.

**Request Body (JSON):**

```json
{
  "name": "John Doe",
  "age": 30,
  "gender": "male",
  "street": "Main Street",
  "street_number": "123",
  "apartment": "4B",
  "postal_code": "12345",
  "city": "Lisbon",
  "is_volunteer": true,
  "is_assisted": false,
  "has_organisation": true,
  "organisation_id": 1
}
```

**Fields:**

- `name` (required): User's full name
- `age` (required): User's age (must be >= 0)
- `gender` (required): "male", "female", or "other"
- `street` (required): Street name
- `street_number` (required): Street number
- `apartment` (optional): Apartment number
- `postal_code` (required): Postal code
- `city` (required): City name
- `is_volunteer` (optional, default: false): Whether user is a volunteer
- `is_assisted` (optional, default: false): Whether user is assisted by a volunteer
- `has_organisation` (optional, default: false): Whether user is part of an organisation
- `organisation_id` (optional): ID of the organisation user belongs to

**Response (201 Created):**

```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "name": "John Doe",
    "age": 30,
    "gender": "male",
    "street": "Main Street",
    "street_number": "123",
    "apartment": "4B",
    "postal_code": "12345",
    "city": "Lisbon",
    "is_volunteer": true,
    "is_assisted": false,
    "has_organisation": true,
    "organisation_id": 1,
    "created_at": "2025-11-05T10:30:00",
    "updated_at": "2025-11-05T10:30:00"
  }
}
```

**Error Responses:**

- `400`: Missing required fields or invalid gender
- `404`: Organisation not found

**Example with curl:**

```bash
curl -X POST http://localhost:5001/user \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","age":30,"gender":"male","street":"Main Street","street_number":"123","postal_code":"12345","city":"Lisbon","is_volunteer":true}'
```

---

### 5. Get Users

**Endpoint:** `GET /users`

**Description:** Get all users.

**Response (200 OK):**

```json
{
  "users": [
    {
      "id": 1,
      "name": "John Doe",
      "age": 30,
      "gender": "male",
      "street": "Main Street",
      "street_number": "123",
      "apartment": "4B",
      "postal_code": "12345",
      "city": "Lisbon",
      "is_volunteer": true,
      "is_assisted": false,
      "has_organisation": true,
      "organisation_id": 1,
      "created_at": "2025-11-05T10:30:00",
      "updated_at": "2025-11-05T10:30:00"
    }
  ],
  "count": 1
}
```

**Example with curl:**

```bash
curl -X GET http://localhost:5001/users
```

---

## Organisations Endpoints

### 6. Create Organisation

**Endpoint:** `POST /organisation`

**Description:** Create a new organisation. Organisation names must be unique. Organisations can specify allowed locations using municipality IDs and/or parish IDs.

**Request Body (JSON):**

```json
{
  "name": "Tech for Good",
  "description": "Technology for social good",
  "allowed_municipality_ids": [11],
  "allowed_parish_ids": [1, 2, 3],
  "head_user_id": 1
}
```

**Fields:**

- `name` (required): Unique name of the organisation
- `description` (optional): Description of the organisation
- `allowed_municipality_ids` (optional): Array of municipality IDs where the organisation can create events
- `allowed_parish_ids` (optional): Array of parish IDs where the organisation can create events
- `head_user_id` (required): ID of the user who is in charge of the organisation
- **Note:** At least one of `allowed_municipality_ids` or `allowed_parish_ids` must be provided

**Response (201 Created):**

```json
{
  "message": "Organisation created successfully",
  "organisation": {
    "id": 1,
    "name": "Tech for Good",
    "description": "Technology for social good",
    "head_user_id": 1,
    "allowed_municipality_ids": [11],
    "allowed_municipalities": ["Braga"],
    "allowed_parish_ids": [1, 2, 3],
    "allowed_parishes": ["Adaúfe", "Arentim e Cunha", "Braga (Maximinos, Sé e Cividade)"],
    "created_at": "2025-11-05T10:30:00",
    "updated_at": "2025-11-05T10:30:00"
  }
}
```

**Error Responses:**

- `400`: Missing required fields or no locations specified
- `404`: User in charge, municipality, or parish not found
- `409`: Organisation with this name already exists

**Example with curl:**

```bash
curl -X POST http://localhost:5001/organisation \
  -H "Content-Type: application/json" \
  -d '{"name":"Tech for Good","description":"Technology for social good","allowed_municipality_ids":[11],"head_user_id":1}'
```

---

### 7. Get Organisations

**Endpoint:** `GET /organisations`

**Description:** Get all organisations with their allowed locations.

**Response (200 OK):**

```json
{
  "organisations": [
    {
      "id": 1,
      "name": "Tech for Good",
      "description": "Technology for social good",
      "head_user_id": 1,
      "allowed_municipality_ids": [11],
      "allowed_municipalities": ["Braga"],
      "allowed_parish_ids": [1, 2, 3],
      "allowed_parishes": ["Adaúfe", "Arentim e Cunha", "Braga (Maximinos, Sé e Cividade)"],
      "created_at": "2025-11-05T10:30:00",
      "updated_at": "2025-11-05T10:30:00"
    }
  ],
  "count": 1
}
```

**Example with curl:**

```bash
curl -X GET http://localhost:5001/organisations
```

---

## Location Endpoints

### 8. Get Districts

**Endpoint:** `GET /districts`

**Description:** Get all districts.

**Response (200 OK):**

```json
{
  "districts": [
    {
      "id": 1,
      "name": "Braga",
      "population": null,
      "description": null,
      "created_at": "2025-11-05T10:30:00",
      "updated_at": "2025-11-05T10:30:00"
    }
  ],
  "count": 1
}
```

**Example with curl:**

```bash
curl -X GET http://localhost:5001/districts
```

---

### 9. Get Municipalities

**Endpoint:** `GET /municipalities`

**Description:** Get all municipalities, optionally filtered by district.

**Query Parameters (optional):**

- `district_id`: Filter by district ID

**Response (200 OK):**

```json
{
  "municipalities": [
    {
      "id": 11,
      "name": "Braga",
      "district_id": 1,
      "district_name": "Braga",
      "population": null,
      "description": null,
      "created_at": "2025-11-05T10:30:00",
      "updated_at": "2025-11-05T10:30:00"
    },
    {
      "id": 1,
      "name": "Celorico de Basto",
      "district_id": 1,
      "district_name": "Braga",
      "population": null,
      "description": null,
      "created_at": "2025-11-05T10:30:00",
      "updated_at": "2025-11-05T10:30:00"
    }
  ],
  "count": 2
}
```

**Example with curl:**

```bash
# Get all municipalities
curl -X GET http://localhost:5001/municipalities

# Get municipalities in a specific district
curl -X GET "http://localhost:5001/municipalities?district_id=1"
```

---

### 10. Get Parishes

**Endpoint:** `GET /parishes`

**Description:** Get all parishes, optionally filtered by municipality.

**Query Parameters (optional):**

- `municipality_id`: Filter by municipality ID

**Response (200 OK):**

```json
{
  "parishes": [
    {
      "id": 1,
      "name": "Adaúfe",
      "municipality_id": 11,
      "municipality_name": "Braga",
      "district_name": "Braga",
      "population": null,
      "description": null,
      "created_at": "2025-11-05T10:30:00",
      "updated_at": "2025-11-05T10:30:00"
    }
  ],
  "count": 1
}
```

**Example with curl:**

```bash
# Get all parishes
curl -X GET http://localhost:5001/parishes

# Get parishes in a specific municipality
curl -X GET "http://localhost:5001/parishes?municipality_id=11"
```

---

## Event Interest Endpoints

### 11. Mark Interest in Event

**Endpoint:** `POST /event/<event_id>/interest`

**Description:** Mark a user as interested in a specific event. This increments the `interested_count` for the event.

**URL Parameters:**

- `event_id`: ID of the event

**Request Body (JSON):**

```json
{
  "user_id": 1
}
```

**Response (201 Created):**

```json
{
  "message": "Interest registered successfully"
}
```

**Response (200 OK) - if already interested:**

```json
{
  "message": "User is already interested in this event"
}
```

**Error Responses:**

- `400`: Missing required field
- `404`: User or event not found

**Example with curl:**

```bash
curl -X POST http://localhost:5001/event/1/interest \
  -H "Content-Type: application/json" \
  -d '{"user_id":1}'
```

---

### 12. Remove Interest in Event

**Endpoint:** `DELETE /event/<event_id>/interest`

**Description:** Remove a user's interest in a specific event. This decrements the `interested_count` for the event.

**URL Parameters:**

- `event_id`: ID of the event

**Request Body (JSON):**

```json
{
  "user_id": 1
}
```

**Response (200 OK):**

```json
{
  "message": "Interest removed successfully"
}
```

**Error Responses:**

- `400`: Missing required field
- `404`: User was not interested in this event

**Example with curl:**

```bash
curl -X DELETE http://localhost:5001/event/1/interest \
  -H "Content-Type: application/json" \
  -d '{"user_id":1}'
```

---

## Health Check

### 13. Health Check

**Endpoint:** `GET /health`

**Description:** Check if the API is running.

**Response (200 OK):**

```json
{
  "status": "ok",
  "message": "Events API is running"
}
```

**Example with curl:**

```bash
curl -X GET http://localhost:5001/health
```

---

## Database Schema

### Tables

#### districts

- `id`: SERIAL PRIMARY KEY
- `name`: VARCHAR(255) NOT NULL UNIQUE
- `population`: INTEGER (nullable)
- `description`: TEXT (nullable)
- `created_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- `updated_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

#### municipalities

- `id`: SERIAL PRIMARY KEY
- `name`: VARCHAR(255) NOT NULL
- `district_id`: INTEGER NOT NULL (FK to districts)
- `population`: INTEGER (nullable)
- `description`: TEXT (nullable)
- `created_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- `updated_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- UNIQUE constraint on (name, district_id)

#### parishes

- `id`: SERIAL PRIMARY KEY
- `name`: VARCHAR(255) NOT NULL
- `municipality_id`: INTEGER NOT NULL (FK to municipalities)
- `population`: INTEGER (nullable)
- `description`: TEXT (nullable)
- `created_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- `updated_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- UNIQUE constraint on (name, municipality_id)

#### users

- `id`: SERIAL PRIMARY KEY
- `name`: VARCHAR(255) NOT NULL
- `age`: INTEGER NOT NULL (must be >= 0)
- `gender`: VARCHAR(10) NOT NULL (male, female, or other)
- `street`: VARCHAR(255) NOT NULL
- `street_number`: VARCHAR(20) NOT NULL
- `apartment`: VARCHAR(50)
- `postal_code`: VARCHAR(20) NOT NULL
- `city`: VARCHAR(100) NOT NULL
- `is_volunteer`: BOOLEAN DEFAULT FALSE
- `is_assisted`: BOOLEAN DEFAULT FALSE
- `has_organisation`: BOOLEAN DEFAULT FALSE
- `organisation_id`: INTEGER (FK to organisations)
- `created_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- `updated_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

#### organisations

- `id`: SERIAL PRIMARY KEY
- `name`: VARCHAR(255) NOT NULL UNIQUE
- `description`: TEXT
- `head_user_id`: INTEGER NOT NULL (FK to users)
- `created_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- `updated_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

#### organisation_allowed_municipalities

- `id`: SERIAL PRIMARY KEY
- `organisation_id`: INTEGER NOT NULL (FK to organisations)
- `municipality_id`: INTEGER NOT NULL (FK to municipalities)
- `created_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- UNIQUE constraint on (organisation_id, municipality_id)

#### organisation_allowed_parishes

- `id`: SERIAL PRIMARY KEY
- `organisation_id`: INTEGER NOT NULL (FK to organisations)
- `parish_id`: INTEGER NOT NULL (FK to parishes)
- `created_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- UNIQUE constraint on (organisation_id, parish_id)

#### events

- `id`: SERIAL PRIMARY KEY
- `name`: VARCHAR(255) NOT NULL UNIQUE
- `description`: TEXT NOT NULL
- `date`: DATE NOT NULL
- `organisation_id`: INTEGER (FK to organisations)
- `interested_count`: INTEGER DEFAULT 0
- `created_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- `updated_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

#### event_interest

- `id`: SERIAL PRIMARY KEY
- `user_id`: INTEGER NOT NULL (FK to users)
- `event_id`: INTEGER NOT NULL (FK to events)
- `created_at`: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- UNIQUE constraint on (user_id, event_id)

---

## Notes

- All timestamps are in ISO 8601 format
- Dates are in dd-MM-yyyy format for input/output
- The API accepts both JSON and form-data for most endpoints
- Foreign key constraints ensure data integrity
- Unique constraints prevent duplicate event and organisation names
- The `interested_count` is automatically maintained when users mark/remove interest
- Organisations can specify allowed locations at both municipality and parish levels
- Initially, only the Braga district is populated with all 14 municipalities and all 37 parishes of Braga municipality
- Location hierarchy: District → Municipality → Parish
