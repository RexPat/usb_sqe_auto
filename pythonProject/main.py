import xmltodict
import pprint
import json
import pandas as pd
import numpy as np
import traceback
import openpyxl

def xml_to_dataframe(path):
    # Reading xml file and converting to dictionary
    with open(path, 'r', encoding='utf-8') as file:
        xml_data = file.read()
    xml_dict = xmltodict.parse(xml_data)

    # converting dictionary to json for viewing purpose
    xml_json = json.dumps(xml_dict)
    # print(xml_json)

    # Obtaining test cases
    xml_dict_tests = xml_dict['testReport']['components']['component']['testTool']['testRuns']['testRun']
    xml_dict_tests_cases_conditions = xml_dict_tests['test']

    # Creating empty dataframe for output
    df_data = pd.DataFrame()
    df_data['test_name'] = np.nan
    df_data['test_result'] = np.nan
    df_data['assertion_name'] = np.nan
    df_data['assertion_id']= np.nan
    df_data['assertion_comment'] = np.nan
    df_data['assertion_result'] = np.nan
    df_data['comment'] = np.nan

    # For comparision and check
    lt=[]
    dty={'a':'cg'}
    count=0

    #
    try:
        for test_data in xml_dict_tests_cases_conditions:
            # print(json.dumps(test_data))
            # print(count)
            if test_data['conditions']:
                # print(test_data)
                if type(test_data['conditions']['condition']) == type(lt):
                    for dt in test_data['conditions']['condition']:
                        # print(type(dt['checks']['check']))
                        # print(json.dumps(dt))
                        # print('here')
                        if dt['checks']:
                            if type(dt['checks']['check']) == type(dty):
                                # print(json.dumps(dt))
                                # print('out')
                                dict_check = {}
                                dict_check['assertion_name'] = dt['@conditionID']
                                dict_check['test_name'] = test_data['@tcID'] + " " + test_data['title']
                                dict_check['test_result'] = test_data['score']['@value']
                                dict_check['assertion_id'] = dt['checks']['check']['@checkID']
                                # print(dt)
                                # print(dt['checks']['check']['score'])
                                # print(dict_check['assertion_name'])
                                dict_check['assertion_comment'] = dt['checks']['check']['comment']
                                dict_check['assertion_result'] = dt['checks']['check']['score']['@value']
                                if not dict_check['assertion_comment']:
                                    dict_check['assertion_comment'] = 'No comment'

                                df_check = pd.DataFrame(dict_check, index=[0])
                                df_check['assertion_comment'].replace(np.nan, 'No comment')
                                df_data = pd.concat([df_data, df_check], axis=0)
                            # elif type(dt['checks']['check']) == type(lt):
                            else:
                                for check in dt['checks']['check']:
                                    dict_check = {}
                                    dict_check['assertion_name'] = dt['@conditionID']
                                    dict_check['test_name'] = test_data['@tcID'] + " " + test_data['title']
                                    dict_check['test_result'] = test_data['score']['@value']
                                    dict_check['assertion_id'] = check['@checkID']
                                    dict_check['assertion_comment'] = check['comment']
                                    # print(dict_check['assertion_name'])
                                    if not dict_check['assertion_comment']:
                                        dict_check['assertion_comment'] = 'No comment'
                                    dict_check['assertion_result'] = check['score']['@value']
                                    df_check=pd.DataFrame(dict_check, index=[0])
                                    df_data = pd.concat([df_data, df_check], axis=0)
                        else:
                            dict_check = {}
                            dict_check['assertion_name'] = dt['@conditionID']
                            dict_check['test_name'] = test_data['@tcID'] + " " + test_data['title']
                            dict_check['test_result'] = test_data['score']['@value']
                            dict_check['assertion_id'] = 'No Checks'
                            dict_check['assertion_comment'] = 'No Comment'
                            dict_check['assertion_result'] = dt['score']['@value']
                            df_check = pd.DataFrame(dict_check, index=[0])
                            df_data = pd.concat([df_data, df_check], axis=0)
                elif test_data['conditions']['condition'] and '@conditionID' in test_data['conditions']['condition']:

                    if test_data['conditions']['condition']['checks']:
                        for check in test_data['conditions']['condition']['checks']['check']:
                            dict_check = {}
                            dict_check['assertion_name'] = test_data['conditions']['condition']['@conditionID']
                            dict_check['test_name'] = test_data['@tcID'] + " " + test_data['title']
                            dict_check['test_result'] = test_data['score']['@value']
                            dict_check['assertion_id'] = check['@checkID']
                            dict_check['assertion_comment'] = check['comment']
                            # print(dict_check['assertion_name'])
                            if not dict_check['assertion_comment']:
                                dict_check['assertion_comment'] = 'No comment'
                            dict_check['assertion_result'] = test_data['conditions']['condition']['score']['@value']
                            df_check = pd.DataFrame(dict_check, index=[0])
                            df_check['assertion_comment'].replace(np.nan, 'No comment')
                            df_data = pd.concat([df_data, df_check], axis=0)
                    else:
                        dict_check = {}
                        dict_check['assertion_name'] = test_data['conditions']['condition']['@conditionID']
                        dict_check['test_name'] = test_data['@tcID'] + " " + test_data['title']
                        dict_check['test_result'] = test_data['score']['@value']
                        dict_check['assertion_result'] = test_data['conditions']['condition']['score']['@value']
                        dict_check['assertion_id'] = 'No Checks'
                        dict_check['assertion_comment'] = 'No comment'
                        df_check = pd.DataFrame(dict_check, index=[0])
                        df_check['assertion_comment'].replace(np.nan, 'No comment')
                        df_data = pd.concat([df_data, df_check], axis=0)
            else:
                dict_check = {}
                # dict_check['assertion_name'] = dt['@conditionID']
                dict_check['test_name'] = test_data['@tcID'] + " " + test_data['title']
                dict_check['test_result'] = test_data['score']['@value']
                df_check = pd.DataFrame(dict_check, index=[0])
                # df_check['assertion_comment'].replace(np.nan, 'No comment')
                df_data = pd.concat([df_data, df_check], axis=0)
            count=count+1

    except Exception as e:
        # df_test = pd.DataFrame.from_dict(df_data)
        # print(df_test)
        # print(e)
        traceback.print_exc()
        return df_data.replace(np.nan, 'no data')
        # .to_csv('chec.csv', index=False)
    return df_data.replace(np.nan,'no data')
# dict_data['test_name'] = xml_dict_tests_cases['@tcID'] + xml_dict_tests_cases['title']
# dict_data['test_result'] = xml_dict_tests_cases['score']['@value']
# dict_data[]
# df_test = pd.DataFrame.from_dict(df_data)
# print(df_test)

df_au = xml_to_dataframe('GRLReport_golden.xml')
df_gen = xml_to_dataframe('GRLReport.xml')

df_au['check'] = df_au['test_name'] + df_au['assertion_name'] + df_au['assertion_id']
df_gen['check'] = df_gen['test_name'] + df_gen['assertion_name'] + df_gen['assertion_id']

gen_assertion_test_result = df_gen['test_result'].to_list()
gen_assertion_comment_list = df_gen['assertion_comment'].to_list()
gen_assertion_result_list = df_gen['assertion_result'].to_list()

gen_test_result_dict = {name:df_gen.iloc[df_gen['check'].to_list().index(name)] ['test_result'] for name in df_gen['check'].to_list()}
gen_assertion_result_dict = {name:df_gen.iloc[df_gen['check'].to_list().index(name)] ['assertion_result'].strip() for name in df_gen['check'].to_list()}
gen_assertion_comment_dict = {name:df_gen.iloc[df_gen['check'].to_list().index(name)] ['assertion_comment'].strip() for name in df_gen['check'].to_list()}
# print(gen_test_result_dict)

test_name_list_au = df_au['test_name'].to_list()

data_comp_dict={
    '           test_name':df_au['test_name'].to_list(),
                'golden_report_test_result':df_au['test_result'].to_list(),
                'generated_report_test_result': np.nan,
                'assertion_name':df_au['assertion_name'].to_list(),
                'assertion_id':df_au['assertion_id'].to_list(),
                'golden_report_assertion_comment':df_au['assertion_comment'].to_list(),
                'generated_report_assertion_comment':np.nan,
                'golden_report_assertion_result':df_au['assertion_result'].to_list(),
                'generated_report_assertion_result': np.nan,
                'compared_result': np.nan,
                'check':df_au['check'].to_list() }

# Creating empty dataframe for output
df_data_comp = pd.DataFrame(data_comp_dict)
# print(df_data_comp)

# df_data_comp['test_name'] = df_au['test_name']
# df_data_comp['golden_report_test_result'] = df_au['test_result']
# df_data_comp['generated_report_test_result'] = np.nan
# df_data_comp['assertion_name'] = df_au['assertion_name']
# df_data_comp['assertion_id']= df_au['assertion_id']
# df_data_comp['golden_report_assertion_comment'] = df_au['assertion_comment']
# df_data_comp['generated_report_assertion_comment'] = np.nan
# df_data_comp['golden_report_assertion_result'] = df_au['assertion_result']
# df_data_comp['generated_report_assertion_result'] = np.nan
# df_data_comp['compared_result'] = np.nan
# df_data_comp['comment'] = np.nan
# df_data_comp['check'] = df_au['check']

test_list = df_data_comp['check'].to_list()
gen_test_list = df_gen['check'].to_list()


for name in test_list:
    try:
        if name in gen_test_list:

            df_data_comp.at[test_list.index(name), 'generated_report_test_result'] = gen_test_result_dict[name]

            df_data_comp.at[test_list.index(name),'generated_report_assertion_result'] = gen_assertion_result_dict[name]
            df_data_comp.at[test_list.index(name), 'generated_report_assertion_comment'] = gen_assertion_comment_dict[name]
            if df_data_comp.iloc[test_list.index(name)]['generated_report_test_result'] == df_data_comp.iloc[test_list.index(name)]['golden_report_test_result']:
                df_data_comp.at[test_list.index(name),'compared_result'] = 'pass'
                df_data_comp.at[test_list.index(name), 'comment'] = 'success'
            else:
                df_data_comp.at[test_list.index(name), 'compared_result'] = 'fail'
                df_data_comp.at[test_list.index(name),'comment'] = 'fail'
        else:
            df_data_comp.at[test_list.index(name),'comment'] = 'test not executed'
    except Exception as e:
        pass
        print(e)

# print(df_data_comp['generated_report_test_result'])
print(df_data_comp['generated_report_test_result'])
df_data_comp.drop('check', axis=1, inplace=True)
df_data_comp['generated_report_test_result'].fillna('NA', inplace=True)
df_data_comp['compared_result'].fillna('NA', inplace=True)
df_data_comp.fillna('no comment', inplace=True)
def color_rule(val):
    return ['background-color: red' if x =='fail' else 'background-color: green' for x in val]

df_data_comp = df_data_comp.style.apply(color_rule, axis=1, subset=['compared_result'])

# print(df_data_comp['generated_report_test_result'])
df_data_comp.to_excel('styled.xlsx', engine='openpyxl')











