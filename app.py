import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import calendar
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ==========================================
# 0. Page Config
# ==========================================
st.set_page_config(page_title="Callie DE - SEO Dashboard", page_icon="🇩🇪", layout="wide")

# ================= 登录验证 =================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.markdown("### 🔐 Callie DE 登录")
    col1, col2 = st.columns([1, 2])
    with col1:
        u = st.text_input("用户名")
        p = st.text_input("密码", type="password")
        if st.button("登录"):
            if u == "Callie" and p == "calliede2026":
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("用户名或密码错误")
    st.stop()
# ============================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    html, body, [class*="css"] { font-family: 'Poppins', 'Segoe UI', sans-serif !important; color: #2D235C !important; }
    [data-testid="stAppViewContainer"], .stApp { background-color: #F1F5F9 !important; }
    [data-testid="stHeader"] { background-color: transparent !important; }

    .soft-card {
        background-color: #ffffff; border: 1px solid #E2E8F0; border-radius: 28px; padding: 30px;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08), 0 4px 10px -2px rgba(15, 23, 42, 0.04);
        margin-bottom: 24px; transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .soft-card:hover { transform: translateY(-4px); box-shadow: 0 20px 40px -10px rgba(15, 23, 42, 0.12), 0 10px 15px -5px rgba(15, 23, 42, 0.08); }
    
    .welcome-banner {
        background: linear-gradient(135deg, #1A1A24 0%, #9B1B30 65%, #D4AF37 100%); 
        border-radius: 28px; padding: 32px 40px; color: white; margin-bottom: 30px; 
        box-shadow: 0 16px 32px -10px rgba(155, 27, 48, 0.4); position: relative; overflow: hidden;
    }
    .welcome-banner h1 { color: white !important; font-size: 36px; font-weight: 800; margin: 0 0 8px 0; display: flex; align-items: center; }
    .welcome-banner p { color: rgba(255,255,255,0.9) !important; font-size: 16px; margin: 0; }
    
    .progress-track { background-color: #F0F1F6; border-radius: 999px; height: 18px; width: 100%; position: relative; }
    .progress-fill-red { background: linear-gradient(90deg, #FF8491 0%, #FF6475 100%); height: 100%; border-radius: 999px; transition: width 0.8s ease; box-shadow: 0 6px 16px -4px rgba(255, 100, 117, 0.6); }
    .progress-fill-blue { background: linear-gradient(90deg, #6BE1F0 0%, #42D2E6 100%); height: 100%; border-radius: 999px; transition: width 0.8s ease; box-shadow: 0 6px 16px -4px rgba(66, 210, 230, 0.6); }
    .rocket-icon { position: absolute; right: -12px; top: -6px; font-size: 22px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.15)); }
    
    .icon-square { display: inline-flex; align-items: center; justify-content: center; width: 48px; height: 48px; border-radius: 16px; margin-right: 16px; font-size: 22px; }
    .icon-small { width: 36px; height: 36px; border-radius: 12px; margin-right: 12px; font-size: 16px; }
    
    .bg-red { background-color: #FFF0F2; color: #FF6475; }
    .bg-blue { background-color: #E8F9FB; color: #42D2E6; }
    .bg-purple { background-color: #F1F0F7; color: #2D235C; }
    .bg-orange { background-color: #FFF6E5; color: #FFB000; }
    .bg-gray { background-color: #F6F8FA; color: #8E8CA7; }
    
    .flex-center { display: flex; align-items: center; }

    div[data-testid="stButton"] button { background-color: #ffffff; border: 2px solid #F0F1F6; border-radius: 20px; color: #2D235C; font-weight: 600; padding: 6px 24px; box-shadow: 0 4px 10px rgba(45, 35, 92, 0.03); transition: all 0.3s ease; }
    div[data-testid="stButton"] button:hover { transform: scale(1.03); background-color: #2D235C; border-color: #2D235C; box-shadow: 0 10px 20px -6px rgba(45, 35, 92, 0.4); color: #ffffff; }
    
    .text-main { color: #2D235C !important; }
    .text-muted { color: #8E8CA7 !important; }
    
    .funnel-item { flex: 1; border-right: 2px solid #F0F1F6; padding-left: 20px; }
    .funnel-item:last-child { border-right: none; }
    .funnel-title { color: #8E8CA7; font-size: 13px; font-weight:500; margin: 0 0 8px 0; display: flex; align-items: center; }
    .funnel-dot { font-size: 10px; margin-right: 8px; }
    .funnel-value { color: #2D235C; font-size: 32px; font-weight: 700; margin: 0; }
    
    .inner-box { padding: 20px 24px; border-radius: 20px; flex: 1; margin-right: 16px; }
    .inner-box:last-child { margin-right: 0; }
    .box-deep { background-color: #2D235C; border: none; color: white;}
    .box-light { background-color: #ffffff; border: 2px solid #F0F1F6; }
    .box-label { font-size: 13px; margin: 0 0 12px 0; display: flex; align-items: center; font-weight:500;}
    .box-value-dark { font-size: 30px; font-weight: 700; color: #2D235C; margin: 0; }
    .box-value-white { font-size: 30px; font-weight: 700; color: #ffffff; margin: 0; }
    .compare-date-str { font-size: 12px; color: #8E8CA7; font-weight: normal; margin-left: 8px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. Data Loader & Smart Matching
# ==========================================
@st.cache_data(ttl=300)
def load_and_clean_data():
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT4KTuYQtC6xsRIwgWLDK9aJUhqmKDmUg4XmMxbsKadyj4QSRM9GNvDjyYz7z8vzKj8nohA7a8ukiLz/pub?gid=0&single=true&output=csv"
    bust_url = f"{csv_url}&_t={int(datetime.now().timestamp())}"
    
    df_raw = pd.read_csv(bust_url, header=None)
    raw_columns = list(df_raw.iloc[21])
    df_de = df_raw.iloc[23:40].copy()
    
    clean_columns = []
    for i, col in enumerate(raw_columns):
        if i == 0: clean_columns.append("Metric")
        else:
            col_str = str(col)
            if pd.isna(col) or col_str.lower() == 'nan': clean_columns.append(f"空列_{i}")
            elif col_str in clean_columns: clean_columns.append(f"{col_str}_重复_{i}")
            else: clean_columns.append(col_str)
                
    df_de.columns = clean_columns
    df_de.reset_index(drop=True, inplace=True)
    df_de['Metric'] = df_de['Metric'].astype(str).str.strip()
    df_de['Metric_Norm'] = df_de['Metric'].str.replace(' ', '', regex=False).str.lower()
    df_de = df_de[df_de['Metric'].notna() & (df_de['Metric'] != '') & (df_de['Metric'].str.lower() != 'nan')]
    cols_to_keep = [c for c in df_de.columns if "空列_" not in c]
    return df_de[cols_to_keep]

@st.cache_data(ttl=300)
def load_gsc_data():
    gsc_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSdRQFVxjh71cKOiUdcf-j5Ob2GQzc_1WidEtXXx1tdc9Qjz5bWgzJtSEDbMU86i_4ATkmNV8rPITg1/pub?gid=0&single=true&output=csv"
    bust_url = f"{gsc_url}&_t={int(datetime.now().timestamp())}"
    df_raw = pd.read_csv(bust_url, header=None)
    
    row0 = df_raw.iloc[0].ffill()
    row1 = df_raw.iloc[1]
    
    new_cols = []
    for c, m in zip(row0, row1):
        c_str = str(c).strip()
        m_str = str(m).strip()
        if '日' in m_str or 'date' in m_str.lower() or pd.isna(c) or c_str == 'nan':
            new_cols.append(m_str)
        else:
            new_cols.append(f"{c_str}_{m_str}")
            
    df = df_raw.iloc[2:].copy()
    df.columns = new_cols
    
    date_col = None
    for col in df.columns:
        if '日' in str(col) or 'date' in str(col).lower():
            date_col = col
            break
            
    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce').dt.date
        df = df.dropna(subset=[date_col]).sort_values(date_col)
    return df, date_col

@st.cache_data(ttl=300)
def load_ai_perf_data():
    ai_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRdK5Va7wCzGJ3ysGE8H3oeCWjjGEVLZud1Y31ghdO68zLgrOfkfwLnh3VU_lhZttlUziSG4f7ZRTLU/pub?output=csv"
    bust_url = f"{ai_url}&_t={int(datetime.now().timestamp())}"
    df_raw = pd.read_csv(bust_url, header=None)
    
    row0 = df_raw.iloc[0].ffill()
    row1 = df_raw.iloc[1]
    
    new_cols = []
    for c, m in zip(row0, row1):
        c_str = str(c).strip()
        m_str = str(m).strip()
        if '日' in m_str or 'date' in m_str.lower() or pd.isna(c) or c_str == 'nan':
            new_cols.append(m_str)
        else:
            new_cols.append(f"{c_str}_{m_str}")
            
    df = df_raw.iloc[2:].copy()
    df.columns = new_cols
    
    date_col = None
    for col in df.columns:
        if '日' in str(col) or 'date' in str(col).lower():
            date_col = col
            break
            
    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce').dt.date
        df = df.dropna(subset=[date_col]).sort_values(date_col)
    return df, date_col

# 辅助函数：十六进制颜色转 RGBA
def hex_to_rgba(hex_color, alpha=0.1):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f'rgba({r}, {g}, {b}, {alpha})'

# 核心：时间聚合引擎
def aggregate_trend(raw_dates, raw_values, freq='D', agg='sum'):
    if not raw_dates or not raw_values or len(raw_dates) == 0: return [], []
    df_temp = pd.DataFrame({'date': pd.to_datetime(raw_dates), 'val': raw_values})
    df_temp.set_index('date', inplace=True)
    if freq == 'D': res = df_temp.resample('D')
    elif freq == 'W': res = df_temp.resample('W-MON')
    elif freq == 'M': res = df_temp.resample('ME')
    
    if agg == 'sum': df_agg = res.sum().fillna(0)
    else: df_agg = res.mean().fillna(0)
        
    if freq == 'M': out_dates = df_agg.index.strftime('%Y-%m').tolist()
    else: out_dates = df_agg.index.strftime('%Y-%m-%d').tolist()
    return out_dates, df_agg['val'].tolist()

font_style = dict(family="Poppins, sans-serif", color="#8E8CA7")

try:
    with st.spinner('🚀 同步 Callie DE 德语站最新数据...'):
        df_de = load_and_clean_data()
        try: df_gsc, date_col_gsc = load_gsc_data()
        except Exception: df_gsc, date_col_gsc = pd.DataFrame(), None
        try: df_ai, date_col_ai = load_ai_perf_data()
        except Exception: df_ai, date_col_ai = pd.DataFrame(), None

        # ==========================================
        # ⭐ T-2 GA 数据延迟基准日逻辑
        # ==========================================
        real_today = datetime.now().date()
        data_date = real_today - timedelta(days=2)
        current_year, current_month = data_date.year, data
