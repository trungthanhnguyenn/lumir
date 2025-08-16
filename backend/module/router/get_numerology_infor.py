from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, validator
from typing import Optional
from backend.module.numorology.cal_num import CalNum
from datetime import datetime

router = APIRouter(prefix="/api/v1", tags=["numerology"])

class NumerologyRequest(BaseModel):
    full_name: str
    date_of_birth: str
    current_date: Optional[str] = None
    
    @validator('full_name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Tên không được để trống')
        if len(v.strip()) < 2:
            raise ValueError('Tên phải có ít nhất 2 ký tự')
        return v.strip()
    
    @validator('date_of_birth')
    def validate_dob(cls, v):
        try:
            datetime.strptime(v, '%d/%m/%Y')
            return v
        except ValueError:
            raise ValueError('Ngày sinh phải có định dạng DD/MM/YYYY')
    
    @validator('current_date')
    def validate_current_date(cls, v):
        if v is not None:
            try:
                datetime.strptime(v, '%d/%m/%Y')
                return v
            except ValueError:
                raise ValueError('Ngày hiện tại phải có định dạng DD/MM/YYYY')
        return v

class NumerologyResponse(BaseModel):
    success: bool
    data: dict
    message: str = "Thành công"

@router.post("/numerology/calculate", response_model=NumerologyResponse)
async def calculate_numerology(request: NumerologyRequest):
    """
    Tính toán thông tin thần số học dựa trên tên và ngày sinh
    """
    try:
        # Tạo calculator instance
        calculator = CalNum(
            dob=request.date_of_birth,
            name=request.full_name,
            current_date=request.current_date
        )
        
        # Lấy kết quả tính toán
        result = calculator.get_personal_date_num()
        
        return NumerologyResponse(
            success=True,
            data={
                "input": {
                    "full_name": request.full_name,
                    "date_of_birth": request.date_of_birth,
                    "current_date": request.current_date
                },
                "pwi_indices": result
            },
            message="Tính toán thần số học thành công"
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi server: {str(e)}")

@router.get("/numerology/health")
async def health_check():
    """Kiểm tra trạng thái endpoint"""
    return {"status": "healthy", "service": "numerology-api"}