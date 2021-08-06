from django.db import models
from django.db.models import query

class EventQuery(models.QuerySet):
    def get_upcoming(self):
        queryset = self
        for i in queryset:
            if i.status() != 'Upcoming':
                queryset = queryset.exclude(id=i.id)
        
        return queryset

class EventManager(models.Manager):
    def get_queryset(self):
        return EventQuery(model=self.model, using=self._db)
    def get_upcoming(self):
        return self.get_queryset().get_upcoming()