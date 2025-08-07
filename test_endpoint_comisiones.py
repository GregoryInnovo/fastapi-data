import requests
import json

# Configuración
base_url = "http://localhost:8000"

def test_endpoint_comisiones():
    print("🚀 PROBANDO ENDPOINT DE COMISIONES POR USUARIO")
    print("=" * 60)
    
    # 1. Probar rango de 3 meses (Enero a Marzo 2024)
    print("\n1️⃣ Probando COMISIONES POR USUARIO (Enero a Marzo 2024)...")
    try:
        response = requests.get(f"{base_url}/transactions/comisiones-por-usuario/?fecha_inicio=2024-01-01&fecha_fin=2024-03-31")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Comisiones por usuario funcionando")
            print(f"📅 Rango: {data['rango_fechas']['fecha_inicio']} a {data['rango_fechas']['fecha_fin']}")
            print(f"👥 Cantidad de usuarios: {data['cantidad_usuarios']}")
            
            if data['cantidad_usuarios'] > 0:
                print(f"\n🏆 RANKING DE COMISIONES (ordenado de mayor a menor):")
                for i, usuario in enumerate(data['usuarios'], 1):
                    print(f"\n   {i}. 👤 {usuario['nombre']} (ID: {usuario['user_id']})")
                    print(f"      📧 Email: {usuario['email']}")
                    print(f"      💰 Ingresos: ${usuario['ingresos']:,.2f}")
                    print(f"      💵 Ganancias (15%): ${usuario['ganancias']:,.2f}")
                    print(f"      💸 Comisión (5%): ${usuario['comision']:,.2f}")
                    print(f"      📈 Evidencias: {usuario['cantidad_evidencias']}")
                    print(f"      📊 Ventas: {usuario['estadisticas_ventas']['total_ventas']} total")
                    print(f"         • Pending: {usuario['estadisticas_ventas']['pending']}")
                    print(f"         • Approved: {usuario['estadisticas_ventas']['approved']}")
                    print(f"         • Incompleta: {usuario['estadisticas_ventas']['incompleta']}")
                    print(f"         • Rejected: {usuario['estadisticas_ventas']['rejected']}")
                    print(f"         • Terminado: {usuario['estadisticas_ventas']['terminado']}")
                
                print(f"\n🏆 TOTAL GENERAL:")
                total = data['total_general']
                print(f"   💰 Ingresos totales: ${total['ingresos']:,.2f}")
                print(f"   💵 Ganancias totales: ${total['ganancias']:,.2f}")
                print(f"   💸 Comisión total: ${total['comision']:,.2f}")
                print(f"   📈 Evidencias totales: {total['cantidad_evidencias']}")
                print(f"   📊 Ventas totales: {total['total_ventas']}")
            else:
                print("📭 No hay usuarios con transacciones en este período")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📄 Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

    # 2. Probar rango de 6 meses (Enero a Junio 2024)
    print("\n2️⃣ Probando RANGO DE 6 MESES (Enero a Junio 2024)...")
    try:
        response = requests.get(f"{base_url}/transactions/comisiones-por-usuario/?fecha_inicio=2024-01-01&fecha_fin=2024-06-30")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Rango de 6 meses funcionando")
            print(f"📅 Rango: {data['rango_fechas']['fecha_inicio']} a {data['rango_fechas']['fecha_fin']}")
            print(f"👥 Cantidad de usuarios: {data['cantidad_usuarios']}")
            
            if data['cantidad_usuarios'] > 0:
                print(f"\n📈 RESUMEN DE COMISIONES:")
                for usuario in data['usuarios']:
                    print(f"   👤 {usuario['nombre']}: ${usuario['comision']:,.2f} | ${usuario['ingresos']:,.2f} ingresos")
                
                total = data['total_general']
                print(f"\n🏆 TOTAL ACUMULADO: ${total['comision']:,.2f} comisiones")
            
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

    # 3. Probar rango de 1 mes (Febrero 2024)
    print("\n3️⃣ Probando RANGO DE 1 MES (Febrero 2024)...")
    try:
        response = requests.get(f"{base_url}/transactions/comisiones-por-usuario/?fecha_inicio=2024-02-01&fecha_fin=2024-02-29")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Rango de 1 mes funcionando")
            print(f"📅 Rango: {data['rango_fechas']['fecha_inicio']} a {data['rango_fechas']['fecha_fin']}")
            print(f"👥 Cantidad de usuarios: {data['cantidad_usuarios']}")
            
            if data['cantidad_usuarios'] > 0:
                print(f"\n📈 COMISIONES DE FEBRERO:")
                for usuario in data['usuarios']:
                    print(f"   👤 {usuario['nombre']}: ${usuario['comision']:,.2f}")
            
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

    # 4. Probar rango que cruza años (Diciembre 2023 a Enero 2024)
    print("\n4️⃣ Probando RANGO CRUZANDO AÑOS (Diciembre 2023 a Enero 2024)...")
    try:
        response = requests.get(f"{base_url}/transactions/comisiones-por-usuario/?fecha_inicio=2023-12-01&fecha_fin=2024-01-31")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Rango cruzando años funcionando")
            print(f"📅 Rango: {data['rango_fechas']['fecha_inicio']} a {data['rango_fechas']['fecha_fin']}")
            print(f"👥 Cantidad de usuarios: {data['cantidad_usuarios']}")
            
            if data['cantidad_usuarios'] > 0:
                print(f"\n📈 COMISIONES CRUZANDO AÑOS:")
                for usuario in data['usuarios']:
                    print(f"   👤 {usuario['nombre']}: ${usuario['comision']:,.2f}")
            
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

    # 5. Probar error - fechas inválidas
    print("\n5️⃣ Probando ERROR - FECHAS INVÁLIDAS...")
    try:
        response = requests.get(f"{base_url}/transactions/comisiones-por-usuario/?fecha_inicio=2024-03-31&fecha_fin=2024-01-01")
        
        if response.status_code == 400:
            print("✅ Manejo de fechas inválidas funcionando")
            print(f"❌ Error: {response.json()['detail']}")
        else:
            print(f"❌ Error inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

    # 6. Probar período sin datos
    print("\n6️⃣ Probando PERÍODO SIN DATOS (Año 2020)...")
    try:
        response = requests.get(f"{base_url}/transactions/comisiones-por-usuario/?fecha_inicio=2020-01-01&fecha_fin=2020-12-31")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Manejo de período sin datos funcionando")
            print(f"👥 Cantidad de usuarios: {data['cantidad_usuarios']}")
            print(f"📭 Respuesta: {data['usuarios']}")
            
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

    print("\n" + "=" * 60)
    print("🏁 PRUEBAS COMPLETADAS")
    print("💡 El endpoint calcula comisiones por usuario y las ordena de mayor a menor")
    print("💡 Incluye detalles completos de cada usuario y totales generales")

if __name__ == "__main__":
    test_endpoint_comisiones() 