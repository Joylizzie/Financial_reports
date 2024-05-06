from django.shortcuts import render

from django.conf import settings
from django.db import connection
from django.http import HttpResponse
from bokeh.plotting import figure, show
from bokeh.resources import CDN
from bokeh.embed import components, file_html
from .models import CustomerNames

def index(request):
    customers_lst = CustomerNames.objects.order_by('customer_id')[:20]
    return HttpResponse(customers_lst)

def homepage(request):

    fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
    counts = [5, 3, 4, 2, 4, 6]

    p = figure(x_range=fruits, height=350, title="Fruit Counts",
           toolbar_location=None, tools="")

    p.vbar(x=fruits, top=counts, width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    script, div = components(p)
    return render(request,'templates/araging/base.html', {'script':script, 'div':div})

# def databases(request):
#     connection.ensure_connection()
#     return HttpResponse("")

# def customers_view(request, customer_id):
#     response = "This is cusomter %s"
#     return HttpResponse(response%customer_id)