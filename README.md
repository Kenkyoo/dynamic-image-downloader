🚀 Descargador Estético de Imágenes con Interfaz Gráfica

Una aplicación de escritorio elegante y funcional desarrollada en Python utilizando Tkinter para la interfaz gráfica, Pandas para la manipulación de datos y Threading para descargas en segundo plano sin congelar la ventana. Cuenta con un diseño moderno basado en la popular paleta de colores Nord.

✨ Características Principales

🎨 Interfaz Gráfica Premium: Diseño moderno y minimalista adaptado por completo utilizando la paleta de colores Nord (tonos oscuros árticos con acentos azules y verdes).

🧵 Concurrencia Inteligente (Threading): Las descargas de archivos se ejecutan en un hilo secundario independiente. Esto evita que la interfaz de usuario se congele o se muestre como "No responde" durante procesos largos.

🔢 Renombrado y Formateo Alfabético: Genera identificadores automáticos secuenciales con ceros a la izquierda (A00001, A00002, etc.) asegurando que los archivos queden ordenados perfectamente en tu explorador de archivos.

📊 Barra de Progreso Interactiva: Implementación visual con ttk.Progressbar combinada con actualizaciones de estado dinámicas en tiempo real.

🛡️ Robustez y Control de Errores: Incluye bloques try-except y validación de códigos de estado HTTP (ej. 200 OK) para resistir enlaces rotos o caídas de conexión sin interrumpir la secuencia.

📁 Reporte Automatizado: Modifica el archivo CSV original añadiendo las columnas de los IDs generados (img_id) y las rutas físicas de destino (img_path).

🛠️ Tecnologías Utilizadas

Python 3 (Núcleo del sistema)

Tkinter / TTK (Construcción de GUI con temas modificados)

Pandas (Lectura, procesamiento y escritura de archivos CSV estructurados)

Requests (Gestión de peticiones HTTP de forma síncrona y segura)

Threading (Gestión de subprocesos concurrentes)

📋 Requisitos Previos e Instalación

1. Clonar el repositorio u organizar los archivos

Descarga el código fuente en tu espacio de trabajo local de la siguiente manera:

git clone [https://github.com/TU_USUARIO/TU_REPOSITORIO.git](https://github.com/TU_USUARIO/TU_REPOSITORIO.git)
cd TU_REPOSITORIO


2. Configurar el Entorno Virtual (Recomendado)

Para mantener limpias tus dependencias globales, crea y activa un entorno virtual de Python:

En Linux / macOS:

python3 -m venv venv
source venv/bin/activate


En Windows (PowerShell):

python -m venv venv
.\venv\Scripts\Activate.ps1


3. Instalar Dependencias

Instala todas las librerías necesarias ejecutando el archivo requirements.txt adjunto:

pip install -r requirements.txt


🚀 Guía de Uso del Sistema

Paso 1: Preparar el archivo CSV de origen

La aplicación requiere un archivo estructurado con formato .csv. Por defecto, el programa buscará un archivo llamado links.csv en la raíz del proyecto, pero podés seleccionar cualquier otro desde la interfaz.

El único requisito obligatorio es que contenga una cabecera llamada img_link con las URLs correspondientes:

img_link
[https://picsum.photos/300/200](https://picsum.photos/300/200)
[https://picsum.photos/300/201](https://picsum.photos/300/201)
[https://picsum.photos/300/202](https://picsum.photos/300/202)


Paso 2: Ejecutar la Aplicación

Inicia la interfaz gráfica ejecutando el archivo principal:

python app.py


Paso 3: Interactuar con la GUI

📂 Seleccionar CSV: Haz clic para abrir el navegador de archivos si deseas utilizar un CSV diferente a links.csv.

📁 Cambiar Destino: Selecciona el directorio donde querés que se guarden tus imágenes (por defecto se creará una carpeta llamada Imgs).

🚀 Iniciar descarga: Presiona el botón verde. La interfaz se deshabilitará de forma segura temporalmente, la barra de progreso comenzará a llenarse y la etiqueta de estado te informará la descarga exacta en tiempo real.

💾 Verificación final: Una vez completado, emergerá un cuadro de diálogo informando el éxito del proceso y tu archivo CSV se actualizará automáticamente con los metadatos correspondientes.

🗂️ Estructura del Proyecto

├── app.py                  # Código fuente principal de la aplicación GUI
├── requirements.txt        # Archivo con la lista completa de dependencias de pip
├── links.csv               # Archivo CSV de ejemplo con tus enlaces (creado por el usuario)
└── Imgs/                   # Carpeta de salida por defecto generada al descargar
    ├── A00001.jpg
    ├── A00002.jpg
    └── A00003.jpg


🎨 Especificaciones de Estilo (Nord Palette)

El entorno gráfico fue desarrollado siguiendo rigurosamente las pautas de diseño estético del ecosistema Nord Theme, asegurando un descanso visual óptimo:

Elemento

Variable

Código Hex

Descripción

Fondo de Ventana

bg_dark

#2E3440

Gris polar profundo

Elementos / Contenedores

bg_widget

#3B4252

Gris polar medio

Campos de Entrada

bg_entry

#434C5E

Gris polar claro

Éxito / Acción Principal

green

#A3BE8C

Verde bosque ártico

Progreso / Enfoque

blue

#81A1C1

Azul glaciar

Desarrollado con ❤️ enfocado en rendimiento de backend y diseño de interfaces nativas limpias.
