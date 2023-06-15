from django.views.generic import ListView
from example.models import ExampleImageModel


class ExampleImageListView(ListView):
    template_name = "home.html"
    model = ExampleImageModel