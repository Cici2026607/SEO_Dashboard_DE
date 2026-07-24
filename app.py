import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import calendar
import plotly.graph_objects as go

# ==========================================
# 0. Page Config
# ==========================================
st.set_page_config(page_title="Callie DE - SEO Dashboard", page_icon="🇩🇪", layout="wide")

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
    
    /* 🇩🇪 德国专属定制：黑 -> 深红 -> 质感金 的高级渐变 */
    .welcome-banner {
        background: linear-gradient(135deg, #1A1A24 0%, #9B1B30 65%, #D4AF37 100%); 
        border-radius: 28px; padding: 32px 40px; color: white; margin-bottom: 30px; 
        box-shadow: 0 16px 32px -10px rgba(155, 27, 48, 0.4); position: relative; overflow: hidden;
    }
    .welcome-banner h1 { color: white !important; font-size: 36px; font-weight: 800; margin: 0 0 8px 0; }
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

try:
    with st.spinner('🚀 同步 Callie DE 德语站最新数据...'):
        df_de = load_and_clean_data()

        # ==========================================
        # ⭐ T-2 GA 数据延迟基准日逻辑
        # ==========================================
        real_today = datetime.now().date()
        data_date = real_today - timedelta(days=2)  # MTD 记录时间延后2天
        current_year, current_month = data_date.year, data_date.month

        # Welcome Banner (加入显眼的国旗)
        st.markdown(f"""
        <div class="welcome-banner">
            <h1>🇩🇪 Hallo, Callie DE Team!</h1>
            <p>Germany (DE) SEO Global Dashboard • Data Date: {data_date.strftime('%Y-%m-%d')} (T-2 GA Delay)</p>
        </div>
        """, unsafe_allow_html=True)
        
        # UI目标输入：硬编码默认值为 9000 和 23000
        col_btn, col_target1, col_target2 = st.columns([1.5, 2, 2])
        with col_btn:
            if st.button("🔄 Sync Data"):
                load_and_clean_data.clear()
                st.rerun()
        with col_target1:
            target_sales = st.number_input("🎯 DE Sales Target ($)", value=9000.0, step=500.0)
        with col_target2:
            target_traffic = st.number_input("⚡ DE Traffic Target", value=23000.0, step=1000.0)
                
        # ==========================================
        # 2. 日期匹配与强力清洗查表函数
        # ==========================================
        date_mapping = {}
        for col in df_de.columns:
            if col not in ['Metric', 'Metric_Norm']:
                try:
                    dt = pd.to_datetime(col).date()
                    date_mapping[col] = dt
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
            
        def get_latest(possible_names, cols):
            if isinstance(possible_names, str): possible_names = [possible_names]
            data = pd.DataFrame()
            for p in possible_names:
                target = p.replace(' ', '').lower()
                matched = df_de[df_de['Metric_Norm'].str.contains(target, na=False)]
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

        mtd_sales = get_sum(['ga4seo销售额', 'ga4销售额'], mtd_cols, True)
        lm_sales = get_sum(['ga4seo销售额', 'ga4销售额'], lm_cols, True)
        ly_sales = get_sum(['ga4seo销售额', 'ga4销售额'], ly_cols, True)

        mtd_traffic = get_sum(['seo流量', '流量'], mtd_cols)
        lm_traffic = get_sum(['seo流量', '流量'], lm_cols)
        ly_traffic = get_sum(['seo流量', '流量'], ly_cols)

        prog_sales = min(mtd_sales / target_sales, 1.0) if target_sales > 0 else 0
        prog_traffic = min(mtd_traffic / target_traffic, 1.0) if target_traffic > 0 else 0
        gap_sales = max(0, target_sales - mtd_sales)
        gap_traffic = max(0, target_traffic - mtd_traffic)

        # 3.1 Target Achievement
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
                <div class="progress-track">
                    <div class="progress-fill-red" style="width: {prog_sales*100}%;"></div>
                    <span class="rocket-icon">🎯</span>
                </div>
                <div style="text-align: right; margin-top: 16px;">
                    <span style="color: #FF6475; font-weight: 800; font-size: 18px;">{prog_sales*100:.1f}%</span>
                </div>
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
                <div class="progress-track">
                    <div class="progress-fill-blue" style="width: {prog_traffic*100}%;"></div>
                    <span class="rocket-icon">⚡</span>
                </div>
                <div style="text-align: right; margin-top: 16px;">
                    <span style="color: #42D2E6; font-weight: 800; font-size: 18px;">{prog_traffic*100:.1f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 3.2 MTD 同环比计算
        st.markdown('<div class="flex-center" style="margin:30px 0 20px 0;"><div class="icon-square bg-purple"><i class="fa-solid fa-chart-simple"></i></div><h3 class="text-main" style="margin:0; font-size:22px;">MTD Monitoring</h3></div>', unsafe_allow_html=True)
        def get_trend_ui(pct): return ("#FF6475" if pct < 0 else "#22C55E", "#FFF0F2" if pct < 0 else "#F0FDF4", "↓" if pct < 0 else "↑")

        mom_sales_pct = ((mtd_sales - lm_sales) / lm_sales) * 100 if lm_sales > 0 else 0.0
        yoy_sales_pct = ((mtd_sales - ly_sales) / ly_sales) * 100 if ly_sales > 0 else 0.0
        c1_m, bg1_m, arr1_m = get_trend_ui(mom_sales_pct)
        c1_y, bg1_y, arr1_y = get_trend_ui(yoy_sales_pct)

        st.markdown(f"""
        <div class="soft-card" style="display: flex; justify-content: space-between; text-align: left; padding-bottom:30px;">
            <div style="flex: 1;">
                <p class="text-muted" style="font-size: 14px; margin-bottom: 8px;">Sales MTD (GA4) <span class="compare-date-str">{curr_str}</span></p>
                <h2 class="text-main" style="margin: 0; font-size: 32px;">$ {mtd_sales:,.2f}</h2>
            </div>
            <div style="flex: 1; border-left: 2px solid #F0F1F6; padding-left: 30px;">
                <p class="text-muted" style="font-size: 14px; margin-bottom: 8px;">Last Month <span class="compare-date-str">{lm_str}</span></p>
                <h2 class="text-main" style="margin: 0; font-size: 26px; margin-bottom: 12px;">$ {lm_sales:,.2f}</h2>
                <span style="color: {c1_m}; font-weight: 600; background: {bg1_m}; padding: 4px 12px; border-radius: 8px; font-size: 13px;">{arr1_m} {abs(mom_sales_pct):.1f}% MoM</span>
            </div>
            <div style="flex: 1; border-left: 2px solid #F0F1F6; padding-left: 30px;">
                <p class="text-muted" style="font-size: 14px; margin-bottom: 8px;">Last Year <span class="compare-date-str">{ly_str}</span></p>
                <h2 class="text-main" style="margin: 0; font-size: 26px; margin-bottom: 12px;">$ {ly_sales:,.2f}</h2>
                <span style="color: {c1_y}; font-weight: 600; background: {bg1_y}; padding: 4px 12px; border-radius: 8px; font-size: 13px;">{arr1_y} {abs(yoy_sales_pct):.1f}% YoY</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        mom_traf_pct = ((mtd_traffic - lm_traffic) / lm_traffic) * 100 if lm_traffic > 0 else 0.0
        yoy_traf_pct = ((mtd_traffic - ly_traffic) / ly_traffic) * 100 if ly_traffic > 0 else 0.0
        c2_m, bg2_m, arr2_m = get_trend_ui(mom_traf_pct)
        c2_y, bg2_y, arr2_y = get_trend_ui(yoy_traf_pct)

        st.markdown(f"""
        <div class="soft-card" style="display: flex; justify-content: space-between; text-align: left; padding-bottom:30px;">
            <div style="flex: 1;">
                <p class="text-muted" style="font-size: 14px; margin-bottom: 8px;">Traffic MTD <span class="compare-date-str">{curr_str}</span></p>
                <h2 class="text-main" style="margin: 0; font-size: 32px;">{mtd_traffic:,.0f}</h2>
            </div>
            <div style="flex: 1; border-left: 2px solid #F0F1F6; padding-left: 30px;">
                <p class="text-muted" style="font-size: 14px; margin-bottom: 8px;">Last Month <span class="compare-date-str">{lm_str}</span></p>
                <h2 class="text-main" style="margin: 0; font-size: 26px; margin-bottom: 12px;">{lm_traffic:,.0f}</h2>
                <span style="color: {c2_m}; font-weight: 600; background: {bg2_m}; padding: 4px 12px; border-radius: 8px; font-size: 13px;">{arr2_m} {abs(mom_traf_pct):.1f}% MoM</span>
            </div>
            <div style="flex: 1; border-left: 2px solid #F0F1F6; padding-left: 30px;">
                <p class="text-muted" style="font-size: 14px; margin-bottom: 8px;">Last Year <span class="compare-date-str">{ly_str}</span></p>
                <h2 class="text-main" style="margin: 0; font-size: 26px; margin-bottom: 12px;">{ly_traffic:,.0f}</h2>
                <span style="color: {c2_y}; font-weight: 600; background: {bg2_y}; padding: 4px 12px; border-radius: 8px; font-size: 13px;">{arr2_y} {abs(yoy_traf_pct):.1f}% YoY</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<br><hr style="border:1px solid #E2E8F0; margin: 20px 0;"><br>', unsafe_allow_html=True)

        # ==========================================
        # 4. 全局漏斗分析区间 (彻底采用单日分拆模式)
        # ==========================================
        valid_dates = list(date_mapping.values())
        min_date = min(valid_dates) if valid_dates else date.today()
        max_date = max(valid_dates) if valid_dates else date.today()

        st.markdown('<div class="flex-center" style="margin-bottom:6px;"><div class="icon-square bg-blue"><i class="fa-regular fa-calendar"></i></div><h3 class="text-main" style="margin:0; font-size:22px;">Interval Analysis</h3></div>', unsafe_allow_html=True)
        st.caption("Modules below (Funnel & Table) are bounded by this selection.")
        
        col_g1, col_g2, col_g3 = st.columns([1, 1, 2])
        with col_g1: start_d1 = st.date_input("🗓️ 开始日期 (Start)", min_date, key="g_start")
        with col_g2: end_d1 = st.date_input("🗓️ 结束日期 (End)", max_date, key="g_end")

        filtered_cols_1 = [col for col, dt in date_mapping.items() if start_d1 <= dt <= end_d1]

        # ==========================================
        # 5. 区间漏斗与资产
        # ==========================================
        int_traffic = get_sum(['seo流量', '流量'], filtered_cols_1)
        int_blog = get_sum(['seo blog 流量', 'blog流量'], filtered_cols_1)
        int_insite = get_sum(['seo 站内流量', '站内流量'], filtered_cols_1)
        int_site_total = get_sum(['网站总流量', '总流量'], filtered_cols_1)
        
        int_bounce_rate = 0.0
        bounce_data = df_de[df_de['Metric_Norm'].str.contains('跳出率', na=False)]
        if not bounce_data.empty and filtered_cols_1:
            valid_br_cols = [c for c in filtered_cols_1 if c in bounce_data.columns]
            if valid_br_cols:
                br_vals = bounce_data[valid_br_cols].iloc[0].astype(str).str.replace('%', '', regex=False)
                br_series = pd.to_numeric(br_vals, errors='coerce').dropna()
                if not br_series.empty: int_bounce_rate = br_series.mean()

        int_ga4_sales = get_sum(['ga4seo销售额', 'ga4销售额'], filtered_cols_1, True)
        int_super_sales = get_sum(['supersetseo销售额', 'seo销售额', 'superset'], filtered_cols_1, True)

        ai_sales = get_sum(['aiassistant销售额', 'ai销售额'], filtered_cols_1, True)
        ai_traffic = get_sum(['aiassistant流量', 'ai流量'], filtered_cols_1)
        google_index = get_latest('收录', filtered_cols_1)
        google_backlinks = get_latest('外链', filtered_cols_1)
        google_domain = get_latest('外链域名广度', filtered_cols_1)

        # 漏斗
        st.markdown(f"""
        <div class="soft-card">
            <h4 class="text-main" style="margin-top: 0; margin-bottom: 24px; display: flex; align-items: center; font-size:18px;">
                <div class="icon-small bg-blue flex-center" style="justify-content:center;"><i class="fa-solid fa-filter"></i></div> Traffic Funnel Health
            </h4>
            <div style="display: flex; justify-content: space-between; border-bottom: 2px dashed #F0F1F6; padding-bottom: 24px; margin-bottom: 18px;">
                <div class="funnel-item" style="padding-left: 0;"><p class="funnel-title"><i class="fa-solid fa-circle funnel-dot" style="color:#2D235C;"></i> SEO 流量</p><p class="funnel-value">{int_traffic:,.0f}</p></div>
                <div class="funnel-item"><p class="funnel-title"><i class="fa-solid fa-circle funnel-dot" style="color:#42D2E6;"></i> SEO Blog 流量</p><p class="funnel-value">{int_blog:,.0f}</p></div>
                <div class="funnel-item"><p class="funnel-title"><i class="fa-solid fa-circle funnel-dot" style="color:#FF6475;"></i> SEO 站内流量</p><p class="funnel-value">{int_insite:,.0f}</p></div>
                <div class="funnel-item"><p class="funnel-title"><i class="fa-solid fa-circle funnel-dot" style="color:#FFB000;"></i> 网站总流量</p><p class="funnel-value">{int_site_total:,.0f}</p></div>
                <div class="funnel-item"><p class="funnel-title"><i class="fa-solid fa-circle funnel-dot" style="color:#8E8CA7;"></i> 跳出率</p><p class="funnel-value">{int_bounce_rate:.2f}%</p></div>
            </div>
            <p class="text-muted" style="font-size: 12px; margin: 0;">✦ Real-time data mapped for Callie DE.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 销售拆解 
        st.markdown(f"""
        <div class="soft-card">
            <h4 class="text-main" style="margin-top: 0; margin-bottom: 24px; display: flex; align-items: center; font-size:18px;">
                <div class="icon-small bg-red flex-center" style="justify-content:center;"><i class="fa-solid fa-sack-dollar"></i></div> Sales Breakdown (Selected Interval)
            </h4>
            <div style="display: flex; gap: 20px;">
                <div class="inner-box box-deep" style="flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
                    <p class="box-label" style="justify-content: center; margin-bottom: 8px; color:rgba(255,255,255,0.9);"><i class="fa-solid fa-circle" style="color:#FF6475; font-size:8px; margin-right:8px;"></i> GA4 SEO Sales (Primary Source)</p>
                    <p class="box-value-white" style="font-size: 36px;">$ {int_ga4_sales:,.2f}</p>
                </div>
                <div class="inner-box box-light" style="flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
                    <p class="box-label text-muted" style="justify-content: center; margin-bottom: 8px;"><i class="fa-solid fa-circle" style="color:#FFB000; font-size:8px; margin-right:8px;"></i> Superset SEO Sales</p>
                    <p class="box-value-dark" style="font-size: 36px;">$ {int_super_sales:,.2f}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 资产
        col_ai, col_google = st.columns(2)
        with col_ai:
            st.markdown(f"""
            <div class="soft-card" style="height: 100%;">
                <p class="asset-card-title"><div class="icon-small bg-purple flex-center" style="display:inline-flex; justify-content:center; margin-bottom:-4px;"><i class="fa-solid fa-robot"></i></div> AI Assistant</p>
                <div style="display: flex; margin-top:24px;">
                    <div class="inner-box box-deep">
                        <p class="box-label" style="color:rgba(255,255,255,0.8);"><i class="fa-solid fa-circle" style="color:#FFB000; font-size:8px; margin-right:8px;"></i> AI Sales</p>
                        <p class="box-value-white">$ {ai_sales:,.2f}</p>
                    </div>
                    <div class="inner-box box-light">
                        <p class="box-label text-muted"><i class="fa-solid fa-circle" style="color:#2D235C; font-size:8px; margin-right:8px;"></i> AI Traffic</p>
                        <p class="box-value-dark">{ai_traffic:,.0f}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_google:
            st.markdown(f"""
            <div class="soft-card" style="height: 100%;">
                <p class="asset-card-title"><div class="icon-small bg-orange flex-center" style="display:inline-flex; justify-content:center; margin-bottom:-4px;"><i class="fa-brands fa-google"></i></div> Google Assets</p>
                <div style="display: flex; margin-top:24px;">
                    <div class="inner-box box-light" style="flex: 1.2;">
                        <p class="box-label text-muted"><i class="fa-solid fa-circle" style="color:#FFB000; font-size:8px; margin-right:8px;"></i> Indexing</p>
                        <p class="box-value-dark">{google_index:,.0f}</p>
                    </div>
                    <div class="inner-box box-light">
                        <p class="box-label text-muted"><i class="fa-solid fa-circle" style="color:#FF6475; font-size:8px; margin-right:8px;"></i> Backlinks</p>
                        <p class="box-value-dark">{google_backlinks:,.0f}</p>
                    </div>
                    <div class="inner-box box-light">
                        <p class="box-label text-muted"><i class="fa-solid fa-circle" style="color:#42D2E6; font-size:8px; margin-right:8px;"></i> Domains</p>
                        <p class="box-value-dark">{google_domain:,.0f}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ==========================================
        # 6. 图表与明细 (彻底拆分为独立的单选日期，完美解决系统Dropdown干扰)
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
                matched = df_de[df_de['Metric_Norm'].str.contains(target, na=False)]
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

        sales_metrics_options = ['GA4 SEO销售额', 'Superset SEO销售额']
        sales_colors = {'GA4 SEO销售额': '#FF6475', 'Superset SEO销售额': '#FFB000'}

        traffic_metrics_options = ['SEO流量', 'SEO Blog 流量', 'SEO 站内流量', '网站总流量']
        traffic_colors = {'SEO流量': '#2D235C', 'SEO Blog 流量': '#42D2E6', 'SEO 站内流量': '#FF6475', '网站总流量': '#FFB000'}
        
        font_style = dict(family="Poppins, sans-serif", color="#8E8CA7")
        
        # ---------------- Sales Chart ----------------
        st.markdown('<div class="soft-card" style="padding-bottom:10px;"><div class="flex-center" style="margin-bottom:20px; justify-content:space-between;"><div class="flex-center"><div class="icon-small bg-red flex-center" style="justify-content:center;"><i class="fa-solid fa-chart-area"></i></div><span class="text-main" style="font-weight:700; font-size:16px;">Sales Trend Breakdown</span></div></div>', unsafe_allow_html=True)
        
        col_s_m, col_s_d = st.columns([1, 2])
        with col_s_m:
            selected_sales_metrics = st.multiselect("Select Sales Metrics", sales_metrics_options, default=['GA4 SEO销售额'], label_visibility="collapsed", key="sales_sel")
            st.markdown('<div style="margin-top:10px;"></div>', unsafe_allow_html=True)
            enable_s_cmp = st.checkbox("☑️ 添加对比时间段 (Enable Compare)", key="s_cmp_chk")
            
        with col_s_d:
            # 第一排：主时间
            sd_col1, sd_col2 = st.columns(2)
            with sd_col1: s_start = st.date_input("开始日期", min_date, key="s_start_1")
            with sd_col2: s_end = st.date_input("结束日期", max_date, key="s_end_1")
            
            # 第二排：对比时间
            if enable_s_cmp:
                st.markdown("<div style='margin: 4px 0; font-size: 14px; font-weight: bold; color: #8E8CA7;'>与 (VS)</div>", unsafe_allow_html=True)
                sc_col1, sc_col2 = st.columns(2)
                with sc_col1: sc_start = st.date_input("开始日期", min_date - timedelta(days=30), key="s_start_2")
                with sc_col2: sc_end = st.date_input("结束日期", max_date - timedelta(days=30), key="s_end_2")
            else:
                sc_start = sc_end = None
                
        sales_cols = [col for col, dt in date_mapping.items() if s_start <= dt <= s_end]
        sales_dates_str = [date_mapping[d].strftime('%Y-%m-%d') for d in sales_cols]
        
        sales_comp_cols = []
        if enable_s_cmp and sc_start and sc_end:
            sales_comp_cols = [col for col, dt in date_mapping.items() if sc_start <= dt <= sc_end]
        
        fig_sales = go.Figure()
        if selected_sales_metrics:
            for metric in selected_sales_metrics:
                color = sales_colors[metric]
                search_names = ['ga4seo销售额', 'ga4销售额'] if metric == 'GA4 SEO销售额' else ['supersetseo销售额', 'seo销售额', 'superset']
                
                s_trend1 = get_trend_series(search_names, sales_cols, True)
                s_trend2 = get_trend_series(search_names, sales_comp_cols, True) if sales_comp_cols else []
                
                if not s_trend2:
                    fig_sales.add_trace(go.Scatter(x=sales_dates_str, y=s_trend1, mode='lines', name=metric, line=dict(color=color, width=3, shape='spline'), fill='tozeroy', fillcolor=hex_to_rgba(color, 0.1)))
                else:
                    max_len = max(len(s_trend1), len(s_trend2))
                    x_axis = [f"Day {i+1}" for i in range(max_len)]
                    fig_sales.add_trace(go.Scatter(x=x_axis[:len(s_trend1)], y=s_trend1, mode='lines', name=f'{metric} (Primary)', line=dict(color=color, width=3, shape='spline')))
                    fig_sales.add_trace(go.Scatter(x=x_axis[:len(s_trend2)], y=s_trend2, mode='lines', name=f'{metric} (Compare)', line=dict(color=color, width=3, dash='dash', shape='spline')))
            
        fig_sales.update_layout(font=font_style, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=10, b=0), height=350, xaxis=dict(showgrid=True, gridcolor='#F0F1F6'), yaxis=dict(showgrid=True, gridcolor='#F0F1F6', tickprefix="$"))
        st.plotly_chart(fig_sales, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ---------------- Traffic Chart ----------------
        st.markdown('<div class="soft-card" style="padding-bottom:10px;"><div class="flex-center" style="margin-bottom:20px; justify-content:space-between;"><div class="flex-center"><div class="icon-small bg-blue flex-center" style="justify-content:center;"><i class="fa-solid fa-chart-line"></i></div><span class="text-main" style="font-weight:700; font-size:16px;">Traffic Breakdown</span></div></div>', unsafe_allow_html=True)
        
        col_t_m, col_t_d = st.columns([1, 2])
        with col_t_m:
            selected_traffic_metrics = st.multiselect("Select Traffic Metrics", traffic_metrics_options, default=['SEO流量'], label_visibility="collapsed", key="traf_sel")
            st.markdown('<div style="margin-top:10px;"></div>', unsafe_allow_html=True)
            enable_t_cmp = st.checkbox("☑️ 添加对比时间段 (Enable Compare)", key="t_cmp_chk")
            
        with col_t_d:
            td_col1, td_col2 = st.columns(2)
            with td_col1: t_start = st.date_input("开始日期", min_date, key="t_start_1")
            with td_col2: t_end = st.date_input("结束日期", max_date, key="t_end_1")
            
            if enable_t_cmp:
                st.markdown("<div style='margin: 4px 0; font-size: 14px; font-weight: bold; color: #8E8CA7;'>与 (VS)</div>", unsafe_allow_html=True)
                tc_col1, tc_col2 = st.columns(2)
                with tc_col1: tc_start = st.date_input("开始日期", min_date - timedelta(days=30), key="t_start_2")
                with tc_col2: tc_end = st.date_input("结束日期", max_date - timedelta(days=30), key="t_end_2")
            else:
                tc_start = tc_end = None
                
        traffic_cols = [col for col, dt in date_mapping.items() if t_start <= dt <= t_end]
        traffic_dates_str = [date_mapping[d].strftime('%Y-%m-%d') for d in traffic_cols]
        
        traffic_comp_cols = []
        if enable_t_cmp and tc_start and tc_end:
            traffic_comp_cols = [col for col, dt in date_mapping.items() if tc_start <= dt <= tc_end]
        
        fig_traffic = go.Figure()
        if selected_traffic_metrics:
            for metric in selected_traffic_metrics:
                color = traffic_colors[metric]
                search_names = [metric.replace(' ', '').lower()]
                if metric == 'SEO Blog 流量': search_names = ['seoblog流量', 'blog流量']
                if metric == 'SEO 站内流量': search_names = ['seo站内流量', '站内流量']
                if metric == '网站总流量': search_names = ['网站总流量', '总流量']
                if metric == 'SEO流量': search_names = ['seo流量', '流量']

                t_trend1 = get_trend_series(search_names, traffic_cols)
                t_trend2 = get_trend_series(search_names, traffic_comp_cols) if traffic_comp_cols else []
                
                if not t_trend2: 
                    fig_traffic.add_trace(go.Scatter(x=traffic_dates_str, y=t_trend1, mode='lines', name=metric, line=dict(color=color, width=3, shape='spline'), fill='tozeroy', fillcolor=hex_to_rgba(color, 0.1)))
                else: 
                    max_len = max(len(t_trend1), len(t_trend2))
                    x_axis = [f"Day {i+1}" for i in range(max_len)]
                    fig_traffic.add_trace(go.Scatter(x=x_axis[:len(t_trend1)], y=t_trend1, mode='lines', name=f'{metric} (Primary)', line=dict(color=color, width=3, shape='spline')))
                    fig_traffic.add_trace(go.Scatter(x=x_axis[:len(t_trend2)], y=t_trend2, mode='lines', name=f'{metric} (Compare)', line=dict(color=color, width=3, dash='dash', shape='spline')))

        fig_traffic.update_layout(font=font_style, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=10, b=0), height=350, xaxis=dict(showgrid=True, gridcolor='#F0F1F6'), yaxis=dict(showgrid=True, gridcolor='#F0F1F6'))
        st.plotly_chart(fig_traffic, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Raw Table (仅受全局漏斗日期控制)
        st.markdown('<div class="flex-center" style="margin:30px 0 20px 0;"><div class="icon-square bg-gray"><i class="fa-solid fa-table"></i></div><h3 class="text-main" style="margin:0; font-size:22px;">Raw Data Matrix (Callie DE)</h3></div>', unsafe_allow_html=True)
        
        dates1 = [date_mapping[d].strftime('%Y-%m-%d') for d in filtered_cols_1]
        df_display = df_de[['Metric'] + [c for c in filtered_cols_1 if c in df_de.columns]].copy()
        df_display.columns = ['Metric'] + dates1
        df_display = df_display.set_index('Metric')
        
        st.markdown('<div class="soft-card" style="padding: 16px;">', unsafe_allow_html=True)
        st.dataframe(df_display, use_container_width=True, height=450)
        st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.error("Error occurred during rendering:")
    st.write(e)
