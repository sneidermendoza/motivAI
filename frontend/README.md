# motivAI Frontend (Next.js)

## Descripción
Frontend de motivAI, construido con Next.js, TypeScript y Tailwind CSS. Este proyecto consume la API REST del backend y ofrece una experiencia moderna, responsiva y accesible para los usuarios.

---

## Estructura recomendada del proyecto

```plaintext
frontend/
├── public/                   # Archivos estáticos (imágenes, favicon, manifest, etc.)
├── src/
│   ├── app/                  # Rutas y páginas (Next.js App Router)
│   │   ├── layout.tsx        # Layout global
│   │   ├── page.tsx          # Página principal
│   │   ├── auth/             # Rutas de autenticación (login, register, reset-password)
│   │   ├── profile/          # Perfil de usuario
│   │   ├── chat/             # Conversación principal
│   │   ├── plans/            # Planes y rutinas
│   │   ├── progress/         # Progreso del usuario
│   │   ├── notifications/    # Notificaciones
│   │   ├── feedback/         # Feedback y sugerencias
│   │   └── ...               # Otras rutas
│   ├── components/           # Componentes reutilizables (Button, Card, Modal, Navbar, etc.)
│   ├── features/             # Features o módulos por dominio
│   │   ├── auth/             # Lógica y hooks de autenticación
│   │   ├── chat/             # Lógica y hooks de conversación
│   │   ├── plans/            # Lógica y hooks de planes
│   │   ├── progress/         # Lógica y hooks de progreso
│   │   ├── notifications/    # Lógica y hooks de notificaciones
│   │   ├── feedback/         # Lógica y hooks de feedback
│   │   └── ...
│   ├── hooks/                # Custom hooks globales (useAuth, useFetch, useChat, etc.)
│   ├── services/             # Lógica de consumo de API (axios/fetch, endpoints centralizados)
│   │   ├── api.ts            # Configuración de axios/fetch
│   │   ├── authService.ts    # Endpoints de autenticación
│   │   ├── chatService.ts    # Endpoints de conversación
│   │   ├── planService.ts    # Endpoints de planes
│   │   ├── progressService.ts# Endpoints de progreso
│   │   ├── notificationService.ts # Endpoints de notificaciones
│   │   └── ...
│   ├── utils/                # Utilidades y helpers generales
│   ├── context/              # Contextos globales (AuthContext, ThemeContext, etc.)
│   ├── styles/               # Archivos CSS/Tailwind personalizados
│   ├── i18n/                 # Archivos de internacionalización (si aplica)
│   ├── types/                # Tipos y modelos TypeScript compartidos
│   └── tests/                # Pruebas unitarias y de integración
├── .env.local                # Variables de entorno locales
├── next.config.ts            # Configuración de Next.js
├── tailwind.config.js        # Configuración de Tailwind CSS
├── tsconfig.json             # Configuración de TypeScript
├── package.json
└── ...otros archivos de configuración
```

### Ejemplos de nombres y estándares por feature

- **Autenticación:**
  - `src/app/auth/login/page.tsx`, `src/features/auth/useLogin.ts`, `src/services/authService.ts`
- **Conversación:**
  - `src/app/chat/page.tsx`, `src/features/chat/useChat.ts`, `src/services/chatService.ts`
- **Planes:**
  - `src/app/plans/page.tsx`, `src/features/plans/usePlan.ts`, `src/services/planService.ts`
- **Progreso:**
  - `src/app/progress/page.tsx`, `src/features/progress/useProgress.ts`, `src/services/progressService.ts`
- **Notificaciones:**
  - `src/app/notifications/page.tsx`, `src/features/notifications/useNotifications.ts`, `src/services/notificationService.ts`
- **Feedback:**
  - `src/app/feedback/page.tsx`, `src/features/feedback/useFeedback.ts`, `src/services/feedbackService.ts`
- **Componentes globales:**
  - `src/components/Button.tsx`, `src/components/Card.tsx`, `src/components/Navbar.tsx`
- **Hooks globales:**
  - `src/hooks/useAuth.ts`, `src/hooks/useFetch.ts`, `src/hooks/useModal.ts`
- **Contextos:**
  - `src/context/AuthContext.tsx`, `src/context/ThemeContext.tsx`
- **Tipos:**
  - `src/types/User.ts`, `src/types/Plan.ts`, `src/types/Chat.ts`, etc.

### ¿Por qué esta estructura?
- Facilita el trabajo en equipo y el escalado del proyecto.
- Permite separar lógica, UI y consumo de API por dominio.
- Promueve la reutilización y el mantenimiento.
- Alineada con las mejores prácticas de Next.js y la comunidad React moderna.

---

## Recomendaciones y estándares
- Mantener la estructura modular y coherente.
- Usar TypeScript en todo el proyecto.
- Seguir la paleta de colores y branding definidos en `docs/branding.md`.
- Documentar cada componente, hook y servicio.
- Mantener la carpeta `services/` como única fuente de consumo de API.
- Usar hooks y contextos para manejo de estado global.
- Priorizar la accesibilidad y la experiencia de usuario.
- Mantener actualizado este README y el plan de trabajo.

---

## Instalación y uso rápido

```bash
cd frontend
npm install
npm run dev
```

Configura las variables de entorno en `.env.local` según los endpoints del backend.

---

**¡Listos para construir el frontend MVP de motivAI! 🚀**

---

## Historial de avances y flujos implementados

### Estructura y configuración
- Proyecto Next.js + TypeScript + Tailwind + ESLint/Prettier configurado.
- Estructura modular: separación de features, servicios, hooks, contextos y componentes reutilizables.
- Branding y estilos base aplicados.

### Autenticación y usuarios
- Registro y login de usuario con JWT (formulario, validaciones, integración backend).
- Logout y gestión de sesión (tokens en localStorage y cookies).
- Contexto global de autenticación.
- Login social (Google/Facebook) con callback y loader.

### Recuperación de contraseña
- Formulario para solicitar email de recuperación.
- Envío de email con link seguro (flujo backend integrado).
- Página de restablecimiento de contraseña con validación de token y email.
- Formulario de nueva contraseña con validaciones y feedback.
- Branding y logo en la página de reset.

### Componentes y utilidades
- Inputs, botones, mensajes de error, branding reutilizables.
- Servicios centralizados para consumo de API.

### Documentación y plan de trabajo
- Documentación de estructura y recomendaciones en README.
- Plan de trabajo y backlog en docs/plan_trabajo_frontend.md.

---

### Siguiente tarea prioritaria para el MVP

**Implementar la interfaz de chat conversacional y conectar con el backend:**
- Crear la página principal de chat.
- Mostrar preguntas y opciones según el flujo recibido del backend.
- Enviar respuestas y manejar validaciones, aclaraciones y fallback.
- Visualizar el estado y contexto de la conversación.
- Este es el core del MVP y la prioridad máxima para avanzar.

---

## Actualización de UI/UX y navegación (Junio 2025)

- Se implementó un **sidebar lateral fijo** en desktop y un **tab bar fijo inferior** en mobile, usando Heroicons para los íconos de navegación.
- El layout ahora es completamente **responsive**: el contenido nunca queda debajo del menú, gracias a `md:pl-20`.
- Se creó el componente `UserAvatar` que muestra la foto de perfil (`foto_perfil`) o un ícono genérico si no hay imagen, junto al username.
- El botón de cerrar sesión ahora es un ícono accesible y nunca se desborda.
- Se eliminaron los problemas de solapamiento del logo y el contenido con el menú.
- **Librerías utilizadas:**
  - `@heroicons/react`: para todos los íconos de navegación y métricas.
  - `tailwindcss`: para estilos responsivos y utilidades de layout.
- Componentes nuevos:
  - `SidebarNav`: navegación lateral/tab bar.
  - `UserAvatar`: avatar de usuario reutilizable.
- El dashboard y el layout general ahora siguen las mejores prácticas de UX para apps modernas.
