import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re

# Import untuk stopwords bahasa Indonesia
try:
    from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
    stopword_factory = StopWordRemoverFactory()
    stopword_remover = stopword_factory.create_stop_word_remover()
    SASTRAWI_AVAILABLE = True
except ImportError:
    SASTRAWI_AVAILABLE = False
    # Fallback stopwords Indonesia
    INDONESIAN_STOPWORDS = {
        'yang', 'untuk', 'pada', 'dalam', 'dengan', 'ini', 'itu', 'dan', 'di', 'ke', 'dari', 
        'oleh', 'saya', 'akan', 'adalah', 'atau', 'juga', 'dapat', 'karena', 'sebagai',
        'ada', 'tidak', 'sudah', 'lebih', 'bisa', 'telah', 'harus', 'sebuah', 'sangat',
        'bps', 'kabupaten', 'kota', 'provinsi', 'lampung',
        "ada","adalah","adanya","adapun","agak","agaknya","agar","akan","akankah","akhir","akhiri","akhirnya","aku","akulah","amat","amatlah","anda","andalah","antar","antara","antaranya","apa","apaan","apabila","apakah","apalagi","apatah","artinya","asal","asalkan","atas","atau","ataukah","ataupun","awal","awalnya","bagai","bagaikan","bagaimana","bagaimanakah","bagaimanapun","bagi","bagian","bahkan","bahwa","bahwasanya","baik","bakal","bakalan","balik","banyak","bapak","baru","bawah","beberapa","begini","beginian","beginikah","beginilah","begitu","begitukah","begitulah","begitupun","bekerja","belakang","belakangan","belum","belumlah","benar","benarkah","benarlah","berada","berakhir","berakhirlah","berakhirnya","berapa","berapakah","berapalah","berapapun","berarti","berawal","berbagai","berdatangan","beri","berikan","berikut","berikutnya","berjumlah","berkali-kali","berkata","berkehendak","berkeinginan","berkenaan","berlainan","berlalu","berlangsung","berlebihan","bermacam","bermacam-macam","bermaksud","bermula","bersama","bersama-sama","bersiap","bersiap-siap","bertanya","bertanya-tanya","berturut","berturut-turut","bertutur","berujar","berupa","besar","betul","betulkah","biasa","biasanya","bila","bilakah","bisa","bisakah","boleh","bolehkah","bolehlah","buat","bukan","bukankah","bukanlah","bukannya","bulan","bung","cara","caranya","cukup","cukupkah","cukuplah","cuma","dahulu","dalam","dan","dapat","dari","daripada","datang","dekat","demi","demikian","demikianlah","dengan","depan","di","dia","diakhiri","diakhirinya","dialah","diantara","diantaranya","diberi","diberikan","diberikannya","dibuat","dibuatnya","didapat","didatangkan","digunakan","diibaratkan","diibaratkannya","diingat","diingatkan","diinginkan","dijawab","dijelaskan","dijelaskannya","dikarenakan","dikatakan","dikatakannya","dikerjakan","diketahui","diketahuinya","dikira","dilakukan","dilalui","dilihat","dimaksud","dimaksudkan","dimaksudkannya","dimaksudnya","diminta","dimintai","dimisalkan","dimulai","dimulailah","dimulainya","dimungkinkan","dini","dipastikan","diperbuat","diperbuatnya","dipergunakan","diperkirakan","diperlihatkan","diperlukan","diperlukannya","dipersoalkan","dipertanyakan","dipunyai","diri","dirinya","disampaikan","disebut","disebutkan","disebutkannya","disini","disinilah","ditambahkan","ditandaskan","ditanya","ditanyai","ditanyakan","ditegaskan","ditujukan","ditunjuk","ditunjuki","ditunjukkan","ditunjukkannya","ditunjuknya","dituturkan","dituturkannya","diucapkan","diucapkannya","diungkapkan","dong","dua","dulu","empat","enggak","enggaknya","entah","entahlah","guna","gunakan","hal","hampir","hanya","hanyalah","hari","harus","haruslah","harusnya","hendak","hendaklah","hendaknya","hingga","ia","ialah","ibarat","ibaratkan","ibaratnya","ibu","ikut","ingat","ingat-ingat","ingin","inginkah","inginkan","ini","inikah","inilah","itu","itukah","itulah","jadi","jadilah","jadinya","jangan","jangankan","janganlah","jauh","jawab","jawaban","jawabnya","jelas","jelaskan","jelaslah","jelasnya","jika","jikalau","juga","jumlah","jumlahnya","justru","kala","kalau","kalaulah","kalaupun","kalian","kami","kamilah","kamu","kamulah","kan","kapan","kapankah","kapanpun","karena","karenanya","kasus","kata","katakan","katakanlah","katanya","ke","keadaan","kebetulan","kecil","kedua","keduanya","keinginan","kelamaan","kelihatan","kelihatannya","kelima","keluar","kembali","kemudian","kemungkinan","kemungkinannya","kenapa","kepada","kepadanya","kesampaian","keseluruhan","keseluruhannya","keterlaluan","ketika","khususnya","kini","kinilah","kira","kira-kira","kiranya","kita","kitalah","kok","kurang","lagi","lagian","lah","lain","lainnya","lalu","lama","lamanya","lanjut","lanjutnya","lebih","lewat","lima","luar","macam","maka","makanya","makin","malah","malahan","mampu","mampukah","mana","manakala","manalagi","masa","masalah","masalahnya","masih","masihkah","masing","masing-masing","mau","maupun","melainkan","melakukan","melalui","melihat","melihatnya","memang","memastikan","memberi","memberikan","membuat","memerlukan","memihak","meminta","memintakan","memisalkan","memperbuat","mempergunakan","memperkirakan","memperlihatkan","mempersiapkan","mempersoalkan","mempertanyakan","mempunyai","memulai","memungkinkan","menaiki","menambahkan","menandaskan","menanti","menanti-nanti","menantikan","menanya","menanyai","menanyakan","mendapat","mendapatkan","mendatang","mendatangi","mendatangkan","menegaskan","mengakhiri","mengapa","mengatakan","mengatakannya","mengenai","mengerjakan","mengetahui","menggunakan","menghendaki","mengibaratkan","mengibaratkannya","mengingat","mengingatkan","menginginkan","mengira","mengucapkan","mengucapkannya","mengungkapkan","menjadi","menjawab","menjelaskan","menuju","menunjuk","menunjuki","menunjukkan","menunjuknya","menurut","menuturkan","menyampaikan","menyangkut","menyatakan","menyebutkan","menyeluruh","menyiapkan","merasa","mereka","merekalah","merupakan","meski","meskipun","meyakini","meyakinkan","minta","mirip","misal","misalkan","misalnya","mula","mulai","mulailah","mulanya","mungkin","mungkinkah","nah","naik","namun","nanti","nantinya","nyaris","nyatanya","oleh","olehnya","pada","padahal","padanya","pak","paling","panjang","pantas","para","pasti","pastilah","penting","pentingnya","per","percuma","perlu","perlukah","perlunya","pernah","persoalan","pertama","pertama-tama","pertanyaan","pertanyakan","pihak","pihaknya","pukul","pula","pun","punya","rasa","rasanya","rata","rupanya","saat","saatnya","saja","sajalah","saling","sama","sama-sama","sambil","sampai","sampai-sampai","sampaikan","sana","sangat","sangatlah","satu","saya","sayalah","se","sebab","sebabnya","sebagai","sebagaimana","sebagainya","sebagian","sebaik","sebaik-baiknya","sebaiknya","sebaliknya","sebanyak","sebegini","sebegitu","sebelum","sebelumnya","sebenarnya","seberapa","sebesar","sebetulnya","sebisanya","sebuah","sebut","sebutlah","sebutnya","secara","secukupnya","sedang","sedangkan","sedemikian","sedikit","sedikitnya","seenaknya","segala","segalanya","segera","seharusnya","sehingga","seingat","sejak","sejauh","sejenak","sejumlah","sekadar","sekadarnya","sekali","sekali-kali","sekalian","sekaligus","sekalipun","sekarang","sekecil","seketika","sekiranya","sekitar","sekitarnya","sekurang-kurangnya","sekurangnya","sela","selagi","selain","selaku","selalu","selama","selama-lamanya","selamanya","selanjutnya","seluruh","seluruhnya","semacam","semakin","semampu","semampunya","semasa","semasih","semata","semata-mata","semaunya","sementara","semisal","semisalnya","sempat","semua","semuanya","semula","sendiri","sendirian","sendirinya","seolah","seolah-olah","seorang","sepanjang","sepantasnya","sepantasnyalah","seperlunya","seperti","sepertinya","sepihak","sering","seringnya","serta","serupa","sesaat","sesama","sesampai","sesegera","sesekali","seseorang","sesuatu","sesuatunya","sesudah","sesudahnya","setelah","setempat","setengah","seterusnya","setiap","setiba","setibanya","setidak-tidaknya","setidaknya","setinggi","seusai","sewaktu","siap","siapa","siapakah","siapapun","sini","sinilah","soal","soalnya","suatu","sudah","sudahkah","sudahlah","supaya","tadi","tadinya","tahu","tahun","tak","tambah","tambahnya","tampak","tampaknya","tandas","tandasnya","tanpa","tanya","tanyakan","tanyanya","tapi","tegas","tegasnya","telah","tempat","tengah","tentang","tentu","tentulah","tentunya","tepat","terakhir","terasa","terbanyak","terdahulu","terdapat","terdiri","terhadap","terhadapnya","teringat","teringat-ingat","terjadi","terjadilah","terjadinya","terkira","terlalu","terlebih","terlihat","termasuk","ternyata","tersampaikan","tersebut","tersebutlah","tertentu","tertuju","terus","terutama","tetap","tetapi","tiap","tiba","tiba-tiba","tidak","tidakkah","tidaklah","tiga","tinggi","toh","tunjuk","turut","tutur","tuturnya","ucap","ucapnya","ujar","ujarnya","umum","umumnya","ungkap","ungkapnya","untuk","usah","usai","waduh","wah","wahai","waktu","waktunya","walau","walaupun","wong","yaitu","yakin","yakni","yang", 'yuk', 'ayo', 'ayo yuk', 'ayo aja', 'ayo dong', 'ayo yuk dong', 'ayo aja yuk', 'ayo dong yuk', 'ayo dong aja', 'ayo yuk aja', 'ayo yuk dong aja'
    }

# Konfigurasi halaman (kode CSS dan fungsi lainnya tetap sama)
st.set_page_config(
    page_title="Aplikasi Pengolahan Data Kompetensi",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# [Semua fungsi CSS dan helper functions yang sudah ada tetap sama...]
# Custom CSS untuk styling yang lebih menarik
def load_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Reset font family */
    .stApp {
        font-family: 'Inter', sans-serif;
        
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        margin: 1rem;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Card styling */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        margin: 0.5rem 0;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
        font-weight: 500;
    }
    
    /* Info cards */
    .info-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    .info-card h3 {
        color: #667eea;
        margin-top: 0;
        font-weight: 600;
    }
    
    /* Success cards */
    .success-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.3);
        font-weight: 500;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .css-1d391kg .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
    }
    
    /* Table styling */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background: rgba(102, 126, 234, 0.1);
        border-radius: 15px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Section dividers */
    .section-divider {
        height: 3px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 2px;
        margin: 2rem 0;
    }
    
    /* Animation for loading */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .loading {
        animation: pulse 2s infinite;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
            margin: 0.5rem;
        }
        
        .metric-value {
            font-size: 2rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

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

@st.cache_data
def load_pemetaan_data():
    """Load data pemetaan from Excel file"""
    try:
        df = pd.read_excel("pemetaan.xlsx")
        return df
    except Exception as e:
        st.error(f"Error loading pemetaan data: {e}")
        return None

def clean_text_for_wordcloud(text):
    """Clean and process text for wordcloud"""
    if pd.isna(text) or text == '':
        return ""
    
    # Convert to lowercase
    text = str(text).lower()
    
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove stopwords
    if SASTRAWI_AVAILABLE:
        text = stopword_remover.remove(text)
    else:
        words = text.split()
        text = ' '.join([word for word in words if word not in INDONESIAN_STOPWORDS])
    
    return text

def create_wordcloud(text_data, title="WordCloud"):
    """Create wordcloud from text data"""
    # Combine all text
    all_text = ' '.join([clean_text_for_wordcloud(text) for text in text_data if pd.notna(text)])
    
    if not all_text.strip():
        return None
    
    # Create wordcloud
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='white',
        colormap='viridis',
        max_words=100,
        relative_scaling=0.5
    ).generate(all_text)
    
    # Create matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    
    return fig

def create_jalur_jabatan_chart(df_pemetaan):
    """Create bar chart for jalur jabatan comparison"""
    # Count jalur jabatan
    jalur_counts = df_pemetaan['Q01_JALUR PENGEMBANGAN KARIR'].value_counts()
    
    # Create bar chart
    fig = px.bar(
        x=jalur_counts.index,
        y=jalur_counts.values,
        title="Perbandingan Jalur Pengembangan Karir",
        labels={'x': 'Jalur Jabatan', 'y': 'Jumlah Pegawai'},
        color=jalur_counts.values,
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(
        height=500,
        showlegend=False,
        title_x=0.5,
        font=dict(family="Inter")
    )
    
    return fig

def create_satuan_kerja_chart(df_pemetaan, pilihan_col):
    """Create bar chart for satuan kerja tujuan"""
    # Count satuan kerja for selected pilihan
    satuan_counts = df_pemetaan[pilihan_col].value_counts().head(14)  # Top 14
    
    # Create bar chart
    fig = px.bar(
        x=satuan_counts.values,
        y=satuan_counts.index,
        orientation='h',
        title=f"Top Satuan Kerja Tujuan - {pilihan_col.split('_')[0]}",
        labels={'x': 'Jumlah Pegawai', 'y': 'Satuan Kerja'},
        color=satuan_counts.values,
        color_continuous_scale='blues'
    )
    
    fig.update_layout(
        height=600,
        showlegend=False,
        title_x=0.5,
        font=dict(family="Inter")
    )
    
    return fig

# [Semua fungsi yang sudah ada sebelumnya tetap sama...]
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
        subplot_titles=('🏢 Kompetensi Manajerial', '⚙️ Kompetensi Teknis'),
        vertical_spacing=0.1,
    )
    
    fig.update_layout(
    margin=dict(t=100, b=10, l=50, r=50)
)

    # Atur posisi title jika masih perlu penyesuaian
    for annotation in fig['layout']['annotations']:
        annotation['y'] = annotation['y'] + 0.02
    
    # Spider Chart 1: Manajerial
    # Layer 1 (dalam): Level Sekarang (gradient biru)
    fig.add_trace(go.Scatterpolar(
        r=manajerial_values_sekarang,
        theta=manajerial_labels,
        fill='toself',
        name='Manajerial - Level Sekarang',
        line_color='#667eea',
        fillcolor='rgba(102, 126, 234, 0.6)',
        subplot='polar'
    ), row=1, col=1)
    
    # Layer 2 (luar): Total (Level Sekarang + Level Atas) (gradient ungu)
    fig.add_trace(go.Scatterpolar(
        r=manajerial_total,
        theta=manajerial_labels,
        fill='tonext',
        name='Manajerial - Level Atas',
        line_color='#764ba2',
        fillcolor='rgba(118, 75, 162, 0.4)',
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
        line=dict(color='#11998e', width=3, dash='dash'),
        subplot='polar'
    ), row=1, col=1)
    
    # Spider Chart 2: Teknis
    # Layer 1 (dalam): Level Sekarang (gradient biru)
    fig.add_trace(go.Scatterpolar(
        r=teknis_values_sekarang,
        theta=teknis_labels,
        fill='toself',
        name='Teknis - Level Sekarang',
        line_color='#667eea',
        fillcolor='rgba(102, 126, 234, 0.6)',
        subplot='polar2'
    ), row=1, col=2)
    
    # Layer 2 (luar): Total (Level Sekarang + Level Atas) (gradient ungu)
    fig.add_trace(go.Scatterpolar(
        r=teknis_total,
        theta=teknis_labels,
        fill='tonext',
        name='Teknis - Level Atas',
        line_color='#764ba2',
        fillcolor='rgba(118, 75, 162, 0.4)',
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
        line=dict(color='#11998e', width=3, dash='dash'),
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
                dtick=1,
                gridcolor='rgba(102, 126, 234, 0.2)',
                linecolor='rgba(102, 126, 234, 0.3)'
            ),
            bgcolor='rgba(0, 0, 0, 0)'
        ),
        
        polar2=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(max(teknis_total) if teknis_total else [0], 10)],  # Dynamic untuk teknis
                tickmode='linear',
                tick0=0,
                dtick=1,
                gridcolor='rgba(102, 126, 234, 0.2)',
                linecolor='rgba(102, 126, 234, 0.3)'
            ),
            bgcolor='rgba(0, 0, 0, 0)'
        ),
        showlegend=True,
        
        font=dict(size=12, family='Inter'),
        height=700,
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)'
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
            'Nilai di Atas Level': nilai_atas_level,
            'Total': nilai_selevel + nilai_atas_level
            
        })
    
    df_table = pd.DataFrame(table_data)
    return df_table

def display_metric_cards(col1, col2, col3, value1, label1, value2, label2, value3, label3):
    """Display beautiful metric cards"""
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{value1}</div>
            <div class="metric-label">{label1}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{value2}</div>
            <div class="metric-label">{label2}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{value3}</div>
            <div class="metric-label">{label3}</div>
        </div>
        """, unsafe_allow_html=True)

def get_category_class(category):
    """Get CSS class based on category"""
    if category == "Optimal":
        return "optimal"
    elif category == "Cukup Optimal":
        return "cukup-optimal"
    elif category == "Kurang Optimal":
        return "kurang-optimal"
    else:
        return ""
    
def display_info_card(title, content, icon="ℹ️"):
    """Display information card with styling"""
    st.markdown(f"""
    <div class="info-card">
        <h3>{icon} {title}</h3>
        {content}
    </div>
    """, unsafe_allow_html=True)

def main():
    # Load custom CSS
    load_css()
    
    # Header dengan styling yang menarik
    st.markdown("""
    <div class="main-header">
        <h1 style="font-size: 3rem; font-weight: 700; margin-bottom: 0.5rem; color: #667eea;">Aplikasi Pengolahan Data Kompetensi</h1>
        <p style="font-size: 1.2rem; opacity: 0.8; font-weight: 500; color=white">Sistem Analisis Kompetensi Pegawai Modern</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Section divider
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    df_pemetaan = load_pemetaan_data()
    
    if df is None:
        st.error("🚨 Gagal memuat data. Pastikan file CSV tersedia.")
        
        # Beautiful file upload section
        st.markdown("""
        <div class="info-card">
            <h3>📂 Upload File CSV</h3>
            <p>Silakan upload file CSV yang berisi data kompetensi pegawai.</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
        if uploaded_file is not None:
            try:
                # Coba baca dengan encoding utf-8 terlebih dahulu
                df = pd.read_csv(uploaded_file, encoding='utf-8')
                st.success("✅ File berhasil diupload!")
            except UnicodeDecodeError:
                # Jika gagal, coba dengan latin-1
                df = pd.read_csv(uploaded_file, encoding='latin-1')
                st.success("✅ File berhasil diupload!")
            except Exception as e:
                st.error(f"❌ Error reading uploaded file: {e}")
                df = None
    
    if df is not None:
        # Sidebar dengan styling yang lebih menarik
        with st.sidebar:
            st.markdown("""
            <div style="text-align: center; padding: 1rem 0; color: white;">
                <h2 style="color: white; margin-bottom: 0;">🎛️ Panel Kontrol</h2>
            </div>
            """, unsafe_allow_html=True)
            
            menu = st.selectbox(
                "🔍 Pilih Menu:",
                ["📋 Tampilkan Tabel", "🔍 Pencarian berdasarkan NIP", "🗺️ Pemetaan Pegawai"],
                index=0
            )
        
        if menu == "📋 Tampilkan Tabel":
            st.markdown("""
            <div style="text-align: center; padding: 1rem 0;">
                <h2 style="color: #667eea; font-weight: 600;">📋 Data Tabel dengan Filter</h2>
                <p style="color: #666; font-size: 1.1rem;">Jelajahi dan filter data kompetensi pegawai</p>
            </div>
            """, unsafe_allow_html=True)
            
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
            
            # Filter controls dengan styling yang lebih menarik
            st.markdown("""
            <div class="info-card">
                <h3>🔍 Filter Data</h3>
                <p style="color: black;">Gunakan filter di bawah untuk menyaring data sesuai kebutuhan Anda.</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Filter berdasarkan Level (assumsi ada kolom Level)
                if 'Level' in df_processed.columns:
                    unique_levels = ['Semua'] + sorted(df_processed['Level'].dropna().unique().tolist())
                    selected_level = st.selectbox("🏢 Filter Level:", unique_levels)
                else:
                    st.warning("⚠️ Kolom 'Level' tidak ditemukan")
                    selected_level = "Semua"
            
            with col2:
                # Filter berdasarkan Nama Wilayah
                if 'Nama Wilayah' in df_processed.columns:
                    unique_wilayah = ['Semua'] + sorted(df_processed['Nama Wilayah'].dropna().unique().tolist())
                    selected_wilayah = st.selectbox("🌍 Filter Nama Wilayah:", unique_wilayah)
                else:
                    st.warning("⚠️ Kolom 'Nama Wilayah' tidak ditemukan")
                    selected_wilayah = "Semua"
            
            # Apply filters
            filtered_df = df_processed.copy()
            
            # Filter berdasarkan level
            if selected_level != "Semua" and 'Level' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['Level'] == selected_level]
            
            # Filter berdasarkan wilayah
            if selected_wilayah != "Semua" and 'Nama Wilayah' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['Nama Wilayah'] == selected_wilayah]
            
            # Pilih kolom untuk ditampilkan
            display_columns = ['Nama Pegawai', 'Nama Wilayah', 'Jabatan', 'percent_Manajerial', 'percent_T']
            available_columns = [col for col in display_columns if col in filtered_df.columns]
            display_df = filtered_df[available_columns].copy()
            
            # Rename kolom untuk tampilan yang lebih baik
            column_rename = {
                'Nama Pegawai': 'Nama',
                'Nama Wilayah': 'Wilayah',
                'Jabatan': 'Jabatan',
                'M_Total': 'Nilai Manajerial',
                'percent_Manajerial': 'Persentase Manajerial (%)',
                'cat_M': 'Kategori Manajerial',
                'T_Total': 'Nilai Teknis',
                'percent_T': 'Persentase Teknis (%)',
                'cat_T': 'Kategori Teknis',
            }
            display_df = display_df.rename(columns=column_rename)
            
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            
            # Tampilkan statistik
            if not filtered_df.empty:
                st.markdown("""
                <div style="text-align: center; padding: 1rem 0;">
                    <h3 style="color: #667eea; font-weight: 600;">📊 Statistik Data Terfilter</h3>
                    <p style="color: #666;">Ringkasan data yang telah difilter</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Hitung statistik
                m_total_avg = filtered_df['M_Total'].mean()
                t_total_avg = filtered_df['T_Total'].mean()
                total_data = len(filtered_df)
                
                # Tampilkan dalam metric cards
                col1, col2, col3 = st.columns(3)
                display_metric_cards(
                    col1, col2, col3,
                    f"{total_data:,}", "Jumlah Data",
                    f"{m_total_avg:.1f}", "Rata-rata Manajerial",
                    f"{t_total_avg:.1f}", "Rata-rata Teknis"
                )
                
                # Statistik detail
                st.markdown("""
                <div style="text-align: center; padding: 1rem 0; margin-top: 2rem;">
                    <h3 style="color: #667eea; font-weight: 600;">📈 Statistik Detail</h3>
                </div>
                """, unsafe_allow_html=True)
                
                stats_col1, stats_col2 = st.columns(2)
                
                with stats_col1:
                    # Manajerial stats
                    avg_manajerial = filtered_df['M_Total'].mean()
                    min_manajerial = filtered_df['M_Total'].min()
                    max_manajerial = filtered_df['M_Total'].max()
                    std_manajerial = filtered_df['M_Total'].std()
                    
                    st.markdown(f"""
                    <div class="info-card">
                        <h3 style="color: #667eea;">🏢 Kompetensi Manajerial</h3>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                            <div style="text-align: center;">
                                <div style="font-size: 1.5rem; font-weight: 600; color: #667eea;">{avg_manajerial:.2f}</div>
                                <div style="font-size: 0.9rem; color: #666;">Rata-rata</div>
                            </div>
                            <div style="text-align: center;">
                                <div style="font-size: 1.5rem; font-weight: 600; color: #11998e;">{min_manajerial:.2f}</div>
                                <div style="font-size: 0.9rem; color: #666;">Minimum</div>
                            </div>
                            <div style="text-align: center;">
                                <div style="font-size: 1.5rem; font-weight: 600; color: #e74c3c;">{max_manajerial:.2f}</div>
                                <div style="font-size: 0.9rem; color: #666;">Maksimum</div>
                            </div>
                            <div style="text-align: center;">
                                <div style="font-size: 1.5rem; font-weight: 600; color: #f39c12;">{std_manajerial:.2f}</div>
                                <div style="font-size: 0.9rem; color: #666;">Std Deviasi</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with stats_col2:
                    # Teknis stats
                    avg_teknis = filtered_df['T_Total'].mean()
                    min_teknis = filtered_df['T_Total'].min()
                    max_teknis = filtered_df['T_Total'].max()
                    std_teknis = filtered_df['T_Total'].std()
                    
                    st.markdown(f"""
                    <div class="info-card">
                        <h3 style="color: #764ba2;">⚙️ Kompetensi Teknis</h3>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                            <div style="text-align: center;">
                                <div style="font-size: 1.5rem; font-weight: 600; color: #667eea;">{avg_teknis:.2f}</div>
                                <div style="font-size: 0.9rem; color: #666;">Rata-rata</div>
                            </div>
                            <div style="text-align: center;">
                                <div style="font-size: 1.5rem; font-weight: 600; color: #11998e;">{min_teknis:.2f}</div>
                                <div style="font-size: 0.9rem; color: #666;">Minimum</div>
                            </div>
                            <div style="text-align: center;">
                                <div style="font-size: 1.5rem; font-weight: 600; color: #e74c3c;">{max_teknis:.2f}</div>
                                <div style="font-size: 0.9rem; color: #666;">Maksimum</div>
                            </div>
                            <div style="text-align: center;">
                                <div style="font-size: 1.5rem; font-weight: 600; color: #f39c12;">{std_teknis:.2f}</div>
                                <div style="font-size: 0.9rem; color: #666;">Std Deviasi</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
                
                # Tampilkan tabel dengan styling yang lebih baik
                st.markdown("""
                <div style="text-align: center; padding: 1rem 0;">
                    <h3 style="color: #667eea; font-weight: 600;">📋 Tabel Data</h3>
                    <p style="color: #666;">Data lengkap berdasarkan filter yang dipilih</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.dataframe(
                    display_df, 
                    use_container_width=True, 
                    height=400,
                    hide_index=True
                )
                
                # Info jumlah data dengan styling
                st.markdown(f"""
                <div class="success-card">
                    ✅ Menampilkan {len(display_df)} dari {len(df)} data total
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.markdown("""
                <div class="info-card" style="border-left-color: #f39c12;">
                    <h3 style="color: #f39c12;">⚠️ Tidak Ada Data</h3>
                    <p>Tidak ada data yang sesuai dengan filter yang dipilih. Silakan coba kombinasi filter lain.</p>
                </div>
                """, unsafe_allow_html=True)
        
        elif menu == "🔍 Pencarian berdasarkan NIP":
            st.markdown("""
            <div style="text-align: center; padding: 1rem 0;">
                <h2 style="color: #667eea; font-weight: 600;">🔍 Pencarian Data berdasarkan NIP</h2>
                <p style="color: white; font-size: 1.1rem;">Masukkan NIP untuk melihat detail kompetensi pegawai</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Input NIP dengan styling yang lebih menarik
            st.markdown("""
            <div class="info-card">
                <h3>🔢 Masukkan NIP</h3>
                <p style="color: black;">Ketik NIP pegawai yang ingin Anda cari</p>
            </div>
            """, unsafe_allow_html=True)
            
            nip_input = st.text_input(
                "NIP:", 
                placeholder="Contoh: 199702220701110024",
                help="Masukkan NIP lengkap untuk hasil yang akurat"
            )
            
            if nip_input:
                # Cari data berdasarkan NIP
                matching_data = df[df['NIP'].astype(str).str.contains(nip_input, na=False)]
                
                if not matching_data.empty:
                    # Ambil data pertama jika ada lebih dari satu
                    data_row = matching_data.iloc[0]
                    
                    # Tampilkan informasi dasar dengan card yang menarik
                    st.markdown("""
                    <div style="text-align: center; padding: 1rem 0; margin-top: 2rem;">
                        <h3 style="color: #11998e; font-weight: 600;">👤 Informasi Pegawai</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Info pegawai dalam card
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"""
                        <div class="success-card">
                            <strong>👤 Nama:</strong> {data_row.get('Nama Pegawai', 'N/A')}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        <div class="success-card">
                            <strong>💼 Jabatan:</strong> {data_row.get('Jabatan', 'N/A')}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class="success-card">
                            <strong>🔢 NIP:</strong> {data_row.get('NIP', 'N/A')}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        <div class="success-card">
                            <strong>🌍 Wilayah:</strong> {data_row.get('Nama Wilayah', 'N/A')}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
                    
                    # Tampilkan spider chart
                    st.markdown("""
                    <div style="text-align: center; padding: 1rem 0;">
                        <h3 style="color: #667eea; font-weight: 600;">📊 Visualisasi Kompetensi</h3>
                        <p style="color: white;">Spider chart menunjukkan profil kompetensi secara visual</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    spider_chart = create_spider_chart(data_row)
                    st.plotly_chart(spider_chart, use_container_width=True)
                    
                    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
                    
                    # Detail nilai kompetensi dengan tab system
                    st.markdown("""
                    <div style="text-align: center; padding: 1rem 0;">
                        <h3 style="color: #667eea; font-weight: 600;">📈 Detail Nilai Kompetensi</h3>
                        <p style="color: #666;">Pilih tab untuk melihat detail kompetensi</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Menggunakan tabs untuk tampilan yang lebih modern
                    tab1, tab2 = st.tabs(["🏢 Kompetensi Manajerial", "⚙️ Kompetensi Teknis"])
                    
                    with tab1:
                        st.markdown("### 🏢 Detail Kompetensi Manajerial")
                        
                        # Buat tabel manajerial
                        manajerial_table = create_competency_table(data_row, 'manajerial')
                        
                        # Tampilkan tabel dengan styling
                        st.dataframe(
                            manajerial_table, 
                            use_container_width=True, 
                            height=400,
                            hide_index=True
                        )
                        
                        # Tampilkan total dalam metric cards
                        # Total Nilai Manajerial
                        total_manajerial = manajerial_table['Total'].sum()
                        persentase_manajerial = data_row.get('percent_Manajerial', 0)
                        kategori_manajerial = data_row.get('cat_M', 'N/A')
                        
                        col1, col2, col3 = st.columns(3)
                        display_metric_cards(
                            col1, col2, col3,
                            int(total_manajerial), "Total Nilai Manajerial",
                            f"{persentase_manajerial:.1f}%", "Persentase Nilai Manajerial",
                            kategori_manajerial, "Kategori Manajerial"
                            
                        )
                        
                    
                    with tab2:
                        st.markdown("### ⚙️ Detail Kompetensi Teknis")
                        
                        # Buat tabel teknis
                        teknis_table = create_competency_table(data_row, 'teknis')
                        
                        # Tampilkan tabel dengan styling
                        st.dataframe(
                            teknis_table, 
                            use_container_width=True, 
                            height=300,
                            hide_index=True
                        )
                        
                        # Tampilkan total dalam metric cards
                        # Total Nilai teknis
                        total_teknis = teknis_table['Total'].sum()
                        persentase_teknis = total_teknis / (len(teknis_table) * 10) * 100
                        kategori_teknis = "Optimal" if persentase_teknis >= 85 else "Cukup Optimal" if persentase_teknis >= 70 else "Kurang Optimal"
                        
                        col1, col2, col3 = st.columns(3)
                        display_metric_cards(
                            col1, col2, col3,
                            int(total_teknis), "Total Nilai Teknis",
                            f"{persentase_teknis:.1f}%", "Persentase Nilai Teknis",
                            kategori_teknis, "Kategori Teknis"
                        )
                
                else:
                    # Error message dengan styling
                    st.markdown(f"""
                    <div class="info-card" style="border-left-color: #e74c3c;">
                        <h3 style="color: #e74c3c;">❌ Data Tidak Ditemukan</h3>
                        <p style="color:black">Data dengan NIP '<strong>{nip_input}</strong>' tidak ditemukan dalam database.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Suggest similar NIPs
                    similar_nips = df[df['NIP'].astype(str).str.contains(nip_input[:8] if len(nip_input) > 8 else nip_input, na=False)]['NIP'].head(5)
                    if not similar_nips.empty:
                        st.markdown("""
                        <div class="info-card" style="border-left-color: #f39c12;">
                            <h3 style="color: #f39c12;">💡 Saran NIP yang Mirip</h3>
                        """, unsafe_allow_html=True)
                        
                        for nip in similar_nips:
                            st.markdown(f"• **{nip}**")
                        
                        st.markdown("</div>", unsafe_allow_html=True)

        elif menu == "🗺️ Pemetaan Pegawai":
            if df_pemetaan is None:
                st.error("🚨 Data pemetaan tidak tersedia. Pastikan file pemetaan.xlsx ada.")
                return
                
            st.markdown("""
            <div style="text-align: center; padding: 1rem 0;">
                <h2 style="color: #667eea; font-weight: 600;">🗺️ Pemetaan Pegawai</h2>
                <p style="color: #666; font-size: 1.1rem;">Analisis pengembangan karir dan satuan kerja tujuan</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Tabs untuk Pengembangan Karir dan Satuan Kerja Tujuan
            tab1, tab2 = st.tabs(["📈 Pengembangan Karir", "🏢 Satuan Kerja Tujuan"])
            
            with tab1:
                st.markdown("### 📈 Analisis Pengembangan Karir")
                
                # Bar chart perbandingan jalur jabatan
                if 'Q01_JALUR PENGEMBANGAN KARIR' in df_pemetaan.columns:
                    st.markdown("#### Perbandingan Jalur Pengembangan Karir")
                    
                    # Create and display bar chart
                    jalur_chart = create_jalur_jabatan_chart(df_pemetaan)
                    st.plotly_chart(jalur_chart, use_container_width=True)
                    
                    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
                    
                    # Buttons untuk filter jalur jabatan
                    st.markdown("#### Analisis Alasan Pemilihan Jalur Jabatan")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("🏗️ Jalur Jabatan Struktural", use_container_width=True):
                            st.session_state.jalur_selected = "1 : Jalur Jabatan Struktural"
                    
                    with col2:
                        if st.button("⚙️ Jalur Jabatan Fungsional", use_container_width=True):
                            st.session_state.jalur_selected = "2 : Jalur Jabatan Fungsional"
                    
                    # Display wordcloud berdasarkan pilihan
                    if hasattr(st.session_state, 'jalur_selected'):
                        selected_jalur = st.session_state.jalur_selected
                        
                        # Filter data berdasarkan jalur yang dipilih
                        filtered_pemetaan = df_pemetaan[
                            df_pemetaan['Q01_JALUR PENGEMBANGAN KARIR'] == selected_jalur
                        ]
                        
                        if not filtered_pemetaan.empty and 'Alasan Pilihan Jalur Karir' in df_pemetaan.columns:
                            st.markdown(f"#### WordCloud Alasan Memilih {selected_jalur}")
                            
                            # Get text data for wordcloud
                            text_data = filtered_pemetaan['Alasan Pilihan Jalur Karir'].dropna().tolist()
                            
                            if text_data:
                                wordcloud_fig = create_wordcloud(
                                    text_data, 
                                    f"Alasan Memilih {selected_jalur}"
                                )
                                
                                if wordcloud_fig:
                                    st.pyplot(wordcloud_fig)
                                else:
                                    st.warning("⚠️ Tidak ada teks yang cukup untuk membuat wordcloud")
                            else:
                                st.warning("⚠️ Tidak ada data alasan untuk jalur yang dipilih")
                        else:
                            st.warning("⚠️ Data tidak tersedia untuk jalur yang dipilih")
                
                else:
                    st.error("❌ Kolom 'Q01_JALUR PENGEMBANGAN KARIR' tidak ditemukan dalam data")
            
            with tab2:
                st.markdown("### 🏢 Analisis Satuan Kerja Tujuan")
                
                # Filter untuk memilih pilihan 1, 2, atau 3
                pilihan_options = {
                    "Pilihan 1": "Q03_Pilih 3 Satuan Kerja Tujuan",
                    "Pilihan 2": "Q04_Pilih 3 Satuan Kerja Tujuan", 
                    "Pilihan 3": "Q05_Pilih 3 Satuan Kerja Tujuan"
                }
                
                selected_pilihan = st.selectbox(
                    "📊 Pilih Satuan Kerja Tujuan:",
                    list(pilihan_options.keys())
                )
                
                pilihan_col = pilihan_options[selected_pilihan]
                
                if pilihan_col in df_pemetaan.columns:
                    # Create bar chart untuk satuan kerja tujuan
                    satuan_chart = create_satuan_kerja_chart(df_pemetaan, pilihan_col)
                    st.plotly_chart(satuan_chart, use_container_width=True)
                    
                    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
                    
                    # WordCloud untuk alasan memilih pilihan 1
                    if selected_pilihan == "Pilihan 1" and 'Q06_Alasan Pilihan Jalur Karir' in df_pemetaan.columns:
                        st.markdown("#### Analisis Alasan Memilih Pilihan 1")
                        
                        # Filter berdasarkan nilai dari pilihan 1
                        unique_pilihan1 = df_pemetaan[pilihan_col].dropna().unique()
                        
                        if len(unique_pilihan1) > 0:
                            selected_satuan = st.selectbox(
                                "🏢 Pilih Satuan Kerja untuk Analisis Alasan:",
                                unique_pilihan1
                            )
                            
                            # Filter data berdasarkan satuan kerja yang dipilih
                            filtered_data = df_pemetaan[
                                df_pemetaan[pilihan_col] == selected_satuan
                            ]
                            
                            if not filtered_data.empty:
                                # Get text data for wordcloud
                                text_data = filtered_data['Q06_Alasan Pilihan Jalur Karir'].dropna().tolist()
                                
                                if text_data:
                                    st.markdown(f"#### WordCloud Alasan Memilih: {selected_satuan}")
                                    
                                    wordcloud_fig = create_wordcloud(
                                        text_data,
                                        f"Alasan Memilih {selected_satuan}"
                                    )
                                    
                                    if wordcloud_fig:
                                        st.pyplot(wordcloud_fig)
                                    else:
                                        st.warning("⚠️ Tidak ada teks yang cukup untuk membuat wordcloud")
                                else:
                                    st.warning("⚠️ Tidak ada data alasan untuk satuan kerja yang dipilih")
                            else:
                                st.warning("⚠️ Data tidak tersedia untuk satuan kerja yang dipilih")
                                
                    elif selected_pilihan == "Pilihan 2" and 'Q06_Alasan Pilihan Jalur Karir' in df_pemetaan.columns:
                        st.markdown("#### Analisis Alasan Memilih Pilihan 2")
                        
                        # Filter berdasarkan nilai dari pilihan 1
                        unique_pilihan1 = df_pemetaan[pilihan_col].dropna().unique()
                        
                        if len(unique_pilihan1) > 0:
                            selected_satuan = st.selectbox(
                                "🏢 Pilih Satuan Kerja untuk Analisis Alasan:",
                                unique_pilihan1
                            )
                            
                            # Filter data berdasarkan satuan kerja yang dipilih
                            filtered_data = df_pemetaan[
                                df_pemetaan[pilihan_col] == selected_satuan
                            ]
                            
                            if not filtered_data.empty:
                                # Get text data for wordcloud
                                text_data = filtered_data['Q06_Alasan Pilihan Jalur Karir'].dropna().tolist()
                                
                                if text_data:
                                    st.markdown(f"#### WordCloud Alasan Memilih: {selected_satuan}")
                                    
                                    wordcloud_fig = create_wordcloud(
                                        text_data,
                                        f"Alasan Memilih {selected_satuan}"
                                    )
                                    
                                    if wordcloud_fig:
                                        st.pyplot(wordcloud_fig)
                                    else:
                                        st.warning("⚠️ Tidak ada teks yang cukup untuk membuat wordcloud")
                                else:
                                    st.warning("⚠️ Tidak ada data alasan untuk satuan kerja yang dipilih")
                            else:
                                st.warning("⚠️ Data tidak tersedia untuk satuan kerja yang dipilih")
                                
                    elif selected_pilihan == "Pilihan 3" and 'Q06_Alasan Pilihan Jalur Karir' in df_pemetaan.columns:
                        st.markdown("#### Analisis Alasan Memilih Pilihan 3")
                        
                        # Filter berdasarkan nilai dari pilihan 1
                        unique_pilihan1 = df_pemetaan[pilihan_col].dropna().unique()
                        
                        if len(unique_pilihan1) > 0:
                            selected_satuan = st.selectbox(
                                "🏢 Pilih Satuan Kerja untuk Analisis Alasan:",
                                unique_pilihan1
                            )
                            
                            # Filter data berdasarkan satuan kerja yang dipilih
                            filtered_data = df_pemetaan[
                                df_pemetaan[pilihan_col] == selected_satuan
                            ]
                            
                            if not filtered_data.empty:
                                # Get text data for wordcloud
                                text_data = filtered_data['Q06_Alasan Pilihan Jalur Karir'].dropna().tolist()
                                
                                if text_data:
                                    st.markdown(f"#### WordCloud Alasan Memilih: {selected_satuan}")
                                    
                                    wordcloud_fig = create_wordcloud(
                                        text_data,
                                        f"Alasan Memilih {selected_satuan}"
                                    )
                                    
                                    if wordcloud_fig:
                                        st.pyplot(wordcloud_fig)
                                    else:
                                        st.warning("⚠️ Tidak ada teks yang cukup untuk membuat wordcloud")
                                else:
                                    st.warning("⚠️ Tidak ada data alasan untuk satuan kerja yang dipilih")
                            else:
                                st.warning("⚠️ Data tidak tersedia untuk satuan kerja yang dipilih")
                                            
                else:
                    st.error(f"❌ Kolom '{pilihan_col}' tidak ditemukan dalam data")

    # Footer
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: #666;">
        <p style="margin: 0; font-size: 0.9rem;">
            © 2024 Aplikasi Pengolahan Data Asesmen Pegawai BPS Lampung - Dikembangkan dengan ❤️
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()