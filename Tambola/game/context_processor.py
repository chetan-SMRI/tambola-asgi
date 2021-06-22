from .models import *
from django.db.models import *

def admin_stats(request):
    ticket_limit = TicketLimit.objects.all().last()
    if not ticket_limit:
        limit = 600
    else:
        limit = ticket_limit.limit_value
    booked_tickets = BookTicket.objects.all().count()
    try:
        if request.user.profile.User_Type == "Developer" or request.user.profile.User_Type == "Admin":
            booked_tickets_status = list(BookTicket.objects.all().values('added_by__username').annotate(total=Count('added_by')))
        else:
            booked_tickets_status = None
    except:
        booked_tickets_status = None
    return {'unsold_tickets':limit-booked_tickets,'sold_tickets':booked_tickets,"booked_tickets_status":booked_tickets_status} 

