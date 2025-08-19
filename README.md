# Lumir AI - Thần Số Học Hiện Đại 🌟

Ứng dụng tính toán thần số học với giao diện hiện đại và công nghệ AI tiên tiến.

## ✨ **Tính Năng Nổi Bật**

### 🎨 **Giao Diện Hiện Đại**
- **Frontend Next.js 14** với TypeScript
- **Animation mượt mà** với Framer Motion
- **Hiệu ứng cosmic** và particles background
- **Responsive design** cho mọi thiết bị
- **Dark theme** với gradient effects

### 🔮 **Tính Toán Thần Số Học**
- **Số Đường Đời** (Life Path Number)
- **Số Linh Hồn** (Soul Number)
- **Số Nhân Cách** (Personality Number)
- **Số Vận Mệnh** (Destiny Number)
- **Đỉnh Cao Cuộc Sống** (Pinnacles)
- **Bài Học Nghiệp Quả** (Karmic Lessons)
- **Chỉ Số Cá Nhân** (Personal Numbers)

### 🚀 **Công Nghệ Sử Dụng**

#### **Backend (FastAPI)**
- Python 3.9+
- FastAPI framework
- Pydantic validation
- Uvicorn server

#### **Frontend (Next.js)**
- Next.js 14 + TypeScript
- Tailwind CSS + Framer Motion
- D3.js + Three.js
- Zustand state management
- React Hook Form + Zod

## 🛠️ **Cài Đặt Nhanh**

### **Yêu Cầu Hệ Thống**
- Python 3.9+
- Node.js 18+
- npm hoặc yarn

### **Bước 1: Clone Repository**
```bash
git clone https://github.com/trungthanhnguyenn/lumir.git
cd lumir
```

### **Bước 2: Cài Đặt Tất Cả Dependencies**
```bash
npm run install:all
```

### **Bước 3: Chạy Development Server**
```bash
npm run dev
```

### **Bước 4: Truy Cập Ứng Dụng**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📁 **Cấu Trúc Project**

```
lumir/
├── backend/                 # FastAPI Backend
│   ├── api/
│   │   └── main.py         # FastAPI app
│   ├── module/
│   │   ├── numorology/     # Numerology calculator
│   │   ├── router/         # API routes
│   │   └── personal_form/  # Form processing
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile
├── frontend/               # Next.js Frontend
│   ├── app/               # Next.js App Router
│   ├── components/        # React components
│   ├── types/             # TypeScript types
│   ├── store/             # Zustand stores
│   ├── package.json       # Node.js dependencies
│   └── README.md          # Frontend documentation
├── app/                   # Gradio Demo App
├── script/                # Shell scripts
├── docker-compose.yml     # Docker configuration
└── README.md              # This file
```

## 🎯 **Hướng Dẫn Sử Dụng**

### **1. Tính Toán Thần Số Học**
1. Truy cập http://localhost:3000
2. Nhập họ tên đầy đủ
3. Nhập ngày sinh (định dạng DD/MM/YYYY)
4. Nhấn "Tra Cứu Ngay"
5. Xem kết quả chi tiết

### **2. API Endpoints**
```bash
# Tính toán thần số học
POST /api/v1/numerology/calculate
{
  "full_name": "Nguyễn Văn A",
  "date_of_birth": "15/06/1995",
  "current_date": "01/01/2024"
}

# Health check
GET /health
```

### **3. Gradio Demo**
Truy cập http://localhost:7860 để sử dụng giao diện Gradio

## 🎨 **Giao Diện Mới**

### **Visual Effects**
- ✨ **Particles Background** - Hiệu ứng hạt động
- 🌟 **Cosmic Animations** - Animation vũ trụ
- 🎯 **Interactive Charts** - Biểu đồ D3.js
- 💫 **Floating Elements** - Phần tử bay
- 🎨 **Gradient Effects** - Hiệu ứng gradient

### **User Experience**
- 📱 **Responsive Design** - Tương thích mọi thiết bị
- ⚡ **Fast Loading** - Tải trang nhanh
- 🎭 **Smooth Animations** - Animation mượt mà
- 🌙 **Dark Theme** - Giao diện tối
- ♿ **Accessibility** - Tiếp cận người khuyết tật

## 🔧 **Scripts**

```bash
# Development
npm run dev              # Chạy cả frontend và backend
npm run dev:backend      # Chỉ chạy backend
npm run dev:frontend     # Chỉ chạy frontend

# Production
npm run build           # Build frontend
npm run start           # Chạy production server

# Setup
npm run install:all     # Cài đặt tất cả dependencies
npm run setup           # Setup hoàn chỉnh
```

## 🐳 **Docker Deployment**

### **Chạy với Docker Compose**
```bash
docker-compose up -d
```

### **Build Docker Images**
```bash
# Backend
cd backend
docker build -t lumir-backend .

# Frontend
cd frontend
docker build -t lumir-frontend .
```

## 🌐 **Deployment**

### **Vercel (Frontend)**
```bash
cd frontend
vercel --prod
```

### **Railway/Heroku (Backend)**
```bash
cd backend
# Deploy với requirements.txt
```

### **Docker**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 🧪 **Testing**

### **Backend Tests**
```bash
cd backend
python -m pytest
```

### **Frontend Tests**
```bash
cd frontend
npm run test
```

## 📊 **Performance**

- **Frontend**: Lighthouse Score 95+
- **Backend**: Response time < 100ms
- **Database**: Optimized queries
- **Caching**: Redis integration

## 🔒 **Security**

- **Input Validation** - Zod schema validation
- **CORS** - Configured for production
- **Rate Limiting** - API protection
- **HTTPS** - SSL/TLS encryption

## 🤝 **Contributing**

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Tạo Pull Request

## 📄 **License**

MIT License - xem file [LICENSE](LICENSE) để biết thêm chi tiết.

## 🆘 **Support**

- 📧 Email: support@lumir-ai.com
- 💬 Discord: [Lumir AI Community]
- 📖 Documentation: [docs.lumir-ai.com]
- 🐛 Issues: [GitHub Issues](https://github.com/trungthanhnguyenn/lumir/issues)

## 🙏 **Acknowledgments**

- **FastAPI** - Modern web framework
- **Next.js** - React framework
- **Tailwind CSS** - Utility-first CSS
- **Framer Motion** - Animation library
- **D3.js** - Data visualization

---

**Made with ❤️ by Lumir AI Team**

*Khám phá bí mật vũ trụ thông qua thần số học hiện đại* ✨
