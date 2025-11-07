from fastapi import FastAPI
from routes import router
from database import Base, engine
import models

# Создаем все таблицы (если их ещё нет)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AAA Auth Service")
app.include_router(router)
