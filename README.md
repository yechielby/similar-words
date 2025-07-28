# Similar Words API

A FastAPI-based web service that finds similar words (anagrams) by analyzing character composition. The API allows you to add new words to the database and find words that contain the same letters.

## Features

- **Find Similar Words**: Get anagrams of a given word (returns 400 if word not found)
- **Add New Words**: Add words to the database (returns 400 if word already exists)
- **Statistics**: View API usage statistics with optional filtering
- **Performance Monitoring**: Automatic timing middleware tracks processing times in microseconds
- **Proper HTTP Status Codes**: 200 and 400 responses as appropriate

## Installation

### Prerequisites
- Python 3.8 or higher

### Setup with Virtual Environment

1. **Clone or download the project**
   ```bash
   cd my_similar_project
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`

## API Documentation

### Interactive Documentation (Swagger)
Once the server is running, you can access the interactive API documentation at:
**http://localhost:8000/docs**

This provides a user-friendly interface to test all endpoints directly from your browser.

### API Endpoints

#### 1. Get Similar Words
**GET** `/api/v1/similar`

Find words that are anagrams of the given word.

**Parameters:**
- `word` (query parameter): The word to find anagrams for

**Example:**
```
GET /api/v1/similar?word=listen
```

**Response:**
```json
{
  "similar": ["silent", "enlist", "tinsel"]
}
```

**Error Response (400):**
```json
{
  "detail": "'eilnst' not found in the database."
}
```

#### 2. Add New Word
**POST** `/api/v1/add-word`

Add a new word to the database.

**Request Body:**
```json
{
  "word": "example"
}
```

**Response:**
```json
{
  "detail": "'example' added successfully!"
}
```

**Error Response (400):**
```json
{
  "detail": "'example' already exists in the database."
}
```

#### 3. Get Statistics
**GET** `/api/v1/stats`

Get API usage statistics with optional filtering.

**Query Parameters (all optional):**
- `from`: Start date for filtering (ISO 8601 format)
- `to`: End date for filtering (ISO 8601 format)
- `endpoint`: Specific endpoint to filter by

**Example:**
```
GET /api/v1/stats?from=2025-07-01T00:00:00&to=2025-09-01T00:00:00&endpoint=/api/v1/similar
```

**Response:**
```json
{
  "totalWords": 1500,
  "totalRequests": 250,
  "avgProcessingTimeMs": 0.45
}
```

## How It Works

The application uses a character-sorting algorithm to find anagrams:
1. Each word is converted to a "key" by sorting its characters alphabetically
2. Words with the same key are anagrams of each other
3. The system stores words grouped by their keys for fast lookup

**Example:**
- "listen" → key: "eilnst"
- "silent" → key: "eilnst" 
- "enlist" → key: "eilnst"

All these words have the same key, making them anagrams.

## Data Storage

- Words are stored in `words_dataset.txt`
- Each word is on a separate line
- The application loads all words into memory on startup for fast access

## Error Handling

- **HTTP 400**: Invalid words (non-alphabetic characters), words that already exist, or words not found
- **HTTP 200**: Successful responses
- File I/O errors are logged to the console
- All responses include proper HTTP status codes and detailed error messages

## Development

To run in development mode with auto-reload:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Key Implementation Details

- **Pydantic Models**: All endpoints use structured request/response validation
- **Automatic Performance Tracking**: Middleware adds timing headers to responses
- **In-Memory Storage**: Fast anagram lookup using character-sorted keys

## Deactivating Virtual Environment

When you're done working, deactivate the virtual environment:
```bash
deactivate
```
