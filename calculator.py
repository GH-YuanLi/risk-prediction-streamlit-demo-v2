import streamlit as st
import numpy as np
import pandas as pd
from time import sleep
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
# from stqdm import stqdm
import random
import base64
# from state import provide_state
 

def main(authenticator):
    # st.set_page_config(layout="wide")

    # # Custom HTML/CSS for the banner
    # custom_html = """
    # <div class="banner">
    #     <img src="https://img.freepik.com/premium-photo/wide-banner-with-many-random-square-hexagons-charcoal-dark-black-color_105589-1820.jpg" alt="Banner Image">
    #     <img src="E:/Workspace/Graph_xml/nxgraph/nxgraphpy/static/img/taibao.png" alt="Banner Image">
    # </div>
    # <style>
    #     .banner {
    #         width: 160%;
    #         height: 200px;
    #         overflow: hidden;
    #     }
    #     .banner img {
    #         width: 100%;
    #         object-fit: cover;
    #     }
    # </style>
    # """
    # # Display the custom HTML
    # st.components.v1.html(custom_html)


    # JS code to modify te decoration on top
    # st.components.v1.html(
    #     """
    #     <script>
    #     // Modify the decoration on top to reuse as a banner

    #     // Locate elements
    #     var decoration = window.parent.document.querySelectorAll('[data-testid="stDecoration"]')[0];
    #     var sidebar = window.parent.document.querySelectorAll('[data-testid="stSidebar"]')[0];

    #     // Observe sidebar size
    #     function outputsize() {
    #         decoration.style.left = `${sidebar.offsetWidth}px`;
    #     }

    #     new ResizeObserver(outputsize).observe(sidebar);

    #     // Adjust sizes
    #     outputsize();
    #     decoration.style.height = "2.5rem";
    #     decoration.style.right = "45px";

    #     // Adjust image decorations
    #     decoration.style.backgroundImage = "loadImg(E:/Workspace/development/img/logo.png)";
    #     decoration.style.backgroundSize = "contain";
    #     </script>        
    #     """, width=0, height=0)




    # st.logo(image='./img/logo2.png', link=None, icon_image=None)
    # st.html("""
    #         <style>
    #             [alt=Logo] {
    #             height: 7rem;
    #             }
    #         </style>
    #         """
    #         )


    # sidebar and decorator logo
    # st.markdown(
    #         f"""
    #             <style>
    #                 [data-testid="stDecoration"] {{
    #                     background-image: url("https://amymhaddad.s3.amazonaws.com/morocco-blue.png");
    #                     background-repeat: repeat;
    #                     padding-top: 80px;
    #                     background-position: 20px 20px;
    #                 }}
                    
    #                 [data-testid="stSidebar"] {{
    #                     background-image: url('./img/logo2.png');
    #                     background-repeat: no-repeat;
    #                     padding-top: 80px;
    #                     background-position: top center;
    #                 }}
    #             </style>
    #             """,
    #         unsafe_allow_html=True,
    #     )
    
    # -------------------------------------------------------------------------------------------------

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
        build_markup_for_logo("image/logo1.png", "stSidebar"),
        unsafe_allow_html=True,
    )

    st.markdown(
        build_markup_for_logo("image/taibao.png", "stDecoration"),
        unsafe_allow_html=True,
    )



    st.subheader("肺结节首年患癌风险概率预测", divider=False)

    # creates a horizontal line
    st.write("---")

    st.markdown("* **投保人信息**")




    def show():
        """Shows the sidebar components for the template and returns user inputs as dict."""
        
        # `show()` is the only method required in this module. You can add any other code 
        # you like above or below. 
        
        inputs = {}  # dict to store all user inputs until return
        
        with st.sidebar:
            
            # # Render all template-specific sidebar components here. 

            # # Use ## to denote sections. Common sections for training templates: 
            # # Model, Input data, Preprocessing, Training, Visualizations
            # st.write("## Model")
            
            # # Store all user inputs in the `inputs` dict. This will be passed to the code
            # # template later.
            # inputs["model"] = st.selectbox("Which model?", ["Top model", "Role model"])
            # st.write("You should probably finish this... ;)")
            
            authenticator.logout()

            st.subheader('填写投保人信息', divider = False)
            st.write("---")


            # input 1
            # st.write("性别")
            # ft2 = st.radio("Select an operation to perform:", ("男", "女"))
            inputs['sex'] = st.selectbox('投保人性别', ("", "男", "女"))
                    
            # input 2
            # inputs['age'] = st.number_input(label="投保人年龄", min_value=1, max_value=150, value = None)
            inputs['age'] = st.select_slider('投保人年龄',options=range(18, 81))
            

            # state.inputs = state.inputs or set()
            # input_string = st.text_input("Give inputs")
            # state.inputs.add(input_string)
            # st.selectbox("Select Dynamic", options=list(state.inputs))

            # input 3
            col1, col2 = st.columns([2, 1])

            with col2:
                inputs['nodule_unit'] = st.selectbox('', ("mm", "cm"))
            with col1:
                if inputs['nodule_unit'] == 'mm':
                    inputs['nodule_size'] = st.number_input(label="肺结节长径", min_value=0.00, max_value=15.00, value = None, format="%.2f")
                if inputs['nodule_unit'] == 'cm':
                    inputs['nodule_size'] = st.number_input(label="肺结节长径", min_value=0.000, max_value=1.500, value = None, format="%.3f")

            # input 4
            # st.write("肺结节形态")
            # ft4 = st.radio("Select an operation to perform:", ("实性", "纯磨玻璃", "部分实性"))
            inputs['nodule_type'] = st.selectbox('肺结节形态', ("", "实性", "纯磨玻璃", "部分实性"))

            # input 5
            # st.write("肺结节发生位置")
            # ft5 = st.radio("Select an operation to perform:", ("上肺", "下肺", "右肺中叶"))
            inputs['nodule_position'] = st.selectbox('肺结节发生位置', ("", "上叶", "中叶", "下叶"))

            # input 6
            # st.write("结节是否存在恶性指征")
            # ft6 = st.radio("Select an operation to perform:", ("是", "否"))
            # nodule_malignent = st.selectbox('结节是否存在恶性指征', ("是", "否"))
            inputs['nodule_malignent'] = st.checkbox("结节存在恶性指征", False)

            
        return inputs


    # To test the sidebar independent of the app or template, just run 
    # `streamlit run sidebar.py` from within this folder.

    inputs = show()

    if inputs['nodule_size'] == None:
        size_show = inputs['nodule_unit']
    else:
        size_show = '{}{}'.format(inputs['nodule_size'], inputs['nodule_unit'])


    if inputs['nodule_malignent'] == True:
        nodule_mali = '是'
    else:
        nodule_mali = '否'



    df = pd.DataFrame(
        {
            "投保人年龄": [inputs['age']],
            "投保人性别": [inputs['sex']],
            "结节大小": [size_show],
            "结节形态": [inputs['nodule_type']],
            "结节位置":[inputs['nodule_position']],
            "结节恶性指征":[nodule_mali]
        }
    )
    st.dataframe(
        df,
        width=800,
        column_config={
            "投保人年龄": "投保人年龄",
            "投保人年龄": "投保人年龄",
            "结节大小": "结节大小",
            "结节形态": "结节形态",
            "结节位置": "结节位置",
            "结节恶性指征": "结节恶性指征"
        },
        hide_index=True,
    )




    st.markdown("* **投保人肺癌风险预测**")

    ratio = 0

    def calculate(inputs = inputs):

        assert inputs['sex'] in ['男','女'], st.error('请选择有效的患者性别！')
        # assert inputs['age'] != None and inputs['age'] >= 18 and inputs['age'] <= 80, st.error('请输入有效的患者年龄！')
        # assert inputs['nodule_size'] != None and inputs['nodule_size'] > 0 and inputs['nodule_size'] <= 30, st.error('请输入有效的结节大小！')
        assert inputs['nodule_type'] in ['实性','纯磨玻璃','部分实性'], st.error('请选择有效的结节形态！')
        assert inputs['nodule_position'] in ['上叶','下叶','中叶'], st.error('请选择有效的结节发生位置！')

        
        if inputs['nodule_unit'] == 'mm':
            size_value = inputs['nodule_size']
        else:
            size_value = inputs['nodule_size'] * 10

        sex_value = 0.6011 if inputs['sex'] == '女' else 0

        mali_value = 0.7729 if inputs['nodule_malignent'] == True else 0

        if inputs['nodule_type'] == '实性':
            type_value = 0
        elif inputs['nodule_type'] == '纯磨玻璃':
            type_value = -0.1276
        else:        
            type_value = 0.377

        if inputs['nodule_position'] == '上叶':
            position_value = 0.6581
        elif inputs['nodule_position'] == '下叶':
            position_value = 0
        elif inputs['nodule_position'] == '中叶':        
            position_value = -0.132

        # if ft2 == "Add":
        #     ans = num1 + num2
        # elif operation == "Subtract":
        #     ans = num1 - num2
        # elif operation == "Multiply":
        #     ans = num1 * num2
        # elif operation=="Divide" and num2!=0:
        #     ans = num1 / num2
        # else:
        #     st.warning("Division by 0 error. Please enter a non-zero number.")
        #     ans = "Not defined"

        Family_History_Lung_Ca = 0
        Emphysema = 0
        Nodule_count = 1

        log_odds = (0.0287 * (inputs['age'] - 62)) + sex_value + Family_History_Lung_Ca + Emphysema - (5.3854 * ((size_value/10)**(-0.5) - 1.58113883)) + type_value + position_value + mali_value - 6.7892 - (0.0824 * (Nodule_count - 4))
        
        ratio = (np.exp(log_odds) / (1 + np.exp(log_odds)))


            
        # for _ in stqdm(range(20), st_container=st.sidebar):
        #     sleep(0.5)

        intro_lst = ['2024 中国专家共识','2023 NCCN指南','2018 ACCP指南','2017 Fleischner指南','2016 亚洲共识指南','Brock 预测模型','自研肺癌风险预测模型']
        bar_lst = [0.5, 1.5, 1, 0.5, 2, 3, 2]

        # pbar = stqdm(range(len(intro_lst)))
        # for x in pbar:
        #     sleep(bar_lst[x])
        #     pbar.set_description('指南和模型分析完成')
        #     st.info('【{}】结果分析完成'.format(intro_lst[x]))
            


        with st.status("模型结果分析..."):
            for i in range(len(intro_lst)):
                st.write("【{}】结果分析完成".format(intro_lst[i]))
                sleep(bar_lst[i])
        

        progress_text = "模型结果整合中..."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            sleep(0.01)
            my_bar.progress(percent_complete + 1, text='模型结果整合完成 {:.0%}'.format((percent_complete + 1)/100))
        sleep(1)
        # my_bar.empty()

        # with st.spinner(progress_text):
        #     sleep(5)


        st.success("【最终预测结果】：该投保人首年患肺癌风险的概率 = {:.2%}".format(ratio))



    if st.button("Calculate result"):
        calculate()



if __name__ == "__main__":
    main(authenticator)