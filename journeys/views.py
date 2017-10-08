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


@login_required()
def create_journey(request, user_id):

    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':

        journey_form = JourneyForm(data=request.POST)

        if journey_form.is_valid():

            journey = journey_form.save(commit=False)

            journey.created_by = user

            journey.save()

            return HttpResponseRedirect(reverse('journeys:single', kwargs={"pk": journey.pk}))

        else:
            print(journey_form.errors)

    else:
        journey_form = JourneyForm()

    context = {'form': journey_form}
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
    return HttpResponseRedirect(reverse("journeys:single", kwargs={"pk":pk}))


@login_required
def leave_journey(request, pk):
    journey = get_object_or_404(Journey, pk=pk)
    user = request.user
    Journey.remove_member(journey, user)
    return HttpResponseRedirect(reverse("journeys:single", kwargs={"pk":pk}))

# todo
# search journey view
def up(request):

    if request.method == 'POST':

        search_journey_form = SearchJourneyForm(data=request.POST)

        if search_journey_form.is_valid():
            starting_from = search_journey_form.cleaned_data['starting_from']
            going_to = search_journey_form.cleaned_data['going_to']

            print(starting_from)
            print(going_to)

            journeys = Journey.objects.all().filter(starting_from=starting_from, going_to=going_to)

            print(journeys)
            context = {'form': search_journey_form, 'journeys': journeys}
            return render(request, 'journeys/search.html', context)
        else:
            print(search_journey_form.errors)

    else:
        search_journey_form = SearchJourneyForm()

    context = {'form': search_journey_form, 'journeys': None}
    return render(request, 'journeys/search.html', context)


#
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
