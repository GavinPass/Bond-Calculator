import numpy as np

def PV_CF(N,rate,FV,coupon,maturity):
    # return a list of present value of cash flow
    PMT=coupon/100*FV/N
    p_yield=rate/N/100
    result=[]
    for i in range(N*maturity):
        if i+1<N*maturity:
            CF=PMT
        else:
            CF=PMT+FV
        result.append(CF/(1+p_yield)**(i+1))
    return result

def MacDuration(N,rate,FV,coupon,maturity):
    cashflow=PV_CF(N,rate,FV,coupon,maturity)
    pv=np.sum(cashflow)
    duration=[]
    for i in range(N*maturity):
        duration.append(cashflow[i]*(i+1)/2/pv)
    Mac_D=np.sum(duration)
    return Mac_D

def convexity(N,rate,FV,coupon,maturity):
    cashflow=PV_CF(N,rate,FV,coupon,maturity)
    pv=np.sum(cashflow)
    con=[]
    for i in range(N*maturity):
        con.append(cashflow[i]*(i+1)*(i+2))
    
    result=1/(pv*(1+rate/N/100)**2)*np.sum(con)
    return "{:.3f}".format(result) 

def fDerivative(N,rate,FV,coupon,maturity):
    PMT=coupon/100*FV/N
    p_yield=rate/N/100
    result=[]
    for i in range(N*maturity):
        if i+1<N*maturity:
            CF=PMT
        else:
            CF=PMT+FV
        result.append((-i-1)*CF/(1+p_yield)**(i+2))
    return result

def Newton_ytm(N,FV,coupon,maturity,PV,y_init,iterations,precision):
    y_input=y_init
    for i in range(iterations):
        market_value_diff=np.sum(PV_CF(N,y_input,FV,coupon,maturity))-PV
        market_value_deriv=np.sum(fDerivative(N,y_input,FV,coupon,maturity))
        if abs(market_value_diff)<precision:
            return y_input
        else:
            y_input=y_input-(market_value_diff/market_value_deriv)
    return y_input
