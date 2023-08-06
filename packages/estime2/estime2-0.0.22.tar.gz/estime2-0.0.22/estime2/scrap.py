
# from config import (
#     get_option
# )
# from provpoptable import (
#     ProvPopTable,
#     calculate_ages_to_modify_and_counter
# )
from estime2 import (
    Age,
    get_option,
    options,
    set_option
)
from estime2.poptable import (
    calculate_ages_to_modify_and_counter,
    calculate_absorbable_in_other_comp,
    calculate_counter_adjustable_in_comp,
    calculate_modifiable_in_comp,
    get_J,
    get_L,
    get_other_comp
)
from estime2.subpoptables import (
    apply_L,
    ProvPopTable,
    SubProvPopTable
)
from estime2.aggregatepoptables import (
    AggregateProvPopTable,
    AggregateSubProvPopTable,
    apply_Ns,
    calculate_ages_to_transfer,
    calculate_agg_rem,
    calculate_signs,
    get_Ms,
    get_Ns,
    sort_tbl_index
)
from functools import reduce
from pprint import pprint
import estime2
import numpy as np
import os
import pandas as pd
pd.options.display.min_rows = 22

RegionSAD = ['RegionCode', 'Sex', 'Age', 'RefDate']
RegionSA = RegionSAD[0:3]
RegionSD = list(np.array(RegionSAD)[[0,1,3]])
RegionS = RegionSA[0:2]

def arrange_by_lvl(df, levels, value_name):
    age_cols = [col for col in df if col.startswith('A_')]
    result =\
        pd.melt(
            df[levels + age_cols],
            id_vars = levels,
            value_vars = age_cols,
            var_name = 'Age',
            value_name = value_name
        )\
        .assign(
            Age = lambda df: \
                df.Age.apply(lambda x: int(x[(x.index('A_') + 2):]))
        )
    return result

def find_tbl_path():
    listed_files = [x for x in os.listdir('..') if 'minus' in x]
    return listed_files

def call_tbl(use_copy: bool = False):
    tbl_names = find_tbl_path()
    tbl_name =  tbl_names[0] if use_copy else tbl_names[-1]
    tbl = pd.read_excel('../' + tbl_name, sheet_name = 1)
    poptbl = ProvPopTable(tbl)
    return poptbl

def call_tbl2():
    tbl_name = "10_DR_2001-02.xlsx"

    with pd.ExcelFile('../' + tbl_name) as tbl:
        pop_2001 = pd.read_excel(tbl, sheet_name = 0)
        bth = pd.read_excel(tbl, sheet_name = 1)
        dth_d01 = pd.read_excel(tbl, sheet_name = 2)
        dth_d02 = pd.read_excel(tbl, sheet_name = 3)
        imm = pd.read_excel(tbl, sheet_name = 4)
        emi = pd.read_excel(tbl, sheet_name = 5)
        rem = pd.read_excel(tbl, sheet_name = 6)
        nte = pd.read_excel(tbl, sheet_name = 7)
        mip = pd.read_excel(tbl, sheet_name = 8)
        mit = pd.read_excel(tbl, sheet_name = 9)
        npr = pd.read_excel(tbl, sheet_name = 10)
        pop_2002_orig = pd.read_excel(tbl, sheet_name = 11, skiprows = 2)
        pop_2002_corrected = pd.read_excel(tbl, sheet_name = 12)

    return {
        'pop_2001': pop_2001, 
        'bth': bth,
        'dth_d01': dth_d01,
        'dth_d02': dth_d02,
        'imm': imm,
        'emi': emi,
        'rem': rem,
        'nte': nte,
        'mip': mip,
        'mit': mit,
        'npr': npr,
        'pop_2002_orig': pop_2002_orig,
        'pop_2002_corrected': pop_2002_corrected
    }

def call_tbls():
    tbl_names = find_tbl_path()
    result = []
    for tbl_name in tbl_names:
        print(tbl_name)
        tbl = pd.read_excel('../' + tbl_name, sheet_name = 1)
        result.append(ProvPopTable(tbl))
    return result

def run0(use_copy: bool = False):
    poptbl = call_tbl(use_copy)
    
    return poptbl.fix_issues(return_all_mods = True)

def run():
    poptbl = call_tbl()

    pop_age = 'Age'
    pop_end = 'Postcensal Population'
    comp = 'DTH'

    # Get basic options
    comp_neg = poptbl.get_comp_neg()
    comp_pos = poptbl.get_comp_pos()
    comps = comp_neg + comp_pos
    at_least = get_option('pop.at_least')
    pop_groups = ['Sex', 'Age']
    cols_required = pop_groups.copy()
    cols_required.append(comp)

    # Get properties of the youngest problematic record
    I = poptbl.get_I()
    I = I.query('I != 0').sort_values(pop_groups)
    problematic = I.iloc[0, :]
    problematic_sex = problematic['Sex']
    problematic_age = problematic['Age']
    problematic_val = problematic['I']
    calculated_pop = poptbl.calculate_pop()
    comp_in_neg = comp in comp_neg
    comp_in_comp_end = False
    age_is_max = problematic_age.is_max()
    
    # Get the corresponding age(s) of comp to modify & counter-adjust
    ages = calculate_ages_to_modify_and_counter(
        problematic_age,
        comp_in_comp_end
    )    
    to_modify_age = ages['age.to_modify']
    to_counter_age = ages['age.to_counter']

    # Get the maximum amounts modifiable & counter-adjustable
    correctable_in_comp = poptbl\
        .loc[lambda df: df['Sex'] == problematic_sex]\
        [cols_required]
    correctable_in_pop_end = calculated_pop.copy()\
        .loc[lambda df: df['Sex'] == problematic_sex]

    df_comp = correctable_in_comp.copy()
    df_pop_end = correctable_in_pop_end.copy()

    # calculate_modifiable_in_comp
    pop_end_query = None
    if age_is_max:
        pop_end_query = "{0} > {1}".format(pop_age, get_option('age.max'))
    else:
        pop_end_query = "{0} == {1}".format(pop_age, problematic_age)
    df_pop_end_problematic = df_pop_end.query(pop_end_query)
    df_comp_modifiable = None
    if isinstance(to_modify_age, int):
        df_comp_modifiable = df_comp\
            .loc[lambda df: df[pop_age] == to_modify_age]
    elif isinstance(to_modify_age, list):
        df_comp_modifiable = df_comp\
            .loc[lambda df: df[pop_age] <= to_modify_age[1]]\
            .loc[lambda df: df[pop_age] >= to_modify_age[0]]
    else:
        raise NotImplementedError

    # print('Problematic record:')
    # print(df_pop_end_problematic)
    # print('')
    # print('Component value to modify:')
    # print(df_comp_modifiable)

    modifiable_val_in_pop_end = df_pop_end_problematic[pop_end].values[0]
    abs_modifiable_val_in_pop_end = abs(modifiable_val_in_pop_end)
    modifiable = None
    if isinstance(to_modify_age, int):
        modifiable_val_in_comp = df_comp_modifiable[comp].values[0]
        if comp_in_neg:
            modifiable = min(
                abs_modifiable_val_in_pop_end,
                modifiable_val_in_comp
            )
        else:
            modifiable = abs_modifiable_val_in_pop_end
    elif isinstance(to_modify_age, list):
        modifiable_val_in_comp = df_comp_modifiable[comp]
        modifiable_val_in_comp_0 = modifiable_val_in_comp.values[0]
        modifiable_val_in_comp_1 = modifiable_val_in_comp.values[1]
        modifiable_0 = None
        modifiable_1 = None
        if comp_in_neg:
            modifiable_1 = min(
                abs_modifiable_val_in_pop_end, 
                modifiable_val_in_comp_1
            )
            modifiable_0 = None
            leftover = None
            if modifiable_1 == abs_modifiable_val_in_pop_end:
                modifiable_0 = 0
            else:
                leftover = abs_modifiable_val_in_pop_end -\
                    modifiable_val_in_comp_1
                modifiable_0 = min(leftover, modifiable_val_in_comp_0)
        else:
            modifiable_0 = abs_modifiable_val_in_pop_end // 2
            modifiable_1 = abs_modifiable_val_in_pop_end - modifiable_0
        modifiable = [modifiable_0, modifiable_1]
    else:
        raise NotImplementedError
    
    df_comp_modifiable["{0}_J".format(comp)] = modifiable
    del df_comp_modifiable[comp]

    # print('Component value modifiable:')
    # print(df_comp_modifiable)

    # calculate_counter_adjustable_in_comp
    modifiable_in_comp = df_comp_modifiable.copy()
    to_counter_age_min = to_counter_age[0]
    to_counter_age_max = to_counter_age[1]

    df_comp_counter_adjust = df_comp\
        .loc[lambda df: df[pop_age] >= to_counter_age_min]\
        .loc[lambda df: df[pop_age] <= to_counter_age_max]
    if comp_in_comp_end:
        df_pop_end_compare = df_pop_end\
            .loc[lambda df: df[pop_age] >= to_counter_age_min]\
            .loc[lambda df: df[pop_age] <= to_counter_age_max]
    else:
        df_pop_end_compare = df_pop_end\
            .loc[lambda df: df[pop_age] >= to_counter_age_min + 1]\
            .loc[lambda df: df[pop_age] <= to_counter_age_max + 1]
    df_pop_end_compare[pop_end] -= at_least

    pop_end_values = df_pop_end_compare[pop_end].values
    comp_values = df_comp_counter_adjust[comp].values
    counter_adjustable = []
    to_append = None

    for val in zip(pop_end_values, comp_values):
        if val[0] <= 0:
            to_append = 0
        elif comp_in_neg:
            to_append = val[0]
        else:
            to_append = val[1]
        counter_adjustable.append(to_append)

    df_comp_counter_adjust["{0}_J".format(comp)] = counter_adjustable
    del df_comp_counter_adjust[comp]

    # print("Component values counter-adjustable:")
    # print(df_comp_counter_adjust)
    df_comp_counter_adjust_reversed = df_comp_counter_adjust\
        .sort_values(pop_groups, ascending = [True, False])

    comp_J = "{0}_J".format(comp)
    comp_K = "{0}_K".format(comp)
    to_modify_val_total = df_comp_modifiable[comp_J].sum()
    # print('Total value to be modified:')
    # print(to_modify_val_total)

    result = []
    method = get_option('method')
    # print('Counter-adjustable records:')
    if method == '1dist':
        for index, row in df_comp_counter_adjust_reversed.iterrows():
            if row[comp_J] > 0 and to_modify_val_total != 0:
                result.append(1)
                to_modify_val_total -= 1
            else:
                result.append(0)
    else: # i.e. prop
        for index, row in df_comp_counter_adjust_reversed.iterrows():
            if row[comp_J] > 0 and to_modify_val_total != 0:
                min_comp_J_val = min(row[comp_J], to_modify_val_total)
                result.append(min_comp_J_val)
                to_modify_val_total -= min_comp_J_val
            else:
                result.append(0)

    df_comp_counter_adjust_reversed[comp_K] = result
    del df_comp_counter_adjust_reversed[comp_J]
    df_comp_counter_adjust_reversed\
        .sort_values(
            pop_groups, 
            ascending = [True, True], 
            inplace = True
        )

    comp_L = '{0}_L'.format(comp)
    J = df_comp_modifiable
    K = df_comp_counter_adjust_reversed

    if comp_in_neg:
        J[comp_L] = -J[comp_J]
        del J[comp_J]
        K[comp_L] = K[comp_K]
        del K[comp_K]
    else: # i.e. comp is positive
        J[comp_L] = J[comp_J]
        del J[comp_J]
        K[comp_L] = -K[comp_K]
        del K[comp_K]

    L = K.append(J, ignore_index = True)

    self_copy = poptbl.copy()
    self_copy = self_copy.merge(L, on = pop_groups, how = 'left')
    self_copy.fillna(0, inplace = True)
    self_copy[comp_L] = self_copy[comp_L].apply(int)
    self_copy[comp] += self_copy[comp_L]
    del self_copy[comp_L]

    self_copy = ProvPopTable(
        self_copy,
        pop_sex = 'Sex', # self.__pop_sex,
        pop_age = 'Age', # self.__pop_age,
        pop_end = 'Postcensal Population', # self.__pop_end,
        pop_start = 'Initial Population', # self.__pop_start,
        pop_birth = 'BTH', # self.__pop_birth,
        comp_neg_temp_out = get_option('comp_neg.temp_out'), # self.__comp_neg_temp_out,
        comp_neg_emi = get_option('comp_neg.emi'),
        comp_neg_npr_out = get_option('comp_neg.npr_out'),
        comp_neg_death = get_option('comp_neg.death'),
        comp_neg_interprov_out = get_option('comp_neg.interprov_out'),
        comp_pos_temp_in = get_option('comp_pos.temp_in'),
        comp_pos_ret_emi = get_option('comp_pos.ret_emi'),
        comp_pos_npr_in = get_option('comp_pos.npr_in'),
        comp_pos_immi = get_option('comp_pos.immi'),
        comp_pos_interprov_in = get_option('comp_pos.interprov_in'),
        comp_end = get_option('comp.end'),
        reorder_cols = False,
        show_pop_end = pop_end in poptbl.columns.tolist(), # self.columns.tolist(),
        flag = False        
    )

    print("self:")
    print(poptbl)
    print("self.calculate_pop():")
    self_calculate_pop = poptbl.calculate_pop()
    print(self_calculate_pop)
    print("Total end-of-period pop of self:")
    print(self_calculate_pop[pop_end].sum())
    print("self_copy after applying comp_L:")
    print(self_copy)
    print("self_copy.calculate_pop():")
    self_copy_calculate_pop = self_copy.calculate_pop()
    print(self_copy_calculate_pop)
    print("self_copy.get_I():")
    print(all(self_copy.get_I()['I'].values == 0))
    print("Total end-of-period pop of self_copy:")
    print(self_copy_calculate_pop[pop_end].sum())

    print('poptbl.fix_issues():')
    result = poptbl.fix_issues()
    print(result.calculate_pop())

    # test = Age('99+')
    # print(str(test)[-1] == '+')
    # print(Age(102).get_showing_age())

    # pop_groups = ['Sex', 'Age']
    # pop_end = 'Postcensal Population'
    # pop_start = 'Initial Population'
    # pop_birth = 'BTH'
    # comp_neg = ['TEM', 'EMI', 'NPR, 2018-07-01', 'DTH', 'IOM']
    # comp_pos = ['RE', 'NPR, 2019-07-01' ,'IMM', 'IIM']
    # comps = comp_neg + comp_pos
    # comp_end = ['NPR, 2019-07-01']
    # comp_not_end = []
    # for comp in comps:
    #     if comp not in comp_end:
    #         comp_not_end.append(comp)
    # comp_aggs = {}
    # comp_aggs[pop_start] = 'sum'
    # comp_aggs[pop_birth] = 'sum'
    # for comp2 in comp_not_end:
    #     comp_aggs[comp2] = 'sum'

    # result1 = poptbl.loc[
    #     :, 
    #     pop_groups + [pop_start, pop_birth] + comp_not_end
    # ]
    # result1['Age'] += 1
    # result1 = result1\
    #     .groupby(pop_groups)\
    #     .agg(comp_aggs)\
    #     .reset_index()

    # result2 = poptbl.loc[:, pop_groups + comp_end]
    # result2 = result2.loc[lambda df: df['Age'] != -1]

    # result3 = result1\
    #     .merge(
    #         result2, 
    #         how = 'left', 
    #         on = ['Sex', 'Age']
    #     )
    
    # result3[pop_end] = result3[pop_start] + result3[pop_birth]
    # if comp_neg != []:
    #     for col_neg in comp_neg:
    #         result3[pop_end] -= result3[col_neg]
    # if comp_pos != []:
    #     for col_pos in comp_pos:
    #         result3[pop_end] += result3[col_pos]

    # result = result3.loc[:, pop_groups + [pop_end]]

    # pop_end =\
    #     poptbl['Initial Population'] + poptbl['BTH']\
    #         - poptbl['TEM'] - poptbl['EMI'] - poptbl['NPR, 2018-07-01']\
    #         - poptbl['DTH'] - poptbl['IOM'] - poptbl['RAO']\
    #         + poptbl['RE'] + poptbl['NPR, 2019-07-01'] + poptbl['IMM']\
    #         + poptbl['IIM'] + poptbl['RAI']
    # pop_grp = poptbl.loc[:, ['Sex', 'Age']]
    # pop_grp['Age'] += 1
    # pop_grp['End-of-period population'] = pop_end
    # result = poptbl\
    #     .groupby(['Sex', 'Age'])\
    #     .agg({
    #         'Initial Population': 'sum',
    #         'BTH': 'sum',
    #         'TEM': 'sum',
    #         'EMI': 'sum',
    #         'NPR, 2018-07-01': 'sum',
    #         'DTH': 'sum',
    #         'IOM': 'sum',
    #         'RAO': 'sum',
    #         'RE': 'sum',
    #         'NPR, 2019-07-01': 'sum',
    #         'IMM': 'sum',
    #         'IIM': 'sum',
    #         'RAI': 'sum'
    #     })\
    #     .reset_index()
    # print(pop_grp)
    # print(result)
    # print(poptbl.calculate_pop())
    # print(poptbl.loc[lambda df: df['Age'] >= '99+'])
    # template =\
    #     '* `{arg_name}`: (`None` by default) a str; the name of ' +\
    #     'the column corresponding to "{real_name}" in the ' +\
    #     'population table. If `None`, it first checks whether the ' +\
    #     'global option value `{glob_name}` is also `None`. If it ' +\
    #     'is also `None`, the "{real_name}" component is ' +\
    #     'discarded from the population table (i.e. not shown and not ' +\
    #     'used). If it is not `None`, the method then checks whether the ' +\
    #     'value `{glob_name}` is one of the column names in the ' +\
    #     'population table. If it is, the column having the same name as ' +\
    #     '`{glob_name}` is selected as the ' +\
    #     '"{real_name}" column. If not, the method raises ' +\
    #     '`AssertionError`.'
    # print(
    #     template.format(
    #         arg_name = 'comp_pos_npr_in',
    #         real_name = 'Non-permanent residents IN',
    #         glob_name = 'comp_pos.npr_in'
    #     )
    # )
    # print(
    #     template.format(
    #         arg_name = 'comp_pos_immi',
    #         real_name = 'Immigrants',
    #         glob_name = 'comp_pos.immi'
    #     )
    # )
    # print(
    #     template.format(
    #         arg_name = 'comp_pos_interprov_in',
    #         real_name = 'Interprovincial migrant IN',
    #         glob_name = 'comp_pos.interprov_in'
    #     )
    # )

def run2():

    method = get_option('method')

    self = call_tbl()

    comp_neg_to_use = self.get_comp_neg()
    comp_pos_to_use = self.get_comp_pos()
    comp_neg_to_use.remove(get_option('comp_neg.interprov_out'))
    comp_pos_to_use.remove(get_option('comp_pos.interprov_in'))
    comps = comp_neg_to_use + comp_pos_to_use

    pop_groups = [get_option('pop.sex'), get_option('pop.age')]
    all_cols = self.columns.tolist()
    show_pop_end = get_option('pop.end') in all_cols
    self_copy = self.copy()

    not_fixed = True
    i = 0
    while not_fixed:
        comp = comps[i]; print(comp)
        i += 1

        comp_L = '{0}_L'.format(comp)
        if i == 1:
            self_copy = ProvPopTable(
                self_copy,
                pop_sex = 'Sex', 
                pop_age = 'Age',
                pop_end = 'Postcensal Population',
                pop_start = 'Initial Population',
                pop_birth = 'BTH',
                comp_neg_temp_out = get_option('comp_neg.temp_out'),
                comp_neg_emi = get_option('comp_neg.emi'),
                comp_neg_npr_out = get_option('comp_neg.npr_out'),
                comp_neg_death = get_option('comp_neg.death'),
                comp_neg_interprov_out = get_option('comp_neg.interprov_out'),
                comp_pos_temp_in = get_option('comp_pos.temp_in'),
                comp_pos_ret_emi = get_option('comp_pos.ret_emi'),
                comp_pos_npr_in = get_option('comp_pos.npr_in'),
                comp_pos_immi = get_option('comp_pos.immi'),
                comp_pos_interprov_in = get_option('comp_pos.interprov_in'),
                comp_end = get_option('comp.end'),
                reorder_cols = False,
                show_pop_end = show_pop_end,
                flag = False  
            )
        L = self_copy.get_L(comp, method); 
        L['Age'] = L['Age'].apply(str); print(L)
        self_copy['Age'] = self_copy['Age'].apply(str)
        self_copy = self_copy.merge(L, on = pop_groups, how = 'left')
        self_copy.fillna(0, inplace = True)
        self_copy[comp_L] = self_copy[comp_L].apply(int)

        print('Before adding:')
        print(self_copy)
        
        self_copy[comp] += self_copy[comp_L]

        print('After adding, before deleting comp_L:')
        print(self_copy)
        
        del self_copy[comp_L]

        print('After adding, after deleting comp_L:')
        print(self_copy)

        self_copy = ProvPopTable(
            self_copy,
            pop_sex = 'Sex', 
            pop_age = 'Age',
            pop_end = 'Postcensal Population',
            pop_start = 'Initial Population',
            pop_birth = 'BTH',
            comp_neg_temp_out = get_option('comp_neg.temp_out'),
            comp_neg_emi = get_option('comp_neg.emi'),
            comp_neg_npr_out = get_option('comp_neg.npr_out'),
            comp_neg_death = get_option('comp_neg.death'),
            comp_neg_interprov_out = get_option('comp_neg.interprov_out'),
            comp_pos_temp_in = get_option('comp_pos.temp_in'),
            comp_pos_ret_emi = get_option('comp_pos.ret_emi'),
            comp_pos_npr_in = get_option('comp_pos.npr_in'),
            comp_pos_immi = get_option('comp_pos.immi'),
            comp_pos_interprov_in = get_option('comp_pos.interprov_in'),
            comp_end = get_option('comp.end'),
            reorder_cols = False,
            show_pop_end = show_pop_end,
            flag = False  
        )

        not_fixed = not (all(self_copy.get_I()['I'].values == 0) or i == len(comps))


    print(self_copy)

def run3():
    poptbl = call_tbl()
    print(poptbl)
    print(poptbl.calculate_pop())

    result = poptbl.fix_issues(return_all_mods = True)

    pprint(result)
    try:
        print(result.calculate_pop())
    except:
        print(result[0].calculate_pop())
    
    return result

def run4():

    self = call_tbl()
    comp = 'DTH'
    comp_in_comp_end = False
    method = '1dist'
    pop_sex = 'Sex'
    pop_age = 'Age'
    pop_end = 'Postcensal Population'
    problematic_sex = 1

    pop_groups = self.get_pop_groups()
    comp_J = f"{comp}_J"
    dfs_comp = self.get_J(comp)
    df_comp_modifiable = dfs_comp['records.to_modify']
    df_comp_counter_adjust = dfs_comp['records.to_counter']
    df_comp_counter_adjust_reversed = df_comp_counter_adjust\
        .sort_values(pop_groups, ascending = [True, False])
    to_modify_val_total = df_comp_modifiable[comp_J].sum()

    print("df_comp_modifiable:")
    print(df_comp_modifiable)
    print("df_comp_counter_adjust_reversed:")
    print(df_comp_counter_adjust_reversed)

    comp_K = f"{comp}_K"
    result = []
    max_correctables =\
        df_comp_counter_adjust_reversed.iloc[:, -1].values.copy()

    if method == '1dist':
        apply_sequentially = get_option('method_use.seq')
        use_2nd_pass = get_option('method_use.second_pass')
        if apply_sequentially:
            seq_size = get_option('age.prop_size')
            len_mc = len(max_correctables)
            for i in np.arange(len_mc, step = seq_size):
                period = [i, min(i + seq_size, len_mc)]
                mc_seq = max_correctables[period[0]:period[1]]
                print(mc_seq)
                for num in mc_seq:
                    if num > 0 and to_modify_val_total != 0:
                        result.append(1)
                        to_modify_val_total -= 1
                    else:
                        result.append(0)
                if to_modify_val_total != 0 and use_2nd_pass:
                    mc_seq -= np.array(result[period[0]:period[1]])
                    for j, num2 in enumerate(mc_seq):
                        if num2 > 0 and to_modify_val_total != 0:
                            result[j + i] += 1
                            to_modify_val_total -= 1
        else:
            for index, row in df_comp_counter_adjust_reversed.iterrows():
                if row[comp_J] > 0 and to_modify_val_total != 0:
                    result.append(1)
                    to_modify_val_total -= 1
                else:
                    result.append(0)
            print("result so far:")
            print(result)
            if to_modify_val_total != 0 and use_2nd_pass:
                # The first pass wasn't enough so that to_modify_val_total
                # didn't come down to 0.
                # Apply the second pass only if the option says so
                print("The second pass has started.")
                max_correctables -= np.array(result)
                print("df_comp_counter_adjust_reversed:")
                print(df_comp_counter_adjust_reversed)
                print("New max_correctables:")
                print(max_correctables)
                for i, item in enumerate(max_correctables):
                    if item > 0 and to_modify_val_total != 0:
                        result[i] += 1
                        to_modify_val_total -= 1
                    print("to_modify_val_total:")
                    print(to_modify_val_total)
                    print("result:")
                    print(result)

    elif method == 'filler':
        for index, row in df_comp_counter_adjust_reversed.iterrows():
            if row[comp_J] > 0 and to_modify_val_total != 0:
                min_comp_J_val = min(row[comp_J], to_modify_val_total)
                result.append(min_comp_J_val)
                to_modify_val_total -= min_comp_J_val
            else:
                result.append(0)
    else: # proportional method
        problematic_sex = df_comp_modifiable[pop_sex].values[0]
        prop_max_age = df_comp_counter_adjust_reversed\
            .iloc[0, :]\
            [pop_age]
        prop_min_age = df_comp_counter_adjust_reversed\
            .iloc[-1, :]\
            [pop_age]
        if not comp_in_comp_end:
            prop_max_age += 1
            prop_min_age += 1
        calculated_pop = self.calculate_pop()
        pop_end_to_compare_reversed = calculated_pop.copy()\
            .loc[lambda df: df[pop_sex] == problematic_sex]\
            .loc[lambda df: df[pop_age] <= prop_max_age]\
            .loc[lambda df: df[pop_age] >= prop_min_age]\
            .sort_values(pop_groups, ascending = [True, False])
        print("pop_end_to_compare_reversed:")
        print(pop_end_to_compare_reversed)

        prop_size = get_option('age.prop_size')
        pop_end_for_prop =\
            pop_end_to_compare_reversed.iloc[:, -1].values
        if comp_in_comp_end:
            pop_end_for_prop[0] = 0
        
        print("pop_end_for_prop:")
        print(pop_end_for_prop)
        print("max_correctables:")
        print(max_correctables)
        
        pop_end_len = len(pop_end_for_prop)
        for i in np.arange(pop_end_len, step = prop_size):
            period = [i, min(i + prop_size, pop_end_len)]
            props_numer = pop_end_for_prop[period[0]:period[1]]
            props_denom = sum(props_numer)
            props = props_numer / props_denom
            print("to_modify_val_total before:")
            print(to_modify_val_total)
            print("props:")
            print(props)
            props_x_m = np.array(
                list(map(int, np.round(to_modify_val_total * props)))
            )
            print("props_x_m:")
            print(props_x_m)
            max_correct_for_each =\
                max_correctables[period[0]:period[1]]
            print("max_correct_for_each:")
            print(max_correct_for_each)
            min_from_each = np.minimum(props_x_m, max_correct_for_each)
            print("min_from_each:")
            print(min_from_each)
            loc_max_prop = np.where(props == max(props))[0][0]
            print("loc_max_prop:")
            print(loc_max_prop)
            sum_min_from_each = sum(min_from_each)
            to_modify_val_total -= sum_min_from_each
            print("to_modify_val_total after:")
            print(to_modify_val_total)
            if props_x_m[loc_max_prop] <= max_correct_for_each[loc_max_prop]:
                more_possible_correction =\
                    max_correct_for_each[loc_max_prop] -\
                    props_x_m[loc_max_prop]
                print("more_possible_correction:")
                print(more_possible_correction)
                min_mod_cor = min(
                    to_modify_val_total,
                    more_possible_correction
                )
                min_from_each[loc_max_prop] += min_mod_cor
                to_modify_val_total -= min_mod_cor
                print("min_from_each further:")
                print(min_from_each)
                print("to_modify_val_total after further:")
                print(to_modify_val_total)
                result.extend(min_from_each)
            else:
                result.extend(min_from_each)
            print("result:")
            print(result)
            print(len(result))
            print("")

    df_comp_counter_adjust_reversed[comp_K] = result
    del df_comp_counter_adjust_reversed[comp_J]
    df_comp_counter_adjust_reversed\
        .sort_values(
            pop_groups, 
            ascending = [True, True], 
            inplace = True
        )
    
    return df_comp_counter_adjust_reversed

def run5(sex = None):
    result = call_tbl2()

    pop_2001 = result['pop_2001']
    bth = result['bth']
    dth_d01 = result['dth_d01']
    dth_d02 = result['dth_d02']
    imm = result['imm']
    emi = result['emi']
    rem = result['rem']
    nte = result['nte']
    mip = result['mip']
    mit = result['mit']
    npr = result['npr']
    pop_2002_orig = result['pop_2002_orig']
    pop_2002_corrected = result['pop_2002_corrected']
    
    nprs = arrange_by_lvl(npr, RegionSD, 'NPR')
    tbl =\
        arrange_by_lvl(pop_2001, RegionS, 'InitialPopulation')\
        .merge(
            bth[RegionS + ['Total']]\
                .assign(Age = -1)\
                .rename(columns = {'Total': 'BTH'})\
                [RegionSA + ['BTH']],
            on = RegionSA,
            how = 'outer'
        )\
        .sort_values(RegionSA)\
        .fillna(0)\
        .assign(
            InitialPopulation = lambda df: df.InitialPopulation.apply(int),
            BTH = lambda df: df.BTH.apply(int)
        )\
        .rename(
            columns = {'InitialPopulation': 'POP_2001'}
        )\
        .merge(
            arrange_by_lvl(dth_d01, RegionS, 'DTH_D01'),
            on = RegionSA,
            how = 'inner'
        )\
        .merge(
            arrange_by_lvl(imm, RegionS, 'IMM'),
            on = RegionSA,
            how = 'inner'
        )\
        .merge(
            arrange_by_lvl(emi, RegionS, 'EMI'),
            on = RegionSA,
            how = 'inner'
        )\
        .merge(
            arrange_by_lvl(rem, RegionS, 'REM'),
            on = RegionSA,
            how = 'inner'
        )\
        .merge(
            arrange_by_lvl(nte, RegionS, 'NTE'),
            on = RegionSA,
            how = 'inner'
        )\
        .merge(
            arrange_by_lvl(mip, RegionS, 'MIP'),
            on = RegionSA,
            how = 'inner'
        )\
        .merge(
            arrange_by_lvl(mit, RegionS, 'MIT'),
            on = RegionSA,
            how = 'inner'
        )\
        .merge(
            nprs.loc[
                lambda df: df['RefDate'] < np.datetime64('2002-01-01')
            ]\
            [RegionSA + ['NPR']]\
            .rename(columns = {'NPR': 'NPR_out'}),
            on = RegionSA,
            how = 'outer'
        )\
        .merge(
            nprs.loc[
                lambda df: df['RefDate'] > np.datetime64('2002-01-01')
            ]\
            [RegionSA + ['NPR']]\
            .rename(columns = {'NPR': 'NPR_in'}),
            on = RegionSA,
            how = 'outer'
        )\
        .fillna(0)\
        .assign(
            NPR_out = lambda df: df.NPR_out.apply(int),
            NPR_in = lambda df: df.NPR_in.apply(int)
        )\
        .assign(
            MIP_out = lambda df: df.MIP.apply(lambda x: abs(min(x, 0))),
            MIP_in = lambda df: df.MIP.apply(lambda x: max(x, 0)),
            MIT_out = lambda df: df.MIT.apply(lambda x: abs(min(x, 0))),    
            MIT_in = lambda df: df.MIT.apply(lambda x: max(x, 0))
        )
    selected_cols = tbl.columns.tolist()
    selected_cols.remove('MIP')
    selected_cols.remove('MIT')
    tbl = tbl[selected_cols]
    
    all_RegionC = np.unique(tbl[RegionSAD[0]])
    poptbl_regions = {}
    for region in all_RegionC:
        tbl_region =\
            tbl\
            .query(f"{RegionSAD[0]} == {region}")\
            [selected_cols[1:]]
        if sex is not None:
            tbl_region = tbl_region.query(f"Sex == {sex}")
        with estime2.option_context(
            'pop.sex', 'Sex',
            'pop.age', 'Age',
            'pop.end', 'POP_2002',
            'pop.start', 'POP_2001',
            'pop.birth', 'BTH',
            'comp_neg.temp_out', 'NTE',
            'comp_neg.emi', 'EMI',
            'comp_neg.npr_out', 'NPR_out',
            'comp_neg.death', 'DTH_D01',
            'comp_neg.interprov_out', 'MIP_out',
            'comp_neg.intraprov_out', 'MIT_out',
            'comp_neg.etc', [],
            'comp_pos.ret_emi', 'REM',
            'comp_pos.npr_in', 'NPR_in',
            'comp_pos.immi', 'IMM',
            'comp_pos.interprov_in', 'MIP_in',
            'comp_pos.intraprov_in', 'MIT_in',
            'comp_pos.etc', [],
            'comp.end', ['NPR_in']
        ):
            poptbl_regions[region] = SubProvPopTable(tbl_region)
    
    return poptbl_regions

def run6():
    poptbl_regions = run5()
    poptbl_1001 = poptbl_regions[1001]
    poptbl_1010 = poptbl_regions[1010]
    estime2.options.method = '1dist'
    poptbl_1001_fixed_onedist =\
        poptbl_1001.fix_issues(return_all_mods = True)
    poptbl_1010_fixed_onedist =\
        poptbl_1010.fix_issues(return_all_mods = True)
    
    print(poptbl_1001_fixed_onedist.summary())
    print('')
    print(poptbl_1010_fixed_onedist.summary())
    print('')

    estime2.options.method = 'filler'
    poptbl_1001_fixed_filler =\
        poptbl_1001.fix_issues(return_all_mods = True)
    poptbl_1010_fixed_filler =\
        poptbl_1010.fix_issues(return_all_mods = True)
    
    print(poptbl_1001_fixed_filler.summary())
    print('')
    print(poptbl_1010_fixed_filler.summary())
    print('')

    estime2.options.method = 'prop'
    poptbl_1001_fixed_prop =\
        poptbl_1001.fix_issues(return_all_mods = True)
    poptbl_1010_fixed_prop =\
        poptbl_1010.fix_issues(return_all_mods = True)

    print(poptbl_1001_fixed_prop.summary())
    print('')
    print(poptbl_1010_fixed_prop.summary())
    print('')

def run7(comp = 'DTH'):

    poptbl = call_tbl()
        
    # Get basic options
    comp_neg = poptbl.get_comp_neg()
    comp_pos = poptbl.get_comp_pos()
    comps = comp_neg + comp_pos
    pop_groups = poptbl.get_pop_groups()
    pop_sex = pop_groups[0]
    pop_age = pop_groups[1]
    pop_end = poptbl.get_pop_end()
    cols_required = pop_groups.copy()
    cols_required.append(comp) 

    # Get properties of the youngest problematic record
    ## .sort_values() will be deprecated in later versions of pandas
    I = poptbl.get_I()
    I = I.query('I != 0').sort_values(pop_groups)
    problematic = I.iloc[0, :] # choose the youngest
    problematic_sex = problematic[pop_sex]
    problematic_age = problematic[pop_age]
    calculated_pop = poptbl.calculate_pop()
    comp_in_neg = comp in comp_neg # comp is in comp_pos otherwise
    comp_in_comp_end = comp in poptbl.get_comp_end()

    # Get the corresponding age(s) of comp to modify & counter-adjust
    ages = calculate_ages_to_modify_and_counter(
        problematic_age, 
        comp_in_comp_end
    )
    # to_modify_age = ages['age.to_modify']
    to_counter_age = ages['age.to_counter']

    # Get the maximum amounts modifiable & counter-adjustable
    correctable_in_pop_end = calculated_pop.copy()\
        .loc[lambda df: df[pop_sex] == problematic_sex]
    correctable_in_comp = poptbl\
        .loc[lambda df: df[pop_sex] == problematic_sex]\
        [cols_required]

    print("df_pop_end:")
    print(correctable_in_pop_end)
    print("df_comp:")
    print(correctable_in_comp)
    print("comp:")
    print(comp)
    print("to_counter_age:")
    print(to_counter_age)

    df_comp_counter_adjust = calculate_counter_adjustable_in_comp(
        df_pop_end = correctable_in_pop_end,
        df_comp = correctable_in_comp,
        pop_age = pop_age,
        pop_end = pop_end,
        comp = comp,
        to_counter_age = to_counter_age,
        comp_in_comp_end = comp_in_comp_end,
        comp_in_neg = comp_in_neg
    )

    return df_comp_counter_adjust

def run8(comp = 'DTH', use_copy = True):

    self = call_tbl(use_copy)
    
    # Get basic options
    comp_neg = self.get_comp_neg()
    comp_pos = self.get_comp_pos()
    comps = comp_neg + comp_pos
    # raise_if_not_subset([comp], comps, 'comp', 'components of self')
    at_least = get_option('pop.at_least')
    pop_groups = self.get_pop_groups()
    cols_required = pop_groups.copy()
    cols_required.append(comp)    

    # Get properties of the youngest problematic record
    ## .sort_values() will be deprecated in later versions of pandas
    I = self.get_I()
    I = I.query('I != 0').sort_values(pop_groups)
    problematic = I.iloc[0, :] # choose the youngest
    problematic_sex = problematic[pop_groups[0]]
    problematic_age = problematic[pop_groups[1]]
    problematic_val = problematic['I']
    calculated_pop = self.calculate_pop()
    comp_in_neg = comp in comp_neg # comp is in comp_pos otherwise
    comp_in_comp_end = comp in self.get_comp_end()
    age_is_max = problematic_age.is_max()

    # Get the corresponding age(s) of comp to modify & counter-adjust
    ages = calculate_ages_to_modify_and_counter(
        problematic_age, 
        comp_in_comp_end
    )
    to_modify_age = ages['age.to_modify']
    to_counter_age = ages['age.to_counter']

    # Get the maximum amounts modifiable & counter-adjustable
    correctable_in_pop_end = calculated_pop.copy()\
        .loc[lambda df: df[pop_groups[0]] == problematic_sex]
    correctable_in_comp = self\
        .loc[lambda df: df[pop_groups[0]] == problematic_sex]\
        [cols_required]
    
    to_counter_records = run7(comp)
    sum_counter_adjustable =\
        to_counter_records.iloc[:, -1].values.sum()    
    df_pop_end = correctable_in_pop_end
    df_comp = correctable_in_comp
    pop_age = self.get_pop_groups()[1]
    pop_end = self.get_pop_end()
    # comp = comp,
    # problematic_age = problematic_age,
    # to_modify_age = to_modify_age,
    # comp_in_neg = comp_in_neg,
    # sum_counter_adjustable = sum_counter_adjustable

    # calculate_modifiable_in_comp(...)
    pop_end_query = None
    if age_is_max:
        pop_end_query = f"{pop_age} > {get_option('age.max')}"
    else:
        pop_end_query = f"{pop_age} == {problematic_age}"
    df_pop_end_problematic = df_pop_end.query(pop_end_query)
    df_comp_modifiable = None
    if isinstance(to_modify_age, int):
        df_comp_modifiable = df_comp\
            .loc[lambda df: df[pop_age] == to_modify_age]
    elif isinstance(to_modify_age, list):
        df_comp_modifiable = df_comp\
            .loc[lambda df: df[pop_age] <= to_modify_age[1]]\
            .loc[lambda df: df[pop_age] >= to_modify_age[0]]
    else:
        raise NotImplementedError

    print("df_pop_end_problematic:")
    print(df_pop_end_problematic)
    print("")
    print("df_comp_modifiable:")
    print(df_comp_modifiable)
    print("")

    modifiable_val_in_pop_end = df_pop_end_problematic[pop_end].values[0]
    abs_modifiable_val_in_pop_end = abs(modifiable_val_in_pop_end)
    print("abs_modifiable_val_in_pop_end:", abs_modifiable_val_in_pop_end)
    modifiable = None
    if isinstance(to_modify_age, int):
        modifiable_val_in_comp = df_comp_modifiable[comp].values[0]
        print("modifiable_val_in_comp:", modifiable_val_in_comp)
        print("sum_counter_adjustable:", sum_counter_adjustable)
        print("")
        if comp_in_neg:
            modifiable = min(
                abs_modifiable_val_in_pop_end,
                modifiable_val_in_comp,
                sum_counter_adjustable
            )
        else:
            modifiable = min(
                abs_modifiable_val_in_pop_end,
                sum_counter_adjustable
            )
        print("modifiable:", modifiable)
        print("")
    elif isinstance(to_modify_age, list):
        modifiable_val_in_comp = df_comp_modifiable[comp]
        modifiable_0 = None
        modifiable_1 = None
        print("modifiable_val_in_comp:")
        print(modifiable_val_in_comp)
        print("sum_counter_adjustable:", sum_counter_adjustable)

        if comp_in_neg:
            modifiable_val_in_comp_0 = modifiable_val_in_comp.values[0]
            modifiable_val_in_comp_1 = modifiable_val_in_comp.values[1]
            print("modifiable_val_in_comp_0:", modifiable_val_in_comp_0)
            print("modifiable_val_in_comp_1:", modifiable_val_in_comp_1)
            print("")
            modifiable_1 = min(
                abs_modifiable_val_in_pop_end,
                modifiable_val_in_comp_1,
                sum_counter_adjustable
            )
            modifiable_0 = min(
                abs_modifiable_val_in_pop_end - modifiable_1, 
                modifiable_val_in_comp_0,
                sum_counter_adjustable - modifiable_1
            )
            print("modifiable_0:", modifiable_0)
            print("modifiable_1:", modifiable_1)
        else:
            to_divide = min(
                abs_modifiable_val_in_pop_end,
                sum_counter_adjustable
            )
            modifiable_0 = to_divide // 2
            modifiable_1 = to_divide - modifiable_0
            print("to_divide:", to_divide)
            print("modifiable_0:", modifiable_0)
            print("modifiable_1:", modifiable_1)
    else:
        raise NotImplementedError

def run9():
    tbl_cp = call_tbl(True)
    tbl = call_tbl(False)
    
    lst_tbl = [tbl_cp, tbl]
    tbl_1st = lst_tbl[0]
    common_args = tbl_1st.get_args()
    prevs = {}
    for k, v in common_args.items():
        prevs[k] = get_option(k)
        set_option(k, v)
    
    comp_neg_to_use = tbl_1st.get_comp_neg()
    comp_pos_to_use = tbl_1st.get_comp_pos()
    comps = comp_neg_to_use + comp_pos_to_use

    pop_groups = tbl_1st.get_pop_groups()
    pop_sex = pop_groups[0]
    all_cols = tbl_1st.columns.tolist()
    show_pop_end = tbl_1st.get_pop_end() in all_cols
    sexes = np.unique(tbl_1st[pop_sex])
    method = '1dist'

    fixed_tables = {
        rl1: {s: None for s in sexes} 
        for rl1 in range(len(lst_tbl))
    }
    comps_modifieds = {rl2: [] for rl2 in range(len(lst_tbl))}

    for sex in sexes:
        all_tbls = [
            ProvPopTable(
                tb.copy().loc[lambda df: df[pop_sex] == sex],
                reorder_cols = False,
                show_pop_end = show_pop_end,
                flag = False
            ) \
            for tb in lst_tbl.copy()
        ]
        dict_all_tbls = {tt: ttbl for tt, ttbl in enumerate(all_tbls)}
        for t, tbl in enumerate(all_tbls):
            interprovs = [
                tbl.get_interprov_out(), tbl.get_interprov_in()
            ]
            # other_tbls is based on the result of previous iteration(s)
            other_tbls = dict_all_tbls.copy()
            other_tbls.pop(t)
            flag = (sum(tbl.get_I()['I'].values != 0) != 0)
            i = 0
            num_zeros = sum(tbl.get_I()['I'].values == 0)
            while flag:
                comp = comps[i]
                if comp in interprovs:
                    tbl, other_tbls = apply_Ns(
                        tbl, 
                        t,  
                        comp, 
                        method, 
                        other_tbls,
                        comps_modifieds
                    )
                else:
                    tbl = apply_L(
                        tbl,
                        comp,
                        method,
                        comps_modifieds[t]
                    )

                I_vec = tbl.get_I()['I'].values
                new_num_zeros = sum(I_vec == 0)
                if all(I_vec == 0):
                    flag = False
                elif num_zeros != new_num_zeros:
                    i = 0
                    num_zeros = new_num_zeros
                elif i != (len(comps) - 1):
                    i += 1
                else:
                    flag = False

            # Update dict_all_tbls after correcting tbl and 
            # (possibly) other_tbls
            for t1 in dict_all_tbls.copy().keys():
                if t1 == t:
                    dict_all_tbls[t1] = tbl
                else:
                    dict_all_tbls[t1] = other_tbls[t1]
                
        # Update fixed_tables after applying corrections to all population
        # tables of dict_all_tbls
        for t2 in fixed_tables.copy().keys():
            fixed_tables[t2][sex] = dict_all_tbls[t2]

    # Append fixed_tables[t2][sex] within each dict
    fixed_tables = {
        ind: reduce(
            lambda a, b: a.append(b, ignore_index = True), 
            dict_tbl_by_sex.values()
        ) \
        for ind, dict_tbl_by_sex in fixed_tables.copy().items()
    }

    fixed_tables = {
        rl3: ProvPopTable(
            tbl3.sort_values(pop_groups),
            reorder_cols = False,
            show_pop_end = show_pop_end,
            flag = False
        ) \
        for rl3, tbl3 in fixed_tables.copy().items()
    }

    for k2, v2 in prevs.items():
        set_option(k2, v2)

def run10():

    tbl_cp = call_tbl(True)
    tbl = call_tbl(False)
    lst_tbl = [tbl_cp, tbl]
    pop_groups = tbl_cp.get_pop_groups()
    pop_age = 'Age'
    pop_end = tbl_cp.get_pop_end()
    comp = 'IOM'
    other_comp = get_other_comp(tbl_cp, comp)
    comp_L = f"{comp}_L"
    comp_M = f"{comp}_M"
    comp_N = f"{comp}_N"
    comp_O = f"{comp}_O"
    method = '1dist'
    comp_in_comp_end = comp in tbl_cp.get_comp_end()
    comp_in_neg = comp in tbl_cp.get_comp_neg()
    
    other_tbls = {1: tbl}
    fixed_tables = {rl1: None for rl1 in range(len(lst_tbl))}
    comps_modifieds = {rl2: [] for rl2 in range(len(lst_tbl))}

    tbl_cp = apply_L(tbl_cp, 'DTH', '1dist', comps_modifieds[0])
    transfer_ages = calculate_ages_to_transfer(
        tbl_cp,
        comp,
        method
    )
    to_transfer_ages_pop_end = transfer_ages['age.to_transfer_pop_end']
    to_transfer_ages_comp = transfer_ages['age.to_transfer_comp']

    I = tbl_cp.get_I()
    I = I.query('I != 0').sort_values(pop_groups)
    problematic = I.iloc[0, :]
    problematic_age = problematic[pop_age]
    L_df = tbl_cp.get_L(comp, method)
    filtered_L_from_tbl = L_df[
        L_df[pop_age]\
            .apply(Age.get_showing_age)\
            .apply(str)\
            .isin([str(sc) for sc in to_transfer_ages_comp])
    ]

    exact_transferrables = get_Ns(
        tbl_cp,
        comp,
        method,
        other_tbls
    )
    print("exact_transferrables:")
    print(exact_transferrables)

    tbl_index = list(exact_transferrables.keys())
    sample_key = tbl_index[0]
    nrow = len(exact_transferrables[sample_key].index)
    comp_N_sum = np.repeat([0], nrow)
    for v in exact_transferrables.values():
        comp_N_sum += v[comp_N].values
    print("comp_N_sum:")
    print(comp_N_sum)

    correction_to_tbl = np.minimum(
        abs(filtered_L_from_tbl[comp_L].values),
        abs(comp_N_sum)
    )
    signs = calculate_signs(
        nrow, 
        problematic_age.is_max(), 
        comp_in_comp_end, 
        comp_in_neg
    )
    correction_to_tbl *= signs
    filtered_L_from_tbl[comp_O] = correction_to_tbl
    
    comp_O_df = filtered_L_from_tbl.copy()
    del comp_O_df[comp_L]
    comp_O_df[pop_age] = comp_O_df[pop_age].apply(str)

    print("comp_O_df with correction_to_tbl:")
    print(comp_O_df)

    tbl_cp_cp = tbl_cp.copy()
    tbl_cp_cp[pop_age] = tbl_cp_cp[pop_age].apply(str)
    tbl_cp_cp = tbl_cp_cp.merge(comp_O_df, on = pop_groups, how = 'left')    
    tbl_cp_cp.fillna(0, inplace = True)
    tbl_cp_cp[comp_O] = tbl_cp_cp[comp_O].apply(int)
    if (tbl_cp_cp[comp_O].values != 0).any():
        comps_modifieds[0].append(tbl_cp_cp[pop_groups + [comp_O]])
    tbl_cp_cp[comp] += tbl_cp_cp[comp_O]
    del tbl_cp_cp[comp_O]

    print("tbl_cp after application of comp_O:")
    print(tbl_cp_cp)

    other_tbls_cp = other_tbls.copy()
    for i in tbl_index:
        other_tbl = other_tbls_cp[i].copy()
        other_tbl[pop_age] = other_tbl[pop_age].apply(str)
        comp_N_to_apply = exact_transferrables[i].copy()
        comp_N_to_apply[pop_age] = comp_N_to_apply[pop_age].apply(str)
        other_tbl = other_tbl\
            .merge(
                comp_N_to_apply, 
                on = pop_groups, 
                how = "left"
            )
        other_tbl.fillna(0, inplace = True)
        print("other_tbl after left-joining:")
        print(other_tbl)
        other_tbl[comp_N] = other_tbl[comp_N].apply(int)
        print(f"Applied comp_N to other_tbls[{i}]:")
        print(other_tbl[pop_groups + [comp_N]])
        if (other_tbl[comp_N].values != 0).any():
            comps_modifieds[i].append(other_tbl[pop_groups + [comp_N]])
        other_tbl[other_comp] += other_tbl[comp_N]
        del other_tbl[comp_N]
        other_tbl = ProvPopTable(
            other_tbl,
            reorder_cols = False,
            show_pop_end = False,
            is_subprov = False,
            flag = False
        )
        other_tbls_cp[i] = other_tbl

    print("other_tbls_cp after application of comp_N:")
    print(other_tbls_cp)

def run11():
    comp_M = 'comp_M'
    comp_N = 'comp_N'
    comp_in_neg = True
    nrow = 5

    max_transferrables = {
        1: pd.DataFrame({
            comp_M: np.array([0,1,2,0,-2]),
            comp_N: np.repeat([0], nrow)
        }),
        2: pd.DataFrame({
            comp_M: np.array([1,1,1,-1,-1]),
            comp_N: np.repeat([0], nrow)
        })
    } if comp_in_neg else {
        1: pd.DataFrame({
            comp_M: np.array([0,-1,-2,0,2]),
            comp_N: np.repeat([0], nrow)
        }),
        2: pd.DataFrame({
            comp_M: np.array([-1,-1,-1,1,1]),
            comp_N: np.repeat([0], nrow)
        })        
    }
    tbl_index = list(max_transferrables.keys())
    filtered_L =\
        np.array([ 1, 1, 2,-1,-3]) if comp_in_neg else \
        np.array([-1,-1,-2, 1, 3])
    comp_L_abs = abs(filtered_L)
    comp_Ms_sum = np.repeat([0], nrow)
    for v2 in max_transferrables.copy().values():
        comp_Ms_sum += v2[comp_M].values
    comp_Ms_sum_abs = abs(comp_Ms_sum)
    signs = calculate_signs(nrow, True, False, comp_in_neg)
    agg_rem = np.minimum(comp_L_abs, comp_Ms_sum_abs)
    agg_rem *= signs
    print(f"agg_rem before while-loop: {agg_rem}")

    exact_transferrables = max_transferrables.copy()
    flag = True
    while flag:
        for i1 in tbl_index:
            print(f'table index : {i1}')
            comp_M_local = exact_transferrables[i1][comp_M].values
            agg_rem_local = np.minimum(
                abs(agg_rem),
                abs(comp_M_local)
            )
            agg_rem_local *= signs
            print(f"agg_rem_local: {agg_rem_local}")
            comp_N_local = np.repeat([0], nrow)
            local_rem = abs(agg_rem_local[-2:])
            at_least_one_to_ca = False
            if local_rem[-1] >= 1:
                comp_N_local[-1] = -1 if comp_in_neg else 1
                at_least_one_to_ca = True
            elif local_rem[-2] >= 1:
                comp_N_local[-2] = -1 if comp_in_neg else 1
                at_least_one_to_ca = True
            
            if at_least_one_to_ca:
                for j1 in range(nrow - 3, -1, -1):
                    if abs(agg_rem_local[j1]) >= 1:
                        comp_N_local[j1] = 1 if comp_in_neg else -1
                        break
            print(f"comp_N_local: {comp_N_local}")
            agg_rem -= comp_N_local
            exact_transferrables[i1][comp_M] -= comp_N_local
            exact_transferrables[i1][comp_N] += comp_N_local
            print(f"comp_N after computations: {exact_transferrables[i1][comp_N].values}")
            print(f'agg_rem after computations: {agg_rem}')
            print(f"comp_M after computations: {exact_transferrables[i1][comp_M].values}")
        flag = (agg_rem[-2:] != [0, 0]).any()

    print(exact_transferrables[1])
    print(exact_transferrables[2])

def run12():
    tbls = call_tbls()
    agg_tbls = AggregateProvPopTable(tbls)
    result = agg_tbls.fix_all_issues(return_all_mods = True)

    return result

def run13():
    
    class Test():
        def __init__(self, hidden):
            self.__hidden = hidden
        def get_hidden(self):
            return self.__hidden

    class SubTest(Test):
        def hidden_printer_using_private_attribute_directly(self):
            # raises AttributeError
            return self.__hidden + ', private'
        def hidden_printer_using_getter(self):
            # returns private attribute of Test
            return self.get_hidden() + ', getter'

    subtest = SubTest(hidden = 'This msg is a private attribute.')
    print(subtest.get_hidden())
    print(subtest.hidden_printer_using_getter())
    print(subtest.hidden_printer_using_private_attribute_directly())

def run14(sex = None):
    tbls = run5(sex)
    # tbls_lst = list(tbls.copy().values())
    set_option(
        'pop.sex', 'Sex',
        'pop.age', 'Age',
        'pop.end', 'POP_2002',
        'pop.start', 'POP_2001',
        'pop.birth', 'BTH',
        'comp_neg.temp_out', 'NTE',
        'comp_neg.emi', 'EMI',
        'comp_neg.npr_out', 'NPR_out',
        'comp_neg.death', 'DTH_D01',
        'comp_neg.interprov_out', 'MIP_out',
        'comp_neg.intraprov_out', 'MIT_out',
        'comp_neg.etc', [],
        'comp_pos.ret_emi', 'REM',
        'comp_pos.npr_in', 'NPR_in',
        'comp_pos.immi', 'IMM',
        'comp_pos.interprov_in', 'MIP_in',
        'comp_pos.intraprov_in', 'MIT_in',
        'comp_pos.etc', [],
        'comp.end', ['NPR_in']
    )
    agg_tbls = AggregateSubProvPopTable(tbls)
    result = agg_tbls.fix_all_issues(return_all_mods = True)

    return result

def run15(sex = 1):
    tbls = run5(sex)
    lst_tbl = list(tbls.copy().values())
    set_option(
        'pop.sex', 'Sex',
        'pop.age', 'Age',
        'pop.end', 'POP_2002',
        'pop.start', 'POP_2001',
        'pop.birth', 'BTH',
        'comp_neg.temp_out', 'NTE',
        'comp_neg.emi', 'EMI',
        'comp_neg.npr_out', 'NPR_out',
        'comp_neg.death', 'DTH_D01',
        'comp_neg.interprov_out', 'MIP_out',
        'comp_neg.intraprov_out', 'MIT_out',
        'comp_neg.etc', [],
        'comp_pos.ret_emi', 'REM',
        'comp_pos.npr_in', 'NPR_in',
        'comp_pos.immi', 'IMM',
        'comp_pos.interprov_in', 'MIP_in',
        'comp_pos.intraprov_in', 'MIT_in',
        'comp_pos.etc', [],
        'comp.end', ['NPR_in']
    )

    tbl_1st = lst_tbl[0]
    comp_neg_to_use = tbl_1st.get_comp_neg()
    comp_pos_to_use = tbl_1st.get_comp_pos()
    comps = comp_neg_to_use + comp_pos_to_use

    pop_groups = tbl_1st.get_pop_groups()
    pop_sex = pop_groups[0]
    pop_age = pop_groups[1]
    pop_end = tbl_1st.get_pop_end()
    at_least = 1
    all_cols = tbl_1st.columns.tolist()
    show_pop_end = tbl_1st.get_pop_end() in all_cols    
    method = '1dist'

    fixed_tables = {
        rl1: {1: None} 
        for rl1 in range(len(lst_tbl))
    }
    comps_modifieds = {rl2: [] for rl2 in range(len(lst_tbl))}

    dict_all_tbls = {
        tt: [ttbl] \
        for tt, ttbl in enumerate(lst_tbl)
    }
    dat_keys = list(dict_all_tbls.copy().keys())

    t = 0
    other_tbls = dict_all_tbls.copy()
    tbl = other_tbls.pop(t)
    tbl = tbl[-1]
    other_tbls = {
        t_other: tbl_other[-1] \
        for t_other, tbl_other in other_tbls.items()
    }
    flag = (sum(tbl.get_I()['I'].values != 0) != 0)
    i = 3
    num_zeros = sum(tbl.get_I()['I'].values == 0)
    
    comp = comps[i]
    tbl, other_tbls = apply_Ns(
        tbl,
        t,
        comp,
        method,
        other_tbls,
        comps_modifieds
    )
    I_vec = tbl.get_I()['I'].values
    new_num_zeros = sum(I_vec == 0)
    if all(I_vec == 0):
        flag = False
    elif num_zeros != new_num_zeros:
        i = 0
        num_zeros = new_num_zeros
    elif i != (len(comps) - 1):
        i += 1
    else:
        flag = False

    # print("tbl after correction at age 96:")
    # print(tbl)

    # print("other_tbls after correction at age 96:")
    # for k, v in other_tbls.items():
    #     print(f"{k}:")
    #     print(v)
    #     print("")

#STARTING_POINT############################################################

    i = 3
    comp = comps[i]
    other_comp = get_other_comp(tbl, comp)
    to_transfer_ages = calculate_ages_to_transfer(
        tbl,
        comp,
        method,
        other_tbls
    )
    to_transfer_ages_pop_end = to_transfer_ages['age.to_transfer_pop_end']
    to_transfer_ages_comp = to_transfer_ages['age.to_transfer_comp']

    I = tbl.get_I()
    I = I.query('I != 0').sort_values(pop_groups)
    problematic = I.iloc[0, :]
    problematic_sex = problematic[pop_sex]
    problematic_age = problematic[pop_age]
    comp_in_comp_end = comp in tbl.get_comp_end()
    comp_J = f"{comp}_J"
    other_comp_J = f"{other_comp}_J"

    # J_df = get_J(tbl, comp, other_tbls)
    # print("J_df (using other_tbls):")
    # print(J_df)
    # print("")

    L_df = get_L(tbl, comp, method, other_tbls)
    print("L_df (using other_tbls):")
    print(L_df)
    print("")
    
    ages = calculate_ages_to_modify_and_counter(
        problematic_age,
        comp_in_comp_end
    )
    to_counter_age = ages['age.to_counter']
    to_modify_age = ages['age.to_modify']
    # to_counter_age_min = to_counter_age[0]
    # to_counter_age_max = to_counter_age[1]

    other_comp = get_other_comp(tbl, comp)
    other_comp_in_neg = other_comp in comp_neg_to_use
    other_comp_in_comp_end = other_comp in tbl.get_comp_end()
    to_absorb_records = calculate_absorbable_in_other_comp(
        pop_sex = pop_sex,
        pop_age = pop_age,
        pop_end = pop_end,
        problematic_sex = problematic_sex,
        problematic_age = problematic_age,
        to_counter_age = to_counter_age,
        to_modify_age = to_modify_age,
        other_comp = other_comp,
        other_comp_in_comp_end = other_comp_in_comp_end,
        other_comp_in_neg = other_comp_in_neg,
        other_tbls = other_tbls
    )

    to_absorb_ca_total = None
    to_absorb_m_total = None
    for to0 in other_tbls.keys():
        if to_absorb_ca_total is None:
            to_absorb_ca_total = to_absorb_records['ca'][to0][other_comp_J].values
        else:
            to_absorb_ca_total += to_absorb_records['ca'][to0][other_comp_J].values
    
        if to_absorb_m_total is None:
            to_absorb_m_total = to_absorb_records['m'][to0][other_comp_J].values
        else:
            to_absorb_m_total += to_absorb_records['m'][to0][other_comp_J].values
    to_absorb_ca = to_absorb_records['ca'][to0][[pop_sex, pop_age]]
    to_absorb_ca[other_comp_J] = to_absorb_ca_total
    to_absorb_m = to_absorb_records['m'][to0][[pop_sex, pop_age]]
    to_absorb_m[other_comp_J] = to_absorb_m_total

    # print("to_absorb_ca:")
    # print(to_absorb_ca)
    # print("to_absorb_m:")
    # print(to_absorb_m)
    # print("")

    # for to, otbl in other_tbls.items():
    #     correctable_in_pop_end = otbl.calculate_pop().copy()
    #     correctable_in_other_comp = otbl[pop_groups + [other_comp]]
    #     print(f"{to + 1001}:")
    #     df_comp_ca = calculate_counter_adjustable_in_comp(
    #         df_pop_end = correctable_in_pop_end,
    #         df_comp = correctable_in_other_comp,
    #         pop_age = pop_age,
    #         pop_end = pop_end,
    #         comp = other_comp,
    #         to_counter_age = to_counter_age,
    #         comp_in_comp_end = other_comp_in_comp_end,
    #         comp_in_neg = not other_comp_in_neg
    #     )
    #     sum_ca = df_comp_ca.iloc[:, -1].values.sum()
    #     df_comp_m = calculate_modifiable_in_comp(
    #         df_pop_end = correctable_in_pop_end,
    #         df_comp = correctable_in_other_comp,
    #         pop_age = pop_age,
    #         pop_end = pop_end,
    #         comp = other_comp,
    #         problematic_age = problematic_age,
    #         to_modify_age = to_modify_age,
    #         comp_in_neg = not other_comp_in_neg,
    #         sum_counter_adjustable = sum_ca
    #     )
        # if (df_comp_m[comp_J].values == 0).all():
        #     df_comp_ca[comp_J] = 0
        # print("correctable_in_pop_end, filtered:")
        # print(
        #     correctable_in_pop_end\
        #         .loc[lambda df: df[pop_age] >= to_counter_age_min + 1]\
        #         .loc[lambda df: df[pop_age] <= to_counter_age_max + 1]
        # )
        # print("")
        # print("correctable_in_other_comp, filtered:")
        # print(
        #     correctable_in_other_comp\
        #         .loc[lambda df: df[pop_age] >= to_counter_age_min + 1]\
        #         .loc[lambda df: df[pop_age] <= to_counter_age_max + 1]
        # )
        # print("")
        # print("df_comp_ca:")
        # print(df_comp_ca)
        # print("")
        # print("df_comp_m")
        # print(df_comp_m)
        # print("")

    # Jsum = np.repeat([0], len(df_comp_ca.index))
    # for Jdf in df_comp_cas.values():
    #     Jsum += Jdf.iloc[:, -1].values
    # print("Jsum:")
    # print(Jsum)
    # print("")
    # print("J_df['records.to_counter'].iloc[:, -1].values:")
    # print(J_df['records.to_counter'].iloc[:, -1].values)
    # print("")
    # minJsumJdf = pd.DataFrame({
    #     'a': Jsum,
    #     'b': J_df['records.to_counter'].iloc[:, -1].values
    # })
    # df_comp_ca_after = df_comp_ca[pop_groups]
    # df_comp_ca_after[comp_J] = minJsumJdf.min(axis = 1).values
    # print("df_comp_ca_after (element-wise minimums):")
    # print(df_comp_ca_after)
    # print("")

#ENDING_POINT##############################################################

    filtered_L_from_tbl = L_df[
        L_df[pop_age]\
            .apply(Age.get_showing_age)\
            .apply(str)\
            .isin([str(sc) for sc in to_transfer_ages_comp])
    ]
    print(f"filtered_L_from_tbl, t = {t}:")
    print(filtered_L_from_tbl)
    others_tbl_pop_end = {
        i0: tb0.calculate_pop()[
            tb0.calculate_pop()[pop_age]\
                .apply(Age.get_showing_age)\
                .apply(str)\
                .isin([str(sp) for sp in to_transfer_ages_pop_end])
        ] \
        for i0, tb0 in other_tbls.copy().items()        
    }
    others_pop_end = {
        i1: tb1.assign(
            max_peal_0 = lambda df: df[pop_end].apply(
                lambda x: max(x - at_least, 0)
            )
        )\
        [pop_groups + ['max_peal_0']] \
        for i1, tb1 in others_tbl_pop_end.copy().items()
    }
    others_other_comp = {
        i2: tb2[
            tb2[pop_age]\
                .apply(Age.get_showing_age)\
                .apply(str)\
                .isin([str(sc) for sc in to_transfer_ages_comp])
        ]\
        [pop_groups + [other_comp]] \
        for i2, tb2 in other_tbls.copy().items()
    }
    print("")
    for k, v in others_pop_end.items():
        print(f"{k + 1001}:")
        print("others_pop_end (max_peal_0):")
        print(v)
        print("")
        print("others_other_comp:")
        print(others_other_comp[k])
        print("")
    # for k, v in others_other_comp.items():
    #     print(f"{k + 1001}:")
    #     print(v)
    #     print("")
    tbl_index, sample_key = sort_tbl_index(others_pop_end)
    print("tbl_index:")
    print(tbl_index)

    max_transferrables_to_other_comp = {
        i2_1: tbl2_1[pop_groups] \
        for i2_1, tbl2_1 in others_other_comp.copy().items()
    }

    comp_L = f"{comp}_L"
    comp_M = f"{comp}_M"
    comp_in_neg = comp in tbl.get_comp_neg()
    filtered_L_from_tbl_ca =\
        filtered_L_from_tbl[comp_L].values[:-1]
    filtered_L_from_tbl_m =\
        filtered_L_from_tbl[comp_L].values[-1]
    for i3, tbl3 in others_pop_end.copy().items():
        other_tbl_max_peal_0_ca =\
            others_pop_end[i3]['max_peal_0'].values[:-1]
        other_tbl_max_peal_0_m =\
            others_pop_end[i3]['max_peal_0'].values[-1]
        other_tbl_other_comp_ca =\
            others_other_comp[i3][other_comp].values[:-1]
        other_tbl_other_comp_m =\
            others_other_comp[i3][other_comp].values[-1]
        if (i3 == 8):
            print("other_tbl_max_peal_0_ca:")
            print(other_tbl_max_peal_0_ca)
            print("other_tbl_max_peal_0_m:")
            print(other_tbl_max_peal_0_m)
            print("other_tbl_other_comp_ca:")
            print(other_tbl_other_comp_ca)
            print("other_tbl_other_comp_m:")
            print(other_tbl_other_comp_m)
            print("abs(filtered_L_from_tbl_ca):")
            print(abs(filtered_L_from_tbl_ca))
        if comp_in_neg:
            transferrable_dfs = pd.DataFrame({
                # 'a': other_tbl_max_peal_0_ca,
                'b': abs(filtered_L_from_tbl_ca),
                'c': other_tbl_other_comp_ca
            })
            transferrable_vals_at_ca =\
                -transferrable_dfs.min(axis = 1).values
            transferrable_val_at_m = min(
                other_tbl_max_peal_0_m,
                abs(filtered_L_from_tbl_m),
                abs(sum(transferrable_vals_at_ca))
            )
            if (i3 == 2):
                print("transferrable_vals_at_ca:")
                print(transferrable_vals_at_ca)
                print("transferrable_vals_at_m:")
                print(transferrable_val_at_m)
            top_items =\
                [0 for i8 in range(len(transferrable_vals_at_ca))]\
                if (transferrable_val_at_m == 0) \
                else list(transferrable_vals_at_ca)
        else:
            transferrable_val_at_m = -min(
                other_tbl_max_peal_0_m,
                abs(filtered_L_from_tbl_m),
                other_tbl_other_comp_m
            )
            top_items =\
                [0 for i7 in range(len(filtered_L_from_tbl_ca))]\
                if (transferrable_val_at_m == 0) \
                else list(abs(filtered_L_from_tbl_ca))
        transferrable_vals = top_items + [transferrable_val_at_m]
        if (i3 == 8):
            print("transferrable_vals:")
            print(transferrable_vals)
        max_transferrables_to_other_comp[i3][comp_M] =\
            transferrable_vals

    print("max_transferrables_to_other_comp:")
    for k, v in max_transferrables_to_other_comp.items():
        print(f"{k}:")
        print(v)
        print("")

    # tbl, other_tbls = apply_Ns(
    #     tbl,
    #     t,
    #     comp,
    #     method,
    #     other_tbls,
    #     comps_modifieds
    # )
    # print(comps_modifieds)

def run16(sex = 1):
    tbls = run5(sex)
    lst_tbl = list(tbls.copy().values())
    set_option(
        'pop.sex', 'Sex',
        'pop.age', 'Age',
        'pop.end', 'POP_2002',
        'pop.start', 'POP_2001',
        'pop.birth', 'BTH',
        'comp_neg.temp_out', 'NTE',
        'comp_neg.emi', 'EMI',
        'comp_neg.npr_out', 'NPR_out',
        'comp_neg.death', 'DTH_D01',
        'comp_neg.interprov_out', 'MIP_out',
        'comp_neg.intraprov_out', 'MIT_out',
        'comp_neg.etc', [],
        'comp_pos.ret_emi', 'REM',
        'comp_pos.npr_in', 'NPR_in',
        'comp_pos.immi', 'IMM',
        'comp_pos.interprov_in', 'MIP_in',
        'comp_pos.intraprov_in', 'MIT_in',
        'comp_pos.etc', [],
        'comp.end', ['NPR_in']
    )

    tbl_1st = lst_tbl[0]
    comp_neg_to_use = tbl_1st.get_comp_neg()
    comp_pos_to_use = tbl_1st.get_comp_pos()
    comps = comp_neg_to_use + comp_pos_to_use

    pop_groups = tbl_1st.get_pop_groups()
    pop_sex = pop_groups[0]
    pop_age = pop_groups[1]
    pop_end = tbl_1st.get_pop_end()
    at_least = 1
    all_cols = tbl_1st.columns.tolist()
    show_pop_end = tbl_1st.get_pop_end() in all_cols    
    method = '1dist'

    fixed_tables = {
        rl1: {1: None} 
        for rl1 in range(len(lst_tbl))
    }
    comps_modifieds = {rl2: [] for rl2 in range(len(lst_tbl))}

    dict_all_tbls = {
        tt: [ttbl] \
        for tt, ttbl in enumerate(lst_tbl)
    }
    dat_keys = list(dict_all_tbls.copy().keys())

    t = 0
    other_tbls = dict_all_tbls.copy()
    tbl = other_tbls.pop(t)
    tbl = tbl[-1]
    other_tbls = {
        t_other: tbl_other[-1] \
        for t_other, tbl_other in other_tbls.items()
    }
    flag = (sum(tbl.get_I()['I'].values != 0) != 0)
    i = 3
    num_zeros = sum(tbl.get_I()['I'].values == 0)
    
    comp = comps[i]
    tbl, other_tbls = apply_Ns(
        tbl,
        t,
        comp,
        method,
        other_tbls,
        comps_modifieds
    )
    I_vec = tbl.get_I()['I'].values
    new_num_zeros = sum(I_vec == 0)
    if all(I_vec == 0):
        flag = False
    elif num_zeros != new_num_zeros:
        i = 0
        num_zeros = new_num_zeros
    elif i != (len(comps) - 1):
        i += 1
    else:
        flag = False

    print("Death:")
    print(f"{t + 1001}:")
    print(tbl[pop_groups + [comp]].query(f"{pop_age} <= 97"))
    print("")
    for k, v in other_tbls.items():
        print(f"{k + 1001}:")
        print(v[pop_groups + [comp]].query(f"{pop_age} <= 97"))
        print("")

    # i = 3
    # comp = comps[i]
    # other_comp = get_other_comp(tbl, comp)

    # exact_transferrables =\
    #     get_Ns(tbl, comp, method, other_tbls)

    # print("exact_transferrables:")
    # for k, v in exact_transferrables.items():
    #     print(f"{k + 1001}:")
    #     print(v)
    #     print("")
