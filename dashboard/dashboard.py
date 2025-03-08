import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import streamlit as st

sns.set(style='dark')


# Funtion

def create_performance_per_year_df(humidity_count_df):
    # Mengelompokkan berdasarkan tahun dan menghitung total penyewaan
    performance_per_year = humidity_count_df.groupby(
        "yr")[["cnt"]].sum().reset_index()
    # Mengganti nama kolom agar lebih deskriptif
    performance_per_year.columns = ["Year", "total_rentals"]
    # Mengurutkan berdasarkan total penyewaan secara menurun
    performance_per_year = performance_per_year.sort_values(
        by="total_rentals", ascending=False)
    return performance_per_year


def create_avg_rentals_per_month_2012_df(humidity_count_df):
    # Filter data hanya untuk tahun 2012
    avg_rentals_per_month_2012_df = humidity_count_df[humidity_count_df["yr"] == 2012].groupby(
        "mnth")[["cnt"]].mean().reset_index()
    # Mengganti nama kolom agar lebih deskriptif
    avg_rentals_per_month_2012_df.columns = ["Month", "avg_rentals"]
    # Mengurutkan berdasarkan rata-rata penyewaan tertinggi
    avg_rentals_per_month_2012_df = avg_rentals_per_month_2012_df.sort_values(
        by="avg_rentals", ascending=False)
    return avg_rentals_per_month_2012_df


def create_total_rentals_per_season_df(humidity_count_df):
    # Grouping data berdasarkan season dan menjumlahkan total penyewaan untuk setiap season
    rentals_per_season = humidity_count_df.groupby(
        "season")[["cnt"]].sum().reset_index()
    # Memastikan kolom "season" terisi dengan benar
    rentals_per_season["season"] = rentals_per_season["season"]
    # Mengganti nama kolom agar lebih deskriptif
    rentals_per_season.columns = ["Season", "total_rentals"]
    # Mengurutkan berdasarkan total penyewaan secara menurun
    rentals_per_season = rentals_per_season.sort_values(
        by="total_rentals", ascending=False)
    return rentals_per_season


def create_total_rentals_per_day_df(humidity_count_df):
    # Grouping data berdasarkan workingday dan menjumlahkan total penyewaan
    rentals_working_day = humidity_count_df.groupby(
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


def create_density_category(humidity_count_df):
    # Menentukan batasan kategori kepadatan
    bins = [0, 2000, 5000, float('inf')]
    labels = ['Sepi', 'Sedang', 'Ramai']

    # Menerapkan binning ke kolom 'cnt'
    humidity_count_df['kategori_kepadatan'] = pd.cut(
        humidity_count_df['cnt'], bins=bins, labels=labels, right=False)

    # Menyimpan hasil dalam DataFrame baru
    density_category_df = humidity_count_df[[
        'dteday', 'cnt', 'kategori_kepadatan']]

    return density_category_df  # Mengembalikan hasil


# Read data
days_df = pd.read_csv("dashboard/day_clean_df.csv")
hours_df = pd.read_csv("dashboard/hour_clean_df.csv")

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
# Memanggil fungsi create_density_category untuk mengelompokkan kepadatan penyewaan
density_category_df = create_density_category(main_df_days)


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


st.subheader("Kinerja Penyewaan Sepeda dalam Beberapa Tahun Terakhir")
# Menggunakan style dengan latar belakang putih
sns.set_style("white")
# Tentukan tahun yang akan diwarnai (misalnya tahun 2011)
highlight_year = 2011
# Tentukan warna: tahun yang disorot berwarna biru, lainnya abu-abu
colors = ["#90CAF9" if year ==
          highlight_year else "#D3D3D3" for year in performance_per_year_df["Year"]]
# Membuat figure dan axis
fig, ax = plt.subplots(figsize=(15, 8))
# Membuat barplot untuk total penyewaan per tahun
sns.barplot(x="Year", y="total_rentals",
            data=performance_per_year_df, palette=colors, ax=ax)
# Menampilkan kembali garis pinggir (spines)
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1)  # Atur ketebalan garis jika perlu
# Menambahkan label dan judul
ax.set_ylabel("Total Rentals", fontsize=20)
ax.set_xlabel("Year", fontsize=20)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=15)
# Menampilkan grafik di Streamlit
st.pyplot(fig)


st.subheader("Tren rata-rata penyewaan sepeda per bulan sepanjang tahun 2012")
# Correct order of months
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
# Remove right border# Set the Y-axis to start at zero
ax.spines["right"].set_visible(False)
# Add a little margin at the top
ax.set_ylim(0, avg_rentals_per_month_2012_df["avg_rentals"].max() + 500)
# Set title and labels
plt.xlabel("Month", fontsize=12)
plt.ylabel("Average Rentals", fontsize=12)
plt.xticks(fontsize=10, rotation=45)  # To avoid overlapping month names
plt.yticks(fontsize=10)
# Remove grid if not needed
ax.grid(False)
# Show plot
st.pyplot(fig)


st.subheader("Total Penyewaan Sepeda Setiap Musim")
# Menggunakan style dengan latar belakang putih
sns.set_style("white")
# Menentukan musim dengan jumlah penyewaan tertinggi
max_season = total_rentals_per_season_df.loc[total_rentals_per_season_df["total_rentals"].idxmax(
), "Season"]
# Menentukan warna: musim dengan jumlah penyewaan tertinggi berwarna biru, lainnya abu-abu
colors = ["#90CAF9" if season ==
          max_season else "#D3D3D3" for season in total_rentals_per_season_df["Season"]]
# Membuat figure dan axis
fig, ax = plt.subplots(figsize=(12, 6))
# Membuat barplot untuk total penyewaan per musim
sns.barplot(x="Season", y="total_rentals",
            data=total_rentals_per_season_df, palette=colors, ax=ax)
# Menyesuaikan batas atas sumbu y agar lebih proporsional
ax.set_ylim(0, total_rentals_per_season_df["total_rentals"].max() * 1.1)
# Format sumbu y agar lebih mudah dibaca
ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))
# Menampilkan kembali garis pinggir (spines)
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1)  # Atur ketebalan garis pinggir jika perlu
# Menambahkan label dan judul
ax.set_ylabel("Jumlah Penyewaan", fontsize=15)
ax.set_xlabel("Musim", fontsize=15)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
# Menampilkan grafik di Streamlit
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


st.subheader("Jam Puncak dengan Penyewaan Sepeda Tertinggi")

# Mengambil 5 jam dengan jumlah penyewaan tertinggi
top_5 = total_rentals_per_hour_df.nlargest(5, "total_rentals")

# Set semua bar berwarna abu-abu
colors = ["#D3D3D3"] * len(top_5)

# Ubah warna bar ke-3 menjadi biru
colors[2] = "#90CAF9"

# Membuat figure dan axis
fig, ax = plt.subplots(figsize=(10, 6))

# Membuat bar chart dengan warna yang telah ditentukan
sns.barplot(
    x="Hour",
    y="total_rentals",
    data=top_5,
    palette=colors,  # Menggunakan warna yang telah ditentukan
    ax=ax
)

# Menampilkan kembali garis pinggir (spines)
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1)  # Atur ketebalan garis pinggir jika perlu

# Menyesuaikan batas atas sumbu y agar lebih luas
ax.set_ylim(0, top_5["total_rentals"].max() * 1.1)

# Format sumbu y agar lebih mudah dibaca
ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))

# Menambahkan judul dan label
ax.set_xlabel("Jam", fontsize=15)
ax.set_ylabel("Jumlah Penyewaan", fontsize=15)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)

# Menampilkan grafik di Streamlit
st.pyplot(fig)


st.subheader("Distribusi Kategori Kepadatan Penyewaan Sepeda")

# Menghitung jumlah hari dalam setiap kategori kepadatan
kategori_counts = density_category_df['kategori_kepadatan'].value_counts()
# Mengurutkan kategori sesuai urutan yang diinginkan
order = ["Sepi", "Sedang", "Ramai"]
# Mengisi 0 jika ada kategori yang tidak muncul
kategori_counts = kategori_counts.reindex(order, fill_value=0)
# Menentukan warna: kategori dengan nilai tertinggi berwarna biru, lainnya abu-abu
colors = ['#B0BEC5', '#B0BEC5', '#B0BEC5']  # Default semua abu-abu
max_index = kategori_counts.idxmax()  # Cari kategori dengan nilai tertinggi
# Ambil posisi di dalam urutan yang kita tentukan
max_position = order.index(max_index)
colors[max_position] = '#90CAF9'  # Ubah warna tertinggi menjadi biru
# Membuat bar chart
fig, ax = plt.subplots(figsize=(6, 4))  # Simpan figure dan axis
kategori_counts.plot(kind='bar', color=colors, ax=ax)  # Plot ke dalam axis
# Menambahkan label dan judul
ax.set_xlabel('Kategori Kepadatan')
ax.set_ylabel('Jumlah Hari')
ax.set_xticklabels(order, rotation=0)
# Menampilkan grafik di Streamlit
st.pyplot(fig)
