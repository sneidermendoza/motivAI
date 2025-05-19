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