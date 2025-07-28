from typing import Optional
from fastapi import FastAPI, HTTPException, Query, Request

from models import WordItem, SimilarWordsResponse, ErrorResponse, AddWordResponse, StatsResponse
from storage import get_words_from_file, add_word_to_file


from collections import defaultdict
from datetime import datetime
import time

app = FastAPI()

file_path = "words_dataset.txt"
word_dict = defaultdict(list)
runtime_records = []
total_words = 0

def get_key(word):
    return ''.join(sorted(word.lower()))

def add_word_to_dict(word):
    key = get_key(word)
    if word not in word_dict[key]:
        word_dict[key].append(word)

def add_new_word(word):
    add_word_to_dict(word)
    add_word_to_file(word, file_path)
    global total_words
    total_words += 1

def init_dictionaries():
    global total_words
    total_words = 0
    try:
        words = get_words_from_file(file_path)
        for word in words:
            add_word_to_dict(word)
        total_words = len(words)
    except Exception as e:
        print(f"Error setting dictionaries: {e}")


def add_runtime_record(endpoint:str, processing_time_us: float):
    runtime_records.append({
        "timestamp": datetime.now(),
        "endpoint": endpoint,
        "processing_time_us": processing_time_us
    })

def get_average_runtime(from_date=None, to_date=None, endpoint=None):
    relevant = []
    for record in runtime_records:
        timestamp = record["timestamp"]
        value = record["processing_time_us"]
        if from_date and timestamp < from_date:
            continue
        if to_date and timestamp > to_date:
            continue
        if endpoint and record["endpoint"] != endpoint:
            continue
        relevant.append(value)

    if not relevant:
        return 0

    return sum(relevant) / len(relevant)


@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start_time = time.perf_counter_ns()
    response = await call_next(request)
    end_time = time.perf_counter_ns()

    processing_time_us = (end_time - start_time) / 1_000 # nanoseconds to microseconds
    endpoint = request.url.path
    if endpoint in ["/api/v1/similar", "/api/v1/add-word"]:
        add_runtime_record(endpoint, processing_time_us)
    
    response.headers["X-Process-Time"] = f"{processing_time_us:.2f}µs"
    return response

# Endpoint GET - Returns Similar Words
@app.get("/api/v1/similar", response_model=SimilarWordsResponse, responses={400: {"model": ErrorResponse}})
def get_similar(word: str):
    if not word or not word.isalpha():
        raise HTTPException(status_code=400, detail="Invalid word – must contain only letters")

    word = word.lower()
    key = get_key(word)
    similar_words = word_dict.get(key, [])

    if word not in similar_words:
        raise HTTPException(status_code=400, detail=f"'{word}' not found in the database.")

    similar_words.remove(word)
    return SimilarWordsResponse(similar=similar_words)



# Endpoint POST - Added New Word
@app.post("/api/v1/add-word", response_model=AddWordResponse, responses={400: {"model": ErrorResponse}})
def add_word(item: WordItem):
    if not item.word or not item.word.isalpha():
        raise HTTPException(status_code=400, detail="Invalid word – must contain only letters")

    word = item.word.lower()
    if word in word_dict[get_key(word)]:
        raise HTTPException(status_code=400, detail=f"'{word}' already exists in the database.")
    
    add_new_word(word)

    return AddWordResponse(detail=f"'{word}' added successfully!")


#for example: /api/v1/stats?from=2025-07-01T00:00:00&to=2025-09-01T00:00:00&endpoint=/api/v1/similar
@app.get("/api/v1/stats", response_model=StatsResponse)
def get_stats(
    from_date: Optional[datetime] = Query(None, alias="from", description="start date for filtering (ISO 8601 format) - optional"),
    to_date: Optional[datetime] = Query(None, alias="to", description="end date for filtering (ISO 8601 format) - optional"),
    endpoint: Optional[str] = Query(None, description="specific endpoint to filter by - optional")
):
    global total_words
    # total_words = sum(len(words) for words in word_dict.values())
    total_requests = len(runtime_records)
    avg_processing_time_us = int(get_average_runtime(from_date, to_date, endpoint))

    return StatsResponse(
        totalWords=total_words,
        totalRequests=total_requests,
        avgProcessingTimeMs=avg_processing_time_us
    )


print("API is running...")
init_dictionaries()
print("Init dictionaries set from file.")

