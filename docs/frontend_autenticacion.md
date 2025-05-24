# Documentación de Autenticación Frontend motivAI

## Formularios implementados

- **Login:** Email y contraseña, validación con zod, feedback de error, enlaces a registro y recuperación, botones sociales.
- **Registro:** Nombre, email, contraseña, confirmar contraseña, validación robusta, feedback, botones sociales, enlace a login.
- **Restablecer contraseña:** Email, validación, mensaje de éxito, enlace a login.
- **Establecer contraseña:** Nueva contraseña y confirmación, validación, mensaje de éxito, enlace a login.
- **Autenticación social:** Botones de Google y Facebook, minimalistas, accesibles y reutilizables.

## Componentes reutilizables
- `InputField`, `Button`, `FormError`, `SocialAuthButtons`, `LoginForm`, `RegisterForm`, `ResetPasswordForm`, `SetPasswordForm`.

## Flujos y recomendaciones
- Todos los formularios usan `react-hook-form` + `zod` para validación.
- Los slides de autenticación se gestionan desde `AuthTabs`.
- Los enlaces de navegación entre formularios están dentro del contenedor blanco para evitar desbordes.
- Los botones sociales usan solo íconos y están centrados.
- El diseño es responsive y preparado para PWA.

## Ejemplo de uso de un formulario
```tsx
<LoginForm />
<RegisterForm onLogin={() => setForm('login')} />
<ResetPasswordForm onLogin={() => setForm('login')} />
<SetPasswordForm onLogin={() => setForm('login')} />
```

## Estructura de carpetas
```
frontend/src/components/
  ├── auth/
  │   ├── LoginForm.tsx
  │   ├── RegisterForm.tsx
  │   ├── ResetPasswordForm.tsx
  │   ├── SetPasswordForm.tsx
  │   └── SocialAuthButtons.tsx
  ├── form/
  │   ├── InputField.tsx
  │   ├── Button.tsx
  │   └── FormError.tsx
  └── AuthTabs.tsx
```

## Recomendaciones
- Mantener los componentes desacoplados y reutilizables.
- Validar siempre en frontend y backend.
- Mejorar la accesibilidad y el feedback visual. 