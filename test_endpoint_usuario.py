import requests
import json

# Configuración
base_url = "http://localhost:8000"

def test_endpoint_usuario():
    print("🚀 PROBANDO ENDPOINT DE INGRESOS POR VENDEDOR/USUARIO")
    print("=" * 60)
    
    # 1. Probar histórico completo de un usuario específico
    print("\n1️⃣ Probando HISTÓRICO COMPLETO por vendedor...")
    try:
        # Cambiar el user_id según los usuarios que tengas en tu base de datos
        user_id = 1
        response = requests.get(f"{base_url}/transactions/ingresos-totales-usuario/?user_id={user_id}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Histórico por vendedor funcionando")
            print(f"👤 Vendedor ID: {data['user_id']}")
            print(f"📧 Email: {data['usuario_email']}")
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
        elif response.status_code == 404:
            print(f"❌ Vendedor con ID {user_id} no encontrado")
            print("💡 Prueba con un user_id que exista en tu base de datos")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al hacer la petición: {e}")

    # 2. Probar rango de fechas específico para un usuario
    print("\n2️⃣ Probando RANGO DE FECHAS por vendedor...")
    try:
        user_id = 1
        response = requests.get(f"{base_url}/transactions/ingresos-totales-usuario/?user_id={user_id}&fecha_inicio=2024-01-01&fecha_fin=2024-01-31")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Rango de fechas por vendedor funcionando")
            print(f"👤 Vendedor ID: {data['user_id']}")
            print(f"📧 Email: {data['usuario_email']}")
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
        elif response.status_code == 404:
            print(f"❌ Usuario con ID {user_id} no encontrado")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al hacer la petición: {e}")

    # 3. Probar rango de fechas más corto para un usuario
    print("\n3️⃣ Probando RANGO CORTO por vendedor...")
    try:
        user_id = 1
        response = requests.get(f"{base_url}/transactions/ingresos-totales-usuario/?user_id={user_id}&fecha_inicio=2024-01-01&fecha_fin=2024-01-15")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Rango corto por vendedor funcionando")
            print(f"👤 Vendedor ID: {data['user_id']}")
            print(f"📧 Email: {data['usuario_email']}")
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
        elif response.status_code == 404:
            print(f"❌ Usuario con ID {user_id} no encontrado")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al hacer la petición: {e}")

    # 4. Probar con usuario que no existe
    print("\n4️⃣ Probando VENDEDOR INEXISTENTE...")
    try:
        user_id = 99999  # Usuario que no existe
        response = requests.get(f"{base_url}/transactions/ingresos-totales-usuario/?user_id={user_id}")
        
        if response.status_code == 404:
            print("✅ Manejo de vendedor inexistente funcionando")
            print(f"❌ Error: {response.json()['detail']}")
        else:
            print(f"❌ Error inesperado: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al hacer la petición: {e}")

    # 5. Probar error de fechas incompletas
    print("\n5️⃣ Probando ERROR - Solo fecha inicio...")
    try:
        user_id = 1
        response = requests.get(f"{base_url}/transactions/ingresos-totales-usuario/?user_id={user_id}&fecha_inicio=2024-01-01")
        
        if response.status_code == 400:
            print("✅ Validación de fechas funcionando")
            print(f"❌ Error: {response.json()['detail']}")
        else:
            print(f"❌ Error inesperado: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al hacer la petición: {e}")

    # 6. Probar error de formato de fecha
    print("\n6️⃣ Probando ERROR - Formato de fecha inválido...")
    try:
        user_id = 1
        response = requests.get(f"{base_url}/transactions/ingresos-totales-usuario/?user_id={user_id}&fecha_inicio=2024/01/01&fecha_fin=2024/01/31")
        
        if response.status_code == 400:
            print("✅ Validación de formato de fecha funcionando")
            print(f"❌ Error: {response.json()['detail']}")
        else:
            print(f"❌ Error inesperado: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al hacer la petición: {e}")

    print("\n" + "=" * 60)
    print("🏁 PRUEBAS COMPLETADAS")
    print("💡 Recuerda cambiar el user_id por uno que exista en tu base de datos")
    print("💡 El user_id debe ser el ID de un vendedor (seller) en la tabla users")

if __name__ == "__main__":
    test_endpoint_usuario() 