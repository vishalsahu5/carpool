# from django.contrib import messages
# from django.contrib.auth.mixins import(
#     LoginRequiredMixin,
#     PermissionRequiredMixin
# )
# from braces.views import SelectRelatedMixin
from django.core.urlresolvers import reverse
# from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from journeys.models import Journey
# from . import models
from django.contrib.auth.decorators import login_required
from .forms import JourneyForm, SearchJourneyForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from geopy import units
from geopy.geocoders import GoogleV3
from carpool import settings


# class CreateJourney(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
#     fields = ("starting_from", "going_to", "going_date", "going_time", "description")
#     model = Journey
#
#     def form_valid(self, form):
#         # self.object = form.save(commit=False)
#         form.instance.created_by = self.kwargs.get('pk')
#         # self.object.user = self.request.user
#         # self.object.save()
#         return super(CreateJourney, self).form_valid(form)


#################################################################################################
# Utility Functions defined here.
#################################################################################################

# todo:
# A function to get the offset
# parameters get longitude and latitude and the distance radius
def get_offset(distance_range=10):
    rough_distance = units.degrees(arcminutes=units.nautical(kilometers=distance_range)) * 2
    return rough_distance


##################################################################################################
# Views functions below.
##################################################################################################
@login_required()
def create_journey(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':

        journey_form = JourneyForm(data=request.POST)

        if journey_form.is_valid():
            starting_from = journey_form.cleaned_data['starting_from']
            going_to = journey_form.cleaned_data['going_to']

            geolocator = GoogleV3(api_key=settings.GOOGLE_API_KEY)

            starting_location = geolocator.geocode(starting_from, timeout=10)
            final_location = geolocator.geocode(going_to, timeout=10)

            journey = journey_form.save(commit=False)

            journey.created_by = user

            journey.starting_from_latitude = starting_location.latitude
            journey.starting_from_longitude = starting_location.longitude
            journey.going_to_latitude = final_location.latitude
            journey.going_to_longitude = final_location.longitude

            journey.save()

            return HttpResponseRedirect(reverse('journeys:single', kwargs={"pk": journey.pk}))

        else:
            print(journey_form.errors)

    else:
        journey_form = JourneyForm()

    context = {'form': journey_form, 'api_key': settings.PLACES_MAPS_API_KEY}
    return render(request, 'journeys/journey_form.html', context)


class SingleJourney(generic.DetailView):
    model = Journey


class ListJourneys(generic.ListView):
    model = Journey


@login_required
def join_journey(request, pk):
    journey = get_object_or_404(Journey, pk=pk)
    user = request.user
    Journey.add_member(journey, user)
    return HttpResponseRedirect(reverse("journeys:single", kwargs={"pk": pk}))


@login_required
def leave_journey(request, pk):
    journey = get_object_or_404(Journey, pk=pk)
    user = request.user
    Journey.remove_member(journey, user)
    return HttpResponseRedirect(reverse("journeys:single", kwargs={"pk": pk}))


# todo
# search journey view
def search_journey(request):
    if request.method == 'POST':

        search_journey_form = SearchJourneyForm(data=request.POST)

        if search_journey_form.is_valid():
            starting_from = search_journey_form.cleaned_data['starting_from']
            going_to = search_journey_form.cleaned_data['going_to']

            geolocator = GoogleV3(api_key=settings.GOOGLE_API_KEY)

            starting_location = geolocator.geocode(starting_from, timeout=10)
            final_location = geolocator.geocode(going_to, timeout=10)

            offset = get_offset(25)
            min_lat_from = starting_location.latitude - offset
            max_lat_from = starting_location.latitude + offset
            min_lon_from = starting_location.longitude - offset
            max_lon_from = starting_location.longitude + offset

            min_lat_to = final_location.latitude - offset
            max_lat_to = final_location.latitude + offset
            min_lon_to = final_location.longitude - offset
            max_lon_to = final_location.longitude + offset

            search_result = Journey.objects.filter(starting_from_longitude__lte=max_lon_from,
                                                   starting_from_longitude__gte=min_lon_from,
                                                   starting_from_latitude__gte=min_lat_from,
                                                   starting_from_latitude__lte=max_lat_from,
                                                   going_to_longitude__gte=min_lon_to,
                                                   going_to_longitude__lte=max_lon_to,
                                                   going_to_latitude__gte=min_lat_to,
                                                   going_to_latitude__lte=max_lat_to,
                                                   )
            # for debugging purposes.
            print(search_result)

            # The commented code below does the exact same thing as above db filtering.
            # journeys = Journey.objects.all()
            # search_result = []
            # for journey in journeys:
            #     bool1 = min_lat_from <= journey.starting_from_latitude <= max_lat_from
            #     bool2 = min_lon_from <= journey.starting_from_longitude <= max_lon_from
            #     bool3 = min_lat_to <= journey.going_to_latitude <= max_lat_to
            #     bool4 = min_lon_to <= journey.going_to_longitude <= max_lon_to
            #
            #     if bool1 and bool2 and bool3 and bool4:
            #         search_result.append(journey)

            context = {'form': search_journey_form, 'journeys': search_result, 'api_key': settings.PLACES_MAPS_API_KEY}
            return render(request, 'journeys/search.html', context)
        else:
            print(search_journey_form.errors)

    else:
        search_journey_form = SearchJourneyForm()

    context = {'form': search_journey_form, 'journeys': None, 'api_key': settings.PLACES_MAPS_API_KEY}
    return render(request, 'journeys/search.html', context)

# class JoinJourney(LoginRequiredMixin, generic.RedirectView):
#
#     def get_redirect_url(self, *args, **kwargs):
#         # return reverse("journeys:single", kwargs={"slug": self.kwargs.get("slug")})
#         # send primary key pk from the templates
#         return reverse("journeys:single", kwargs={"pk": self.kwargs.get("pk")})
#
#     def get(self, request, *args, **kwargs):
#         # journeys = get_object_or_404(Journey, slug=self.kwargs.get("slug"))
#         # send primary key pk from the templates
#         journey = get_object_or_404(Journey, pk=self.kwargs.get("pk"))
#
#         try:
#             JourneyMember.objects.create(user=self.request.user, journey=journey)
#
#         except IntegrityError:
#             messages.warning(self.request, ("Warning, already a partner of {}'s Journey".format(journey.created_by)))
#
#         else:
#             messages.success(self.request, "You are now a partner of the {}'s journeys.".format(journey.created_by))
#
#         return super().get(request, *args, **kwargs)
#
#
# class LeaveJourney(LoginRequiredMixin, generic.RedirectView):
#
#     def get_redirect_url(self, *args, **kwargs):
#         return reverse("journeys:single", kwargs={"pk": self.kwargs.get("pk")})
#
#     def get(self, request, *args, **kwargs):
#
#         try:
#
#             membership = models.JourneyMember.objects.filter(
#                 user=self.request.user,
#                 # send pk through templates
#                 journey__pk=self.kwargs.get("pk")
#             ).get()
#
#         except models.JourneyMember.DoesNotExist:
#             messages.warning(
#                 self.request,
#                 "You can't leave this Journey because you aren't in it."
#             )
#         else:
#             membership.delete()
#             messages.success(
#                 self.request,
#                 "You have successfully cancelled the Journey."
#             )
#         return super().get(request, *args, **kwargs)
