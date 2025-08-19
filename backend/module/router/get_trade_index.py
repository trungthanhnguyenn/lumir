from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pydantic import BaseModel
from typing import Optional, Dict, Any, List, Tuple
import pandas as pd
import io

from backend.module.trade_index.calculate_trade import calculate_trade_index

router = APIRouter(prefix="/api/v1", tags=["trade-index"])


class TradeIndexResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    message: str = "Thành công"


def _head_tail(seq: List[Any], n: int = 5) -> Dict[str, Any]:
    return {
        "len": len(seq),
        "head": seq[:n],
        "tail": seq[-n:] if len(seq) > n else []
    }


def _top_items(d: Dict[str, Dict[str, Any]], by_key: str, k: int = 5) -> List[Tuple[str, Dict[str, Any]]]:
    items = list(d.items())
    try:
        return sorted(items, key=lambda kv: kv[1].get(by_key, 0), reverse=True)[:k]
    except Exception:
        return items[:k]


def _compact_result(res: Dict[str, Any]) -> Dict[str, Any]:
    # Summary subset
    summary_keys = [
        "trades", "net_profit", "gross_profit", "total_fees", "win_rate_pct",
        "profit_factor", "avg_profit_per_trade", "max_drawdown_pct", "max_consecutive_losses"
    ]
    summary = {k: res.get(k) for k in summary_keys}

    # Analyses (compact)
    time_analysis = res.get("time_analysis", {})
    symbol_analysis = res.get("symbol_analysis", {})
    side_analysis = res.get("side_analysis", {})

    top_hours = _top_items(time_analysis, by_key="profit", k=5) if isinstance(time_analysis, dict) else []
    top_symbols = _top_items(symbol_analysis, by_key="profit", k=5) if isinstance(symbol_analysis, dict) else []

    # Equity/DD compact
    equity = res.get("equity", {})
    rb = equity.get("rb", [])
    dd_pct = equity.get("dd_pct", [])

    # Monthly compact
    monthly = res.get("monthly") or {}
    if monthly:
        months = monthly.get("periods", [])
        m_preview = {
            "periods": months[:3] + (months[-3:] if len(months) > 3 else []),
            "varpc": (monthly.get("varpc", [])[:3] + (monthly.get("varpc", [])[-3:] if len(monthly.get("varpc", [])) > 3 else [])),
            "dividend": (monthly.get("dividend", [])[:3] + (monthly.get("dividend", [])[-3:] if len(monthly.get("dividend", [])) > 3 else [])),
            "rt": (monthly.get("rt", [])[:3] + (monthly.get("rt", [])[-3:] if len(monthly.get("rt", [])) > 3 else [])),
            "index": (monthly.get("index", [])[:3] + (monthly.get("index", [])[-3:] if len(monthly.get("index", [])) > 3 else [])),
        }
    else:
        m_preview = None

    return {
        "summary": summary,
        "analyses": {
            "top_hours_by_profit": top_hours,
            "top_symbols_by_profit": top_symbols,
            "side_analysis": side_analysis,
        },
        "equity": {
            "rb": _head_tail(rb, 5),
            "drawdown_pct": _head_tail(dd_pct, 5),
        },
        "behavioral": res.get("behavioral", {}),
        "risk_kpi": res.get("risk_kpi", {}),
        "monthly": m_preview,
    }


@router.post("/trade-index/calculate", response_model=TradeIndexResponse)
async def calculate_trade_index_api(
    file: UploadFile = File(...),
    sheet_name: Optional[str] = Form(None)
):
    """
    Tính trade index từ file upload (.xlsx hoặc .csv).
    Trả về kết quả đã rút gọn, dễ xử lý.
    """
    try:
        content = await file.read()
        buffer = io.BytesIO(content)

        # Load DataFrame
        filename = (file.filename or "").lower()
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            df = pd.read_excel(buffer, sheet_name=sheet_name or 0)
        elif filename.endswith(".csv"):
            # Attempt utf-8 first, fallback latin-1
            try:
                df = pd.read_csv(io.BytesIO(content))
            except UnicodeDecodeError:
                df = pd.read_csv(io.BytesIO(content), encoding="latin-1")
        else:
            raise HTTPException(status_code=400, detail="Định dạng tệp không hỗ trợ. Chỉ hỗ trợ .xlsx, .xls, .csv")

        # Calculate and compact
        raw_result = calculate_trade_index(df)
        compact = _compact_result(raw_result)

        return TradeIndexResponse(success=True, data=compact)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý: {e}")


@router.get("/trade-index/health")
async def trade_index_health():
    return {"status": "healthy", "service": "trade-index"}


