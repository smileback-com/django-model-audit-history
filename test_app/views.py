from django.forms import ModelForm
from django.shortcuts import render, redirect

from .models import BlogPost


class BlogPostForm(ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'position', 'created_on']


def edit(request, id):
    post = BlogPost.objects.get(id=int(id))

    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            post.save_with_audit_record(None, 'CHANGE_VIA_FORM', payload=form.cleaned_data)
            return redirect('edit', id=id)

    else:
        form = BlogPostForm(instance=post)

    return render(request, 'edit.html', {'id': id, 'form': form})
