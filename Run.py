# -*- coding: utf-8 -*-
import numpy as np
import streamlit as st
from streamlit_echarts import st_echarts
from params import *
import pandas as pd
import time
import copy
from utils import *
from scipy.stats import norm
from itertools import chain

np.seterr(divide='ignore', invalid='ignore')

st.set_page_config(layout='wide')
st.header('ADRFI Toolkit')
st.text('')

show_layering_empyt = st.sidebar.empty()
survival_empty = st.sidebar.empty()

new_input = {}

st.sidebar.markdown('## Set a policy:')

for k in show_name:
    dvalue = dps[user_input][0][k]*100 if k in input_pct else dps[user_input][0][k]
    nv = st.sidebar.text_input(show_name[k], dvalue, key=k)
    nv = float(nv)/100.0 if k in input_pct else float(nv)
    new_input[k] = nv

bg_params = st.sidebar.empty()
bg_expander = bg_params.beta_expander('Other model settings')
new_bg_input = {}
for k in dps[bg_input][0]:
    new_bg_input[k] = float(bg_expander.text_input(k, value=dps[bg_input][0][k], key=k))

st.sidebar.text('')
st.sidebar.text('')
if st.sidebar.button('Save this policy'):
    # is_default = True
    # for k in new_input:
    #     if new_input[k] != dps[user_input][0][k]:
    #         is_default = False
    # for k in new_bg_input:
    #     if new_bg_input[k] != dps[bg_input][0][k]:
    #         is_default = False
    # if not (new_bg_input in dps[bg_input] and new_input in dps[user_input]) and not is_default:
    dps[bg_input].append(new_bg_input)
    dps[user_input].append(new_input)


if st.sidebar.button('reset the policies'):
    with open('Run.py', 'a', encoding='utf-8') as f:
        f.write('#')
    st.experimental_rerun()


pses = []  # 计算过程的多组参数

for i in range(len(dps[user_input])):
    dps_ = copy.deepcopy(dps)
    uinp = copy.deepcopy(dps_[user_input][i])
    dps_.update(uinp)
    del dps_[user_input]
    bginp = copy.deepcopy(dps_[bg_input][i])
    dps_.update(bginp)
    del dps_[bg_input]


    dps_[cb_AMT] = dps_[cb_limit] - dps_[cb_att]
    dps_[tier1_RL] = dps_[tier1_AMT] * dps_[tier1_BenRate]
    dps_[tier1_Int] = dps_[tier1_AMT] * dps_[tier1_IntRate]
    dps_[tier2_RL] = dps_[tier1_RL] * dps_[tier2_BenRate]
    dps_[tier2_Int] = dps_[tier2_RL] * dps_[tier2_IntRate]
    dps_[dataSR] = min(dps_[data_Invest] * dps_[dataSR_ImpRatio], dps_[dataSR_Cap])
    dps_[dataCBLoad] = dps_[dataCBLoad_Base] * max(0, 1 - dps_[data_Invest] * dps_[dataCBLoad_ImpRatio])
    dps_[ipSR] = min(dps_[ip_Invest] * dps_[ipSR_ImpRate], dps_[ipSR_Cap])
    dps_[ipCBLoad] = dps_[ipCBLoad_Base] * max(0, 1 - dps_[ip_Invest] * dps_[ipCBLoad_ImpRatio])
    dps_[ipRLLoad] = dps_[ipRLLoad_Base] * max(0, 1 - min(dps_[ip_Invest] * dps_[ipRLLoad_ImpRatio],
                                                          dps_[ipRLLoad_ImpRatio_Cap]))
    dps_[inSize] = dps_[inSize_Base] * (1 + min(dps_[ip_Invest] * dps_[inSize_ImpRatio], dps_[inSize_ImpRatio_Cap]))

    dps_[unit] = round(3 * dps_[L200Y] / dps_[no_cells], 0)
    dps_[SharpeRatio] = dps_[SharpeRatioBaseline]*(1-dps_[dataSR])*(1-dps_[ipSR])

    pses.append(dps_)
    pass


AnInt = np.array(range(0, int(dps[no_cells])+1, 1))
Unit = round(3 * dps[L200Y] / dps[no_cells], 0)
LossAmountMillion: np.ndarray = AnInt * Unit
pencentile = [0.75, 0.9, 0.95, 0.975, 0.99, 0.995]
# st.write(LossAmountMillion.size)
output_df = pd.DataFrame()
# 算出x轴
EP_X = np.zeros(LossAmountMillion.size)

S2 = 1 / 2 * (0.01 + 0.05) * (dps[L100Y] - dps[L20Y])
S3 = 1 / 2 * (0.01 + 0.005) * (dps[L200Y] - dps[L100Y])
S4 = dps[PctAELTail] * dps[AEL]
S1 = dps[AEL] - S2 - S3 - S4
f1 = S1 - dps[L20Y] * 0.05
f2 = f1 / (dps[L0Y] - 0.05)
b = 1 / f2
r = S4 / 0.005

t1 = LossAmountMillion < dps[L20Y]
t2 = LossAmountMillion >= dps[L20Y]
t3 = LossAmountMillion < dps[L100Y]
t4 = LossAmountMillion >= dps[L100Y]
t5 = LossAmountMillion < dps[L200Y]
t6 = LossAmountMillion >= dps[L200Y]
EP_X[t1] = func1(LossAmountMillion[t1], b, dps[L0Y])
EP_X[t2 & t3] = func2(LossAmountMillion[t2 & t3], dps[L20Y], dps[L100Y])
EP_X[t4 & t5] = func3(LossAmountMillion[t4 & t5], dps[L100Y], dps[L200Y])
EP_X[t6] = func4(LossAmountMillion[t6], r, dps[L200Y])
CDF = 1 - EP_X



layering_empty = st.empty()
st.text('')
if survival_empty.checkbox('Show the Exceedance Probablility Curve'):
    st.markdown('### Exceedance Probablility Curve')
    # x1 = np.linspace(0, dps[L20Y])
    # x2 = np.linspace(dps[L20Y], dps[L100Y])
    # x3 = np.linspace(dps[L100Y], dps[L200Y])
    # x4 = np.linspace(dps[L200Y], dps[no_cells])
    # y1 = func1(x1, b)
    # y2 = func2(x2, dps[L20Y], dps[L100Y])
    # y3 = func3(x3, dps[L100Y], dps[L200Y])
    # y4 = func4(x4, r, dps[L200Y])
    # xxxx = np.hstack([x1, x2, x3, x4])
    # st.write(xxxx)
    # yyyy = np.hstack([y1, y2, y3, y4])

    # zip_ = chain(zip(x1, y1), zip(x2, y2), zip(x3, y3),zip(x4, y4))
    # linedata = [list(e) for e in zip_]
    linedata = [list(e) for e in zip(LossAmountMillion, EP_X)]
    line_serie = {
        'name': 'Exceedance Probablility',
        'type': 'line',
        'symbolSize': 0,
        'showSymbol': 'false',
        'data': linedata,
        'lineStyle': {'smooth': 'true'}
    }
    line_options = {
        'title': {'text': ''},
        'xAxis': {'name': 'Loss Amount'},
        'yAxis': {'name': 'Exceedance Probablility', 'scale': 'true'},
        'tooltip': {
            'trigger': 'axis',
            'axisPointer': {
                'type': 'cross'
            }
        },
        'legend': {'data': ['Exceedance Probablility']},
        'dataZoom': [{'show': 'false', 'type': 'slider',}],
        'series': line_serie,
    }
    st_echarts(line_options)

if show_layering_empyt.checkbox('Show the Disaster Risk layering'):
    layering_empty.beta_expander('Disaster Risk Layering').image('Layering.png', width=800, height=494)


RetainedLossWithoutPolicy = LossAmountMillion / dps[natBdt]

series = [{
    'name': 'Without DRFI Strategy',
    'type': 'bar',
    'data': [round(RetainedLossWithoutPolicy[np.argmin(np.abs(CDF-pctile))]*100, 2) for pctile in pencentile]
}]
legend = ['Without DRFI Strategy']

options = {
    'title': {'text': ''},
    'xAxis': {'name': 'Percentile', 'type': 'category', 'data': ['75%', '90%', '95%', '97.5%', '99%', '99.5%']},
    'yAxis': {'name': ' % of National Budget', 'scale': 'true', 'type': 'value'},
    'tooltip': {'trigger': 'axis', 'axisPointer': {'type': 'shadow'}, 'formatter': ''},
    'dataZoom': {'show': 'false', 'type': 'slider', 'xAxisIndex': 0},
    'legend': {'data': []},
    'series': []
}


for ps in pses:
    Limit = ps[inSize]

    RevisedLossRetainedRatio = ps[ipRLLoad]
    PctLossRetained = RevisedLossRetainedRatio
    LossTransfer = 1 - PctLossRetained

    InsurancePayout = (LossAmountMillion - ps[attachment]).clip(0, Limit) * LossTransfer

    Tier1FinancingDollarImpactOnRetainedLoss = ps[tier1_RL]
    Layer1ImpactOnRetainedLoss = np.minimum((LossAmountMillion - ps[attachment]).clip(0, Limit) * PctLossRetained,
                                            Tier1FinancingDollarImpactOnRetainedLoss)
    Tier2FinancingDollarImpactOnRetainedLoss = ps[tier2_RL]
    Layer2ImpactOnRetainedLoss = np.minimum(
        (LossAmountMillion - ps[attachment]).clip(0, Limit) * PctLossRetained - Layer1ImpactOnRetainedLoss,
        Tier2FinancingDollarImpactOnRetainedLoss)

    CatbondSize = ps[cb_limit] - ps[cb_att]
    CatbondRecovery = (LossAmountMillion - ps[cb_att]).clip(0, CatbondSize)

    before_div = LossAmountMillion - sum(
        [InsurancePayout, Layer1ImpactOnRetainedLoss, Layer2ImpactOnRetainedLoss, CatbondRecovery])
    before_div[before_div < 0] = 0
    RetainedLossAsPctOfNationalBudget = before_div / ps[natBdt]

    WT_CDF = np.zeros(CDF.size)
    WT_CDF[CDF!=0] = norm.cdf(norm.ppf(CDF[CDF!=0]) - ps[SharpeRatio])


    TransformedProbability = np.diff(WT_CDF)
    TransformedProbability = np.insert(TransformedProbability, 0, WT_CDF[0])
    InsurancePremium = (TransformedProbability * InsurancePayout).sum()
    InsurancePremiumAsPctNationalBudget = InsurancePremium / ps[natBdt]

    PDF = np.diff(CDF)
    PDF = np.insert(PDF, 0, CDF[0])
    ExpectedLoss = (CatbondRecovery * PDF).sum()
    CatbondAnnualCost = ExpectedLoss * ps[hisMul] * (1 + ps[ipCBLoad]) * (1 + ps[dataCBLoad])
    CatbondCoupon = CatbondAnnualCost
    CatbondCostAsPctNationalBudget = CatbondCoupon / ps[natBdt]

    InsurancePenetrationCostAsPctNationalBudget = ps[ip_Invest]
    DataInfrastractureCostAsPctNationalBudget = ps[data_Invest]

    Layer1BorrowingCost = ps[tier1_Int]
    Layer1CostAsPctNationalBudget = Layer1BorrowingCost / ps[natBdt]
    Layer2BorrowingCost = ps[tier2_Int]
    Layer2CostAsPctNationalBudget = Layer2BorrowingCost / ps[natBdt]

    TotalPolicyCostPctNationalBudget = InsurancePremiumAsPctNationalBudget + CatbondCostAsPctNationalBudget \
                                       + DataInfrastractureCostAsPctNationalBudget + InsurancePenetrationCostAsPctNationalBudget \
                                       + Layer1CostAsPctNationalBudget + Layer2CostAsPctNationalBudget

    VaR_pct_NationalBudget = RetainedLossAsPctOfNationalBudget + TotalPolicyCostPctNationalBudget
    # st.write(InsurancePremiumAsPctNationalBudget, CatbondCostAsPctNationalBudget, DataInfrastractureCostAsPctNationalBudget, InsurancePenetrationCostAsPctNationalBudget, Layer1CostAsPctNationalBudget, Layer2CostAsPctNationalBudget,TotalPolicyCostPctNationalBudget)
    # VaR_pct_NationalBudget[VaR_pct_NationalBudget<0] = 0
    output_df['EP'] = EP_X
    output_df['amt'] = LossAmountMillion
    output_df['without'] = RetainedLossWithoutPolicy
    output_df['wt_cdf'] = WT_CDF
    output_df['transp'] = TransformedProbability
    output_df['insurancepayout'] = InsurancePayout
    output_df['1st rl'] = Layer1ImpactOnRetainedLoss
    output_df['2nd rl'] = Layer2ImpactOnRetainedLoss
    output_df['cat re'] = CatbondRecovery
    output_df['retained loss'] = RetainedLossAsPctOfNationalBudget
    output_df['VaR'] = VaR_pct_NationalBudget
    output_df.to_excel('epamt.xlsx', index=False)

    serie_name = f'DRFI Strategy {n2c[len(series)]}'
    legend.append(serie_name)
    serie = {
        'name': serie_name,
        'type': 'bar',
    }
    serie_data = []
    for pctile in pencentile:
        var = VaR_pct_NationalBudget[np.argmin(np.abs(CDF-pctile))]
        var = round(var*100, 2)
        serie_data.append(var)
    serie['data'] = serie_data
    series.append(serie)

options['series'] = series
options['legend']['data'] = legend

tooltip_formatter = 'Percentile {b}:<br>'
for i in range(len(series)):
    tooltip_formatter += '{a'+str(i)+'}: {c' + str(i) + '}%<br>'
options['tooltip']['formatter'] = tooltip_formatter

st.markdown('### Loss Impact as % of National Budget under Various Scenarios')
st_echarts(options, width='100%', height='400%')


df = pd.DataFrame(dps[user_input])
params_df = df.copy(deep=True)
for pname in pct_params:
    params_df[pname] = params_df[pname].map(lambda x: str(round(x*100, 2))+'%')
rn = copy.deepcopy(show_name)
rn.update(bg_show_name)
params_df.rename(columns=rn, inplace=True)
params_df = pd.DataFrame(params_df.values.T, index=params_df.columns, columns=[f'DRFI Strategy {n2c[i+1]}' for i in params_df.index])
st.markdown('**The Policy Settings**')
st.write(params_df)
export_button = st.empty()
export = st.empty()
if export_button.button('Export the policies'):
    df.to_excel(f'policies/{time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())}.xlsx', index=False)
    export.text('Exported!')
    time.sleep(2)
    export.text('')

