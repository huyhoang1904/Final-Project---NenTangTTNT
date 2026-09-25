from dotenv import load_dotenv
# Load các biến môi trường từ file .env vào hệ thống
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from ai_service import analyze_sentiment_logic
from db_module import save_request_history

app = FastAPI(title="Sentiment Analysis API")

# Cấu hình thư mục chứa giao diện HTML
templates = Jinja2Templates(directory="templates")

# Quy định định dạng request và response
class AnalyzeRequest(BaseModel):
        text: str

class AnalyzeResponse(BaseModel):
        original_text: str
        sentiment: str

# Route hiển thị giao diện UI
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

# Route xử lý logic phân tích cảm xúc
@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(request: AnalyzeRequest):
        result = analyze_sentiment_logic(request.text)
        save_request_history(request.text, result)

        return AnalyzeResponse(
                original_text=request.text,
                sentiment=result
        )