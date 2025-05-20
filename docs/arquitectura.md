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

## Diagrama de Flujo (MVP)

```ascii
+-------------------+
|   Registro/Login  |
+-------------------+
          |
          v
+-------------------+
|  Preguntas IA/Plan|
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

**Descripción:**
1. El usuario se registra o inicia sesión.
2. La IA realiza preguntas para personalizar el plan.
3. Se genera un plan de entrenamiento personalizado.
4. El usuario sigue una rutina diaria (entrenamiento o descanso).
5. El usuario marca su progreso y puede subir fotos/medidas.
6. El sistema envía notificaciones y recoge feedback para mejorar la experiencia.

## Modelo de Datos (Resumen)
- Usuario: datos personales, foto, autenticación
- PreguntaPlan: preguntas editables por admin
- RespuestaPlan: respuestas de usuario a preguntas
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
- **backend/**: Proyecto Django, con apps separadas por dominio (users, plans, progress, notifications, ai).
- **frontend/**: Proyecto Next.js, estructura modular y escalable.

## Recomendaciones
- Mantener la documentación y el backlog actualizados.
- Documentar cada endpoint, modelo y funcionalidad.
- Usar control de versiones (Git) y ramas para nuevas features. 