# Lumir AI Numerology Backend API

Backend API để tính toán thần số học dựa trên tên và ngày sinh.

## 🚀 Tính năng

- **API tính toán thần số học**: Tính toán 20+ chỉ số thần số học
- **Validation dữ liệu**: Kiểm tra định dạng tên và ngày sinh
- **Error handling**: Xử lý lỗi một cách an toàn
- **CORS support**: Hỗ trợ cross-origin requests
- **API documentation**: Tự động tạo docs với Swagger UI

## 🛠️ Cài đặt

### Yêu cầu hệ thống
- Python 3.8+
- pip

### Cài đặt dependencies
```bash
cd backend
pip install -r requirements.txt
```

## 🚀 Chạy ứng dụng

### Development mode
```bash
cd backend
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Production mode
```bash
cd backend
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

## 📚 API Endpoints

### 1. Tính toán thần số học
```
POST /api/v1/numerology/calculate
```

**Request Body:**
```json
{
  "full_name": "Nguyễn Văn A",
  "date_of_birth": "15/06/1995",
  "current_date": "20/12/2024"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "input": {...},
    "pwi_indices": {
      "life_path": 9,
      "soul": 3,
      "personality": 7,
      ...
    }
  },
  "message": "Tính toán thần số học thành công"
}
```

### 2. Health check
```
GET /health
GET /api/v1/numerology/health
```

### 3. API Documentation
```
GET /docs          # Swagger UI
GET /redoc         # ReDoc
```

## 🔧 Cấu trúc dự án

```
backend/
├── api/
│   └── main.py                    # FastAPI app chính
├── module/
│   ├── numorology/
│   │   └── cal_num.py            # Module tính toán thần số học
│   └── router/
│       └── get_numerology_infor.py # API routes
├── requirements.txt               # Python dependencies
└── README.md                     # Tài liệu này
```

## 🧪 Testing

### Test endpoint với curl
```bash
curl -X POST "http://localhost:8000/api/v1/numerology/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Nguyễn Văn A",
    "date_of_birth": "15/06/1995"
  }'
```

### Test health check
```bash
curl http://localhost:8000/health
```

## 🔒 Security

- **Input validation**: Kiểm tra định dạng dữ liệu đầu vào
- **Error handling**: Không expose thông tin nhạy cảm
- **CORS**: Cấu hình cross-origin requests
- **Rate limiting**: Có thể thêm trong production

## 🚀 Production Deployment

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables
```bash
# Production settings
export PYTHONPATH=/app
export ENVIRONMENT=production
```

## 📝 License

MIT License
