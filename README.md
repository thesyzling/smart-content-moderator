# Smart Content Moderator API

## Setup

1. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```
2. Create your `.env` file and add your API keys (see `.env.example` for reference).
3. Create the database tables:
   ```sh
   python -m app.create_tables
   ```
4. Start the application:
   ```sh
   uvicorn app.main:app --reload
   ```

## API Endpoints

- `POST /api/v1/moderate/text`
- `POST /api/v1/moderate/image`
- `GET /api/v1/moderate/analytics/summary?user=mail@example.com`

### Example Request (Text)
```sh
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/moderate/text" -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"email": "test@example.com", "text": "Test message."}'
```

### Example Request (Image)
```sh
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/moderate/image" -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"email": "test@example.com", "image_url": "https://via.placeholder.com/150"}'
```

## Testing

```sh
pytest
```

## Notes
- Add your API keys for OpenAI and Slack integration in the `.env` file.
- Additional files will be provided for Docker support.
