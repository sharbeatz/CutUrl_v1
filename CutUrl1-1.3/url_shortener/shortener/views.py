from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import URL
from .forms import URLForm
import string, random

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def home(request):
    url_data = URL.objects.order_by('-created_at')
    short_code = None
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url = form.save(commit=False)
            url.short_code = generate_short_code()
            if request.user.is_authenticated:
                url.user = request.user
            else:
                url.user = None
            url.save()
            short_code = url.short_code
            form = URLForm()  # Сброс формы после успешного создания URL
    else:
        form = URLForm()
    return render(request, 'shortener/home.html', {'form': form, 'short_code': short_code})

@login_required
def user_urls(request):
    url_list = URL.objects.filter(user=request.user).order_by('-created_at')

    paginator = Paginator(url_list, 10)  # Показывать 10 URL на каждой странице
    page = request.GET.get('page')
    try:
        urls = paginator.page(page)
    except PageNotAnInteger:
        # Если page не является целым числом, отображаем первую страницу
        urls = paginator.page(1)
    except EmptyPage:
        # Если page находится за пределами допустимых значений (например, 9999), отображаем последнюю страницу результатов
        urls = paginator.page(paginator.num_pages)

    return render(request, 'shortener/user_urls.html', {'urls': urls})

@login_required
def edit_url(request, short_code):
    url = get_object_or_404(URL, short_code=short_code, user=request.user)
    if request.method == 'POST':
        form = URLForm(request.POST, instance=url)
        if form.is_valid():
            form.save()
            return redirect('user_urls')
    else:
        form = URLForm(instance=url)
    return render(request, 'shortener/edit_url.html', {'form': form, 'short_code': short_code})

@login_required
def delete_url(request, short_code):
    url = get_object_or_404(URL, short_code=short_code, user=request.user)
    if request.method == 'POST':
        url.delete()
        return redirect('user_urls')
    return render(request, 'shortener/delete_url.html', {'url': url})

def redirect_to_original(request, short_code):
    url = get_object_or_404(URL, short_code=short_code)
    return redirect(url.original_url)
