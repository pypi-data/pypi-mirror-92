import numpy as np
import pandas as pd
import os

from svolfit import svolfit
    
dt=1.0/252.0
FILE='test_path.csv'
SERIES='asset'

dir_name = os.path.dirname(__file__)
file_path = os.path.join(dir_name, 'data', FILE)

#TODO: need to test that test data file exists...
series=pd.read_csv(file_path)
series=series[SERIES].to_numpy()
#print(series)

#TODO: test vpath as well...?

models=[]
methods=[]
testpars=[]

cc=0
models.append('Template')
methods.append('tree')
testpars.append(
    {}
    )

cc=1
models.append('GBM')
methods.append('analytic')
testpars.append(
    {'rep_mu': 0.01542585774471747, 'rep_sigma': 0.05512169247825324, 'sim_wrk_mu': 0.016652991518886752, 'sim_wrk_sigma': 0.055184064089833784, 'sim_rep_mu': 0.016652991518886752, 'sim_rep_sigma': 0.055184064089833784, 'misc_theta': 0.00303840098166712, 'misc_v0': 0.00303840098166712, 'misc_vT': 0.00303840098166712, 'misc_GBM_mu': 0.016652991518886752, 'misc_GBM_sigma': 0.055184064089833784}
    )
cc=2
models.append('HestonNandi')
methods.append('v')
testpars.append(
    {'rep_mu': 0.019167046975972598, 'rep_theta': 0.006074114143482877, 'misc_rho': -1.0, 'rep_alpha': 19.999999999999993, 'rep_eta': 0.007793660336121198, 'rep_v0': 0.0060778089007671, 'sim_wrk_mu': 0.016652991518886752, 'sim_wrk_sigma': 0.055184064089833784, 'sim_wrk_alpha': 2.0, 'sim_wrk_xi': 1.0, 'sim_wrk_u0': 1.0, 'sim_rep_mu': 0.016652991518886752, 'sim_rep_theta': 0.0030452809294708827, 'sim_rep_alpha': 2.0, 'sim_rep_eta': 0.055184064089833784, 'sim_rep_v0': 0.0030452809294708827, 'misc_q': 3999.9999999999977, 'misc_vT': 0.006022323697355837}
    )
cc=3
models.append('MertonJD')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.016829262757863787, 'rep_sigma': 0.05133736891858502, 'rep_lambda': 15.34978223934659, 'rep_gamma': -0.0008166762347772405, 'rep_omega': 0.0050492573268496824, 'misc_theta': 0.0026355254474828994, 'misc_v0': 0.0026355254474828994, 'misc_vT': 0.0026355254474828994, 'misc_V': 1.2052007264619928e-05, 'misc_S': -0.09172959477644152, 'misc_S_sig': 0.21821789023599236, 'misc_Kexc': 0.8607092963483204, 'misc_Kexc_sig': 0.8728715609439694, 'misc_JB': 24.396049662132373, 'misc_JBpvalue': 0.9999949595985741, 'sim_wrk_mu': 0.0, 'sim_wrk_s': 0.05514755461571507, 'sim_wrk_lambda': 0.0033289299867899605, 'sim_wrk_r': 0.6289680483856873, 'sim_wrk_phi': 0.0, 'sim_rep_mu': 0.0, 'sim_rep_sigma': 0.04668159147922306, 'sim_rep_lambda': 3.3289299867899604, 'sim_rep_gamma': 0.0, 'sim_rep_omega': 0.016092440308084908}     
    )
cc=4
models.append('PureJump')
methods.append('grid')
testpars.append(
    {'rep_mu': -0.4127115779658027, 'rep_lambda': 504.0, 'rep_gamma': -0.0010562249997286186, 'rep_omega': 0.003131844651102303, 'sim_wrk_mu': 0.0, 'sim_wrk_lambda': 3.3289299867899604, 'sim_wrk_r': 0.055147554615715064, 'sim_wrk_phi': 0.0, 'sim_rep_mu': 0.0, 'sim_rep_lambda': 3.3289299867899604, 'sim_rep_gamma': 0.0, 'sim_rep_omega': 0.030225530274410235}
    )

cc=5
models.append('Heston')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.031598578372465116, 'rep_theta': 0.0031625449896207154, 'rep_rho': 0.3783686034802998, 'rep_alpha': 3.2654036384020606, 'rep_eta': 0.03593784165348757, 'rep_v0': 0.0037384545754480065, 'sim_wrk_mu': 0.016652991518886752, 'sim_wrk_sigma': 0.055184064089833784, 'sim_wrk_rho': 0.0, 'sim_wrk_alpha': 2.0, 'sim_wrk_xi': 1.0, 'sim_wrk_u0': 1.0, 'sim_rep_mu': 0.016652991518886752, 'sim_rep_theta': 0.0030452809294708827, 'sim_rep_rho': 0.0, 'sim_rep_alpha': 2.0, 'sim_rep_eta': 0.055184064089833784, 'sim_rep_v0': 0.0030452809294708827, 'misc_q': 15.99188281772672, 'misc_vT': 0.0029216493740896183}
    )
cc=6
models.append('Heston')
methods.append('tree')
testpars.append(
    {'rep_mu': 0.03055071749984695, 'rep_theta': 0.003132865268790383, 'rep_rho': 0.3607679427218266, 'rep_alpha': 4.233093285968648, 'rep_eta': 0.04028996174265257, 'rep_v0': 0.004270168559368956, 'sim_wrk_mu': 0.016652991518886752, 'sim_wrk_sigma': 0.055184064089833784, 'sim_wrk_rho': 0.0, 'sim_wrk_alpha': 2.0, 'sim_wrk_xi': 1.0, 'sim_wrk_u0': 1.0, 'sim_rep_mu': 0.016652991518886752, 'sim_rep_theta': 0.0030452809294708827, 'sim_rep_rho': 0.0, 'sim_rep_alpha': 2.0, 'sim_rep_eta': 0.055184064089833784, 'sim_rep_v0': 0.0030452809294708827, 'misc_q': 16.33939015419114, 'misc_vT': 0.002914018962491343}
    )
cc=7
models.append('Heston')
methods.append('treeX2')
testpars.append(
    {'rep_mu': 0.03411855836869871, 'rep_theta': 0.003156592911928414, 'rep_rho': 0.48495286998294873, 'rep_alpha': 3.3384898883577567, 'rep_eta': 0.03799206422445619, 'rep_v0': 0.004408771967202047, 'sim_wrk_mu': 0.016652991518886752, 'sim_wrk_sigma': 0.055184064089833784, 'sim_wrk_rho': 0.0, 'sim_wrk_alpha': 2.0, 'sim_wrk_xi': 1.0, 'sim_wrk_u0': 1.0, 'sim_rep_mu': 0.016652991518886752, 'sim_rep_theta': 0.0030452809294708827, 'sim_rep_rho': 0.0, 'sim_rep_alpha': 2.0, 'sim_rep_eta': 0.055184064089833784, 'sim_rep_v0': 0.0030452809294708827, 'misc_q': 14.602017222890494, 'misc_vT': 0.0030085719536116946}
    )

cc=8
models.append('Bates')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.024282093304013447, 'rep_theta': 0.002664553630475097, 'rep_rho': 0.6783076631346147, 'rep_alpha': 3.4734791198936166, 'rep_eta': 0.021015357087713557, 'rep_lambda': 17.395111433042292, 'rep_gamma': -0.0006031371552400282, 'rep_omega': 0.00485860295359551, 'rep_v0': 0.00307076688575078, 'sim_wrk_mu': 0.0, 'sim_wrk_sigma': 0.055184064089833784, 'sim_wrk_rho': 0.0, 'sim_wrk_alpha': 2.0, 'sim_wrk_xi': 1.0, 'sim_wrk_lambda': 0.0033289299867899605, 'sim_wrk_r': 0.05, 'sim_wrk_phi': 0.0, 'sim_wrk_u0': 1.1524507709770713, 'sim_rep_mu': 0.0, 'sim_rep_theta': 0.0030452809294708827, 'sim_rep_rho': 0.0, 'sim_rep_alpha': 2.0, 'sim_rep_eta': 0.055184064089833784, 'sim_rep_lambda': 3.3289299867899604, 'sim_rep_gamma': 0.0, 'sim_rep_omega': 0.001512277027907376, 'sim_rep_v0': 0.003509536355010491, 'misc_q': 41.912696874092596, 'misc_vT': 0.002736008231538955}
    )
cc=9
models.append('Bates')
methods.append('tree')
testpars.append(
    {'rep_mu': 0.01845205014760575, 'rep_theta': 0.002583588513157721, 'rep_rho': 0.6578375609726738, 'rep_alpha': 19.999999999999062, 'rep_eta': 0.02750856349457921, 'rep_lambda': 18.592369872039722, 'rep_gamma': -0.0007444304597282094, 'rep_omega': 0.0049199927596691615, 'rep_v0': 0.0025999976391450543, 'sim_wrk_mu': 0.016652991518886752, 'sim_wrk_sigma': 0.055184064089833784, 'sim_wrk_rho': 0.0, 'sim_wrk_alpha': 2.0, 'sim_wrk_xi': 1.0, 'sim_wrk_lambda': 0.0033289299867899605, 'sim_wrk_r': 0.36242347006994863, 'sim_wrk_phi': 0.0, 'sim_wrk_u0': 1.0, 'sim_rep_mu': 0.016652991518886752, 'sim_rep_theta': 0.0030452809294708827, 'sim_rep_rho': 0.0, 'sim_rep_alpha': 2.0, 'sim_rep_eta': 0.055184064089833784, 'sim_rep_lambda': 3.3289299867899604, 'sim_rep_gamma': 0.0, 'sim_rep_omega': 0.010961693763225196, 'sim_rep_v0': 0.0030452809294708827, 'misc_q': 136.56754811391426, 'misc_vT': 0.002719184815549582}
    )
cc=10
models.append('Bates')
methods.append('treeX2')
testpars.append(
    {'rep_mu': 0.018110536872049852, 'rep_theta': 0.0025000000000000005, 'rep_rho': 0.857612520839358, 'rep_alpha': 20.0, 'rep_eta': 0.02420637987327147, 'rep_lambda': 20.419516249706493, 'rep_gamma': -0.0005244088909793458, 'rep_omega': 0.00488026653665172, 'rep_v0': 0.002507896727784008, 'sim_wrk_mu': 0.0, 'sim_wrk_sigma': 0.055184064089833784, 'sim_wrk_rho': 0.0, 'sim_wrk_alpha': 2.0, 'sim_wrk_xi': 1.0, 'sim_wrk_lambda': 0.0033289299867899605, 'sim_wrk_r': 0.05, 'sim_wrk_phi': 0.0, 'sim_wrk_u0': 1.0, 'sim_rep_mu': 0.0, 'sim_rep_theta': 0.0030452809294708827, 'sim_rep_rho': 0.0, 'sim_rep_alpha': 2.0, 'sim_rep_eta': 0.055184064089833784, 'sim_rep_lambda': 3.3289299867899604, 'sim_rep_gamma': 0.0, 'sim_rep_omega': 0.001512277027907376, 'sim_rep_v0': 0.0030452809294708827, 'misc_q': 170.66336762806606, 'misc_vT': 0.0026699013411632575}
    )

cc=11
models.append('H32')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.035319851283899334, 'rep_theta': 0.0036560879003834364, 'rep_rho': 0.4464775392335281, 'rep_alpha': 567.7257321334562, 'rep_eta': 11.197457987805034, 'rep_v0': 0.00430649913663229, 'sim_wrk_mu': 0.016652991518886752, 'sim_wrk_sigma': 0.055184064089833784, 'sim_wrk_rho': 0.0, 'sim_wrk_alpha': 2.0, 'sim_wrk_xi': 1.0, 'sim_wrk_u0': 1.0, 'sim_rep_mu': 0.016652991518886752, 'sim_rep_theta': 0.006090561858941766, 'sim_rep_rho': 0.0, 'sim_rep_alpha': 328.3769291438573, 'sim_rep_eta': 18.12117350349743, 'sim_rep_v0': 0.0030452809294708827, 'misc_q': 11.055859822435137, 'misc_theta': 333.9229002023523, 'misc_eta': 11.197457987805034, 'misc_vT': 0.0029017053006185484}
    )

cc=12
models.append('B32')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.025513627748892972, 'rep_theta': 0.0026110936592812213, 'rep_rho': 0.6679567450785638, 'rep_alpha': 3.3193819771581485, 'rep_eta': 0.022696792558756767, 'rep_lambda': 17.4191493340028, 'rep_gamma': -0.0005664112916849165, 'rep_omega': 0.004772115602905029, 'rep_v0': 0.0031606837873011918, 'sim_wrk_mu': 0.0, 'sim_wrk_sigma': 0.055184064089833784, 'sim_wrk_rho': 0.0, 'sim_wrk_alpha': 2.0, 'sim_wrk_xi': 1.0, 'sim_wrk_u0': 1.0, 'sim_wrk_lambda': 0.0033289299867899605, 'sim_wrk_r': 0.05, 'sim_wrk_phi': 0.0, 'sim_rep_mu': 0.0, 'sim_rep_theta': 0.0030452809294708827, 'sim_rep_rho': 0.0, 'sim_rep_alpha': 2.0, 'sim_rep_eta': 0.055184064089833784, 'sim_rep_v0': 0.0030452809294708827, 'sim_rep_lambda': 3.3289299867899604, 'sim_rep_gamma': 0.0, 'sim_rep_omega': 0.001512277027907376, 'misc_q': 33.649661571510336, 'misc_vT': 0.0027488371119861878}
    )

cc=13
models.append('GARCHdiff')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.03042537186423229, 'rep_theta': 0.003169068293374862, 'rep_rho': 0.32992493777168147, 'rep_alpha': 3.697982718742663, 'rep_eta': 0.7331282453343007, 'rep_v0': 0.004275322841112933, 'sim_wrk_mu': 0.016652991518886752, 'sim_wrk_sigma': 0.055184064089833784, 'sim_wrk_rho': 0.0, 'sim_wrk_alpha': 2.0, 'sim_wrk_xi': 1.0, 'sim_wrk_u0': 1.0, 'sim_rep_mu': 0.016652991518886752, 'sim_rep_theta': 0.0030452809294708827, 'sim_rep_rho': 0.0, 'sim_rep_alpha': 2.0, 'sim_rep_eta': 1.0, 'sim_rep_v0': 0.0030452809294708827, 'misc_q': 13.760523902903858, 'misc_vT': 0.002897869549584506}
    )

cc=14
models.append('GARCHjdiff')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.022871672353646184, 'rep_theta': 0.0026678379299749496, 'rep_rho': 0.5575597462598441, 'rep_alpha': 4.129647265704092, 'rep_eta': 0.47880681167871697, 'rep_lambda': 17.886706722592717, 'rep_gamma': -0.0005484956367412671, 'rep_omega': 0.0047210537912829535, 'rep_v0': 0.0033599940790542088, 'sim_wrk_mu': 0.0, 'sim_wrk_sigma': 0.055184064089833784, 'sim_wrk_rho': 0.0, 'sim_wrk_alpha': 2.0, 'sim_wrk_xi': 1.0, 'sim_wrk_u0': 1.0, 'sim_wrk_lambda': 0.0033289299867899605, 'sim_wrk_r': 0.05, 'sim_wrk_phi': 0.0, 'sim_rep_mu': 0.0, 'sim_rep_theta': 0.0030452809294708827, 'sim_rep_rho': 0.0, 'sim_rep_alpha': 2.0, 'sim_rep_eta': 1.0, 'sim_rep_lambda': 3.3289299867899604, 'sim_rep_gamma': 0.0, 'sim_rep_omega': 0.001512277027907376, 'sim_rep_v0': 0.0030452809294708827, 'misc_q': 36.026519993518306, 'misc_vT': 0.0027198253558737857}
    )

#for cc in range(0,len(models)):
#for cc in [9]:
#    print(models[cc]+' '+methods[cc])
#    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
#    print(cc,status,message)
#    print(pars)


def compare(testpars,pars):

# a bit subtle -- seems a couple of these (5,8) are not so stable numerically
# 1e-8 is what i've seen as differences between math libraries, leave this here
# and look into the failures at some point...
#TODO: investigate
#    fittol=1.0e-4 # would pass...
    fittol=1.0e-5
    passed=True    
    for x in testpars:
# only compare reporting parmeters so that the testing is less sensitive to output changes
        if(x[0:4]=='rep_'): 
            if( x in pars ):
                if( np.abs(testpars[x]-pars[x]) > fittol ):
                    passed = False
            else:
                passed = False

    return passed

def test_0():
    cc=0
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert not pars

def test_1():
    cc=1
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_2():
    cc=2
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_3():
    cc=3
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_4():
    cc=4
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_5():
    cc=5
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_6():
    cc=6
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_7():
    cc=7
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_8():
    cc=8
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_9():
    cc=9
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_10():
    cc=10
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_11():
    cc=11
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_12():
    cc=12
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_13():
    cc=13
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_14():
    cc=14
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)
