from django.shortcuts import render
from rest_framework import viewsets
from .models import Resource, Booking
from .serializers import ResourceSerializer, BookingSerializer
from rest_framework.response import Response
from rest_framework import status


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        resource_id = request.data.get('resource')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')

        try:
            resource = Resource.objects.get(id=resource_id)
        except Resource.DoesNotExist:
            return Response({'error':'Resource not found'}, status=status.HTTP_404_NOT_FOUND)
        
        bookings = Booking.objects.filter(resourc=resource, status='active').filter(
            start_time__lt=end_time,
            end_time__gt=start_time
        )

        if bookings.count() < resource.max_capacity:
            booking = Booking.objects.create(
                user=user,
                resource=resource,
                start_time=start_time,
                end_time=end_time,
                status='active'
            )
            return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
        else:

            booking = Booking.objects.create(
                user=user,
                resource=resource,
                start_time = start_time,
                end_time=end_time,
                status='waiting'
            )
            return Response(BookingSerializer(booking).data, status=status.HTTP_202_ACCEPTED)
    def destroy(self, request, *args, **kwargs):
        booking = self.get_object()
        if booking.status == 'waiting':
            booking.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        
        if booking.status == 'active':
            booking.delete()

            next_booking = Booking.objects.filter(resource=booking.resource, status='waiting').order_by('id').first()
            if next_booking:
                next_booking.status = 'active'
                next_booking.save()

                print('asdjashd')
            
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({'error':'Booking not found or cannot be cancelled'}, status=status.HTTP_404_NOT_FOUND)