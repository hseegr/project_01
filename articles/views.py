from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin

class CategoryListView(ListView):
    model = Article
    template_name = 'articles/category_list.html'
    context_object_name = 'articles'
    login_url = '/accounts/login/'

    def get_queryset(self):
        category = self.kwargs.get('category')
        return Article.objects.filter(category=category).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs.get('category')
        return context

class MainPageView(ListView):
    model = Article
    template_name = 'articles/main_page.html'
    context_object_name = 'articles'
    login_url = '/accounts/login/'
    
    def get_queryset(self):
        return Article.objects.all().order_by('-created_at')
    
@login_required
def articles_list(request):
   keys_to_clear = [key for key in request.session.keys() if key.startswith('viewed_article_')]
   for key in keys_to_clear:
       del request.session[key]
   
   articles = Article.objects.all().order_by('-created_at')
   context = {
       'articles': articles,
   }
   return render(request, 'articles/articles_list.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('articles:main_page')
    else:
        form = ArticleForm()
    context ={
        'form' : form,
    }
    return render(request, 'articles/create.html', context)

@login_required
def articles_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    # 조회수 증가 로직: 로그인한 유저의 ID 기반으로 관리
    if request.user.is_authenticated:  # 유저가 로그인한 경우
        # 유저의 조회 기록 확인
        if not article.views_set.filter(user=request.user).exists():  
            article.views += 1
            article.save()
            article.views_set.create(user=request.user)  # 조회 기록 생성
    else:  # 비로그인 유저는 기존 세션 기반으로 관리
        session_key = f'viewed_article_{article_pk}'  # 세션 키 설정
        if session_key not in request.session:
            article.views += 1
            article.save()
            request.session[session_key] = True

    # 댓글 작성 및 대댓글 작성 처리
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            content = data.get("content")
            parent_comment_id = data.get("parent_comment_id", None)

            if not content:
                return JsonResponse({"success": False, "error": "댓글 내용을 입력해주세요."})

            if parent_comment_id:
                parent_comment = get_object_or_404(Comment, id=parent_comment_id)
                comment = Comment.objects.create(
                    article=article,
                    author=request.user,
                    content=content,
                    parent_comment=parent_comment
                )
            else:
                comment = Comment.objects.create(
                    article=article,
                    author=request.user,
                    content=content
                )

            return JsonResponse({
                "success": True,
                "comment_id": comment.id,
                "nickname": comment.author.nickname,
                "author": comment.author.username,
                "content": comment.content,
                "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    # 댓글 목록 가져오기
    comments = Comment.objects.filter(article=article, parent_comment=None).order_by("-created_at")
    context = {
        "article": article,
        "comments": comments,
    }
    return render(request, "articles/detail.html", context)
    
    # # 댓글 조회
    # comments = Comment.objects.filter(article=article, parent_comment=None).order_by("-created_at")
    # context = {
    #     "article": article,
    #     "comments": comments,
    # }
    # return render(request, "articles/detail.html", context)

@login_required
def toggle_like(request):
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        article = get_object_or_404(Article, id=article_id)

        if article.likes.filter(id=request.user.id).exists():
            article.likes.remove(request.user)  # 좋아요 취소
            liked = False
        else:
            article.likes.add(request.user)  # 좋아요 추가
            liked = True

        return JsonResponse({
            'liked': liked,
            'total_likes': article.likes.count(),
        })

@login_required
def articles_delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if article.author != request.user:
        return JsonResponse({'error': '권한이 없습니다.'}, status=403)  # 권한이 없음을 알리는 응답

    article.delete()  # 게시글 삭제
    return redirect('articles:main_page')

@login_required
def articles_update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:articles_detail', article.pk)
    else:
        form = ArticleForm(instance=article)
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'articles/update.html', context)

@login_required
def comment_delete(request, comment_id):
   if request.method == "POST":
       comment = get_object_or_404(Comment, id=comment_id)
       if comment.author == request.user:
           comment.delete()
           return JsonResponse({"success": True})
   return JsonResponse({"success": False, "error": "권한이 없습니다."})

    