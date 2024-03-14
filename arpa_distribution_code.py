# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 12:50:13 2021

@author: Cody Kallen
"""


import os
os.chdir('C:/Users/cody_/Documents/GitHub/Tax-Calculator/')
import numpy as np
import pandas as pd
import copy
import taxcalc
from taxcalc import *


"""
Distribution table

Measures to compute:
    Pct change in after-tax income
    Share of total change
    Average tax change ($)
    Average tax rate, before, after and difference
"""

def make_calculator(refdict = {}, year=2020):
    """
    Creates a calculator advanced to the given year and calculates tax results
    Note: Passing an empty dictionary to refdict produces a 
          current law calculator
    """
    assert year in range(2014, 2030)
    assert type(refdict) is dict
    pol = Policy()
    rec = Records('puf.csv')
    if refdict != {}:
        pol.implement_reform(refdict)
    calc1 = Calculator(pol, rec)
    calc1.advance_to_year(year)
    calc1.calc_all()
    return calc1

dict1 = Calculator.read_json_param_objects('taxcalc/reforms/ARPA.json', None)['policy']
calc0 = make_calculator({}, 2021)
calc1 = make_calculator(dict1, 2021)

df1 = pd.DataFrame({'expanded_income': calc0.array('expanded_income'),
                    'size': np.maximum(calc0.array('XTOT'), 1),
                    'wgt': calc0.array('s006'),
                    'tax0': calc0.array('combined'),
                    'tax1': calc1.array('combined'),
                    'aftertax0': calc0.array('aftertax_income'),
                    'aftertax1': calc1.array('aftertax_income'),
                    'rrc': calc1.array('recovery_rebate_credit')})

# Identify filers by income group
df1['adjustedinc'] = np.array(df1['expanded_income']) / np.sqrt(df1['size'])
df1.sort_values(by='adjustedinc', axis=0, inplace=True)
df2 = df1[df1['expanded_income'] >= 0]
df2.reset_index(drop=True, inplace=True)
popmeasure = np.array(df2['wgt']) * np.array(df2['size'])
qtile = np.cumsum(popmeasure) / sum(popmeasure)
groupid = np.ones(len(qtile))
groupid = np.where(qtile >= 0.2, 2, groupid)
groupid = np.where(qtile >= 0.4, 3, groupid)
groupid = np.where(qtile >= 0.6, 4, groupid)
groupid = np.where(qtile >= 0.8, 5, groupid)
groupid = np.where(qtile >= 0.9, 6, groupid)
groupid = np.where(qtile >= 0.95, 7, groupid)
groupid = np.where(qtile >= 0.99, 8, groupid)

dfg1 = df2[groupid == 1]
dfg2 = df2[groupid == 2]
dfg3 = df2[groupid == 3]
dfg4 = df2[groupid == 4]
dfg5 = df2[groupid == 5]
dfg6 = df2[groupid == 6]
dfg7 = df2[groupid == 7]
dfg8 = df2[groupid == 8]

# Compute percent changes in after-tax income
dres1 = [sum(dfg1['aftertax1'] * dfg1['wgt']) / sum(dfg1['aftertax0'] * dfg1['wgt']) - 1,
         sum(dfg2['aftertax1'] * dfg2['wgt']) / sum(dfg2['aftertax0'] * dfg2['wgt']) - 1,
         sum(dfg3['aftertax1'] * dfg3['wgt']) / sum(dfg3['aftertax0'] * dfg3['wgt']) - 1,
         sum(dfg4['aftertax1'] * dfg4['wgt']) / sum(dfg4['aftertax0'] * dfg4['wgt']) - 1,
         sum(dfg5['aftertax1'] * dfg5['wgt']) / sum(dfg5['aftertax0'] * dfg5['wgt']) - 1,
         sum(dfg6['aftertax1'] * dfg6['wgt']) / sum(dfg6['aftertax0'] * dfg6['wgt']) - 1,
         sum(dfg7['aftertax1'] * dfg7['wgt']) / sum(dfg7['aftertax0'] * dfg7['wgt']) - 1,
         sum(dfg8['aftertax1'] * dfg8['wgt']) / sum(dfg8['aftertax0'] * dfg8['wgt']) - 1,
         sum(df1['aftertax1'] * df1['wgt']) / sum(df1['aftertax0'] * df1['wgt']) - 1]
for i in range(9): print(dres1[i])
# Compute average tax change in dollars
dres2 = [sum((dfg1['tax1'] - dfg1['tax0']) * dfg1['wgt']) / sum(dfg1['wgt']),
         sum((dfg2['tax1'] - dfg2['tax0']) * dfg2['wgt']) / sum(dfg2['wgt']),
         sum((dfg3['tax1'] - dfg3['tax0']) * dfg3['wgt']) / sum(dfg3['wgt']),
         sum((dfg4['tax1'] - dfg4['tax0']) * dfg4['wgt']) / sum(dfg4['wgt']),
         sum((dfg5['tax1'] - dfg5['tax0']) * dfg5['wgt']) / sum(dfg5['wgt']),
         sum((dfg6['tax1'] - dfg6['tax0']) * dfg6['wgt']) / sum(dfg6['wgt']),
         sum((dfg7['tax1'] - dfg7['tax0']) * dfg7['wgt']) / sum(dfg7['wgt']),
         sum((dfg8['tax1'] - dfg8['tax0']) * dfg8['wgt']) / sum(dfg8['wgt']),
         sum((df1['tax1'] - df1['tax0']) * df1['wgt']) / sum(df1['wgt'])]
for i in range(9): print(dres2[i])
# Compute share of total tax change
dres3 = [sum((dfg1['tax1'] - dfg1['tax0']) * dfg1['wgt']),
         sum((dfg2['tax1'] - dfg2['tax0']) * dfg2['wgt']),
         sum((dfg3['tax1'] - dfg3['tax0']) * dfg3['wgt']),
         sum((dfg4['tax1'] - dfg4['tax0']) * dfg4['wgt']),
         sum((dfg5['tax1'] - dfg5['tax0']) * dfg5['wgt']),
         sum((dfg6['tax1'] - dfg6['tax0']) * dfg6['wgt']),
         sum((dfg7['tax1'] - dfg7['tax0']) * dfg7['wgt']),
         sum((dfg8['tax1'] - dfg8['tax0']) * dfg8['wgt']),
         sum((df1['tax1'] - df1['tax0']) * df1['wgt'])]
for i in range(9): print(dres3[i] / dres3[8])
# Compute average tax rate, pre-ARPA
dres4 = [sum(dfg1['tax0'] * dfg1['wgt']) / sum(dfg1['expanded_income'] * dfg1['wgt']),
         sum(dfg2['tax0'] * dfg2['wgt']) / sum(dfg2['expanded_income'] * dfg2['wgt']),
         sum(dfg3['tax0'] * dfg3['wgt']) / sum(dfg3['expanded_income'] * dfg3['wgt']),
         sum(dfg4['tax0'] * dfg4['wgt']) / sum(dfg4['expanded_income'] * dfg4['wgt']),
         sum(dfg5['tax0'] * dfg5['wgt']) / sum(dfg5['expanded_income'] * dfg5['wgt']),
         sum(dfg6['tax0'] * dfg6['wgt']) / sum(dfg6['expanded_income'] * dfg6['wgt']),
         sum(dfg7['tax0'] * dfg7['wgt']) / sum(dfg7['expanded_income'] * dfg7['wgt']),
         sum(dfg8['tax0'] * dfg8['wgt']) / sum(dfg8['expanded_income'] * dfg8['wgt']),
         sum(df1['tax0'] * df1['wgt']) / sum(df1['expanded_income'] * df1['wgt'])]
for i in range(9): print(dres4[i])
# Compute average tax rate, under ARPA
dres5 = [sum(dfg1['tax1'] * dfg1['wgt']) / sum(dfg1['expanded_income'] * dfg1['wgt']),
         sum(dfg2['tax1'] * dfg2['wgt']) / sum(dfg2['expanded_income'] * dfg2['wgt']),
         sum(dfg3['tax1'] * dfg3['wgt']) / sum(dfg3['expanded_income'] * dfg3['wgt']),
         sum(dfg4['tax1'] * dfg4['wgt']) / sum(dfg4['expanded_income'] * dfg4['wgt']),
         sum(dfg5['tax1'] * dfg5['wgt']) / sum(dfg5['expanded_income'] * dfg5['wgt']),
         sum(dfg6['tax1'] * dfg6['wgt']) / sum(dfg6['expanded_income'] * dfg6['wgt']),
         sum(dfg7['tax1'] * dfg7['wgt']) / sum(dfg7['expanded_income'] * dfg7['wgt']),
         sum(dfg8['tax1'] * dfg8['wgt']) / sum(dfg8['expanded_income'] * dfg8['wgt']),
         sum(df1['tax1'] * df1['wgt']) / sum(df1['expanded_income'] * df1['wgt'])]
for i in range(9): print(dres5[i])












