# Vibe Tweet - Implementation Plan

## Overview
AI-powered tweet generator that learns a user's writing style from their tweet history and generates personalized tweet suggestions based on their tone preferences and trending topics.

## Tech Stack
- **Backend**: Python + FastAPI
- **Database**: PostgreSQL
- **LLM**: Configurable (Claude API + OpenAI GPT-4)
- **Data Source**: Mock data for MVP (folder for scraped data)

---

## Project Structure

```
vibe-tweet/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Environment config & LLM provider settings
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── users.py        # User CRUD endpoints
│   │   │   ├── tweets.py       # Tweet generation endpoints
│   │   │   └── preferences.py  # User preferences endpoints
│   │   └── dependencies.py     # Auth, DB session deps
│   ├── core/
│   │   ├── __init__.py
│   │   ├── style_analyzer.py   # Extracts writing style from tweet history
│   │   ├── trend_matcher.py    # Matches trends with user interests
│   │   └── tweet_generator.py  # Generates personalized tweets
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── base.py             # Abstract LLM interface
│   │   ├── claude_provider.py  # Claude API implementation
│   │   └── openai_provider.py  # OpenAI API implementation
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # User SQLAlchemy model
│   │   ├── tweet.py            # Tweet history model
│   │   └── preferences.py      # User preferences model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py             # Pydantic schemas for users
│   │   ├── tweet.py            # Tweet request/response schemas
│   │   └── preferences.py      # Preferences schemas
│   └── db/
│       ├── __init__.py
│       ├── database.py         # DB connection setup
│       └── migrations/         # Alembic migrations
├── mock_data/
│   ├── README.md               # Instructions for adding mock data
│   ├── sample_tweets.json      # Sample tweet history
│   └── trending_topics.json    # Sample trending topics
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

---

## Core Components

### 1. Style Analyzer (`core/style_analyzer.py`)
Analyzes user's tweet history to extract:
- Average tweet length
- Vocabulary patterns (common words, hashtag usage)
- Sentence structure preferences
- Humor/sarcasm indicators
- Emoji usage patterns
- Common themes/topics

**Output**: A "style profile" JSON object passed to LLM for context.

### 2. Trend Matcher (`core/trend_matcher.py`)
- Takes user interests (e.g., ["tech", "startups", "AI"])
- Matches against trending topics
- Scores and ranks trends by relevance
- Returns top N relevant trends

### 3. Tweet Generator (`core/tweet_generator.py`)
Orchestrates the generation:
1. Fetch user's style profile
2. Get matched trends
3. Build LLM prompt with: style profile + tone preference + selected trends
4. Call configured LLM provider
5. Return list of tweet suggestions

---

## Database Schema

### Users
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| username | VARCHAR | Unique username |
| created_at | TIMESTAMP | Account creation |

### Preferences
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | FK to users |
| interests | JSONB | List of interest topics |
| tone | VARCHAR | Preferred tone (sarcastic, serious, etc.) |
| llm_provider | VARCHAR | "claude" or "openai" |

### TweetHistory
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | FK to users |
| content | TEXT | Tweet content |
| created_at | TIMESTAMP | Original tweet date |
| metadata | JSONB | Likes, retweets, etc. |

### StyleProfiles
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | FK to users |
| profile | JSONB | Extracted style patterns |
| updated_at | TIMESTAMP | Last analysis time |

---

## API Endpoints

### Users
- `POST /users` - Create user
- `GET /users/{id}` - Get user details

### Preferences
- `PUT /users/{id}/preferences` - Update interests, tone, LLM choice
- `GET /users/{id}/preferences` - Get current preferences

### Tweets
- `POST /users/{id}/tweets/import` - Import tweet history (JSON)
- `POST /users/{id}/tweets/analyze` - Trigger style analysis
- `POST /users/{id}/tweets/generate` - Generate tweet suggestions
- `GET /users/{id}/style-profile` - View extracted style

---

## Implementation Steps

1. **Project setup** - FastAPI scaffold, PostgreSQL connection, env config
2. **Database models** - SQLAlchemy models + Alembic migrations
3. **Mock data structure** - Set up mock_data folder with sample data
4. **LLM abstraction** - Base interface + Claude/OpenAI providers
5. **Style analyzer** - Tweet history analysis logic
6. **Trend matcher** - Interest-to-trend matching
7. **Tweet generator** - Main orchestration + LLM prompting
8. **API routes** - Expose all functionality via REST
9. **Testing** - Unit tests for core logic

---

## Dependencies

```
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
alembic==1.13.1
asyncpg==0.29.0
psycopg2-binary==2.9.9
pydantic==2.5.3
pydantic-settings==2.1.0
anthropic==0.18.1
openai==1.12.0
python-dotenv==1.0.0
httpx==0.26.0
```
