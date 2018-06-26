from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django import forms
from django.forms import modelformset_factory

from timetabledata.models import Room, Group, Teacher, Data, ConexionType, Activity, TimetableSettings
from timetabledata.forms import ConexionTypeForm
from timetabledata.util.util import loadDriveData, loadDriveTeachers


def index(request):
    template = loader.get_template('timetabledata/index.html')
    return HttpResponse(template.render({},request))

def drivedata(request):
    template = loader.get_template('timetabledata/alldata.html')
    rlist, errors = loadDriveData()
    context = {
        'rlist': rlist,
        'errors': errors
    }
    return HttpResponse(template.render(context, request))


def showData():
    Data.objects.all()


def ajax(request):
    print(request)
    if request.method == 'POST':
        print(request.POST['action'])
        if request.POST['action'] == 'delete':
            pass
        if request.POST['action'] == 'gendepm':
            try:
                Activity.objects.create_dept_meetings()
                return HttpResponse('Success')
            except Exception as inst:
                HttpResponse(inst)
        if request.POST['action'] == 'genact':
            pass
    return HttpResponse('Hello')


def editConexion(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ConexionTypeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/ConexionTypeForm/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ConexionTypeForm()

    return render(request,
        'timetabledata/ConexionTypeForm.html',
        {'form': form}
        )


def editMultiConexion(request):
    MCFormSet = modelformset_factory(ConexionType, fields=('name', 'ctype'))
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        formset = MCFormSet(request.POST)
        instances = formset.save(commit=False)
        for instance in instances:
            # check whether it's valid:
            #if instance.is_valid():
            # process the data in form.cleaned_data as required
            instance.save()
        # redirect to a new URL:
        return HttpResponseRedirect('/MultiConexionTypeForm/')
    # if a GET (or any other method) we'll create a blank form
    else:
        formset = MCFormSet()

    return render(request,
        'timetabledata/MultiConexionTypeForm.html',
        {'formset': formset}
        )

def editSettings(request):
    SettingsFormSet = modelformset_factory(TimetableSettings, fields=('key', 'value'))
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        formset = SettingsFormSet(request.POST)
        instances = formset.save(commit=False)
        for instance in instances:
            # check whether it's valid:
            #if instance.is_valid():
            # process the data in form.cleaned_data as required
            instance.save()
        # redirect to a new URL:
        return HttpResponseRedirect('/SettingsForm/')
    # if a GET (or any other method) we'll create a blank form
    else:
        formset = SettingsFormSet()

    return render(request,
        'timetabledata/SettingsForm.html',
        {'formset': formset}
        )


def showTeachers(request):
    template = loader.get_template('timetabledata/teachers.html')
    context = {
        'teachers': Teacher.objects.all()
    }
    print(context)
    return HttpResponse(template.render(context, request))


def editMultiTeacher(request):
    MTeacherFormSet = modelformset_factory(Teacher, exclude=('',))
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        formset = MTeacherFormSet(request.POST)
        instances = formset.save(commit=False)
        #FIXME: Validation
        for instance in instances:
            # check whether it's valid:
            #if instance.is_valid():
            # process the data in form.cleaned_data as required
            instance.save()
        # redirect to a new URL:
        return HttpResponseRedirect('/MultiTeacherForm/')
    # if a GET (or any other method) we'll create a blank form
    else:
        formset = MTeacherFormSet()

    return render(request,
    'timetabledata/MultTeachersForm.html',
    {'formset': formset}
    )


def driveTeachers(request):
    template = loader.get_template('timetabledata/teacherdata.html')
    rlist, errors = loadDriveTeachers()
    context = {
        'teachers': rlist,
        'errors': errors
    }
    return HttpResponse(template.render(context, request))