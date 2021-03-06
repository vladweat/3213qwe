from statistics import mode
from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.

from users.models import CustomUser


class Proposal(models.Model):

    # fields
    start_date = models.DateTimeField(default=datetime.now())
    long_name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    num_of_options = models.IntegerField(default=0)
    options = models.CharField(max_length=500)
    voters = models.IntegerField(default=0)
    end_date = models.DateTimeField(default=datetime.now())

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
        self.end_date = datetime.now()

    def get_end_date(self):
        return self.end_date
    
    def return_index_of_proposal(self, option):
        ops = self.options.split("*")
        index = ops.index(option)
        return index


class Option(models.Model):
    name = models.ForeignKey(Proposal, on_delete=models.CASCADE)


class VotingVoters(models.Model):
    voter = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    time_of_voting = models.DateTimeField(default=timezone.now)


class Web3Deploy(models.Model):
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    contract_address = models.CharField(max_length=200, default="")
