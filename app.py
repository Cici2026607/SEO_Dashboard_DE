import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import calendar
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
        with col_target1: target_sales = st.number_input("🎯 DE Sales Target ($)", value=7500.0, step=500.0)
        with col_target2: target_traffic = st.number_input("⚡ DE Traffic Target", value=20000.0, step=1000.0)
                
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

        st.markdown('<br><hr style="border:1px solid #E2E8F0; margin: 20px 0;"><br>', unsafe_allow_html=True)

        # ==========================================
        # 4. 全局漏斗分析区间 
        # ==========================================
        valid_dates = list(date_mapping.values())
        min_date = min(valid_dates) if valid_dates else date.today()
        max_date = max(valid_dates) if valid_dates else date.today()

        header_col1, header_col2, header_col3 = st.columns([1.5, 1, 1])
        with header_col1:
            st.markdown('<div class="flex-center" style="margin-bottom:6px;"><div class="icon-square bg-blue"><i class="fa-regular fa-calendar"></i></div><h3 class="text-main" style="margin:0; font-size:22px;">Interval Analysis</h3></div>', unsafe_allow_html=True)
            st.caption("Modules below are strictly bounded by your date selection.")
        with header_col2:
            primary_dates = st.date_input("🗓️ Primary Date Range", [min_date, max_date])
        with header_col3:
            enable_compare = st.checkbox("🔄 Enable Trend Comparison")
            if enable_compare:
                compare_dates = st.date_input("🗓️ Compare Date Range", [min_date - timedelta(days=30), max_date - timedelta(days=30)])
            else: compare_dates = []

        if len(primary_dates) == 2: start_d1, end_d1 = primary_dates
        else: start_d1 = end_d1 = primary_dates[0]
        filtered_cols_1 = [col for col, dt in date_mapping.items() if start_d1 <= dt <= end_d1]

        if enable_compare and len(compare_dates) == 2:
            start_d2, end_d2 = compare_dates
            filtered_cols_2 = [col for col, dt in date_mapping.items() if start_d2 <= dt <= end_d2]
        else: filtered_cols_2 = []

        # ==========================================
        # 5. 区间漏斗与资产
        # ==========================================
        int_traffic = get_sum(['seo流量'], filtered_cols_1)
        int_blog = get_sum(['seoblog流量'], filtered_cols_1)
        int_insite = get_sum(['seo站内流量'], filtered_cols_1)
        int_site_total = get_sum(['网站总流量'], filtered_cols_1)
        
        int_bounce_rate = 0.0
        bounce_data = df_de[df_de['Metric_Norm'].str.contains('跳出率', na=False)]
        if not bounce_data.empty and filtered_cols_1:
            valid_br_cols = [c for c in filtered_cols_1 if c in bounce_data.columns]
            if valid_br_cols:
                br_vals = bounce_data[valid_br_cols].iloc[0].astype(str).str.replace('%', '', regex=False)
                br_series = pd.to_numeric(br_vals, errors='coerce').dropna()
                if not br_series.empty: int_bounce_rate = br_series.mean()

        int_ga4_sales = get_sum(['ga4seo销售额'], filtered_cols_1, True)
        int_super_sales = get_sum(['supersetseo销售额'], filtered_cols_1, True)
        ai_sales = get_sum(['aiassistant销售额'], filtered_cols_1, True)
        ai_traffic = get_sum(['aiassistant流量'], filtered_cols_1)
        
        def get_latest(possible_names, cols):
            if isinstance(possible_names, str): possible_names = [possible_names]
            data = pd.DataFrame()
            for p in possible_names:
                target = p.replace(' ', '').lower()
                matched = df_de[df_de['Metric_Norm'] == target]
                if data.empty: matched = df_de[df_de['Metric_Norm'].str.contains(target, na=False)]
                if not matched.empty:
                    data = matched
                    break
            if not data.empty and cols:
                valid_cols = [c for c in cols if c in data.columns]
                if valid_cols:
                    vals = data[valid_cols].iloc[0].replace(['None', 'nan', '', '#DIV/0!'], pd.NA).dropna()
                    if not vals.empty:
                        val = str(vals.iloc[-1]).replace(',', '').replace('$', '')
                        return pd.to_numeric(val, errors='coerce')
            return 0
            
        google_index = get_latest('收录', filtered_cols_1)
        google_backlinks = get_latest('外链', filtered_cols_1)
        google_domain = get_latest('外链域名广度', filtered_cols_1)

        comp_traffic = get_sum(['seo流量'], filtered_cols_2) if filtered_cols_2 else 0
        comp_blog = get_sum(['seoblog流量'], filtered_cols_2) if filtered_cols_2 else 0
        comp_insite = get_sum(['seo站内流量'], filtered_cols_2) if filtered_cols_2 else 0
        comp_site_total = get_sum(['网站总流量'], filtered_cols_2) if filtered_cols_2 else 0
        
        comp_bounce_rate = 0.0
        if not bounce_data.empty and filtered_cols_2:
            valid_br_cols_c = [c for c in filtered_cols_2 if c in bounce_data.columns]
            if valid_br_cols_c:
                br_vals_c = bounce_data[valid_br_cols_c].iloc[0].astype(str).str.replace('%', '', regex=False)
                br_series_c = pd.to_numeric(br_vals_c, errors='coerce').dropna()
                if not br_series_c.empty: comp_bounce_rate = br_series_c.mean()

        comp_ga4_sales = get_sum(['ga4seo销售额'], filtered_cols_2, True) if filtered_cols_2 else 0
        comp_super_sales = get_sum(['supersetseo销售额'], filtered_cols_2, True) if filtered_cols_2 else 0
        comp_ai_sales = get_sum(['aiassistant销售额'], filtered_cols_2, True) if filtered_cols_2 else 0
        comp_ai_traffic = get_sum(['aiassistant流量'], filtered_cols_2) if filtered_cols_2 else 0
        comp_google_index = get_latest('收录', filtered_cols_2) if filtered_cols_2 else 0
        comp_google_backlinks = get_latest('外链', filtered_cols_2) if filtered_cols_2 else 0
        comp_google_domain = get_latest('外链域名广度', filtered_cols_2) if filtered_cols_2 else 0

        def format_cmp(v1, v2, is_curr=False, is_pct=False, inverse=False, dark_bg=False):
            if not enable_compare: return ""
            if v2 == 0 and v1 > 0: pct = 999999
            elif v2 == 0 and v1 == 0: pct = 0
            else: pct = ((v1 - v2) / v2) * 100
            v2_str = f"$ {v2:,.2f}" if is_curr else (f"{v2:.2f}%" if is_pct else f"{v2:,.0f}")
            if pct == 0: c, arr, p_str = "#8E8CA7", "", "0.0%"
            else:
                c = "#22C55E" if (pct > 0 and not inverse) or (pct < 0 and inverse) else "#FF6475"
                arr = "↑" if pct > 0 else "↓"
                p_str = f"{abs(pct):.1f}%" if pct != 999999 else "+∞%"
            vs_c = "rgba(255,255,255,0.7)" if dark_bg else "#8E8CA7"
            return f"<div style='font-size:13px; color:{vs_c}; font-weight:500; margin-top:4px;'>vs {v2_str} <span style='color:{c}; font-weight:700; margin-left:4px;'>{arr} {p_str}</span></div>"

        st.markdown(f"""
<div class="soft-card">
<h4 class="text-main" style="margin-top: 0; margin-bottom: 24px; display: flex; align-items: center; font-size:18px;"><div class="icon-small bg-blue flex-center" style="justify-content:center;"><i class="fa-solid fa-filter"></i></div> Traffic Funnel Health</h4>
<div style="display: flex; justify-content: space-between; border-bottom: 2px dashed #F0F1F6; padding-bottom: 24px; margin-bottom: 18px;">
<div class="funnel-item" style="padding-left: 0;"><p class="funnel-title"><i class="fa-solid fa-circle funnel-dot" style="color:#2D235C;"></i> SEO 流量</p><p class="funnel-value" style="margin: 0;">{int_traffic:,.0f}</p>{format_cmp(int_traffic, comp_traffic)}</div>
<div class="funnel-item"><p class="funnel-title"><i class="fa-solid fa-circle funnel-dot" style="color:#42D2E6;"></i> SEO Blog 流量</p><p class="funnel-value" style="margin: 0;">{int_blog:,.0f}</p>{format_cmp(int_blog, comp_blog)}</div>
<div class="funnel-item"><p class="funnel-title"><i class="fa-solid fa-circle funnel-dot" style="color:#FF6475;"></i> SEO 站内流量</p><p class="funnel-value" style="margin: 0;">{int_insite:,.0f}</p>{format_cmp(int_insite, comp_insite)}</div>
<div class="funnel-item"><p class="funnel-title"><i class="fa-solid fa-circle funnel-dot" style="color:#FFB000;"></i> 网站总流量</p><p class="funnel-value" style="margin: 0;">{int_site_total:,.0f}</p>{format_cmp(int_site_total, comp_site_total)}</div>
<div class="funnel-item"><p class="funnel-title"><i class="fa-solid fa-circle funnel-dot" style="color:#8E8CA7;"></i> 跳出率</p><p class="funnel-value" style="margin: 0;">{int_bounce_rate:.2f}%</p>{format_cmp(int_bounce_rate, comp_bounce_rate, is_pct=True, inverse=True)}</div>
</div>
<p class="text-muted" style="font-size: 12px; margin: 0;">✦ Real-time data mapped for Callie DE.</p>
</div>
""", unsafe_allow_html=True)
        
        st.markdown(f"""
<div class="soft-card">
<h4 class="text-main" style="margin-top: 0; margin-bottom: 24px; display: flex; align-items: center; font-size:18px;"><div class="icon-small bg-red flex-center" style="justify-content:center;"><i class="fa-solid fa-sack-dollar"></i></div> Sales Breakdown (Selected Interval)</h4>
<div style="display: flex; gap: 20px;">
<div class="inner-box box-deep" style="flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;"><p class="box-label" style="justify-content: center; margin-bottom: 8px; color:rgba(255,255,255,0.9);"><i class="fa-solid fa-circle" style="color:#FF6475; font-size:8px; margin-right:8px;"></i> GA4 SEO Sales (Primary Source)</p><p class="box-value-white" style="font-size: 36px; margin: 0;">$ {int_ga4_sales:,.2f}</p>{format_cmp(int_ga4_sales, comp_ga4_sales, is_curr=True, dark_bg=True)}</div>
<div class="inner-box box-light" style="flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;"><p class="box-label text-muted" style="justify-content: center; margin-bottom: 8px;"><i class="fa-solid fa-circle" style="color:#FFB000; font-size:8px; margin-right:8px;"></i> Superset SEO Sales</p><p class="box-value-dark" style="font-size: 36px; margin: 0;">$ {int_super_sales:,.2f}</p>{format_cmp(int_super_sales, comp_super_sales, is_curr=True)}</div>
</div>
</div>
""", unsafe_allow_html=True)
        
        col_ai, col_google = st.columns(2)
        with col_ai:
            st.markdown(f"""
<div class="soft-card" style="height: 100%;">
<p class="asset-card-title" style="margin-bottom:12px;"><span class="icon-small bg-purple flex-center" style="display:inline-flex; justify-content:center; margin-bottom:-4px;"><i class="fa-solid fa-robot"></i></span> AI Assistant</p>
<div style="display: flex; margin-top:16px;">
<div class="inner-box box-deep"><p class="box-label" style="color:rgba(255,255,255,0.8);"><i class="fa-solid fa-circle" style="color:#FFB000; font-size:8px; margin-right:8px;"></i> AI Sales</p><p class="box-value-white" style="margin: 0;">$ {ai_sales:,.2f}</p>{format_cmp(ai_sales, comp_ai_sales, is_curr=True, dark_bg=True)}</div>
<div class="inner-box box-light"><p class="box-label text-muted"><i class="fa-solid fa-circle" style="color:#2D235C; font-size:8px; margin-right:8px;"></i> AI Traffic</p><p class="box-value-dark" style="margin: 0;">{ai_traffic:,.0f}</p>{format_cmp(ai_traffic, comp_ai_traffic)}</div>
</div>
</div>
""", unsafe_allow_html=True)
            
        with col_google:
            st.markdown(f"""
<div class="soft-card" style="height: 100%;">
<p class="asset-card-title" style="margin-bottom:12px;"><span class="icon-small bg-orange flex-center" style="display:inline-flex; justify-content:center; margin-bottom:-4px;"><i class="fa-brands fa-google"></i></span> Google Assets</p>
<div style="display: flex; margin-top:16px;">
<div class="inner-box box-light" style="flex: 1.2;"><p class="box-label text-muted"><i class="fa-solid fa-circle" style="color:#FFB000; font-size:8px; margin-right:8px;"></i> Indexing</p><p class="box-value-dark" style="margin: 0;">{google_index:,.0f}</p>{format_cmp(google_index, comp_google_index)}</div>
<div class="inner-box box-light"><p class="box-label text-muted"><i class="fa-solid fa-circle" style="color:#FF6475; font-size:8px; margin-right:8px;"></i> Backlinks</p><p class="box-value-dark" style="margin: 0;">{google_backlinks:,.0f}</p>{format_cmp(google_backlinks, comp_google_backlinks)}</div>
<div class="inner-box box-light"><p class="box-label text-muted"><i class="fa-solid fa-circle" style="color:#42D2E6; font-size:8px; margin-right:8px;"></i> Domains</p><p class="box-value-dark" style="margin: 0;">{google_domain:,.0f}</p>{format_cmp(google_domain, comp_google_domain)}</div>
</div>
</div>
""", unsafe_allow_html=True)

        # ==========================================
        # 6. 图表与明细 
        # ==========================================
        def hex_to_rgba(hex_color, alpha=0.1):
            hex_color = hex_color.lstrip('#')
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            return f'rgba({r}, {g}, {b}, {alpha})'

        def get_trend_series(possible_names, cols, is_curr=False):
            if isinstance(possible_names, str): possible_names = [possible_names]
            data = pd.DataFrame()
            for p in possible_names:
                target = p.replace(' ', '').lower()
                matched = df_de[df_de['Metric_Norm'] == target]
                if data.empty: matched = df_de[df_de['Metric_Norm'].str.contains(target, na=False)]
                if not matched.empty:
                    data = matched
                    break
            if not data.empty and cols:
                valid_cols = [c for c in cols if c in data.columns]
                if valid_cols:
                    vals = data[valid_cols].iloc[0].astype(str).str.replace(',', '', regex=False)
                    if is_curr: vals = vals.str.replace('$', '', regex=False)
                    return pd.to_numeric(vals, errors='coerce').fillna(0).tolist()
            return []

        sales_metrics_options = ['GA4 SEO销售额', 'Superset SEO销售额', 'AI Assistant 销售额']
        sales_colors = {'GA4 SEO销售额': '#FF6475', 'Superset SEO销售额': '#FFB000', 'AI Assistant 销售额': '#8B5CF6'}

        traffic_metrics_options = ['SEO流量', 'SEO Blog 流量', 'SEO 站内流量', '网站总流量', 'AI Assistant 流量']
        traffic_colors = {'SEO流量': '#2D235C', 'SEO Blog 流量': '#42D2E6', 'SEO 站内流量': '#FF6475', '网站总流量': '#FFB000', 'AI Assistant 流量': '#8B5CF6'}
        
        font_style = dict(family="Poppins, sans-serif", color="#8E8CA7")
        dates1 = [date_mapping[d].strftime('%Y-%m-%d') for d in filtered_cols_1]
        dates2 = [date_mapping[d].strftime('%Y-%m-%d') for d in filtered_cols_2] if filtered_cols_2 else []
        
        # Sales Chart
        st.markdown("""
<div class="soft-card" style="padding: 16px 24px; margin-bottom: 16px; border-radius: 16px;">
    <div class="flex-center">
        <div class="icon-small bg-red flex-center" style="justify-content:center; margin-bottom: 0;">
            <i class="fa-solid fa-chart-area"></i>
        </div>
        <span class="text-main" style="font-weight:700; font-size:16px;">Sales Trend Breakdown</span>
    </div>
</div>
""", unsafe_allow_html=True)
        selected_sales_metrics = st.multiselect("Select Sales Metrics", sales_metrics_options, default=['GA4 SEO销售额'], label_visibility="collapsed", key="sales_sel")
        
        fig_sales = go.Figure()
        if selected_sales_metrics:
            for metric in selected_sales_metrics:
                color = sales_colors[metric]
                if metric == 'GA4 SEO销售额': search_names = ['ga4seo销售额']
                elif metric == 'AI Assistant 销售额': search_names = ['aiassistant销售额']
                else: search_names = ['supersetseo销售额']
                
                s_trend1 = get_trend_series(search_names, filtered_cols_1, True)
                s_trend2 = get_trend_series(search_names, filtered_cols_2, True) if filtered_cols_2 else []
                
                if not s_trend2:
                    fig_sales.add_trace(go.Scatter(x=dates1, y=s_trend1, mode='lines', name=metric, line=dict(color=color, width=3, shape='spline'), fill='tozeroy', fillcolor=hex_to_rgba(color, 0.1)))
                else:
                    max_len = max(len(s_trend1), len(s_trend2))
                    x_axis = [f"Day {i+1}" for i in range(max_len)]
                    fig_sales.add_trace(go.Scatter(x=x_axis[:len(s_trend1)], y=s_trend1, mode='lines', name=f'{metric} (Pri)', line=dict(color=color, width=3, shape='spline')))
                    fig_sales.add_trace(go.Scatter(x=x_axis[:len(s_trend2)], y=s_trend2, mode='lines', name=f'{metric} (Cmp)', line=dict(color=color, width=3, dash='dash', shape='spline')))
            
        fig_sales.update_layout(font=font_style, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=10, b=0), height=350, xaxis=dict(showgrid=True, gridcolor='#F0F1F6'), yaxis=dict(showgrid=True, gridcolor='#F0F1F6', tickprefix="$"))
        st.plotly_chart(fig_sales, use_container_width=True)
        
        # Traffic Chart
        st.markdown("""
<div class="soft-card" style="padding: 16px 24px; margin-bottom: 16px; margin-top: 20px; border-radius: 16px;">
    <div class="flex-center">
        <div class="icon-small bg-blue flex-center" style="justify-content:center; margin-bottom: 0;">
            <i class="fa-solid fa-chart-line"></i>
        </div>
        <span class="text-main" style="font-weight:700; font-size:16px;">Traffic Breakdown</span>
    </div>
</div>
""", unsafe_allow_html=True)
        selected_traffic_metrics = st.multiselect("Select Traffic Metrics", traffic_metrics_options, default=['SEO流量'], label_visibility="collapsed", key="traf_sel")
        
        fig_traffic = go.Figure()
        if selected_traffic_metrics:
            for metric in selected_traffic_metrics:
                color = traffic_colors[metric]
                search_names = [metric.replace(' ', '').lower()]
                if metric == 'SEO Blog 流量': search_names = ['seoblog流量']
                elif metric == 'SEO 站内流量': search_names = ['seo站内流量']
                elif metric == '网站总流量': search_names = ['网站总流量']
                elif metric == 'AI Assistant 流量': search_names = ['aiassistant流量']
                elif metric == 'SEO流量': search_names = ['seo流量']

                t_trend1 = get_trend_series(search_names, filtered_cols_1)
                t_trend2 = get_trend_series(search_names, filtered_cols_2) if filtered_cols_2 else []
                
                if not t_trend2: 
                    fig_traffic.add_trace(go.Scatter(x=dates1, y=t_trend1, mode='lines', name=metric, line=dict(color=color, width=3, shape='spline'), fill='tozeroy', fillcolor=hex_to_rgba(color, 0.1)))
                else: 
                    max_len = max(len(t_trend1), len(t_trend2))
                    x_axis = [f"Day {i+1}" for i in range(max_len)]
                    fig_traffic.add_trace(go.Scatter(x=x_axis[:len(t_trend1)], y=t_trend1, mode='lines', name=f'{metric} (Pri)', line=dict(color=color, width=3, shape='spline')))
                    fig_traffic.add_trace(go.Scatter(x=x_axis[:len(t_trend2)], y=t_trend2, mode='lines', name=f'{metric} (Cmp)', line=dict(color=color, width=3, dash='dash', shape='spline')))

        fig_traffic.update_layout(font=font_style, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=10, b=0), height=350, xaxis=dict(showgrid=True, gridcolor='#F0F1F6'), yaxis=dict(showgrid=True, gridcolor='#F0F1F6'))
        st.plotly_chart(fig_traffic, use_container_width=True)

        # ==========================================
        # 7. GSC Performance Breakdown 
        # ==========================================
        if date_col_gsc and not df_gsc.empty:
            st.markdown("""
<div class="soft-card" style="padding: 16px 24px; margin-top: 20px; margin-bottom: 16px; border-radius: 16px;">
    <div class="flex-center">
        <div class="icon-small bg-orange flex-center" style="justify-content:center; margin-bottom: 0;">
            <i class="fa-brands fa-google"></i>
        </div>
        <span class="text-main" style="font-weight:700; font-size:16px;">GSC Performance Breakdown</span>
    </div>
</div>
""", unsafe_allow_html=True)
            
            col_gd1, col_gchk, col_gd2 = st.columns([1.5, 1, 1.5])
            with col_gd1:
                gsc_dates = st.date_input("🗓️ Primary Date Range (GSC)", [min_date, max_date], key="gsc_d1")
            with col_gchk:
                st.markdown('<div style="margin-top:28px;"></div>', unsafe_allow_html=True)
                enable_gsc_cmp = st.checkbox("☑️ Enable GSC Comparison", key="gsc_cmp_chk")
            with col_gd2:
                if enable_gsc_cmp:
                    gsc_comp_dates = st.date_input("🗓️ Compare Date Range (GSC)", [min_date - timedelta(days=30), max_date - timedelta(days=30)], key="gsc_d2")
                else:
                    gsc_comp_dates = []

            if len(gsc_dates) == 2: gs_start, gs_end = gsc_dates
            else: gs_start = gs_end = gsc_dates[0]
            
            mask_g1 = (df_gsc[date_col_gsc] >= gs_start) & (df_gsc[date_col_gsc] <= gs_end)
            df_gsc_1 = df_gsc[mask_g1].copy()
            dates_g1 = df_gsc_1[date_col_gsc].astype(str).tolist()

            df_gsc_2 = pd.DataFrame()
            if enable_gsc_cmp and len(gsc_comp_dates) == 2:
                gc_start, gc_end = gsc_comp_dates
                mask_g2 = (df_gsc[date_col_gsc] >= gc_start) & (df_gsc[date_col_gsc] <= gc_end)
                df_gsc_2 = df_gsc[mask_g2].copy()

            def clean_gsc(s):
                if pd.isna(s): return 0
                return pd.to_numeric(str(s).replace(',', '').replace('%', ''), errors='coerce')

            def get_gsc_clicks_series(df_source, seg):
                if df_source.empty: return []
                c_clk = f"{seg}_点击次数"
                if c_clk not in df_source.columns:
                    c_clk = f"{seg}_点击" 
                if c_clk not in df_source.columns:
                    for c in df_source.columns:
                        if seg in c and ('点击' in c or 'click' in c.lower()):
                            c_clk = c
                            break
                if c_clk in df_source.columns:
                    return df_source[c_clk].apply(clean_gsc).fillna(0).tolist()
                return []

            # ----------------- 找回 GSC Clicks Trend 折线图板块 (去白框) -----------------
            gsc_segments = ['点击（GSC）', '点击（非品牌词点击）', '点击（Blog）', '点击（非Blog）', '点击（非品牌词非Blog）', '点击（非品牌词非Blog非utm）']
            gsc_trend_colors = {
                '点击（GSC）': '#2D235C',
                '点击（非品牌词点击）': '#42D2E6',
                '点击（Blog）': '#FF6475',
                '点击（非Blog）': '#FFB000',
                '点击（非品牌词非Blog）': '#8B5CF6',
                '点击（非品牌词非Blog非utm）': '#10B981'
            }
            
            selected_gsc_metrics = st.multiselect("Select GSC Metrics", gsc_segments, default=['点击（GSC）'], label_visibility="collapsed", key="gsc_trend_sel")
            
            fig_gsc_trend = go.Figure()
            if selected_gsc_metrics and not df_gsc_1.empty:
                for metric in selected_gsc_metrics:
                    color = gsc_trend_colors[metric]
                    y_gsc1 = get_gsc_clicks_series(df_gsc_1, metric)
                    y_gsc2 = get_gsc_clicks_series(df_gsc_2, metric) if not df_gsc_2.empty else []
                    
                    if not enable_gsc_cmp:
                        fig_gsc_trend.add_trace(go.Scatter(x=dates_g1, y=y_gsc1, mode='lines', name=metric, line=dict(color=color, width=3, shape='spline'), fill='tozeroy', fillcolor=hex_to_rgba(color, 0.1)))
                    else:
                        max_len = max(len(y_gsc1), len(y_gsc2))
                        x_axis = [f"Day {j+1}" for j in range(max_len)]
                        fig_gsc_trend.add_trace(go.Scatter(x=x_axis[:len(y_gsc1)], y=y_gsc1, mode='lines', name=f'{metric} (Pri)', line=dict(color=color, width=3, shape='spline')))
                        fig_gsc_trend.add_trace(go.Scatter(x=x_axis[:len(y_gsc2)], y=y_gsc2, mode='lines', name=f'{metric} (Cmp)', line=dict(color=color, width=3, dash='dash', shape='spline')))
                
                fig_gsc_trend.update_layout(font=font_style, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=10, b=10), height=350, xaxis=dict(showgrid=True, gridcolor='#F0F1F6'), yaxis=dict(showgrid=True, gridcolor='#F0F1F6'))
                st.plotly_chart(fig_gsc_trend, use_container_width=True)
            elif df_gsc_1.empty:
                st.info("所选时间段暂无 GSC 数据。")
            
            # ----------------- 详细展示 Tabs -----------------
            gsc_tabs = st.tabs(gsc_segments)
                
            for i, tab in enumerate(gsc_tabs):
                with tab:
                    seg = gsc_segments[i]
                    c_clk = f"{seg}_点击次数"
                    c_imp = f"{seg}_展示"
                    c_ctr = f"{seg}_点击率"
                    c_pos = f"{seg}_排名"
                    
                    avail_cols = list(df_gsc.columns)
                    if c_clk not in avail_cols: c_clk = avail_cols[1] if len(avail_cols)>1 else avail_cols[-1]
                    if c_imp not in avail_cols: c_imp = avail_cols[2] if len(avail_cols)>2 else avail_cols[-1]
                    if c_ctr not in avail_cols: c_ctr = avail_cols[3] if len(avail_cols)>3 else avail_cols[-1]
                    if c_pos not in avail_cols: c_pos = avail_cols[4] if len(avail_cols)>4 else avail_cols[-1]
                    
                    with st.expander(f"⚙️ 数据列校准 (如当前无数据，请点此手动指定列)"):
                        c1, c2, c3, c4 = st.columns(4)
                        with c1: c_clk = st.selectbox("点击次数 (Clicks)", avail_cols, index=avail_cols.index(c_clk), key=f"clk_{i}")
                        with c2: c_imp = st.selectbox("展示 (Impressions)", avail_cols, index=avail_cols.index(c_imp), key=f"imp_{i}")
                        with c3: c_ctr = st.selectbox("点击率 (CTR)", avail_cols, index=avail_cols.index(c_ctr), key=f"ctr_{i}")
                        with c4: c_pos = st.selectbox("排名 (Position)", avail_cols, index=avail_cols.index(c_pos), key=f"pos_{i}")
                        
                    if not df_gsc_1.empty:
                        y_clk1 = df_gsc_1[c_clk].apply(clean_gsc).fillna(0).tolist()
                        y_imp1 = df_gsc_1[c_imp].apply(clean_gsc).fillna(0).tolist()
                        y_ctr1 = df_gsc_1[c_ctr].apply(clean_gsc).fillna(0).tolist()
                        y_pos1 = df_gsc_1[c_pos].apply(clean_gsc).fillna(0).tolist()

                        y_clk2 = df_gsc_2[c_clk].apply(clean_gsc).fillna(0).tolist() if not df_gsc_2.empty else []
                        y_imp2 = df_gsc_2[c_imp].apply(clean_gsc).fillna(0).tolist() if not df_gsc_2.empty else []
                        y_ctr2 = df_gsc_2[c_ctr].apply(clean_gsc).fillna(0).tolist() if not df_gsc_2.empty else []
                        y_pos2 = df_gsc_2[c_pos].apply(clean_gsc).fillna(0).tolist() if not df_gsc_2.empty else []

                        fig_g1 = make_subplots(specs=[[{"secondary_y": True}]])
                        if not enable_gsc_cmp:
                            fig_g1.add_trace(go.Bar(x=dates_g1, y=y_clk1, name="点击次数", marker=dict(color='rgba(66, 210, 230, 0.65)', line=dict(color='#42D2E6', width=2))), secondary_y=False)
                            fig_g1.add_trace(go.Scatter(x=dates_g1, y=y_imp1, mode='lines+markers', name="展示", line=dict(color='#FF6475', width=3, shape='spline'), marker=dict(size=8, color='#FF6475', line=dict(width=2, color='white'))), secondary_y=True)
                        else:
                            max_len = max(len(y_clk1), len(y_clk2))
                            x_axis = [f"Day {j+1}" for j in range(max_len)]
                            fig_g1.add_trace(go.Bar(x=x_axis[:len(y_clk1)], y=y_clk1, name="点击次数 (Pri)", marker=dict(color='rgba(66, 210, 230, 0.65)', line=dict(color='#42D2E6', width=2))), secondary_y=False)
                            fig_g1.add_trace(go.Bar(x=x_axis[:len(y_clk2)], y=y_clk2, name="点击次数 (Cmp)", marker=dict(color='rgba(142, 140, 167, 0.3)', line=dict(color='#8E8CA7', width=2))), secondary_y=False)
                            fig_g1.add_trace(go.Scatter(x=x_axis[:len(y_imp1)], y=y_imp1, mode='lines+markers', name="展示 (Pri)", line=dict(color='#FF6475', width=3, shape='spline'), marker=dict(size=8, color='#FF6475', line=dict(width=2, color='white'))), secondary_y=True)
                            fig_g1.add_trace(go.Scatter(x=x_axis[:len(y_imp2)], y=y_imp2, mode='lines+markers', name="展示 (Cmp)", line=dict(color='rgba(255, 100, 117, 0.5)', width=3, dash='dash', shape='spline'), marker=dict(size=8)), secondary_y=True)

                        fig_g1.update_layout(height=280, margin=dict(l=0, r=0, t=30, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(orientation="h", y=1.1, x=1, xanchor="right"))
                        fig_g1.update_xaxes(showgrid=True, gridcolor='#F0F1F6')
                        fig_g1.update_yaxes(showgrid=True, gridcolor='#F0F1F6', secondary_y=False)
                        st.plotly_chart(fig_g1, use_container_width=True)
                        
                        fig_g2 = make_subplots(specs=[[{"secondary_y": True}]])
                        if not enable_gsc_cmp:
                            fig_g2.add_trace(go.Scatter(x=dates_g1, y=y_ctr1, mode='lines+markers', name="点击率 (%)", line=dict(color='#22C55E', width=3, shape='spline'), marker=dict(size=7, color='#22C55E', line=dict(width=1.5, color='white'))), secondary_y=False)
                            fig_g2.add_trace(go.Scatter(x=dates_g1, y=y_pos1, mode='lines+markers', name="排名", line=dict(color='#8B5CF6', width=2, dash='dot', shape='spline'), marker=dict(size=6, color='#8B5CF6')), secondary_y=True)
                        else:
                            fig_g2.add_trace(go.Scatter(x=x_axis[:len(y_ctr1)], y=y_ctr1, mode='lines+markers', name="点击率 (Pri)", line=dict(color='#22C55E', width=3, shape='spline'), marker=dict(size=7, color='#22C55E', line=dict(width=1.5, color='white'))), secondary_y=False)
                            fig_g2.add_trace(go.Scatter(x=x_axis[:len(y_ctr2)], y=y_ctr2, mode='lines+markers', name="点击率 (Cmp)", line=dict(color='rgba(34, 197, 94, 0.5)', width=3, dash='dash', shape='spline'), marker=dict(size=7)), secondary_y=False)
                            fig_g2.add_trace(go.Scatter(x=x_axis[:len(y_pos1)], y=y_pos1, mode='lines+markers', name="排名 (Pri)", line=dict(color='#8B5CF6', width=2, dash='dot', shape='spline'), marker=dict(size=6, color='#8B5CF6')), secondary_y=True)
                            fig_g2.add_trace(go.Scatter(x=x_axis[:len(y_pos2)], y=y_pos2, mode='lines+markers', name="排名 (Cmp)", line=dict(color='rgba(139, 92, 246, 0.5)', width=2, dash='dash', shape='spline'), marker=dict(size=6)), secondary_y=True)

                        fig_g2.update_layout(height=280, margin=dict(l=0, r=0, t=30, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(orientation="h", y=1.1, x=1, xanchor="right"))
                        fig_g2.update_yaxes(autorange="reversed", secondary_y=True) 
                        fig_g2.update_xaxes(showgrid=True, gridcolor='#F0F1F6')
                        fig_g2.update_yaxes(showgrid=True, gridcolor='#F0F1F6', secondary_y=False)
                        st.plotly_chart(fig_g2, use_container_width=True)

        # ==========================================
        # 8. AI Performance Breakdown
        # ==========================================
        if date_col_ai and not df_ai.empty:
            st.markdown("""
<div class="soft-card" style="padding: 16px 24px; margin-top: 20px; margin-bottom: 16px; border-radius: 16px;">
    <div class="flex-center">
        <div class="icon-small bg-purple flex-center" style="justify-content:center; margin-bottom: 0;">
            <i class="fa-solid fa-microchip"></i>
        </div>
        <span class="text-main" style="font-weight:700; font-size:16px;">AI Performance Breakdown</span>
    </div>
</div>
""", unsafe_allow_html=True)
            
            col_ad1, col_achk, col_ad2 = st.columns([1.5, 1, 1.5])
            with col_ad1:
                ai_dates = st.date_input("🗓️ Primary Date Range (AI)", [min_date, max_date], key="ai_d1")
            with col_achk:
                st.markdown('<div style="margin-top:28px;"></div>', unsafe_allow_html=True)
                enable_ai_cmp = st.checkbox("☑️ Enable AI Comparison", key="ai_cmp_chk")
            with col_ad2:
                if enable_ai_cmp:
                    ai_comp_dates = st.date_input("🗓️ Compare Date Range (AI)", [min_date - timedelta(days=30), max_date - timedelta(days=30)], key="ai_d2")
                else:
                    ai_comp_dates = []

            if len(ai_dates) == 2: as_start, as_end = ai_dates
            else: as_start = as_end = ai_dates[0]
            
            mask_a1 = (df_ai[date_col_ai] >= as_start) & (df_ai[date_col_ai] <= as_end)
            df_ai_1 = df_ai[mask_a1].copy()
            dates_a1 = df_ai_1[date_col_ai].astype(str).tolist()

            df_ai_2 = pd.DataFrame()
            if enable_ai_cmp and len(ai_comp_dates) == 2:
                ac_start, ac_end = ai_comp_dates
                mask_a2 = (df_ai[date_col_ai] >= ac_start) & (df_ai[date_col_ai] <= ac_end)
                df_ai_2 = df_ai[mask_a2].copy()
            
            ai_metrics_options = [c for c in df_ai.columns if c != date_col_ai]
            selected_ai_metrics = st.multiselect("Select AI Metrics", ai_metrics_options, default=ai_metrics_options[:1] if ai_metrics_options else None, label_visibility="collapsed", key="ai_sel")
            
            fig_ai = go.Figure()
            if selected_ai_metrics and not df_ai_1.empty:
                colors = ['#8B5CF6', '#42D2E6', '#FF6475', '#FFB000', '#22C55E']
                for idx, metric in enumerate(selected_ai_metrics):
                    c_color = colors[idx % len(colors)]
                    
                    def clean_ai(s):
                        if pd.isna(s): return 0
                        return pd.to_numeric(str(s).replace(',', '').replace('%', ''), errors='coerce')
                    
                    y_ai1 = df_ai_1[metric].apply(clean_ai).fillna(0).tolist()
                    y_ai2 = df_ai_2[metric].apply(clean_ai).fillna(0).tolist() if not df_ai_2.empty else []
                    
                    if not enable_ai_cmp:
                        fig_ai.add_trace(go.Scatter(x=dates_a1, y=y_ai1, mode='lines', name=metric, line=dict(color=c_color, width=3, shape='spline'), fill='tozeroy', fillcolor=hex_to_rgba(c_color, 0.1)))
                    else:
                        max_len = max(len(y_ai1), len(y_ai2))
                        x_axis = [f"Day {j+1}" for j in range(max_len)]
                        fig_ai.add_trace(go.Scatter(x=x_axis[:len(y_ai1)], y=y_ai1, mode='lines', name=f'{metric} (Pri)', line=dict(color=c_color, width=3, shape='spline')))
                        fig_ai.add_trace(go.Scatter(x=x_axis[:len(y_ai2)], y=y_ai2, mode='lines', name=f'{metric} (Cmp)', line=dict(color=c_color, width=3, dash='dash', shape='spline')))
                
                fig_ai.update_layout(font=font_style, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=30, b=0), height=350, xaxis=dict(showgrid=True, gridcolor='#F0F1F6'), yaxis=dict(showgrid=True, gridcolor='#F0F1F6'))
                st.plotly_chart(fig_ai, use_container_width=True)
            elif df_ai_1.empty:
                st.info("所选时间段暂无 AI Performance 数据。")

        # ==========================================
        # 9. Custom Comparison Table (手动录入 + 动态表头 + 自动计算)
        # ==========================================
        st.markdown("""
<div class="soft-card" style="padding: 16px 24px; margin-top: 30px; margin-bottom: 16px; border-radius: 16px;">
    <div class="flex-center">
        <div class="icon-small bg-blue flex-center" style="justify-content:center; margin-bottom: 0;">
            <i class="fa-solid fa-table-list"></i>
        </div>
        <span class="text-main" style="font-weight:700; font-size:16px;">Weekly Data Comparison</span>
    </div>
</div>
""", unsafe_allow_html=True)
        
        col_td1, col_tspace, col_td2 = st.columns([1.5, 0.5, 1.5])
        default_t1_end = data_date
        default_t1_start = data_date - timedelta(days=6)
        default_t2_end = default_t1_start - timedelta(days=1)
        default_t2_start = default_t2_end - timedelta(days=6)
        
        with col_td1:
            t_dates_1 = st.date_input("🗓️ 本期时间 (Primary Period)", [default_t1_start, default_t1_end], key="tbl_d1")
        with col_tspace:
            st.markdown("<div style='text-align:center; padding-top:28px; font-weight:bold; color:#8E8CA7;'>VS</div>", unsafe_allow_html=True)
        with col_td2:
            t_dates_2 = st.date_input("🗓️ 参照时间 (Compare Period)", [default_t2_start, default_t2_end], key="tbl_d2")
            
        if len(t_dates_1) == 2: t1_start, t1_end = t_dates_1
        else: t1_start = t1_end = t_dates_1[0]
        
        if len(t_dates_2) == 2: t2_start, t2_end = t_dates_2
        else: t2_start = t2_end = t_dates_2[0]

        col_label_ref = f"{t2_start.month}/{t2_start.day}-{t2_end.month}/{t2_end.day} (参照期)"
        col_label_pri = f"{t1_start.month}/{t1_start.day}-{t1_end.month}/{t1_end.day} (本期)"

        metrics_list = [
            "销售额（GA4）", "流量（GA4）", "流量（Blog）", "流量（站内）", 
            "AI Assistant 流量", "AI Assistant 销售额", "点击（GSC）", 
            "AI Performance（总）", "AI Performance（非Blog）", "AI Performance（Blog）", 
            "点击（非品牌词）", "点击（Blog）", "点击（非Blog）", 
            "点击（非品牌词非Blog）", "点击（非品牌词非Blog非utm）"
        ]
        currency_metrics = ["销售额（GA4）", "AI Assistant 销售额"]

        if "manual_df" not in st.session_state:
            st.session_state.manual_df = pd.DataFrame({
                "指标 (Metric)": metrics_list,
                "参照期数值": [997.74, 3389, 2641, 666, 100, 221.60, 5322, 29405, 2049, 28723, 2308, 4461, 892, 161, 133],
                "本期数值": [1272.99, 4002, 3276, 745, 153, 105.51, 6825, 35927, 2313, 34811, 3136, 5858, 993, 169, 140]
            })

        st.caption("✍️ **手动录入区**：双击单元格可直接修改数值（支持从 Excel 复制整列粘贴）：")
        edited_df = st.data_editor(
            st.session_state.manual_df, 
            hide_index=True, 
            use_container_width=True,
            column_config={
                "指标 (Metric)": st.column_config.Column(disabled=True),
                "参照期数值": st.column_config.Column(label=col_label_ref),
                "本期数值": st.column_config.Column(label=col_label_pri)
            }
        )
        st.session_state.manual_df = edited_df

        html_table = f"""
<div class="soft-card" style="padding: 0; overflow: hidden; margin-top: 10px;">
<table style="width: 100%; border-collapse: collapse; text-align: center; font-family: 'Poppins', sans-serif;">
<thead style="background-color: #F8FAFC; border-bottom: 2px solid #E2E8F0;">
<tr>
<th style="padding: 16px; font-weight: 600; color: #2D235C; text-align: center;">指标 (Metric)</th>
<th style="padding: 16px; font-weight: 600; color: #2D235C;">{t2_start.month}/{t2_start.day}-{t2_end.month}/{t2_end.day}</th>
<th style="padding: 16px; font-weight: 600; color: #2D235C;">{t1_start.month}/{t1_start.day}-{t1_end.month}/{t1_end.day}</th>
<th style="padding: 16px; font-weight: 600; color: #2D235C;">环比上期 (Change)</th>
</tr>
</thead>
<tbody>
"""
        for i, row in edited_df.iterrows():
            m_name = row["指标 (Metric)"]
            try: v2 = float(str(row["参照期数值"]).replace(',', '').replace('$', '').replace('%', '').strip())
            except: v2 = 0.0
            try: v1 = float(str(row["本期数值"]).replace(',', '').replace('$', '').replace('%', '').strip())
            except: v1 = 0.0
            
            is_curr = m_name in currency_metrics
            v1_str = f"${v1:,.2f}" if is_curr else f"{v1:,.0f}"
            v2_str = f"${v2:,.2f}" if is_curr else f"{v2:,.0f}"
            
            if v2 == 0 and v1 > 0: pct = 999999
            elif v2 == 0 and v1 == 0: pct = 0
            else: pct = ((v1 - v2) / v2) * 100
            
            if pct == 0: pct_str, pct_color = "0.00%", "#8E8CA7"
            elif pct == 999999: pct_str, pct_color = "+∞%", "#22C55E"
            else:
                sign = "+" if pct > 0 else ""
                pct_str = f"{sign}{pct:.2f}%"
                pct_color = "#22C55E" if pct > 0 else "#FF6475"
                
            html_table += f"""
<tr style="border-bottom: 1px solid #F0F1F6;">
<td style="padding: 14px; font-weight: 500; color: #2D235C;">{m_name}</td>
<td style="padding: 14px; color: #8E8CA7;">{v2_str}</td>
<td style="padding: 14px; color: #2D235C; font-weight: 500;">{v1_str}</td>
<td style="padding: 14px; font-weight: 700; color: {pct_color};">{pct_str}</td>
</tr>
"""
        html_table += "</tbody></table></div>"
        st.markdown(html_table, unsafe_allow_html=True)

        # ==========================================
        # 10. Raw Tables
        # ==========================================
        st.markdown("""
<div class="soft-card" style="padding: 16px 24px; margin-top: 30px; margin-bottom: 16px; border-radius: 16px;">
    <div class="flex-center">
        <div class="icon-small bg-gray flex-center" style="justify-content:center; margin-bottom: 0;">
            <i class="fa-solid fa-database"></i>
        </div>
        <span class="text-main" style="font-weight:700; font-size:16px;">Raw Data Matrix (Callie DE)</span>
    </div>
</div>
""", unsafe_allow_html=True)
        df_display = df_de[['Metric'] + [c for c in filtered_cols_1 if c in df_de.columns]].copy()
        df_display.columns = ['Metric'] + dates1
        df_display = df_display.set_index('Metric')
        st.dataframe(df_display, use_container_width=True, height=350)
        
        if date_col_gsc and not df_gsc.empty:
            st.markdown("""
<div class="soft-card" style="padding: 16px 24px; margin-top: 30px; margin-bottom: 16px; border-radius: 16px;">
    <div class="flex-center">
        <div class="icon-small bg-gray flex-center" style="justify-content:center; margin-bottom: 0;">
            <i class="fa-brands fa-google"></i>
        </div>
        <span class="text-main" style="font-weight:700; font-size:16px;">Raw Data Matrix (GSC)</span>
    </div>
</div>
""", unsafe_allow_html=True)
            st.dataframe(df_gsc_1, use_container_width=True, height=350)
            
        if date_col_ai and not df_ai.empty:
            st.markdown("""
<div class="soft-card" style="padding: 16px 24px; margin-top: 30px; margin-bottom: 16px; border-radius: 16px;">
    <div class="flex-center">
        <div class="icon-small bg-gray flex-center" style="justify-content:center; margin-bottom: 0;">
            <i class="fa-solid fa-microchip"></i>
        </div>
        <span class="text-main" style="font-weight:700; font-size:16px;">Raw Data Matrix (AI Performance)</span>
    </div>
</div>
""", unsafe_allow_html=True)
            st.dataframe(df_ai_1, use_container_width=True, height=350)

except Exception as e:
    st.error("Error occurred during rendering:")
    st.write(e)
