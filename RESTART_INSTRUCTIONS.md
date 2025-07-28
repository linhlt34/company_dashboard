# Hướng Dẫn Restart Dashboard

## Vấn Đề Hiện Tại
Từ ảnh chụp, tôi thấy biểu đồ vẫn đang hiển thị theo theme cũ (không có MA lines, không có legend đẹp). Điều này có thể do:

1. **Cache của Streamlit** - Dashboard vẫn đang sử dụng code cũ từ cache
2. **Dependencies chưa được cài đặt** - Cần cài pandas, plotly, requests

## Giải Pháp

### Bước 1: Cài Đặt Dependencies
```bash
pip install pandas plotly requests streamlit
```

### Bước 2: Clear Cache và Restart Dashboard

#### Cách 1: Clear Cache Streamlit
```bash
# Nếu streamlit đã được cài đặt globally
streamlit cache clear

# Hoặc
python -m streamlit cache clear
```

#### Cách 2: Restart Dashboard Hoàn Toàn
1. **Dừng dashboard hiện tại** (Ctrl+C trong terminal đang chạy)
2. **Xóa cache thủ công**:
   ```bash
   # Xóa thư mục cache
   rm -rf .streamlit/cache/
   ```
3. **Restart dashboard**:
   ```bash
   streamlit run Company_Dashboard.py
   ```

### Bước 3: Kiểm Tra

Sau khi restart, biểu đồ mới sẽ có:

✅ **MA(20) và MA(50) lines** - Đường trung bình động màu cam và xanh
✅ **Legend đẹp** - Chú thích rõ ràng ở trên cùng
✅ **Theme đẹp** - Màu sắc chuyên nghiệp, grid lines tinh tế
✅ **Volume color-coded** - Thanh volume màu xanh/đỏ theo giá

## Cấu Trúc Mới Đã Được Tạo

```
ssi/
├── __init__.py      # Package initialization
├── fetch.py         # API data fetching
├── chart.py         # Chart creation with MA lines
├── loader.py        # Main interface
└── README.md        # Documentation
```

## Tính Năng Mới

### Technical Indicators
- **MA(20)**: 20-day moving average (orange line)
- **MA(50)**: 50-day moving average (blue line)
- **Volume**: Color-coded bars (green for up, red for down)

### Visual Enhancements
- Professional color scheme
- Clear horizontal legend
- Subtle grid lines
- Responsive layout
- Better typography

### Error Handling
- Network timeout handling
- API error management
- Data validation
- User-friendly messages

## Nếu Vẫn Không Hoạt Động

1. **Kiểm tra dependencies**:
   ```bash
   pip list | grep -E "(pandas|plotly|requests|streamlit)"
   ```

2. **Kiểm tra import**:
   ```bash
   python -c "from ssi import load_ticker_price; print('✅ Import successful')"
   ```

3. **Restart hoàn toàn**:
   - Đóng tất cả terminal
   - Mở terminal mới
   - Chạy lại dashboard

## Lưu Ý

- File `SSI_API.py` cũ đã được xóa
- Dashboard đã được cập nhật để sử dụng package mới
- Code mới có đầy đủ MA lines và legend đẹp
- Chỉ cần restart để áp dụng thay đổi 