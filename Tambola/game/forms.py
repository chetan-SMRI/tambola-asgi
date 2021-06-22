from django import forms
from .models import *
from django.core.exceptions import ValidationError
class BookTicketForm(forms.ModelForm):
    class Meta:
        model = BookTicket
        fields = "__all__"


class HalfSheetBookingForm(forms.ModelForm):    
    class Meta:
        model = HalfSheet
        fields = '__all__'
    
    def clean_select_tickets(self):                
        data = self.cleaned_data['select_tickets']
        tickets = data.split('-')
        if BookTicket.objects.filter(ticket__ticket_no__in=tickets).exists():
            raise ValidationError('This ticket is already booked')
        return data

    def save(self,commit=True):
        data= self.cleaned_data['select_tickets']        
        tickets = data.split('-')
        for ticket in tickets:
            ticket_obj = Ticket.objects.get(ticket_no=int(ticket))
            BookTicket.objects.create(ticket=ticket_obj,username=self.cleaned_data['username'],email=self.cleaned_data['username'],phone=self.cleaned_data['phone'],address=self.cleaned_data['address'])
        if commit:
            # If committing, save the instance and the m2m data immediately.
            self.instance.save()
            self._save_m2m()
        else:
            # If not committing, add a method to the form to allow deferred
            # saving of m2m data.
            self.save_m2m = self._save_m2m
        return self.instance


class FullSheetBookingForm(forms.ModelForm):    
    class Meta:
        model = FullSheet
        fields = '__all__'
    
    def clean_select_tickets(self):                
        data = self.cleaned_data['select_tickets']
        tickets = data.split('-')
        if BookTicket.objects.filter(ticket__ticket_no__in=tickets).exists():
            raise ValidationError('This ticket is already booked')
        return data

    def save(self,commit=True):
        data= self.cleaned_data['select_tickets']        
        tickets = data.split('-')
        for ticket in tickets:
            ticket_obj = Ticket.objects.get(ticket_no=int(ticket))
            BookTicket.objects.create(ticket=ticket_obj,username=self.cleaned_data['username'],email=self.cleaned_data['username'],phone=self.cleaned_data['phone'],address=self.cleaned_data['address'])
        if commit:
            # If committing, save the instance and the m2m data immediately.
            self.instance.save()
            self._save_m2m()
        else:
            # If not committing, add a method to the form to allow deferred
            # saving of m2m data.
            self.save_m2m = self._save_m2m
        return self.instance