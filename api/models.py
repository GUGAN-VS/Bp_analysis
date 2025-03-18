from django.db import models

class BPRecord(models.Model):
    patient_id = models.CharField(max_length=100)
    systolic = models.IntegerField()
    diastolic = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_id} - {self.systolic}/{self.diastolic} - {self.created_at}"


