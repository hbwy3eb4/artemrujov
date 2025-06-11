from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Family, FamilyMember, Comment
from .forms import FamilyForm, FamilyMemberForm, CommentForm
from .utils import build_tree
from django.conf import settings
# Create your views here.
from .models import Post

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('family_tree')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



    



@login_required
def family_tree(request):
    # Получаем или создаем семью для пользователя
    family, created = Family.objects.get_or_create(creator=request.user)
    
    if request.method == 'POST':
        form = FamilyMemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.family = family
            member.save()
            return redirect('family_tree')
    else:
        form = FamilyMemberForm()
    
    # Строим дерево
    root_members = family.members.filter(parents__isnull=True)
    tree = []
    for member in root_members:
        tree.append(build_tree(member))
    
    context = {
        'family': family,
        'tree': tree,
        'form': form,
        'yandex_maps_api_key': settings.YANDEX_MAPS_API_KEY
    }
    return render(request, 'family/family_tree.html', context)

@login_required
def member_detail(request, member_id):
    member = get_object_or_404(FamilyMember, id=member_id)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.member = member
            comment.author = request.user
            comment.save()
            return redirect('member_detail', member_id=member_id)
    else:
        comment_form = CommentForm()
    
    context = {
        'member': member,
        'comments': member.comments.all().order_by('-created_at'),
        'comment_form': comment_form,
        'yandex_maps_api_key': settings.YANDEX_MAPS_API_KEY
    }
    return render(request, 'family/member_detail.html', context)