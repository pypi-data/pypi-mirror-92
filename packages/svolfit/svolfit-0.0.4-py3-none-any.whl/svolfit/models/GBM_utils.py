import numpy as np

#-------------------------------------------------

def GBM_lncondassetprob(y,dt,mu,sigma,lncp):

    coeff_dt=(mu-sigma*sigma/2.0)*dt
    coeff_dt=mu*dt
    
    vol_tmp=sigma*np.sqrt(dt)
        
    yy_tmp=np.tile((y-coeff_dt)/vol_tmp,(1,1)).T
    
# log-probs    
    lncp[:,:]=-0.5*yy_tmp*yy_tmp-np.log(vol_tmp)-0.5*np.log(2.0*np.pi)
        
    return 
    
