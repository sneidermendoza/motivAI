# motivAI

Tu motivación, potenciada por IA

---

## Visión
Aplicación web para crear, seguir y adaptar planes de entrenamiento personalizados, con ayuda de inteligencia artificial. Pensada para quienes buscan salud, motivación y progreso, especialmente quienes trabajan muchas horas sentados.

## Stack Tecnológico
- **Backend:** Django (Python)
- **Frontend:** Next.js (PWA, React)
- **Base de datos:** MariaDB/MySQL (desarrollo), migrable a PostgreSQL
- **IA:** Modelos open source (GPT4All, Llama.cpp, HuggingFace)
- **Notificaciones:** Push API (PWA)

## Estructura del Proyecto
```
motivAI/
├── README.md
├── docs/
├── backlog/
├── logo/
├── backend/
│   ├── manage.py
│   ├── backend/         # Configuración principal de Django (settings.py, urls.py, etc.)
│   ├── users/           # App de usuarios (incluye modelos de gamificación)
│   ├── plans/
│   ├── progress/
│   ├── notifications/
│   ├── feedback/
│   └── ... (otras apps)
└── frontend/
```

## Plan de Trabajo
El plan de trabajo y las prioridades del proyecto están documentados en:
- [`docs/plan_trabajo.md`](docs/plan_trabajo.md) (checklist editable y seguimiento)
- [`backlog/motivAI-backlog.csv`](backlog/motivAI-backlog.csv) (tareas y prioridades)

Aquí encontrarás todas las tareas, subtareas y mejoras futuras, ordenadas por prioridad y área.

- **Tareas principales:** Desarrollo de modelos, endpoints, integración IA, seguimiento de usuario, notificaciones, feedback y documentación.
- **Mejoras futuras:** Gamificación, integración con dispositivos externos, planes de nutrición, comunidad.

Consulta estos archivos para ver el estado y responsables de cada tarea.

## Cómo contribuir
1. Revisa el backlog, el plan de trabajo y el README para entender el estado actual del proyecto.
2. Consulta la documentación técnica en `docs/`.
3. Si quieres colaborar, abre un issue o haz un fork y pull request.
4. Mantén la documentación y el backlog actualizados con cada cambio.

## Branding
- Nombre: **motivAI**
- Paleta de colores, logo y favicon en `docs/branding.md` y `logo/`

## Enlaces útiles
- [Plan de trabajo (checklist)](docs/plan_trabajo.md)
- [Backlog de tareas](backlog/motivAI-backlog.csv)
- [Documentación técnica](docs/arquitectura.md)

---

> Proyecto personal, código abierto y en constante evolución. ¡Súmate o aporta ideas!

- Modelos principales: Usuario, Plan, Rutina, Ejercicio, Progreso, Notificación, Feedback, PreguntaPlan, RespuestaPlan
- Gamificación: Logro, UsuarioLogro 