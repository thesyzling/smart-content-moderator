from app.database import Base, engine
import app.models  # ensure all models are imported

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("All tables created.")
