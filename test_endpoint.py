import requests
import json
from datetime import datetime

def test_ingresos_endpoint():
    """Script para probar el endpoint de ingresos totales"""
    
    # URL base del servidor
    base_url = "http://localhost:8000"
    
    # Probar el endpoint principal
    print("🔍 Probando conexión al servidor...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Servidor funcionando correctamente")
            print(f"Respuesta: {response.json()}")
        else:
            print(f"❌ Error en el servidor: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor. Asegúrate de que esté corriendo en http://localhost:8000")
        return
    
    print("\n" + "="*60)
    print("🧪 PRUEBAS DEL ENDPOINT DE INGRESOS TOTALES")
    print("="*60)
    
    # 1. Probar histórico completo (sin parámetros)
    print("\n1️⃣ Probando HISTÓRICO COMPLETO...")
    try:
        response = requests.get(f"{base_url}/transactions/ingresos-totales/")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Histórico completo funcionando")
            print(f"📋 Título: {data['titulo_periodo']}")
            print(f"💰 Total de ingresos: ${data['total_ingresos']:,.2f}")
            print(f"💵 Total de ganancias (15%): ${data['total_ganancias']:,.2f}")
            print(f"💸 Total de comisión (5%): ${data['total_comision']:,.2f}")
            print(f"📈 Cantidad de evidencias: {data['cantidad_evidencias']}")
            print(f"📊 Estadísticas de ventas:")
            print(f"   • Total ventas: {data['estadisticas_ventas']['total_ventas']}")
            print(f"   • Pending: {data['estadisticas_ventas']['pending']}")
            print(f"   • Approved: {data['estadisticas_ventas']['approved']}")
            print(f"   • Incompleta: {data['estadisticas_ventas']['incompleta']}")
            print(f"   • Rejected: {data['estadisticas_ventas']['rejected']}")
            print(f"   • Terminado: {data['estadisticas_ventas']['terminado']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al hacer la petición: {e}")
    
    # 2. Probar rango de fechas específico
    print("\n2️⃣ Probando RANGO DE FECHAS (Enero 2024)...")
    try:
        response = requests.get(f"{base_url}/transactions/ingresos-totales/?fecha_inicio=2024-01-01&fecha_fin=2024-01-31")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Rango de fechas funcionando")
            print(f"📋 Título: {data['titulo_periodo']}")
            print(f"📅 Fecha inicio: {data['fecha_inicio']}")
            print(f"📅 Fecha fin: {data['fecha_fin']}")
            print(f"💰 Total de ingresos: ${data['total_ingresos']:,.2f}")
            print(f"💵 Total de ganancias (15%): ${data['total_ganancias']:,.2f}")
            print(f"💸 Total de comisión (5%): ${data['total_comision']:,.2f}")
            print(f"📈 Cantidad de evidencias: {data['cantidad_evidencias']}")
            print(f"📊 Estadísticas de ventas:")
            print(f"   • Total ventas: {data['estadisticas_ventas']['total_ventas']}")
            print(f"   • Pending: {data['estadisticas_ventas']['pending']}")
            print(f"   • Approved: {data['estadisticas_ventas']['approved']}")
            print(f"   • Incompleta: {data['estadisticas_ventas']['incompleta']}")
            print(f"   • Rejected: {data['estadisticas_ventas']['rejected']}")
            print(f"   • Terminado: {data['estadisticas_ventas']['terminado']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al hacer la petición: {e}")
    
    # 3. Probar rango de fechas más corto
    print("\n3️⃣ Probando RANGO CORTO (Primera quincena Enero 2024)...")
    try:
        response = requests.get(f"{base_url}/transactions/ingresos-totales/?fecha_inicio=2024-01-01&fecha_fin=2024-01-15")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Rango corto funcionando")
            print(f"📋 Título: {data['titulo_periodo']}")
            print(f"📅 Fecha inicio: {data['fecha_inicio']}")
            print(f"📅 Fecha fin: {data['fecha_fin']}")
            print(f"💰 Total de ingresos: ${data['total_ingresos']:,.2f}")
            print(f"💵 Total de ganancias (15%): ${data['total_ganancias']:,.2f}")
            print(f"💸 Total de comisión (5%): ${data['total_comision']:,.2f}")
            print(f"📈 Cantidad de evidencias: {data['cantidad_evidencias']}")
            print(f"📊 Estadísticas de ventas:")
            print(f"   • Total ventas: {data['estadisticas_ventas']['total_ventas']}")
            print(f"   • Pending: {data['estadisticas_ventas']['pending']}")
            print(f"   • Approved: {data['estadisticas_ventas']['approved']}")
            print(f"   • Incompleta: {data['estadisticas_ventas']['incompleta']}")
            print(f"   • Rejected: {data['estadisticas_ventas']['rejected']}")
            print(f"   • Terminado: {data['estadisticas_ventas']['terminado']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al hacer la petición: {e}")
    
    # 4. Probar error - solo fecha inicio
    print("\n4️⃣ Probando ERROR - Solo fecha inicio...")
    try:
        response = requests.get(f"{base_url}/transactions/ingresos-totales/?fecha_inicio=2024-01-01")
        
        if response.status_code == 400:
            print("✅ Error manejado correctamente")
            print(f"📋 Mensaje: {response.json()['detail']}")
        else:
            print(f"❌ Error inesperado: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al hacer la petición: {e}")
    
    # 5. Probar error - fechas invertidas
    print("\n5️⃣ Probando ERROR - Fechas invertidas...")
    try:
        response = requests.get(f"{base_url}/transactions/ingresos-totales/?fecha_inicio=2024-01-31&fecha_fin=2024-01-01")
        
        if response.status_code == 400:
            print("✅ Error manejado correctamente")
            print(f"📋 Mensaje: {response.json()['detail']}")
        else:
            print(f"❌ Error inesperado: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al hacer la petición: {e}")
    
    # 6. Probar con usuario específico (histórico completo)
    print("\n6️⃣ Probando CON USUARIO ESPECÍFICO (histórico completo)...")
    try:
        # Cambiar el user_id según los usuarios que tengas en tu base de datos
        user_id = 1
        response = requests.get(f"{base_url}/transactions/ingresos-totales/?user_id={user_id}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Filtro por usuario funcionando")
            print(f"📋 Título: {data['titulo_periodo']}")
            if 'usuario' in data:
                print(f"👤 Usuario: {data['usuario']['nombre']} ({data['usuario']['email']})")
            print(f"💰 Total de ingresos: ${data['total_ingresos']:,.2f}")
            print(f"💵 Total de ganancias (15%): ${data['total_ganancias']:,.2f}")
            print(f"💸 Total de comisión (5%): ${data['total_comision']:,.2f}")
            print(f"📈 Cantidad de evidencias: {data['cantidad_evidencias']}")
            print(f"📊 Estadísticas de ventas:")
            print(f"   • Total ventas: {data['estadisticas_ventas']['total_ventas']}")
            print(f"   • Pending: {data['estadisticas_ventas']['pending']}")
            print(f"   • Approved: {data['estadisticas_ventas']['approved']}")
            print(f"   • Incompleta: {data['estadisticas_ventas']['incompleta']}")
            print(f"   • Rejected: {data['estadisticas_ventas']['rejected']}")
            print(f"   • Terminado: {data['estadisticas_ventas']['terminado']}")
        elif response.status_code == 404:
            print(f"❌ Usuario con ID {user_id} no encontrado")
            print("💡 Prueba con un user_id que exista en tu base de datos")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al hacer la petición: {e}")

    # 7. Probar con usuario específico y rango de fechas
    print("\n7️⃣ Probando CON USUARIO Y RANGO DE FECHAS...")
    try:
        user_id = 1
        response = requests.get(f"{base_url}/transactions/ingresos-totales/?user_id={user_id}&fecha_inicio=2024-01-01&fecha_fin=2024-03-31")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Usuario con rango de fechas funcionando")
            print(f"📋 Título: {data['titulo_periodo']}")
            if 'usuario' in data:
                print(f"👤 Usuario: {data['usuario']['nombre']} ({data['usuario']['email']})")
            print(f"📅 Fecha inicio: {data['fecha_inicio']}")
            print(f"📅 Fecha fin: {data['fecha_fin']}")
            print(f"💰 Total de ingresos: ${data['total_ingresos']:,.2f}")
            print(f"💵 Total de ganancias: ${data['total_ganancias']:,.2f}")
            print(f"💸 Total de comisión: ${data['total_comision']:,.2f}")
        elif response.status_code == 404:
            print(f"❌ Usuario con ID {user_id} no encontrado")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al hacer la petición: {e}")

    # 8. Probar con usuario inexistente
    print("\n8️⃣ Probando USUARIO INEXISTENTE...")
    try:
        user_id = 99999  # Usuario que no existe
        response = requests.get(f"{base_url}/transactions/ingresos-totales/?user_id={user_id}")
        
        if response.status_code == 404:
            print("✅ Manejo de usuario inexistente funcionando")
            print(f"❌ Error: {response.json()['detail']}")
        else:
            print(f"❌ Error inesperado: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al hacer la petición: {e}")
    
    print("\n" + "="*60)
    print("✅ PRUEBAS COMPLETADAS")
    print("💡 El endpoint ahora soporta filtro opcional por usuario")
    print("="*60)

if __name__ == "__main__":
    test_ingresos_endpoint() 