from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Subject
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            username = u_form.cleaned_data.get('username')
            messages.success(request, f' {username} Your account has been Updated !')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'appquiz/profile.html', context)


class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Subject
    success_url = '/subjects'
    template_name = 'AppQuiz/Subject/delete.html'


class SubjectListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Subject
    template_name = 'AppQuiz/Subject/index.html'
    context_object_name = 'subject'
    paginate_by = 2

    def test_func(self):
        return self.request.user.is_superuser


class SubjectCreateView(LoginRequiredMixin, CreateView):
    model = Subject
    success_url = '/subjects'
    template_name = 'AppQuiz/Subject/create.html'
    fields = ['name', 'color']


class SubjectUpdateView(LoginRequiredMixin,  UpdateView):
    model = Subject
    success_url = '/subjects'
    template_name = 'AppQuiz/Subject/update.html'
    fields = ['name', 'color']

