from google import genai
from google.genai import types

# Khởi tạo client. SDK sẽ tự động tìm và sử dụng biến môi trường GEMINI_API_KEY
client = genai.Client()


def analyze_sentiment_logic(text: str) -> str:
    # Ép AI chỉ trả về đúng 1 trong 3 từ khóa để backend dễ xử lý
    prompt = f"Phân tích cảm xúc của đoạn văn bản sau. Chỉ trả về đúng 1 từ duy nhất trong 3 từ (Positive, Negative, Neutral). Văn bản: '{text}'"

    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.0,  # Đặt temperature = 0 để câu trả lời có tính xác định cao nhất
            )
        )

        # Xóa khoảng trắng thừa hoặc ký tự xuống dòng
        result = response.text.strip()

        # Bộ lọc an toàn: Nếu AI trả về câu dài ngoằng sai yêu cầu, mặc định trả về Neutral
        if result not in ["Positive", "Negative", "Neutral"]:
            print(f"[Cảnh báo] AI trả về sai định dạng: {result}")
            return "Neutral"

        return result
    except Exception as e:
        print(f"[Lỗi] Không thể kết nối tới Gemini API: {e}")
        return "Neutral"  # Trả về Neutral để app không bị sập (crash) khi có lỗi mạng