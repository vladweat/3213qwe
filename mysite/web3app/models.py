from statistics import mode
from django.db import models
from django.utils import timezone
# Create your models here.

from users.models import CustomUser

class Proposal(models.Model):
    
    # fields
    start_date = models.DateTimeField(default=timezone.now)
    long_name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    num_of_options = models.IntegerField(default=0)
    options = models.IntegerField(default=0)
    voters = models.IntegerField(default=0)
    end_date = models.DateTimeField(default=timezone.now)
    
    # metadata
    class Meta:
        pass
    
    # methods
    def get_start_date(self):
        return self.start_date
     
    def set_status(self, status):
        if status == 0:
            self.status = "created"
        if status == 1:
            self.status = "progressed"
        if status == 2:
            self.status = "finished"
    
    def get_status(self):
        return self.status
    
    def set_end_date(self):
        self.end_date = timezone.now
    
    def get_end_date(self):
        return self.end_date
    
class Option(models.Model):
    name = models.ForeignKey(Proposal, on_delete=models.CASCADE)