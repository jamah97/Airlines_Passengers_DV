import streamlit as st
import plotly.figure_factory as ff
import numpy as np
import pandas as pd
from numpy import percentile
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
from matplotlib import pyplot
import seaborn as sns
st.set_option('deprecation.showPyplotGlobalUse', False)

def main():
    df = pd.read_csv('https://raw.githubusercontent.com/jamah97/Airlines_Passengers_DV/main/airline_passenger_satisfaction.csv')
    df = df.dropna(inplace=True)
    df = df.drop(['ID'], axis=1)
    df2 = df[['Gender', 'Customer Type', 'Type of Travel', 'Class',
       'Departure and Arrival Time Convenience', 'Ease of Online Booking',
       'Check-in Service', 'Online Boarding',
       'On-board Service', 'Seat Comfort', 'Leg Room Service', 'Cleanliness',
       'Food and Drink', 'In-flight Service', 'In-flight Wifi Service',
       'In-flight Entertainment', 'Baggage Handling']]

    df4 = df[['Departure and Arrival Time Convenience', 'Ease of Online Booking',
       'Check-in Service', 'Online Boarding',
       'On-board Service', 'Seat Comfort', 'Leg Room Service', 'Cleanliness',
       'Food and Drink', 'In-flight Service', 'In-flight Wifi Service',
       'In-flight Entertainment', 'Baggage Handling']]

    outliner_check = df[['Age', 'Flight Distance', 'Departure Delay', 'Arrival Delay']]

    st.subheader('Table of Content')
    st.write('1. About the data')
    st.write('2. Outlier Detection & Removal')
    st.write('3. Visualizing Customer Experience & Categorical Distribution')
    st.write('4. Correlation heatmap of Customer Experience')

    st.subheader('About dataset:')
    st.write("""
    The dataset consist of 120,000+ airlines passengers overall experience in their travel. There are several metrics analyzing overall customer experience. The list of features are:
    - Gender (Binary: Male or Female),
    - Age (Discrete value)
    - Type of customer (Binary: Returning or First-time),
    - Type of travel (Binary: Business or Personal),
    - Class (Categorical: Business, Economy, Economy Plus),
    - Flight Distance (Continuous value),
    - Departure Delay (Continuous value),
    - Arrival Delay (Continuous value),
    - Departure and Arrival Time Convenience (Categorical: 0 to 5 rating),
    - Ease of Online Booking (Categorical: 0 to 5 rating),
    - Check-in Service (Categorical: 0 to 5 rating),
    - Online Boarding (Categorical :0 to 5 rating),
    - Gate Location (Categorical: 0 to 5),
    - On-board Service (Categorical: 0 to 5 rating),
    - Seat Comfort (Categorical: 0 to 5 rating),
    - Leg Room Service (Categorical: 0 to 5 rating),
    - Cleanliness (Categorical: 0 to 5 rating),
    - Food and Drink (Categorical: 0 to 5 rating),
    - In-flight Service (Categorical: 0 to 5 rating),
    - In-flight Wifi Service (Categorical: 0 to 5 rating),
    - In-flight Entertainment (Categorical: 0 to 5 rating),
    - Baggage (Categorical: 0 to 5 rating),
    - Overall Satisfaction (Binary: Neutral/Dissatisfied or Satisfied),\n
    Link to the dataset can be found at: https://www.kaggle.com/datasets/mysarahmadbhat/airline-passenger-satisfaction
    """)

    try:
        st.dataframe(df.head(int(st.text_input("Select Number of Rows To View From Dataset"))))
    except ValueError:
        pass
    st.subheader('Outlier detection using Turkey Method:')
    st.write('A great way to detect outliers in a dataset is to visualize the distribution using a box plot. For our outlier detection method, we will be using the Turkey method. Turkey Method is an outlier detection method that states that outliers are values that fall outside 1.5 times the interquartile range from the quartiles 1 or 3. In other words values that are either below Q1 − 1.5 X IQR, or above Q3 + 1.5 X IQR are considered outliers. ')
    st.write('After looking at the boxplots there are several outliers in Flight distance, departure delays and arrival delays. So, lets remove them.')
    st.write('Data shape before outliers removed', df.shape)

    all_columns_names2 = outliner_check.columns.tolist()
    columnsx1 = st.selectbox("Select Numerical columns to Visualize outliers",all_columns_names2)
    fig3 = px.box(outliner_check, y=columnsx1)
    st.plotly_chart(fig3)

    figh = px.histogram(outliner_check, x=columnsx1)
    st.plotly_chart(figh)



    q1_f = df['Flight Distance'].quantile(.25)
    q3_f = df['Flight Distance'].quantile(.75)
    iqr_f = q3_f-q1_f

    q1_dd = df['Departure Delay'].quantile(.25)
    q3_dd = df['Departure Delay'].quantile(.75)
    iqr_dd = q3_dd-q1_dd

    q1_ad = df['Arrival Delay'].quantile(.25)
    q3_ad = df['Arrival Delay'].quantile(.75)
    iqr_ad = q3_ad-q1_ad

    df = df[~((df['Flight Distance'] < (q1_f - 1.5 * iqr_f)) | (df['Flight Distance'] > (q3_f + 1.5 * iqr_f)))]
    df = df[~((df['Departure Delay'] < (q1_dd - 1.5 * iqr_dd)) | (df['Departure Delay'] > (q3_dd + 1.5 * iqr_dd)))]
    df = df[~((df['Arrival Delay'] < (q1_ad - 1.5 * iqr_ad)) | (df['Arrival Delay'] > (q3_ad + 1.5 * iqr_ad)))]



    outliner_check2 = df[['Age', 'Flight Distance', 'Departure Delay', 'Arrival Delay']]


    st.write('Below are Boxplot and Histogram after outliners removed')

    columnsx2 = st.selectbox("Select Numerical columns to Visualize after outliers are Removed",outliner_check2.columns.tolist())
    figor = px.box(outliner_check2, y=columnsx2)
    st.plotly_chart(figor)

    fighor = px.histogram(outliner_check2, x=columnsx2)
    st.plotly_chart(fighor)

    st.write('Data shape after outliners removed', df.shape)

    st.subheader('Visualizing Customer Experience & Categorical Distribution')


    all_columns_names1 = df2.columns.tolist()
    columnsx = st.selectbox("Select Customer Experience Metric to Visualize its Distribution",all_columns_names1)
    columns_selected_pie = df.groupby(columnsx)[columnsx].agg(Frequency='count').reset_index()
    st.write(columns_selected_pie)

    fig2 = px.pie(columns_selected_pie, values='Frequency', names=columnsx, color_discrete_sequence=[
                 px.colors.qualitative.Alphabet[6],
                 px.colors.qualitative.Alphabet[11],
               px.colors.qualitative.Plotly[2],
                 px.colors.qualitative.Plotly[7],
               px.colors.qualitative.G10[5]])
    fig2.update_layout(width=600, height=600,title={"text" :columnsx,'y':0.95,'x':0.5,'xanchor': 'center','yanchor': 'top'})
    st.plotly_chart(fig2)


    columns_selected_bar = df.groupby([columnsx, 'Satisfaction'])[columnsx].agg(Frequency='count').reset_index()
    st.write(columns_selected_bar)
    fig = px.bar(columns_selected_bar, x=columnsx, y = "Frequency", color="Satisfaction",
                    color_discrete_map={'Satisfied':'lightcyan','Neutral or Dissatisfied':'darkblue'},  text_auto=True)
    fig.update_layout(width=600, height=600,title={"text" :columnsx,'y':0.95,'x':0.5,'xanchor': 'center','yanchor': 'top'})
    st.plotly_chart(fig)

#plot corrlation using heatmap
    #plt.figure(figsize=(10,8))
    #st.write(sns.heatmap(df4.corr(),annot= True, cmap = 'BuPu', linewidths=2))
    #st.pyplot()
    st.subheader('Correlation heatmap of Customer Experience')
    fig4 = px.imshow(df4.corr(), color_continuous_scale='BuPu', text_auto=True)
    fig4.update_layout(width=1200, height=1000)
    st.plotly_chart(fig4)

if __name__ == '__main__':
	main()
