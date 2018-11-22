from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.views.generic import View
import pdb


from bokeh.plotting import figure, output_file, show
from bokeh.embed import components, autoload_server

from .models import Cart, CartGroup, DataSet, CartFleet, DataCollection, Fault
from .file_parser import parse_file
from .forms import CartGroupForm

selected_fleet = CartFleet.objects.get(pk=1)
# Called by home view to convert cart group color values to rgb when presenting the graph
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    t = [int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)]
    return tuple(t)

class home(View):
    def get(self, request):
        if request.GET.get("selected_fleet", ""):
            global selected_fleet
            selected_fleet = CartFleet.objects.get(name = request.GET.get("selected_fleet", "").strip())

        title = str(selected_fleet.name)
        plot = figure(title= None,
                x_axis_label= 'Cart Number',
                y_axis_label= 'Amp Hours',
                plot_width =900,
                plot_height =380)

        x = []
        y = []
        for cart in Cart.objects.filter(cart_fleet = selected_fleet):
            if not cart.group.all().exists():
                x.append(float(cart.number))
                for data_collection in list(DataSet.objects.filter(cart = cart).values()):
                    y.append(float(data_collection['amp_hours']))
            else:
                for data_collection in list(DataSet.objects.filter(cart = cart).values()):
                    plot.circle(float(cart.number), float(data_collection['amp_hours']), size=20, color=hex_to_rgb(cart.group.all()[0].group_color), alpha=0.5)

        plot.circle(x, y, size=20, color="navy", alpha=0.5)
        script, div = components(plot)
        context = {
            'selected_fleet': selected_fleet,
            'cart_fleet_list': CartFleet.objects.all(),
            'plot_script' : script,
            'plot_div' : div,
            'home' : True
            }
        return render(request, 'carts/home.html', context)

class import_data(View):
    def post(self, request):
        parse_file(request.FILES, selected_fleet)
        return self.get(self, request)

    def get(self, request):
        if request.GET.get("selected_fleet", ""):
            global selected_fleet
            selected_fleet = CartFleet.objects.get(name = request.GET.get("selected_fleet", "").strip())

        context = {
            'selected_fleet': selected_fleet,
            'cart_fleet_list': CartFleet.objects.all(),
            'import_data' : True
            }
        return render(request, 'carts/import data.html', context)

class cart_viewer(View):
    def get(self, request):
        if request.GET.get("selected_fleet", ""):
            global selected_fleet
            selected_fleet = CartFleet.objects.get(name = request.GET.get("selected_fleet", "").strip())

        print(selected_fleet)
        context = {
            'selected_fleet': selected_fleet,
            'cart_fleet_list': CartFleet.objects.all(),
            'fleet_carts_list': [serializers.serialize("json", Cart.objects.filter(cart_fleet=fleet)) for fleet in CartFleet.objects.all()],
            'fleet_carts_data': [[serializers.serialize("json", DataSet.objects.filter(cart__cart_fleet=fleet, collection=set)) for set in DataCollection.objects.all()] for fleet in CartFleet.objects.all()],
            'fleet_fault_data': [[serializers.serialize("json", Fault.objects.filter(cart__cart_fleet=fleet, cart=cart)) for cart in Cart.objects.all()] for fleet in CartFleet.objects.all()]
        }
        print(context['fleet_carts_data'][0])
        return render(request, 'carts/cart viewer.html', context)

class cart_groups(View):
    def post(self, request):
        cg = CartGroup.objects.create(group_name=request.POST.get("GroupName", ""), group_color=request.POST.get("GroupColor", ""))
        cg.save
        for cartNumber in request.POST.getlist("GroupCarts"):
            c = Cart.objects.get(number=cartNumber)
            c.group.add(cg)
            c.save
        return self.get(self, request)

    def get(self, request):
        if request.GET.get("selected_fleet", ""):
            global selected_fleet
            selected_fleet = CartFleet.objects.get(name = request.GET.get("selected_fleet", "").strip())

        context = {
            'selected_fleet': selected_fleet,
            'cart_fleet_list': CartFleet.objects.all(),
            'fleet_carts_list': [serializers.serialize("json", Cart.objects.filter(cart_fleet=fleet)) for fleet in CartFleet.objects.all()],
            'fleet_carts_data': [[serializers.serialize("json", DataSet.objects.filter(cart__cart_fleet=fleet, collection=set)) for set in DataCollection.objects.all()] for fleet in CartFleet.objects.all()],
            'fleet_fault_data': [[serializers.serialize("json", Fault.objects.filter(cart__cart_fleet=fleet, cart=cart)) for cart in Cart.objects.all()] for fleet in CartFleet.objects.all()]
        }
        return render(request, 'carts/cart groups.html', context)
