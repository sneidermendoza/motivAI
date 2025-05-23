## Soft delete y filtrado por estado

### Campo `status`
- Todos los endpoints de planes, rutinas y ejercicios incluyen el campo `status`.
- Valores posibles: `activo`, `inactivo`.

### Eliminación lógica (soft delete)
- El endpoint DELETE no borra físicamente, solo marca el objeto como `inactivo`.
- Ejemplo:

```http
DELETE /api/plans/planentrenamiento/1/
```

Respuesta:
```json
{
  "success": true,
  "message": "Plan marcado como inactivo (eliminación lógica).",
  "data": null
}
```

### Filtrado por estado
- Listar solo activos (por defecto):

```http
GET /api/plans/planentrenamiento/
```

- Listar inactivos:

```http
GET /api/plans/planentrenamiento/?status=inactivo
```

Respuesta:
```json
{
  "success": true,
  "message": "Listado obtenido correctamente",
  "data": [
    { "id": 1, "objetivo": "Ganar músculo", "status": "inactivo", ... },
    ...
  ]
}
```

### Permisos para eliminar (soft delete)
- **Planes/Rutinas:** Solo el dueño o admin puede eliminar.
- **Ejercicios:** Cualquier usuario autenticado puede eliminar.

### Checklist de comportamiento esperado
- El objeto no se borra físicamente, solo cambia su `status`.
- Los listados solo muestran activos por defecto.
- Se puede filtrar por inactivos.
- Los tests automáticos cubren soft delete y filtrado. 