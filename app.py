import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from plotly import graph_objs as go

st.set_page_config(page_title="Dashboard Covid-19 di Indonesia", page_icon=":bar_chart:", layout="wide")

# --- Load Data From CSV ----
@st.cache
def get_data_from_csv():
    df = pd.read_csv('data/covid19.csv')
    df_province = pd.read_csv('data/daily_case_province_covid19.csv')
    df_province_death = pd.read_csv('data/daily_death_province_covid19.csv')
    df_province_recovered = pd.read_csv('data/daily_recovered_province_covid19.csv')
    df_vaccinated = pd.read_csv('data/vaccine_covid19.csv')
    return df, df_province, df_province_death, df_province_recovered, df_vaccinated

df, df_province, df_province_death, df_province_recovered, df_vaccinated = get_data_from_csv()

# --- Header ---
st.header("Dashboard Covid-19 di Indonesia")
st.markdown("----")

# --- Information of total Several Data ---
total_case, total_recovered, total_death = st.columns(3)

total_case.metric("Total Kasus", df.kasus_harian.sum())
total_recovered.metric("Total Sembuh",  df.sembuh_baru.sum())
total_death.metric("Total Meninggal",  df.meninggal_baru.sum())

st.markdown("----")

# --- Main Plot ---
# --- sidebar ---
st.sidebar.write('Filter Data Covid-19:')
option_1 = st.sidebar.checkbox('Total Kasus')
option_2 = st.sidebar.checkbox('Kasus Harian')
option_3 = st.sidebar.checkbox('Total Sembuh')
option_4 = st.sidebar.checkbox('Sembuh Harian')
option_5 = st.sidebar.checkbox('Total Meninggal')
option_6 = st.sidebar.checkbox('Meninggal Harian')

fig_main = go.Figure()
if (option_1 or option_2 or option_3 or option_4 or option_4 or option_5 or option_6) is False:
    fig_main.add_trace(go.Scatter(x=df['Date'], y=df['kasus_harian'], name='Kasus Harian'))
    fig_main.add_trace(go.Scatter(x=df['Date'], y=df['sembuh_baru'], name='Sembuh Harian'))
    fig_main.add_trace(go.Scatter(x=df['Date'], y=df['meninggal_baru'], name='Meninggal Harian'))
else:
    if option_1:
        fig_main.add_trace(go.Scatter(x=df['Date'], y=df['total_kasus'], name='Total Kasus'))
    if option_2:
        fig_main.add_trace(go.Scatter(x=df['Date'], y=df['kasus_harian'], name='Kasus Harian'))
    if option_3:
        fig_main.add_trace(go.Scatter(x=df['Date'], y=df['Sembuh'], name='Total Sembuh'))
    if option_4:
        fig_main.add_trace(go.Scatter(x=df['Date'], y=df['sembuh_baru'], name='Sembuh Harian'))
    if option_5:
        fig_main.add_trace(go.Scatter(x=df['Date'], y=df['Meninggal'], name='Total Meninggal'))
    if option_6:
        fig_main.add_trace(go.Scatter(x=df['Date'], y=df['meninggal_baru'], name='Meninggal Harian'))
fig_main.layout.update(title_text='Perkembangan Covid-19 di Indonesia', 
                       xaxis_rangeslider_visible=True, 
                       hovermode='x',
                       legend_orientation='v')
fig_main.add_vrect(
    x0="2021-07-12", x1="2021-08-23",
    fillcolor="green", opacity=0.5,
    layer="below", line_width=0,
    annotation_text="PPKM Darurat", 
)


st.plotly_chart(fig_main, use_container_width=True)


# handling province
st.sidebar.write("Plot Berdasarkan Provinsi")
jenis = st.sidebar.radio("Pilih Kasus ", ('Tampilkan Semua','Terkonfirmasi','Sembuh','Meninggal'))
nums = st.sidebar.slider('Pilih jumlah provinsi', 5,35,5)
def plot_province(jenis, n_province):
    top_cases = df_province.iloc[:,1:].sum().reset_index().rename(columns={
                        'index': 'Provinsi',
                        0:'Total Kasus'}).sort_values(by='Total Kasus', ascending=False).head(n_province)
    top_death = df_province_death.iloc[:,1:].sum().reset_index().rename(columns={
                            'index': 'Provinsi',
                            0:'Total Meninggal'}).sort_values(by='Total Meninggal', ascending=False).head(n_province)
    top_recovered = df_province_recovered.iloc[:,1:].sum().reset_index().rename(columns={
                            'index': 'Provinsi',
                            0:'Total Sembuh'}).sort_values(by='Total Sembuh', ascending=False).head(n_province)
    confirmed = go.Bar(
                            y=top_cases['Total Kasus'], 
                            x=top_cases['Provinsi'], 
                            name = 'Terkonfirmasi',
                            marker={
                                'color': top_cases['Total Kasus'],
                                'colorscale': 'Blues'}
                        )
    recovered = go.Bar(
                    y=top_recovered['Total Sembuh'], 
                    x=top_recovered['Provinsi'], 
                    name='Sembuh',
                    marker={
                        'color': top_recovered['Total Sembuh'],
                        'colorscale': 'Greens'}
                )

    death =  go.Bar(
                            y=top_death['Total Meninggal'], 
                            x=top_death['Provinsi'], 
                            name='Meninggal Dunia',
                            marker={
                                'color': top_death['Total Meninggal'],
                                'colorscale': 'Reds'}
                    )
    if jenis == 'Tampilkan Semua' :
        data = [confirmed,recovered,death]  
        fig = go.Figure(data)
        title = 'Provinsi Teratas Kasus Covid-19'
    elif jenis == 'Terkonfirmasi':
        data = [confirmed]
        fig = go.Figure(data)
        title = 'Total Terkonfirmasi Per-Provinsi'
    elif jenis == 'Sembuh':
        data = [recovered]
        fig = go.Figure(data)
        title = 'Total Sembuh per-Provinsi'
    else:
        data = [death]
        fig = go.Figure(data)
        title = 'Total Meninggal Per-Provinsi'
    fig.layout.update(
        title=title, 
        xaxis_title='Time Periode', 
        yaxis_title='Count', 
        hovermode="x"
    )
    st.plotly_chart(fig, use_container_width=True)
plot_province(jenis, nums)

# note

# --- Vaccination Plot ---
# df_vaccinated = df[['Date', 'dosis_pertama', 'dosis_kedua', 'total_kasus']].loc[304:]

graph1 = go.Scatter(
               hoverinfo='skip', 
               x=df_vaccinated['Date'], 
               y=df_vaccinated['dosis_pertama'],  
               fill ='tozeroy',
               hovertemplate='<b>%{x}</b><br>' + '<b>Total Vaksin Pertama: </b>'+'%{y}<extra></extra>', 
               marker_color='#00FF1E', 
               name='Vaksin Pertama'
    ) 

graph2 = go.Scatter(
               hoverinfo='skip', 
               x=df_vaccinated['Date'], 
               y=df_vaccinated['dosis_kedua'], 
               fill ='tozeroy',
               hovertemplate='<b>%{x}</b><br><b>Total Vaksin Kedua: </b>%{y}<extra></extra>', 
               marker_color='#FFE000', 
               name='Vaksin Kedua'
    ) 

data = [graph1, graph2]
fig_vaccine = go.Figure(data)

fig_vaccine.update_layout(
    title='Perkembangan Vaksinasi Covid-19 di Indonesia',  
    yaxis_title='Total', 
    hovermode='x', 
    legend_orientation='v',
)

# st.plotly_chart(fig_vaccine, use_container_width=True)


vaccine_plot1, vaccine_plot2 = st.columns([100,3])
vaccine_plot1.plotly_chart(fig_vaccine, use_container_width=True)



