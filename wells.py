import streamlit as st
import matplotlib.pyplot as plt 
import numpy as np 
import pandas as pd
import scipy.special as ssp
pd.options.display.float_format = '{:.5f}'.format

st.beta_set_page_config(page_icon="potable_water")
st.set_option('deprecation.showfileUploaderEncoding', False)


"## **The Problem** ##"
st.markdown("A community is installing a new well in a regionally confined aquifer with a transmissivity of 248.5 m$^2$/day and the storativity of 0.0002. the planned pumping rate is 4088.24 m$^3$/day. There are several nearby wells tapping the same aquifer, and the hydrogeologist in charge needs to know if the new well will cause significant interference with these wells. compute the theoretical drawdown caused by the new well after 30 days of continuous pumping at the distnces of 50, 250, and 1000 meters. _Source: C.W. Fetter, Applied Hydrogeology_")


def user_input():

    st.sidebar.header("The input data")
    Ty = st.sidebar.number_input("Transmissivity (m\u00b2/d):", value =250.0)
    S = st.sidebar.number_input("Storativity:",value=2e-6, format='%e' )
    Q = st.sidebar.number_input("Pumping rate (m\u00b3/d)" , value=4088.24)
    t = st.sidebar.slider("Time (d)", value=30 )


    st.sidebar.text("The Well locations:")
    r1 = st.sidebar.number_input("Location for Well 1 (m):", value=10.0)
    r2 = st.sidebar.number_input("Location for Well 2 (m):", value=100.0 )
    r3 = st.sidebar.number_input("Location for Well 3 (m):", value= 200.0 )

    in_data = {"Transmissivity": Ty, 
    "Storativity": S, 
    "Pumping rate": Q, 
    "Time": t,
    "Location for Well 1": r1,
    "Location for Well 2": r2,
    "Location for Well 3": r3,}
    

    Input = pd.DataFrame(in_data, index=[0])
    return  Input 

df = user_input()

"### Input data ###" 

if st.checkbox("Show input data"):
    st.table(df.T,)
    #st.write(df.T)

def calc_wells(Ty,S,Q,t, r1, r2, r3):
    
    u1= (S*(r1**2))/(4*Ty*t)
    W1=-ssp.expi(u1)
    s1=(Q/(4*np.pi*Ty)*W1)

    u2= (S*(r2**2))/(4*Ty*t)
    W2=-ssp.expi(u2)
    s2=(Q/(4*np.pi*Ty)*W2)

    u3= (S*(r3**2))/(4*Ty*t)
    W3=-ssp.expi(u3)
    s3=(Q/(4*np.pi*Ty)*W3)
    
    res_1 = str("Drawdown for Well 1 at " + str("%d m is %0.2f m " % (r1, s1) ))
    res_2 = str("Drawdown for Well 2 at " + str("%d m is %0.2f m " % (r2, s2) ))
    res_3 = str("Drawdown for Well 3 at " + str("%d m is %0.2f m " % (r3, s3) ))

    res_out = {"Well 1": res_1, "Well 2": res_2, "Well 3": res_3}
    result = pd.DataFrame(res_out, index=[0])

    X = [r1, r2, r3]
    Y = [s1, s2, s3]
    
    if st.checkbox("Show Plot"):
        plt.plot(X, Y, "x--", color= "red")
        plt.xlabel("Well Location (m)")
        plt.ylabel("Drawdown (m)")
        st.pyplot()

    return result

st.subheader("Intresting results")

df_1 = calc_wells(df["Transmissivity"], df["Storativity"], df["Pumping rate"], df["Time"], df["Location for Well 1"], df["Location for Well 2"], df["Location for Well 3"])

st.write(df_1.T)

st.text("") # adding space
    # About
#if st.button("About App"):
 

About = st.sidebar.checkbox("About App")
if About:
    st.sidebar.text("Problem by Ms. Haniedh Mehrdad")
    st.sidebar.text("App created using Streamlit")
else:
    st.sidebar.text(" ")

