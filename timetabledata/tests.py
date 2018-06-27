from django.test import TestCase
from django.db import IntegrityError
from timetabledata.models import Room, Group, Groupings, Data, ConexionType, Teacher, Activity, TimetableSettings, ActivityConexion


class BuildingsTestCase(TestCase):
    def setUp(self):
        Room.objects.create(name="1_1A5", building=1)
        Room.objects.create(name="2_013", building=2)

    def test_room_in_building(self):
        """Rooms are in the correct building"""
        room1 = Room.objects.get(name="1_1A5")
        room2 = Room.objects.get(name="2_013")
        self.assertEqual(room1.building, 1)
        self.assertEqual(room2.building, 2)

    def test_create_room_building(self):
        room1 = Room.objects.create_room_building(name="1_1A6")
        room2 = Room.objects.create_room_building(name="2_011")
        self.assertEqual(room1.building, 1)
        self.assertEqual(room2.building, 2)

    def test_room_unique_name(self):
        """A existing room is not inserted again"""
        with self.assertRaises(Exception) as raised:
            Room.objects.create(name="1_1A5", building=1)
        self.assertEqual(IntegrityError, type(raised.exception))
        self.assertIn('UNIQUE constraint failed', str(raised.exception))

    def test_room_unique_building(self):
        """Rooms with the same name may exists but in diferent buildings"""
        Room.objects.create(name="1_1A5", building=2)
        roomCount = Room.objects.filter(name='1_1A5').count()
        self.assertEqual(roomCount, 2)

    def test_rooms_XML(self):
        """Rooms are in the correct building"""
        room1 = Room.objects.get(name="1_1A5")
        room2 = Room.objects.get(name="2_013")
        generatedRooms = Room.objects.create_rooms_xml()
        expectedResult = '''
        <Buildings_List>
            <Building>
                    <Name>1</Name>
                    <Comments></Comments>
            </Building>
            <Building>
                    <Name>2</Name>
                    <Comments></Comments>
            </Building>
        </Buildings_List>
        
        <Rooms_List>
            <Room>
                    <Name>1_1A5</Name>
                    <Building>1</Building>
                    <Capacity>30</Capacity>
                    <Comments></Comments>
            </Room>    
            <Room>
                    <Name>2_013</Name>
                    <Building>2</Building>
                    <Capacity>30</Capacity>
                    <Comments></Comments>
            </Room>    
        </Rooms_List>
        '''
        self.assertXMLEqual(generatedRooms, expectedResult)


class GroupsTestCase(TestCase):
    def setUp(self):
        Group.objects.create(name="1A", course="1")
        Group.objects.create(name="4H", course="4")

    def test_group_and_course(self):
        """Groups are in the correct course"""
        group1 = Group.objects.get(name="1A")
        group2 = Group.objects.get(name="4H")
        self.assertEqual(group1.course, "1")
        self.assertEqual(group2.course, "4")

    def test_create_group_course(self):
        group1 = Group.objects.create_group_course(name="1B")
        group2 = Group.objects.create_group_course(name="4J")
        self.assertEqual(group1.course, "1")
        self.assertEqual(group2.course, "4")

    def test_group_unique_name(self):
        """A existing group is not inserted again"""
        with self.assertRaises(Exception) as raised:
            Group.objects.create(name="1A", course="1")
        #print(raised.exception)
        self.assertEqual(IntegrityError, type(raised.exception))
        self.assertIn('UNIQUE constraint failed', str(raised.exception))

    def test_grouping(self):
        row = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher1',
            'Orduak': 2,
            'Aula': '1_3A',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3A',
            'Maila': '3.DBH',
            'Tipo': 'h',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': '3-Sub1'}
        d = Data.objects.create_data(row)
        gp = list(Group.objects.get_groupings(d.Group.first()))[0].name
        self.assertEqual(row['AgrupacionEDUCA'], gp)

    def test_group_subgroup(self):
        row = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher1',
            'Orduak': 2,
            'Aula': '1_3A',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3A',
            'Maila': '3.DBH',
            'Tipo': 'h',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': '3-Sub1'}
        d = Data.objects.create_data(row)
        row = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher1',
            'Orduak': 2,
            'Aula': '1_3A',
            'Loturak': '3AG_002',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3A',
            'Maila': '3.DBH',
            'Tipo': 'h',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': '3-Sub2'}
        d = Data.objects.create_data(row)
        expectedResult = ['3A_3-Sub1','3A_3-Sub2']
        gp = list(Group.objects.get_groupings(d.Group.first()))[0].name
        sg = Group.objects.get_subgroups(d.Group.first())
        for i, item in enumerate(sg):
            self.assertEqual(expectedResult[i],item)

    def test_grouping_subgroup(self):
        row = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher1',
            'Orduak': 2,
            'Aula': '1_3A',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3A',
            'Maila': '3.DBH',
            'Tipo': 'h',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': '3-Sub1'}
        d = Data.objects.create_data(row)
        row = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher1',
            'Orduak': 2,
            'Aula': '1_3B',
            'Loturak': '3AG_002',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3B',
            'Maila': '3.DBH',
            'Tipo': 'h',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': '3-Sub1'}
        d = Data.objects.create_data(row)
        expectedResult = set(['3A_3-Sub1','3B_3-Sub1'])
        groups = Groupings.objects.get(name=row['AgrupacionEDUCA']).group.all()
        result = set()
        for group in groups:
            subgroups = Group.objects.get_subgroups(group)
            for sg in subgroups:
                result.add(sg)
        self.assertEqual(expectedResult,result)
                

        

class DataTestCase(TestCase):

    def test_create_data(self):
        row = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher1',
            'Orduak': 2,
            'Aula': '1_3A',
            'Loturak': '',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3A',
            'Maila': '3.DBH',
            'Tipo': 'independiente',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': ''}
        data = Data.objects.create_data(row)
        self.assertEqual(data.Subject, row['Ikasgaia'])

    def test_dup_teacher_con(self):
        row1 = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher1',
            'Orduak': 2,
            'Aula': '1_3A',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3A',
            'Maila': '3.DBH',
            'Tipo': 'independiente',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': ''}
        row2 = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher1',
            'Orduak': 2,
            'Aula': '1_3B',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3B',
            'Maila': '3.DBH',
            'Tipo': 'independiente',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': ''}
        Data.objects.create_data(row1)
        with self.assertRaises(Exception) as raised:
            Data.objects.create_data(row2)
        self.assertEqual(IntegrityError, type(raised.exception))
        self.assertIn('UNIQUE constraint failed', str(raised.exception))

    def test_dup_room_con_Fail(self):
        '''
        Connected activities are NOT allowed in the same class
        '''
        row1 = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher1',
            'Orduak': 2,
            'Aula': '1_3A',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3A',
            'Maila': '3.DBH',
            'Tipo': 'h',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': ''}
        row2 = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher2',
            'Orduak': 2,
            'Aula': '1_3A',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3B',
            'Maila': '3.DBH',
            'Tipo': 'h',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': ''}
        Data.objects.create_data(row1)
        with self.assertRaises(Exception) as raised:
            Data.objects.create_data(row2)
        self.assertEqual(IntegrityError, type(raised.exception))
        self.assertIn('UNIQUE constraint failed: room already in conexion', str(raised.exception))
        
    def test_dup_room_con(self):
        '''
        Not connected activities are allowed in the same class
        '''
        row1 = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher1',
            'Orduak': 2,
            'Aula': '1_3A',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3A',
            'Maila': '3.DBH',
            'Tipo': 'independiente',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': ''}
        row2 = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher2',
            'Orduak': 2,
            'Aula': '1_3A',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3B',
            'Maila': '3.DBH',
            'Tipo': 'independiente',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': ''}
        Data.objects.create_data(row1)
        Data.objects.create_data(row2)
        dataCount = Data.objects.all().count()
        self.assertEqual(dataCount, 2)

    def test_dup_grouping_con(self):
        row1 = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher1',
            'Orduak': 2,
            'Aula': '1_3A',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3A',
            'Maila': '3.DBH',
            'Tipo': 'independiente',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': '3-Sub1'}
        row2 = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher2',
            'Orduak': 2,
            'Aula': '1_3B',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3B',
            'Maila': '3.DBH',
            'Tipo': 'independiente',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': '3-Sub1'}
        Data.objects.create_data(row1)
        with self.assertRaises(Exception) as raised:
            Data.objects.create_data(row2)
        self.assertEqual(IntegrityError, type(raised.exception))
        self.assertIn('UNIQUE constraint failed', str(raised.exception))

    def test_gen_dept_meetings(self):
        print('--------------')
        row = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher1',
            'Orduak': 2,
            'Aula': '1_3A',
            'Loturak': '',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3A',
            'Maila': '3.DBH',
            'Tipo': 'independiente',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': ''}
        Data.objects.create_data(row)
        row = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher2',
            'Orduak': 2,
            'Aula': '1_3A',
            'Loturak': '',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3A',
            'Maila': '3.DBH',
            'Tipo': 'independiente',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject2',
            'AgrupacionEDUCA': ''}
        Data.objects.create_data(row)
        TimetableSettings.objects.create(key='deptbuildings', value='2')
        ct = ConexionType.objects.create(name='bilera', ctype='ME')
        Data.objects.create_dept_meetings()
        dataCount = Data.objects.filter(Type=ct).count()
        self.assertEqual(dataCount, 2)

    def test_gen_dept_meetings_rooms(self):
        row = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher1',
            'Orduak': 2,
            'Aula': '1_3A',
            'Loturak': '',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3A',
            'Maila': '3.DBH',
            'Tipo': 'independiente',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': ''}
        Data.objects.create_data(row)
        TimetableSettings.objects.create(key='deptbuildings', value='2')
        ct = ConexionType.objects.create(name='bilera', ctype='ME')
        Data.objects.create_dept_meetings()
        roomCount = Data.objects.filter(Type=ct).first().Room.all().count()
        self.assertEqual(roomCount, 2)
        #I thougth Rooms were not assigned to data record!

class ConexionTypeTestCase(TestCase):

    def test_con_type(self):
        row = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher1',
            'Orduak': 2,
            'Aula': '1_3A',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3A',
            'Maila': '3.DBH',
            'Tipo': 'independiente',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': '3-Sub1'}
        d = Data.objects.create_data(row)
        c = ConexionType.objects.get(name='independiente')
        self.assertEqual(row['Tipo'], c.name)
        self.assertEqual(c, d.Type)


class TeachersTestCase(TestCase):

    def test_teachers(self):
        row1 = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher1',
            'Orduak': 2,
            'Aula': '1_3A',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3A',
            'Maila': '3.DBH',
            'Tipo': 'independiente',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': '3-Sub1'}
        row2 = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher2',
            'Orduak': 2,
            'Aula': '1_3B',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3B',
            'Maila': '3.DBH',
            'Tipo': 'independiente',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': '3-Sub2'}
        Data.objects.create_data(row1)
        Data.objects.create_data(row2)
        teacherCount = Teacher.objects.all().count()
        self.assertEqual(teacherCount, 2)

    def test_create_teacher(self):
        row = {'Irakaslea': 'Teacher1',
            'Zaintza_Kop': 1,
            'NumHoras': 20,
            'Max_Dias_Sem': '',
            'Max_intervalo_dia': '',
            'CompTutoría': 3,
            'compensacion_gt_20': 0,
            'HorasContrato': 20,
            'Complementarias': '',
            'Reducción': 0,
            'Max_horas_dia': '',
            'Edificios': 1,
            'HorasTutoria': 3,
            'Mas_It_Sem': 1,
            'Max_huecos_semana': '',
            'Max_huecos_días': ''}
        Teacher.objects.update_teacher(row)
        teacher = Teacher.objects.get(name=row['Irakaslea'])
        self.assertEqual(teacher.classHours, row['NumHoras'])

class ActivitiesTestCase(TestCase):

    def test_activity(self):
        row = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher1',
            'Orduak': 2,
            'Aula': '1_3A',
            'Loturak': '',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3A',
            'Maila': '3.DBH',
            'Tipo': 'independiente',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': ''}
        data = Data.objects.create_data(row)
        Activity.objects.create_activities(data)
        activities = Activity.objects.filter(Data=data).count()
        self.assertEqual(activities, row['Orduak'])

    def test_con(self):
        row = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher1',
            'Orduak': 2,
            'Aula': '1_3A',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3A',
            'Maila': '3.DBH',
            'Tipo': 'h',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': ''}
        data = Data.objects.create_data(row)
        Activity.objects.create_activities(data)
        row = {'Mintegia': 'Dept2',
            'Irakaslea': 'Teacher2',
            'Orduak': 2,
            'Aula': '1_3B',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3B',
            'Maila': '3.DBH',
            'Tipo': 'h',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject2',
            'AgrupacionEDUCA': ''}
        data = Data.objects.create_data(row)
        Activity.objects.create_activities(data)
        Activity.objects.create_conexions()
        activitiesCount = ActivityConexion.objects.filter(conexion=row['Loturak']).count()
        self.assertEqual(activitiesCount, 2)

    def test_con_groups(self):
        row = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher1',
            'Orduak': 2,
            'Aula': '1_3A',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3A',
            'Maila': '3.DBH',
            'Tipo': 'h',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': ''}
        data = Data.objects.create_data(row)
        Activity.objects.create_activities(data)
        row = {'Mintegia': 'Dept2',
            'Irakaslea': 'Teacher2',
            'Orduak': 2,
            'Aula': '1_3B',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3B',
            'Maila': '3.DBH',
            'Tipo': 'h',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject2',
            'AgrupacionEDUCA': ''}
        data = Data.objects.create_data(row)
        Activity.objects.create_activities(data)
        Activity.objects.create_conexions()
        activities = ActivityConexion.objects.filter(subconexion='C1_'+row['Loturak'])
        self.assertNotEqual(activities[0].activity.all()[0].Data, activities[0].activity.all()[1].Data)
        #FIXME: test activities groups, it does now join the same and not mixing


class XMLGenerationTestCase(TestCase):

    def test_sameStartingTimeXML(self):
        row = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher1',
            'Orduak': 2,
            'Aula': '1_3A',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3A',
            'Maila': '3.DBH',
            'Tipo': 'h',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': ''}
        data = Data.objects.create_data(row)
        Activity.objects.create_activities(data)
        row = {'Mintegia': 'Dept2',
            'Irakaslea': 'Teacher2',
            'Orduak': 2,
            'Aula': '1_3B',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3B',
            'Maila': '3.DBH',
            'Tipo': 'h',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject2',
            'AgrupacionEDUCA': ''}
        data = Data.objects.create_data(row)
        Activity.objects.create_activities(data)
        Activity.objects.create_conexions()
        sameTimeActivities = ActivityConexion.objects.generate_conexion_xml()
        expectedResult = '''<ConstraintActivitiesSameStartingTime>
            <Weight_Percentage>100</Weight_Percentage>
            <Number_of_Activities>2</Number_of_Activities>
            <Activity_Id>1</Activity_Id>
            <Activity_Id>3</Activity_Id>
            <Active>true</Active>
            <Comments> </Comments>
        </ConstraintActivitiesSameStartingTime>
        ''','''<ConstraintActivitiesSameStartingTime>
            <Weight_Percentage>100</Weight_Percentage>
            <Number_of_Activities>2</Number_of_Activities>
            <Activity_Id>2</Activity_Id>
            <Activity_Id>4</Activity_Id>
            <Active>true</Active>
            <Comments> </Comments>
        </ConstraintActivitiesSameStartingTime>
        '''
        for i, item in enumerate(sameTimeActivities):
            self.assertXMLEqual(item,expectedResult[i])

    def test_ActivityXML(self):
        row = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher1',
            'Orduak': 2,
            'Aula': '1_3A',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3A',
            'Maila': '3.DBH',
            'Tipo': 'h',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': ''}
        data = Data.objects.create_data(row)
        Activity.objects.create_activities(data)
        activities = Activity.objects.create_activity_XML()
        expectedResult = '''<Activity>
            <Subject>Subject1</Subject>
            <Students>3A</Students>
            <Duration>1</Duration>
            <Total_Duration>2</Total_Duration>
            <Id>1</Id>
            <Activity_Group_Id>1</Activity_Group_Id>
            <Active>true</Active>
            <Comments> </Comments>
        </Activity>
        ''','''<Activity>
            <Subject>Subject1</Subject>
            <Students>3A</Students>
            <Duration>1</Duration>
            <Total_Duration>2</Total_Duration>
            <Id>2</Id>
            <Activity_Group_Id>1</Activity_Group_Id>
            <Active>true</Active>
            <Comments> </Comments>
        </Activity>        
        '''
        for i, item in enumerate(activities):
            self.assertXMLEqual(item,expectedResult[i])
        

    def test_subjectsXML(self):
        row = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher1',
            'Orduak': 2,
            'Aula': '1_3A',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3A',
            'Maila': '3.DBH',
            'Tipo': 'h',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': ''}
        data = Data.objects.create_data(row)
        Activity.objects.create_activities(data)
        row = {'Mintegia': 'Dept2',
            'Irakaslea': 'Teacher2',
            'Orduak': 2,
            'Aula': '1_3B',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3B',
            'Maila': '3.DBH',
            'Tipo': 'h',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject2',
            'AgrupacionEDUCA': ''}
        data = Data.objects.create_data(row)
        subjectsResult = Data.objects.create_subjects_xml()
        expectedResult = '''<Subjects_List>
            <Subject>
                    <Name>Subject1</Name>
                    <Comments></Comments>
            </Subject>
            <Subject>
                    <Name>Subject2</Name>
                    <Comments></Comments>
            </Subject>
        </Subjects_List>
        '''
        self.assertXMLEqual(subjectsResult, expectedResult)
        
    def test_teacherXML(self):
        row = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher1',
            'Orduak': 2,
            'Aula': '1_3A',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3A',
            'Maila': '3.DBH',
            'Tipo': 'h',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': ''}
        data = Data.objects.create_data(row)
        Activity.objects.create_activities(data)
        row = {'Mintegia': 'Dept2',
            'Irakaslea': 'Teacher2',
            'Orduak': 2,
            'Aula': '1_3B',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3B',
            'Maila': '3.DBH',
            'Tipo': 'h',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject2',
            'AgrupacionEDUCA': ''}
        data = Data.objects.create_data(row)
        subjectsResult = Data.objects.create_teachers_xml()
        expectedResult = '''<Teachers_List>
            <Teacher>
                    <Name>Teacher1</Name>
                    <Target_Number_of_Hours>0</Target_Number_of_Hours>
                    <Qualified_Subjects>
                    </Qualified_Subjects>
                    <Comments></Comments>
            </Teacher>
            <Teacher>
                    <Name>Teacher2</Name>
                    <Target_Number_of_Hours>0</Target_Number_of_Hours>
                    <Qualified_Subjects>
                    </Qualified_Subjects>
                    <Comments></Comments>
            </Teacher>
        </Teachers_List>
        '''
        self.assertXMLEqual(subjectsResult, expectedResult)
        
    def test_studentsXML(self):
        row = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher1',
            'Orduak': 2,
            'Aula': '1_3A',
            'Loturak': '3AG_001',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3A',
            'Maila': '3.DBH',
            'Tipo': 'h',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': '3-Sub1'}
        d = Data.objects.create_data(row)
        row = {'Mintegia': 'Dept1',
            'Irakaslea': 'Teacher1',
            'Orduak': 2,
            'Aula': '1_3B',
            'Loturak': '3AG_002',
            'Oharrak': '',
            'Kopurua': 49,
            'Taldea': '3B',
            'Maila': '3.DBH',
            'Tipo': 'h',
            'Eredua': 'AG',
            'OharrakMintegitik': '',
            'Ikasgaia': 'Subject1',
            'AgrupacionEDUCA': '3-Sub1'}
        d = Data.objects.create_data(row)
        expectedResult = '''
        <Students_List>
            <Year>
                <Name>3.DBH</Name>
                <Number_of_Students>0</Number_of_Students>
                <Comments></Comments>
                <Group>
                    <Name>3A</Name>
                    <Number_of_Students>0</Number_of_Students>
                    <Comments></Comments>
                    <Subgroup>
                        <Name>3A_3-Sub1</Name>
                        <Number_of_Students>0</Number_of_Students>
                        <Comments></Comments>
                    </Subgroup>
                </Group>
                <Group>
                    <Name>3B</Name>
                    <Number_of_Students>0</Number_of_Students>
                    <Comments></Comments>
                    <Subgroup>
                        <Name>3B_3-Sub1</Name>
                        <Number_of_Students>0</Number_of_Students>
                        <Comments></Comments>
                    </Subgroup>
                </Group>
                <Group>
                    <Name>3-Sub1</Name>
                    <Number_of_Students>0</Number_of_Students>
                    <Comments></Comments>
                    <Subgroup>
                        <Name>3A_3-Sub1</Name>
                        <Number_of_Students>0</Number_of_Students>
                        <Comments></Comments>
                    </Subgroup>
                    <Subgroup>
                        <Name>3B_3-Sub1</Name>
                        <Number_of_Students>0</Number_of_Students>
                        <Comments></Comments>
                    </Subgroup>
                </Group>
            </Year>
        </Students_List>
        '''
        studentsXML = Group.objects.create_students_xml()
        self.assertXMLEqual(expectedResult, studentsXML)
        # because of this test OrderedDict() is used 

