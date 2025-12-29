# 🎵 Invoice Manager Pro

Sistema moderno de gestión de facturas con interfaz estilo Spotify, construido con tecnologías de vanguardia.

## 🚀 Stack Tecnológico

### Frontend
- **Refine** - Framework React para aplicaciones data-intensive
- **Tailwind CSS** - Estilos utilities-first
- **React** - Biblioteca UI
- **Vite** - Build tool ultrarrápido
- **Tema Spotify** - Dark/Light mode con estética premium

### Backend
- **FastAPI** - Framework Python moderno y rápido
- **SQLAlchemy** - ORM para PostgreSQL
- **Docling** - Extracción avanzada de datos de PDFs
- **Pydantic** - Validación de datos

### Base de Datos
- **PostgreSQL** - Base de datos relacional (esquema basado en Crater)

### DevOps
- **Docker Compose** - Orquestación de contenedores
- **Nginx** - Reverse proxy

## 📁 Estructura del Proyecto

```
invoice-manager-pro/
├── frontend/                 # Aplicación Refine + React
│   ├── src/
│   │   ├── components/      # Componentes reutilizables
│   │   ├── pages/          # Páginas principales
│   │   ├── providers/      # Data providers
│   │   ├── styles/         # Estilos Tailwind
│   │   └── theme/          # Configuración de temas
│   └── package.json
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/            # Endpoints
│   │   ├── models/         # Modelos SQLAlchemy
│   │   ├── schemas/        # Esquemas Pydantic
│   │   ├── services/       # Lógica de negocio
│   │   └── docling/        # Procesamiento de PDFs
│   └── requirements.txt
├── database/               # Scripts SQL y migraciones
│   └── init.sql
├── docker-compose.yml      # Configuración de servicios
└── README.md
```

## 🎨 Características

### Interfaz Estilo Spotify
- ✅ Dark mode y Light mode con transiciones suaves
- ✅ Sidebar colapsable
- ✅ Paleta de colores Spotify (#1DB954, #121212, #181818)
- ✅ Tipografía Inter
- ✅ Animaciones fluidas
- ✅ Hover effects premium

### Gestión de Facturas (Basado en Crater)
- ✅ Crear, editar y eliminar facturas
- ✅ Gestión de clientes
- ✅ Gestión de productos/servicios
- ✅ Múltiples monedas
- ✅ Impuestos y descuentos
- ✅ Reportes y estadísticas

### Módulo CRM Integral
- ✅ **Pipeline Kanban**: Gestión visual de cotizaciones (Prospección -> Ganada)
- ✅ **Dashboard CRM**: Métricas de conversión y Top 5 de clientes
- ✅ **Seguimiento de Clientes**: Timeline de notas y registro de llamadas
- ✅ **Tareas y Recordatorios**: Gestión de pendientes vinculados a clientes
- ✅ **Automatización n8n**: Flujos automáticos (ej. Gracias por su compra)

### Procesamiento Inteligente de PDFs
- ✅ Extracción automática usando Docling
- ✅ Carga de listas de precios de proveedores
- ✅ OCR para PDFs escaneados
- ✅ Validación y limpieza de datos

## 🐳 Inicio Rápido

### Prerrequisitos
- Docker Desktop (Instalado y Corriendo)

### Instalación Automática (Windows)

1. Abrir la carpeta del proyecto.
2. Hacer doble clic en `start-dev.bat`.
   - Este script preparará la base de datos, construirá las imágenes y levantará los servicios.

### Acceso
- **Frontend**: http://localhost:3000
- **CRM Dashboard**: http://localhost:3000 (Página de inicio)
- **Pipeline**: http://localhost:3000/pipeline
- **n8n Automation**: http://localhost:5678
- **Backend API**: http://localhost:8000

## 🎯 Roadmap

- [x] Configuración inicial del proyecto
- [x] Esquema de base de datos basado en Crater
- [x] API REST completa
- [x] Interfaz Refine con tema Spotify
- [x] Integración Docling para PDFs
- [x] Módulo CRM & Pipeline Kanban
- [x] Automatización con n8n
- [ ] Autenticación JWT avanzada
- [ ] Sistema de roles y permisos
- [ ] Exportación de reportes PDF personalizados
- [ ] Notificaciones en tiempo real

## 📄 Licencia

Proyecto privado para REDMIL Honduras

## 👨‍💻 Desarrollador

Desarrollado con ❤️ usando Antigravity AI
