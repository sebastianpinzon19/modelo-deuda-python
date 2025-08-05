# Archivo CSS - Procesador de Archivos Grupo Planeta

## 📁 Archivo: `styles.css`

Este archivo CSS contiene todos los estilos para la interfaz del Procesador de Archivos del Grupo Planeta. Está diseñado con un enfoque moderno, responsive y accesible.

## 🎨 Características Principales

### ✨ Diseño Moderno
- **Variables CSS**: Uso extensivo de custom properties para consistencia
- **Gradientes**: Efectos visuales atractivos en botones e iconos
- **Sombras**: Efectos de profundidad y elevación
- **Animaciones**: Transiciones suaves y efectos hover

### 📱 Responsive Design
- **Mobile-first**: Optimizado para dispositivos móviles
- **Grid Layout**: Sistema de grid flexible y adaptativo
- **Breakpoints**: Diseño adaptativo en múltiples tamaños de pantalla

### ♿ Accesibilidad
- **Contraste**: Colores con buen contraste para legibilidad
- **Focus visible**: Indicadores claros para navegación por teclado
- **Reduced motion**: Respeto por las preferencias de movimiento del usuario
- **Semántica**: Estructura HTML semántica y bien organizada

## 🏗️ Estructura del CSS

### 1. **Variables CSS (Custom Properties)**
```css
:root {
    /* Colores principales */
    --primary-color: #283593;
    --primary-light: #5f5fc4;
    --primary-dark: #001064;
    
    /* Espaciado */
    --spacing-xs: 5px;
    --spacing-sm: 10px;
    /* ... */
}
```

### 2. **Reset y Configuración Base**
- Box-sizing universal
- Configuración de fuente y colores base
- Reset de márgenes y padding

### 3. **Layout Principal**
- Container con ancho máximo
- Sistema de grid para procesadores
- Header con diseño centrado

### 4. **Componentes**
- **Tarjetas de Procesador**: Diseño de tarjetas con hover effects
- **Zonas de Drag & Drop**: Interfaz intuitiva para subida de archivos
- **Formularios**: Controles de entrada estilizados
- **Botones**: Botones con gradientes y efectos hover
- **Barras de Progreso**: Indicadores visuales de progreso
- **Notificaciones Toast**: Sistema de notificaciones no intrusivo
- **Modales**: Ventanas emergentes con animaciones

### 5. **Utilidades**
- Clases de espaciado (margin, padding)
- Clases de texto (alineación)
- Clases de visibilidad
- Animaciones reutilizables

## 🎯 Secciones Principales

### Header
- Título principal con icono
- Descripción del sistema
- Fondo blanco con sombra

### Grid de Procesadores
- **Cartera**: Procesamiento de archivos PROVCA.CSV
- **Anticipos**: Procesamiento de archivos de anticipos
- **Modelo Deuda**: Generación de modelo de deuda

### Características de Cada Tarjeta
- Icono con gradiente único
- Título y subtítulo descriptivo
- Zona de drag & drop
- Vista previa de archivos
- Validación en tiempo real
- Barra de progreso
- Botón de procesamiento

## 🌈 Paleta de Colores

### Colores Principales
- **Primario**: `#283593` (Azul oscuro)
- **Primario Claro**: `#5f5fc4` (Azul medio)
- **Primario Oscuro**: `#001064` (Azul muy oscuro)

### Colores de Estado
- **Éxito**: `#4caf50` (Verde)
- **Error**: `#f44336` (Rojo)
- **Advertencia**: `#ff9800` (Naranja)

### Colores de Texto
- **Primario**: `#333` (Gris oscuro)
- **Secundario**: `#666` (Gris medio)

## 📱 Breakpoints Responsive

### Desktop (> 768px)
- Grid de 3 columnas
- Espaciado completo
- Efectos hover completos

### Tablet (≤ 768px)
- Grid de 1 columna
- Espaciado reducido
- Modal adaptado

### Mobile (≤ 480px)
- Layout vertical
- Botones de ancho completo
- Texto más pequeño

## 🎭 Animaciones y Transiciones

### Transiciones Principales
- **Normal**: `0.3s ease`
- **Rápida**: `0.2s ease`
- **Lenta**: `0.5s ease`

### Efectos Animados
- **Hover en tarjetas**: Elevación y sombra
- **Drag & Drop**: Escala y cambio de color
- **Modal**: Slide-in desde arriba
- **Toast**: Slide-in desde la derecha
- **Loading**: Spinner rotatorio

## 🔧 Utilidades CSS

### Espaciado
```css
.mb-0, .mb-1, .mb-2, .mb-3, .mb-4, .mb-5
.mt-0, .mt-1, .mt-2, .mt-3, .mt-4, .mt-5
```

### Texto
```css
.text-center, .text-left, .text-right
```

### Visibilidad
```css
.hidden, .visible
```

### Animaciones
```css
.fade-in, .slide-up
```

## 🚀 Optimizaciones

### Performance
- Variables CSS para consistencia
- Transiciones optimizadas
- Selectores eficientes

### Mantenibilidad
- Comentarios descriptivos
- Estructura modular
- Nomenclatura consistente

### Compatibilidad
- Fallbacks para navegadores antiguos
- Prefijos automáticos (si se usa PostCSS)
- Soporte para navegadores modernos

## 📋 Uso

Para usar este CSS en tu proyecto:

1. **Incluir el archivo**:
```html
<link rel="stylesheet" href="styles.css">
```

2. **Fuentes requeridas**:
```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:400,500,700&display=swap">
```

3. **Iconos requeridos**:
```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
```

## 🔄 Actualizaciones

### Versión 1.0
- Estructura base completa
- Diseño responsive
- Sistema de componentes
- Utilidades CSS
- Optimizaciones de accesibilidad

## 📞 Soporte

Para preguntas o sugerencias sobre el CSS, contactar al equipo de desarrollo del Grupo Planeta.

---

**Desarrollado para Grupo Planeta**  
*Sistema de Procesamiento de Archivos* 