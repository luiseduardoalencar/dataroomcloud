from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from django.utils import timezone

from django.db import models
from django.utils.timezone import now
from django.conf import settings


class Diretorio(models.Model):
    nome = models.CharField('Nome do Diretório', max_length=255)
    descricao = models.TextField('Descrição', blank=True, null=True)

    class Meta:
        verbose_name = 'Diretório'
        verbose_name_plural = 'Diretórios'

    def __str__(self):
        return self.nome


class Subdiretorio(models.Model):
    nome = models.CharField('Nome do Subdiretório', max_length=255)
    descricao = models.TextField('Descrição', blank=True, null=True)
    diretorio = models.ForeignKey(Diretorio, on_delete=models.CASCADE, related_name='subdiretorios')

    class Meta:
        verbose_name = 'Subdiretório'
        verbose_name_plural = 'Subdiretórios'

    def __str__(self):
        return f"{self.diretorio.nome} / {self.nome}"


class Arquivo(models.Model):
    titulo = models.CharField('Título do Arquivo', max_length=255)
    arquivo = models.FileField('Arquivo', upload_to='arquivos/')
    descricao = models.TextField('Descrição', blank=True, null=True)
    subdiretorio = models.ForeignKey(Subdiretorio, on_delete=models.CASCADE, related_name='arquivos')
    data_envio = models.DateTimeField('Data de Envio', default=timezone.now)
    enviado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Arquivo'
        verbose_name_plural = 'Arquivos'

    def __str__(self):
        return self.titulo


class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, name, password=None):
        if not username:
            raise ValueError('O nome de usuário é obrigatório')
        if not email:
            raise ValueError('O email é obrigatório')
        if not name:
            raise ValueError('O nome completo é obrigatório')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, name, password):
        user = self.create_user(
            username=username,
            email=email,
            name=name,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Nome de Usuário', max_length=150, unique=True)
    email = models.EmailField('Email', unique=True)
    name = models.CharField('Nome Completo', max_length=255)
    is_active = models.BooleanField('Ativo', default=True)
    is_staff = models.BooleanField('Membro da Equipe', default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']

    def get_short_name(self):
        return self.name.split(' ')[0]  

    def get_full_name(self):
        return self.name

    def __str__(self):
        return self.username

class Consideracao(models.Model):
    arquivo = models.ForeignKey(Arquivo, on_delete=models.CASCADE, related_name='consideracoes')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    descricao = models.TextField('Descrição', blank=True, null=True)
    arquivo_consideracao = models.FileField('Arquivo da Consideração', upload_to='consideracoes/')
    data_envio = models.DateTimeField('Data de Envio', auto_now_add=True)
    is_aprovada = models.BooleanField(default=False)  

    class Meta:
        verbose_name = 'Consideração'
        verbose_name_plural = 'Considerações'

    def __str__(self):
        return f"Consideração por {self.usuario.get_full_name()} em {self.data_envio.strftime('%d/%m/%Y %H:%M')}"
