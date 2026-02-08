from django.shortcuts import redirect
from rest_framework.decorators import api_view

@api_view()
def api_root_view(request):
    return redirect('/api/v1/')