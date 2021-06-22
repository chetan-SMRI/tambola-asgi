from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, ClockedSchedule
from .tasks import run_game
# Create your models here.
class TicketLimit(models.Model):
	limit_value = models.IntegerField(default=600,validators=[MinValueValidator(1),MaxValueValidator(600)])

	class Meta:
		db_table='ticket_limit_no'
		verbose_name_plural = "Ticket Limit"

def generate_half_sheet_choices():
	try:
		limit_value = TicketLimit.objects.first().limit_value
	except:
		limit_value = 600
	limit_value = int(limit_value/3)
	choices = []
	for i in range(1, limit_value+1):
		temp_list = [i*3-2, i*3-1, i*3]
		choices.append(('-'.join(str(e) for e in temp_list),'-'.join(str(e) for e in temp_list),))
	return choices

def generate_full_sheet_choices():
	try:
		limit_value = TicketLimit.objects.first().limit_value
	except:
		limit_value = 600
	limit_value = int(limit_value / 6)
	choices = []
	for i in range(1, limit_value + 1):
		temp_list = [i * 6 - 5, i * 6 - 4, i * 6 - 3, i * 6 - 2, i * 6 - 1, i * 6]
		choices.append(('-'.join(str(e) for e in temp_list),'-'.join(str(e) for e in temp_list),))
	return choices


HALF_SHEET_CHOICES = generate_half_sheet_choices()
FULL_SHEET_CHOICES = generate_full_sheet_choices()

ACHIEVEMENTS = (
	("full_house", "Full House"),
	("second_full_house", "Second Full House"),
	("third_full_house","Third Full House"),
	("line_1", "Line 1"),
	("line_2", "Line 2"),
	("line_3", "Line 3"),
	('star', 'Star'),
	('quick_five', 'Quick Five'),
	('quick_seven','Quick Seven'),
	('corner','Corner'),
	('full_sheet','Full Sheet'),
	('half_sheet','Half Sheet'),
)


class Ticket(models.Model):
	ticket_no = models.IntegerField(unique=True)
	ticket_digits = models.CharField(max_length=150)

	def __str__(self):
		return 'Ticket No '+str(self.ticket_no)
	
	class Meta:
		db_table = 'ticket'

class BookTicketQuerySet(models.QuerySet):
	def delete(self, *args, **kwargs):
		for obj in self:
			#print("Deleting Ticket "+str(obj.ticket.ticket_no))
			for i in HalfSheet.objects.all():
				if str(obj.ticket.ticket_no) in i.select_tickets.split("-"):
					i.delete()
					print("Found HalfSheet entry for ticket")
			for i in FullSheet.objects.all():
				if str(obj.ticket.ticket_no) in i.select_tickets.split("-"):
					i.delete()
					print("Found FullSheet entry for ticket")

		super(BookTicketQuerySet, self).delete(*args, **kwargs)


class BookTicket(models.Model):
	objects = BookTicketQuerySet.as_manager()
	added_by = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	username = models.CharField(max_length=255)
	date = models.DateField(auto_now=True)
	email = models.EmailField(blank=True)
	phone = models.CharField(max_length=50)
	address = models.TextField(max_length=2000)
	ticket = models.OneToOneField(Ticket,on_delete=models.CASCADE)	
	def __str__(self):
		return self.username

	class Meta:
		db_table='book_ticket'	
		verbose_name_plural = "Book Ticket"



class BannerImage(models.Model):
	image = models.ImageField(blank=True,null=True)

	class Meta:
		db_table = 'banner_image'
		verbose_name_plural = "Banner Image"


class TicketDailyData(models.Model):
	date = models.DateField(auto_now=True, unique=True)
	ticket_digits = models.TextField(max_length=2000)
	class Meta:
		verbose_name_plural = "Ticket Daily Data"


class WinnerData(models.Model):		
	date = models.DateField(auto_now=True)
	ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL,blank=True,null=True)	
	achievement = models.CharField(choices=ACHIEVEMENTS,max_length=100)
	last_called_no = models.IntegerField(default=0)
	half_sheet = models.CharField(max_length = 255,blank=True,null=True)
	full_sheet = models.CharField(max_length = 255,blank=True,null=True)
	def __str__(self):		
		return str(str(self.date) + " " + str(self.achievement))
	class Meta:
		verbose_name_plural = "Match Winners"
class ScheduleGame(models.Model):
	schedule_time = models.DateTimeField(default=timezone.now,blank=True,null=True)	
	class Meta:
		verbose_name_plural = "Set Time"
	
	def save(self):
		clocked_obj = ClockedSchedule.objects.get_or_create(clocked_time=self.schedule_time)

		check = PeriodicTask.objects.filter(name="TambolaGame")		
		if check:
			check.update(clocked=clocked_obj[0], name="TambolaGame", task='game.tasks.run_game',one_off=True,enabled=True)
		else:
			PeriodicTask.objects.create(clocked=clocked_obj[0], name="TambolaGame", task='game.tasks.run_game',one_off=True,enabled=True)
		super().save()

class GameplayStatus(models.Model):
	game_started = models.BooleanField(default=False,blank=True)
	game_over = models.BooleanField(default=True,blank=True)
	class Meta:
		verbose_name = "Game Stop"

class WhoWillWin(models.Model):
	winner_type = models.CharField(
		verbose_name="Type",
		max_length=20,
		choices=ACHIEVEMENTS,
		unique=True
		)
	winner_ticket = models.ForeignKey(Ticket,on_delete=models.DO_NOTHING)
	class Meta:
		verbose_name_plural = "System Winners"
	def __str__(self):
		return str(self.winner_type)


class SetDivident(models.Model):
    full_house = models.IntegerField(
        verbose_name="No. Of Houses",
        choices=(
            (1, 1),
            (2, 2),
            (3, 3),
        ),
        default=1
        )
    first_line =  models.BooleanField(default=True, verbose_name="Line 1")
    second_line = models.BooleanField(default=True, verbose_name="Line 2")
    third_line =  models.BooleanField(default=True, verbose_name="Line 3")
    quickfive =   models.BooleanField(default=True, verbose_name="Quick Five")
    quickseven =  models.BooleanField(default=False, verbose_name="Quick Seven")
    star =        models.BooleanField(default=True, verbose_name="Star")
    corner =      models.BooleanField(default=False, verbose_name="Corner")
    half_sheet =  models.BooleanField(default=True, verbose_name="Half Sheet")
    full_sheet =  models.BooleanField(default=False, verbose_name="Full Sheet")

    class Meta:
        verbose_name_plural = "Change Dividend"
        db_table = 'Dividend'

    def __str__(self):
        return 'Configuration'

class SetGameDelay(models.Model):
    Delay = models.IntegerField(default=10, validators=[MinValueValidator(5), MaxValueValidator(20)]
                                , help_text="Delay Between Calling Numbers In The Game (In Sec)")

    class Meta:
        verbose_name_plural = "Game Delay"

    def __str__(self):
        return 'Configuration'


class HalfSheet(models.Model):
	select_tickets = models.CharField(max_length=255,choices=HALF_SHEET_CHOICES,unique=True)
	username = models.CharField(max_length=255)
	address = models.TextField()
	email = models.EmailField(blank=True)
	phone = models.CharField(max_length=50)
	added_by = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)

	class Meta:
		verbose_name_plural = 'Book Half Sheet'


class FullSheet(models.Model):
	select_tickets = models.CharField(max_length=255,choices=FULL_SHEET_CHOICES,unique=True)
	username = models.CharField(max_length=255)
	address = models.TextField()
	email = models.EmailField(blank=True)
	phone = models.CharField(max_length=50)
	added_by = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)

	class Meta:
		verbose_name_plural = 'Book Full Sheet'

from django.contrib.auth.models import User,Group
from django.dispatch import receiver #add this
from django.db.models.signals import post_save #add this
from django import forms

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	CHOICES = (
	("Admin","Admin"),
	("Developer", "Developer"),
	("SuperUser","SuperUser"),
	("Agent","Agent")
	)
	User_Type = models.CharField(max_length=20,default="Agent", choices=CHOICES)
	Phone = models.CharField(max_length=20,default="-")
	def save(self, *args, **kwargs):
		self.user.groups.clear()
		group = Group.objects.get(name=self.User_Type)
		self.user.groups.add(group)
		super(Profile, self).save(*args, **kwargs)
	@receiver(post_save, sender=User) #add this
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)
			sss = User.objects.get(username=instance)
			sss.is_staff=True
			sss.save()

	@receiver(post_save, sender=User) #add this
	def save_user_profile(sender, instance, **kwargs):
		try:
		    instance.profile.save()
		except:
		    pass
	def __str__(self):
		return self.user.username 

class SuspendDate(models.Model):
    suspend_date = models.DateField(default=timezone.now)
    def __str__(self):
        return str(self.suspend_date)


		    
@receiver(post_save, sender=HalfSheet)
def update_half_sheet_tickets(instance, *args, **kwargs):
	tickets = instance.select_tickets.split('-')
	for ticket in tickets:
		ticket_obj = Ticket.objects.get(ticket_no=int(ticket))
		BookTicket.objects.filter(ticket=ticket_obj).update(added_by=instance.added_by)

@receiver(post_save, sender=FullSheet)
def update_full_sheet_tickets(instance, *args, **kwargs):
	tickets = instance.select_tickets.split('-')
	for ticket in tickets:
		ticket_obj = Ticket.objects.get(ticket_no=int(ticket))
		BookTicket.objects.filter(ticket=ticket_obj).update(added_by=instance.added_by) 


