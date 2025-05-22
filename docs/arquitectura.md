# Arquitectura y Estructura de Carpetas motivAI

## Estructura General
```
motivAI/
├── README.md                # Documentación principal
├── docs/                    # Documentación adicional y recursos
│   ├── branding.md          # Branding, paleta de colores, logo, favicon
│   ├── arquitectura.md      # Arquitectura y estructura de carpetas
│   ├── politicas.md         # Políticas de privacidad y términos (borrador)
│   └── enlaces.md           # Enlaces útiles (incluyendo Google Sheets)
├── backlog/                 # Backlog y gestión de tareas
│   └── motivAI-backlog.csv  # Backlog inicial (para Google Sheets)
├── logo/                    # Recursos visuales (logo, favicon)
├── backend/                 # Proyecto Django (backend)
└── frontend/                # Proyecto Next.js (frontend)
```

## Diagrama de Flujo Conversacional

```ascii
+-------------------+
|   Registro/Login  |
+-------------------+
          |
          v
+-------------------+
|  Inicio Conversación |
+-------------------+
          |
          v
+-------------------+
|  Procesamiento IA  |
+-------------------+
          |
          v
+-------------------+
|  Extracción Datos  |
+-------------------+
          |
          v
+-------------------+
|  Validación/Clarificación |
+-------------------+
          |
          v
+-------------------+
|  Generar Plan     |
+-------------------+
          |
          v
+-------------------+
|  Rutina Diaria    |
+-------------------+
          |
          v
+-------------------+
|  Marcar Progreso  |
+-------------------+
          |
          v
+-------------------+
|  Feedback/Notifs  |
+-------------------+
```

## Sistema Conversacional

### Flujo de Conversación
1. **Inicio**: Usuario se registra/inicia sesión
2. **Conversación Inicial**:
   - IA pregunta sobre motivación y objetivos
   - Usuario responde libremente
   - IA extrae información relevante
3. **Validación y Clarificación**:
   - Si la respuesta no es clara, IA pide aclaración
   - Sistema de fallback para respuestas no entendidas
4. **Recopilación de Datos**:
   - Edad, peso, condiciones médicas, etc.
   - Respuestas abiertas procesadas por IA
   - Validación de datos críticos
5. **Generación de Plan**:
   - IA usa datos recopilados para crear plan
   - Plan se adapta a respuestas y contexto

### Componentes del Sistema
- **ConversationManager**: Gestiona estado y contexto
- **NLPProcessor**: Procesa respuestas abiertas
- **DataExtractor**: Extrae información relevante
- **ValidationSystem**: Valida y clarifica respuestas
- **ContextManager**: Mantiene contexto de conversación

## Modelo de Datos (Resumen)
- Usuario: datos personales, foto, autenticación
- Conversacion: estado, contexto, historial
- Pregunta: tipo (abierta, opción múltiple, numérica)
- Respuesta: texto, datos extraídos, validación
- PlanEntrenamiento: un plan activo por usuario, historial lógico
- Rutina: cronograma diario del plan
- Ejercicio: base de datos creada por IA
- EjercicioRutina: ejercicios asignados a cada rutina
- Progreso: registro de peso, medidas, fotos
- Notificación: push y motivacionales
- Feedback: sugerencias y reportes
- (Futuro) Logros, integración dispositivos, nutrición

## Explicación de Carpetas
- **docs/**: Toda la documentación técnica, branding, políticas y enlaces.
- **backlog/**: Archivo CSV con el backlog de tareas, para importar a Google Sheets.
- **logo/**: Archivos SVG del logo y favicon.
- **backend/**: Proyecto Django, con apps separadas por dominio:
  - users: gestión de usuarios
  - conversation: sistema conversacional
  - plans: planes y rutinas
  - progress: seguimiento de progreso
  - notifications: notificaciones y feedback
  - ai: integración con modelos de IA
- **frontend/**: Proyecto Next.js, estructura modular y escalable.

## Recomendaciones
- Mantener la documentación y el backlog actualizados.
- Documentar cada endpoint, modelo y funcionalidad.
- Usar control de versiones (Git) y ramas para nuevas features.
- Implementar pruebas para el sistema conversacional.
- Monitorear calidad de extracción de datos.
- Mantener logs de conversaciones para mejora continua. 