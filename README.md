# Vocabulary App

Ứng dụng FastAPI để nhập file txt chứa danh sách từ vựng và xuất file CSV với thông tin chi tiết từ Cambridge Dictionary.

## Tính năng

- **Nhập file txt**: Upload file chứa danh sách từ vựng (mỗi từ một dòng)
- **Lấy dữ liệu từ điển**: Tự động lấy thông tin từ Cambridge Dictionary
- **Dịch tiếng Việt**: Tự động dịch nghĩa và ví dụ sang tiếng Việt
- **Xuất CSV**: Tạo file CSV theo định dạng: Word | Meaning_EN | Meaning_VI | Example | IPA | POS

## Cài đặt

### 1. Tạo và kích hoạt virtual environment

```bash
# Tạo virtual environment
python3 -m venv venv

# Kích hoạt virtual environment
# Trên macOS/Linux:
source venv/bin/activate
# Trên Windows:
# venv\Scripts\activate
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Chạy ứng dụng

```bash
python main.py
```

Hoặc sử dụng uvicorn trực tiếp:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Sử dụng

### 1. Truy cập ứng dụng

Mở trình duyệt và truy cập: `http://localhost:8000`

### 2. API Documentation

FastAPI tự động tạo documentation tại:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 3. API Endpoints

#### Upload và preview vocabulary
```
POST /upload-vocabulary/
```
- Upload file txt để xem preview danh sách từ

#### Xử lý vocabulary và trả về JSON
```
POST /process-vocabulary/
```
- Xử lý file txt và trả về dữ liệu đã được làm giàu

#### Xuất file CSV
```
POST /export-csv/
```
- Xử lý file txt và tải xuống file CSV

### 4. Định dạng file input

Tạo file `.txt` với mỗi từ một dòng:

```
hello
world
computer
science
language
```

### 5. Định dạng file output

File CSV sẽ có cấu trúc:

| Word | Meaning_EN | Meaning_VI | Example | IPA | POS |
|------|------------|------------|---------|-----|-----|
| hello | used as a greeting | xin chào | Hello, how are you? \| Xin chào, bạn khỏe không? | /həˈloʊ/ | exclamation |

## Cấu trúc project

```
Vocab-app/
├── main.py                 # FastAPI application chính
├── requirements.txt        # Dependencies
├── .env                   # Biến môi trường
├── README.md              # Hướng dẫn sử dụng
├── sample_vocabulary.txt   # File mẫu
├── models/
│   ├── __init__.py
│   └── vocabulary.py      # Pydantic models
└── services/
    ├── __init__.py
    ├── dictionary_service.py    # Cambridge Dictionary API
    ├── translation_service.py   # Google Translate
    └── vocabulary_service.py    # Xử lý vocabulary và CSV
```

## Lưu ý

1. **Rate Limiting**: Ứng dụng có delay giữa các requests để tránh bị chặn bởi APIs
2. **Error Handling**: Nếu không thể lấy dữ liệu cho từ nào đó, sẽ ghi lỗi trong CSV
3. **Encoding**: File CSV sử dụng UTF-8 với BOM để hiển thị đúng tiếng Việt
4. **Internet Required**: Cần kết nối internet để truy cập Cambridge Dictionary và Google Translate

## Troubleshooting

### Lỗi kết nối
- Kiểm tra kết nối internet
- Thử lại sau vài phút nếu bị rate limit

### Lỗi encoding
- Đảm bảo file input sử dụng UTF-8 encoding
- Kiểm tra file CSV với Excel hoặc text editor hỗ trợ UTF-8

### Lỗi cài đặt
```bash
# Nếu gặp lỗi với googletrans
pip install googletrans==4.0.0rc1

# Nếu gặp lỗi với dependencies khác
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
``` 