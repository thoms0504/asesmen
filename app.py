import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

# Konfigurasi halaman
st.set_page_config(
    page_title="Aplikasi Pengolahan Data Kompetensi",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_data():
    """Load data from CSV file"""
    try:
        # Ganti dengan path file CSV Anda
        df = pd.read_csv("hasil-manajerial-teknis.csv", encoding='utf-8')
        return df
    except Exception as e:
        try:
            # Coba dengan encoding alternatif
            df = pd.read_csv("hasil-manajerial-teknis.csv", encoding='latin-1')
            return df
        except Exception as e2:
            st.error(f"Error loading data: {e2}")
            return None

def create_spider_chart(data_row):
    """Create separate stacked spider charts for managerial and technical competencies"""
    
    # Definisi kompetensi manajerial dan teknis
    manajerial_labels = ['Integritas', 'Kerjasama', 'Komunikasi', 'Mengelola Perubahan', 
                        'Orientasi pada Hasil', 'Pelayanan Publik', 'Pengambilan Keputusan', 
                        'Pengembangan Diri', 'Perekat Bangsa']
    
    teknis_labels = ['Distribusi', 'IPDS', 'Neraca', 'Produksi', 'Sosial', 'Umum']
    
    # Kolom untuk level sekarang (biru - dalam)
    manajerial_sekarang = ['M1_0', 'M2_0', 'M3_0', 'M4_0', 'M5_0', 'M6_0', 'M7_0', 'M8_0', 'M9_0']
    teknis_sekarang = ['T1_0', 'T2_0', 'T3_0', 'T4_0', 'T5_0', 'T6_0']
    
    # Kolom untuk level atasnya (merah - luar)
    manajerial_atas = ['M1_1', 'M2_1', 'M3_1', 'M4_1', 'M5_1', 'M6_1', 'M7_1', 'M8_1', 'M9_1']
    teknis_atas = ['T1_1', 'T2_1', 'T3_1', 'T4_1', 'T5_1', 'T6_1']
    
    # Ambil nilai dari data
    manajerial_values_sekarang = [data_row[col] if col in data_row else 0 for col in manajerial_sekarang]
    manajerial_values_atas = [data_row[col] if col in data_row else 0 for col in manajerial_atas]
    teknis_values_sekarang = [data_row[col] if col in data_row else 0 for col in teknis_sekarang]
    teknis_values_atas = [data_row[col] if col in data_row else 0 for col in teknis_atas]
    
    # Hitung total untuk stacking (level sekarang + level atas)
    manajerial_total = [s + a for s, a in zip(manajerial_values_sekarang, manajerial_values_atas)]
    teknis_total = [s + a for s, a in zip(teknis_values_sekarang, teknis_values_atas)]
    
    # Buat subplot dengan 2 spider chart
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'polar'}, {'type': 'polar'}]],
        subplot_titles=('Kompetensi Manajerial', 'Kompetensi Teknis')
    )
    
    # Spider Chart 1: Manajerial
    # Layer 1 (dalam): Level Sekarang (biru)
    fig.add_trace(go.Scatterpolar(
        r=manajerial_values_sekarang,
        theta=manajerial_labels,
        fill='toself',
        name='Manajerial - Level Sekarang',
        line_color='blue',
        fillcolor='rgba(0, 0, 255, 0.4)',
        subplot='polar'
    ), row=1, col=1)
    
    # Layer 2 (luar): Total (Level Sekarang + Level Atas) (merah)
    fig.add_trace(go.Scatterpolar(
        r=manajerial_total,
        theta=manajerial_labels,
        fill='tonext',
        name='Manajerial - Level Atas',
        line_color='red',
        fillcolor='rgba(255, 0, 0, 0.3)',
        subplot='polar'
    ), row=1, col=1)
    
    # Garis ambang batas manajerial (4) - tutup loop untuk garis tidak terputus
    manajerial_threshold = [4] * len(manajerial_labels)
    manajerial_threshold.append(manajerial_threshold[0])  # Tutup loop
    manajerial_labels_closed = manajerial_labels + [manajerial_labels[0]]  # Tutup loop
    
    fig.add_trace(go.Scatterpolar(
        r=manajerial_threshold,
        theta=manajerial_labels_closed,
        mode='lines',
        name='Ambang Batas Manajerial (4)',
        line=dict(color='green', width=2, dash='dash'),
        subplot='polar'
    ), row=1, col=1)
    
    # Spider Chart 2: Teknis
    # Layer 1 (dalam): Level Sekarang (biru)
    fig.add_trace(go.Scatterpolar(
        r=teknis_values_sekarang,
        theta=teknis_labels,
        fill='toself',
        name='Teknis - Level Sekarang',
        line_color='blue',
        fillcolor='rgba(0, 0, 255, 0.4)',
        subplot='polar2'
    ), row=1, col=2)
    
    # Layer 2 (luar): Total (Level Sekarang + Level Atas) (merah)
    fig.add_trace(go.Scatterpolar(
        r=teknis_total,
        theta=teknis_labels,
        fill='tonext',
        name='Teknis - Level Atas',
        line_color='red',
        fillcolor='rgba(255, 0, 0, 0.3)',
        subplot='polar2'
    ), row=1, col=2)
    
    # Garis ambang batas teknis (7) - tutup loop untuk garis tidak terputus
    teknis_threshold = [7] * len(teknis_labels)
    teknis_threshold.append(teknis_threshold[0])  # Tutup loop
    teknis_labels_closed = teknis_labels + [teknis_labels[0]]  # Tutup loop
    
    fig.add_trace(go.Scatterpolar(
        r=teknis_threshold,
        theta=teknis_labels_closed,
        mode='lines',
        name='Ambang Batas Teknis (7)',
        line=dict(color='green', width=2, dash='dash'),
        subplot='polar2'
    ), row=1, col=2)
    
    # Update layout untuk kedua polar chart
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 6],  # Maksimum 6 untuk manajerial
                tickmode='linear',
                tick0=0,
                dtick=1
            )
        ),
        polar2=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(max(teknis_total) if teknis_total else [0], 10)],  # Dynamic untuk teknis
                tickmode='linear',
                tick0=0,
                dtick=1
            )
        ),
        showlegend=True,
        title="Spider Chart Kompetensi (Stacked)",
        font=dict(size=10),
        height=600
    )
    
    return fig

def create_competency_table(data_row, competency_type):
    """Create competency table for either managerial or technical competencies"""
    
    if competency_type == "manajerial":
        labels = {
            'M1': 'Integritas', 'M2': 'Kerjasama', 'M3': 'Komunikasi',
            'M4': 'Mengelola Perubahan', 'M5': 'Orientasi pada Hasil',
            'M6': 'Pelayanan Publik', 'M7': 'Pengambilan Keputusan',
            'M8': 'Pengembangan Diri', 'M9': 'Perekat Bangsa'
        }
        codes = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9']
    else:  # teknis
        labels = {
            'T1': 'Distribusi', 'T2': 'IPDS', 'T3': 'Neraca',
            'T4': 'Produksi', 'T5': 'Sosial', 'T6': 'Umum'
        }
        codes = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6']
    
    # Buat DataFrame untuk tabel
    table_data = []
    for code in codes:
        kompetensi = labels.get(code, code)
        nilai_selevel = data_row.get(f'{code}_0', 0)
        nilai_atas_level = data_row.get(f'{code}_1', 0)
        
        table_data.append({
            'Kompetensi': kompetensi,
            'Nilai Selevel': nilai_selevel,
            'Nilai di Atas Level': nilai_atas_level
        })
    
    df_table = pd.DataFrame(table_data)
    return df_table

def display_competency_data(data_row):
    """Display competency values in a structured format"""
    
    # Hitung total nilai manajerial (M1 = M1_0 + M1_1, dst)
    manajerial_totals = {}
    teknis_totals = {}
    
    for i in range(1, 10):  # M1-M9
        col_0 = f'M{i}_0'
        col_1 = f'M{i}_1'
        if col_0 in data_row and col_1 in data_row:
            manajerial_totals[f'M{i}'] = data_row[col_0] + data_row[col_1]
    
    for i in range(1, 7):  # T1-T6
        col_0 = f'T{i}_0'
        col_1 = f'T{i}_1'
        if col_0 in data_row and col_1 in data_row:
            teknis_totals[f'T{i}'] = data_row[col_0] + data_row[col_1]
    
    # Tampilkan dalam dua kolom
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Kompetensi Manajerial")
        manajerial_labels = {
            'M1': 'Integritas', 'M2': 'Kerjasama', 'M3': 'Komunikasi',
            'M4': 'Mengelola Perubahan', 'M5': 'Orientasi pada Hasil',
            'M6': 'Pelayanan Publik', 'M7': 'Pengambilan Keputusan',
            'M8': 'Pengembangan Diri', 'M9': 'Perekat Bangsa'
        }
        
        for code, total in manajerial_totals.items():
            label = manajerial_labels.get(code, code)
            sekarang = data_row.get(f'{code}_0', 0)
            atas = data_row.get(f'{code}_1', 0)
            st.write(f"**{label} ({code}):** {total} (Sekarang: {sekarang}, Atas: {atas})")
    
    with col2:
        st.subheader("Kompetensi Teknis")
        teknis_labels = {
            'T1': 'Distribusi', 'T2': 'IPDS', 'T3': 'Neraca',
            'T4': 'Produksi', 'T5': 'Sosial', 'T6': 'Umum'
        }
        
        for code, total in teknis_totals.items():
            label = teknis_labels.get(code, code)
            sekarang = data_row.get(f'{code}_0', 0)
            atas = data_row.get(f'{code}_1', 0)
            st.write(f"**{label} ({code}):** {total} (Sekarang: {sekarang}, Atas: {atas})")

def main():
    st.title("📊 Aplikasi Pengolahan Data Kompetensi")
    st.markdown("---")
    
    # Load data
    df = load_data()
    
    if df is None:
        st.error("Gagal memuat data. Pastikan file CSV tersedia.")
        st.warning("Silakan upload file CSV Anda:")
        uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
        if uploaded_file is not None:
            try:
                # Coba baca dengan encoding utf-8 terlebih dahulu
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            except UnicodeDecodeError:
                # Jika gagal, coba dengan latin-1
                df = pd.read_csv(uploaded_file, encoding='latin-1')
            except Exception as e:
                st.error(f"Error reading uploaded file: {e}")
                df = None
    
    if df is not None:
        # Menu sidebar
        menu = st.sidebar.selectbox(
            "Pilih Menu:",
            ["Tampilkan Tabel", "Pencarian berdasarkan NIP"]
        )
        
        if menu == "Tampilkan Tabel":
            st.header("📋 Data Tabel dengan Filter")
            
            # Hitung M_Total dan T_Total untuk semua data
            df_processed = df.copy()
            
            # Hitung M_Total (M1 sampai M9)
            m_columns = []
            for i in range(1, 10):
                col_0 = f'M{i}_0'
                col_1 = f'M{i}_1'
                if col_0 in df.columns and col_1 in df.columns:
                    df_processed[f'M{i}'] = df_processed[col_0] + df_processed[col_1]
                    m_columns.append(f'M{i}')
            
            if m_columns:
                df_processed['M_Total'] = df_processed[m_columns].sum(axis=1)
            else:
                df_processed['M_Total'] = 0
            
            # Hitung T_Total (T1 sampai T6)
            t_columns = []
            for i in range(1, 7):
                col_0 = f'T{i}_0'
                col_1 = f'T{i}_1'
                if col_0 in df.columns and col_1 in df.columns:
                    df_processed[f'T{i}'] = df_processed[col_0] + df_processed[col_1]
                    t_columns.append(f'T{i}')
            
            if t_columns:
                df_processed['T_Total'] = df_processed[t_columns].sum(axis=1)
            else:
                df_processed['T_Total'] = 0
            
            # Filter controls
            st.subheader("🔍 Filter Data")
            col1, col2 = st.columns(2)
            
            
            with col1:
                # Filter berdasarkan Level (assumsi ada kolom Level)
                if 'Level' in df_processed.columns:
                    unique_levels = ['Semua'] + sorted(df_processed['Level'].dropna().unique().tolist())
                    selected_level = st.selectbox("Filter Level:", unique_levels)
                else:
                    st.warning("Kolom 'Level' tidak ditemukan")
                    selected_level = "Semua"
            
            with col2:
                # Filter berdasarkan Nama Wilayah
                if 'Nama Wilayah' in df_processed.columns:
                    unique_wilayah = ['Semua'] + sorted(df_processed['Nama Wilayah'].dropna().unique().tolist())
                    selected_wilayah = st.selectbox("Filter Nama Wilayah:", unique_wilayah)
                else:
                    st.warning("Kolom 'Nama Wilayah' tidak ditemukan")
                    selected_wilayah = "Semua"
            
            # Apply filters
            filtered_df = df_processed.copy()
            
            # Filter berdasarkan nama
            
            # Filter berdasarkan level
            if selected_level != "Semua" and 'Level' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['Level'] == selected_level]
            
            # Filter berdasarkan wilayah
            if selected_wilayah != "Semua" and 'Nama Wilayah' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['Nama Wilayah'] == selected_wilayah]
            
            # Pilih kolom untuk ditampilkan
            display_columns = ['Nama Pegawai', 'Nama Wilayah', 'Jabatan', 'M_Total', 'T_Total']
            available_columns = [col for col in display_columns if col in filtered_df.columns]
            display_df = filtered_df[available_columns].copy()
            
            # Rename kolom untuk tampilan yang lebih baik
            column_rename = {
                'Nama Pegawai': 'Nama',
                'Nama Wilayah': 'Wilayah',
                'Jabatan': 'Jabatan',
                'M_Total': 'Nilai Manajerial',
                'T_Total': 'Nilai Teknis',
            }
            display_df = display_df.rename(columns=column_rename)
            
            st.markdown("---")
            
            # Tampilkan statistik
            if not filtered_df.empty:
                st.subheader("📊 Statistik Data Terfilter")
                
                # Hitung statistik
                m_total_avg = filtered_df['M_Total'].mean()
                t_total_avg = filtered_df['T_Total'].mean()
                total_data = len(filtered_df)
                
                # Tampilkan dalam metric cards
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Jumlah Data", f"{total_data:,}")
                with col2:
                    st.metric("Rata-rata M_Total", f"{m_total_avg:.2f}")
                with col3:
                    st.metric("Rata-rata T_Total", f"{t_total_avg:.2f}")
                
                # Statistik tambahan
                st.markdown("### 📈 Statistik Detail")
                stats_col1, stats_col2 = st.columns(2)
                
                with stats_col1:
                    with st.container():
                        st.markdown("""
                        <div style="
                            background-color: #f0f8ff;
                            padding: 20px;
                            border-radius: 10px;
                            border-left: 5px solid #4CAF50;
                            margin-bottom: 20px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        ">
                            <h3 style="color: #2E8B57; margin-top: 0;">🏢 Kompetensi Manajerial</h3>
                        """, unsafe_allow_html=True)
                        
                        col1, col2, col3, col4 = st.columns(4)
                        avg_manajerial = filtered_df['M_Total'].mean()
                        min_manajerial = filtered_df['M_Total'].min()
                        max_manajerial = filtered_df['M_Total'].max()
                        std_manajerial = filtered_df['M_Total'].std()
                    
                        with col1:
                            st.metric("Rata-rata", f"{avg_manajerial:.2f}")
                        with col2:
                            st.metric("Minimum", f"{min_manajerial:.2f}")
                        with col3:
                            st.metric("Maksimum", f"{max_manajerial:.2f}")
                        with col4:
                            st.metric("Std Deviasi", f"{std_manajerial:.2f}")
                        
                        st.markdown("</div>", unsafe_allow_html=True)

                with stats_col2:
                    with st.container():
                        st.markdown("""
                        <div style="
                            background-color: #f0fff0;
                            padding: 20px;
                            border-radius: 10px;
                            border-left: 5px solid #FF6347;
                            margin-bottom: 20px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        ">
                            <h3 style="color: #FF4500; margin-top: 0;">⚙️ Kompetensi Teknis</h3>
                        """, unsafe_allow_html=True)
                        
                        col1, col2, col3, col4 = st.columns(4)
                        avg_teknis = filtered_df['T_Total'].mean()
                        min_teknis = filtered_df['T_Total'].min()
                        max_teknis = filtered_df['T_Total'].max()
                        std_teknis = filtered_df['T_Total'].std()
                    
                        with col1:
                            st.metric("Rata-rata", f"{avg_teknis:.2f}")
                        with col2:
                            st.metric("Minimum", f"{min_teknis:.2f}")
                        with col3:
                            st.metric("Maksimum", f"{max_teknis:.2f}")
                        with col4:
                            st.metric("Std Deviasi", f"{std_teknis:.2f}")
                        
                        st.markdown("</div>", unsafe_allow_html=True)

                
                st.markdown("---")
                
                # Tampilkan tabel
                st.subheader("📋 Tabel Data")
                st.dataframe(display_df, use_container_width=True, height=400)
                
                # Info jumlah data
                st.success(f"Menampilkan {len(display_df)} dari {len(df)} data total")
                
                # Download button
                
                
            else:
                st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
        
        elif menu == "Pencarian berdasarkan NIP":
            st.header("🔍 Pencarian Data berdasarkan NIP")
            
            # Input NIP
            nip_input = st.text_input("Masukkan NIP:", placeholder="Contoh: 199702220701110024")
            
            if nip_input:
                # Cari data berdasarkan NIP
                matching_data = df[df['NIP'].astype(str).str.contains(nip_input, na=False)]
                
                if not matching_data.empty:
                    # Ambil data pertama jika ada lebih dari satu
                    data_row = matching_data.iloc[0]
                    
                    # Tampilkan informasi dasar
                    st.subheader("ℹ️ Informasi Pegawai")
                    
                    st.success(f"Nama: {data_row.get('Nama Pegawai', 'N/A')}")
                    st.success(f"NIP: {data_row.get('NIP', 'N/A')}")
                    st.success(f"Jabatan: {data_row.get('Jabatan', 'N/A')}")
                    st.success(f"Wilayah: {data_row.get('Nama Wilayah', 'N/A')}")
                    
                    st.markdown("---")
                    
                    # Tampilkan spider chart
                    st.subheader("📊 Spider Chart Kompetensi")
                    spider_chart = create_spider_chart(data_row)
                    st.plotly_chart(spider_chart, use_container_width=True)
                    
                    st.markdown("---")
                    
                    # Tampilkan detail nilai kompetensi dengan tombol
                    st.subheader("📈 Detail Nilai Kompetensi")
                    
                    # Inisialisasi session state dengan key unik untuk NIP
                    nip_key = f"competency_view_{data_row.get('NIP', 'default')}"
                    if nip_key not in st.session_state:
                        st.session_state[nip_key] = 'manajerial'
                    
                    # Buat dua tombol untuk memilih jenis kompetensi
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🏢 Manajerial", use_container_width=True, key="btn_manajerial"):
                            st.session_state[nip_key] = 'manajerial'
                    with col2:
                        if st.button("⚙️ Teknis", use_container_width=True, key="btn_teknis"):
                            st.session_state[nip_key] = 'teknis'
                    
                    # Tampilkan tabel berdasarkan pilihan
                    st.markdown("---")
                    
                    # Debug info (hapus jika sudah berfungsi)
                    # st.write(f"Current view: {st.session_state[nip_key]}")
                    
                    if st.session_state[nip_key] == 'manajerial':
                        st.subheader("🏢 Tabel Kompetensi Manajerial")
                        
                        # Buat tabel manajerial
                        manajerial_table = create_competency_table(data_row, 'manajerial')
                        
                        # Tampilkan tabel tanpa styling kompleks dulu
                        st.dataframe(manajerial_table, use_container_width=True, height=400)
                        
                        # Tampilkan total
                        total_selevel = manajerial_table['Nilai Selevel'].sum()
                        total_atas = manajerial_table['Nilai di Atas Level'].sum()
                        total_keseluruhan = total_selevel + total_atas
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Nilai Selevel", int(total_selevel))
                        with col2:
                            st.metric("Total Nilai Atas Level", int(total_atas))
                        with col3:
                            st.metric("Total Keseluruhan", int(total_keseluruhan))
                    
                    elif st.session_state[nip_key] == 'teknis':
                        st.subheader("⚙️ Tabel Kompetensi Teknis")
                        
                        # Buat tabel teknis
                        teknis_table = create_competency_table(data_row, 'teknis')
                        
                        # Tampilkan tabel tanpa styling kompleks dulu
                        st.dataframe(teknis_table, use_container_width=True, height=300)
                        
                        # Tampilkan total
                        total_selevel = teknis_table['Nilai Selevel'].sum()
                        total_atas = teknis_table['Nilai di Atas Level'].sum()
                        total_keseluruhan = total_selevel + total_atas
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Nilai Selevel", int(total_selevel))
                        with col2:
                            st.metric("Total Nilai Atas Level", int(total_atas))
                        with col3:
                            st.metric("Total Keseluruhan", int(total_keseluruhan))
                    
                    # Tampilkan tabel manajerial secara default juga (untuk debugging)
                    # if st.session_state[nip_key] == 'manajerial':
                    #     # Debug: tampilkan data mentah
                    #     with st.expander("🔍 Debug: Lihat Data Mentah Manajerial"):
                    #         debug_data = {}
                    #         for i in range(1, 10):
                    #             m_code = f'M{i}'
                    #             m0_col = f'M{i}_0'
                    #             m1_col = f'M{i}_1'
                    #             debug_data[m_code] = {
                    #                 'Selevel': data_row.get(m0_col, 0),
                    #                 'Atas Level': data_row.get(m1_col, 0)
                    #             }
                    #         st.json(debug_data)
                
                else:
                    st.error(f"Data dengan NIP '{nip_input}' tidak ditemukan.")
                    
                    # Suggest similar NIPs
                    similar_nips = df[df['NIP'].astype(str).str.contains(nip_input[:8] if len(nip_input) > 8 else nip_input, na=False)]['NIP'].head(5)
                    if not similar_nips.empty:
                        st.warning("NIP yang mirip:")
                        for nip in similar_nips:
                            st.write(f"- {nip}")

if __name__ == "__main__":
    main()