from django.shortcuts import render

from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from apps.cycles.forms.cycle_form import CycleForm
from apps.cycles.forms.daily_log_form import LogDayForm
from apps.cycles.models.cycle import Cycle
from apps.cycles.models.daily_log import DailyLog
from django.http import JsonResponse

# Create your views here.
class CycleView(LoginRequiredMixin, TemplateView):
    template_name = "cycles/cycle.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        active_cycle = Cycle.objects.filter(
            user=self.request.user,
            end_date__isnull=True,
        ).first()

        today_log = None
        current_phase = None
        phase_day = None
        days_remaining = None

        if active_cycle:
            current_phase = active_cycle.current_phase

            today_log = DailyLog.objects.filter(
                cycle=active_cycle,
                log_date=date.today(),
            ).first()

            phase_record = active_cycle.phases.filter(
                start_date__lte=date.today(),
                end_date__gte=date.today(),
            ).first()

            if phase_record:
                phase_day = (date.today() - phase_record.start_date).days + 1
                days_remaining = (phase_record.end_date - date.today()).days

        context["form"] = CycleForm()
        context["log_form"] = LogDayForm(instance=today_log)
        context["active_cycle"] = active_cycle
        context["current_phase"] = current_phase
        context["today_log"] = today_log
        context["phase_day"] = phase_day
        context["days_remaining"] = days_remaining

        return context
    
    
class CycleCreateView(LoginRequiredMixin, View):

    def post(self, request):
        form = CycleForm(request.POST)

        if form.is_valid():

            active_cycle = Cycle.objects.filter(
                user=request.user,
                end_date__isnull=True,
            ).exists()

            if active_cycle:
                form.add_error(
                    None,
                    "Ya tienes un ciclo activo."
                )
            else:
                cycle = form.save(commit=False)
                cycle.user = request.user
                cycle.save()

                return redirect("cycles:cycle")

        return render(
            request,
            "cycles/cycle.html",
            {
                "form": form,
            },
        )
        
        
class LogDayView(LoginRequiredMixin, View):

    def post(self, request):
        active_cycle = Cycle.objects.filter(
            user=request.user,
            end_date__isnull=True,
        ).first()

        if not active_cycle:
            return JsonResponse({
                "success": False,
                "message": "No existe un ciclo activo."
            }, 
            status=400)

        form = LogDayForm(request.POST)

        if not form.is_valid():
            return JsonResponse(
                {
                    "success": False,
                    "message": "Hay errores en el formulario.",
                    "errors": form.errors,
                },
                status=400,
            )

        daily_log = DailyLog.objects.filter(
            cycle=active_cycle,
            log_date=date.today(),
        ).first()

        if daily_log:
            daily_log.energy_level = form.cleaned_data["energy_level"]
            daily_log.mood = form.cleaned_data["mood"]
            daily_log.notes = form.cleaned_data["notes"]
            daily_log.save()

            daily_log.symptoms.set(
                form.cleaned_data["symptoms"]
            )

        else:
            daily_log = form.save(commit=False)
            daily_log.cycle = active_cycle
            daily_log.log_date = date.today()
            daily_log.save()

            form.save_m2m()

        return JsonResponse({
            "success": True,
            "message": "Registro guardado",
        })