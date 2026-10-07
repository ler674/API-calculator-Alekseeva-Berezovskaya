from typing import Literal, Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
import math


# Создание приложения FastAPI
app = FastAPI(
    title="API-калькулятор",
    description="API-калькулятор Алексеева, Березовская",
    version="1.0.0",
)


# Модели запроса и ответа
class CalcRequest(BaseModel):
    """Тело запроса для POST /calculate."""
    operation: Literal["add", "subtract", "multiply", "divide", "power", "sqrt"] = Field(
        ..., description="Арифметическая операция"
    )
    a: float = Field(..., description="Первый операнд")
    b: Optional[float] = Field(
        None, description="Второй операнд (не требуется для sqrt)"
    )

class CalcResponse(BaseModel):
    """Единый формат ответа."""
    operation: str
    a: float
    b: Optional[float] = None
    result: float


@app.get("/health", tags=["системные"])
async def health() -> dict:
    return {"status": "ok"}

@app.get("/version", tags=["системные"])
async def version() -> dict:
    return {"version": app.version}


# POST
@app.post("/calculate", response_model=CalcResponse, tags=["вычисления"])
async def calculate(req: CalcRequest) -> CalcResponse:
    """Выполняет операцию, указанную в теле запроса."""
    a = req.a
    b = req.b

    if req.operation == "add":
        if b is None:
            raise HTTPException(status_code=400, detail="Операция 'Сложение' требует второй операнд 'b'")
        result = a + b

    elif req.operation == "subtract":
        if b is None:
            raise HTTPException(status_code=400, detail="Операция 'Вычитание' требует второй операнд 'b'")
        result = a - b

    elif req.operation == "multiply":
        if b is None:
            raise HTTPException(status_code=400, detail="Операция 'Умножение' требует второй операнд 'b'")
        result = a * b

    elif req.operation == "divide":
        if b is None:
            raise HTTPException(status_code=400, detail="Операция 'Деление' требует второй операнд 'b'")
        if b == 0:
            raise HTTPException(status_code=400, detail="Нельзя делить на ноль")
        result = a / b

    elif req.operation == "power":
        if b is None:
            raise HTTPException(status_code=400, detail="Операция 'Возведение в степень' требует второй операнд 'b'")
        try:
            result = float(a ** b)
        except OverflowError:
            raise HTTPException(status_code=400, detail="Слишком большой результат")

    elif req.operation == "sqrt":
        if a < 0:
            raise HTTPException(status_code=400, detail="Нельзя извлечь корень из отрицательного числа")
        result = math.sqrt(a)

    else:
        raise HTTPException(status_code=400, detail=f"Неизвестная операция: {req.operation}")

    return CalcResponse(operation=req.operation, a=a, b=b, result=result)


# GET
@app.get("/add", response_model=CalcResponse, tags=["вычисления"])
async def add(
    a: float = Query(..., description="Первый операнд"),
    b: float = Query(..., description="Второй операнд"),
) -> CalcResponse:
    """Сложение"""
    result = a + b
    return CalcResponse(operation="add", a=a, b=b, result=result)

@app.get("/subtract", response_model=CalcResponse, tags=["вычисления"])
async def subtract(
    a: float = Query(..., description="Первый операнд"),
    b: float = Query(..., description="Второй операнд"),
) -> CalcResponse:
    """Вычитание"""
    result = a - b
    return CalcResponse(operation="subtract", a=a, b=b, result=result)

@app.get("/multiply", response_model=CalcResponse, tags=["вычисления"])
async def multiply(
    a: float = Query(..., description="Первый операнд"),
    b: float = Query(..., description="Второй операнд"),
) -> CalcResponse:
    """Умножение"""
    result = a * b
    return CalcResponse(operation="multiply", a=a, b=b, result=result)

@app.get("/divide", response_model=CalcResponse, tags=["вычисления"])
async def divide(
    a: float = Query(..., description="Первый операнд"),
    b: float = Query(..., description="Второй операнд"),
) -> CalcResponse:
    """Деление"""
    if b == 0:
        raise HTTPException(status_code=400, detail="Деление на ноль недопустимо")
    result = a / b
    return CalcResponse(operation="divide", a=a, b=b, result=result)

@app.get("/power", response_model=CalcResponse, tags=["вычисления"])
async def power(
    a: float = Query(..., description="Основание"),
    b: float = Query(..., description="Показатель степени"),
) -> CalcResponse:
    """Возведение в степень"""
    try:
        result = float(a ** b)
    except OverflowError:
        raise HTTPException(status_code=400, detail="Результат слишком велик")
    return CalcResponse(operation="power", a=a, b=b, result=result)

@app.get("/sqrt", response_model=CalcResponse, tags=["вычисления"])
async def sqrt(
    a: float = Query(..., description="Число, из которого берётся корень"),
) -> CalcResponse:
    """Квадратный корень"""
    if a < 0:
        raise HTTPException(status_code=400, detail="Нельзя извлечь корень из отрицательного числа")
    result = math.sqrt(a)
    return CalcResponse(operation="sqrt", a=a, result=result)