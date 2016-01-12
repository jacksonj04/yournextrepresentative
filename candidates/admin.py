from django.contrib import admin

from django.core.urlresolvers import reverse
from django.forms import ModelForm

from .models import LoggedAction, PartySet
# Register your models here.


class LoggedActionAdminForm(ModelForm):
    pass


class LoggedActionAdmin(admin.ModelAdmin):
    form = LoggedActionAdminForm
    search_fields = ('user__username', 'popit_person_new_version',
                     'person', 'ip_address', 'source')
    list_filter = ('action_type',)
    list_display = ['user', 'ip_address', 'action_type',
                    'popit_person_new_version', 'person_link',
                    'created', 'updated', 'source']
    ordering = ('-created',)

    def person_link(self, o):
        if not o.person:
            return ''
        url = reverse('person-view', kwargs={'person_id': o.person.id})
        return '<a href="{0}">{1}</a>'.format(
            url,
            o.person.name,
        )
    person_link.allow_tags = True


class PartySetAdminForm(ModelForm):
    pass


class PartySetAdmin(admin.ModelAdmin):
    form = PartySetAdminForm


admin.site.register(LoggedAction, LoggedActionAdmin)
admin.site.register(PartySet, PartySetAdmin)
