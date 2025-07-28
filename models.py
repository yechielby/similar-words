from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# WordItem - Represents a word to be added to the database
class WordItem(BaseModel):
    word: str = Field(..., description="Word to add to database", min_length=1)

# SimilarWordsResponse - Represents a response containing similar words (anagrams)
class SimilarWordsResponse(BaseModel):
    similar: List[str] = Field(..., description="List of similar words (anagrams)")

# AddWordResponse - Represents a response after adding a new word
class AddWordResponse(BaseModel):
    detail: str = Field(..., description="Success message")

# StatsResponse - Represents statistics about the word database
class StatsResponse(BaseModel):
    totalWords: int = Field(..., description="Total number of words in dictionary")
    totalRequests: int = Field(..., description="Total number of requests to /api/v1/similar or /api/v1/add-word endpoint")
    avgProcessingTimeMs: int = Field(..., description="Average time for request handling in microseconds")

# ErrorResponse - Represents an error response
class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error message")