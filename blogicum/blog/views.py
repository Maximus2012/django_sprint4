from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.paginator import Paginator
from blog.models import Post, Category, Comment
from blog.forms import  PostForm, CommentForm

# Create your views here.
from django.utils import timezone


def post_detail(request, post_id):
    template = "blog/detail.html"
    
    post = get_object_or_404(
        Post, pk=post_id
    )
    comments = Comment.objects.filter(post_id=post_id)

    if post.category and not post.category.is_published:
        raise Http404("Пост относится к категории, снятой с публикации.")

    return render(request, template, {"post": post, "comments": comments})


def category_posts(request, category_slug):
    template = "blog/category.html"
    # Получение объекта категории
    category_object = get_object_or_404(
        Category, slug=category_slug,
        is_published=True,
        created_at__lte=timezone.now()
    )
    # Фильтрация публикаций категории
    posts = Post.objects.filter(
        category=category_object,
        is_published=True,
        pub_date__lte=timezone.now(),
    ).order_by('-pub_date')

    # Пагинация
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Контекст
    context = {
        "page_obj": page_obj,  # Ожидаемый ключ контекста
        "category": category_object,
    }
    return render(request, template, context)


def index(request):
    template = "blog/index.html"
    category_object = Category.objects.filter(is_published=True)
    page_obj = Post.objects.all().filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__in=category_object,
        ).order_by('-pub_date',"-id" )
    paginator = Paginator(page_obj, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj
        
    }
    
    return render(request, template, context)

def create_post(request, pk=None):
    template = "blog/create.html"

    instance = None
    form = PostForm(
        request.POST or None,
        # Файлы, переданные в запросе, указываются отдельно.
        files=request.FILES or None,
        instance=instance,
    )

    if form.is_valid():
        form.instance.author_id = request.user.id
        form.save()
 
 
    return render(request, template, context={'form': form})

def profile(request, username):
    template = "blog/profile.html"

    page_obj = Post.objects.all().filter(author_id=request.user.id,
                                         ).order_by('-pub_date')
    paginator = Paginator(page_obj, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj":  page_obj,
        'profile': {'get_full_name': username} 
    }
    context['profile'].update({
    'date_joined': request.user.date_joined,
    'is_staff': request.user.is_staff,

})
    
    return render(request, template, context=context)


def add_comment(request):
    template = "blog/detail.html"

    form = CommentForm(
        request.POST or None,
        # Файлы, переданные в запросе, указываются отдельно.
    )
    context = {'form': form}

    if form.is_valid():

        form.save()
        
    return render(request, template, context)


def post_delete(request, pk):
    template = "blog/detail.html"
    # Получаем объект модели или выбрасываем 404 ошибку.
    instance = get_object_or_404(Post, pk=pk)
    # В форму передаём только объект модели;
    # передавать в форму параметры запроса не нужно.
    form = PostForm(instance=instance)
    context = {'form': form}
    # Если был получен POST-запрос...
    if request.method == 'POST':
        # ...удаляем объект:
        instance.delete()
        # ...и переадресовываем пользователя на страницу со списком записей.
        return redirect('blog:profile')
    # Если был получен GET-запрос — отображаем форму.
    return render(request, template, context)


def comment_delete(request, pk, comment_pk):
    pass

def comment(request, pk, comment_pk):
    pass
