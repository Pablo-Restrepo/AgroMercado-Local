"""
Script para poblar la base de datos de AgroMercado Local con datos de prueba.
Ejecutar con: python seed_database.py

Este script:
1. Registra usuarios productores-admin
2. Hace login para obtener tokens
3. Crea gremios
4. Espera a que los productores se sincronicen vía RabbitMQ
5. Registra productos para cada productor

IMPORTANTE: Asegúrate de que todos los microservicios estén corriendo:
- Gateway (puerto 8090)
- Eureka
- Microservicio de usuarios
- Microservicio de productores
- Microservicio de productos
- RabbitMQ
- MySQL
- MongoDB
"""

import requests
import time
import base64

# Configuración
BASE_URL = "http://localhost:8090"
TIMEOUT = 30  # Timeout para requests en segundos
MAX_RETRIES = 10  # Número máximo de reintentos para productos
RETRY_DELAY = 3  # Segundos entre reintentos para productos

# Cache para imágenes descargadas (evitar descargar la misma imagen varias veces)
IMAGE_CACHE = {}


def descargar_imagen_base64(url):
    """Descarga una imagen desde una URL y la convierte a base64"""
    if url in IMAGE_CACHE:
        return IMAGE_CACHE[url]

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # Convertir a base64 (solo el contenido, sin prefijo data:)
            img_base64 = base64.b64encode(response.content).decode('utf-8')
            IMAGE_CACHE[url] = img_base64
            return img_base64
        else:
            print(f"  ⚠ No se pudo descargar imagen: {url}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"  ⚠ Error descargando imagen: {e}")
        return None


# Datos de productores con sus gremios
PRODUCTORES_ADMIN = [
    {
        "usuario": {
            "u_nombre_usuario": "productor_carlos",
            "u_contrasenia": "password123",
            "u_email": "carlos.agricola@gmail.com",
            "u_rol": "productor-admin",
            "persona": {
                "p_cedula": "1061234567",
                "p_apellido": "Martínez",
                "p_nombre": "Carlos",
                "p_fecha_nacimiento": "1985-03-15",
                "p_direccion": "Vereda El Rosal, Popayán",
                "p_telefono": "3101234567"
            }
        },
        "gremio": {
            "nombre": "Gremio Agricultores del Valle",
            "descripcion": "Asociación de agricultores dedicados al cultivo de frutas y verduras orgánicas en el Valle del Cauca",
            "ubicacion": "Vereda El Rosal, Popayán, Cauca"
        }
    },
    {
        "usuario": {
            "u_nombre_usuario": "productor_maria",
            "u_contrasenia": "password123",
            "u_email": "maria.campo@gmail.com",
            "u_rol": "productor-admin",
            "persona": {
                "p_cedula": "1067654321",
                "p_apellido": "García",
                "p_nombre": "María",
                "p_fecha_nacimiento": "1990-07-22",
                "p_direccion": "Vereda Santa Rosa, Timbío",
                "p_telefono": "3157654321"
            }
        },
        "gremio": {
            "nombre": "Cooperativa Campesinos Unidos",
            "descripcion": "Cooperativa de pequeños productores enfocados en agricultura sostenible y productos tradicionales",
            "ubicacion": "Vereda Santa Rosa, Timbío, Cauca"
        }
    },
    {
        "usuario": {
            "u_nombre_usuario": "productor_jose",
            "u_contrasenia": "password123",
            "u_email": "jose.tierrafertil@gmail.com",
            "u_rol": "productor-admin",
            "persona": {
                "p_cedula": "1069876543",
                "p_apellido": "López",
                "p_nombre": "José",
                "p_fecha_nacimiento": "1978-11-05",
                "p_direccion": "Vereda La Esperanza, Silvia",
                "p_telefono": "3209876543"
            }
        },
        "gremio": {
            "nombre": "Asociación Tierra Fértil",
            "descripcion": "Productores especializados en tubérculos, hierbas medicinales y productos ancestrales de la región",
            "ubicacion": "Vereda La Esperanza, Silvia, Cauca"
        }
    }
]

# Productos organizados por categoría
# cat_id: 1=frutas, 2=verduras, 3=tubérculos, 4=hierbas, 5=hortalizas
PRODUCTOS_POR_GREMIO = [
    # Productos para Gremio 1 - Agricultores del Valle (frutas y verduras)
    [
        {"p_nombre": "Manzana Roja", "cat_id": 1, "p_unidad": "kg",
            "img": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=400", "p_precio": 4500, "p_stock": 100, "p_medicinal": False},
        {"p_nombre": "Naranja Valencia", "cat_id": 1, "p_unidad": "kg",
            "img": "https://images.unsplash.com/photo-1547514701-42782101795e?w=400", "p_precio": 3200, "p_stock": 150, "p_medicinal": False},
        {"p_nombre": "Banano Criollo", "cat_id": 1, "p_unidad": "kg",
            "img": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400", "p_precio": 2800, "p_stock": 200, "p_medicinal": False},
        {"p_nombre": "Mango Tommy", "cat_id": 1, "p_unidad": "kg",
            "img": "https://images.unsplash.com/photo-1553279768-865429fa0078?w=400", "p_precio": 5500, "p_stock": 80, "p_medicinal": False},
        {"p_nombre": "Piña Gold", "cat_id": 1, "p_unidad": "unidad",
            "img": "https://images.unsplash.com/photo-1550258987-190a2d41a8ba?w=400", "p_precio": 6000, "p_stock": 50, "p_medicinal": False},
        {"p_nombre": "Tomate Chonto", "cat_id": 2, "p_unidad": "kg",
            "img": "https://images.unsplash.com/photo-1546470427-227c7a68ae4e?w=400", "p_precio": 3800, "p_stock": 120, "p_medicinal": False},
        {"p_nombre": "Zanahoria", "cat_id": 2, "p_unidad": "kg", "img": "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=400",
            "p_precio": 2500, "p_stock": 180, "p_medicinal": False},
        {"p_nombre": "Pepino Cohombro", "cat_id": 2, "p_unidad": "kg",
            "img": "https://images.unsplash.com/photo-1449300079323-02e209d9d3a6?w=400", "p_precio": 2200, "p_stock": 90, "p_medicinal": False},
        {"p_nombre": "Lechuga Crespa", "cat_id": 5, "p_unidad": "unidad",
            "img": "https://images.unsplash.com/photo-1622206151226-18ca2c9ab4a1?w=400", "p_precio": 2000, "p_stock": 70, "p_medicinal": False},
        {"p_nombre": "Espinaca Fresca", "cat_id": 5, "p_unidad": "atado",
            "img": "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=400", "p_precio": 2500, "p_stock": 60, "p_medicinal": True},
    ],
    # Productos para Gremio 2 - Campesinos Unidos (verduras y hortalizas)
    [
        {"p_nombre": "Cebolla Cabezona", "cat_id": 2, "p_unidad": "kg",
            "img": "https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=400", "p_precio": 3000, "p_stock": 200, "p_medicinal": False},
        {"p_nombre": "Pimentón Rojo", "cat_id": 2, "p_unidad": "kg",
            "img": "https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?w=400", "p_precio": 4500, "p_stock": 80, "p_medicinal": False},
        {"p_nombre": "Brócoli", "cat_id": 2, "p_unidad": "kg", "img": "https://images.unsplash.com/photo-1459411552884-841db9b3cc2a?w=400",
            "p_precio": 5000, "p_stock": 60, "p_medicinal": True},
        {"p_nombre": "Coliflor", "cat_id": 2, "p_unidad": "unidad",
            "img": "https://images.unsplash.com/photo-1568584711075-3d021a7c3ca3?w=400", "p_precio": 4000, "p_stock": 45, "p_medicinal": False},
        {"p_nombre": "Repollo Verde", "cat_id": 5, "p_unidad": "unidad",
            "img": "https://images.unsplash.com/photo-1594282486552-05b4d80fbb9f?w=400", "p_precio": 3500, "p_stock": 70, "p_medicinal": False},
        {"p_nombre": "Acelga", "cat_id": 5, "p_unidad": "atado",
            "img": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400", "p_precio": 2000, "p_stock": 90, "p_medicinal": True},
        {"p_nombre": "Apio Fresco", "cat_id": 5, "p_unidad": "atado",
            "img": "https://images.unsplash.com/photo-1580391564590-aeca65c5e2d3?w=400", "p_precio": 2500, "p_stock": 80, "p_medicinal": True},
        {"p_nombre": "Limón Tahití", "cat_id": 1, "p_unidad": "kg",
            "img": "https://images.unsplash.com/photo-1590502593747-42a996133562?w=400", "p_precio": 4000, "p_stock": 150, "p_medicinal": True},
        {"p_nombre": "Papaya Tainung", "cat_id": 1, "p_unidad": "kg",
            "img": "https://images.unsplash.com/photo-1526318472351-c75fcf070305?w=400", "p_precio": 3500, "p_stock": 60, "p_medicinal": False},
        {"p_nombre": "Maracuyá", "cat_id": 1, "p_unidad": "kg", "img": "https://images.unsplash.com/photo-1604495772376-9657f0035eb5?w=400",
            "p_precio": 5500, "p_stock": 70, "p_medicinal": False},
    ],
    # Productos para Gremio 3 - Tierra Fértil (tubérculos y hierbas)
    [
        {"p_nombre": "Papa Criolla", "cat_id": 3, "p_unidad": "kg",
            "img": "https://images.unsplash.com/photo-1518977676601-b53f82ber3e3?w=400", "p_precio": 4500, "p_stock": 300, "p_medicinal": False},
        {"p_nombre": "Papa Pastusa", "cat_id": 3, "p_unidad": "kg",
            "img": "https://images.unsplash.com/photo-1508313880080-c4bef0730395?w=400", "p_precio": 3200, "p_stock": 250, "p_medicinal": False},
        {"p_nombre": "Yuca", "cat_id": 3, "p_unidad": "kg", "img": "https://images.unsplash.com/photo-1598030304671-5aa1d6f21128?w=400",
            "p_precio": 2800, "p_stock": 200, "p_medicinal": False},
        {"p_nombre": "Arracacha", "cat_id": 3, "p_unidad": "kg", "img": "https://images.unsplash.com/photo-1590165482129-1b8b27698780?w=400",
            "p_precio": 5000, "p_stock": 100, "p_medicinal": False},
        {"p_nombre": "Ñame", "cat_id": 3, "p_unidad": "kg", "img": "https://images.unsplash.com/photo-1585155770913-89e2506f0ec1?w=400",
            "p_precio": 4000, "p_stock": 80, "p_medicinal": False},
        {"p_nombre": "Cilantro", "cat_id": 4, "p_unidad": "atado",
            "img": "https://images.unsplash.com/photo-1526318472351-c75fcf070305?w=400", "p_precio": 1500, "p_stock": 150, "p_medicinal": True},
        {"p_nombre": "Perejil", "cat_id": 4, "p_unidad": "atado",
            "img": "https://images.unsplash.com/photo-1600857544200-b2f666a9a2ec?w=400", "p_precio": 1500, "p_stock": 130, "p_medicinal": True},
        {"p_nombre": "Albahaca", "cat_id": 4, "p_unidad": "atado",
            "img": "https://images.unsplash.com/photo-1618164435735-413d3b066c9a?w=400", "p_precio": 2000, "p_stock": 80, "p_medicinal": True},
        {"p_nombre": "Hierbabuena", "cat_id": 4, "p_unidad": "atado",
            "img": "https://images.unsplash.com/photo-1628556270448-4d4e4148e1b1?w=400", "p_precio": 1800, "p_stock": 100, "p_medicinal": True},
        {"p_nombre": "Manzanilla", "cat_id": 4, "p_unidad": "atado",
            "img": "https://images.unsplash.com/photo-1587593810167-a84920ea0781?w=400", "p_precio": 2500, "p_stock": 60, "p_medicinal": True},
        {"p_nombre": "Ruda", "cat_id": 4, "p_unidad": "atado", "img": "https://images.unsplash.com/photo-1515694590489-2879d33d88a0?w=400",
            "p_precio": 2000, "p_stock": 50, "p_medicinal": True},
        {"p_nombre": "Jengibre", "cat_id": 4, "p_unidad": "kg", "img": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=400",
            "p_precio": 12000, "p_stock": 40, "p_medicinal": True},
    ]
]


def registrar_usuario(usuario_data):
    """Registra un nuevo usuario"""
    url = f"{BASE_URL}/api/usuarios/registro"
    try:
        response = requests.post(url, json=usuario_data, timeout=TIMEOUT)
        if response.status_code == 200:
            print(f"✓ Usuario registrado: {usuario_data['u_email']}")
            return response.json()
        elif response.status_code == 400 and "duplicado" in response.text.lower():
            print(f"⚠ Usuario ya existe: {usuario_data['u_email']}")
            return {"exists": True}
        else:
            print(
                f"✗ Error registrando usuario {usuario_data['u_email']}: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"✗ Error de conexión: {e}")
        return None


def login_usuario(email, password):
    """Hace login y retorna el token"""
    url = f"{BASE_URL}/api/usuarios/login"
    try:
        response = requests.post(url, json={
            "u_email": email,
            "u_contrasenia": password
        }, timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Login exitoso: {email}")
            return data['access_token'], data['u_id']
        else:
            print(
                f"✗ Error en login {email}: {response.status_code} - {response.text}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"✗ Error de conexión: {e}")
        return None, None


def crear_gremio(token, user_id, gremio_data):
    """Crea un nuevo gremio con reintentos"""
    url = f"{BASE_URL}/api/gremios/{user_id}"
    headers = {"Authorization": f"Bearer {token}"}

    for intento in range(MAX_RETRIES):
        try:
            response = requests.post(
                url, json=gremio_data, headers=headers, timeout=TIMEOUT)
            if response.status_code == 201:
                data = response.json()
                print(
                    f"✓ Gremio creado: {gremio_data['nombre']} (ID: {data['id']})")
                return data
            elif response.status_code == 400 and "ya existe" in response.text.lower():
                print(f"⚠ Gremio ya existe: {gremio_data['nombre']}")
                # Intentar obtener el gremio existente
                return obtener_gremios_y_buscar(gremio_data['nombre'])
            elif response.status_code == 400 and "no encontrado" in response.text.lower():
                if intento < MAX_RETRIES - 1:
                    print(
                        f"  ⏳ Esperando sincronización del productor... (intento {intento + 1}/{MAX_RETRIES})")
                    time.sleep(RETRY_DELAY)
                    continue
            else:
                print(
                    f"✗ Error creando gremio: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"✗ Error de conexión: {e}")
            if intento < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
                continue
            return None

    print(f"✗ No se pudo crear el gremio después de {MAX_RETRIES} intentos")
    return None


def obtener_gremios_y_buscar(nombre):
    """Obtiene todos los gremios y busca uno por nombre"""
    url = f"{BASE_URL}/api/gremios/"
    try:
        response = requests.get(url, timeout=TIMEOUT)
        if response.status_code == 200:
            gremios = response.json()
            for gremio in gremios:
                if gremio['nombre'] == nombre:
                    return gremio
    except requests.exceptions.RequestException:
        pass
    return None


def obtener_productor_por_user_id(user_id):
    """Obtiene el productor asociado a un user_id con reintentos"""
    url = f"{BASE_URL}/api/productores/user/{user_id}"

    for intento in range(MAX_RETRIES):
        try:
            response = requests.get(url, timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Productor encontrado: ID {data['id']}")
                return data
            elif response.status_code == 404:
                if intento < MAX_RETRIES - 1:
                    print(
                        f"  ⏳ Esperando registro del productor... (intento {intento + 1}/{MAX_RETRIES})")
                    time.sleep(RETRY_DELAY)
                    continue
            else:
                print(
                    f"✗ Error obteniendo productor: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"✗ Error de conexión: {e}")
            if intento < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
                continue
            return None

    print(f"✗ No se encontró el productor después de {MAX_RETRIES} intentos")
    return None


def registrar_producto(token, producto_data):
    """Registra un nuevo producto con reintentos para esperar sincronización"""
    url = f"{BASE_URL}/api/productos/"
    headers = {"Authorization": f"Bearer {token}"}

    # Convertir la imagen URL a base64
    if 'img' in producto_data and producto_data['img'].startswith('http'):
        print(f"  📷 Descargando imagen para {producto_data['p_nombre']}...")
        img_base64 = descargar_imagen_base64(producto_data['img'])
        if img_base64:
            producto_data = {**producto_data, 'img': img_base64}
        else:
            # Si falla la descarga, usar una imagen placeholder en base64
            producto_data = {**producto_data, 'img': ''}

    for intento in range(MAX_RETRIES):
        try:
            response = requests.post(
                url, json=producto_data, headers=headers, timeout=TIMEOUT)
            if response.status_code == 200:
                print(f"  ✓ Producto registrado: {producto_data['p_nombre']}")
                return response.json()
            elif response.status_code == 500:
                # Puede ser que el productor aún no esté sincronizado en el microservicio de productos
                if intento < MAX_RETRIES - 1:
                    print(
                        f"  ⏳ Esperando sincronización del productor en micro_productos... (intento {intento + 1}/{MAX_RETRIES})")
                    time.sleep(RETRY_DELAY)
                    continue
                else:
                    print(
                        f"  ✗ Error registrando producto {producto_data['p_nombre']}: {response.status_code} - Productor no sincronizado")
                    return None
            else:
                print(
                    f"  ✗ Error registrando producto {producto_data['p_nombre']}: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"  ✗ Error de conexión: {e}")
            if intento < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
                continue
            return None

    return None


def verificar_conexion():
    """Verifica que el gateway esté accesible"""
    try:
        response = requests.get(f"{BASE_URL}/api/productos/", timeout=5)
        return True
    except requests.exceptions.RequestException:
        return False


def main():
    print("=" * 60)
    print("   SEED DATABASE - AgroMercado Local")
    print("=" * 60)
    print()

    # Verificar conexión
    print("🔌 Verificando conexión al gateway...")
    if not verificar_conexion():
        print("✗ No se puede conectar al gateway en", BASE_URL)
        print("  Asegúrate de que todos los microservicios estén corriendo.")
        return
    print("✓ Gateway accesible")
    print()

    productores_info = []
    productos_registrados = 0
    productos_fallidos = 0

    # Paso 1: Registrar usuarios productores-admin
    print("📝 Paso 1: Registrando usuarios productores...")
    print("-" * 40)
    for productor in PRODUCTORES_ADMIN:
        registrar_usuario(productor["usuario"])
        time.sleep(0.5)  # Pequeña pausa para evitar sobrecarga

    print()

    # Esperar a que RabbitMQ procese los mensajes
    print("⏳ Esperando 5 segundos para sincronización vía RabbitMQ...")
    time.sleep(5)
    print()

    # Paso 2: Hacer login con cada productor y crear gremios
    print("🔐 Paso 2: Login y creación de gremios...")
    print("-" * 40)
    for i, productor in enumerate(PRODUCTORES_ADMIN):
        email = productor["usuario"]["u_email"]
        password = productor["usuario"]["u_contrasenia"]

        token, user_id = login_usuario(email, password)
        if token and user_id:
            # Obtener info del productor primero
            productor_info = obtener_productor_por_user_id(user_id)

            if productor_info:
                # Verificar si ya tiene gremio
                if productor_info.get("id_gremio"):
                    print(
                        f"⚠ Productor ya tiene gremio asignado (ID: {productor_info['id_gremio']})")
                    gremio_id = productor_info['id_gremio']
                else:
                    # Crear gremio
                    gremio = crear_gremio(token, user_id, productor["gremio"])
                    gremio_id = gremio['id'] if gremio else None

                if gremio_id:
                    productores_info.append({
                        "token": token,
                        "user_id": user_id,
                        "productor_id": productor_info["id"],
                        "gremio_id": gremio_id,
                        "email": email
                    })

        time.sleep(0.5)

    print()

    if not productores_info:
        print("✗ No se pudieron registrar productores. Abortando.")
        return

    # Esperar más tiempo para sincronización de productores en el microservicio de productos
    print("⏳ Esperando 10 segundos para sincronización de productores en micro_productos...")
    time.sleep(10)
    print()

    # Paso 3: Registrar productos para cada productor
    print("🥕 Paso 3: Registrando productos...")
    print("-" * 40)

    for i, info in enumerate(productores_info):
        if i >= len(PRODUCTOS_POR_GREMIO):
            break

        print(
            f"\n📦 Productos para productor ID {info['productor_id']} ({info['email']}):")
        productos = PRODUCTOS_POR_GREMIO[i]

        for producto in productos:
            producto_data = {
                **producto,
                "prod_id": info["productor_id"]
            }
            result = registrar_producto(info["token"], producto_data)
            if result:
                productos_registrados += 1
            else:
                productos_fallidos += 1
            time.sleep(0.3)  # Pausa entre productos

    print()
    print("=" * 60)
    print("   ✅ SEED COMPLETADO")
    print("=" * 60)
    print()
    print("📊 Resumen:")
    print(f"   - Productores configurados: {len(productores_info)}")
    print(f"   - Productos registrados exitosamente: {productos_registrados}")
    if productos_fallidos > 0:
        print(f"   - Productos con error: {productos_fallidos}")
    print()
    print("🔑 Credenciales de acceso:")
    for productor in PRODUCTORES_ADMIN:
        print(
            f"   - {productor['usuario']['u_email']} / {productor['usuario']['u_contrasenia']}")
    print()

    if productos_fallidos > 0:
        print("⚠ NOTA: Algunos productos fallaron. Esto puede deberse a que los")
        print("  productores no se sincronizaron correctamente con el microservicio")
        print("  de productos vía RabbitMQ. Verifica que RabbitMQ esté funcionando")
        print("  correctamente y vuelve a ejecutar el script si es necesario.")


if __name__ == "__main__":
    main()
