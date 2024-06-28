from django.shortcuts import render
from .models import ParkingInfo, Reservation
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from django.contrib import messages
from .forms import ReservationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone


import random
import string
def product_list(request):
    products = ParkingInfo.objects.all().filter(is_active=True)
    return render(request, 'list_all_parking.html', {'products': products})


def product_detail(request, pk):
    product = ParkingInfo.objects.get(pk=pk)
    return render(request, 'detail_parking.html', {'product': product})


def create_ticket_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))



class ReservationView(View):
    def get(self, request):
        try:
            user_reservation = Reservation.objects.get(customer=request.user, checked_out=False)
            if user_reservation:
                messages.warning(self.request, 'Please Check Out Your Previous Reservation')
                return redirect('home')
        except ObjectDoesNotExist:
            pass   
                
        reservation = ReservationForm()

        return render(request, 'booking.html', {'form': reservation})
    def post(self, request):
        try:
            user_reservation = Reservation.objects.get(customer=request.user, checked_out=False)
            if user_reservation:
                messages.warning(self.request, 'Please Check Out Your Previous Reservation ')
                return redirect('home')

        except ObjectDoesNotExist:
            pass    

        reservation_form = ReservationForm(data=request.POST)

        if reservation_form.is_valid():
            start_date = reservation_form.cleaned_data['start_date']
            finish_date = reservation_form.cleaned_data['finish_date']
            parking_zone = reservation_form.cleaned_data['parking_zone']
            plate_number = reservation_form.cleaned_data['plate_number']

            parkingzone = ParkingInfo.objects.get(name=parking_zone)
            if parkingzone.vacant_slots == 0:
                messages.warning(self.request, 'Parking Zone Full!')
                return redirect('home')

            reservation = reservation_form.save(commit=False)
            reservation.customer = request.user
            reservation.parking_zone = parking_zone
            reservation.ticket_code = create_ticket_code()
            reservation.save()
            #parkingzone = Parking_Zone.objects.get(name=parking_zone)
            parkingzone.occupied_slots += 1
            parkingzone.save()
            vacantslots = int(parkingzone.limit_number_car) - int(parkingzone.occupied_slots)
            parkingzone.vacant_slots = vacantslots
            parkingzone.save()
            messages.info(request, 'Successfully Booked')
            return redirect('home')

        return render(request, 'booking.html', {'form': reservation_form})


@login_required
def check_out(request):
    try:
        reservation = Reservation.objects.get(customer=request.user, checked_out=False)
        if reservation:
            reservation.checked_out = True
            reservation.save()
            parking_zone_name = reservation.parking_zone.name
            parking_zone = ParkingInfo.objects.get(name=parking_zone_name)
            parking_zone.occupied_slots -= 1
            parking_zone.vacant_slots += 1
            parking_zone.save()
            messages.info(request, 'Successfully Checked Out')
        
    except ObjectDoesNotExist:
            messages.warning(request, f'No Parking reservation exists for {request.user}')        

    return redirect('home')      
