## Feature 1: Tổng quan/Performance Summary
- Công thức:
  - `trades = số dòng của df`
  - `total_commission = sum(commission)`; `total_swap = sum(swap)`
  - `total_fees = |total_commission| + |total_swap|`
  - `net_profit = sum(net_profit)`
  - `gross_profit = sum(profit_gross)` theo công thức trong docs
  - `win_rate_pct = count(net_profit > 0) / trades * 100`
  - `avg_profit_per_trade (expectancy) = mean(net_profit)`
  - `avg_profit_win = mean(net_profit | net_profit > 0)`, nếu không có trade thắng → 0
  - `avg_loss_loss = mean(net_profit | net_profit < 0)`, nếu không có trade thua → 0
  - `best_trade = max(net_profit)`; `worst_trade = min(net_profit)` -> cần bổ sung kèm `symbol`, `side`, `date`

## Feature 2: Chỉ số hiệu suất
- **profit_factor**:  |avg_profit_win| / |avg_loss_loss| nếu `avg_loss_loss` ≠ 0 ngược lại `0`
- **Expectancy**: EXP = 
- **Tổng pips**: pip
- **Avg pips per trade**: pip
- **Max drawdown**:

## Feature 3: Equity & Drawdown chi tiết