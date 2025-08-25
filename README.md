# Smart Content Moderator API

## Kurulum

1. Gerekli paketleri yükleyin:
   ```sh
   pip install -r requirements.txt
   ```
2. `.env` dosyanızı oluşturun ve API anahtarlarınızı girin (örnek için `.env.example` dosyasına bakın).
3. Veritabanı tablolarını oluşturun:
   ```sh
   python -m app.create_tables
   ```
4. Uygulamayı başlatın:
   ```sh
   uvicorn app.main:app --reload
   ```

## API Endpointleri

- `POST /api/v1/moderate/text`
- `POST /api/v1/moderate/image`
- `GET /api/v1/moderate/analytics/summary?user=mail@example.com`

### Örnek İstek (Text)
```sh
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/moderate/text" -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"email": "test@example.com", "text": "Test mesajı."}'
```

### Örnek İstek (Image)
```sh
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/moderate/image" -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"email": "test@example.com", "image_url": "https://via.placeholder.com/150"}'
```

## Test

```sh
pytest
```

## Notlar
- OpenAI ve Slack entegrasyonu için anahtarlarınızı `.env` dosyasına ekleyin.
- Docker desteği için ek dosyalar sağlanacaktır.
