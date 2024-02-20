from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Par
from .serializers import ParSerializer
from .utils import createPar, getParsList, getParDetail, updatePar, deletePar, export_heats, export_all, export_rsr

from .models import Par
from django.http import JsonResponse
from django.http import HttpResponse


# Create your views here.

@api_view(['GET'])
def getRoutes(request):

    routes = [
        {
            #json response of all methods/participants in db
            'Endpoint': '/par/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of participants'
        },
        {
            #get a single participant, query db for specific participant
            'Endpoint': '/par/${armNum}', # arm num????
            'method': 'GET',
            'body': None,
            'description': 'Returns a single participant obj'
        },
        {
            #create a particpant 
            'Endpoint': '/par/create/',
            'method': 'POST',
            'body': {
                'name': 'Participant name',
                # 'lastName' : 'Participant last name',
                'armNum': 'Parcipant arm num',
                'swimTime': 'Participant Swim Time', 
                'rsrTime': 'Particpant RSR Time',

            },
            'description': 'Creates new participant with data sent in post request'
        },
        {
            #update times
            'Endpoint': '/par/${armNum}/update/',
            'method': 'PUT',
            'body': {
                'name': 'Updated participant name',
                # 'lastName' : 'Updated participant last name',
                'armNum': 'Updated parcipant arm num',
                'swimTime': 'Updated participant Swim Time', 
                'rsrTime': 'Updated particpant RSR Time',
            },
            'description': 'Creates an existing participant with data sent in post request'
        },
        {
            #deletes a single particpant
            'Endpoint': '/par/${armNum}/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes and exiting participant'
        },

        {
            #exports swim times into excel
            'Endpoint': '/pars/export_heats/',
            'method': 'GET',
            'body': None,
            'description': 'Export swim times from excel'
        },
        {
            'Endpoint': '/pars/export_all/',
            'method': 'GET',
            'body': None,
            'description': 'Export swim + rsr times from excel'
        },
    ]
    return Response(routes)


@api_view(['GET', 'POST'])
def getPars(request):
    if request.method == 'GET':
        return getParsList(request)
    
    if request.method == 'POST':
        return createPar(request)


@api_view(['GET', 'PUT', 'DELETE'])
def getPar(request, an):
    if request.method == 'GET':
        return getParDetail(request, an)
        
    if request.method == 'PUT':
        return updatePar(request, an)
        
    if request.method == 'DELETE':
        return deletePar(request, an)


@api_view(['GET'])
def export_heats_route(request):
    if request.method == 'GET':
        return export_heats()
    
@api_view(['GET'])
def export_all_route(request):
    if request.method == 'GET':
        return export_all()
    
@api_view(['GET'])
def export_rsr_route(request):
    if request.method == 'GET':
        return export_rsr()


