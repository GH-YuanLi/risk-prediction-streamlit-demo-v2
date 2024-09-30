# https://github.com/xiaoyw71/BigBooks

import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import calculator
import base64
from streamlit_authenticator.utilities import (CredentialsError,
                                               ForgotError,
                                               Hasher,
                                               LoginError,
                                               RegisterError,
                                               ResetError,
                                               UpdateError)


# hashed_passwords = stauth.Hasher(['abc', 'def']).generate()



def get_base64_of_bin_file(png_file: str) -> str:
    with open(png_file, "rb") as f:
        return base64.b64encode(f.read()).decode()


@st.cache_resource
def build_markup_for_logo(png_file: str, type: str) -> str:
    file_path = get_base64_of_bin_file(png_file)

    if type == "stSidebar":
        return f"""
            <style>
                [data-testid="stSidebar"] {{
                    background-image: url("data:image/logo2;base64,{file_path}");
                    background-repeat: no-repeat;
                    background-size: 80%;
                    padding-top: 110px;
                    background-position: top center;
                    }}
            </style>
            """
    elif type == "stDecoration":
        return f"""
            <style>
                [data-testid="stDecoration"] {{
                    background-image: url("data:image/taibao;base64,{file_path}");
                    background-repeat: repeat;
                    background-size: contain;
                    padding-top: 50px;
                    background-position: top center;
                }}
            </style>
            """

st.markdown(
    build_markup_for_logo("image/taibao.png", "stDecoration"),
    unsafe_allow_html=True,
)


# Loading config file
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# st.image('logo.png')

# st.code(f"""
# Credentials:

# Name: {config['credentials']['usernames']['jsmith']['name']}
# Username: jsmith
# Password: {'abc' if 'pp' not in config['credentials']['usernames']['jsmith'].keys() else config['credentials']['usernames']['jsmith']['pp']}

# Name: {config['credentials']['usernames']['rbriggs']['name']}
# Username: rbriggs
# Password: {'def' if 'pp' not in config['credentials']['usernames']['rbriggs'].keys() else config['credentials']['usernames']['rbriggs']['pp']}
# """
# )

# Creating the authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    #config['pre-authorized']
)

# Creating a login widget
try:
    authenticator.login()
except LoginError as e:
    st.error(e)

if st.session_state["authentication_status"]:
    # authenticator.logout()
    # st.write(f'Welcome *{st.session_state["name"]}*')
    # st.title('Some content')
    # BigBooks.main()
    calculator.main(authenticator = authenticator)
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

