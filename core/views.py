from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Diretorio, Subdiretorio
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from .models import Usuario
from django.contrib.auth import logout
from django.contrib import messages
from .models import Arquivo, Consideracao
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        
        if password1 != password2:
            return render(request, 'registration/register.html', {
                'error': 'As senhas não coincidem!'
            })

        
        user = Usuario.objects.create(
            username=username,
            name=full_name,  
            email=email,
            password=make_password(password1)
        )
        user.save()
        login(request, user)  
        return redirect('home')  

    return render(request, 'registration/register.html')

@login_required
def home(request):
    diretorios = Diretorio.objects.all()  
    return render(request, 'core/home.html', {'diretorios': diretorios})

@login_required
def profile(request):
    return render(request, 'core/profile.html', {'user': request.user})

@login_required
def main_directories(request):
    diretorios = Diretorio.objects.all()
    return render(request, 'core/main_directories.html', {'diretorios': diretorios})

@login_required
def subdirectories(request, diretorio_id):
    diretorio = get_object_or_404(Diretorio, id=diretorio_id)
    subdiretorios = diretorio.subdiretorios.all()
    return render(request, 'core/subdirectories.html', {'diretorio': diretorio, 'subdiretorios': subdiretorios})

@login_required
def files(request, subdiretorio_id):
    subdiretorio = get_object_or_404(Subdiretorio, id=subdiretorio_id)
    arquivos = subdiretorio.arquivos.all()
    return render(request, 'core/files.html', {'subdiretorio': subdiretorio, 'arquivos': arquivos})

@login_required
def file_details(request, arquivo_id):
    arquivo = get_object_or_404(Arquivo, id=arquivo_id)

    consideracoes_aprovadas = arquivo.consideracoes.filter(is_aprovada=True)
    consideracoes_pendentes = arquivo.consideracoes.filter(is_aprovada=False)

    if request.method == 'POST':
        if 'aprovar' in request.POST:
            consideracao_id = request.POST.get('consideracao_id')
            consideracao = get_object_or_404(Consideracao, id=consideracao_id)
            consideracao.is_aprovada = True
            consideracao.save()
        elif 'rejeitar' in request.POST:
            consideracao_id = request.POST.get('consideracao_id')
            consideracao = get_object_or_404(Consideracao, id=consideracao_id)
            consideracao.delete()
        else:
            # Tratamento do envio da consideração
            descricao = request.POST.get('descricao')
            arquivo_consideracao = request.FILES.get('arquivo_consideracao')

            if arquivo_consideracao:
                Consideracao.objects.create(
                    arquivo=arquivo,
                    usuario=request.user,
                    descricao=descricao,
                    arquivo_consideracao=arquivo_consideracao
                )
                messages.success(request, "Consideração enviada com sucesso!")
            else:
                messages.error(request, "Erro ao enviar a consideração. O arquivo é obrigatório.")

        return HttpResponseRedirect(reverse('file_details', args=[arquivo_id]))

    return render(request, 'core/file_details.html', {
        'arquivo': arquivo,
        'consideracoes_aprovadas': consideracoes_aprovadas,
        'consideracoes_pendentes': consideracoes_pendentes,
    })

