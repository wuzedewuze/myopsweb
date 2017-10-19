from django.http import HttpResponse
from django.views.decorators.csrf import  csrf_exempt
from resources.models import Server
import  datetime

@csrf_exempt
def ServerInfoAuto(request):
    if request.method == "POST":
        data = request.POST.dict()
        data['check_update_time'] = datetime.datetime.now()
        try:
            s=Server.objects.get(uuid__exact=data['uuid'])
            s.save(update_fields=["check_update_time"])
            '''
            Server.objects.filter(uuid=data['uuid']).update(**data)
            s.save(update_fields=['hostname'])
          '''
        except Server.DoesNotExist:
            s = Server(**data)
            s.save()
        return HttpResponse("")




