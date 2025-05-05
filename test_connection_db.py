import psycopg2

# Configuración de conexión
#DATABASE_URL = "postgresql+psycopg2://postgres:GUSTAVO316_@awsrds164.cn4gky80egt7.us-east-1.rds.amazonaws.com:5432/postgres"
try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="GUSTAVO316_",
        host="database-agencia-test.cqxuac6ekcdy.us-east-1.rds.amazonaws.com",
        port="5432"
    )
    print("✅ Conexión exitosa a la base de datos")
except Exception as e:
    print("❌ Error al conectar:", e)
