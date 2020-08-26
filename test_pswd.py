def pswd_complex(s):
    l = list(s)
    bool_numbers = False
    bool_letters = False
    bool_lower = False
    bool_upper = False
    bool_symbols = False
    for elem in l:
        if elem.isdigit():
            bool_numbers = True
        elif elem.isalpha():
            bool_letters = True
            if elem.islower():
                bool_lower = True
            elif elem.isupper():
                bool_upper = True
        else:
            bool_symbols = True
    if len(l)<4:
        return 0
    if bool_numbers and not bool_letters and not bool_symbols:
        return 1
    if bool_letters and not bool_numbers and not bool_symbols:
        return 1
    if bool_numbers and bool_letters and (bool_lower or bool_upper) and not bool_symbols:
        return 2
    if bool_numbers and bool_letters and bool_lower and bool_upper and bool_symbols:
        return 3


    if pswd_complex(input) == 0:
        html_too_short = """
                    <div style="background-color:#FF5733 ;padding:10px">
                    <h2 style="color:#FF5733;text-align:center;">Your password is too short </h2>
                     </div>
                    """
        st.markdown(html_too_short,unsafe_allow_html=True)
    elif pswd_complex(input) == 1:
        html_weak = """
                    <div style="background-color:#FF5722 ;padding:10px">
                    <h2 style="color:#FF5722;text-align:center;">Weak Password </h2>
                     </div>
                    """
        st.markdown(html_weak,unsafe_allow_html=True)
    elif pswd_complex(input) == 2:
        html_medium = """
                    <div style="background-color:#2196F3 ;padding:10px">
                    <h2 style="color:#2196F3;text-align:center;">Medium Password </h2>
                     </div>
                    """
        st.markdown(html_medium, unsafe_allow_html=True)
    elif pswd_complex(input) == 3:
        html_strong = """
                    <div style="background-color:#689F38 ;padding:10px">
                    <h2 style="color:#689F38;text-align:center;">Strong Password </h2>
                     </div>
                    """
        st.markdown(html_strong, unsafe_allow_html=True)
