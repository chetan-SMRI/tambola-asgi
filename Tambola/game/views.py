from django.shortcuts import render, redirect
from django.template import loader
from django.views.generic import TemplateView, View
from django.utils import timezone
from .models import *
from django.http import JsonResponse, HttpResponse
from django.utils.html import mark_safe
import ast
from celery.execute import send_task
from .tasks import run_game

from asgiref.sync import sync_to_async
from Tambola.settings import WEBSITE_DISPLAY_NAME,WEBSITE_TITLE_NAME, WEBSITE_WS_PORT
from django.utils import timezone

# Create your views here.

class Homepage(TemplateView):
    template_name = 'index.html'
    def get(self, request):
        request.session['reload'] = True
        context = {}
        context['banner_image'] = BannerImage.objects.all().last()
        ticket_limit = TicketLimit.objects.all().last()
        if not ticket_limit:
            limit = 600
        else:
            limit = ticket_limit.limit_value
        booked_tickets = BookTicket.objects.all().values('username','address','email','ticket__ticket_no','phone')
        context['tickets'] = Ticket.objects.all()[:limit]
        set_time = ScheduleGame.objects.all().last()
        game_play = GameplayStatus.objects.all().last()
        if (SuspendDate.objects.first().suspend_date - timezone.now().date()).days <= -1:
            return JsonResponse("Website is temporarily suspended, admins are required to renew it", safe=False) 
        if set_time:
            check_time = set_time.schedule_time - timezone.timedelta(minutes=30)
            if timezone.now() >= check_time:
                context['called_no_range'] = range(1,91)
                context['show_tickets'] = False
                context['time_obj'] = set_time
                context['limit'] = limit
                context['website_name'] = WEBSITE_DISPLAY_NAME
                context['website_title'] = WEBSITE_TITLE_NAME
                context['WEBSITE_WS_PORT'] = WEBSITE_WS_PORT
                return render(request,'game.html',context)
        context['todays_time'] = set_time
        context['show_tickets'] = True
        context['website_name'] = WEBSITE_DISPLAY_NAME
        context['website_title'] = WEBSITE_TITLE_NAME
        context['WEBSITE_WS_PORT'] = WEBSITE_WS_PORT
        agent_list = []
        agent_phone_list = []
        for agent in User.objects.filter(profile__User_Type="Agent"):
            if agent.profile.Phone == '-' or agent.profile.Phone == '' :
                pass
            else:
                if agent.first_name == "":
                    agent_list.append(agent.username)
                else:
                    agent_list.append(agent.first_name + " " + agent.last_name)
                agent_phone_list.append(agent.profile.Phone)
        context['agents'] = zip(agent_list,agent_phone_list)
        context['wantToShowAgents'] = False
        return render(request,self.template_name,context)

class LoadTicket(View):
    def post(self, *args, **kwargs):
        context = {}
        ticket_limit = TicketLimit.objects.all().last()
        if not ticket_limit:
            limit = 600
        else:
            limit = ticket_limit.limit_value
        booked_tickets = BookTicket.objects.all().values('username','address','email','ticket__ticket_no','phone')
        context['tickets'] = Ticket.objects.all()[:limit]
        context['show_tickets'] = True
        html = loader.render_to_string('tickets.html',context)
        return HttpResponse(html)


class LastNoCalled(View):
    play_audio = True
    def get(self,*args,**kwargs):
        get_reload = self.request.session['reload']
        
        if get_reload == True:
            self.request.session['reload'] = False
            play_audio = False
        else:
            play_audio = True
        ticket_data = TicketDailyData.objects.all().last()
        winner_data = WinnerData.objects.all()
        full_house_winner = WinnerData.objects.filter(achievement="full_house").values('ticket__ticket_no','ticket__bookticket__username')
        second_full_house_winner = WinnerData.objects.filter(achievement="second_full_house").values('ticket__ticket_no','ticket__bookticket__username')
        third_full_house_winner = WinnerData.objects.filter(achievement="third_full_house").values('ticket__ticket_no','ticket__bookticket__username')
        first_line_winner = WinnerData.objects.filter(achievement="line_1").values('ticket__ticket_no','ticket__bookticket__username')
        second_line_winner = WinnerData.objects.filter(achievement="line_2").values('ticket__ticket_no','ticket__bookticket__username')
        third_line_winner = WinnerData.objects.filter(achievement="line_3").values('ticket__ticket_no','ticket__bookticket__username')
        star_winner = WinnerData.objects.filter(achievement="star").values('ticket__ticket_no','ticket__bookticket__username')
        quickfive_winner = WinnerData.objects.filter(achievement="quick_five").values('ticket__ticket_no','ticket__bookticket__username')
        quickseven_winner = WinnerData.objects.filter(achievement="quick_seven").values('ticket__ticket_no','ticket__bookticket__username')
        corner = WinnerData.objects.filter(achievement="corner").values('ticket__ticket_no','ticket__bookticket__username')
        half_sheet = WinnerData.objects.filter(achievement="half_sheet").values('half_sheet')
        
        temp_half_sheet = []
        for half in half_sheet:
            temp  = {}
            temp['ticket__ticket_no']  = half['half_sheet']
            ticket = Ticket.objects.get(ticket_no=half['half_sheet'].split('-')[0])
            try:
                temp['ticket__bookticket__username'] = ticket.bookticket.username
            except:
                temp['ticket__bookticket__username'] = ''
            temp_half_sheet.append(temp)
        half_sheet = temp_half_sheet
        
        full_sheet = WinnerData.objects.filter(achievement="full_sheet").values('full_sheet')
        temp_full_sheet = []
        for half in full_sheet:
            temp  = {}
            temp['ticket__ticket_no']  = half['full_sheet']
            ticket = Ticket.objects.get(ticket_no=half['full_sheet'].split('-')[0])
            try:
                temp['ticket__bookticket__username'] = ticket.bookticket.username
            except:
                temp['ticket__bookticket__username'] = ''
            temp_full_sheet.append(temp)
        full_sheet = temp_full_sheet
        try:
            start_game = GameplayStatus.objects.all().last()
            game_over = start_game.game_over
            game_started = start_game.game_started
        except:
            game_over = False
            game_started = False
        b = {
            "Full_House": list(full_house_winner),
            "Second_House": list(second_full_house_winner),
            "Third_House":list(third_full_house_winner),
            "Line_1": list(first_line_winner),
            "Line_2": list(second_line_winner),
            "Line_3": list(third_line_winner),
            "Star": list(star_winner),
            "Quick_Five": list(quickfive_winner),
            "Quick_Seven":list(quickseven_winner),
            "Corner":list(corner),
            "Half_Sheet":list(half_sheet),
            "Full_Sheet":list(full_sheet),
            'game_over':game_over,
            'game_started':game_started,            
        }        
        try:
            numbers = ast.literal_eval(ticket_data.ticket_digits)
            return {"numbers": numbers,'winner_data':b,'play_audio':play_audio,"last_no":numbers[-1]}
        except Exception as e:
            print(e)
            return {"numbers":[],'winner_data':b,'play_audio':play_audio,"last_no":numbers[-1]}

@sync_to_async
def last_called_no():
        play_audio = True
        ticket_data = TicketDailyData.objects.all().last()
        winner_data = WinnerData.objects.all()
        full_house_winner = WinnerData.objects.filter(achievement="full_house").values('ticket__ticket_no','ticket__bookticket__username')
        second_full_house_winner = WinnerData.objects.filter(achievement="second_full_house").values('ticket__ticket_no','ticket__bookticket__username')
        third_full_house_winner = WinnerData.objects.filter(achievement="third_full_house").values('ticket__ticket_no','ticket__bookticket__username')
        first_line_winner = WinnerData.objects.filter(achievement="line_1").values('ticket__ticket_no','ticket__bookticket__username')
        second_line_winner = WinnerData.objects.filter(achievement="line_2").values('ticket__ticket_no','ticket__bookticket__username')
        third_line_winner = WinnerData.objects.filter(achievement="line_3").values('ticket__ticket_no','ticket__bookticket__username')
        star_winner = WinnerData.objects.filter(achievement="star").values('ticket__ticket_no','ticket__bookticket__username')
        quickfive_winner = WinnerData.objects.filter(achievement="quick_five").values('ticket__ticket_no','ticket__bookticket__username')
        quickseven_winner = WinnerData.objects.filter(achievement="quick_seven").values('ticket__ticket_no','ticket__bookticket__username')
        corner = WinnerData.objects.filter(achievement="corner").values('ticket__ticket_no','ticket__bookticket__username')
        half_sheet = WinnerData.objects.filter(achievement="half_sheet").values('half_sheet')
        temp_half_sheet = []
        for half in half_sheet:
            temp  = {}
            temp['ticket__ticket_no']  = half['half_sheet']
            ticket = Ticket.objects.get(ticket_no=half['half_sheet'].split('-')[0])
            try:
                temp['ticket__bookticket__username'] = ticket.bookticket.username
            except:
                temp['ticket__bookticket__username'] = ''
            temp_half_sheet.append(temp)
        half_sheet = temp_half_sheet
        
        full_sheet = WinnerData.objects.filter(achievement="full_sheet").values('full_sheet')
        temp_full_sheet = []
        for half in full_sheet:
            temp  = {}
            temp['ticket__ticket_no']  = half['full_sheet']
            ticket = Ticket.objects.get(ticket_no=half['full_sheet'].split('-')[0])
            try:
                temp['ticket__bookticket__username'] = ticket.bookticket.username
            except:
                temp['ticket__bookticket__username'] = ''
            temp_full_sheet.append(temp)
        full_sheet = temp_full_sheet
        try:
            start_game = GameplayStatus.objects.all().last()
            game_over = start_game.game_over
            game_started = start_game.game_started
        except:
            game_over = False
            game_started = False
        b = {
            "Full_House": list(full_house_winner),
            "Second_House": list(second_full_house_winner),
            "Third_House":list(third_full_house_winner),
            "Line_1": list(first_line_winner),
            "Line_2": list(second_line_winner),
            "Line_3": list(third_line_winner),
            "Star": list(star_winner),
            "Quick_Five": list(quickfive_winner),
            "Quick_Seven":list(quickseven_winner),
            "Corner":list(corner),
            "Half_Sheet":list(half_sheet),
            "Full_Sheet":list(full_sheet),
            'game_over':game_over,
            'game_started':game_started,            
        }        
        try:
            numbers = ast.literal_eval(ticket_data.ticket_digits)
            return {"numbers": numbers,'winner_data':b,'play_audio':play_audio,"last_no":numbers[-1]}
        except Exception as e:
            print(e)
            return {"numbers":[],'winner_data':b,'play_audio':play_audio,"last_no":numbers[-1]}


class CheckTicketStatus(TemplateView):
    template_name = "ticket_status.html"
    def get_context_data(self,*args,**kwargs):
        context = {}
        ticket_limit = TicketLimit.objects.all().last()
        if not ticket_limit:
            limit = 600
        else:
            limit = ticket_limit.limit_value
        context['tickets'] = range(1,limit+1)
        booked_tickets = list(BookTicket.objects.all().values_list('ticket__ticket_no',flat=True))
        booked_tickets = [int(i) for i in booked_tickets]
        context['booked_tickets'] = booked_tickets
        context['website_name'] = WEBSITE_DISPLAY_NAME
        context['website_title'] = WEBSITE_TITLE_NAME
        return context


def reset_game_manually(request):
    try:
        if request.user.profile.User_Type == "Developer" or request.user.profile.User_Type == "Admin":
            WinnerData.objects.all().delete()
            TicketDailyData.objects.all().delete()
            dataToSave = TicketDailyData.objects.create(
                ticket_digits=str([]),
            )
            dataToSave.save()
            game_play = GameplayStatus.objects.all().last()
            game_play.game_started = False
            game_play.game_over = False
            game_play.save()
        else:
            return JsonResponse({"fail":"You don't have permission."})
        return JsonResponse({"success":"Game has been resetted successfully !"})
    except:
        return JsonResponse({"fail":"You don't have permission."})
    
def start_task_manually(request):
    try:
        if request.user.profile.User_Type == "Developer" or request.user.profile.User_Type == "Admin":
            run_game.delay()
            return JsonResponse({'success':"Task run successfully"})
        else:
            return JsonResponse({"fail":"You don't have permission."})
    except:
        return JsonResponse({"fail":"You don't have permission."})

def agentlist(request):
    return JsonResponse({"Status":"Will Be Launched Soon."})

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

@staff_member_required
def multiticketbook(request):
    if request.method == "POST":
        username = request.POST.get('username')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        tickets = request.POST.get('tickets')
        agent = request.user
        print(username)
        print(address)
        print(phone)
        if len(tickets) != 0:
            ticket_list = tickets.split(',')
            for ticket in ticket_list:
                try:
                    if ticket.isdigit():
                        book = BookTicket.objects.create(username=username,address=address,phone=phone,ticket=Ticket.objects.get(ticket_no=int(ticket)),added_by=agent)
                        book.save()
                    else:
                        print('it was not an int')
                except:
                    messages.error('All Tickets Were Not Booked Successfully!')
                    return redirect('/ticket-status')
            messages.success(request, 'All Tickets Booked Successfully!')
            return redirect('/ticket-status')
    return JsonResponse({"Success":"All Tickets Were Booked Successfully !"})


def show_sheets(logged_user,fetchAll=False):

    def checkIfQueued(l):
        total = 0
        minimum = float('+inf')
        maximum = float('-inf')
        seen = set()
        for n in l:
            if n in seen:
                return False
            seen.add(n)
            if n < minimum:
                minimum = n
            if n > maximum:
                maximum = n
            total += n
        if 2 * total != maximum * (maximum + 1) - minimum * (minimum - 1):
            return False
    
        return True

    def indices(lst, element):
        result = []
        offset = -1
        while True:
            try:
                offset = lst.index(element, offset+1)
            except ValueError:
                return result
            result.append(offset)

    
    fullsheet_list = []
    halfsheet_list = []
    username_list = []
    user_username_list = []
    ticket_id = []
    #Getting All Booked Ticket's Username
    if fetchAll == False:
        for ticket in BookTicket.objects.filter(added_by=logged_user).order_by('ticket__ticket_no'):
            username_list.append(ticket.username)
            ticket_id.append(ticket.ticket.ticket_no)
    else:
        for ticket in BookTicket.objects.all().order_by('ticket__ticket_no'):
            username_list.append(ticket.username)
            ticket_id.append(ticket.ticket.ticket_no)
    
    #Removing Duplicate Combination Of Username
    for i in username_list:
        if i not in user_username_list:
            user_username_list.append(i)
    
    #Getting Fullsheet And Halfsheet
    for user in user_username_list:
        last_value = ticket_id[ len(username_list) - username_list[::-1].index(user) - 1]
        if username_list.count(user) == 6 and last_value % 6 == 0:
            lis = []
            for index in indices(username_list, user):
                lis.append(ticket_id[index])
            if checkIfQueued(lis):
                fullsheet_list.append(user)
        if username_list.count(user) == 3:
            lis = []
            for index in indices(username_list, user):
                lis.append(ticket_id[index])
            if checkIfQueued(lis):
                halfsheet_list.append(user)
    return {"halfsheet":halfsheet_list, "fullsheet":fullsheet_list}

import json
def show_hs(request):
    context = {}
    if request.user.profile.User_Type == "Developer" or request.user.profile.User_Type == "Admin":
        halfsheet_usernamed = json.loads(json.dumps(show_sheets(logged_user=request.user,fetchAll=True )))['halfsheet']
    else:
        halfsheet_usernamed = json.loads(json.dumps(show_sheets(logged_user=request.user)))['halfsheet']
    halfsheet_username = []
    halfsheet_tickets = []
    halfsheet_added_by = []
    for halfsheet_usernamess in halfsheet_usernamed:
        halfsheet_username.append(BookTicket.objects.filter(username=halfsheet_usernamess)[0].username)
        halfsheet_added_by.append(BookTicket.objects.filter(username=halfsheet_usernamess)[0].added_by.username)
        myArr = []
        for i in BookTicket.objects.filter(username=halfsheet_usernamess):
            myArr.append(str(i.ticket.ticket_no))
        res = str(myArr)[1:-1]
        res = res.replace("'", "")
        res = res.replace(",", "-")
        res = res.replace(" ", "")
        halfsheet_tickets.append(res)
    #print(halfsheet_username)
    #print(halfsheet_tickets)
    #print(halfsheet_added_by)
    context['website_name'] = WEBSITE_DISPLAY_NAME
    context['website_title'] = WEBSITE_TITLE_NAME
    context['halfsheets'] = zip(halfsheet_username,halfsheet_tickets,halfsheet_added_by)
    return render(request, 'show_hs.html', context)


def show_fs(request):
    context = {}
    if request.user.profile.User_Type == "Developer" or request.user.profile.User_Type == "Admin":
        fullsheet_usernamed = json.loads(json.dumps(show_sheets(logged_user=request.user,fetchAll=True )))['fullsheet']
    else:
        fullsheet_usernamed = json.loads(json.dumps(show_sheets(logged_user=request.user)))['fullsheet']
    fullsheet_username = []
    fullsheet_tickets = []
    fullsheet_added_by = []
    for fullsheet_usernamess in fullsheet_usernamed:
        fullsheet_username.append(BookTicket.objects.filter(username=fullsheet_usernamess)[0].username)
        fullsheet_added_by.append(BookTicket.objects.filter(username=fullsheet_usernamess)[0].added_by.username)
        myArr = []
        for i in BookTicket.objects.filter(username=fullsheet_usernamess):
            myArr.append(str(i.ticket.ticket_no))
        res = str(myArr)[1:-1]
        res = res.replace("'", "")
        res = res.replace(",", "-")
        res = res.replace(" ", "")
        fullsheet_tickets.append(res)
    #print(fullsheet_username)
    #print(fullsheet_tickets)
    #print(fullsheet_added_by)
    context['website_name'] = WEBSITE_DISPLAY_NAME
    context['website_title'] = WEBSITE_TITLE_NAME
    context['fullsheets'] = zip(fullsheet_username,fullsheet_tickets,fullsheet_added_by)
    return render(request, 'show_fs.html', context)
    
def del_sheets(request):
    try:
        q = str(request.GET.get('q')).split('-')
        q = list(filter(None, q))
        if request.user.profile.User_Type == "Developer" or request.user.profile.User_Type == "Admin":
            for ticket in q:
                BookTicket.objects.get(ticket=Ticket.objects.get(ticket_no=ticket)).delete()
        else:
            for ticket in q:
                if BookTicket.objects.get(ticket=Ticket.objects.get(ticket_no=ticket)).added_by == request.user:
                    BookTicket.objects.get(ticket=Ticket.objects.get(ticket_no=ticket)).delete()
                else:
                    return JsonResponse("Backend is strong dont try to penetrate", safe=False)
    except:
        return JsonResponse("Some Error Occured!", safe=False)
    return JsonResponse("Success!", safe=False)

