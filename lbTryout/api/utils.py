from rest_framework.response import Response
from .models import Par
from .serializers import ParSerializer
from django.http import Http404
from django.db.models import DurationField


import pandas as pd
from django.http import JsonResponse



from django.utils.dateparse import parse_duration

def getParsList(request):
    participants = Par.objects.all().order_by('armNum')
    serializer = ParSerializer(participants, many=True)
    return Response(serializer.data)

def createPar(request):
    data = request.data
    par = Par.objects.create(
        name=data['name'],
        armNum=data['armNum'],
        swimTime=parse_duration(data.get('swimTime')),  
        rsrTime=parse_duration(data.get('rsrTime')),
    )
    serializer = ParSerializer(par, many=False)
    return Response(serializer.data)

def getParDetail(request, an):
    try:
        participant = Par.objects.get(armNum=an)
        serializer = ParSerializer(participant, many=False)
        return Response(serializer.data)
    except Par.DoesNotExist: # if an unvalid arm number is received
        raise Http404("Participant not found")
    
def updatePar(request, an):
    data = request.data # get data
    par = Par.objects.get(armNum=an)
    serializer = ParSerializer(instance=par, data=data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

def deletePar(request, an):
    participant = Par.objects.get(armNum=an)
    participant.delete()
    return Response('Note was deleted!')

def duration_to_time_format(duration):
    """
    Convert Django DurationField to a string representation in time format (HH:MM:SS).
    """
    if duration:
        # Convert duration to hours, minutes, and seconds components
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return None



def export_heats(request):
    
    objs = Par.objects.all().order_by('swimTime')

    fields_to_export = ['name', 'swimTime', 'swimPts']

    data = {field: [] for field in fields_to_export}

    # Calculate swim points based on swim performance
    #max_swim_time = Par.objects.order_by('-swimTime').first().swimTime  # Assuming swimTime is a DurationField
    swim_pts = list(range(1, 101, +1))
    

    for obj, pts in zip(objs, swim_pts):
        obj.swimPts = pts
        obj.save()
        for field in fields_to_export:
            if field == 'swimPts':
                value = pts
            elif isinstance(Par._meta.get_field(field), DurationField):
                value = duration_to_time_format(getattr(obj, field))
            else:
                value = getattr(obj, field)
            # Replace null values with 'N/A'
            data[field].append(value if value is not None else 'N/A')
    
    # Create a DataFrame using the data dictionary
    df = pd.DataFrame(data)


    # Save the DataFrame to an Excel file
    df.to_excel('heats.xlsx', index=False)

    return JsonResponse({'status': 200})

def calculate_rsr_pts():
    objs = Par.objects.all().order_by('rsrTime')

    # Calculate swim points based on swim performance
    #max_swim_time = Par.objects.order_by('-swimTime').first().swimTime  # Assuming swimTime is a DurationField
    rsr_pts = list(range(1, 101, +1))
    
    for obj, pts in zip(objs, rsr_pts):
        obj.rsrPts = pts
        obj.save()

    return [obj.rsrPts for obj in objs]

def export_rsr(request):
    calculate_rsr_pts()
    objs = Par.objects.all().order_by('rsrTime')

    fields_to_export = ['name', 'rsrTime', 'rsrPts']
    data = {field: [] for field in fields_to_export}

    for obj in objs:
        for field in fields_to_export:
            if isinstance(Par._meta.get_field(field), DurationField):
                value = duration_to_time_format(getattr(obj, field))
            else:
                value = getattr(obj, field)
                # Replace null values with 'N/A'
            data[field].append(value if value is not None else 'N/A')

    df = pd.DataFrame(data)
    #print(df)
    df.index = df.index + 1
    df.to_excel('rsr.xlsx', index=True) 


    return JsonResponse({'status': 200})       


   
def export_all(request):
    calculate_rsr_pts()
    objs = Par.objects.all()

    # Specify the fields you want to export
    fields_to_export = ['rank','name', 'swimTime', 'swimPts', 'rsrTime', 'rsrPts', 'totalPts'] 

    # Create a dictionary to store data for each field
    data = {field: [] for field in fields_to_export}
    

    # Populate the data dictionary with values from the queryset
    for idx, obj in enumerate(objs, start=1):

        obj.totalPts = obj.swimPts + obj.rsrPts
        for field in fields_to_export:
            if field == 'rank':
                obj.rank = idx
                obj.save()
            if isinstance(Par._meta.get_field(field), DurationField):
                value = duration_to_time_format(getattr(obj, field))
            else:
                value = getattr(obj, field)
            # Replace null values with 'N/A'
            data[field].append(value if value is not None else 'N/A')

           

    # Create a DataFrame using the data dictionary
    df = pd.DataFrame(data)
    
    #print(df)

    # Save the DataFrame to an Excel file
    df.to_excel('output.xlsx', index=False)

    return JsonResponse({'status': 200})
