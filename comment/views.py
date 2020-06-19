from django.http import HttpResponse, JsonResponse
import json
from django.views import View
from .models import Posting
from login.views import login_required
from login.models import Users

class PostingView(View):
    @login_required
    def post(self, request):
        posting_data = json.loads(request.body)
        account  = request.user
        Posting(
            user = Users.objects.get(id = account.id),
            comments = posting_data['comments']
        ).save()

        return JsonResponse({'message': 'success'}, status=200)

    def get(self, request):
        a = []
        oll = Posting.objects.values()
        for i in oll:
            a.append(i['comments'])
        return JsonResponse({'message':a},status=200)
# Create your views here.
