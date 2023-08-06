from django.db import models

from django.apps import apps


class GOStatus(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=128)
    parent_obj_description = models.CharField(max_length=128) #'$appname___$modelname
    next_statuses = models.CharField(max_length=256, blank=True, null=True, \
            default='')
    is_entrant = models.BooleanField(default=False)
    is_leaving = models.BooleanField(default=False)
    is_forward = models.BooleanField(default=True)
    is_backward = models.BooleanField(default=False)

    def get_next_statuses(self):
        return GOStatus.objects.filter(\
                parent_obj_description=self.parent_obj_description).filter(\
                code__in=self.next_statuses.split('|'))

    def add_status(self, name):
        if not self.next_statuses:
            self.next_statuses = ''
        if '|%s|' % name in self.next_statuses:
            return True
        else:
            if not self.next_statuses.startswith('|'):
                self.next_statuses = '|%s' % self.next_statuses
            if not self.next_statuses.endswith('|'):
                self.next_statuses += '|'
            self.next_statuses += '%s|' % name
            self.save()

    def remove_status(self, name):
        if '|%s|' % name in self.next_statuses:
            self.next_statuses = self.next_statuses.replace('%s|' % name, '')
            self.save()

    def add_statuses(self, name_lst):
        self.next_statuses = '|%s|' % '|'.join(sorted(name_lst))
        self.save()


    def get_model(self):
        try:
            pob = self.parent_obj_description.split('___')
            return apps.get_model(pob[0], pob[1])
        except:
            return False


    def __str__(self):
        return '%s -> %s' % (self.code, self.next_statuses)
