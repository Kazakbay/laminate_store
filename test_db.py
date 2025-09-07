from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost:5432/laminate_store"

try:
    engine = create_engine(DATABASE_URL, echo=True)
    with engine.connect() as conn:
        print("✅ Connection successful:", conn)
except Exception as e:
    print("❌ Error:", e)