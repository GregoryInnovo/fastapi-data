from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user_router, transaction_router, event_router, auth_router, cuentas_recaudo_router

app = FastAPI()

# # Configuración de CORS
# origins = [
#     #"http://localhost:3000",  # Permitir acceso desde localhost en el puerto 3000
#     #"http://localhost:5173",
#     #"http://localhost:3000",
#     #"http://127.0.0.1:5173",
#     "http://0.0.0.0:3000",
#     "http://0.0.0.0:5173",
#     "https://0.0.0.0:3000"
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Lista de orígenes permitidos
    allow_credentials=False,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

app.include_router(user_router.router)
app.include_router(transaction_router.router)
app.include_router(event_router.router)
app.include_router(auth_router.router)
app.include_router(cuentas_recaudo_router.router)

@app.get("/")
def root():
    return {"message": "API de Gestión de Ventas Activa"}
