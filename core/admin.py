from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import Usuario, Diretorio, Subdiretorio, Arquivo, Consideracao

@admin.register(Diretorio)
class DiretorioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)

@admin.register(Subdiretorio)
class SubdiretorioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'diretorio', 'descricao')
    list_filter = ('diretorio',)
    search_fields = ('nome',)

@admin.register(Arquivo)
class ArquivoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'subdiretorio', 'data_envio', 'enviado_por', 'arquivo_link')
    list_filter = ('subdiretorio', 'data_envio')
    search_fields = ('titulo',)
    readonly_fields = ('enviado_por', 'data_envio')

    fieldsets = (
        (None, {
            'fields': ('titulo', 'arquivo', 'descricao', 'subdiretorio')
        }),
    )

    def save_model(self, request, obj, form, change):
        # Atribuir o usuário atual como quem enviou o arquivo
        if not obj.enviado_por:
            obj.enviado_por = request.user
        super().save_model(request, obj, form, change)
        self.message_user(request, f"Arquivo '{obj.titulo}' enviado com sucesso!")

    def arquivo_link(self, obj):
        if obj.arquivo:
            return format_html('<a href="{}" target="_blank">Abrir Arquivo</a>', obj.arquivo.url)
        return "Nenhum arquivo"
    arquivo_link.short_description = "Link do Arquivo"

class CustomUserAdmin(UserAdmin):
    model = Usuario
    list_display = ('username', 'email', 'name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    ordering = ('username',)
    search_fields = ('username', 'email', 'name')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('email', 'name')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'name', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

admin.site.register(Usuario, CustomUserAdmin)


@admin.register(Consideracao)
class ConsideracaoAdmin(admin.ModelAdmin):
    list_display = ('arquivo', 'usuario', 'data_envio', 'is_aprovada')
    list_filter = ('is_aprovada',)
    search_fields = ('usuario__username', 'arquivo__titulo', 'descricao')
