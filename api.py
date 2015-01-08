import os
import MySQLdb
import json
import endpoints
from random import randint


from protorpc import messages
from protorpc import message_types
from protorpc import remote

package = 'isb-cgc-api'

def rand():
    return randint(1, 1000)

# Database connection
env = os.getenv('SERVER_SOFTWARE')
if env and env.startswith('Google App Engine/') or os.getenv('SETTINGS_MODE') == 'prod':
    # Connecting from App Engine
    db = MySQLdb.connect(
        unix_socket='/cloudsql/isb-cgc:demo01',
        db='demo',
        user='root',
    )
else:
    # Connecting to localhost
    db = MySQLdb.connect(host='127.0.0.1', port=3306, db='test', user='root')

class ReturnJSON(messages.Message):
    msg = messages.StringField(1)

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
    TP53                                 = messages.StringField(37)
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

class FMAttrValue(messages.Message):
    value = messages.StringField(1)

class FMAttrList(messages.Message):
    sample                               = messages.MessageField(FMAttrValue, 1, repeated=True)
    percent_lymphocyte_infiltration      = messages.MessageField(FMAttrValue, 2, repeated=True)
    percent_monocyte_infiltration        = messages.MessageField(FMAttrValue, 3, repeated=True)
    percent_necrosis                     = messages.MessageField(FMAttrValue, 4, repeated=True)
    percent_neutrophil_infiltration      = messages.MessageField(FMAttrValue, 5, repeated=True)
    percent_normal_cells                 = messages.MessageField(FMAttrValue, 6, repeated=True)
    percent_stromal_cells                = messages.MessageField(FMAttrValue, 7, repeated=True)
    percent_tumor_cells                  = messages.MessageField(FMAttrValue, 8, repeated=True)
    percent_tumor_nuclei                 = messages.MessageField(FMAttrValue, 9, repeated=True)
    gender                               = messages.MessageField(FMAttrValue, 10, repeated=True)
    history_of_neoadjuvant_treatment     = messages.MessageField(FMAttrValue, 11, repeated=True)
    icd_o_3_histology                    = messages.MessageField(FMAttrValue, 12, repeated=True)
    prior_dx                             = messages.MessageField(FMAttrValue, 13, repeated=True)
    vital_status                         = messages.MessageField(FMAttrValue, 14, repeated=True)
    country                              = messages.MessageField(FMAttrValue, 15, repeated=True)
    disease_code                         = messages.MessageField(FMAttrValue, 16, repeated=True)
    histological_type                    = messages.MessageField(FMAttrValue, 17, repeated=True)
    icd_10                               = messages.MessageField(FMAttrValue, 18, repeated=True)
    icd_o_3_site                         = messages.MessageField(FMAttrValue, 19, repeated=True)
    tumor_tissue_site                    = messages.MessageField(FMAttrValue, 20, repeated=True)
    tumor_type                           = messages.MessageField(FMAttrValue, 21, repeated=True)
    age_at_initial_pathologic_diagnosis  = messages.MessageField(FMAttrValue, 22, repeated=True)
    days_to_birth                        = messages.MessageField(FMAttrValue, 23, repeated=True)
    days_to_initial_pathologic_diagnosis = messages.MessageField(FMAttrValue, 24, repeated=True)
    year_of_initial_pathologic_diagnosis = messages.MessageField(FMAttrValue, 25, repeated=True)
    days_to_last_known_alive             = messages.MessageField(FMAttrValue, 26, repeated=True)
    tumor_necrosis_percent               = messages.MessageField(FMAttrValue, 27, repeated=True)
    tumor_nuclei_percent                 = messages.MessageField(FMAttrValue, 28, repeated=True)
    tumor_weight                         = messages.MessageField(FMAttrValue, 29, repeated=True)
    person_neoplasm_cancer_status        = messages.MessageField(FMAttrValue, 30, repeated=True)
    pathologic_N                         = messages.MessageField(FMAttrValue, 31, repeated=True)
    radiation_therapy                    = messages.MessageField(FMAttrValue, 32, repeated=True)
    pathologic_T                         = messages.MessageField(FMAttrValue, 33, repeated=True)
    race                                 = messages.MessageField(FMAttrValue, 34, repeated=True)
    days_to_last_followup                = messages.MessageField(FMAttrValue, 35, repeated=True)
    ethnicity                            = messages.MessageField(FMAttrValue, 36, repeated=True)
    TP53                                 = messages.MessageField(FMAttrValue, 37, repeated=True)
    RB1                                  = messages.MessageField(FMAttrValue, 38, repeated=True)
    NF1                                  = messages.MessageField(FMAttrValue, 39, repeated=True)
    APC                                  = messages.MessageField(FMAttrValue, 40, repeated=True)
    CTNNB1                               = messages.MessageField(FMAttrValue, 41, repeated=True)
    PIK3CA                               = messages.MessageField(FMAttrValue, 42, repeated=True)
    PTEN                                 = messages.MessageField(FMAttrValue, 43, repeated=True)
    FBXW7                                = messages.MessageField(FMAttrValue, 44, repeated=True)
    NRAS                                 = messages.MessageField(FMAttrValue, 45, repeated=True)
    ARID1A                               = messages.MessageField(FMAttrValue, 46, repeated=True)
    CDKN2A                               = messages.MessageField(FMAttrValue, 47, repeated=True)
    SMAD4                                = messages.MessageField(FMAttrValue, 48, repeated=True)
    BRAF                                 = messages.MessageField(FMAttrValue, 49, repeated=True)
    NFE2L2                               = messages.MessageField(FMAttrValue, 50, repeated=True)
    IDH1                                 = messages.MessageField(FMAttrValue, 51, repeated=True)
    PIK3R1                               = messages.MessageField(FMAttrValue, 52, repeated=True)
    HRAS                                 = messages.MessageField(FMAttrValue, 53, repeated=True)
    EGFR                                 = messages.MessageField(FMAttrValue, 54, repeated=True)
    BAP1                                 = messages.MessageField(FMAttrValue, 55, repeated=True)
    KRAS                                 = messages.MessageField(FMAttrValue, 56, repeated=True)
    sampleType                           = messages.MessageField(FMAttrValue, 57, repeated=True)


@endpoints.api(name='gae_endpoints', version='v1',)
class GAE_Endpoints_API(remote.Service):


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
                            TP53                                 = str(row[36]),
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
                      name='fmdata.getFmdata')
    def fmdata_list(self, request):

        query_dict = {}

        for key, value in FMItem.__dict__.items():
            if not key.startswith('_'):
                if request.__getattribute__(key) != None:
                    query_dict[key] = request.__getattribute__(key)

        if len(query_dict) == 0:
            query_str = 'SELECT * FROM fmdata'
        else:
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
                                    TP53                                 = str(row[36]),
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

    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.StringField(1))
    @endpoints.method(ID_RESOURCE, FMItem,
                      path='fmdata_attr', http_method='GET',
                      name='fmdata.getFmdata_attr')
    def fmdata_get(self, request):
        key_list = []

        for key, value in FMItem.__dict__.items():
            if not key.startswith('_'):
                key_list.append(key)

        try:
            cursor = db.cursor()
            value_list = {}
            for key in key_list:
                query_str = 'SELECT DISTINCT %s FROM fmdata;' % key
                print query_str
                cursor.execute(query_str)

                value_list[key] = []
                for row in cursor.fetchall():
                    value_list[key].append(row[0])
            return FMItem(  sample                               = str(value_list['sample']),
                            percent_lymphocyte_infiltration      = str(value_list['percent_lymphocyte_infiltration']),
                            percent_monocyte_infiltration        = str(value_list['percent_monocyte_infiltration']),
                            percent_necrosis                     = str(value_list['percent_necrosis']),
                            percent_neutrophil_infiltration      = str(value_list['percent_neutrophil_infiltration']),
                            percent_normal_cells                 = str(value_list['percent_normal_cells']),
                            percent_stromal_cells                = str(value_list['percent_stromal_cells']),
                            percent_tumor_cells                  = str(value_list['percent_tumor_cells']),
                            percent_tumor_nuclei                 = str(value_list['percent_tumor_nuclei']),
                            gender                               = str(value_list['gender']),
                            history_of_neoadjuvant_treatment     = str(value_list['history_of_neoadjuvant_treatment']),
                            icd_o_3_histology                    = str(value_list['icd_o_3_histology']),
                            prior_dx                             = str(value_list['prior_dx']),
                            vital_status                         = str(value_list['vital_status']),
                            country                              = str(value_list['country']),
                            disease_code                         = str(value_list['disease_code']),
                            histological_type                    = str(value_list['histological_type']),
                            icd_10                               = str(value_list['icd_10']),
                            icd_o_3_site                         = str(value_list['icd_o_3_site']),
                            tumor_tissue_site                    = str(value_list['tumor_tissue_site']),
                            tumor_type                           = str(value_list['tumor_type']),
                            age_at_initial_pathologic_diagnosis  = str(value_list['age_at_initial_pathologic_diagnosis']),
                            days_to_birth                        = str(value_list['days_to_birth']),
                            days_to_initial_pathologic_diagnosis = str(value_list['days_to_initial_pathologic_diagnosis']),
                            year_of_initial_pathologic_diagnosis = str(value_list['year_of_initial_pathologic_diagnosis']),
                            days_to_last_known_alive             = str(value_list['days_to_last_known_alive']),
                            tumor_necrosis_percent               = str(value_list['tumor_necrosis_percent']),
                            tumor_nuclei_percent                 = str(value_list['tumor_nuclei_percent']),
                            tumor_weight                         = str(value_list['tumor_weight']),
                            person_neoplasm_cancer_status        = str(value_list['person_neoplasm_cancer_status']),
                            pathologic_N                         = str(value_list['pathologic_N']),
                            radiation_therapy                    = str(value_list['radiation_therapy']),
                            pathologic_T                         = str(value_list['pathologic_T']),
                            race                                 = str(value_list['race']),
                            days_to_last_followup                = str(value_list['days_to_last_followup']),
                            ethnicity                            = str(value_list['ethnicity']),
                            TP53                                 = str(value_list['TP53']),
                            RB1                                  = str(value_list['RB1']),
                            NF1                                  = str(value_list['NF1']),
                            APC                                  = str(value_list['APC']),
                            CTNNB1                               = str(value_list['CTNNB1']),
                            PIK3CA                               = str(value_list['PIK3CA']),
                            PTEN                                 = str(value_list['PTEN']),
                            FBXW7                                = str(value_list['FBXW7']),
                            NRAS                                 = str(value_list['NRAS']),
                            ARID1A                               = str(value_list['ARID1A']),
                            CDKN2A                               = str(value_list['CDKN2A']),
                            SMAD4                                = str(value_list['SMAD4']),
                            BRAF                                 = str(value_list['BRAF']),
                            NFE2L2                               = str(value_list['NFE2L2']),
                            IDH1                                 = str(value_list['IDH1']),
                            PIK3R1                               = str(value_list['PIK3R1']),
                            HRAS                                 = str(value_list['HRAS']),
                            EGFR                                 = str(value_list['EGFR']),
                            BAP1                                 = str(value_list['BAP1']),
                            KRAS                                 = str(value_list['KRAS']),
                            sampleType                           = str(value_list['sampleType']),
                            )
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Error computing attributes.')
APPLICATION = endpoints.api_server([GAE_Endpoints_API])