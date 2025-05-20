from django.contrib import admin
from .models import User, Logro, UsuarioLogro

# Register your models here.
admin.site.register(User)
admin.site.register(Logro)
admin.site.register(UsuarioLogro)
