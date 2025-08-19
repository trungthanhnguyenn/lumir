### Trade Report Index – README tổng quát

Tài liệu này tóm tắt theo từng mục trong “Công thức tính trade report”, nêu rõ phần nào đã triển khai, cách dùng, và phần nào còn thiếu.

### Yêu cầu hệ thống
- **Python** >= 3.9
- **Thư viện**: `pandas`, `openpyxl`

```bash
pip install pandas openpyxl
```

### Dữ liệu đầu vào
- File Excel mẫu: `data/data_trading.xlsx` (sheet: `Records`)
- Cột tối thiểu cần có:
  - `symbol`
  - `side` (có thể là `Mua/Bán` hoặc `BUY/SELL`)
  - `close_time`
  - `net_profit`
  - `commission`, `swap`
  - Tùy chọn: `profit_gross`, `balance_after`, `pips`, `volume_lots_closed` hoặc `quantity_closed`
- Hệ thống sẽ tự:
  - Trim tên cột (ví dụ ` side` → `side`)
  - Map `Mua/Bán → BUY/SELL`
  - Parse `close_time` với `dayfirst=True`
  - Ép kiểu số cho các cột số

### Cách sử dụng (chạy nhanh)
```python
import pandas as pd
from importlib.machinery import SourceFileLoader

# Tải hàm từ file
calc = SourceFileLoader(
    'calc',
    'lumir-ai/lumir/backend/module/trade_index/calculate_trade.py'
).load_module()

df = pd.read_excel('data/data_trading.xlsx', sheet_name=0)
result = calc.calculate_trade_index(df)

print(result['trades'], result['win_rate_pct'], result['profit_factor'])
```

---

### 1) Tổng quan / Performance Summary – ĐÃ LÀM
- Bao gồm:
  - **trades**, **net_profit**, **gross_profit**, **total_commission**, **total_swap**, **total_fees**
  - **win_rate_pct**, **avg_profit_per_trade** (expectancy), **avg_profit_win**, **avg_loss_loss**
  - **best_trade**, **worst_trade**

Sử dụng: Xem trực tiếp trong `result` theo các key trên.

Giải thích logic:
- Cột sử dụng: `net_profit`, `commission`, `swap` (bắt buộc); các cột khác không ảnh hưởng.
- Tiền xử lý: trim tên cột, ép kiểu số; `side` được map `Mua/Bán → BUY/SELL` (không ảnh hưởng mục này).
- Công thức:
  - `trades = số dòng của df`
  - `total_commission = sum(commission)`; `total_swap = sum(swap)`
  - `total_fees = |total_commission| + |total_swap|`
  - `net_profit = sum(net_profit)`
  - `gross_profit = net_profit + total_fees` (khôi phục lợi nhuận trước phí theo ví dụ trong docs)
  - `win_rate_pct = count(net_profit > 0) / trades * 100`
  - `avg_profit_per_trade (expectancy) = mean(net_profit)`
  - `avg_profit_win = mean(net_profit | net_profit > 0)`, nếu không có trade thắng → 0
  - `avg_loss_loss = mean(net_profit | net_profit < 0)`, nếu không có trade thua → 0
  - `best_trade = max(net_profit)`; `worst_trade = min(net_profit)`

### 2) Chỉ số hiệu suất – ĐÃ LÀM
- **profit_factor**: tổng lãi (trade dương) / |tổng lỗ| (trade âm)
- **pips**: `total_pips`, `avg_pips_per_trade` (nếu có cột `pips`)

Sử dụng: `result['profit_factor']`, `result['total_pips']`, `result['avg_pips_per_trade']`.

Giải thích logic:
- Cột sử dụng: `net_profit` (bắt buộc); `pips` (tuỳ chọn).
- Công thức:
  - `wins_sum = sum(net_profit | net_profit > 0)`
  - `losses_sum = sum(net_profit | net_profit < 0)` (âm)
  - `profit_factor = wins_sum / abs(losses_sum)`; nếu không có lệnh thua → `inf`
  - Nếu có `pips`: `total_pips = sum(pips)`; `avg_pips_per_trade = mean(pips)`

### 3) Equity & Drawdown chi tiết – ĐÃ LÀM
- Tính từ chuỗi lũy kế **RB_k = cumsum(net_profit)**
- Trả về:
  - `result['equity']['rb']`, `['peak']`, `['dd_abs']`, `['dd_pct']`
  - **max_drawdown_pct** (tối đa của DD%)

Sử dụng: Lấy series để vẽ chart hoặc phân tích sâu.

Giải thích logic:
- Cột sử dụng: `net_profit` (bắt buộc). Có thể thay thế bằng `balance_after` nếu muốn (hiện đang dùng `net_profit`).
- Công thức (theo thứ tự dòng dữ liệu; gợi ý: đảm bảo đã sắp theo `close_time`):
  - `RB_k[i] = RB_k[i-1] + net_profit[i]` với `RB_0 = 0`
  - `Peak_k[i] = max(Peak_k[i-1], RB_k[i])`
  - `DD_k[i] = Peak_k[i] - RB_k[i]`
  - `DD_pct[i] = (DD_k[i] / Peak_k[i]) * 100` nếu `Peak_k[i] != 0`, ngược lại `0`
  - `max_drawdown_pct = max(DD_pct)`

### 4) Bảng tháng / Index / RT / Dividend – ĐÃ LÀM
- Trả về `result['monthly']` với các trường: `periods`, `varpc`, `dividend`, `rt`, `index`.

Giải thích logic:
- Cột sử dụng: `close_time` (để nhóm theo tháng), `net_profit`, `commission`, `swap`, và nếu có `balance_after` để tính `rt` chính xác theo số dư đầu kỳ.
- Bước tính:
  1) Sắp xếp theo `close_time`, nhóm theo `year_month`.
  2) `varpc_m = sum(net_profit) theo tháng m`.
  3) `dividend_m = -(sum(|commission|) + sum(|swap|)) theo tháng` (âm, đại diện phí phân bổ theo tháng như ví dụ docs).
  4) `rt_m = (varpc_m - dividend_m) / balance_end_{m-1}` nếu có `balance_after` của tháng trước; ngược lại `None`.
  5) `index`: khởi tạo `100.0`. Nếu `rt_m` là `None` thì reset `index` về `100.0` cho tháng đầu tiên. Các tháng tiếp theo: `index = index * (1 + rt_m)`.
  6) Ví dụ: `periods=['2025-04', ...]`, `index=[100.0, 222.17, 368.29, ...]`.

### 5) Phân tích theo thời gian – ĐÃ LÀM
- Theo giờ: `{trades, profit, wins, losses}`
- Sử dụng: `result['time_analysis']` (dict keyed by giờ 0–23).

Giải thích logic:
- Cột sử dụng: `close_time`, `net_profit` (bắt buộc).
- Tiền xử lý: `close_time → datetime` với `dayfirst=True`; lấy `hour = close_time.hour`.
- Công thức (theo từng `hour`):
  - `trades = số dòng nhóm đó`
  - `profit = sum(net_profit)`
  - `wins = count(net_profit > 0)`
  - `losses = count(net_profit < 0)`

### 6) Phân tích theo Symbol – ĐÃ LÀM
- `{trades, profit, volume, wins, losses}` cho mỗi `symbol`.
- Sử dụng: `result['symbol_analysis']`.

Giải thích logic:
- Cột sử dụng: `symbol`, `net_profit` (bắt buộc); `volume_lots_closed` hoặc `quantity_closed` (tuỳ chọn cho khối lượng).
- Công thức (theo từng `symbol`):
  - `trades = số dòng nhóm symbol`
  - `profit = sum(net_profit)`
  - `volume = sum(volume_lots_closed)` nếu có, ngược lại dùng `quantity_closed` nếu có, không có thì `0`
  - `wins = count(net_profit > 0)`, `losses = count(net_profit < 0)`

### 7) Phân tích theo Side (BUY/SELL) – ĐÃ LÀM
- `{trades, profit, volume, wins, losses}` cho từng side.
- Sử dụng: `result['side_analysis']`.

Giải thích logic:
- Cột sử dụng: `side`, `net_profit` (bắt buộc); `volume_lots_closed`/`quantity_closed` (tuỳ chọn).
- Tiền xử lý: map `side` từ tiếng Việt → `BUY/SELL`.
- Công thức (theo từng `side`): tương tự mục 6 (`symbol`).

### 8) Phân tích hành vi – ĐÃ LÀM
- Heuristic:
  - **rapid_fire_trades** (đóng lệnh cách nhau ≤ 5 phút), **rapid_fire_ratio**
  - **revenge_trades** (mở lệnh sau lệnh lỗ và trong ≤ 30 phút)
  - **max_consecutive_losses**
- Sử dụng: `result['behavioral']`.

Giải thích logic:
- Cột sử dụng: `close_time`, `net_profit` (bắt buộc).
- Công thức (duyệt tuần tự theo thời gian đóng lệnh):
  - `rapid_fire_trades`: đếm cặp lệnh liên tiếp có `delta_minutes ≤ 5`.
  - `rapid_fire_ratio = rapid_fire_trades / trades`.
  - `revenge_trades`: nếu lệnh trước có `net_profit < 0` và `delta_minutes ≤ 30` ⇒ đếm 1.
  - `max_consecutive_losses`: chạy qua chuỗi `net_profit < 0`, tăng `current_streak` khi lỗ, reset khi lãi, lấy max.

### 9) Khuyến nghị Risk/KPI cá nhân hóa – ĐÃ LÀM
- Tính:
  - **avgTradesPerDay**, **max_trades_per_day**
  - **maxDailyLoss → limit_daily_stop (0.8×)**
  - **avgTradeSize → recommended_position_size**
  - **maxLoss → max_risk_per_trade (0.8×)**
- Sử dụng: `result['risk_kpi']`.

Giải thích logic:
- Cột sử dụng: `close_time`, `net_profit` (bắt buộc); `volume_lots_closed`/`quantity_closed` (tuỳ chọn).
- Tiền xử lý: lấy `date = close_time.date()` để nhóm theo ngày.
- Công thức:
  - `daily_pnl = sum(net_profit) theo từng ngày`; `min_daily_loss = min(daily_pnl)`
  - `days_count = max(số ngày, 1)`
  - `avgTradesPerDay = trades / days_count`
  - `max_trades_per_day = ceil(avgTradesPerDay * 1.5)` (hệ số có thể tuỳ chỉnh)
  - `avgTradeSize = mean(volume)` nếu có; `recommended_position_size = avgTradeSize`
  - `maxLoss = min(net_profit)`
  - `max_risk_per_trade = 0.8 * |maxLoss|` (hệ số 0.8 theo ví dụ docs)
  - `limit_daily_stop = 0.8 * |min_daily_loss|`

### 10) Chart Data – ĐÃ LÀM
- `result['chart']`: `labels`, `equity` (RB_k), `drawdown_pct`.

Giải thích logic:
- `labels = [1..trades]`
- `equity = RB_k` (chuỗi lũy kế từ mục 3)
- `drawdown_pct = DD_pct` (chuỗi phần trăm drawdown tương ứng)

### 11) Giao diện mẫu – THAM KHẢO
- Tài liệu có nêu link tham khảo UI. Phần UI không nằm trong module này.

---

### Ngưỡng tham chiếu (theo docs)
- **Profit Factor**: <1 không ổn; 1.0–1.5 theo dõi; >1.5 tốt; >2 rất mạnh
- **Expectancy/trade**: <=0 không ổn; >0 càng cao càng tốt
- **MaxDD%**: >30% không ổn; 15–30% theo dõi; <=15% tốt
- **Rapid-fire ratio**: >0.30 không ổn; <=0.10 tốt
- **Chuỗi thua liên tiếp**: >=5 không ổn; <=2 tốt
- **Rủi ro mỗi lệnh**: nên <=1–2% vốn

---

### Gợi ý mở rộng
- Bổ sung bảng tháng (`varpc`, `dividend`, `rt`, `index`) để khớp đầy đủ mục (4).
- Tùy chọn chuyển cách tính Drawdown sang `balance_after` (hiện tại đang theo RB_k).


