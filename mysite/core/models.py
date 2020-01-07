from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Simulations(models.Model):
    name = models.CharField(max_length=50)
    cirfile_link = models.FileField()
    outfile_link = models.FileField()
    netlist_content = models.TextField(null=True)
    simulation_output_text = models.TextField(null=True)
    created_by = models.ForeignKey(User, null=True)
    created_on = models.DateTimeField(null=True)

    def __str__(self):
        return self.name + ' - ' + str(self.created_by)