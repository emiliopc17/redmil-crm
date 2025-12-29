# 🎵 Tema Spotify - REDMIL Quoter Pro
**Fecha de Implementación**: 22 de Diciembre, 2025  
**Inspiración**: Spotify Dark Mode

---

## 🎨 Paleta de Colores

###Colors Principales
```css
/* Backgrounds */
#121212  /* Fondo principal - Spotify Dark */
#181818  /* Tarjetas y cards */
#282828  /* Bordes y separadores */
#000000  /* Sidebar */

/* Texto */
#FFFFFF  /* Texto principal */
#B3B3B3  /* Texto secundario */
#535353  /* Texto deshabilitado */

/* Spotify Green */
#1DB954  /* Verde principal */
#1ED760  /* Verde hover */
#1FDF64  /* Verde activo */

/* Estados */
#E22134  /* Error (Spotify Red) */
#FFB800  /* Warning */
```

---

## ✨ Características Implementadas

### 1. **Dark Mode Completo** 🌙
- ✅ Fondo principal: `#121212` (Spotify Dark)
- ✅ Tarjetas: `#181818` (Cards)
- ✅ Texto blanco sobre fondo oscuro
- ✅ Alto contraste para legibilidad

### 2. **Barra Lateral Fija** 📌
```css
position: fixed;
left: 0;
top: 0;
height: 100vh;
background-color: #000000;
```
- Permanece visible al hacer scroll
- Fondo negro puro (#000000)
- Borde derecho sutil (#282828)

### 3. **Fuente Inter** 📝
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900');
font-family: 'Inter', -apple-system, sans-serif;
```
- **300**: Light (textos descriptivos)
- **400**: Regular (cuerpo de texto)
- **500**: Medium (labels)
- **600**: Semi-Bold (subtítulos)
- **700**: Bold (títulos)
- **800**: Extra-Bold (métricas)
- **900**: Black (títulos principales)

### 4. **Botones Estilo Píldora** 💊

#### Botones Primarios (Guardar/Imprimir)
```css
background: linear-gradient(135deg, #1ED760, #1DB954);
border-radius: 500px;  /* Pill shape */
color: #000000;
font-weight: 800;
box-shadow: 0 8px 24px rgba(29, 185, 84, 0.4);
```

**Efectos de Hover:**
- Transform: `scale(1.04)`
- Box-shadow intenso verde
- Gradiente más brillante

**Ejemplo Visual:**
```
┌─────────────────────────────┐
│  💾 GUARDAR COTIZACIÓN      │  ← Verde vibrante
└─┬───────────────────────┬───┘    Forma de píldora
  └───────────────────────┘        Sombra verde
```

#### Botones Secundarios
```css
background: transparent;
border: 1px solid #535353;
border-radius: 500px;
color: #FFFFFF;
```

### 5. **Efectos Hover Elegantes** ✨

#### En Tablas
```css
tbody tr:hover {
    background-color: #282828;
    transform: scale(1.01);
    box-shadow: 0 2px 8px rgba(29, 185, 84, 0.2);
}
```

#### En Cards
```css
.bento-card:hover {
    background: #202020;
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6);
    border-color: #1DB954;
}
```

### 6. **Animaciones Tipo Framer Motion** 🎬

#### Fade In
```css
@keyframes fadeIn {
    from { 
        opacity: 0; 
        transform: translateY(20px); 
    }
    to { 
        opacity: 1; 
        transform: translateY(0); 
    }
}
```

#### Slide From Right (Preview Panel)
```css
@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(100px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}
```

**Uso:**
```css
.animate-slide-right {
    animation: slideInRight 0.7s cubic-bezier(0.4, 0, 0.2, 1);
}
```

#### Otras Animaciones Disponibles
- **fadeIn**: Entrada suave con desplazamiento
- **slideInLeft**: Desliza desde la izquierda
- **slideInRight**: Desliza desde la derecha
- **scaleIn**: Escala desde 90% a 100%

### 7. **Scrollbar Personalizado** 📜
```css
::-webkit-scrollbar {
    width: 12px;
    background: #121212;
}

::-webkit-scrollbar-thumb {
    background: #535353;
    border-radius: 6px;
    border: 3px solid #121212;
}

::-webkit-scrollbar-thumb:hover {
    background: #B3B3B3;
}
```

---

## 🖼️ Componentes Estilizados

### Login Page
```
┌─────────────────────────────────────┐
│                                     │
│         🎵 REDMIL                   │  ← Verde Spotify
│         QUOTER PRO                  │  ← Gris claro
│                                     │
│  ┌─────────────────────────────┐   │
│  │ USUARIO                     │   │
│  │ [___________________]       │   │  ← Fondo #121212
│  └─────────────────────────────┘   │    Borde gris
│                                     │
│  ┌─────────────────────────────┐   │
│  │ CONTRASEÑA                  │   │
│  │ [___________________]       │   │
│  └─────────────────────────────┘   │
│                                     │
│  ╔═════════════════════════════╗   │
│  ║   INICIAR SESIÓN            ║   │  ← Botón verde
│  ╚═════════════════════════════╝   │    píldora
│                                     │
└─────────────────────────────────────┘
Fondo: #181818 (Card oscuro)
```

### Dashboard Cards
```
┌───────────────────────────────┐
│ TASA DE CAMBIO                │ ← Label gris claro
│                                │
│ L. 24.5000                     │ ← Valor blanco bold
│                                │
│ ✅ Actualizado: 2024-12-22     │ ← Verde Spotify
│                                │
│ Fuente: Manual                 │ ← Gris oscuro
└───────────────────────────────┘
```

### Tabla de Productos
```
╔════════════════════════════════════════╗
║ CÓDIGO  │ DESCRIPCIÓN  │ PRECIO       ║ ← Headers negros
╠════════════════════════════════════════╣
║ P-001   │ Laptop HP    │ L. 15,000.00 ║
╠════════════════════════════════════════╣
║ P-002   │ Mouse        │ L. 250.00    ║ ← Hover: + brillo
╚════════════════════════════════════════╝          + sombra verde
```

---

## 📁 Archivos Modificados

### 1. `.streamlit/config.toml`
```toml
[theme]
primaryColor = "#1DB954"          # Spotify Green
backgroundColor = "#121212"        # Spotify Background
secondaryBackgroundColor = "#181818"  # Spotify Cards
textColor = "#FFFFFF"              # White text
font = "sans serif"
```

### 2. `utils/styles.py`
- **Líneas**: ~450 líneas de CSS
- **Componentes**:
  - Global Spotify Theme
  - Sidebar fijo
  - Botones píldora verdes
  - Efectos hover en tablas
  - Animaciones Framer Motion-style
  - Scrollbar personalizado
  - Cards oscuros
  - Inputs y forms
  - Alerts y mensajes

### 3. `app.py` - Login
- Actualizado con tema Spotify
- Botón verde píldora
- Inputs oscuros con borde
- Card #181818

---

## 🎯 Casos de Uso

### Aplicar Animación Slide Right
```python
st.markdown('<div class="animate-slide-right">', unsafe_allow_html=True)
# Tu contenido aquí
st.markdown('</div>', unsafe_allow_html=True)
```

### Crear Card Spotify
```python
from utils import styles

styles.card("""
    <div class="metric-label">TOTAL VENTAS</div>
    <div class="metric-value">L. 150,000.00</div>
    <div class="metric-delta delta-pos">↑ 15% vs mes anterior</div>
""")
```

### Botón Verde Primario
```python
if st.button("💾 Guardar Cotización", type="primary"):
    # El botón será verde píldora automáticamente
    pass
```

---

## 🎨 Jerarquía Visual

### Títulos
```
H1 (3rem, weight 800) → Títulos principales
H2 (2rem, weight 800) → Secciones
H3 (1.5rem, weight 800) → Subsecciones
```

### Texto
```
Normal (1rem, weight 400) → Content
Medium (1rem, weight 500) → Labels
Bold (1rem, weight 700) → Emphasis
```

### Colores de Estado
```
✅ Success: #1DB954 (Verde Spotify)
❌ Error: #E22134 (Rojo Spotify)
⚠️ Warning: #FFB800 (Amarillo)
ℹ️ Info: #B3B3B3 (Gris)
```

---

## 🚀 Ventajas del Tema

1. **Reducción de Fatiga Visual**: Dark mode reduce el cansancio
2. **Profesionalismo**: Diseño moderno y elegante
3. **Consistencia**: Usa la paleta probada de Spotify
4. **Accesibilidad**: Alto contraste para mejor legibilidad
5. **Performance**: Animaciones optimizadas con `cubic-bezier`
6. **Branding**: Verde distintivo para acciones importantes

---

## 📱 Responsive Design

El tema es completamente responsivo:
- Sidebar fija en desktop
- Botones adaptativos
- Scroll suave en móviles
- Cards apilables en pantallas pequeñas

---

## 🔧 Mantenimiento

Para ajustar colores:
1. **Editar** `.streamlit/config.toml` para colores base
2. **Editar** `utils/styles.py` para estilos detallados

Para añadir nuevas animaciones:
```css
@keyframes miAnimacion {
    from { /* estado inicial */ }
    to { /* estado final */ }
}

.mi-clase {
    animation: miAnimacion 0.5s ease-out;
}
```

---

**Tema implementado y listo para uso** ✅  
**Inspiración**: Spotify Web Player  
**Framework**: Streamlit + Custom CSS  
**Animaciones**: CSS Keyframes (Framer Motion style)
