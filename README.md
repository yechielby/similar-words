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
   git clone https://github.com/yechielby/similar-words.git
   cd similar-words
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

## CLI Tool (Bonus)

The project includes a command-line interface for easy interaction with the API.

### CLI Installation

The CLI tool requires the `requests` package, which is included in the requirements.txt:
```bash
pip install -r requirements.txt
```

### CLI Usage

#### Interactive Mode (Recommended)
Start the interactive mode for a user-friendly experience:
```bash
python cli.py interactive
```

**Interactive Mode Commands:**
- `find <word>` - Find similar words (anagrams)
- `add <word>` - Add a new word to the database
- `stats` - Show API statistics
- `help` - Show available commands
- `quit` or `exit` - Exit the CLI

#### Direct Commands
You can also run commands directly from the terminal:

**Find Similar Words:**
```bash
python cli.py find listen
```

**Add New Word:**
```bash
python cli.py add example
```

**Get Statistics:**
```bash
python cli.py stats
```

**Get Filtered Statistics:**
```bash
# Filter by date range
python cli.py stats --from 2025-07-01T00:00:00 --to 2025-09-01T00:00:00

# Filter by endpoint
python cli.py stats --endpoint /api/v1/similar

# Combined filters
python cli.py stats --from 2025-07-01T00:00:00 --to 2025-09-01T00:00:00 --endpoint /api/v1/similar
```

### CLI Examples

#### Interactive Session Example:
```bash
$ python cli.py interactive

🔤 Similar Words API - Interactive Mode
========================================
Commands:
  1. find <word>     - Find similar words
  2. add <word>      - Add new word
  3. stats           - Show statistics
  4. help            - Show this help
  5. quit            - Exit
========================================

> find listen
✅ Similar words to 'listen':
  1. silent
  2. enlist
  3. tinsel

> add newword
✅ 'newword' added successfully!

> find newword
📝 No similar words found for 'newword'

> add drowwen
✅ 'drowwen' added successfully!

> find newword
✅ Similar words to 'newword':
  1. drowwen

> stats
📊 API Statistics:
  Total Words: 1,502
  Total Requests: 3
  Avg Processing Time: 0.45 microseconds

> quit
👋 Goodbye!
```

#### Direct Commands Examples:
```bash
# Find anagrams
$ python cli.py find listen
✅ Similar words to 'listen':
  1. silent
  2. enlist
  3. tinsel

# Add word that already exists
$ python cli.py add listen
❌ Error: 'listen' already exists in the database.

# Add invalid word
$ python cli.py add test123
❌ Error: Invalid word – must contain only letters

# Word not found
$ python cli.py find xyz123
❌ Error: 'xyz123' not found in the database.

# Statistics with filters
$ python cli.py stats --endpoint /api/v1/similar
📊 API Statistics:
  Total Words: 1,500
  Total Requests: 125
  Avg Processing Time: 0.42 microseconds

🔍 Filters applied:
  Endpoint: /api/v1/similar
```

### CLI Help
Get help for any command:
```bash
# General help
python cli.py --help

# Help for specific command
python cli.py stats --help
python cli.py find --help
python cli.py add --help
```

### CLI Error Handling
The CLI handles various error scenarios gracefully:

- **Server not running**: Provides clear instructions to start the server
- **Invalid words**: Shows validation error messages
- **Network errors**: Displays connection error information
- **API errors**: Shows detailed error messages from the server

### Prerequisites for CLI
1. **API Server Running**: Make sure the FastAPI server is running:
   ```bash
   uvicorn main:app --reload
   ```
2. **Dependencies Installed**: Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

The CLI tool provides a convenient way to test and interact with the Similar Words API without needing to use curl or a web browser!
