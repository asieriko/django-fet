from django.db import models, IntegrityError
from django.db.models.fields import IntegerField
from timetabledata.util.renderxml import renderSameTime, renderBuildingRooms, renderActivity

# Create your models here.


class TimetableSettings(models.Model):
    key = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=500)

    def __str__(self):
        return self.key + ': ' + self.value


class TeacherManager(models.Manager):
    def update_teacher(self, row):
        if row['Irakaslea'] == '':
                print(row)
                return False
        teacher, tc = Teacher.objects.get_or_create(name=row['Irakaslea'])
        if row['HorasContrato'] != '':
            teacher.contractHours = row['HorasContrato']
        if row['NumHoras'] != '':
            teacher.classHours = row['NumHoras']
        if row['Zaintza_Kop'] != '':
            teacher.guardHours = row['Zaintza_Kop']
        if row['HorasTutoria'] != '':
            teacher.tutHours = row['HorasTutoria']
        if row['compensacion_gt_20'] != '':
            teacher.compensationHours = row['compensacion_gt_20']
        if row['CompTutoría'] != '':
            teacher.tutCompHours = row['CompTutoría']
        if row['Complementarias'] != '':
            teacher.complementaryHours = row['Complementarias']
        if row['Max_Dias_Sem'] != '':
            teacher.maxDaysWeek = row['Max_Dias_Sem']
        if row['Max_intervalo_dia'] != '':
            teacher.MaxSpanDay = row['Max_intervalo_dia']
        if row['Max_huecos_semana'] != '':
            teacher.MaxGapsWeek = row['Max_huecos_semana']
        if row['Max_huecos_días'] != '':
            teacher.MaxGapsDay = row['Max_huecos_días']
        if row['Edificios'] != '':
            teacher.MaxBuildingChangesWeek = row['Edificios']
        if row['Reducción'] != '':
            freeDict = {0: 'NO', 1: 'FH', 2: 'DF'}
            teacher.FreeType = freeDict[row['Reducción']]
        teacher.save()
        return teacher


class Teacher(models.Model):
    FREE_CHOICES = (
        ('FH', 'FirstHours'),
        ('DF', 'DayFree'),
        ('NO', 'Nothing'),
    )
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    contractHours = models.IntegerField(default=20)
    classHours = models.IntegerField(null=True)
    guardHours = models.IntegerField(null=True)
    tutHours = models.IntegerField(null=True)
    compensationHours = models.IntegerField(null=True)
    tutCompHours = models.IntegerField(null=True)
    complementaryHours = models.IntegerField(null=True)  # Float
    maxDaysWeek = models.IntegerField(null=True)
    MaxSpanDay = models.IntegerField(null=True)
    MaxGapsWeek = models.IntegerField(null=True)
    MaxGapsDay = models.IntegerField(null=True)
    MaxBuildingChangesWeek = models.IntegerField(null=True)
    FreeType = models.CharField(
        max_length=2,
        choices=FREE_CHOICES,
        default='NO',)

    objects = TeacherManager()

    def __str__(self):
        if self.code:
            return self.name + "(" + self.code + ")"
        else:
            return self.name


class RoomManager(models.Manager):
    def create_room_building(self, name):
        room = Room.objects.filter(name=name, building=int(name[0])).first()
        if room is None:
            room = self.create(name=name, building=int(name[0]))
        return room

    def create_rooms_xml(self):
        buildings = [b['building'] for b in Room.objects.all().values('building').distinct()]
        rooms = [[r.name, r.capacity, r.building] for r in Room.objects.all()]
        result = renderBuildingRooms(buildings,rooms)
        return result

class Room(models.Model):
    name = models.CharField(max_length=10)
    capacity = models.IntegerField(default=30)
    building = models.IntegerField(default=1)

    objects = RoomManager()

    class Meta:
        unique_together = (("name", "building"),)  # percival 273

    def __str__(self):
        return self.name + "(" + str(self.building) + ")"


class GroupManager(models.Manager):
    def create_group_course(self, name):
        group = self.create(name=name, course=name[0])
        return group


class Group(models.Model):
    name = models.CharField(max_length=10)
    course = models.CharField(max_length=10)

    objects = GroupManager()

    class Meta:
        unique_together = (("name", "course"),)

    def __str__(self):
        return self.name + "(" + self.course + ")"


class DataManager(models.Manager):
    def create_data(self, row):
        if row["Irakaslea"] == '':
                print(row)
                return False
        teacher, tc = Teacher.objects.get_or_create(name=row['Irakaslea'])
        record = Data.objects.create(Subject=row['Ikasgaia'], Teacher=teacher,
            Department=row['Mintegia'], Language=row['Eredua'],
            Hours=row['Orduak'])
        record.save()
        if row["Taldea"][0] == 'B' and row["Taldea"][1] in ['1', '2']:
            row["Taldea"] = row["Taldea"][1:]
        if row["Taldea"][0] in ['1', '2', '3', '4']:  # 1ABC, B2HI, Murrizketa
            gcourse = row["Taldea"][0]
            groups = row["Taldea"][1:]
            gs = []
            for g in groups:
                group, gc = Group.objects.get_or_create(name=gcourse + g,
                    course=row["Maila"])
                gs.append(group)
                record.Group.add(group)
        if row['Tipo'] != '':
            ctype = ConexionType.objects.create_ctype(row)
            record.Type = ctype
        if row['Loturak'] != '':
            #print(row['Loturak'])
            record.Conexion = row['Loturak']
            if row['AgrupacionEDUCA'] != '':
                #print("not:", row['AgrupacionEDUCA'])
                record.Grouping = row['AgrupacionEDUCA']
        record.save()
        if row["Aula"] not in ['', '-']:
            room, rc = Room.objects.get_or_create(name=row['Aula'],
            building=row['Aula'][0])
            rooms = Data.objects.filter(Conexion=record.Conexion).values('Room')
            #For most activities is not possible to share room, but meetings are in the same room
            if ctype.ctype == 'OP' and room in [Room.objects.get(pk=r['Room']) for r in rooms if r['Room'] is not None]:
                raise IntegrityError('UNIQUE constraint failed: room already in conexion')
            record.Room.add(room)
        record.save()
        return record

    def create_dept_meetings(self):
        deptea = Data.objects.all().values("Department", "Teacher").distinct()
        ct = ConexionType.objects.filter(ctype='ME').first()
        #print(teachers)
        for dt in deptea:
            teacher = Teacher.objects.get(pk=dt['Teacher'])
            lang = Data.objects.filter(Teacher=teacher).values('Language').first()
            #FIXME: lang as max of all?
            #FIXME: Rooms!!
            dept = dt['Department']
            row = {'Mintegia': dept,
                'Irakaslea': teacher.name,
                'Taldea':'MB',
                'Aula': '',
                'AgrupacionEDUCA': '',
                'Orduak': 0,
                'Loturak': dept + '_Meeting',
                'Tipo': 'bilera',
                'Eredua':  lang['Language'],
                'Ikasgaia': dept + '_Meeting'}
            d = Data.objects.create_data(row)
            depbuildings = TimetableSettings.objects.filter(key='deptbuildings').first()
            if depbuildings is None:
                depbuildings = '1'
            else:
                depbuildings = depbuildings.value
            for b in range(int(depbuildings)):
                room = str(b + 1) + '_' + dept
                r, c = Room.objects.get_or_create(name=room,
                                               building=room[0])
                d.Room.add(r)
            d.save()


class ConexionTypeManager(models.Manager):
    def create_ctype(self, row):
        if row['Tipo'] == 'bilera':
            ct, c = self.get_or_create(name=row['Tipo'], ctype='ME')
        elif row['Tipo'] == 'independiente':
            ct, c = self.get_or_create(name=row['Tipo'], ctype='IN')
        elif row['Tipo'] == 'nada':
            ct, c = self.get_or_create(name=row['Tipo'], ctype='NO')
        elif row['Tipo'] == 'h':
            ct, c = self.get_or_create(name=row['Tipo'], ctype='OP')
        else:
            raise ValueError(row['Tipo'], ' not a valid conexion type')
        return ct
        

class ConexionType(models.Model):
    CONEXION_CHOICES = (
        ('ME', 'Meeting'),
        ('OP', 'Option'),
        ('NO', 'Nothing'),
        ('IN', 'Indepednent'),
    )
    ctype = models.CharField(
        max_length=2,
        choices=CONEXION_CHOICES,
        blank=True,
        unique=True)
    name = models.CharField(max_length=50)

    objects = ConexionTypeManager()

class Data(models.Model):
    Teacher = models.ForeignKey(Teacher)
    Group = models.ManyToManyField(Group, blank=True)
    Subject = models.CharField(max_length=50)
    Hours = models.IntegerField(default=3)
    Grouping = models.CharField(max_length=50, blank=True, null=True)
    Conexion = models.CharField(max_length=50, blank=True, null=True)
    Type = models.ForeignKey(ConexionType, blank=True, null=True)
    Room = models.ManyToManyField(Room, blank=True, null=True)
    Notes = models.CharField(max_length=50, blank=True)
    NotesDept = models.CharField(max_length=200, blank=True)
    Department = models.CharField(max_length=50, blank=True)
    Language = models.CharField(max_length=5, blank=True)
    Students = models.IntegerField(default=0)

    objects = DataManager()

    class Meta:
        unique_together = (("Teacher", "Conexion"), ("Grouping", "Conexion"))


class Tag(models.Model):
    name = models.CharField(max_length=20)


class ActivityManager(models.Manager):
    def create_activities(self, data):
        tduration = data.Hours
        act = Activity.objects.create(
            Activity_Id=0,
            Group_Id=0,
            Duration=1,
            Subject=data.Subject,
            Data=data)
        act.save()
        act.Activity_Id = act.pk
        act.Group_Id = act.pk
        act.save()
        for _ in range(tduration - 1):
            eact = Activity.objects.create(
                Activity_Id=0,
                Group_Id=act.Group_Id,
                Duration=1,
                Subject=data.Subject,
                Data=data)
            eact.Activity_Id = eact.pk
            eact.save()
        return True

    def create_conexions(self):
        conexions = Data.objects.all().values("Conexion").distinct()
        for con in conexions:
            data = Data.objects.filter(Conexion=con["Conexion"])
            ac = []
            for d in data:
                ac1 = []
                activities = Activity.objects.filter(Data=d)
                for activity in activities:
                    ac1.append(activity)
                ac.append(ac1)
            ac = [list(x) for x in zip(*ac)]
            hours = data[0].Hours
            for i in range(hours):
                actCon = ActivityConexion(conexion=con["Conexion"], subconexion='C' + str(i+1) + '_' + con["Conexion"])
                actCon.save()
                for a in ac[i]:
                    actCon.activity.add(a)
        return True
    
    def create_activity_XML(self):
        activities = Activity.objects.all()
        xml = []
        for activity in activities:
            context = {
                'activity_id': activity.Activity_Id,
                'group_id': activity.Group_Id,
                'subject': activity.Subject,
                'duration': activity.Duration,
                'total_duration': activity.Data.Hours,
                'teachers': [teacher.name for teacher in activity.Teachers.all()],
                'students': activity.Students      
            }
            xml.append(renderActivity(context))
        return xml

class Activity(models.Model):
    Activity_Id = models.IntegerField()
    Group_Id = models.IntegerField()
    Subject = models.CharField(max_length=50)
    Teachers = models.ManyToManyField(Teacher, blank=True)
    Duration = models.IntegerField()
    Students = models.CharField(max_length=50, blank=True)
    # manytomany, grouping...¿?
    Tags = models.ManyToManyField(Tag, blank=True)
    Data = models.ForeignKey(Data)

    objects = ActivityManager()
    

class ActivityConexionManager(models.Manager):
    def generate_conexion_xml(self):
        subconexions = ActivityConexion.objects.all().values('subconexion').distinct()
        xml = []
        for subconexion in subconexions:
            acs = ActivityConexion.objects.filter(subconexion=subconexion['subconexion'])
            for ac in acs:
                stactivities = []
                for a in ac.activity.all():
                    stactivities.append(a.Activity_Id)
                xml.append(renderSameTime(stactivities))
        return xml

class ActivityConexion(models.Model):
    conexion = models.CharField(max_length=50)
    subconexion = models.CharField(max_length=52)
    activity = models.ManyToManyField(Activity, blank=True)    
    
    objects = ActivityConexionManager()