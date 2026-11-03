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
        current_year, current_month = data_date.year, data_date.month

        st.markdown(f"""
<div class="welcome-banner">
<h1><img src="https://flagcdn.com/w80/de.png" style="height: 36px; margin-right: 16px; border-radius: 4px; box-shadow: 0 2px 6px rgba(0,0,0,0.3);" alt="Germany Flag">Hallo, Callie DE Team!</h1>
<p>Germany (DE) SEO Global Dashboard • Data Date: {data_date.strftime('%Y-%m-%d')} (T-2 GA Delay)</p>
</div>
""", unsafe_allow_html=True)
        
        col_btn, col_target1, col_target2 = st.columns([1.5, 2, 2])
        with col_btn:
            if st.button("🔄 Sync Data (刷新底层缓存)"):
                load_and_clean_data.clear()
                load_gsc_data.clear()
                load_ai_perf_data.clear()
                st.rerun()
        with col_target1: target_sales = st.number_input("🎯 DE Sales Target ($)", value=6000.0, step=500.0)
        with col_target2: target_traffic = st.number_input("⚡ DE Traffic Target", value=18000.0, step=1000.0)
                
        # ==========================================
        # 2. 日期匹配与强力精准查表引擎
        # ==========================================
        date_mapping = {}
        for col in df_de.columns:
            if col not in ['Metric', 'Metric_Norm']:
                try: date_mapping[col] = pd.to_datetime(col).date()
                except: pass
        
        mtd_cols = [col for col, dt in date_mapping.items() if dt.year == current_year and dt.month == current_month and dt <= data_date]
        lm_year = current_year if current_month > 1 else current_year - 1
        lm_month = current_month - 1 if current_month > 1 else 12
        lm_day = min(data_date.day, calendar.monthrange(lm_year, lm_month)[1])
        lm_start = date(lm_year, lm_month, 1)
        lm_end = date(lm_year, lm_month, lm_day)
        lm_cols = [col for col, dt in date_mapping.items() if lm_start <= dt <= lm_end]

        ly_year = current_year - 1
        ly_day = min(data_date.day, calendar.monthrange(ly_year, current_month)[1])
        ly_start = date(ly_year, current_month, 1)
        ly_end = date(ly_year, current_month, ly_day)
        ly_cols = [col for col, dt in date_mapping.items() if ly_start <= dt <= ly_end]

        curr_str = f"({current_month:02d}/01 - {current_month:02d}/{data_date.day:02d})"
        lm_str = f"({lm_year}/{lm_month:02d}/01 - {lm_month:02d}/{lm_day:02d})"
        ly_str = f"({ly_year}/{current_month:02d}/01 - {current_month:02d}/{ly_day:02d})"

        def get_sum(possible_names, cols, is_currency=False):
            if isinstance(possible_names, str): possible_names = [possible_names]
            data = pd.DataFrame()
            for p in possible_names:
                target = p.replace(' ', '').lower()
                matched = df_de[df_de['Metric_Norm'] == target]
                if not matched.empty:
                    data = matched
                    break
            if data.empty:
                for p in possible_names:
                    target = p.replace(' ', '').lower()
                    matched = df_de[df_de['Metric_Norm'].str.contains(target, na=False)]
                    if not matched.empty:
                        data = matched
                        break
            if not data.empty and cols:
                valid_cols = [c for c in cols if c in data.columns]
                if valid_cols:
                    vals = data[valid_cols].iloc[0].astype(str).str.replace(',', '', regex=False)
                    if is_currency: vals = vals.str.replace('$', '', regex=False)
                    return pd.to_numeric(vals, errors='coerce').fillna(0).sum()
            return 0.0

        mtd_sales = get_sum(['ga4seo销售额'], mtd_cols, True)
        lm_sales = get_sum(['ga4seo销售额'], lm_cols, True)
        ly_sales = get_sum(['ga4seo销售额'], ly_cols, True)

        mtd_traffic = get_sum(['seo流量'], mtd_cols)
        lm_traffic = get_sum(['seo流量'], lm_cols)
        ly_traffic = get_sum(['seo流量'], ly_cols)

        prog_sales = min(mtd_sales / target_sales, 1.0) if target_sales > 0 else 0
        prog_traffic = min(mtd_traffic / target_traffic, 1.0) if target_traffic > 0 else 0
        gap_sales = max(0, target_sales - mtd_sales)
        gap_traffic = max(0, target_traffic - mtd_traffic)

        st.markdown('<div class="flex-center" style="margin:20px 0;"><div class="icon-square bg-orange"><i class="fa-solid fa-bullseye"></i></div><h3 class="text-main" style="margin:0; font-size:22px;">Target Achievement (Monat)</h3></div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
<div class="soft-card">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
<div class="flex-center text-muted" style="font-size: 15px; font-weight: 500;"><i class="fa-solid fa-sack-dollar" style="color:#FF6475; margin-right:8px;"></i> Sales Progress (GA4 Data)</div>
<div style="color: #FF6475; font-size: 14px; font-weight: 700;">Gap: $ {gap_sales:,.2f}</div>
</div>
<div style="margin-bottom: 28px; display: flex; align-items: baseline;">
<span class="text-main" style="font-size: 38px; font-weight: 700;">$ {mtd_sales:,.2f}</span>
<span class="text-muted" style="font-size: 16px; margin-left: 8px;">/ $ {target_sales:,.2f}</span>
</div>
<div class="progress-track"><div class="progress-fill-red" style="width: {prog_sales*100}%;"></div><span class="rocket-icon">🎯</span></div>
<div style="text-align: right; margin-top: 16px;"><span style="color: #FF6475; font-weight: 800; font-size: 18px;">{prog_sales*100:.1f}%</span></div>
</div>
""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
<div class="soft-card">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
<div class="flex-center text-muted" style="font-size: 15px; font-weight: 500;"><i class="fa-solid fa-users" style="color:#42D2E6; margin-right:8px;"></i> Traffic Progress</div>
<div style="color: #42D2E6; font-size: 14px; font-weight: 700;">Gap: {gap_traffic:,.0f}</div>
</div>
<div style="margin-bottom: 28px; display: flex; align-items: baseline;">
<span class="text-main" style="font-size: 38px; font-weight: 700;">{mtd_traffic:,.0f}</span>
<span class="text-muted" style="font-size: 16px; margin-left: 8px;">/ {target_traffic:,.0f}</span>
</div>
<div class="progress-track"><div class="progress-fill-blue" style="width: {prog_traffic*100}%;"></div><span class="rocket-icon">⚡</span></div>
<div style="text-align: right; margin-top: 16px;"><span style="color: #42D2E6; font-weight: 800; font-size: 18px;">{prog_traffic*100:.1f}%</span></div>
</div>
""", unsafe_allow_html=True)

        st.markdown('<div class="flex-center" style="margin:30px 0 20px 0;"><div class="icon-square bg-purple"><i class="fa-solid fa-chart-simple"></i></div><h3 class="text-main" style="margin:0; font-size:22px;">MTD Monitoring</h3></div>', unsafe_allow_html=True)
        def get_trend_ui(pct): return ("#FF6475" if pct < 0 else "#22C55E", "#FFF0F2" if pct < 0 else "#F0FDF4", "↓" if pct < 0 else "↑")

        mom_sales_pct = ((mtd_sales - lm_sales) / lm_sales) * 100 if lm_sales > 0 else 0.0
        yoy_sales_pct = ((mtd_sales - ly_sales) / ly_sales) * 100 if ly_sales > 0 else 0.0
        c1_m, bg1_m, arr1_m = get_trend_ui(mom_sales_pct)
        c1_y, bg1_y, arr1_y = get_trend_ui(yoy_sales_pct)

        st.markdown(f"""
<div class="soft-card" style="display: flex; justify-content: space-between; text-align: left; padding-bottom:30px;">
<div style="flex: 1;"><p class="text-muted" style="font-size: 14px; margin-bottom: 8px;">Sales MTD (GA4) <span class="compare-date-str">{curr_str}</span></p><h2 class="text-main" style="margin: 0; font-size: 32px;">$ {mtd_sales:,.2f}</h2></div>
<div style="flex: 1; border-left: 2px solid #F0F1F6; padding-left: 30px;"><p class="text-muted" style="font-size: 14px; margin-bottom: 8px;">Last Month <span class="compare-date-str">{lm_str}</span></p><h2 class="text-main" style="margin: 0; font-size: 26px; margin-bottom: 12px;">$ {lm_sales:,.2f}</h2><span style="color: {c1_m}; font-weight: 600; background: {bg1_m}; padding: 4px 12px; border-radius: 8px; font-size: 13px;">{arr1_m} {abs(mom_sales_pct):.1f}% MoM</span></div>
<div style="flex: 1; border-left: 2px solid #F0F1F6; padding-left: 30px;"><p class="text-muted" style="font-size: 14px; margin-bottom: 8px;">Last Year <span class="compare-date-str">{ly_str}</span></p><h2 class="text-main" style="margin: 0; font-size: 26px; margin-bottom: 12px;">$ {ly_sales:,.2f}</h2><span style="color: {c1_y}; font-weight: 600; background: {bg1_y}; padding: 4px 12px; border-radius: 8px; font-size: 13px;">{arr1_y} {abs(yoy_sales_pct):.1f}% YoY</span></div>
</div>
""", unsafe_allow_html=True)
        
        mom_traf_pct = ((mtd_traffic - lm_traffic) / lm_traffic) * 100 if lm_traffic > 0 else 0.0
        yoy_traf_pct = ((mtd_traffic - ly_traffic) / ly_traffic) * 100 if ly_traffic > 0 else 0.0
        c2_m, bg2_m, arr2_m = get_trend_ui(mom_traf_pct)
        c2_y, bg2_y, arr2_y = get_trend_ui(yoy_traf_pct)

        st.markdown(f"""
<div class="soft-card" style="display: flex; justify-content: space-between; text-align: left; padding-bottom:30px;">
<div style="flex: 1;"><p class="text-muted" style="font-size: 14px; margin-bottom: 8px;">Traffic MTD <span class="compare-date-str">{curr_str}</span></p><h2 class="text-main" style="margin: 0; font-size: 32px;">{mtd_traffic:,.0f}</h2></div>
<div style="flex: 1; border-left: 2px solid #F0F1F6; padding-left: 30px;"><p class="text-muted" style="font-size: 14px; margin-bottom: 8px;">Last Month <span class="compare-date-str">{lm_str}</span></p><h2 class="text-main" style="margin: 0; font-size: 26px; margin-bottom: 12px;">{lm_traffic:,.0f}</h2><span style="color: {c2_m}; font-weight: 600; background: {bg2_m}; padding: 4px 12px; border-radius: 8px; font-size: 13px;">{arr2_m} {abs(mom_traf_pct):.1f}% MoM</span></div>
<div style="flex: 1; border-left: 2px solid #F0F1F6; padding-left: 30px;"><p class="text-muted" style="font-size: 14px; margin-bottom: 8px;">Last Year <span class="compare-date-str">{ly_str}</span></p><h2 class="text-main" style="margin: 0; font-size: 26px; margin-bottom: 12px;">{ly_traffic:,.0f}</h2><span style="color: {c2_y}; font-weight: 600; background: {bg2_y}; padding: 4px 12px; border-radius: 8px; font-size: 13px;">{arr2_y} {abs(yoy_traf_pct):.1f}% YoY</span></div>
</div>
""", unsafe_allow_html=True)

        def get_gsc_period_sum(start_d, end_d, seg='点击（GSC）'):
            if df_gsc is None or df_gsc.empty or not date_col_gsc: return 0.0
            c_clk = f"{seg}_点击次数"
            if c_clk not in df_gsc.columns: c_clk = f"{seg}_点击" 
            if c_clk not in df_gsc.columns:
                for c in df_gsc.columns:
                    if seg in c and ('点击' in c or 'click' in c.lower()):
                        c_clk = c
                        break
            if c_clk not in df_gsc.columns: return 0.0
            mask = (df_gsc[date_col_gsc] >= start_d) & (df_gsc[date_col_gsc] <= end_d)
            sub_df = df_gsc[mask]
            def clean_val(s):
                if pd.isna(s): return 0
                return pd.to_numeric(str(s).replace(',', '').replace('%', ''), errors='coerce')
            return sub_df[c_clk].apply(clean_val).fillna(0).sum()

        mtd_start = date(current_year, current_month, 1)
        mtd_gsc = get_gsc_period_sum(mtd_start, data_date)
        lm_gsc = get_gsc_period_sum(lm_start, lm_end)
        ly_gsc = get_gsc_period_sum(ly_start, ly_end)
        
        mom_gsc_pct = ((mtd_gsc - lm_gsc) / lm_gsc) * 100 if lm_gsc > 0 else 0.0
        yoy_gsc_pct = ((mtd_gsc - ly_gsc) / ly_gsc) * 100 if ly_gsc > 0 else 0.0
        c3_m, bg3_m, arr3_m = get_trend_ui(mom_gsc_pct)
        c3_y, bg3_y, arr3_y = get_trend_ui(yoy_gsc_pct)

        st.markdown(f"""
<div class="soft-card" style="display: flex; justify-content: space-between; text-align: left; padding-bottom:30px;">
<div style="flex: 1;"><p class="text-muted" style="font-size: 14px; margin-bottom: 8px;">GSC Clicks MTD <span class="compare-date-str">{curr_str}</span></p><h2 class="text-main" style="margin: 0; font-size: 32px;">{mtd_gsc:,.0f}</h2></div>
<div style="flex: 1; border-left: 2px solid #F0F1F6; padding-left: 30px;"><p class="text-muted" style="font-size: 14px; margin-bottom: 8px;">Last Month <span class="compare-date-str">{lm_str}</span></p><h2 class="text-main" style="margin: 0; font-size: 26px; margin-bottom: 12px;">{lm_gsc:,.0f}</h2><span style="color: {c3_m}; font-weight: 600; background: {bg3_m}; padding: 4px 12px; border-radius: 8px; font-size: 13px;">{arr3_m} {abs(mom_gsc_pct):.1f}% MoM</span></div>
<div style="flex: 1; border-left: 2px solid #F0F1F6; padding-left: 30px;"><p class="text-muted" style="font-size: 14px; margin-bottom: 8px;">Last Year <span class="compare-date-str">{ly_str}</span></p><h2 class="text-main" style="margin: 0; font-size: 26px; margin-bottom: 12px;">{ly_gsc:,.0f}</h2><span style="color: {c3_y}; font-weight: 600; background: {bg3_y}; padding: 4px 12px; border-radius: 8px; font-size: 13px;">{arr3_y} {abs(yoy_gsc_pct):.1f}% YoY</span></div>
</div>
""", unsafe_allow_html=True)

        st.markdown('<br><hr style="border:1px solid #E2E8F0; margin: 20px 0;"><br>', unsafe_allow_html=True)

        # ==========================================
        # ⭐ 新增: 全局免筛选年度趋势面板 (Annual Trends Overview YoY)
        # ==========================================
        st.markdown('<div class="flex-center" style="margin-bottom:6px;"><div class="icon-square bg-blue"><i class="fa-solid fa-chart-line"></i></div><h3 class="text-main" style="margin:0; font-size:22px;">Annual Trends (YoY Overview)</h3></div>', unsafe_allow_html=True)
        st.caption("Auto-aggregated monthly trends comparing 2026 vs 2025 across all available data.")
        
        # 1. 抽取 25/26 两年的数据列 (针对 df_de)
        def get_yearly_series(metric_names, target_year, is_curr=False):
            if isinstance(metric_names, str): metric_names = [metric_names]
            data = pd.DataFrame()
            for p in metric_names:
                target = p.replace(' ', '').lower()
                matched = df_de[df_de['Metric_Norm'] == target]
                if data.empty: matched = df_de[df_de['Metric_Norm'].str.contains(target, na=False)]
                if not matched.empty:
                    data = matched
                    break
            
            monthly_vals = {str(m): 0.0 for m in range(1, 13)}
            if not data.empty:
                for col in data.columns:
                    if col not in ['Metric', 'Metric_Norm']:
                        try:
                            dt = pd.to_datetime(col)
                            if dt.year == target_year:
                                val_raw = str(data[col].iloc[0]).replace(',', '').replace('$', '').replace('%', '')
                                val_num = pd.to_numeric(val_raw, errors='coerce')
                                if not pd.isna(val_num):
                                    monthly_vals[str(dt.month)] += val_num
                        except: pass
            
            res_vals = [monthly_vals[str(m)] for m in range(1, 13)]
            # 过滤掉全年全是0的情况，如果某月之后全是0（即未来月份），则截断
            if sum(res_vals) == 0: return []
            
            # 找到最后一个有数据的月份
            last_valid_month = 12
            for i in range(11, -1, -1):
                if res_vals[i] != 0:
                    last_valid_month = i + 1
                    break
                    
            # 2026年的数据，不能超过当前月份
            if target_year == current_year:
                last_valid_month = min(last_valid_month, current_month)
                
            return res_vals[:last_valid_month]

        # 2. 抽取 25/26 两年的数据 (针对 df_gsc)
        def get_gsc_yearly_series(seg, target_year):
            if df_gsc is None or df_gsc.empty or not date_col_gsc: return []
            c_clk = f"{seg}_点击次数"
            if c_clk not in df_gsc.columns: c_clk = f"{seg}_点击"
            if c_clk not in df_gsc.columns:
                for c in df_gsc.columns:
                    if seg in c and ('点击' in c or 'click' in c.lower()):
                        c_clk = c
                        break
            if c_clk not in df_gsc.columns: return []
            
            df_gsc['Temp_Year'] = pd.to_datetime(df_gsc[date_col_gsc]).dt.year
            df_gsc['Temp_Month'] = pd.to_datetime(df_gsc[date_col_gsc]).dt.month
            
            df_yr = df_gsc[df_gsc['Temp_Year'] == target_year].copy()
            if df_yr.empty: return []
            
            def clean_val(s):
                if pd.isna(s): return 0
                return pd.to_numeric(str(s).replace(',', '').replace('%', ''), errors='coerce')
                
            df_yr['Val_Clean'] = df_yr[c_clk].apply(clean_val)
            monthly_sum = df_yr.groupby('Temp_Month')['Val_Clean'].sum().to_dict()
            
            res_vals = [monthly_sum.get(m, 0.0) for m in range(1, 13)]
            if sum(res_vals) == 0: return []
            
            last_valid_month = 12
            if target_year == current_year:
                last_valid_month = current_month
                
            return res_vals[:last_valid_month]

        # 渲染两个模块的组合图表
        col_yoy_1, col_yoy_2 = st.columns(2)
        month_labels = [f"{m}月" for m in range(1, 13)]
        
        with col_yoy_1:
            st.markdown("""
            <div class="soft-card" style="padding: 16px 24px; margin-bottom: 16px; border-radius:
