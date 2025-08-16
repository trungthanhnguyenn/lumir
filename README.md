# Lumir AI - Numerology Calculator & Trading Assistant

Dự án bao gồm 2 phần chính:
1. **Backend API**: Tính toán thần số học dựa trên tên và ngày sinh
2. **Gradio App**: Giao diện demo để test API

## 🚀 Tính năng chính

### 🔮 Numerology Calculator (Backend)
- **20+ chỉ số thần số học**: Life Path, Soul, Personality, Balance, etc.
- **Hỗ trợ tiếng Việt**: Xử lý đầy đủ ký tự có dấu
- **Validation dữ liệu**: Kiểm tra định dạng tên và ngày sinh
- **RESTful API**: Endpoint chuẩn với documentation tự động

### 🤖 Gradio Demo App
- **Giao diện thân thiện**: Chat với AI về thần số học
- **Upload file**: Hỗ trợ PDF, DOCX, TXT, MD
- **Đa ngôn ngữ**: Vietnamese, English, Chinese, Japanese, Korean
- **Session management**: Quản lý phiên chat riêng biệt

## 🏗️ Cấu trúc dự án

```
lumir-ai/
├── backend/                    # FastAPI Backend
│   ├── api/
│   │   └── main.py           # FastAPI app
│   ├── module/
│   │   ├── numorology/
│   │   │   └── cal_num.py    # Numerology calculator
│   │   └── router/
│   │       └── get_numerology_infor.py # API routes
│   ├── requirements.txt       # Python dependencies
│   └── README.md             # Backend documentation
├── app/
│   └── gr.py                 # Gradio demo app
├── README.md                  # Tài liệu này
└── .gitignore                # Git ignore rules
```

## 🛠️ Cài đặt & Chạy

### Backend API
```bash
# Cài đặt dependencies
cd backend
pip install -r requirements.txt

# Chạy API server
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Gradio Demo App
```bash
# Cài đặt dependencies
pip install gradio requests python-dotenv

# Chạy app
cd app
python gr.py
```

## 📚 API Documentation

### Endpoint chính
```
POST /api/v1/numerology/calculate
```

**Request:**
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
      "balance": 8,
      ...
    }
  },
  "message": "Tính toán thần số học thành công"
}
```

### Health Check
```
GET /health
GET /api/v1/numerology/health
```

### API Docs
```
GET /docs          # Swagger UI
GET /redoc         # ReDoc
```

## 🧪 Testing

### Test API với curl
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

## 🔒 Security & Production

- **Input validation**: Kiểm tra dữ liệu đầu vào
- **Error handling**: Xử lý lỗi an toàn
- **CORS support**: Hỗ trợ cross-origin requests
- **Logging**: Ghi log cho debugging
- **Environment variables**: Cấu hình linh hoạt

## 🚀 Deployment

### Backend
```bash
# Production
uvicorn api.main:app --host 0.0.0.0 --port 8686

# Docker
docker build -t lumir-ai-backend .
docker run -p 8686:8686 lumir-ai-backend
```

### Frontend
```bash
# Gradio app
python gr.py --server-name 0.0.0.0 --server-port 7861
```

## 📝 License

MIT License

## 🤝 Đóng góp

1. Fork dự án
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📞 Liên hệ

- Email: [your-email@example.com]
- GitHub: [repository-link]

---

⭐ Nếu dự án hữu ích, hãy cho chúng tôi một star!
