from django.contrib import admin
from .models import *
from game.forms import BookTicketForm, HalfSheetBookingForm, FullSheetBookingForm
from django.shortcuts import render, redirect
#Overwriting Admin Site
from django.contrib import admin
from django.contrib.auth.models import *
from django.http import HttpResponse
from django.apps import apps
from Tambola.settings import WEBSITE_DISPLAY_NAME,WEBSITE_TITLE_NAME
from django.contrib import messages
from datetime import timedelta
from django.utils import timezone

# for app_config in apps.get_app_configs():
#     if app_config.name == "django.contrib.auth":        
#         pass
#     else:
#         for model in app_config.get_models():
#             if admin.site.is_registered(model):
#                 admin.site.unregister(model)

admin.site.site_header = WEBSITE_DISPLAY_NAME
admin.site.site_title = WEBSITE_TITLE_NAME
admin.site.index_title = 'Admin Panel'

@admin.register(SuspendDate)
class suspendAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def history_view(self, request, object_id, extra_context=None):
        return False
    def changelist_view(self, request, extra_context=None):
        return redirect('/admin/game/suspenddate/1/change/')

# Register your models here.
@admin.register(ScheduleGame)
class setTimeAdmin(admin.ModelAdmin):
    change_list_template = "set_time_change_list.html"
    list_display = ["schedule_game"]
    list_display_links = ['schedule_game']

    def schedule_game(self,obj):
        return "Schedule Game"

    def get_model_perms(self, request):
        qs = super(setTimeAdmin, self).get_model_perms(request)
        
        if request.user.profile.User_Type == "Developer" or request.user.profile.User_Type == "Admin":
            return qs
        return {}

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def history_view(self, request, object_id, extra_context=None):
        return False

@admin.register(Ticket)
class TicketsAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        qs = super(TicketsAdmin, self).get_model_perms(request)
        if request.user.profile.User_Type == "Developer" or request.user.profile.User_Type == "Admin":
            return qs
        return {}
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False
    def history_view(self, request, object_id, extra_context=None):
        return False


@admin.register(BookTicket)
class BookTicketAdmin(admin.ModelAdmin):
    change_list_template = "book_ticket_list.html"
    list_display = ['username', 'ticket', 'added_by','date']
    readonly_fields = ['added_by']
    search_fields = ('username', 'ticket__ticket_no', 'address', 'phone', 'added_by__username')
    ordering = ['ticket','-date']
    
    def get_queryset(self, request):
        if timezone.now().date() >= SuspendDate.objects.first().suspend_date -  timezone.timedelta(days=7):
            if (SuspendDate.objects.first().suspend_date - timezone.now().date()).days < 0:
                self.message_user(request, "Your Website Is Suspended , Renew It Immediately", level=messages.ERROR)
            else:
                self.message_user(request, "Your Server Is Getting Suspended In "+str((SuspendDate.objects.first().suspend_date - timezone.now().date()).days)+" Day(s),Admins Are Required To Renew It", level=messages.ERROR)
        if request.user.profile.User_Type == "Developer" or request.user.profile.User_Type == "Admin":
            return BookTicket.objects.all()
        else:
            return BookTicket.objects.filter(added_by=request.user)

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        obj.save()

class DividendAdmin(admin.ModelAdmin):
    list_display = ['change_dividend','full_house', 'first_line', 'second_line', 'third_line', 'quickfive',
                    'quickseven', 'star', 'corner', 'half_sheet', 'full_sheet']
    list_display_links = ['change_dividend']

    def change_dividend(self,obj):
        return "Change Dividend"
        
    def get_model_perms(self, request):
            qs = super(DividendAdmin, self).get_model_perms(request)
            if request.user.profile.User_Type == "Developer" or request.user.profile.User_Type == "Admin":
                return qs
            return {}
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def history_view(self, request, object_id, extra_context=None):
        return False

    def changelist_view(self, request, extra_context=None):
        return redirect('/admin/game/setdivident/1/change/')

class SetGameDelayAdmin(admin.ModelAdmin):
    list_display = ['set_game_delay']
    list_display_links = ['set_game_delay']

    def set_game_delay(self, obj):
        return 'Set Game Delay'

    def get_model_perms(self, request):
            qs = super(SetGameDelayAdmin, self).get_model_perms(request)
            if request.user.profile.User_Type == "Developer" or request.user.profile.User_Type == "Admin":
                return qs
            return {}
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def history_view(self, request, object_id, extra_context=None):
        return False
    def changelist_view(self, request, extra_context=None):
        return redirect('/admin/game/setgamedelay/1/change/')


class TicketLimitAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
            qs = super(TicketLimitAdmin, self).get_model_perms(request)
            if request.user.profile.User_Type == "Developer" or request.user.profile.User_Type == "Admin":
                return qs
            return {}
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def history_view(self, request, object_id, extra_context=None):
        return False

    def changelist_view(self, request, extra_context=None):
        return redirect('/admin/game/ticketlimit/1/change/')


admin.site.register(SetDivident, DividendAdmin)
admin.site.register(TicketLimit, TicketLimitAdmin)
admin.site.register(SetGameDelay, SetGameDelayAdmin)



@admin.register(GameplayStatus)
class TicketAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        qs = super(TicketAdmin, self).get_model_perms(request)
        if request.user.profile.User_Type == "Developer":
            return qs
        return {}
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False


from django_celery_beat.models import (
    PeriodicTask, PeriodicTasks,
    IntervalSchedule, CrontabSchedule,
    SolarSchedule, ClockedSchedule
)
from django_celery_results.models import TaskResult
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(PeriodicTask)
admin.site.unregister(TaskResult)

from django import forms

class ProfileForm(forms.ModelForm):
    CHOICES = (
            ("Admin","Admin"),
            ("Agent","Agent")
    )
    User_Type = forms.ChoiceField(choices=CHOICES)
    class Meta:
        model = Profile
        fields = '__all__'
    

from django.db.models import Q

#@admin.register(Profile)
#class ProfileAdmin(admin.ModelAdmin):
#    list_display = ['user', 'User_Type']
#    def get_queryset(self, request):
#        qs = super(ProfileAdmin, self).get_queryset(request)
#        if request.user.profile.User_Type == "Developer":
#            return qs
#        elif request.user.profile.User_Type == "Admin":
#            return qs.filter(Q(User_Type="Agent") | Q(User_Type="Admin"))
#    def get_model_perms(self, request):
#        qs = super(ProfileAdmin, self).get_model_perms(request)
#        if request.user.profile.User_Type == "Developer" or request.user.profile.User_Type == "Admin":
#            return qs
#        return {}
#    def get_form(self, request,*args, **kwargs):
#        form = ProfileForm
#        return form
@admin.register(WhoWillWin)
class SystemWinnerAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        qs = super(SystemWinnerAdmin, self).get_model_perms(request)
        if request.user.profile.User_Type == "Developer" or request.user.profile.User_Type == "SuperUser":
            return qs
        return {}
        
@admin.register(BannerImage)
class BannerImageAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        qs = super(BannerImageAdmin, self).get_model_perms(request)
        if request.user.profile.User_Type == "Developer" or request.user.profile.User_Type == "Admin":
            return qs
        return {}
    def has_add_permission(self, request):
        if BannerImage.objects.first() == None:    
            return True
        return False
@admin.register(WinnerData)
class WinnersAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if request.user.profile.User_Type == "Developer" or request.user.profile.User_Type == "Admin":
            super().save_model(request, obj, form, change)
        else:
            return

    def get_model_perms(self, request):
        qs = super(WinnersAdmin, self).get_model_perms(request)
        if request.user.profile.User_Type == "Developer" or request.user.profile.User_Type == "Admin" or request.user.profile.User_Type == "Agent":
            return qs
        return {}
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False

from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q
from django.utils.translation import ugettext, ugettext_lazy as _

admin.site.unregister(User)
#admin.site.unregister(Group)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    form = ProfileForm
    

@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
    (None, {'fields': ('username', 'password')}),

    (_('Personal info'), {'fields': ('first_name', 'last_name')}),        
    )
    list_display = ('username', 'first_name', 'last_name', 'get_Type', 'get_phone')
    def get_Type(self, instance):
        return instance.profile.User_Type
    get_Type.short_description = 'Role'
    def get_phone(self, instance):
        return instance.profile.Phone
    get_phone.short_description = 'Phone'

    inlines = (ProfileInline, )
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)
    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        #return qs
        try:
            request.user.profile.User_Type
        except:
            request.user.profile.objects.create(user=request.user, User_Type="Agent")
        if request.user.profile.User_Type == "Developer":
            return qs
        elif request.user.profile.User_Type == "Admin":
            #return qs.filter(profile__User_Type="Agent")
            return qs.filter(Q(profile__User_Type="Agent") | Q(profile__User_Type="Admin"))

    def get_model_perms(self, request):
        qs = super(UserAdmin, self).get_model_perms(request)
        if request.user.profile.User_Type == "Developer":
            return qs
        elif request.user.profile.User_Type == "Admin":
            return qs
            #return User.objects.filter(profile__User_Type="Agent")
        return {}
