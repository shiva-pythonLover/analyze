# -*-coding: utf-8 -*-
import copy

tier1_UL = 'tier1_UL'
tier2_UL = 'tier2_UL'
tier3_UL = 'tier3_UL'
cb_att = 'cb_att'
cb_limit = 'cb_limit'

tier1_AMT = 'tier1_AMT'
tier2_AMT = 'tier2_AMT'
cb_AMT = 'cb_AMT'

tier1_BenRate = 'tier1_BenRate'
tier1_RL = 'tier1_RL'
tier1_IntRate = 'tier1_IntRate'
tier1_Int = 'tier1_Int'

tier2_BenRate = 'tier2_BenRate'
tier2_RL = 'tier2_RL'
tier2_IntRate = 'tier2_IntRate'
tier2_Int = 'tier2_Int'

data_Invest = 'data_Invest'
dataSR_ImpRatio = 'dataSR_ImpRatio'
dataSR = 'dataSR'
dataSR_Cap = 'dataSR_Cap'

dataCBLoad_Base = 'dataCBLoad_Base'
dataCBLoad_ImpRatio = 'dataCBLoad_ImpRatio'
dataCBLoad = 'dataCBLoad'

ip_Invest = 'ip_Invest'
ipSR_ImpRate = 'ipSR_ImpRate'
ipSR = 'ipSR'
ipSR_Cap = 'ipSR_Cap'

ipCBLoad_Base = 'ipCBLoad_Base'
ipCBLoad_ImpRatio = 'ipCBLoad_ImpRatio'
ipCBLoad = 'ipCBLoad'

ipRLLoad_Base = 'ipRLLoad_Base'
ipRLLoad_ImpRatio = 'ipRLLoad_ImpRatio'
ipRLLoad = 'ipRLLoad'
ipRLLoad_ImpRatio_Cap = 'ipRLLoad_ImpRatio_Cap'

inSize_Base = 'inSize_Base'
inSize_ImpRatio = 'inSize_ImpRatio'
inSize = 'inSize'
inSize_ImpRatio_Cap = 'inSize_ImpRatio_Cap'

AEL = 'AEL'
PctAELTail = 'PctAELTail'
L200Y = 'L200Y'
L100Y = 'L100Y'
L20Y = 'L20Y'
L0Y = 'L0Y'
SharpeRatioBaseline = 'SharpeRatioBaseline'
SharpeRatio = 'SharpeRatio'
no_cells = 'no_cells'
unit = 'unit'
hisMul = 'hisMul'

natBdt = 'natBdt'  # National Budget

attachment = 'attachment'


user_input = 'user_input'
bg_input = 'bg_input'

show_name = {
    tier1_UL: ' Tier 1: Low Risk Layer ',
    tier1_AMT: 'Tier 1 Financing Amount',
    tier2_UL: ' Tier 2: Medium Risk Layer ',
    tier2_AMT: 'Tier 2 Financing Amount',
    tier3_UL: ' Tier 3: High Risk Layer ',

    cb_att: ' Cat Bond Attachment ',
    cb_limit: ' Cat Bond Limit ',

    data_Invest: ' Investment on Data Infrastructure as % National Budget ',

    ip_Invest: ' Investment to improve insurance penetration as % National Budget ',


    SharpeRatioBaseline: 'Sharpe Ratio Baseline'
}

bg_show_name = {
    # tier1_AMT: 'tier1amt',
    # tier2_AMT: 'tier2amt',
    # SharpeRatio: 'sr'
}

pct_params = [data_Invest, ip_Invest]

dps = {
    user_input: [{
        tier1_UL: 50.0,
        tier1_AMT: 10.0,
        tier2_UL: 100.0,
        tier2_AMT: 10.0,
        tier3_UL: 600.0,
        cb_att: 200.00,
        cb_limit: 250.0,
        data_Invest: 0.001,
        ip_Invest: 0.001,
        SharpeRatioBaseline: 0.6
    }],

    bg_input: [{}],

    tier1_BenRate: 0.5,
    tier1_IntRate: 0.08,

    tier2_BenRate: 0.4,
    tier2_IntRate: 0.05,

    dataSR_ImpRatio: 100.0,
    dataSR_Cap: 0.4,

    dataCBLoad_Base: 0.5,
    dataCBLoad_ImpRatio: 200.0,

    ipSR_ImpRate: 200.0,
    ipSR_Cap: 0.4,

    ipCBLoad_Base: 0.4,
    ipCBLoad_ImpRatio: 200.0,

    ipRLLoad_Base: 0.5,
    ipRLLoad_ImpRatio: 300.0,
    ipRLLoad_ImpRatio_Cap: 0.6,

    inSize_Base: 200.0,
    inSize_ImpRatio: 300.0,
    inSize_ImpRatio_Cap: 1.0,

    PctAELTail: 0.02,
    L200Y: 1020.6,
    L100Y: 875.3,
    L20Y: 342.6,
    L0Y: 0.3,
    AEL: 52.3,
    no_cells: 500.0,
    hisMul: 2.98,

    attachment: 0.0,
    natBdt: 1452.0

}

dps_original = copy.deepcopy(dps)

input_pct = [data_Invest, ip_Invest]
