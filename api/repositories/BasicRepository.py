import os

class BasicRepository:
    def helloa(self):
        return {"message": "API funcionando 🚀 sim"}

    def hello(self):
        return {"message": "API funcionando 🚀 "}

    def db_info(self):
        return {"database_url": os.getenv("DATABASE_URL")}