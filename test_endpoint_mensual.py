import requests
import json

# Configuración
base_url = "http://localhost:8000"

def test_endpoint_mensual():
    print("🚀 PROBANDO ENDPOINT DE INGRESOS MENSUALES")
    print("=" * 60)
    
    # 1. Probar rango de 3 meses (Enero a Marzo 2024)
    print("\n1️⃣ Probando RANGO DE 3 MESES (Enero a Marzo 2024)...")
    try:
        response = requests.get(f"{base_url}/transactions/ingresos-totales-mensual/?fecha_inicio=2024-01-01&fecha_fin=2024-03-31")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Rango de 3 meses funcionando")
            print(f"📅 Rango: {data['rango_fechas']['fecha_inicio']} a {data['rango_fechas']['fecha_fin']}")
            print(f"📊 Cantidad de meses: {data['cantidad_meses']}")
            
            print(f"\n📈 DATOS POR MES:")
            for i, mes in enumerate(data['datos_mensuales'], 1):
                print(f"\n   {i}. {mes['nombre_mes']} {mes['año']}:")
                print(f"      📅 Período: {mes['fecha_inicio']} a {mes['fecha_fin']}")
                print(f"      💰 Ingresos: ${mes['ingresos']:,.2f}")
                print(f"      💵 Ganancias (15%): ${mes['ganancias']:,.2f}")
                print(f"      💸 Comisión (5%): ${mes['comision']:,.2f}")
                print(f"      📈 Evidencias: {mes['cantidad_evidencias']}")
                print(f"      📊 Ventas: {mes['estadisticas_ventas']['total_ventas']} total")
                print(f"         • Pending: {mes['estadisticas_ventas']['pending']}")
                print(f"         • Approved: {mes['estadisticas_ventas']['approved']}")
                print(f"         • Incompleta: {mes['estadisticas_ventas']['incompleta']}")
                print(f"         • Rejected: {mes['estadisticas_ventas']['rejected']}")
                print(f"         • Terminado: {mes['estadisticas_ventas']['terminado']}")
            
            print(f"\n🏆 TOTAL ACUMULADO:")
            total = data['total_acumulado']
            print(f"   💰 Ingresos totales: ${total['ingresos']:,.2f}")
            print(f"   💵 Ganancias totales: ${total['ganancias']:,.2f}")
            print(f"   💸 Comisión total: ${total['comision']:,.2f}")
            print(f"   📈 Evidencias totales: {total['cantidad_evidencias']}")
            print(f"   📊 Ventas totales: {total['estadisticas_ventas']['total_ventas']}")
            print(f"      • Pending: {total['estadisticas_ventas']['pending']}")
            print(f"      • Approved: {total['estadisticas_ventas']['approved']}")
            print(f"      • Incompleta: {total['estadisticas_ventas']['incompleta']}")
            print(f"      • Rejected: {total['estadisticas_ventas']['rejected']}")
            print(f"      • Terminado: {total['estadisticas_ventas']['terminado']}")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📄 Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

    # 2. Probar rango de 6 meses (Enero a Junio 2024)
    print("\n2️⃣ Probando RANGO DE 6 MESES (Enero a Junio 2024)...")
    try:
        response = requests.get(f"{base_url}/transactions/ingresos-totales-mensual/?fecha_inicio=2024-01-01&fecha_fin=2024-06-30")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Rango de 6 meses funcionando")
            print(f"📅 Rango: {data['rango_fechas']['fecha_inicio']} a {data['rango_fechas']['fecha_fin']}")
            print(f"📊 Cantidad de meses: {data['cantidad_meses']}")
            
            print(f"\n📈 RESUMEN POR MES:")
            for mes in data['datos_mensuales']:
                print(f"   📅 {mes['nombre_mes']} {mes['año']}: ${mes['ingresos']:,.2f} | G: ${mes['ganancias']:,.2f} | C: ${mes['comision']:,.2f}")
            
            total = data['total_acumulado']
            print(f"\n🏆 TOTAL ACUMULADO: ${total['ingresos']:,.2f}")
            
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

    # 3. Probar rango de 1 mes (Febrero 2024)
    print("\n3️⃣ Probando RANGO DE 1 MES (Febrero 2024)...")
    try:
        response = requests.get(f"{base_url}/transactions/ingresos-totales-mensual/?fecha_inicio=2024-02-01&fecha_fin=2024-02-29")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Rango de 1 mes funcionando")
            print(f"📅 Rango: {data['rango_fechas']['fecha_inicio']} a {data['rango_fechas']['fecha_fin']}")
            print(f"📊 Cantidad de meses: {data['cantidad_meses']}")
            
            if data['datos_mensuales']:
                mes = data['datos_mensuales'][0]
                print(f"📈 {mes['nombre_mes']} {mes['año']}:")
                print(f"   💰 Ingresos: ${mes['ingresos']:,.2f}")
                print(f"   💵 Ganancias: ${mes['ganancias']:,.2f}")
                print(f"   💸 Comisión: ${mes['comision']:,.2f}")
            
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

    # 4. Probar rango que cruza años (Diciembre 2023 a Enero 2024)
    print("\n4️⃣ Probando RANGO CRUZANDO AÑOS (Diciembre 2023 a Enero 2024)...")
    try:
        response = requests.get(f"{base_url}/transactions/ingresos-totales-mensual/?fecha_inicio=2023-12-01&fecha_fin=2024-01-31")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Rango cruzando años funcionando")
            print(f"📅 Rango: {data['rango_fechas']['fecha_inicio']} a {data['rango_fechas']['fecha_fin']}")
            print(f"📊 Cantidad de meses: {data['cantidad_meses']}")
            
            print(f"\n📈 MESES INCLUIDOS:")
            for mes in data['datos_mensuales']:
                print(f"   📅 {mes['nombre_mes']} {mes['año']}: ${mes['ingresos']:,.2f}")
            
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

    # 5. Probar error - fechas inválidas
    print("\n5️⃣ Probando ERROR - FECHAS INVÁLIDAS...")
    try:
        response = requests.get(f"{base_url}/transactions/ingresos-totales-mensual/?fecha_inicio=2024-03-31&fecha_fin=2024-01-01")
        
        if response.status_code == 400:
            print("✅ Manejo de fechas inválidas funcionando")
            print(f"❌ Error: {response.json()['detail']}")
        else:
            print(f"❌ Error inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

    print("\n" + "=" * 60)
    print("🏁 PRUEBAS COMPLETADAS")
    print("💡 El endpoint desglosa automáticamente por mes y calcula totales acumulados")

if __name__ == "__main__":
    test_endpoint_mensual() 