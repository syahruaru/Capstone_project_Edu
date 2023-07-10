import streamlit as st
import pandas as  pd
import plotly.express as px
import math
import altair as alt



st.set_page_config(layout = "wide")
with st.expander("Prolog"):
    st.write("""
            Sekolah swasta sering dipersepsikan sebagai sekolah yang lebih mahal jika dibandingkan sekolah negeri.\n
            namun apakah perbedaan tersebut mempengaruhi kualitas sekolah?\n
            Apakah sekolah swasta lebih baik dibandingkan sekolah negeri?\n
            

            Bahan bacaan lebih lanjut: \n
            https://www.kompas.com/edu/read/2022/10/11/115136771/serba-serbi-perbedaan-sekolah-swasta-dan-negeri?page=all \n
            https://edukasi.sindonews.com/read/1069865/212/ini-perbedaan-signifikan-sekolah-negeri-dan-sekolah-swasta-1681193078?showpage=all \n
            https://www.finansialku.com/bingung-pilih-sekolah-negeri-atau-swasta-cek-biayanya-dulu-22022304/ \n


            
            Berikut disajikan data Sekolah Menengah Pertama pada tahun 2021 di Kota Bekasi.\n
            *Data diambil dari: https://danta-admin.bekasikota.go.id/id/dataset/?organization=disdik&res_format=CSV&page=1
        """)









tab1, tab2, tab3= st.tabs(["Negeri", "Swasta", "Perbandingan"])

with tab1:
    df_negeri = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSrueDfCPVfBXfM9bnmDwZeOi1ZpsrybUZTWNFmcbcWfGRvU4FFVs63RWJcJ-7U73DUaGbUJcIpnV92/pub?output=csv')
    #df_negeri


    st.title('Data Sekolah Menengah Pertama (SMP) Negeri per-Kecamatan di Kota Bekasi')
    # 1. Jumlah Sekolah Per Kecamatan -> BarChart
    st.subheader('Jumlah Sekolah Per Kecamatan')
    df_negeri = df_negeri.sort_values(by='JUMLAH SMP NEGERI', ascending=False)
    fig = px.bar(df_negeri, x='KECAMATAN', y='JUMLAH SMP NEGERI')
    st.plotly_chart(fig, use_container_width=True)
    

    with st.expander("See explanation"):
        st.write("""
            Grafik di atas Merupakan data jumlah SMP Negeri per-kecamatan di kota bekasi.
            Dapat dilihat kecamatan Bekasi Timur, Bekasi Utara dan Jatiasih Menjadi kecamatan dengan jumlah SMP Terbanyak di Kota Bekasi.
        """)
    
    # 2. Perbandingan Akreditasi Sekolah
    st.subheader('Perbandingan Akreditasi Sekolah per-Kecamatan di Kota Bekasi')
    # Membuat bar chart menggunakan Plotly Express
    df_negeri = df_negeri.sort_values(by='TERAKREDITASI (A)', ascending=False)
    fig = px.bar(df_negeri, x='KECAMATAN', y=['TERAKREDITASI (A)', 'TERAKREDITASI (B)', 'TERAKREDITASI (C)', 'SEKOLAH MENENGAH PERTAMA (SMP) NEGERI BELUM TERAKREDITASI'], barmode='group')
    # Mengatur layout agar grafik memenuhi lebar halaman
    fig.update_layout(width=1400)
    # Menampilkan grafik menggunakan Streamlit
    st.plotly_chart(fig)
    with st.expander("See explanation"):
        st.write("""
            Grafik diatas merupakan perbandingan akreditasi SMP Negeri di Kota bekasi Per-Kecamatan.
            Umumnya SMP Negeri di Kota Bekasi sudah berakreditasi (A)
        """)


    # 3. Matric Perbandingan Jumlah sekolah dengan akreditasi (A) dengan Total JUmlah sekolah per-Kecamatan
    st.subheader('Persentase sekolah dengan Akreditasi A per-Kecamatan di Kota Bekasi')
    # Menghitung persentase akreditasi A terhadap jumlah sekolah
    df_negeri['Persentase (A)'] = (df_negeri['TERAKREDITASI (A)'] / df_negeri['JUMLAH SMP NEGERI']) * 100
    # Menghitung jumlah baris dan kolom dalam layout
    total_kecamatan = len(df_negeri)
    num_columns = 6
    num_rows = math.ceil(total_kecamatan / num_columns)
    # Membagi layar menjadi 6 kolom
    columns = st.columns(num_columns)
    # Menampilkan metrik perbandingan persentase akreditasi A dengan jumlah sekolah di setiap kecamatan
    for kecamatan_index in range(total_kecamatan):
        with columns[kecamatan_index % num_columns]:
            kecamatan = df_negeri.loc[kecamatan_index, 'KECAMATAN']
            persentase_a = df_negeri.loc[kecamatan_index, 'Persentase (A)']
            st.metric(label=kecamatan, value=f'{persentase_a:.2f}%', delta_color='inverse')
    with st.expander("See explanation"):
        st.write("""
            Delapan kecamatan di Kota Bekasi sudah memiliki persentase sekolah berakreditasi (A) diatas 50%.
            Namun hal ini juga bisa dijadikan catatan untuk kecamatan lain yang memiliki persentase sekolah akreditasi A di bawah 50% untuk meningkatkan kualiatas sekolah pada daerah tersebut.
        """)

    # 4. Perbandingan jumlah lab -> LineChart
    st.subheader('Jumlah Lab di SMP Negeri per-Kecamatan di Kota Bekasi')
    # Menambahkan kolom Total Lab
    df_negeri['Total Lab'] = df_negeri[['JUMLAH LABORATORIUM KOMPUTER', 'JUMLAH LABORATORIUM BAHASA', 'JUMLAH LABORATORIUM IPA']].sum(axis=1)
    # Membuat bar chart menggunakan Plotly Express
    fig = px.bar(df_negeri, x='KECAMATAN', y='Total Lab', title='Perbandingan Total Lab per Kecamatan')
    # Menampilkan bar chart menggunakan st.plotly_chart
    st.plotly_chart(fig, use_container_width=True)
    # Membuat DataFrame hanya dengan 3 kolom yang ingin ditampilkan
    df_lab = pd.DataFrame(df_negeri, columns=['KECAMATAN', 'JUMLAH LABORATORIUM IPA', 'JUMLAH LABORATORIUM BAHASA', 'JUMLAH LABORATORIUM KOMPUTER'])
    # Mengubah format data menjadi format yang cocok untuk line chart
    df_lab = df_lab.melt('KECAMATAN', var_name='Lab', value_name='Jumlah Lab')
    # Membuat line chart menggunakan Plotly Express
    fig = px.line(df_lab, x='KECAMATAN', y='Jumlah Lab', color='Lab')
    # Menampilkan grafik menggunakan Streamlit
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("See explanation"):
        st.write("""
            Grafik diatas menunjukan jumlah dan perbandingan fasilatas laboratorium di SMP Negeri Kota Bekasi per-Kecamatan.
            Fasilitas laboratorium dibagi menjadi 3 kategori yaitu Lab IPA, Lab Komputer dan Lab Bahasa.
            Umumnya SMP Negeri di kota bekasi memiliki jumlah lab komputer lebih banyak dibandingkan fasilitas laboratorium lainnya.
            Kecuali pada kecamatan Bekasi Utara dan Bantargebang yang memiliki jumlah lab IPA lebih banyak.
        """)

    # 5. Rasio Perbandingan murid/guru
    st.subheader('Rasio Perbandingan Jumlah Murid dengan Jumlah Guru SMP Negeri per-Kecamatan di Kota Bekasi')
    # Membuat bar chart menggunakan Plotly Express
    fig = px.bar(df_negeri, x='KECAMATAN', y=['JUMLAH TOTAL SISWA', 'JUMLAH TOTAL GURU SMP NEGERI'], barmode='group')
    # Mengatur layout agar grafik memenuhi lebar halaman
    fig.update_layout(width=1400)
    # Menampilkan grafik menggunakan Streamlit
    st.plotly_chart(fig)
    # Membuat menu dropdown untuk memilih kecamatan
    selected_kecamatan = st.selectbox('Pilih Kecamatan', df_negeri['KECAMATAN'])
    # Mendapatkan nilai rasio berdasarkan kecamatan yang dipilih
    rasio = df_negeri[df_negeri['KECAMATAN'] == selected_kecamatan]['RASIO (perbandingan Jumlah Murid dengan Jumlah Guru)'].values[0]
    # Menampilkan nilai rasio
    st.write('Rasio Perbandingan Jumlah Murid dengan Jumlah Guru', selected_kecamatan, ':', rasio)
    # Menghapus karakter "," dan mengonversi ke tipe numerik
    df_negeri['RASIO (perbandingan Jumlah Murid dengan Jumlah Guru)'] = df_negeri['RASIO (perbandingan Jumlah Murid dengan Jumlah Guru)'].str.replace(',', '.').astype(float)
    # Menghitung nilai rata-rata kolom rasio
    rata_rata_rasio_negeri = df_negeri['RASIO (perbandingan Jumlah Murid dengan Jumlah Guru)'].mean()
    rata_rata_rasio_negeri = int(rata_rata_rasio_negeri)
    # Menampilkan nilai rata-rata menggunakan Streamlit
    # Menampilkan nilai rata-rata di tengah-tengah halaman
    st.markdown("<h2 style='text-align: center;'>Nilai Rata-Rata Perbandingan Jumlah Murid dengan Jumlah Guru di SMP Negeri di Kota Bekasi:</h2>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center;'>{rata_rata_rasio_negeri}</h1>", unsafe_allow_html=True)
    with st.expander("See explanation"):
        st.write("""
            Grafik diatas menunjukan rasio perbandingan jumlah murid dengan jumlah guru di SMP Negeri Kota Bekasi.
            Nilai rata-rata yang didapatkan adalah 19, sehingga dapat disimpulkan setiap guru berbanding dengan 19 murid.
        """)

    # 6. Perbandingan Jumlah Murid dengan Jumlah Kelas -> LineChart
    st.subheader('Perbandingan Jumlah Murid dengan Jumlah Kelas')
    fig = px.line(df_negeri, x='KECAMATAN', y=['JUMLAH TOTAL SISWA', 'JUMLAH RUANG KELAS SMP NEGERI'])
    # Menampilkan line chart menggunakan Streamlit
    st.plotly_chart(fig, use_container_width=True)
    # Inisialisasi list untuk mengumpulkan nilai per kecamatan
    nilai_per_kecamatan = []
    # Mengatur layout grid dengan 2 baris dan 6 kolom
    columns = st.columns(6)
    # Iterasi setiap kecamatan
    for index, row in df_negeri.iterrows():
        kecamatan = row['KECAMATAN']
        jumlah_murid = row['JUMLAH TOTAL SISWA']
        jumlah_kelas = row['JUMLAH RUANG KELAS SMP NEGERI']
        # Menghitung rasio jumlah murid dengan jumlah kelas
        rasio = int(jumlah_murid / jumlah_kelas)
        # Menampilkan st.metric untuk setiap kecamatan
        with columns[index % 6]:
            st.metric(label=kecamatan, value=f"{rasio}")
            # Menambahkan nilai rasio per kecamatan ke list nilai_per_kecamatan
            nilai_per_kecamatan.append(rasio)
    # Menghitung rata-rata dari nilai per kecamatan
    rata_rata_jumlah_murid_perkelas = int(sum(nilai_per_kecamatan) / len(nilai_per_kecamatan))
    # Menampilkan nilai rata-rata
    #st.metric(label="Rata-rata", value=f"{rata_rata_jumlah_murid_perkelas:.2f}")
    # Menampilkan nilai rata-rata di tengah-tengah halaman
    st.markdown("<h2 style='text-align: center;'>Rata-Rata Jumlah Murid per Kelas di SMP Negeri di Kota Bekasi:</h2>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center;'>{rata_rata_jumlah_murid_perkelas}</h1>", unsafe_allow_html=True)
    with st.expander("See explanation"):
        st.write("""
            Grafik diatas menunjukan perbandingan jumlah murid dengan jumlah kelas.
            Rata-Rata yang didapatkan adalah 1 kelas SMP Negeri di Kota Bekasi berisikan 44 murid.
            Hal ini melampaui rasio murid dengan guru pada grafik sebelumnya.
            Jika 1 kelas hanya terdapat 1 guru maka jumlah murid pada 1 kelas terlampau banyak.
        """)

    # 7. Perbandingan guru bersertifikat
    st.subheader('Perbandingan Jumlah Guru Bersertifikat di SMP Negeri')
    # Membuat bar chart menggunakan Plotly Express
    fig = px.bar(df_negeri, x='KECAMATAN', y=['JUMLAH GURU SMP NEGERI YANG SUDAH SERTIFIKASI', 'JUMLAH TOTAL GURU SMP NEGERI'], barmode='group')
    # Mengatur layout agar grafik memenuhi lebar halaman
    fig.update_layout(width=1400)
    # Menampilkan grafik menggunakan Streamlit
    st.plotly_chart(fig)
    # Dropdown menu
    selected_kecamatan = st.selectbox('Pilih Kecamatan Sertifikasi Guru SMP Negeri', df_negeri['KECAMATAN'])
    # Ambil data persentase guru yang sudah bersertifikat
    guru_sertifikasi = df_negeri.loc[df_negeri['KECAMATAN'] == selected_kecamatan, 'JUMLAH GURU SMP NEGERI YANG SUDAH SERTIFIKASI'].values[0]
    total_guru = df_negeri.loc[df_negeri['KECAMATAN'] == selected_kecamatan, 'JUMLAH TOTAL GURU SMP NEGERI'].values[0]
    persentase_sertifikasi = guru_sertifikasi / total_guru * 100
    # Format persentase sebagai string dengan 2 angka di belakang koma
    persentase_formatted = "{:.2f} %".format(persentase_sertifikasi)
    # Tampilkan data persentase guru yang sudah bersertifikat
    st.metric(label='Persentase Guru Sertifikasi', value=persentase_formatted)
    # Hitung rata-rata persentase guru bersertifikat per kecamatan
    rata_rata_sertifikasi = df_negeri['JUMLAH GURU SMP NEGERI YANG SUDAH SERTIFIKASI'] / df_negeri['JUMLAH TOTAL GURU SMP NEGERI'] * 100
    rata_rata_sertifikasi = rata_rata_sertifikasi.mean()
    # Format rata-rata persentase sebagai string dengan 2 angka di belakang koma
    rata_rata_formatted = "{:.2f} %".format(rata_rata_sertifikasi)
    # Tampilkan data rata-rata persentase guru bersertifikat per kecamatan
    # Menampilkan nilai rata-rata di tengah-tengah halaman
    st.markdown("<h2 style='text-align: center;'>Rata-rata Persentase Guru bersertifikat di SMP Negeri Kota Bekasi:</h2>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center;'>{rata_rata_formatted}</h1>", unsafe_allow_html=True)
    with st.expander("See explanation"):
        st.write("""
            Grafik diatas menunjukan jumlah guru yang sudah bersertifikat di SMP Kota Bekasi.
            Nilai rata-rata yang didapat sebesar 42.39% guru SMP Negeri di Kota Bekasi sudah tersertifikasi.
        """)

    # 8. Perbandingan kualifikasi guru
    st.subheader('Perbandingan kualifikasi guru di SMP Negeri')
    # Membuat bar chart menggunakan Plotly Express
    fig = px.bar(df_negeri, x='KECAMATAN', y=['JUMLAH GURU SMP NEGERI KUALIFIKASI D3/D4', 'JUMLAH GURU SMP NEGERI KUALIFIKASI S1', 'JUMLAH GURU SMP NEGERI KUALIFIKASI S2'], barmode='group')
    # Mengatur layout agar grafik memenuhi lebar halaman
    fig.update_layout(width=1400)
    # Menampilkan grafik menggunakan Streamlit
    st.plotly_chart(fig)
    jumlah_s1 = df_negeri['JUMLAH GURU SMP NEGERI KUALIFIKASI S1'].sum()
    jumlah_s2 = df_negeri['JUMLAH GURU SMP NEGERI KUALIFIKASI S2'].sum()
    jumlah_d3_d4 = df_negeri['JUMLAH GURU SMP NEGERI KUALIFIKASI D3/D4'].sum()
    jumlahTotal_guru = df_negeri['JUMLAH TOTAL GURU SMP NEGERI'].sum()
    n_s2, n_s1, n_d3_d4 = st.columns(3)
    with n_s2:
        persentase_guru_S2_n = round(jumlah_s2/jumlahTotal_guru * 100, 2)
        st.metric(
            label='Jumlah Guru Kualifikasi S2',
            value=jumlah_s2,
        )
    with n_s1:
        persentase_guru_S1_n = round(jumlah_s1/jumlahTotal_guru * 100, 2)
        st.metric(
            label='Jumlah Guru Kualifikasi S1',
            value=jumlah_s1, 
        )
    with n_d3_d4:
        persentase_guru_d3_n = round(jumlah_d3_d4/jumlahTotal_guru * 100, 2)
        st.metric(
            label='Jumlah Guru Kualifikasi D3/D4',
            value=jumlah_d3_d4,
        )
    pn_s2, pn_s1, pn_d3_d4 = st.columns(3)
    with pn_s2:
        persentase_guru_S2_n = round(jumlah_s2/jumlahTotal_guru * 100, 2)
        st.metric(
            label='Jumlah Guru Kualifikasi S2',
            value=f"{persentase_guru_S2_n}%",
            #delta=f"{persentase_guru_S2_n}%"
        )
    with pn_s1:
        persentase_guru_S1_n = round(jumlah_s1/jumlahTotal_guru * 100, 2)
        st.metric(
            label='Jumlah Guru Kualifikasi S1',
            value=f"{persentase_guru_S1_n}%", 
            #delta=f"{persentase_guru_S1_n}%"
        )
    with pn_d3_d4:
        persentase_guru_d3_n = round(jumlah_d3_d4/jumlahTotal_guru * 100, 2)
        st.metric(
            label='Jumlah Guru Kualifikasi D3/D4',
            value=f"{persentase_guru_d3_n}%",
            #delta=f"{persentase_guru_d3_n}%"
        )
    with st.expander("See explanation"):
        st.write("""
            Grafik diatas menunjukan jumlah kualifikasi guru pada SMP negeri di Kota bekasi.
            dengan jumlah guru lulusan S1 terbanyak disusul dengan jumlah guru lulusan S2 dan Guru lulusan D3/D4.
        """)

with tab2:
    df_s = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vQJJf15EmuUIzpJ8y1ygBdBQGauVdCgq_r3a3AyVQmwsDEke26_jGTplruGriEswcpWLC0YpDTBXAhA/pub?output=csv')
    #df_s


    st.title('Data Sekolah Menengah Pertama (SMP) Swasta per-Kecamatan di Kota Bekasi')
    # 1. Jumlah Sekolah Per Kecamatan -> BarChart
    st.subheader('Jumlah Sekolah Per Kecamatan')
    st.bar_chart(data=df_s, x='KECAMATAN', y='JUMLAH SMP SWASTA', width=0, height=0, use_container_width=True)
    with st.expander("See explanation"):
        st.write("""
            Grafik di atas Merupakan data jumlah SMP Swasta per-kecamatan di kota bekasi.
            Dapat dilihat kecamatan Bekasi Utara menjadi kecamatan dengan jumlah SMP Swasta Terbanyak di Kota Bekasi.
        """)

    # 2. Perbandingan Akreditasi Sekolah -> LineChart
    st.subheader('Perbandingan Akreditasi Sekolah per-Kecamatan di Kota Bekasi')
    # Membuat DataFrame hanya dengan 4 kolom yang ingin ditampilkan
    df_akr_s = pd.DataFrame(df_s, columns=['KECAMATAN', 'TERAKREDITASI (A)', 'TERAKREDITASI (B)', 'TERAKREDITASI (C)', 'SEKOLAH MENENGAH PERTAMA (SMP) SWASTA BELUM TERAKREDITASI'])
    # Mengubah format data menjadi format yang cocok untuk line chart
    df_akr_s = df_akr_s.melt('KECAMATAN', var_name='Akreditasi', value_name='Jumlah Sekolah')
    # Membuat line chart menggunakan Plotly Express
    fig_s = px.line(df_akr_s, x='KECAMATAN', y='Jumlah Sekolah', color='Akreditasi')
    # Menampilkan grafik menggunakan Streamlit
    st.plotly_chart(fig_s, use_container_width=True)
    with st.expander("See explanation"):
        st.write("""
            Grafik diatas merupakan perbandingan akreditasi SMP Swasta di Kota bekasi Per-Kecamatan.
            Umumnya SMP Swasta di Kota Bekasi sudah berakreditasi (A)
        """)

    # 3. Matric Perbandingan Jumlah sekolah dengan akreditasi (A) dengan Total JUmlah sekolah per-Kecamatan
    st.subheader('Persentase sekolah dengan Akreditasi A per-Kecamatan di Kota Bekasi')
    # Menghitung persentase akreditasi A terhadap jumlah sekolah
    df_s['Persentase (A)'] = (df_s['TERAKREDITASI (A)'] / df_s['JUMLAH SMP SWASTA']) * 100
    # Menghitung jumlah baris dan kolom dalam layout
    total_kecamatan = len(df_s)
    num_columns = 6
    num_rows = math.ceil(total_kecamatan / num_columns)
    # Membagi layar menjadi 6 kolom
    columns = st.columns(num_columns)
    # Menampilkan metrik perbandingan persentase akreditasi A dengan jumlah sekolah di setiap kecamatan
    for kecamatan_index in range(total_kecamatan):
        with columns[kecamatan_index % num_columns]:
            kecamatan = df_s.loc[kecamatan_index, 'KECAMATAN']
            persentase_a_s = df_s.loc[kecamatan_index, 'Persentase (A)']
            st.metric(label=kecamatan, value=f'{persentase_a_s:.2f}%', delta_color='inverse')
    with st.expander("See explanation"):
        st.write("""
            Seluruh kecamatan di Kota Bekasi sudah memiliki persentase SMP Swasta berakreditasi A diatas 50%.
        """)

    # 4. Perbandingan jumlah lab -> LineChart
    st.subheader('Jumlah Lab di SMP Swasta per-Kecamatan di Kota Bekasi')
    # Menambahkan kolom Total Lab
    df_s['Total Lab s'] = df_s[['JUMLAH LABORATORIUM KOMPUTER', 'JUMLAH LABORATORIUM BAHASA', 'JUMLAH LABORATORIUM IPA']].sum(axis=1)
    # Membuat bar chart menggunakan Plotly Express
    fig_s = px.bar(df_s, x='KECAMATAN', y='Total Lab s', title='Perbandingan Total Lab per Kecamatan')
    # Menampilkan bar chart menggunakan st.plotly_chart
    st.plotly_chart(fig_s, use_container_width=True)
    # Membuat DataFrame hanya dengan 3 kolom yang ingin ditampilkan
    df_lab_s = pd.DataFrame(df_s, columns=['KECAMATAN', 'JUMLAH LABORATORIUM IPA', 'JUMLAH LABORATORIUM BAHASA', 'JUMLAH LABORATORIUM KOMPUTER'])
    # Mengubah format data menjadi format yang cocok untuk line chart
    df_lab_s = df_lab_s.melt('KECAMATAN', var_name='Lab', value_name='Jumlah Lab')
    # Membuat line chart menggunakan Plotly Express
    fig_s = px.line(df_lab_s, x='KECAMATAN', y='Jumlah Lab', color='Lab')
    # Menampilkan grafik menggunakan Streamlit
    st.plotly_chart(fig_s, use_container_width=True)
    with st.expander("See explanation"):
        st.write("""
            Grafik diatas menunjukan jumlah dan perbandingan fasilatas laboratorium di SMP Swasta Kota Bekasi per-Kecamatan.
            Fasilitas laboratorium dibagi menjadi 3 kategori yaitu Lab IPA, Lab Komputer dan Lab Bahasa.
            Umumnya SMP Swasta di kota bekasi memiliki jumlah lab komputer lebih banyak dibandingkan fasilitas laboratorium lainnya.
            Kecuali pada kecamatan medansatria dan Rawalumbu yang memiliki jumlah lab IPA lebih banyak.
        """)

    # 5. Rasio Perbandingan murid/guru
    st.subheader('Rasio Perbandingan Jumlah Murid dengan Jumlah Guru SMP Swasta per-Kecamatan di Kota Bekasi')
    # Membuat bar chart menggunakan Plotly Express
    fig_s = px.bar(df_s, x='KECAMATAN', y=['JUMLAH TOTAL SISWA', 'JUMLAH TOTAL GURU SMP SWASTA'], barmode='group')
    # Mengatur layout agar grafik memenuhi lebar halaman
    #fig_s.update_layout(width=1400)
    # Menampilkan grafik menggunakan Streamlit
    st.plotly_chart(fig_s, use_container_width=True)
    # Membuat menu dropdown untuk memilih kecamatan
    selected_kecamatan_s = st.selectbox('Pilih Kecamatan Sekolah Swasta', df_s['KECAMATAN'])
    # Mendapatkan nilai rasio berdasarkan kecamatan yang dipilih
    rasio_s = df_s[df_s['KECAMATAN'] == selected_kecamatan_s]['RASIO (perbandingan Jumlah Murid dengan Jumlah Guru)'].values[0]
    # Menampilkan nilai rasio
    st.write('Rasio Perbandingan Jumlah Murid dengan Jumlah Guru', selected_kecamatan_s, ':', rasio_s)
    # Menghapus karakter "," dan mengonversi ke tipe numerik
    df_s['RASIO (perbandingan Jumlah Murid dengan Jumlah Guru)'] = df_s['RASIO (perbandingan Jumlah Murid dengan Jumlah Guru)'].str.replace(',', '.').astype(float)
    # Menghitung nilai rata-rata kolom rasio
    rata_rata_rasio_s = df_s['RASIO (perbandingan Jumlah Murid dengan Jumlah Guru)'].mean()
    rata_rata_rasio_s = int(rata_rata_rasio_s)
    # Menampilkan nilai rata-rata menggunakan Streamlit
    # Menampilkan nilai rata-rata di tengah-tengah halaman
    st.markdown("<h2 style='text-align: center;'>Nilai Rata-Rata Perbandingan Jumlah Murid dengan Jumlah Guru di SMP Swasta di Kota Bekasi:</h2>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center;'>{rata_rata_rasio_s}</h1>", unsafe_allow_html=True)
    with st.expander("See explanation"):
        st.write("""
            Grafik diatas menunjukan rasio perbandingan jumlah murid dengan jumlah guru di SMP Swasta Kota Bekasi.
            Nilai rata-rata yang didapatkan adalah 10, sehingga dapat disimpulkan setiap guru berbanding dengan 10 murid.
        """)

    # 6. Perbandingan Jumlah Murid dengan Jumlah Kelas -> LineChart
    st.subheader('Perbandingan Jumlah Murid dengan Jumlah Kelas')
    fig_s = px.line(df_s, x='KECAMATAN', y=['JUMLAH TOTAL SISWA', 'JUMLAH RUANG KELAS SMP SWASTA'])
    # Menampilkan line chart menggunakan Streamlit
    st.plotly_chart(fig_s, use_container_width=True)
    # Inisialisasi list untuk mengumpulkan nilai per kecamatan
    nilai_per_kecamatan_s = []
    # Mengatur layout grid dengan 2 baris dan 6 kolom
    columns = st.columns(6)
    # Iterasi setiap kecamatan
    for index, row in df_s.iterrows():
        kecamatan = row['KECAMATAN']
        jumlah_murid = row['JUMLAH TOTAL SISWA']
        jumlah_kelas = row['JUMLAH RUANG KELAS SMP SWASTA']
        # Menghitung rasio jumlah murid dengan jumlah kelas
        rasio_s = int(jumlah_murid / jumlah_kelas)
        # Menampilkan st.metric untuk setiap kecamatan
        with columns[index % 6]:
            st.metric(label=kecamatan, value=f"{rasio_s}")
            # Menambahkan nilai rasio per kecamatan ke list nilai_per_kecamatan
            nilai_per_kecamatan_s.append(rasio_s)
    # Menghitung rata-rata dari nilai per kecamatan
    rata_rata_jumlah_murid_perkelas_s = int(sum(nilai_per_kecamatan_s) / len(nilai_per_kecamatan_s))
    # Menampilkan nilai rata-rata
    #st.metric(label="Rata-rata", value=f"{rata_rata_jumlah_murid_perkelas:.2f}")
    # Menampilkan nilai rata-rata di tengah-tengah halaman
    st.markdown("<h2 style='text-align: center;'>Rata-Rata Jumlah Murid per Kelas di SMP SWASTA di Kota Bekasi:</h2>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center;'>{rata_rata_jumlah_murid_perkelas_s}</h1>", unsafe_allow_html=True)
    with st.expander("See explanation"):
        st.write("""
            Grafik diatas menunjukan perbandingan jumlah murid dengan jumlah kelas.
            Rata-Rata yang didapatkan adalah 1 kelas SMP Swasta di Kota Bekasi berisikan 18 murid.
            Hal ini melampaui rasio murid dengan guru pada grafik sebelumnya.
            Jika 1 kelas hanya terdapat 1 guru maka jumlah murid pada 1 kelas terlampau banyak.
        """)

    # 7. Perbandingan guru bersertifikat
    st.subheader('Perbandingan Jumlah Guru Bersertifikat di SMP Swasta')
    # Membuat bar chart menggunakan Plotly Express
    fig_s = px.bar(df_s, x='KECAMATAN', y=['JUMLAH GURU SMP SWASTA YANG SUDAH SERTIFIKASI', 'JUMLAH TOTAL GURU SMP SWASTA'], barmode='group')
    # Mengatur layout agar grafik memenuhi lebar halaman
    fig_s.update_layout(width=1400)
    # Menampilkan grafik menggunakan Streamlit
    st.plotly_chart(fig_s)
    # Dropdown menu
    selected_kecamatan = st.selectbox('Pilih Kecamatan Sertifikasi Guru SMP Swasta', df_s['KECAMATAN'])
    # Ambil data persentase guru yang sudah bersertifikat
    guru_sertifikasi_s = df_s.loc[df_s['KECAMATAN'] == selected_kecamatan, 'JUMLAH GURU SMP SWASTA YANG SUDAH SERTIFIKASI'].values[0]
    total_guru_s = df_s.loc[df_s['KECAMATAN'] == selected_kecamatan, 'JUMLAH TOTAL GURU SMP SWASTA'].values[0]
    persentase_sertifikasi_s = guru_sertifikasi_s / total_guru_s * 100
    # Format persentase sebagai string dengan 2 angka di belakang koma
    persentase_formatted_s = "{:.2f} %".format(persentase_sertifikasi_s)
    # Tampilkan data persentase guru yang sudah bersertifikat
    st.metric(label='Persentase Guru Sertifikasi', value=persentase_formatted_s)
    # Hitung rata-rata persentase guru bersertifikat per kecamatan
    rata_rata_sertifikasi_s = df_s['JUMLAH GURU SMP SWASTA YANG SUDAH SERTIFIKASI'] / df_s['JUMLAH TOTAL GURU SMP SWASTA'] * 100
    rata_rata_sertifikasi_s = rata_rata_sertifikasi_s.mean()
    # Format rata-rata persentase sebagai string dengan 2 angka di belakang koma
    rata_rata_formatted_s = "{:.2f} %".format(rata_rata_sertifikasi_s)
    # Tampilkan data rata-rata persentase guru bersertifikat per kecamatan
    # Menampilkan nilai rata-rata di tengah-tengah halaman
    st.markdown("<h2 style='text-align: center;'>Rata-rata Persentase Guru bersertifikat di SMP Swasta Kota Bekasi:</h2>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center;'>{rata_rata_formatted_s}</h1>", unsafe_allow_html=True)
    with st.expander("See explanation"):
        st.write("""
            Grafik diatas menunjukan jumlah guru yang sudah bersertifikat di SMP Swasta Kota Bekasi.
            Nilai rata-rata yang didapat sebesar 25.88% guru SMP Swasta di Kota Bekasi sudah tersertifikasi.
        """)

    # 8. Perbandingan kualifikasi guru
    st.subheader('Perbandingan kualifikasi guru di SMP Swasta')
    # Membuat bar chart menggunakan Plotly Express
    fig = px.bar(df_s, x='KECAMATAN', y=['JUMLAH GURU SMP SWASTA KUALIFIKASI D3/D4', 'JUMLAH GURU SMP SWASTA KUALIFIKASI S1', 'JUMLAH GURU SMP SWASTA KUALIFIKASI S2'], barmode='group')
    # Mengatur layout agar grafik memenuhi lebar halaman
    fig.update_layout(width=1400)
    # Menampilkan grafik menggunakan Streamlit
    st.plotly_chart(fig)
    jumlah_s1_s = df_s['JUMLAH GURU SMP SWASTA KUALIFIKASI S1'].sum()
    jumlah_s2_s = df_s['JUMLAH GURU SMP SWASTA KUALIFIKASI S2'].sum()
    jumlah_d3_d4_s = df_s['JUMLAH GURU SMP SWASTA KUALIFIKASI D3/D4'].sum()
    jumlahTotal_guru_s = df_s['JUMLAH TOTAL GURU SMP SWASTA'].sum()
    s_s2, s_s1, s_d3_d4 = st.columns(3)
    with s_s2:
        persentase_guru_S2_s = round(jumlah_s2_s/jumlahTotal_guru_s * 100, 2)
        st.metric(
            label='Jumlah Guru Kualifikasi S2',
            value=jumlah_s2_s,
        )
    with s_s1:
        persentase_guru_S1_s = round(jumlah_s1_s/jumlahTotal_guru_s * 100, 2)
        st.metric(
            label='Jumlah Guru Kualifikasi S1',
            value=jumlah_s1_s, 
        )
    with s_d3_d4:
        persentase_guru_d3_s = round(jumlah_d3_d4_s/jumlahTotal_guru_s * 100, 2)
        st.metric(
            label='Jumlah Guru Kualifikasi D3/D4',
            value=jumlah_d3_d4_s,
        )
    ps_s2, ps_s1, ps_d3_d4 = st.columns(3)
    with ps_s2:
        persentase_guru_S2_s = round(jumlah_s2_s/jumlahTotal_guru_s * 100, 2)
        st.metric(
            label='Jumlah Guru Kualifikasi S2',
            value=f"{persentase_guru_S2_s}%",
            #delta=f"{persentase_guru_S2_n}%"
        )
    with ps_s1:
        persentase_guru_S1_s = round(jumlah_s1_s/jumlahTotal_guru_s * 100, 2)
        st.metric(
            label='Jumlah Guru Kualifikasi S1',
            value=f"{persentase_guru_S1_s}%", 
            #delta=f"{persentase_guru_S1_n}%"
        )
    with ps_d3_d4:
        persentase_guru_d3_s = round(jumlah_d3_d4_s/jumlahTotal_guru_s * 100, 2)
        st.metric(
            label='Jumlah Guru Kualifikasi D3/D4',
            value=f"{persentase_guru_d3_s}%",
            #delta=f"{persentase_guru_d3_n}%"
        )
    with st.expander("See explanation"):
        st.write("""
            Grafik diatas menunjukan jumlah kualifikasi guru pada SMP Swasta di Kota bekasi.
            dengan jumlah guru lulusan S1 terbanyak disusul dengan jumlah guru lulusan S2 dan Guru lulusan D3/D4.
        """)

with tab3:
# Final. Perbandingan Negeri VS Swasta
    st.title('Perbandingan Data SMP Negeri dengan SMP Swasta')
    Jumlah_sekolah_s = df_s['JUMLAH SMP SWASTA'].sum()
    Jumlah_sekolah_n = df_negeri['JUMLAH SMP NEGERI'].sum()
    Jumlah_lab_s = (df_s['JUMLAH LABORATORIUM IPA'].sum() + df_s['JUMLAH LABORATORIUM KOMPUTER'].sum() + df_s['JUMLAH LABORATORIUM BAHASA'].sum())
    Jumlah_lab_n = (df_negeri['JUMLAH LABORATORIUM IPA'].sum() + df_negeri['JUMLAH LABORATORIUM KOMPUTER'].sum() + df_negeri['JUMLAH LABORATORIUM BAHASA'].sum())

    # Dataframe
    data_X = {
        'Jenis Sekolah': ['Negeri', 'Swasta'],
        'Jumlah Sekolah': [Jumlah_sekolah_n, Jumlah_sekolah_s],
        'Persentase Sertifikasi guru' : [rata_rata_formatted, rata_rata_formatted_s],
        'jumlah rata-rata murid per-Kelas' : [rata_rata_jumlah_murid_perkelas, rata_rata_jumlah_murid_perkelas_s],
        'persentase guru lulusan s1' : [persentase_guru_S1_n, persentase_guru_S1_s],
        'persentase guru lulusan s2' : [persentase_guru_S2_n, persentase_guru_S2_s],
        'persentase guru lulusan D3/D4' : [persentase_guru_d3_n, persentase_guru_d3_s],
        'jumlah laboratorium' : [Jumlah_lab_n, Jumlah_lab_s]
    }
    df_X = pd.DataFrame(data_X)
    #df_X

    chart_1,chart_2,chart_3 = st.columns(3)
    with chart_1:
        # Tampilkan bar chart menggunakan Altair
        chart = alt.Chart(df_X).mark_bar().encode(
        x='Jenis Sekolah',
        y='Jumlah Sekolah',
        color=alt.Color('Jenis Sekolah', legend=None),
        tooltip=['Jenis Sekolah', 'Jumlah Sekolah']
        )
        # Tampilkan chart menggunakan Streamlit
        st.altair_chart(chart, use_container_width=True)
    with chart_2:
        # Tampilkan bar chart menggunakan Altair
        chart = alt.Chart(df_X).mark_bar().encode(
        x='Jenis Sekolah',
        y='jumlah rata-rata murid per-Kelas',
        color=alt.Color('Jenis Sekolah', legend=None),
        tooltip=['Jenis Sekolah', 'jumlah rata-rata murid per-Kelas']
        )
        # Tampilkan chart menggunakan Streamlit
        st.altair_chart(chart, use_container_width=True)
    with chart_3:
        # Tampilkan bar chart menggunakan Altair
        chart = alt.Chart(df_X).mark_bar().encode(
        x='Jenis Sekolah',
        y='jumlah laboratorium',
        color=alt.Color('Jenis Sekolah', legend=None),
        tooltip=['Jenis Sekolah', 'jumlah laboratorium']
        )
        # Tampilkan chart menggunakan Streamlit
        st.altair_chart(chart, use_container_width=True)
    with st.expander("See explanation"):
        st.write("""
            Grafik diatas menunjukan perbandingan jumlah sekolah, jumlah murid per-kelas, dan jumlah laboratorium sekolah Negeri dan Swasta di Kota bekasi.
            Dapat dilihat, jumlah SMP Swasta lebih banyak dan jumlah fasilitas laboratorium SMP swasta juga lebih banyak.
            Namun, jumlah murid per-kelas pada SMP Negeri lebih banyak dibandingkan dengan SMP Swasta.
            Jika dilihat dari grafik ini jumlah murid perkelas yang telampau banyak dapat mempengaruhi beban kerja seorang guru.
            Jika dibandingkan dengan rasio jumlah murid dan jumlah guru, 1 orang guru di SMP negeri seharusnya hanya bertanggung jawab kepada 19 murid.
            Dan 1 orang guru SMP swasta bertanggung jawab terhadap 10 murid. Keduanya memang berada dibawah jumlah murid per-kelas, namun perbandingan jumlah murid SMP swasta per-kelas
            relatif tidak terlalu jauh dimana 1 kelas hanya diisi 18 murid berbanding jauh pada jumlah murid per-kelas pada SMP Negeri yang berisikan 44 murid.

        """)
    chart_4,chart_5,chart_6 = st.columns(3)
    with chart_4:
        # Tampilkan bar chart menggunakan Altair
        chart = alt.Chart(df_X).mark_bar().encode(
        x='Jenis Sekolah',
        y='persentase guru lulusan s1',
        color=alt.Color('Jenis Sekolah', legend=None),
        tooltip=['Jenis Sekolah', 'persentase guru lulusan s1']
        )
        # Tampilkan chart menggunakan Streamlit
        st.altair_chart(chart, use_container_width=True)
    with chart_5:
        # Tampilkan bar chart menggunakan Altair
        chart = alt.Chart(df_X).mark_bar().encode(
        x='Jenis Sekolah',
        y='persentase guru lulusan s2',
        color=alt.Color('Jenis Sekolah', legend=None),
        tooltip=['Jenis Sekolah', 'persentase guru lulusan s2']
        )
        # Tampilkan chart menggunakan Streamlit
        st.altair_chart(chart, use_container_width=True)
    with chart_6:
        # Tampilkan bar chart menggunakan Altair
        chart = alt.Chart(df_X).mark_bar().encode(
        x='Jenis Sekolah',
        y='persentase guru lulusan D3/D4',
        color=alt.Color('Jenis Sekolah', legend=None),
        tooltip=['Jenis Sekolah', 'persentase guru lulusan D3/D4']
        )
        # Tampilkan chart menggunakan Streamlit
        st.altair_chart(chart, use_container_width=True)
    with st.expander("See explanation"):
        st.write("""
            Grafik diatas menunjukan kualifikasi guru lulusan S1, S2, dan D3/D4.
            Persentase guru lulusan s1 lebih besar mengajar di SMP Swasta, 
            namun persentase guru lulusan S2 lebih besar di SMP Negeri.
            Persentase guru lulusan D3/D4 lebih besar di SMP Swasta.
            Grafik ini menunjukan sebenarnya kualitas guru SMP Negeri lebih baik dari guru SMP Swasta,
            jika dilihat dari persentase jumlah guru lulusan S2.
        """)
    # Menampilkan nilai rata-rata di tengah-tengah halaman
    st.markdown("<h2 style='text-align: center;'>Persentase Sertifikasi guru SMP Negeri dan SMP Swasta:</h2>", unsafe_allow_html=True)
    st.write(f"<h1 style='text-align: center;'>Negeri: {rata_rata_formatted}</h1>", unsafe_allow_html=True)
    st.write(f"<h1 style='text-align: center;'>Swasta: {rata_rata_formatted_s}</h1>", unsafe_allow_html=True)
    with st.expander("See explanation"):
        st.write("""
            Berikut adalah perbandingan persentase guru SMP Negeri dan SMP Swasta yang sudah bersertifikat.
            Dari hasil diatas juga dapat dilihat kulaitas guru SMP Negeri lebih baik jika mengacu pada persentase guru yang sudah bersertifikat.
        """)

    with st.expander("Lihat Kesimpulan"):
        st.write("""
            Meskipun fasilitas laboratorium, jumlah sekolah dan jumlah kelas SMP Swasta lebih banyak dibandingkan SMP Negeri,
            Sejatinya kualitas pengajar pada SMP Negeri tidak kalah dibandingkan dengan pengajar di SMP Swasta.
            Yang bisa ditingkatkan adalah penambahan jumlah kelas pada SMP Negeri, sehingga rasio jumlah murid perkelas tidak terlalu banyak.
            Sedangkan pada SMP Swasta dapat meningkatkan jumlah guru dengan kualifikasi lulusan s2 dan juga meningkatkan jumlah guru yang mengikuti sertifikasi.
        """)
