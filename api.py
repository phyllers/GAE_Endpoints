import os
import MySQLdb
import json
import endpoints
from random import randint


from protorpc import messages
from protorpc import message_types
from protorpc import remote

package = 'hello'
class Greeting(messages.Message):
    message = messages.StringField(1)

class GreetingCollection(messages.Message):
    items = messages.MessageField(Greeting, 1, repeated=True)

STORED_GREETINGS = GreetingCollection(items=[
    Greeting(message='Hello World!'),
    Greeting(message='Goodbye Cruel World!'),
])

class ReturnJSON(messages.Message):
    msg = messages.StringField(1)

def rand():
    return randint(1, 1000)

env = os.getenv('SERVER_SOFTWARE')
if env and env.startswith('Google App Engine/') or os.getenv('SETTINGS_MODE') == 'prod':
    # Connecting from App Engine
    db = MySQLdb.connect(
        unix_socket='/cloudsql/striking-berm-771:django-test',
        db='pong',
        user='root',
    )
else:
    # Connecting from an external network.
    # Make sure your network is whitelisted
    db = MySQLdb.connect(host='127.0.0.1', port=3306, db='test', user='root')

class DBItem(messages.Message):
    id = messages.IntegerField(1)
    content = messages.StringField(2)
    date = messages.StringField(3)

class DBItemList(messages.Message):
    items = messages.MessageField(DBItem, 1, repeated=True)

class FMItem(messages.Message):
    sample                               = messages.StringField(1)
    percent_lymphocyte_infiltration      = messages.StringField(2)
    percent_monocyte_infiltration        = messages.StringField(3)
    percent_necrosis                     = messages.StringField(4)
    percent_neutrophil_infiltration      = messages.StringField(5)
    percent_normal_cells                 = messages.StringField(6)
    percent_stromal_cells                = messages.StringField(7)
    percent_tumor_cells                  = messages.StringField(8)
    percent_tumor_nuclei                 = messages.StringField(9)
    gender                               = messages.StringField(10)
    history_of_neoadjuvant_treatment     = messages.StringField(11)
    icd_o_3_histology                    = messages.StringField(12)
    prior_dx                             = messages.StringField(13)
    vital_status                         = messages.StringField(14)
    country                              = messages.StringField(15)
    disease_code                         = messages.StringField(16)
    histological_type                    = messages.StringField(17)
    icd_10                               = messages.StringField(18)
    icd_o_3_site                         = messages.StringField(19)
    tumor_tissue_site                    = messages.StringField(20)
    tumor_type                           = messages.StringField(21)
    age_at_initial_pathologic_diagnosis  = messages.StringField(22)
    days_to_birth                        = messages.StringField(23)
    days_to_initial_pathologic_diagnosis = messages.StringField(24)
    year_of_initial_pathologic_diagnosis = messages.StringField(25)
    days_to_last_known_alive             = messages.StringField(26)
    tumor_necrosis_percent               = messages.StringField(27)
    tumor_nuclei_percent                 = messages.StringField(28)
    tumor_weight                         = messages.StringField(29)
    person_neoplasm_cancer_status        = messages.StringField(30)
    pathologic_N                         = messages.StringField(31)
    radiation_therapy                    = messages.StringField(32)
    pathologic_T                         = messages.StringField(33)
    race                                 = messages.StringField(34)
    days_to_last_followup                = messages.StringField(35)
    ethnicity                            = messages.StringField(36)
    P53                                  = messages.StringField(37)
    RB1                                  = messages.StringField(38)
    NF1                                  = messages.StringField(39)
    APC                                  = messages.StringField(40)
    CTNNB1                               = messages.StringField(41)
    PIK3CA                               = messages.StringField(42)
    PTEN                                 = messages.StringField(43)
    FBXW7                                = messages.StringField(44)
    NRAS                                 = messages.StringField(45)
    ARID1A                               = messages.StringField(46)
    CDKN2A                               = messages.StringField(47)
    SMAD4                                = messages.StringField(48)
    BRAF                                 = messages.StringField(49)
    NFE2L2                               = messages.StringField(50)
    IDH1                                 = messages.StringField(51)
    PIK3R1                               = messages.StringField(52)
    HRAS                                 = messages.StringField(53)
    EGFR                                 = messages.StringField(54)
    BAP1                                 = messages.StringField(55)
    KRAS                                 = messages.StringField(56)
    sampleType                           = messages.StringField(57)

class FMItemList(messages.Message):
    items = messages.MessageField(FMItem, 1, repeated=True)


@endpoints.api(name='gae_endpoints', version='v1',)
class GAE_Endpoints_API(remote.Service):

    MULTIPLY_METHOD_RESOURCE = endpoints.ResourceContainer(
        Greeting,
        times=messages.IntegerField(2, variant=messages.Variant.INT32,
                                    required=True))
    @endpoints.method(MULTIPLY_METHOD_RESOURCE, Greeting,
                      path='hellogreeting/{times}', http_method='POST',
                      name='greetings.mulitply')
    def greetings_multiply(self, request):
        return Greeting(message=request.message * request.times)

    @endpoints.method(message_types.VoidMessage, DBItemList,
                      path='hellogreeting', http_method='GET',
                      name='greetings.listGreeting',)
    def greetings_list(self, unused_request):
        cursor = db.cursor()
        cursor.execute('SELECT id, content, date FROM testapp_greeting;')
        data = []
        for row in cursor.fetchall():
            data.append(DBItem(id=row[0],
                               content=row[1],
                               date=row[2].isoformat()))

        return DBItemList(items=data)

    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.IntegerField(1, variant=messages.Variant.INT32))
    @endpoints.method(ID_RESOURCE, DBItem,
                      path='hellogreeting/{id}', http_method='GET',
                      name='greetings.getGreeting')
    def greeting_get(self, request):
        try:
            cursor = db.cursor()
            cursor.execute('SELECT id, content, date FROM testapp_greeting where id=%s;' % request.id)
            row = cursor.fetchone()
            return DBItem(id=row[0], content=row[1], date=row[2].isoformat())
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Greeting %s not found.' % (request.id,))

    @endpoints.method(message_types.VoidMessage, Greeting,
                      path='hellogreetings/authed', http_method='POST',
                      name='greetings.authed',)
    def greeting_authed(self, request):
        current_user = endpoints.get_current_user()
        email = (current_user.email() if current_user is not None else 'Anonymous')
        return Greeting(message='Hello %s' % (email,))

    @endpoints.method(message_types.VoidMessage, ReturnJSON,
                      path='fake_data', http_method='GET',
                      name='fake.data')
    def fake_data(self, request):
        data = {'test': "Hello world"}
        ret = ReturnJSON(msg=json.dumps(data))
        return ret

    @endpoints.method(message_types.VoidMessage, ReturnJSON,
                      path='rand_int', http_method='GET',
                      name='rand.int')
    def fake_random_data(self, request):
        data = {'int': rand()}
        ret = ReturnJSON(msg=json.dumps(data))
        return ret

    @endpoints.method(message_types.VoidMessage, ReturnJSON,
                      path='fake_treegraph_data', http_method='GET',
                      name='fake.treegraph.data')
    def fake_treegraph_data(self, request):
        data = {
            "children": [
            {
            "name": "Project",
            "children": [
                  {"name": "BLCA-US", "size": 3938},
              {"name": "BLCA-CN", "size": 3812},
              {"name": "BOCA-UK", "size": 6714},
              {"name": "GBM-US", "size": 743}
               ]
            },
            {
            "name": "Primary Site",
            "children": [
                {"name": "Brain", "size": 17010},
                {"name": "Breast", "size": 5842},
                {"name": "Blood", "size": 1983},
                {"name": "Lung", "size": 2047},
                {"name": "Head and Neck", "size": 1375},
                {"name": "Kidney", "size": 2202},
                {"name": "Liver", "size": 1382}
            ]
            },
            {
            "name": "Gender",
            "children": [
              {"name": "Male", "size": 4721},
              {"name": "Female", "size": 4294}
             ]
            },

            {
            "name": "Tumor Stage",
            "children": [
            {"name": "No Data", "size": 8833},
            {"name": "Others", "size": 1732},
            {"name": "4", "size": 3623},
            {"name": "A", "size": 10066}
            ]
            }
            ]}
        ret = ReturnJSON(msg=json.dumps(data))
        return ret

    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.StringField(1))
    @endpoints.method(ID_RESOURCE, FMItem,
                      path='fmdata/{id}', http_method='GET',
                      name='fmdata.getFmdata')
    def fmdata_get(self, request):
        try:
            cursor = db.cursor()
            cursor.execute('SELECT * FROM fmdata where sample="%s";' % request.id)
            row = cursor.fetchone()
            return FMItem(  sample                               = str(row[0]),
                            percent_lymphocyte_infiltration      = str(row[1]),
                            percent_monocyte_infiltration        = str(row[2]),
                            percent_necrosis                     = str(row[3]),
                            percent_neutrophil_infiltration      = str(row[4]),
                            percent_normal_cells                 = str(row[5]),
                            percent_stromal_cells                = str(row[6]),
                            percent_tumor_cells                  = str(row[7]),
                            percent_tumor_nuclei                 = str(row[8]),
                            gender                               = str(row[9]),
                            history_of_neoadjuvant_treatment     = str(row[10]),
                            icd_o_3_histology                    = str(row[11]),
                            prior_dx                             = str(row[12]),
                            vital_status                         = str(row[13]),
                            country                              = str(row[14]),
                            disease_code                         = str(row[15]),
                            histological_type                    = str(row[16]),
                            icd_10                               = str(row[17]),
                            icd_o_3_site                         = str(row[18]),
                            tumor_tissue_site                    = str(row[19]),
                            tumor_type                           = str(row[20]),
                            age_at_initial_pathologic_diagnosis  = str(row[21]),
                            days_to_birth                        = str(row[22]),
                            days_to_initial_pathologic_diagnosis = str(row[23]),
                            year_of_initial_pathologic_diagnosis = str(row[24]),
                            days_to_last_known_alive             = str(row[25]),
                            tumor_necrosis_percent               = str(row[26]),
                            tumor_nuclei_percent                 = str(row[27]),
                            tumor_weight                         = str(row[28]),
                            person_neoplasm_cancer_status        = str(row[29]),
                            pathologic_N                         = str(row[30]),
                            radiation_therapy                    = str(row[31]),
                            pathologic_T                         = str(row[32]),
                            race                                 = str(row[33]),
                            days_to_last_followup                = str(row[34]),
                            ethnicity                            = str(row[35]),
                            P53                                  = str(row[36]),
                            RB1                                  = str(row[37]),
                            NF1                                  = str(row[38]),
                            APC                                  = str(row[39]),
                            CTNNB1                               = str(row[40]),
                            PIK3CA                               = str(row[41]),
                            PTEN                                 = str(row[42]),
                            FBXW7                                = str(row[43]),
                            NRAS                                 = str(row[44]),
                            ARID1A                               = str(row[45]),
                            CDKN2A                               = str(row[46]),
                            SMAD4                                = str(row[47]),
                            BRAF                                 = str(row[48]),
                            NFE2L2                               = str(row[49]),
                            IDH1                                 = str(row[50]),
                            PIK3R1                               = str(row[51]),
                            HRAS                                 = str(row[52]),
                            EGFR                                 = str(row[53]),
                            BAP1                                 = str(row[54]),
                            KRAS                                 = str(row[55]),
                            sampleType                           = str(row[56]),
                            )
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Sample %s not found.' % (request.id,))

    GET_RESOURCE = endpoints.ResourceContainer(
        FMItem,
        tester=messages.StringField(2))
    @endpoints.method(GET_RESOURCE, FMItemList,
                      path='fmdata', http_method='GET',
                      name='fmdata.fmdata')
    def fmdata_list(self, request):

        query_dict = {}

        for key, value in FMItem.__dict__.items():
            if not key.startswith('_'):
                if request.__getattribute__(key) != None:
                    query_dict[key] = request.__getattribute__(key)

        query_str = 'SELECT * FROM fmdata where'

        first = True
        for key, value in query_dict.items():
            if first:
                first = False
                query_str += ' %s="%s"' % (key, value)
            else:
                query_str += ' and %s="%s"' % (key, value)

        try:

            cursor = db.cursor()
            cursor.execute(query_str)
            data = []
            for row in cursor.fetchall():
                data.append(FMItem( sample                               = str(row[0]),
                                    percent_lymphocyte_infiltration      = str(row[1]),
                                    percent_monocyte_infiltration        = str(row[2]),
                                    percent_necrosis                     = str(row[3]),
                                    percent_neutrophil_infiltration      = str(row[4]),
                                    percent_normal_cells                 = str(row[5]),
                                    percent_stromal_cells                = str(row[6]),
                                    percent_tumor_cells                  = str(row[7]),
                                    percent_tumor_nuclei                 = str(row[8]),
                                    gender                               = str(row[9]),
                                    history_of_neoadjuvant_treatment     = str(row[10]),
                                    icd_o_3_histology                    = str(row[11]),
                                    prior_dx                             = str(row[12]),
                                    vital_status                         = str(row[13]),
                                    country                              = str(row[14]),
                                    disease_code                         = str(row[15]),
                                    histological_type                    = str(row[16]),
                                    icd_10                               = str(row[17]),
                                    icd_o_3_site                         = str(row[18]),
                                    tumor_tissue_site                    = str(row[19]),
                                    tumor_type                           = str(row[20]),
                                    age_at_initial_pathologic_diagnosis  = str(row[21]),
                                    days_to_birth                        = str(row[22]),
                                    days_to_initial_pathologic_diagnosis = str(row[23]),
                                    year_of_initial_pathologic_diagnosis = str(row[24]),
                                    days_to_last_known_alive             = str(row[25]),
                                    tumor_necrosis_percent               = str(row[26]),
                                    tumor_nuclei_percent                 = str(row[27]),
                                    tumor_weight                         = str(row[28]),
                                    person_neoplasm_cancer_status        = str(row[29]),
                                    pathologic_N                         = str(row[30]),
                                    radiation_therapy                    = str(row[31]),
                                    pathologic_T                         = str(row[32]),
                                    race                                 = str(row[33]),
                                    days_to_last_followup                = str(row[34]),
                                    ethnicity                            = str(row[35]),
                                    P53                                  = str(row[36]),
                                    RB1                                  = str(row[37]),
                                    NF1                                  = str(row[38]),
                                    APC                                  = str(row[39]),
                                    CTNNB1                               = str(row[40]),
                                    PIK3CA                               = str(row[41]),
                                    PTEN                                 = str(row[42]),
                                    FBXW7                                = str(row[43]),
                                    NRAS                                 = str(row[44]),
                                    ARID1A                               = str(row[45]),
                                    CDKN2A                               = str(row[46]),
                                    SMAD4                                = str(row[47]),
                                    BRAF                                 = str(row[48]),
                                    NFE2L2                               = str(row[49]),
                                    IDH1                                 = str(row[50]),
                                    PIK3R1                               = str(row[51]),
                                    HRAS                                 = str(row[52]),
                                    EGFR                                 = str(row[53]),
                                    BAP1                                 = str(row[54]),
                                    KRAS                                 = str(row[55]),
                                    sampleType                           = str(row[56])
                                    ))
            return FMItemList(items=data)
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Sample %s not found.' % (request.id,))

APPLICATION = endpoints.api_server([GAE_Endpoints_API])