import streamlit as stimport numpy as npimport pandas as pdfrom manage_db import *import matplotlib.pyplot as pltimport osimport hashlibimport joblibfrom PIL import Imageimport streamlit.components.v1 as componentsmodel = joblib.load("BNK_Model.joblib")features = ['CYCLE', 'AGE','HOME YEARS','BUS YEARS',          'CF TO LOAN','COLL TO LOAN','AMOUNT GRANTED']def generate_hashes(password):    return hashlib.sha256(str.encode(password)).hexdigest()def verify_hashed(password,hashed_text):    if generate_hashes(password) == hashed_text:        return hashed_text    return Falsedef logo():    logo = Image.open('bnk-logo.png')    st.image(logo, height=100, width=100)def predict_default(CYCLE,AGE,HOME_YEARS,BUS_YEARS,CF_TO_LOAN,COLL_TO_LOAN,AMOUNT_GRANTED):    x = np.array([[CYCLE,AGE,HOME_YEARS,BUS_YEARS,CF_TO_LOAN,COLL_TO_LOAN,AMOUNT_GRANTED]])    prediction = model.predict_proba(x)    pred = (prediction[0][0]).astype('float64')    print("Default rate: ",float(pred))    print("Payback rate: ",1-float(pred))    res = round(float(pred),2)    #default rate    return resdef plot_default_payback(output):    plt.style.use('seaborn')    fig = plt.figure(figsize=(12, 5))    label = ['Default', 'Payback']    s = pd.Series([output * 100, (1 - output) * 100])    my_color = ['palevioletred','mediumseagreen']    chart = s.plot.barh(color=my_color)    plt.yticks([0, 1], label)    plt.title('Default rate VS Payback rate')    plt.xlabel("Percentage")    # plt.legend(('Default','Payback'))    plt.xlim(xmax=100, xmin=0)    # plt.legend(loc = 'best')    st.pyplot(fig)def pswd_complex(s):    l = list(s)    bool_numbers = False    bool_letters = False    bool_lower = False    bool_upper = False    bool_symbols = False    for elem in l:        if elem.isdigit():            bool_numbers = True        elif elem.isalpha():            bool_letters = True            if elem.islower():                bool_lower = True            elif elem.isupper():                bool_upper = True        else:            bool_symbols = True    if len(l)<4:        return 0    if bool_numbers and not bool_letters and not bool_symbols:        return 1    if bool_letters and not bool_numbers and not bool_symbols:        return 1    if bool_numbers and bool_letters and (bool_lower or bool_upper) and not bool_symbols:        return 2    if bool_numbers and bool_letters and bool_lower and bool_upper and bool_symbols:        return 3def warn(input):    if pswd_complex(input) == 0:        st.error("Password is too short")    elif pswd_complex(input) == 1:        st.warning("Password is Weak")    elif pswd_complex(input) == 2:        st.info("Password is okay")    else:        st.success("Password is strong")def show():    html_temp = """                <div style="background-color:##A569BD ;padding:10px">                <h2 style="color:purple;text-align:center;">BNK Prediction ML App </h2>                 </div>                """    st.markdown(html_temp, unsafe_allow_html=True)    CYCLE = st.slider("CYCLE",0,72)    AGE = st.slider("AGE",15,100)    HOME_YEARS = st.slider("Years in current home",1,65)    BUS_YEARS = st.slider("Years in business",1,43)    Cashflow = st.slider("Cashflow",0,700000,step = 10000)    Collateral = st.slider("Collateral",0,12800000,step = 10000)    AMOUNT_GRANTED = st.slider("Loan size",0,300000,step = 10000)    if st.button("Predict"):        CF_TO_LOAN = float(Cashflow)/float(AMOUNT_GRANTED)        COLL_TO_LOAN = float(Collateral)/float(AMOUNT_GRANTED)        output= predict_default(CYCLE,AGE,HOME_YEARS,BUS_YEARS,CF_TO_LOAN,COLL_TO_LOAN,AMOUNT_GRANTED)        #st.success("Loan Default Rate: {}".format(str(round(output*100,2))) + '%')        st.success("Loan Payback Rate: {}".format(str(round(100-output*100,2)))+'%')        plot_default_payback(output)        if output >= 0.5:            add_to_result(CYCLE, AGE, HOME_YEARS, BUS_YEARS, Cashflow, Collateral, AMOUNT_GRANTED, output, "further review")            st.subheader("Needs further review ! :red_circle:")            review = Image.open('review.png')            st.image(review,width = 300)        else:            add_to_result(CYCLE, AGE, HOME_YEARS, BUS_YEARS, Cashflow, Collateral, AMOUNT_GRANTED, output, "Recommended")            st.subheader("Recommended ! :white_check_mark:")            recommend = Image.open('recommend.png')            st.image(recommend,width = 300)def main():    #creating user input page    menu = ["Home","Login","Signup"]    submenu = ["Prediction","Plot","Map"]    choice = st.sidebar.selectbox("Menu",menu)    if choice == "Home":        logo()        st.title("Welcome to Beautiful Phillipine :heart_eyes:")        i = 1        for image in os.listdir('image'):            if image != '.DS_Store' and i < 12:                image = Image.open('image/' + f'image{i}.jpg')                i += 1                st.image(image,width = 800,height = 200)    elif choice == "Login":        logo()        st.title("BNK Prediction App")        enter = st.selectbox(        'Would you like to enter your username or email address?',        ('Username', 'Email'))        if enter == "Username":            username = st.text_input("Username")            email = None        if enter == "Email":            email = st.text_input("Email")            username = None        password = st.text_input("Password",type = 'password')        if st.checkbox("Login"):            create_usertable()            create_usertable_prediction()            hashed_pswd = generate_hashes(password)            if not email and username:                result = login_user(username = username,email = None,password =verify_hashed(password,hashed_pswd))            if not username and email:                result = login_user(username = None,email = email,password =verify_hashed(password,hashed_pswd))            if result:                st.success("You have successfully logged in !")                activity = st.selectbox("Task",submenu)                if activity == "Map":                    st.subheader("Data Map")                    components.html(                        """                        <script src='https://api.mapbox.com/mapbox-gl-js/v1.12.0/mapbox-gl.js'></script>                        <link href='https://api.mapbox.com/mapbox-gl-js/v1.12.0/mapbox-gl.css' rel='stylesheet' />                        <div id='map' style='width: 2000px; height: 2000px;'></div>                        <script>                        mapboxgl.accessToken = 'pk.eyJ1IjoibWFyaWFtYW1tYXIiLCJhIjoiY2tkdG9ucGYxMHpicDJxbjl1cWFzeGZhbCJ9.9rcbwhGpByNZnKzlchKFeQ';                        var map = new mapboxgl.Map({                        container: 'map',                        style: 'mapbox://styles/mariamammar/cke9pbdmh3ls819lklyv870ha', // stylesheet location                        center: [122, 15], // starting position [lng, lat]                        zoom: 9 // starting zoom                        });                        </script>""",                        height=700, width=700)                    print('Hello')                if activity == "Plot":                    st.subheader("Data Plot")                    df = pd.read_csv("merged.csv")                    st.dataframe(df)                elif activity == "Prediction":                    show()            else:                st.error("Log in unsuccessful")    elif choice == "Signup":        logo()        st.title("BNK Prediction App")        create_usertable()        new_username = st.text_input("User name")        email = st.text_input("email")        if check_unique(new_username,email) == False:            st.warning("The account has already existed,please try another one!")        else:            new_password = st.text_input("Password",type = 'password')            warn(new_password)            confirm_password = st.text_input("Confirmed Password",type = 'password')            if new_password == confirm_password:                st.success("Password Confirmed")            else:                st.error("Passwords not the same")            bank_code = st.text_input("Bank_Code")            if bank_code == "BNK":                if st.button("Submit"):                    hashed_new_password = generate_hashes(new_password)                    add_username(new_username,hashed_new_password)                    add_user_email(email,hashed_new_password)                    st.success("You have successfully created a new account")                    st.info("Login to Get Started")            else:                st.error("Your bank code is incorrect !")if __name__=='__main__':    main()