import streamlit as st
import numpy as np
import pandas as pd
from manage_db import *
import os
import hashlib
import joblib

model = joblib.load("BNK_Model.joblib")
features = ['CYCLE', 'AGE','HOME YEARS','BUS YEARS',
          'CF TO LOAN','COLL TO LOAN','AMOUNT GRANTED']
def generate_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def verify_hashed(password,hashed_text):
    if generate_hashes(password) == hashed_text:
        return hashed_text
    return False


def predict_default(CYCLE,AGE,HOME_YEARS,BUS_YEARS,CF_TO_LOAN,COLL_TO_LOAN,AMOUNT_GRANTED):
    x = np.array([[CYCLE,AGE,HOME_YEARS,BUS_YEARS,CF_TO_LOAN,COLL_TO_LOAN,AMOUNT_GRANTED]])
    prediction = model.predict_proba(x)
    pred = (prediction[0][0]).astype('float64')
    print("Default rate: ",float(pred))
    print("Payback rate: ",1-float(pred))
    res = round(float(pred),2)
    #default rate
    return res

#print(predict_default(12,23,1,11.5,2.5,10000))

def show():
    html_temp = """
                <div style="background-color:##A569BD ;padding:10px">
                <h2 style="color:purple;text-align:center;">BNK Prediction ML App </h2>
                 </div>
                """
    st.markdown(html_temp, unsafe_allow_html=True)

    CYCLE = st.number_input("CYCLE",1,72)
    AGE = st.number_input("AGE",7,80)
    HOME_YEARS = st.number_input("HOME_YEARS",1,30)
    BUS_YEARS = st.number_input("BUS_YEARS",1,30)
    Cashflow = st.text_input("Cashflow","")
    Collateral = st.text_input("Collateral","")
    AMOUNT_GRANTED = st.text_input("AMOUNT_GRANTED","")

    safe_html="""
      <div style="background-color:#F4D03F;padding:10px >
       <h2 style="color:white;text-align:center;"> It's a safe loan</h2>
       </div>
        """
    danger_html="""
      <div style="background-color:#F08080;padding:10px >
       <h2 style="color:black ;text-align:center;"> It's a risky loan</h2>
       </div>
    """

    second_review_html = """
      <div style="background-color:##7D3C98;padding:10px >
       <h2 style="color:#7D3C98;text-align:center;"> Loan needs second review</h2>
       </div>
    """
    if st.button("Predict"):
        CF_TO_LOAN = float(Cashflow)/float(AMOUNT_GRANTED)
        COLL_TO_LOAN = float(Collateral)/float(AMOUNT_GRANTED)
        output= predict_default(CYCLE,AGE,HOME_YEARS,BUS_YEARS,CF_TO_LOAN,COLL_TO_LOAN,AMOUNT_GRANTED)
        st.success("The probability of loan default is {},\
            The probability of payback rate is {}".format(output,round(1-output,2)))

        if output > 0.52:
            st.markdown(danger_html,unsafe_allow_html=True)
        elif output <0.48:
            st.markdown(safe_html,unsafe_allow_html=True)
        else:
            st.markdown(second_review_html,unsafe_allow_html = True)

def main():
    st.title("BNK Prediction App")
    #creating user input page
    menu = ["Home","Login","Signup"]
    submenu = ["Prediction","Plot","Map"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        st.subheader("Home")
        st.text("Welcome to Home")

    elif choice == "Login":
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password",type = 'password')

        if st.checkbox("Login"):
            create_usertable()
            hashed_pswd = generate_hashes(password)
            if not email and username:
                result = login_user(username = username,email = None,password =verify_hashed(password,hashed_pswd))
            if not username and email:
                result = login_user(username = None,email = email,password =verify_hashed(password,hashed_pswd))

            if result:
                st.success("You have successfully logged in !")
                activity = st.selectbox("Task",submenu)

                if activity == "Map":
                    st.subheader("Data Map")
                    df2 = pd.DataFrame(\
                    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
                    columns=['lat', 'lon'])

                    st.map(df2)
                if activity == "Plot":
                    st.subheader("Data Plot")
                    df = pd.read_csv("merged.csv")
                    st.dataframe(df)

                    if st.checkbox("Area Chart"):
                        all_columns = df.columns.tolist()
                        feat_choices = st.multiselect("Choose a feature",all_columns)
                        new_df = df[feat_choices]
                        st.area_chart(new_df)
                elif activity == "Prediction":
                    show()
            else:
                st.warning("Log in unsuccessful")

    elif choice == "Signup":
        create_usertable()
        new_username = st.text_input("User name")
        email = st.text_input("email")

        if check_unique(new_username,email) == False:
            st.warning("The account has already existed,please try another one!")
        else:
            new_password = st.text_input("Password",type = 'password')
            confirm_password = st.text_input("Confirmed Password",type = 'password')
            if new_password == confirm_password:
                st.success("Password Confirmed")
            else:
                st.warning("Passwords not the same")
            bank_code = st.text_input("Bank_Code")
            if bank_code == "BNK":
                if st.button("Submit"):
                    hashed_new_password = generate_hashes(new_password)
                    add_username(new_username,hashed_new_password)
                    add_user_email(email,hashed_new_password)
                    st.success("You have successfully created a new account")
                    st.info("Login to Get Started")
            else:
                st.warning("Your bank code is incorrect !")

if __name__=='__main__':
    main()



