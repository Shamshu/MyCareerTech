# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 09:38:25 2023

@author: shamshu
"""

import streamlit as st
import pickle
import pandas as ps 
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    st.title("Shortify for MyCareerTech")
    
    total_number_of_questions = 7
    st.sidebar.title("Welcome Jeremy & Brian")
    
    q_indus = st.sidebar.selectbox(
        'choose a video',
        ('Adaptability','Creativity',
          "Teamwork"))
    
    if(st.sidebar.button("Get my shorts")):
        #scores_for_q1
        if(q_indus == 'Adaptability'):
            with open('Adaptability.pickle', 'rb') as handle:
                data_dic = ps.read_pickle(handle)
        elif(q_indus == 'Creativity'):
            with open('CreativityInnovation.pickle', 'rb') as handle:
                data_dic = ps.read_pickle(handle)
        else:
            with open('Teamwork.pickle', 'rb') as handle:
                data_dic = ps.read_pickle(handle)
            
        vid_files = data_dic['files']
        df = data_dic['words_per_min']
        
        vi, vid1, vid2, vid3 = st.tabs(["Video Insights","Short Video 1","Short Video 2","Short Video 3"])
        
        with vi:
            st.subheader("Video Title: "+q_indus)
            display_score = data_dic['total_mins']
            org_string = "Total Minutes"
            st.metric(label=org_string, value=display_score)
            st.subheader("Key Topics Discussed")
            topics = data_dic['topics']
            stri = ""
            for top in topics:
                stri = stri+"#"+top
                stri = stri +", "
            
            def create_wordcloud(topic):
                wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(topic)
                return wordcloud
            
            wordcloud = create_wordcloud(stri)
            fig, ax = plt.subplots(figsize = (12, 8))
            ax.imshow(wordcloud)
            plt.axis("off")
            st.pyplot(fig)
            st.caption(stri)
            
            st.subheader("Discussion Trend")
            st.bar_chart(df)
            
            # st.subheader("Key Questions")
            # st.text(data_dic['questions'])
            
            
        with vid1:
            fl1 = vid_files[0]
            video_file = open(fl1, 'rb')
            video_bytes1 = video_file.read()
            st.video(video_bytes1)
            dvid_name = q_indus[0:10]+"_1.mp4"
            st.download_button("Download Short", data = video_bytes1,file_name=dvid_name,mime="application/octet-stream")
        with vid2:
            fl2 = vid_files[1]
            video_file = open(fl2, 'rb')
            video_bytes2 = video_file.read()
            st.video(video_bytes2)
            dvid_name = q_indus[0:10]+"_2.mp4"
            st.download_button("Download Short", data = video_bytes2,file_name=dvid_name,mime="application/octet-stream")
        with vid3:
            fl2 = vid_files[2]
            video_file = open(fl2, 'rb')
            video_bytes3 = video_file.read()
            st.video(video_bytes3)
            dvid_name = q_indus[0:10]+"_3.mp4"
            st.download_button("Download Short", data = video_bytes3,file_name=dvid_name,mime="application/octet-stream")
    
