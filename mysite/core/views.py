from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView

from .forms import GenerateRandomUserForm, GenerateSimulationForm
from .tasks import create_random_user_accounts, create_simulation

from django.core.files.storage import FileSystemStorage
import uuid, os

from .models import Simulations

class UsersListView(ListView):
    template_name = 'core/users_list.html'
    model = User


class GenerateRandomUserView(FormView):
    template_name = 'core/generate_random_users.html'
    form_class = GenerateRandomUserForm

    def form_valid(self, form):
        total = form.cleaned_data.get('total')
        create_random_user_accounts.delay(total)
        messages.success(self.request, 'We are generating your random users! Wait a moment and refresh this page.')
        return redirect('users_list')

class GenerateSimulation(CreateView):
    template_name = 'core/generate_simulation.html'
    form_class = GenerateSimulationForm

    def form_valid(self, form):
        # Get file 
        myfile = self.request.FILES['cirfile']
        fs = FileSystemStorage()
        uid=uuid.uuid4().hex # Unique name
        filename = fs.save(uid+'.cir', myfile) #Save the file on system with unique name
        cirfile = os.getcwd() + '/media/' + filename #Get entire file path and name

        #Save record: cirfile, created by
        self.object = form.save(commit=False)
        self.object.cirfile = cirfile
        self.object.created_by = self.request.user
        self.object.save()

        create_simulation.delay(cirfile, uid, self.object.pk)
        messages.success(self.request, 'simulation is being created')
        return redirect('users_list')

class ViewSimulationList(ListView):
    model = Simulations
    context_object_name = 'simulations'
    template_name = 'core/view_simulation_list.html'

class ViewSimulation(DetailView):
    model = Simulations
    context_object_name = 'simulation'
    template_name = 'core/view_simulation.html'
