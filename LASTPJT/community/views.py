from unicodedata import category
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_safe, require_GET, require_POST, require_http_methods
from .models import Community, CommunityComment
from .forms import CommunityForm, CommunityCommentForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Create your views here.
@login_required
@require_GET
def index(request):
    if request.user.is_authenticated:
        communitys = Community.objects.order_by('-pk')
        commus_announce = Community.objects.filter(category="('공지',)")
        commus_chat = Community.objects.filter(category="('잡담',)")
        commus_review = Community.objects.filter(category="('영화리뷰',)")
        commus_event = Community.objects.filter(category="('극장/이벤트',)")
        commus_etc = Community.objects.filter(category="('기타',)")
        context = {
            'communitys': communitys,
            'commus_announce':commus_announce,
            'commus_chat':commus_chat,
            'commus_review':commus_review,
            'commus_event':commus_event,
            'commus_etc':commus_etc,
        }
        print(context)
        return render(request, 'community/index.html', context)
    return redirect('accounts:login')


@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = CommunityForm(request.POST, request.FILES)
        if form.is_valid():
            community = form.save(commit=False)
            community.user = request.user
            community.save()
            return redirect('community:detail', community.pk)
    else:
        form = CommunityForm()
    context = {
        'form': form,
    }
    return render(request, 'community/create.html', context)


@require_safe
def detail(request, community_pk):
    community = get_object_or_404(Community, pk=community_pk)
    comments = community.communitycomment_set.all()
    comment_form = CommunityCommentForm()
    context = {
        'community': community,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'community/detail.html', context)


@require_POST
def delete(request, community_pk):
    if request.user.is_authenticated:
        community = get_object_or_404(Community, pk=community_pk)
        community.delete()
    return redirect('community:index')


@login_required
@require_http_methods(["GET", "POST"])
def update(request, community_pk):
    community = get_object_or_404(Community, pk=community_pk)

    if request.method == 'POST':
        form = CommunityForm(request.POST, files=request.FILES, instance=community)
        if form.is_valid():
            form.save()
            return redirect('community:detail', community.pk)
    else:
        form = CommunityForm(instance=community)
    context = {
        'form': form,
        'community': community,
    }
    return render(request, 'community/update.html', context)


@require_POST
def like(request, community_pk):
    if request.user.is_authenticated:
        community = get_object_or_404(Community, pk=community_pk)
        user = request.user

        if community.like.filter(pk=user.pk).exists():
            community.like.remove(user)
            like = False
        else:
            community.like.add(user)
            like = True
        return JsonResponse({'like':like, 'count':community.like.count()})
    else:
        community = get_object_or_404(Community, pk=community_pk)
        return JsonResponse({'like':False, 'count':community.like.count()})


@require_POST
def comment_create(request, community_pk):
    if request.user.is_authenticated:
        community = get_object_or_404(Community, pk=community_pk)
        comment_form = CommunityCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.title = community
            comment.user = request.user
            comment.save()
        return redirect('community:detail', community.pk)
    return redirect('accounts:login')


@require_POST
def comment_delete(request, community_pk ,comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(CommunityComment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('community:detail', community_pk)

@login_required
@require_http_methods(["GET", "POST"])
def comments_update(request, community_pk, comment_pk):
    comment = CommunityComment.objects.get(pk = comment_pk)
    if request.method == "POST":
        form = CommunityCommentForm(request.POST, instance = comment)
        if form.is_valid():
            form.save()
            return redirect('community:detail', community_pk)

    return_form = CommunityCommentForm(instance = comment)
    context = {
        'form':return_form,
    }
    return render(request, 'community/comments_update.html', context)


@require_GET
def index_commu1(request):
    communitys = Community.objects.filter(category="('공지',)").order_by('-pk')
    commus_all = Community.objects.all()
    commus_chat = Community.objects.filter(category="('잡담',)")
    commus_review = Community.objects.filter(category="('영화리뷰',)")
    commus_event = Community.objects.filter(category="('극장/이벤트',)")
    commus_etc = Community.objects.filter(category="('기타',)")
    context = {
        'communitys': communitys,
        'commus_all':commus_all,
        'commus_chat':commus_chat,
        'commus_review':commus_review,
        'commus_event':commus_event,
        'commus_etc':commus_etc,
    }
    print(context)
    return render(request, 'community/index_commu1.html', context)


@require_GET
def index_commu2(request):
    communitys = Community.objects.filter(category="('잡담',)").order_by('-pk')
    commus_all = Community.objects.all()
    commus_announce = Community.objects.filter(category="('공지',)")
    commus_review = Community.objects.filter(category="('영화리뷰',)")
    commus_event = Community.objects.filter(category="('극장/이벤트',)")
    commus_etc = Community.objects.filter(category="('기타',)")
    context = {
        'communitys': communitys,
        'commus_all':commus_all,
        'commus_announce':commus_announce,
        'commus_review':commus_review,
        'commus_event':commus_event,
        'commus_etc':commus_etc,
    }
    print(context)
    return render(request, 'community/index_commu2.html', context)


@require_GET
def index_commu3(request):
    communitys = Community.objects.filter(category="('영화리뷰',)").order_by('-pk')
    commus_all = Community.objects.all()
    commus_announce = Community.objects.filter(category="('공지',)")
    commus_chat = Community.objects.filter(category="('잡담',)")
    commus_event = Community.objects.filter(category="('극장/이벤트',)")
    commus_etc = Community.objects.filter(category="('기타',)")
    context = {
        'communitys': communitys,
        'commus_all':commus_all,
        'commus_announce':commus_announce,
        'commus_event':commus_event,
        'commus_etc':commus_etc,
        'commus_chat':commus_chat,

    }
    print(context)
    return render(request, 'community/index_commu3.html', context)


@require_GET
def index_commu4(request):
    communitys = Community.objects.filter(category="('극장/이벤트',)").order_by('-pk')
    commus_all = Community.objects.all()
    commus_announce = Community.objects.filter(category="('공지',)")
    commus_chat = Community.objects.filter(category="('잡담',)")
    commus_review = Community.objects.filter(category="('영화리뷰',)")
    commus_etc = Community.objects.filter(category="('기타',)")
    context = {
        'communitys': communitys,
        'commus_all':commus_all,
        'commus_announce':commus_announce,
        'commus_chat':commus_chat,
        'commus_etc':commus_etc,
        'commus_review':commus_review,
    }
    print(context)
    return render(request, 'community/index_commu4.html', context)


@require_GET
def index_commu5(request):
    communitys = Community.objects.filter(category="('기타',)").order_by('-pk')
    commus_all = Community.objects.all()
    commus_announce = Community.objects.filter(category="('공지',)")
    commus_chat = Community.objects.filter(category="('잡담',)")
    commus_review = Community.objects.filter(category="('영화리뷰',)")
    commus_event = Community.objects.filter(category="('극장/이벤트',)")
    context = {
        'communitys': communitys,
        'commus_all':commus_all,
        'commus_announce': commus_announce,
        'commus_chat':commus_chat,
        'commus_review':commus_review,
        'commus_event':commus_event,
    }
    print(context)
    return render(request, 'community/index_commu5.html', context)