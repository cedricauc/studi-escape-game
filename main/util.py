from .models import Scenario


def footer_scenario(request):
    """
    Retourne liste des scénarios
    """
    return {'footer_scenario': Scenario.objects.all()}
