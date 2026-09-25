import psycopg2
import os


def get_connection():
    # Lấy chuỗi kết nối từ file .env
    db_url = os.getenv("DATABASE_URL")
    return psycopg2.connect(db_url)


def create_table_if_not_exists():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Tạo bảng lưu lịch sử
        cursor.execute("""
           CREATE TABLE IF NOT EXISTS request_history (
                id SERIAL PRIMARY KEY,
                input_text TEXT NOT NULL,
                sentiment_result VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("[DB INIT] Đã kiểm tra/khởi tạo bảng request_history.")
    except Exception as e:
        print(f"[DB ERROR] Lỗi khởi tạo bảng: {e}")


# Chạy hàm tạo bảng ngay khi module này được import vào app.py
create_table_if_not_exists()


def save_request_history(text: str, sentiment: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO request_history (input_text, sentiment_result) VALUES (%s, %s)"
        cursor.execute(sql, (text, sentiment))

        conn.commit()
        cursor.close()
        conn.close()
        print(f"[DB SUCCESS] Đã lưu '{sentiment}' vào CSDL.")
        return True
    except Exception as e:
        print(f"[DB ERROR] Không thể lưu dữ liệu: {e}")
        return False