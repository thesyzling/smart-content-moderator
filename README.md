# Smart Content Moderator API


## Getting Started

### 1. Install Dependencies
Install Python 3.10 or higher, then run:
```sh
pip install -r requirements.txt
```

### 2. Environment Variables
Copy `.env.example` to `.env` and fill in your API keys and webhook URLs:
```sh
cp .env.example .env
# Edit .env with your editor
```

### 3. Initialize the Database
Create the required tables:
```sh
python -m app.create_tables
```

### 4. Run the Application (Development)
Start the FastAPI server with hot-reload:
```sh
uvicorn app.main:app --reload
```
The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 5. Run with Docker (Optional)
To run the app and a PostgreSQL database using Docker Compose:
```sh
docker-compose up --build
```
This will start the API at `http://localhost:8000` and the database at `localhost:5432`.

---


## API Endpoints

- `POST /api/v1/moderate/text` — Moderate a text message
- `POST /api/v1/moderate/image` — Moderate an image by URL
- `GET /api/v1/analytics/summary?user=mail@example.com` — Get moderation analytics for a user


### Example Request (Text)
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/moderate/text" -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"email": "test@example.com", "text": "Test message."}'
```
Or with `curl`:
```sh
curl -X POST "http://127.0.0.1:8000/api/v1/moderate/text" -H "Content-Type: application/json" -d '{"email": "test@example.com", "text": "Test message."}'
```

### Example Request (Image)
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/moderate/image" -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"email": "test@example.com", "image_url": "https://via.placeholder.com/150"}'
```
Or with `curl`:
```sh
curl -X POST "http://127.0.0.1:8000/api/v1/moderate/image" -H "Content-Type: application/json" -d '{"email": "test@example.com", "image_url": "https://via.placeholder.com/150"}'
```


## Running Tests

To run all automated tests:
```sh
pytest
```


## Notes
- Add your API keys for OpenAI, Gemini, and Slack integration in the `.env` file.
- For production, use Docker or a process manager like Gunicorn/Uvicorn with workers.
- See `.env.example` for required environment variables.
