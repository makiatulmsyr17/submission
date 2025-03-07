import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import streamlit as st

sns.set(style='dark')


# Funtion

def create_performance_per_year_df(day_df):
    # Mengelompokkan berdasarkan tahun dan menghitung total penyewaan
    performance_per_year = day_df.groupby("yr")[["cnt"]].sum().reset_index()
    # Mengganti nama kolom agar lebih deskriptif
    performance_per_year.columns = ["Year", "total_rentals"]
    # Mengurutkan berdasarkan total penyewaan secara menurun
    performance_per_year = performance_per_year.sort_values(
        by="total_rentals", ascending=False)
    return performance_per_year


def create_avg_rentals_per_month_2012_df(day_df):
    # Filter data hanya untuk tahun 2012
    avg_permonth_2012 = day_df[day_df["yr"] == "2012"].groupby(
        "mnth")[["cnt"]].mean().reset_index()
    # Mengganti nama kolom agar lebih deskriptif
    avg_permonth_2012.columns = ["Month", "avg_rentals"]
    # Mengurutkan berdasarkan rata-rata penyewaan tertinggi
    avg_permonth_2012 = avg_permonth_2012.sort_values(
        by="avg_rentals", ascending=False)
    return avg_permonth_2012


def create_total_rentals_per_season_df(day_df):
    # Grouping data berdasarkan season dan menjumlahkan total penyewaan untuk setiap season
    rentals_per_season = day_df.groupby("season")[["cnt"]].sum().reset_index()
    # Memastikan kolom "season" terisi dengan benar
    rentals_per_season["season"] = rentals_per_season["season"]
    # Mengganti nama kolom agar lebih deskriptif
    rentals_per_season.columns = ["Season", "total_rentals"]
    # Mengurutkan berdasarkan total penyewaan secara menurun
    rentals_per_season = rentals_per_season.sort_values(
        by="total_rentals", ascending=False)
    return rentals_per_season


def create_total_rentals_per_day_df(day_df):
    # Grouping data berdasarkan workingday dan menjumlahkan total penyewaan
    rentals_working_day = day_df.groupby(
        "workingday")[["cnt"]].sum().reset_index()
    # Mengganti nama kolom agar lebih deskriptif
    rentals_working_day.columns = ["Day", "total_rentals"]
    # Mengganti 'Yes' dengan 'Working Day' dan 'No' dengan 'Holiday'
    rentals_working_day["Day"] = rentals_working_day["Day"].replace(
        {"Yes": "Working Day", "No": "Holiday"})
    # Mengurutkan berdasarkan total_rentals secara menurun
    rentals_working_day = rentals_working_day.sort_values(
        by="total_rentals", ascending=False)
    return rentals_working_day


def create_total_rentals_per_hour_df(hour_df):
    # Grouping data berdasarkan jam dan menjumlahkan total penyewaan
    rentals_per_hour = hour_df.groupby("hr")[["cnt"]].sum().reset_index()
    # Mengganti nama kolom agar lebih deskriptif
    rentals_per_hour.columns = ["Hour", "total_rentals"]
    # Mengurutkan berdasarkan total penyewaan secara menurun
    rentals_per_hour_sorted = rentals_per_hour.sort_values(
        by="total_rentals", ascending=False)
    # Menemukan 5 jam dengan total penyewaan tertinggi
    top_5 = rentals_per_hour_sorted.nlargest(5, "total_rentals")
    return top_5


days_df = pd.read_csv("day_clean_df.csv")
hours_df = pd.read_csv("hour_clean_df.csv")

datetime_columns = ["dteday"]
days_df.sort_values(by="dteday", inplace=True)
days_df.reset_index(inplace=True)

hours_df.sort_values(by="dteday", inplace=True)
hours_df.reset_index(inplace=True)

for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
    hours_df[column] = pd.to_datetime(hours_df[column])

min_date_days = days_df["dteday"].min()
max_date_days = days_df["dteday"].max()

min_date_hour = hours_df["dteday"].min()
max_date_hour = hours_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image(
        "https://i.pinimg.com/1200x/0f/4d/30/0f4d30bc4f7eb9eb428b7296e60d4393.jpg")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])

main_df_days = days_df[(days_df["dteday"] >= str(start_date)) &
                       (days_df["dteday"] <= str(end_date))]

main_df_hour = hours_df[(hours_df["dteday"] >= str(start_date)) &
                        (hours_df["dteday"] <= str(end_date))]

# Memanggil fungsi create_performance_per_year_df untuk mendapatkan total penyewaan per tahun
performance_per_year_df = create_performance_per_year_df(main_df_days)
# Memanggil fungsi create_avg_rentals_per_month_2012_df untuk mendapatkan rata-rata penyewaan per bulan di tahun 2012
avg_rentals_per_month_2012_df = create_avg_rentals_per_month_2012_df(
    main_df_days)
# Memanggil fungsi create_total_rentals_per_season_df untuk mendapatkan total penyewaan per musim
total_rentals_per_season_df = create_total_rentals_per_season_df(main_df_days)
# Memanggil fungsi create_total_rentals_per_day_df untuk mendapatkan total penyewaan per hari kerja
total_rentals_per_day_df = create_total_rentals_per_day_df(main_df_days)
# Memanggil fungsi create_total_rentals_per_hour_df untuk mendapatkan 5 jam dengan total penyewaan tertinggi
total_rentals_per_hour_df = create_total_rentals_per_hour_df(main_df_hour)


# Visualisasi
st.markdown("<h1 style='text-align: center;'>🚴 Bike Sharing 🚴</h1>",
            unsafe_allow_html=True)


st.subheader("Daily")

# Membuat dua kolom
col1, col2 = st.columns(2)

# Menggunakan with statement untuk menampilkan metrik di dalam kolom
with col1:
    # Pastikan kamu menggunakan kolom yang benar
    total_orders = days_df['cnt'].sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    # Pastikan kamu menggunakan kolom yang benar
    total_sum = days_df['registered'].sum()
    st.metric("Total Registered", value=total_sum)


st.subheader("kinerja penyewaan sepeda dalam beberapa tahun terakhir")

# Set style with no background
sns.set_style("white")

# Tentukan tahun yang akan diwarnai (tahun 2012)
highlight_year = 2011

# Tentukan warna: tahun 2012 akan memiliki warna biru, yang lain warna abu-abu muda
colors = ["#90CAF9" if year ==
          highlight_year else "#D3D3D3" for year in performance_per_year_df["Year"]]
# Buat figure dan axis
fig, ax = plt.subplots(figsize=(15, 8))
# Buat barplot untuk total sewa per tahun
sns.barplot(x="Year", y="total_rentals",
            data=performance_per_year_df, palette=colors, ax=ax)
# Hilangkan background dan border
ax.set_facecolor("white")
for spine in ax.spines.values():
    spine.set_visible(False)
# Set label dan judul
ax.set_ylabel("Total Rentals", fontsize=20)
ax.set_xlabel("Year", fontsize=20)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=15)
# Tampilkan plot
st.pyplot(fig)


st.subheader("Tren rata-rata penyewaan sepeda per bulan sepanjang tahun 2012")
# Sample DataFrame (replace with your actual data)
avg_rentals_per_month_2012_df = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "avg_rentals": [500, 600, 700, 650, 800, 900, 950, 1000, 1050, 1100, 1150, 1200]
})
# Correct order of months
month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
# Convert "Month" column to a categorical type with the correct order
avg_rentals_per_month_2012_df["Month"] = pd.Categorical(
    avg_rentals_per_month_2012_df["Month"], categories=month_order, ordered=True
)
# Sort the DataFrame by the month category
avg_rentals_per_month_2012_df = avg_rentals_per_month_2012_df.sort_values(
    by="Month")
# Plot line chart
fig, ax = plt.subplots(figsize=(15, 6))
ax.plot(avg_rentals_per_month_2012_df["Month"], avg_rentals_per_month_2012_df["avg_rentals"],
        marker='o', linewidth=2, color="#72BCD4")
# Remove background
ax.set_facecolor("white")   # Background color of the plot
fig.patch.set_facecolor("white")  # Background color of the figure
ax.spines["top"].set_visible(False)  # Remove top border
ax.spines["right"].set_visible(False)  # Remove right border
# Set the Y-axis to start at zero
# Add a little margin at the top
ax.set_ylim(0, avg_rentals_per_month_2012_df["avg_rentals"].max() + 500)
plt.xlabel("Month", fontsize=12)
plt.ylabel("Average Rentals", fontsize=12)
plt.xticks(fontsize=10, rotation=45)  # To avoid overlapping month names
plt.yticks(fontsize=10)
# Remove grid if not needed
ax.grid(False)
# Show plot
st.pyplot(fig)


st.subheader("Total Penyewaan Sepeda Setiap Musim")
# Using style with no background
sns.set_style("white")
# Determining the season with the highest rentals
max_season = total_rentals_per_season_df.loc[total_rentals_per_season_df["total_rentals"].idxmax(
), "Season"]
# Defining colors: the season with the highest rentals is blue, others are gray
colors = ["#90CAF9" if season ==
          max_season else "#D3D3D3" for season in total_rentals_per_season_df["Season"]]
# Creating figure and axis
fig, ax = plt.subplots(figsize=(12, 6))
# Creating barplot for total rentals per season
sns.barplot(x="Season", y="total_rentals",
            data=total_rentals_per_season_df, palette=colors, ax=ax)
# Adjusting y-axis limits for better proportionality
ax.set_ylim(0, total_rentals_per_season_df["total_rentals"].max() * 1.1)
# Formatting y-axis labels for easier readability
ax.yaxis.set_major_formatter(mticker.StrMethodFormatter(
    '{x:,.0f}'))  # Format numbers with commas
# Removing background and borders
ax.set_facecolor("white")
for spine in ax.spines.values():
    spine.set_visible(False)
# Adding labels and title
ax.set_ylabel("total_rentals", fontsize=15)
ax.set_xlabel("Season", fontsize=15)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
# Displaying the plot
st.pyplot(fig)


st.subheader("Distribusi penyewaan sepeda antara hari kerja dan akhir pekan")
total_rentals = total_rentals_per_day_df.groupby("Day")["total_rentals"].sum()
# Menghapus latar belakang grid
sns.set_style("white")
# Membuat figure dan axis
# Membuat figure dan axis
fig, ax = plt.subplots(figsize=(8, 5))
# Membuat pie chart
ax.pie(
    total_rentals,
    labels=total_rentals.index,
    autopct="%1.1f%%",
    colors=["#90CAF9", "#D3D3D3"],
    startangle=90,
    wedgeprops={"edgecolor": "black"}
)
# Menampilkan plot
st.pyplot(fig)


st.subheader("Top Hours with the Highest Bikes Rentals")
# Taking the top 5 hours with the highest total rentals
top_5 = total_rentals_per_hour_df.nlargest(5, "total_rentals")
# Set all bars to gray
colors = ["#D3D3D3"] * len(top_5)
# Change the color of the third bar to blue
colors[2] = "#90CAF9"  # Blue for the 3rd bar
# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 6))
# Create a bar chart with the pre-defined colors
sns.barplot(
    x="Hour",
    y="total_rentals",
    data=top_5,
    palette=colors,  # Using the predefined colors
    ax=ax
)
# Remove border lines
for spine in ax.spines.values():
    spine.set_visible(False)
# Adjust the upper limit of the y-axis to make the chart more spacious
ax.set_ylim(0, top_5["total_rentals"].max() * 1.1)
# Format the y-axis to make the numbers easier to read
ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))
# Add title and labels
ax.set_xlabel("Hour", fontsize=15)
ax.set_ylabel("total_rentals", fontsize=15)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
# Show the plot
st.pyplot(fig)
