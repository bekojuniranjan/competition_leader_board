import streamlit as st
import json
from models import Score
from db import Database
import pandas as pd
import config


database = Database()


with st.sidebar:
    team_name = st.text_input('Team Name')
    submission_json = st.file_uploader(
        "Upload your submission file(.json)",
        type='json',
        key="File uploader for result file submission"
    )

    if st.button("Submit"):
        if team_name:
            if submission_json:
                with st.spinner("Uploading your submission"):
                    st.markdown(f"The Result of Team: **{team_name}**")
                    result = json.load(submission_json)
                    st.write(result)
                    result['team_name'] = team_name
                    pydantic_data = Score.parse_obj(result)
                    database.insert_row(pydantic_data)

                    
            else:
                st.error("Please upload a submission json file")
        else:
            st.error("Please add the team name")


result_display, leader_board = st.tabs(['Results', "Leader Board"])

with result_display:
    all_data = database.get_all_employees()
    df = pd.DataFrame(all_data)
    df = df.iloc[:,1:].set_index('team_name')
    df.rename(columns={'CrossEntropyLoss': 'cross_entropy_loss'}, inplace=True)
    st.write(df)

    st.markdown("#### Accuracy Score")
    st.bar_chart(df[['accuracy_score']])

    st.markdown("#### Precision Score")
    st.bar_chart(df[['precision_score']])

    st.markdown("#### Recall Score")
    st.bar_chart(df[['recall_score']])


    st.markdown("#### F1 Score")
    st.bar_chart(df[['f1_score']])

    st.markdown("#### ROC AUC Score")
    st.bar_chart(df[['roc_auc_score']])

    st.markdown("#### Cross Entropy Loss")
    st.bar_chart(df[['cross_entropy_loss']])

    st.markdown("#### Inference Time")
    st.bar_chart(df[['inference_time']])

    st.markdown("#### No. of Model Parameters")
    st.bar_chart(df[['model_parameters_count']])

    if st.button("Calculate Score"):
        if 'calculate_score' not in st.session_state:
            st.session_state['calculate_score'] = True


with leader_board:
    if 'calculate_score' in st.session_state and st.session_state['calculate_score']:
        st.write(df)
        ranked_df = pd.DataFrame()
        ranked_df['accuracy_rank'] = df['accuracy_score'].rank(ascending=False, method='min')
        ranked_df['precision_rank'] = df['precision_score'].rank(ascending=False, method='min')
        ranked_df['recall_rank'] = df['recall_score'].rank(ascending=False, method='min')
        ranked_df['f1_rank'] = df['f1_score'].rank(ascending=False, method='min')
        ranked_df['roc_auc_rank'] = df['roc_auc_score'].rank(ascending=False, method='min')
        ranked_df['crossentropy_rank'] = df['cross_entropy_loss'].rank(ascending=True, method='min')
        ranked_df['inference_time_rank'] = df['inference_time'].rank(ascending=True, method='min')
        ranked_df['model_parameters_rank'] = df['model_parameters_count'].rank(ascending=True, method='min')
        ranked_df.index = df.index
        st.write(ranked_df)

        score_df = ranked_df.applymap(lambda x: config.score_from_rank.get(x, 0))
        st.write(score_df)

        # if 'show_columns' in st.session_state:
        #     for i in range(st.session_state['show_columns']):
        #         st.markdown(f'#### {df.columns[i].replace("_", " ").title()}')
        #         st.bar_chart(df[df.columns[i]], y_label=score_df[score_df.columns[i]])

        st.bar_chart(score_df)


        total_score = score_df.sum(axis=1)
        total_score.name = "Final Score"
        total_score = total_score.to_frame()
        total_score['Rank'] = total_score['Final Score'].rank(ascending=False, method='min')
        total_score.sort_values(by='Rank',inplace=True)
        st.write(total_score)


        # if st.button("Show Next Column"):
        #     if 'show_columns' not in st.session_state:
        #         st.session_state['show_columns'] = 1
        #     else: 
        #         st.session_state['show_columns'] += 1
    else:
        st.write("Please upload Submission File for all the Participants and click on calculate score")