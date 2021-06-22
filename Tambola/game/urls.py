from django.urls import path
from .views import *
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path('',Homepage.as_view(),name='home'),
    path('get-tickets',LoadTicket.as_view(),name='get-tickets'),    
    path('last-no-called',LastNoCalled.as_view(),name='last_no_called'),    
    path('ticket-status',staff_member_required(CheckTicketStatus.as_view()),name='check_ticket_status'),
    path('reset-game',reset_game_manually,name='reset_game'),
    path('start_game',start_task_manually,name="start_game"),
    path('agentlist',agentlist,name="agentlist"),
    path('multiticketbook',multiticketbook,name="multiticketbook"),
    path('show_hs',show_hs,name="show_hs"),
    path('show_fs',show_fs,name="show_fs"),
    path('del_sheets',del_sheets,name="del_sheets"),
]
