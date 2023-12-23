import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set(style='dark')

st.set_page_config(layout="wide")

# Menyiapkan data hour_df
hour_df = pd.read_csv("hour_clean.csv")
hour_df.head()

hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Mengubah nama kolom
hour_df.rename(columns={
    'dteday': 'dateday',
    'hr': 'hour',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather',
    'cnt': 'count'
}, inplace=True)

# Mengubah index value
hour_df['month'] = hour_df['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 
    5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agst',
    9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Des'
})
hour_df['weather'] = hour_df['weather'].map({
    1: 'Cerah',
    2: 'Berawan atau kabut',
    3: 'Hujan ringan'
})

# Menyiapkan daily_hour_rent_df
def create_daily_hour_rent_df(df):
    daily_hour_rent_df = df.groupby(by='hour').agg({
        'count': 'sum'
    }).reset_index()
    return daily_hour_rent_df

# Menyiapkan daily_rent_df
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent_df

# Menyiapkan monthly_rent_df
def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='month').agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 
        'Mei', 'Juni', 'Juli', 'Agst',
        'Sep', 'Okt', 'Nov', 'Des'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

# Menyiapkan weather_rent_df
def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='weather').agg({
        'count': 'sum'
    })
    return weather_rent_df

# Membuat filter
min_date = pd.to_datetime(hour_df['dateday']).dt.date.min()
max_date = pd.to_datetime(hour_df['dateday']).dt.date.max()

# ----- SIDEBAR -----

with st.sidebar:
    # Logo
    image_url = "https://github.com/asvrn/bike_sharing/blob/main/img/LOGO.png?raw=true"
    st.image(image_url, caption='Rifqi Asverian Putra', use_column_width=True)

    st.sidebar.header("Filter:")

     # Date input
    start_date, end_date = st.date_input(
        label='Interval Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)

main_df = hour_df[(hour_df['dateday'] >= str(start_date)) & 
                (hour_df['dateday'] <= str(end_date))]

# Menyiapkan dataframe
daily_rent_df = create_daily_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)
daily_hour_rent_df = create_daily_hour_rent_df(main_df)

# Page
st.title("Bike Sharing Dashboard")
st.text("Predicting bike sharing demand")
st.markdown("##")

col1, col2, col3 = st.columns(3)

with col1:
    total_registered = main_df['registered'].sum()
    st.metric("Jumlah Penyewa Terdaftar", value=total_registered)
with col2:
    total_casual = main_df['casual'].sum()
    st.metric("Jumlah Penyewa Biasa", value=total_casual)
with col3:
    all_total = main_df['count'].sum()
    st.metric("Jumlah Seluruh Penyewa", value=all_total)

st.markdown("---")

#1
st.subheader('Penyewaan Perbulan')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    monthly_rent_df.index,
    monthly_rent_df['count'],
    marker='o', 
    linewidth=2,
    color='tab:red'
)

for index, row in enumerate(monthly_rent_df['count']):
    ax.text(index, row + 1, int(row), ha='center', va='bottom', fontsize=16, color='white')

ax.tick_params(axis='x', labelsize=25, color='white')
ax.tick_params(axis='y', labelsize=20)
ax.set_facecolor('none')
fig.patch.set_alpha(0.0)
st.pyplot(fig)

# 2
st.subheader('Penyewaan sepeda pada Cuaca Tertentu')
fig, ax = plt.subplots(figsize=(12, 8))

weather_rent_df = weather_rent_df.sort_values(by='count', ascending=False)
sns.barplot(
    x=weather_rent_df.index,
    y=weather_rent_df['count'],
    width=0.5
)

for index, row in enumerate(weather_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=10, color='white')

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)
ax.set_facecolor('none')
fig.patch.set_alpha(0.0)
st.pyplot(fig)

# 3
st.subheader('Penyewaan Perjam')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    daily_hour_rent_df.index,
    daily_hour_rent_df['count'],
    marker='o', 
    linewidth=2,
    color='tab:red'
)

for index, row in enumerate(daily_hour_rent_df['count']):
    ax.text(index, row + 1, int(row), ha='center', va='bottom', fontsize=16, color='white')

ax.set_xticks(daily_hour_rent_df.index)
ax.tick_params(axis='x', labelsize=25, color='white')
ax.tick_params(axis='y', labelsize=20)
ax.set_facecolor('none')
fig.patch.set_alpha(0.0)
st.pyplot(fig)


st.caption('Copyright (c), created by Rifqi Asverian Putra')
