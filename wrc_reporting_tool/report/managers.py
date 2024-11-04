from django.db import models


class SesizareQuerySet(models.QuerySet):
    def get_status_count(self):
        return self.values('status').annotate(status_count=models.Count('status'))

    def get_conflict_count(self):
        return self.values('raportvoluntar__tip_conflict').annotate(conflict_count=models.Count('raportvoluntar__tip_conflict'))
