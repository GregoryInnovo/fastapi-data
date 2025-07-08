import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Datos de conexión
DATABASE_URL = (os.getenv("DB_URL_CONNECTION_INFO"))


#"postgresql+psycopg2://postgres:GUSTAVO316_@awsrds164.cn4gky80egt7.us-east-1.rds.amazonaws.com:5432/postgres"

#database-agencia-test.cqxuac6ekcdy.us-east-1.rds.amazonaws.com
# Crear el motor de conexión
engine = create_engine(DATABASE_URL)

# Crear la sesión de conexión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Prueba de conexión
#try:
#    with engine.connect() as connection:
#        print("Conexión a la base de datos exitosa")
#except Exception as e:
#    print(f"Error al conectar: {e}")
# Dependencia para obtener una sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
