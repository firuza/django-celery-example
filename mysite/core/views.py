from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView

from .forms import GenerateRandomUserForm, GenerateSimulationForm
from .tasks import create_random_user_accounts, create_simulation

from django.core.files.storage import FileSystemStorage
import uuid, os

from .models import Simulations

from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import ColumnDataSource
import pandas as pd

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
        myfile = self.request.FILES['cirfile_link']
        fs = FileSystemStorage()
        uid=uuid.uuid4().hex # Unique name
        filename = fs.save(uid+'.cir', myfile) #Save the file on system with unique name
        cirfile = os.getcwd() + '/media/' + filename #Get entire file path and name

        #Save record: cirfile, created by
        self.object = form.save(commit=False)
        self.object.cirfile_link = cirfile #Circuit file link
        savecontent(cirfile, self.object, 'netlist_content')
        self.object.created_by = self.request.user
        self.object.save()

        create_simulation.delay(cirfile, uid, self.object.pk)
        messages.success(self.request, 'simulation is being created')
        return redirect('viewsimulationlist')

class ViewSimulationList(ListView):
    model = Simulations
    context_object_name = 'simulations'
    template_name = 'core/view_simulation_list.html'

    def get_queryset(self):
        return Simulations.objects.filter(created_by=self.request.user)

class ViewSimulation(DetailView):
    model = Simulations
    context_object_name = 'simulation'
    template_name = 'core/view_simulation.html'

def savecontent(filename, obj, field):
    f = open(filename,"r")
    if f.mode == "r":
        contents = f.read()

        # using setattr to set value of a field, where fieldname is passed to the function
        # self.object.<fieldname> = contents
        setattr(obj, field, contents)


def showbokehplot(self):
    d = pd.read_csv('media/AC1.ssv.data', sep=' ', header=None, usecols=[1,2], names=['f', 'A'])
    plot = figure(title='ph(out)', x_axis_type="log", x_axis_label='f [Hz]', y_axis_label='V', plot_width=600, plot_height=400)
    plot.line(x='f', y='A', source=ColumnDataSource(d), legend='Ideal Response')
    script, div = components(plot)
    return render(self, 'core/plotbokeh.html', {'script':script, 'div':div})
