import string

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from celery import shared_task
import uuid, os
from .models import Simulations

@shared_task
def create_random_user_accounts(total):
    for i in range(total):
        username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
        email = '{}@example.com'.format(username)
        password = get_random_string(50)
        User.objects.create_user(username=username, email=email, password=password)
    return '{} random users created with success!'.format(total)


@shared_task
def create_simulation(cirfile, uid, pk):
    cmd = 'ngspice -b ' + cirfile + ' >  ' + os.getcwd()+'/media/'+ uid + '_out.txt'
    os.system(cmd)
    sim = Simulations.objects.get(pk=pk)
    outfile_link = os.getcwd()+'/media/'+ uid + '_out.txt'
    sim.outfile_link = outfile_link
    f = open(outfile_link,"r")
    if f.mode == "r":
        contents = f.read()
        sim.simulation_output_text = contents    
    sim.save()
    return 'Output file generated'    
