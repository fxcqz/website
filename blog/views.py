from itertools import zip_longest

from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory, widgets
from django.shortcuts import redirect, render
from .constants import CONFIG
from .models import ListItem, Post, Section


def front_page(request):
    sections = Section.objects.filter(enabled=True)
    return render(request, 'blog/front_page.html', {
        'sections': sections.filter(sidebar=False).order_by('-index'),
        'side_sections': sections.filter(sidebar=True).order_by('-index'),
        'config': CONFIG,
    })

@login_required
def profile(request):
    sections = Section.objects.all()
    display_sections = zip_longest(sections.filter(sidebar=False).order_by('-index'),
                                   sections.filter(sidebar=True).order_by('-index'),
                                   fillvalue='')
    return render(request, 'blog/profile.html', {
        'sections': sections.filter(model_name__isnull=True),
        'display_sections': display_sections,
        'config': CONFIG,
    })

@login_required
def add_items(request, section=None):
    extra = 5 if section is None else 0
    formset = modelformset_factory(
        ListItem, exclude=(), extra=extra, min_num=1,
        widgets={
            'title': widgets.TextInput(attrs={
                'style': 'width: 100%;',
            }),
            'url': widgets.Textarea(attrs={
                'rows': 1,
                'style': 'resize: none; height: 1.2rem; width: 100%;',
            }),
            'style': widgets.Textarea(attrs={
                'rows': 5,
            }),
        }
    )

    if request.POST:
        formset = formset(request.POST, request.FILES)
        if formset.is_valid():
            instances = formset.save()
            return redirect('profile')

    if section:
        formset = formset(queryset=ListItem.objects.filter(section__slug=section))
    else:
        formset = formset(queryset=ListItem.objects.none())

    return render(request, 'blog/add_items.html', {
        'config': CONFIG,
        'forms': formset,
        'adding': section is None,
    })


def view_post(request, post):
    post = Post.objects.get(slug=post)
    return render(request, 'blog/view_post.html', {
        'config': CONFIG,
        'post': post,
    })