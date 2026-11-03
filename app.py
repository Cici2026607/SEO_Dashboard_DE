import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import calendar
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==========================================
# 0. Page Config & Login
# ==========================================
st.set_page_config(page_title="Callie DE - SEO Dashboard", page_icon="🇩🇪", layout="wide")

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

# ==========================================
# CSS 样式精简版
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif !important; color: #2D235C !important; }
    [data-testid="stAppViewContainer"], .stApp { background-color: #F1F5F9 !important; }
    [data-testid="stHeader"] { background-color: transparent !important; }
    .soft-card { background: #ffffff; border: 1px solid #E2E8F0; border-radius: 28px; padding: 30px; box-shadow: 0 10px 25px -5px rgba(15,23,42,0.08); margin-bottom: 24px; transition: 0.3s; }
    .soft-card:hover { transform: translateY(-4px); box-shadow: 0 20px 40px -10px rgba(15,23,42,0.12); }
    .welcome-banner { background: linear-gradient(135deg, #1A1A24 0%, #9B1B30 65%, #D4AF37 100%); border-radius: 28px; padding: 32px 40px; color: white; margin-bottom: 30px; box-shadow: 0 16px 32px -10px rgba(155,27,48,0.4); }
    .welcome-banner h1 { color: white !important; font-size: 36px; font-weight: 800; margin: 0 0 8px 0; display: flex; align-items: center; }
    .progress-track { background-color: #F0F1F6; border-radius: 999px; height: 18px; width: 100%; position: relative; }
    .progress-fill-red { background: linear-gradient(90deg, #FF8491 0%, #FF6475 100%); height: 100%; border-radius: 999px; }
    .progress-fill-blue { background: linear-gradient(90deg, #6BE1F0 0%, #42D2E6 100%); height: 100%; border-radius: 999px; }
    .rocket-icon { position: absolute; right: -12px; top: -6px; font-size: 22px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.15)); }
    .icon-square { display: inline-flex; align-items: center; justify-content: center; width: 48px; height: 48px; border-radius: 16px; margin-right: 16px; font-size: 22px; }
    .icon-small { width: 36px; height: 36px; border-radius: 12px; margin-right: 12px; font-size: 16px; }
    .bg-red { background: #FFF0F2; color: #FF6475; } .bg-blue { background: #E8F9FB; color: #42D2E6; } .bg-purple { background: #F1F0F7; color: #2D235C; } .bg-orange { background: #FFF6E5; color: #FFB000; } .bg-gray { background: #F6F8FA; color: #8E8CA7; }
    .flex-center { display: flex; align-items: center; }
    div[data-testid="stButton"] button { background-color: #ffffff; border: 2px solid #F0F1F6; border-radius: 20px; color: #2D235C; font-weight: 600; padding: 6px 24px; box-shadow: 0 4px 10px rgba(45,35,92,0.03); transition: 0.3s; }
    div[data-testid="stButton"] button:hover { transform: scale(1.03); background-color: #2D235C; border-color: #2D235C; color: #ffffff; }
    .text-main { color: #2D235C !important; } .text-muted { color: #8E8CA7 !important; }
    .funnel-item { flex: 1; border-right: 2px solid #F0F1F6; padding-left: 20px; } .funnel-item:last-child { border-right: none; }
    .funnel-title { color: #8E8CA7; font-size: 13px; font-weight:500; margin: 0 0 8px 0; display: flex; align-items: center; }
    .funnel-dot { font-size: 10px; margin-right: 8px; } .funnel-value { color: #2D235C; font-size: 32px; font-weight: 700; margin: 0; }
    .inner-box { padding: 20px 24px; border-radius: 20px; flex: 1; margin-right: 16px; } .inner-box:last-child { margin-right: 0; }
    .box-deep { background-color: #2D235C; border: none; color: white;} .box-light { background-color: #ffffff; border: 2px solid #F0F1F6; }
    .box-label { font-size: 13px; margin: 0 0 12px 0; display: flex; align-items: center; font-weight:500;}
    .box-value-dark { font-size: 30px; font-weight: 700; color: #2D235C; margin: 0; } .box-value-white { font-size: 30px; font-weight: 700; color: #ffffff; margin: 0; }
    .compare-date-str { font-size: 12px; color: #8E8CA7; font-weight: normal; margin-left: 8px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 核心图表与数据处理工具集 (防截断压缩重构版)
# ==========================================
def hex_to_rgba(hex_color, alpha=0.1):
    hex_color = hex_color.lstrip('#')
    return f"rgba({int(hex_color[0:2],16)}, {int(hex_color[2:4],16)}, {int(hex_color[4:6],16)}, {alpha})"

def clean_val(s):
    if pd.isna(s): return 0
    return pd.to_numeric(str(s).replace(',','').replace('$','').replace('%',''), errors='coerce')

def get_agg_series(df_src, keys, dates, freq='D', agg='sum', is_row_based=True):
    if not dates or df_src.empty: return [], []
    if is_row_based:
        data = pd.DataFrame()
        for k in keys:
            kc = str(k).replace(' ','').lower()
            matched = df_src[df_src['Metric_Norm'].str.contains(kc, na=False)]
            if not matched.empty: data = matched; break
        if data.empty: return [], []
        raw_vals = [clean_val(data[d].iloc[0]) if d in data.columns else 0 for d in dates]
        temp = pd.DataFrame({'date': pd.to_datetime(dates), 'val': raw_vals})
    else:
        c_tgt = ""
        for k in keys:
            kc = str(k).replace(' ','').lower()
            for c in df_src.columns:
                cc = str(c).replace(' ','').lower()
                if kc in cc and ('点击' in cc or '展示' in cc or kc == cc): c_tgt = c; break
            if c_tgt: break
        if not c_tgt: return [], []
        dc = [c for c in df_src.columns if '日' in str(c) or 'date' in str(c).lower()][0]
        mask = df_src[dc].astype(str).isin(dates)
        temp = df_src[mask].copy()
        temp['val'] = temp[c_tgt].apply(clean_val)
        temp['date'] = pd.to_datetime(temp[dc])
        
    temp.set_index('date', inplace=True)
    res = temp.resample('D') if freq=='D' else (temp.resample('W-MON') if freq=='W' else temp.resample('ME'))
    df_agg = res.sum().fillna(0) if agg=='sum' else res.mean().fillna(0)
    out_d = df_agg.index.strftime('%Y-%m').tolist() if freq=='M' else df_agg.index.strftime('%Y-%m-%d').tolist()
    return out_d, df_agg['val'].tolist()

def draw_trend(fig, x, y, name, color, is_cmp=False, fill=False, is_bar=False, sec_y=False, is_dot_line=False):
    if is_bar:
        c = 'rgba(142,140,167,0.3)' if is_cmp else hex_to_rgba(color, 0.65)
        lc = '#8E8CA7' if is_cmp else color
        fig.add_trace(go.Bar(x=x, y=y, name=name, marker=dict(color=c, line=dict(color=lc, width=2))), secondary_y=sec_y)
    else:
        dash = 'dash' if is_cmp else ('dot' if is_dot_line else 'solid')
        sz = 10 if is_cmp else 12
        fc = hex_to_rgba(color, 0.1) if (fill and not is_cmp) else 'rgba(0,0,0,0)'
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name=name, line=dict(color=color, width=2 if is_dot_line else 3, dash=dash, shape='spline'), marker=dict(size=sz, color=color, line=dict(width=2.5, color='white')), fill='tozeroy' if fill and not is_cmp else 'none', fillcolor=fc), secondary_y=sec_y)

def apply_layout(fig, prefix=""):
    fig.update_layout(font=dict(family="Poppins", color="#8E8CA7"), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=10, b=10), height=350, legend=dict(orientation="h", y=1.12, x=0, xanchor="left", itemwidth=50))
    fig.update_xaxes(showgrid=True, gridcolor='#F0F1F6')
    fig.update_yaxes(showgrid=True, gridcolor='#F0F1F6', tickprefix=prefix, secondary_y=False)

# ==========================================
# 2. Data Loaders
# ==========================================
@st.cache_data(ttl=300)
def load_data(url, is_de=False):
    bust = f"{url}&_t={int(datetime.now().timestamp())}"
    df_raw = pd.read_csv(bust, header=None)
    if is_de:
        r_cols = list(df_raw.iloc[21])
        df = df_raw.iloc[23:40].copy()
        c_cols = []
        for i, c in enumerate(r_cols):
            cs = str(c)
            if i==0: c_cols.append("Metric")
            elif pd.isna(c) or cs.lower()=='nan': c_cols.append(f"空_{i}")
            elif cs in c_cols: c_cols.append(f"{cs}_重_{i}")
            else: c_cols.append(cs)
        df.columns = c_cols
        df['Metric'] = df['Metric'].astype(str).str.strip()
        df['Metric_Norm'] = df['Metric'].str.replace(' ','').str.lower()
        return df[[c for c in df.columns if "空_" not in c]].dropna(subset=['Metric'])
    else:
        r0, r1 = df_raw.iloc[0].ffill(), df_raw.iloc[1]
        new_cols = []
        for c, m in zip(r0, r1):
            cs, ms = str(c).strip(), str(m).strip()
            new_cols.append(ms if ('日' in ms or 'date' in ms.lower() or pd.isna(c) or cs=='nan') else f"{cs}_{ms}")
        df = df_raw.iloc[2:].copy()
        df.columns = new_cols
        dc = [c for c in df.columns if '日' in str(c) or 'date' in str(c).lower()][0]
        df[dc] = pd.to_datetime(df[dc], errors='coerce').dt.date
        return df.dropna(subset=[dc]).sort_values(dc), dc

try:
    with st.spinner('🚀 同步 Callie DE 数据...'):
        url_de = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT4KTuYQtC6xsRIwgWLDK9aJUhqmKDmUg4XmMxbsKadyj4QSRM9GNvDjyYz7z8vzKj8nohA7a8ukiLz/pub?gid=0&single=true&output=csv"
        url_gsc = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSdRQFVxjh71cKOiUdcf-j5Ob2GQzc_1WidEtXXx1tdc9Qjz5bWgzJtSEDbMU86i_4ATkmNV8rPITg1/pub?gid=0&single=true&output=csv"
        url_ai = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRdK5Va7wCzGJ3ysGE8H3oeCWjjGEVLZud1Y31ghdO68zLgrOfkfwLnh3VU_lhZttlUziSG4f7ZRTLU/pub?output=csv"
        
        df_de = load_data(url_de, True)
        try: df_gsc, dc_gsc = load_data(url_gsc)
        except: df_gsc, dc_gsc = pd.DataFrame(), None
        try: df_ai, dc_ai = load_data(url_ai)
        except: df_ai, dc_ai = pd.DataFrame(), None

        today = datetime.now().date()
        dt_data = today - timedelta(days=2)
        c_yr, c_mo = dt_data.year, dt_data.month

        st.markdown(f'<div class="welcome-banner"><h1><img src="https://flagcdn.com/w80/de.png" style="height:36px; margin-right:16px; border-radius:4px; box-shadow:0 2px 6px rgba(0,0,0,0.3);">Hallo, Callie DE Team!</h1><p>Germany (DE) SEO Global Dashboard • Data Date: {dt_data.strftime("%Y-%m-%d")} (T-2)</p></div>', unsafe_allow_html=True)
        
        col_b, col_t1, col_t2 = st.columns([1.5, 2, 2])
        with col_b:
            if st.button("🔄 Sync Data"): load_data.clear(); st.rerun()
        with col_t1: target_sales = st.number_input("🎯 DE Sales Target ($)", value=6000.0, step=500.0)
        with col_t2: target_traffic = st.number_input("⚡ DE Traffic Target", value=18000.0, step=1000.0)
                
        d_map = {c: pd.to_datetime(c).date() for c in df_de.columns if c not in ['Metric', 'Metric_Norm']}
        
        mtd_cols = [c for c, d in d_map.items() if d.year==c_yr and d.month==c_mo and d<=dt_data]
        lm_yr, lm_mo = (c_yr, c_mo-1) if c_mo>1 else (c_yr-1, 12)
        lm_d = min(dt_data.day, calendar.monthrange(lm_yr, lm_mo)[1])
        lm_cols = [c for c, d in d_map.items() if date(lm_yr, lm_mo, 1) <= d <= date(lm_yr, lm_mo, lm_d)]
        ly_yr = c_yr - 1
        ly_d = min(dt_data.day, calendar.monthrange(ly_yr, c_mo)[1])
        ly_cols = [c for c, d in d_map.items() if date(ly_yr, c_mo, 1) <= d <= date(ly_yr, c_mo, ly_d)]

        curr_str = f"({c_mo:02d}/01 - {c_mo:02d}/{dt_data.day:02d})"
        lm_str = f"({lm_yr}/{lm_mo:02d}/01 - {lm_mo:02d}/{lm_d:02d})"
        ly_str = f"({ly_yr}/{c_mo:02d}/01 - {c_mo:02d}/{ly_d:02d})"

        def sum_de(keys, cols, curr=False):
            data = pd.DataFrame()
            for k in keys:
                m = df_de[df_de['Metric_Norm'].str.contains(k.replace(' ','').lower(), na=False)]
                if not m.empty: data = m; break
            if data.empty or not cols: return 0.0
            vc = [c for c in cols if c in data.columns]
            if vc: return pd.to_numeric(data[vc].iloc[0].astype(str).str.replace(',','').str.replace('$',''), errors='coerce').fillna(0).sum()
            return 0.0

        m_sls, lm_sls, ly_sls = sum_de(['ga4seo销售额'], mtd_cols, True), sum_de(['ga4seo销售额'], lm_cols, True), sum_de(['ga4seo销售额'], ly_cols, True)
        m_trf, lm_trf, ly_trf = sum_de(['seo流量'], mtd_cols), sum_de(['seo流量'], lm_cols), sum_de(['seo流量'], ly_cols)

        p_sls = min(m_sls/target_sales, 1.0) if target_sales>0 else 0
        p_trf = min(m_trf/target_traffic, 1.0) if target_traffic>0 else 0

        st.markdown('<div class="flex-center" style="margin:20px 0;"><div class="icon-square bg-orange"><i class="fa-solid fa-bullseye"></i></div><h3 class="text-main" style="margin:0; font-size:22px;">Target Achievement (Monat)</h3></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="soft-card"><div style="display:flex; justify-content:space-between; margin-bottom:24px;"><div class="flex-center text-muted" style="font-weight:500;"><i class="fa-solid fa-sack-dollar" style="color:#FF6475; margin-right:8px;"></i> Sales Progress (GA4)</div><div style="color:#FF6475; font-weight:700;">Gap: $ {max(0, target_sales-m_sls):,.2f}</div></div><div style="margin-bottom:28px;"><span class="text-main" style="font-size:38px; font-weight:700;">$ {m_sls:,.2f}</span><span class="text-muted" style="margin-left:8px;">/ $ {target_sales:,.2f}</span></div><div class="progress-track"><div class="progress-fill-red" style="width: {p_sls*100}%;"></div><span class="rocket-icon">🎯</span></div><div style="text-align:right; margin-top:16px;"><span style="color:#FF6475; font-weight:800; font-size:18px;">{p_sls*100:.1f}%</span></div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="soft-card"><div style="display:flex; justify-content:space-between; margin-bottom:24px;"><div class="flex-center text-muted" style="font-weight:500;"><i class="fa-solid fa-users" style="color:#42D2E6; margin-right:8px;"></i> Traffic Progress</div><div style="color:#42D2E6; font-weight:700;">Gap: {max(0, target_traffic-m_trf):,.0f}</div></div><div style="margin-bottom:28px;"><span class="text-main" style="font-size:38px; font-weight:700;">{m_trf:,.0f}</span><span class="text-muted" style="margin-left:8px;">/ {target_traffic:,.0f}</span></div><div class="progress-track"><div class="progress-fill-blue" style="width: {p_trf*100}%;"></div><span class="rocket-icon">⚡</span></div><div style="text-align:right; margin-top:16px;"><span style="color:#42D2E6; font-weight:800; font-size:18px;">{p_trf*100:.1f}%</span></div></div>', unsafe_allow_html=True)

        def t_ui(pct): return ("#FF6475" if pct<0 else "#22C55E", "#FFF0F2" if pct<0 else "#F0FDF4", "↓" if pct<0 else "↑")
        mm_s = ((m_sls-lm_sls)/lm_sls)*100 if lm_sls>0 else 0; yy_s = ((m_sls-ly_sls)/ly_sls)*100 if ly_sls>0 else 0
        mm_t = ((m_trf-lm_trf)/lm_trf)*100 if lm_trf>0 else 0; yy_t = ((m_trf-ly_trf)/ly_trf)*100 if ly_trf>0 else 0
        
        st.markdown('<div class="flex-center" style="margin:30px 0 20px 0;"><div class="icon-square bg-purple"><i class="fa-solid fa-chart-simple"></i></div><h3 class="text-main" style="margin:0; font-size:22px;">MTD Monitoring</h3></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="soft-card" style="display:flex; justify-content:space-between; padding-bottom:30px;"><div style="flex:1;"><p class="text-muted" style="margin-bottom:8px;">Sales MTD <span class="compare-date-str">{curr_str}</span></p><h2 class="text-main" style="margin:0; font-size:32px;">$ {m_sls:,.2f}</h2></div><div style="flex:1; border-left:2px solid #F0F1F6; padding-left:30px;"><p class="text-muted" style="margin-bottom:8px;">Last Month <span class="compare-date-str">{lm_str}</span></p><h2 class="text-main" style="margin:0; font-size:26px; margin-bottom:12px;">$ {lm_sls:,.2f}</h2><span style="color:{t_ui(mm_s)[0]}; background:{t_ui(mm_s)[1]}; padding:4px 12px; border-radius:8px; font-weight:600; font-size:13px;">{t_ui(mm_s)[2]} {abs(mm_s):.1f}% MoM</span></div><div style="flex:1; border-left:2px solid #F0F1F6; padding-left:30px;"><p class="text-muted" style="margin-bottom:8px;">Last Year <span class="compare-date-str">{ly_str}</span></p><h2 class="text-main" style="margin:0; font-size:26px; margin-bottom:12px;">$ {ly_sls:,.2f}</h2><span style="color:{t_ui(yy_s)[0]}; background:{t_ui(yy_s)[1]}; padding:4px 12px; border-radius:8px; font-weight:600; font-size:13px;">{t_ui(yy_s)[2]} {abs(yy_s):.1f}% YoY</span></div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="soft-card" style="display:flex; justify-content:space-between; padding-bottom:30px;"><div style="flex:1;"><p class="text-muted" style="margin-bottom:8px;">Traffic MTD <span class="compare-date-str">{curr_str}</span></p><h2 class="text-main" style="margin:0; font-size:32px;">{m_trf:,.0f}</h2></div><div style="flex:1; border-left:2px solid #F0F1F6; padding-left:30px;"><p class="text-muted" style="margin-bottom:8px;">Last Month <span class="compare-date-str">{lm_str}</span></p><h2 class="text-main" style="margin:0; font-size:26px; margin-bottom:12px;">{lm_trf:,.0f}</h2><span style="color:{t_ui(mm_t)[0]}; background:{t_ui(mm_t)[1]}; padding:4px 12px; border-radius:8px; font-weight:600; font-size:13px;">{t_ui(mm_t)[2]} {abs(mm_t):.1f}% MoM</span></div><div style="flex:1; border-left:2px solid #F0F1F6; padding-left:30px;"><p class="text-muted" style="margin-bottom:8px;">Last Year <span class="compare-date-str">{ly_str}</span></p><h2 class="text-main" style="margin:0; font-size:26px; margin-bottom:12px;">{ly_trf:,.0f}</h2><span style="color:{t_ui(yy_t)[0]}; background:{t_ui(yy_t)[1]}; padding:4px 12px; border-radius:8px; font-weight:600; font-size:13px;">{t_ui(yy_t)[2]} {abs(yy_t):.1f}% YoY</span></div></div>', unsafe_allow_html=True)

        def g_gsc(sd, ed, key):
            if df_gsc is None or df_gsc.empty: return 0.0
            tgt = ""
            for c in df_gsc.columns:
                if key.lower() in str(c).lower() and '点击' in str(c).lower(): tgt=c; break
            if not tgt: return 0.0
            return df_gsc[(df_gsc[dc_gsc]>=sd) & (df_gsc[dc_gsc]<=ed)][tgt].apply(clean_val).sum()
        
        m_g, lm_g, ly_g = g_gsc(date(c_yr, c_mo, 1), dt_data, '点击（gsc）'), g_gsc(date(lm_yr, lm_mo, 1), date(lm_yr, lm_mo, lm_d), '点击（gsc）'), g_gsc(date(ly_yr, c_mo, 1), date(ly_yr, c_mo, ly_d), '点击（gsc）')
        mm_g = ((m_g-lm_g)/lm_g)*100 if lm_g>0 else 0; yy_g = ((m_g-ly_g)/ly_g)*100 if ly_g>0 else 0
        st.markdown(f'<div class="soft-card" style="display:flex; justify-content:space-between; padding-bottom:30px;"><div style="flex:1;"><p class="text-muted" style="margin-bottom:8px;">GSC Clicks MTD <span class="compare-date-str">{curr_str}</span></p><h2 class="text-main" style="margin:0; font-size:32px;">{m_g:,.0f}</h2></div><div style="flex:1; border-left:2px solid #F0F1F6; padding-left:30px;"><p class="text-muted" style="margin-bottom:8px;">Last Month <span class="compare-date-str">{lm_str}</span></p><h2 class="text-main" style="margin:0; font-size:26px; margin-bottom:12px;">{lm_g:,.0f}</h2><span style="color:{t_ui(mm_g)[0]}; background:{t_ui(mm_g)[1]}; padding:4px 12px; border-radius:8px; font-weight:600; font-size:13px;">{t_ui(mm_g)[2]} {abs(mm_g):.1f}% MoM</span></div><div style="flex:1; border-left:2px solid #F0F1F6; padding-left:30px;"><p class="text-muted" style="margin-bottom:8px;">Last Year <span class="compare-date-str">{ly_str}</span></p><h2 class="text-main" style="margin:0; font-size:26px; margin-bottom:12px;">{ly_g:,.0f}</h2><span style="color:{t_ui(yy_g)[0]}; background:{t_ui(yy_g)[1]}; padding:4px 12px; border-radius:8px; font-weight:600; font-size:13px;">{t_ui(yy_g)[2]} {abs(yy_g):.1f}% YoY</span></div></div>', unsafe_allow_html=True)
        st.markdown('<br><hr style="border:1px solid #E2E8F0; margin: 20px 0;"><br>', unsafe_allow_html=True)

        # ==========================================
        # ⭐ Annual Trends (YoY Overview) 无需筛选时间
        # ==========================================
        st.markdown('<div class="flex-center" style="margin-bottom:6px;"><div class="icon-square bg-blue"><i class="fa-solid fa-chart-line"></i></div><h3 class="text-main" style="margin:0; font-size:22px;">Annual Trends (YoY Overview)</h3></div>', unsafe_allow_html=True)
        st.caption("Auto-aggregated monthly trends comparing 2026 vs 2025 across all available data.")
        
        def get_yoy_data(key, y, is_gsc=False):
            res = {str(m):0.0 for m in range(1,13)}
            if is_gsc:
                if df_gsc is None or df_gsc.empty: return []
                c_tgt = ""
                for c in df_gsc.columns:
                    if key.replace(' ','').lower() in str(c).replace(' ','').lower() and '点击' in str(c).lower(): c_tgt=c; break
                if not c_tgt: return []
                df_t = df_gsc[pd.to_datetime(df_gsc[dc_gsc]).dt.year == y].copy()
                if df_t.empty: return []
                ms = df_t.groupby(pd.to_datetime(df_t[dc_gsc]).dt.month)[c_tgt].apply(lambda x: x.apply(clean_val).sum()).to_dict()
                for m,v in ms.items(): res[str(m)] = v
            else:
                data = df_de[df_de['Metric_Norm'].str.contains(key.replace(' ','').lower(), na=False)]
                if data.empty: return []
                for c in data.columns:
                    try:
                        dt = pd.to_datetime(c)
                        if dt.year == y: res[str(dt.month)] += clean_val(data[c].iloc[0])
                    except: pass
            vals = [res[str(m)] for m in range(1,13)]
            if sum(vals)==0: return []
            last_m = 12
            for i in range(11,-1,-1):
                if vals[i]!=0: last_m=i+1; break
            if y == c_yr: last_m = min(last_m, c_mo)
            return vals[:last_m]

        col_y1, col_y2 = st.columns(2)
        mlbs = [f"{m}月" for m in range(1,13)]
        layout_yoy = dict(font=dict(family="Poppins", color="#8E8CA7"), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=10, b=10), height=250, legend=dict(orientation="h", y=1.15, x=0.5, xanchor="center", itemwidth=50))
        
        with col_y1:
            st.markdown('<div class="soft-card" style="padding:16px 24px; margin-bottom:16px; border-radius:16px;"><div class="flex-center"><div class="icon-small bg-gray flex-center" style="margin-bottom:0;"><i class="fa-solid fa-chart-line"></i></div><span class="text-main" style="font-weight:700;">SEO 点击数据对比 (GSC 2026 vs 2025 YoY)</span></div></div>', unsafe_allow_html=True)
            y_tbs = st.tabs(['站内点击走势 (非品牌词非Blog非utm)', '全站 GSC 大盘总点击走势', 'Blog 点击走势'])
            y_ks = ['点击（非品牌词非Blog非utm）', '点击（GSC）', '点击（Blog）']
            for i, tb in enumerate(y_tbs):
                with tb:
                    v25, v26 = get_yoy_data(y_ks[i], 2025, True), get_yoy_data(y_ks[i], 2026, True)
                    fy = go.Figure()
                    if v25: fy.add_trace(go.Scatter(x=mlbs[:len(v25)], y=v25, mode='lines+markers', name='2025年', line=dict(color='#F59E0B', width=3, shape='spline'), marker=dict(size=10, color='#F59E0B', line=dict(width=2, color='white'))))
                    if v26: fy.add_trace(go.Scatter(x=mlbs[:len(v26)], y=v26, mode='lines+markers', name='2026年', line=dict(color='#3B82F6', width=3, shape='spline'), marker=dict(size=10, color='#3B82F6', line=dict(width=2, color='white')), fill='tozeroy', fillcolor=hex_to_rgba('#3B82F6', 0.1)))
                    fy.update_layout(**layout_yoy); fy.update_xaxes(showgrid=True, gridcolor='#F0F1F6'); fy.update_yaxes(showgrid=True, gridcolor='#F0F1F6')
                    st.plotly_chart(fy, use_container_width=True)
        with col_y2:
            st.markdown('<div class="soft-card" style="padding:16px 24px; margin-bottom:16px; border-radius:16px;"><div class="flex-center"><div class="icon-small bg-gray flex-center" style="margin-bottom:0;"><i class="fa-solid fa-robot"></i></div><span class="text-main" style="font-weight:700;">AI Assistant 年度对比 (2026 vs 2025 YoY)</span></div></div>', unsafe_allow_html=True)
            a_tbs = st.tabs(['AI 贡献销售额月度同比', 'AI 来源流量月度同比'])
            with a_tbs[0]:
                v25, v26 = get_yoy_data('aiassistant销售额', 2025), get_yoy_data('aiassistant销售额', 2026)
                fa1 = go.Figure()
                if v25: fa1.add_trace(go.Scatter(x=mlbs[:len(v25)], y=v25, mode='lines+markers', name='2025年', line=dict(color='#F59E0B', width=3, shape='spline'), marker=dict(size=10, color='#F59E0B', line=dict(width=2, color='white'))))
                if v26: fa1.add_trace(go.Scatter(x=mlbs[:len(v26)], y=v26, mode='lines+markers', name='2026年', line=dict(color='#3B82F6', width=3, shape='spline'), marker=dict(size=10, color='#3B82F6', line=dict(width=2, color='white')), fill='tozeroy', fillcolor=hex_to_rgba('#3B82F6', 0.1)))
                fa1.update_layout(**layout_yoy); fa1.update_xaxes(showgrid=True, gridcolor='#F0F1F6'); fa1.update_yaxes(showgrid=True, gridcolor='#F0F1F6', tickprefix="$")
                st.plotly_chart(fa1, use_container_width=True)
            with a_tbs[1]:
                v25, v26 = get_yoy_data('aiassistant流量', 2025), get_yoy_data('aiassistant流量', 2026)
                fa2 = go.Figure()
                if v25: fa2.add_trace(go.Scatter(x=mlbs[:len(v25)], y=v25, mode='lines+markers', name='2025年', line=dict(color='#F59E0B', width=3, shape='spline'), marker=dict(size=10, color='#F59E0B', line=dict(width=2, color='white'))))
                if v26: fa2.add_trace(go.Scatter(x=mlbs[:len(v26)], y=v26, mode='lines+markers', name='2026年', line=dict(color='#3B82F6', width=3, shape='spline'), marker=dict(size=10, color='#3B82F6', line=dict(width=2, color='white')), fill='tozeroy', fillcolor=hex_to_rgba('#3B82F6', 0.1)))
                fa2.update_layout(**layout_yoy); fa2.update_xaxes(showgrid=True, gridcolor='#F0F1F6'); fa2.update_yaxes(showgrid=True, gridcolor='#F0F1F6')
                st.plotly_chart(fa2, use_container_width=True)

        st.markdown('<br><hr style="border:1px solid #E2E8F0; margin: 20px 0;"><br>', unsafe_allow_html=True)

        # ==========================================
        # 4. 全局漏斗分析区间 (全局时间中控)
        # ==========================================
        v_dates = list(d_map.values())
        mn_d, mx_d = min(v_dates) if v_dates else date.today(), max(v_dates) if v_dates else date.today()

        hc1, hc2, hc3, hc4 = st.columns([1.5, 1, 1, 1.2])
        with hc1:
            st.markdown('<div class="flex-center" style="margin-bottom:6px;"><div class="icon-square bg-blue"><i class="fa-regular fa-calendar"></i></div><h3 class="text-main" style="margin:0; font-size:22px;">Interval Analysis</h3></div>', unsafe_allow_html=True)
            st.caption("Modules below are strictly bounded by your date selection.")
        with hc2: d1 = st.date_input("🗓️ Primary Date Range", [mn_d, mx_d])
        with hc3:
            en_cmp = st.checkbox("🔄 Enable Trend Comparison")
            d2 = st.date_input("🗓️ Compare Date Range", [mn_d - timedelta(days=30), mx_d - timedelta(days=30)]) if en_cmp else []
        with hc4:
            st.markdown('<div style="margin-top:2px;"></div>', unsafe_allow_html=True)
            freq = {"日 (Daily)": "D", "周 (Weekly)": "W", "月 (Monthly)": "M"}[st.radio("📊 Trend Aggregation", ["日 (Daily)", "周 (Weekly)", "月 (Monthly)"], horizontal=True)]

        sd1, ed1 = d1 if len(d1)==2 else (d1[0], d1[0])
        sd2, ed2 = d2 if len(d2)==2 else (d2[0], d2[0]) if en_cmp and d2 else (None, None)
        
        fc1 = [c for c, d in d_map.items() if sd1 <= d <= ed1]
        fc2 = [c for c, d in d_map.items() if sd2 and sd2 <= d <= ed2] if en_cmp else []
        
        d_g1 = [str(d) for d in pd.date_range(sd1, ed1)]
        d_g2 = [str(d) for d in pd.date_range(sd2, ed2)] if en_cmp and sd2 else []

        def f_cmp(v1, v2, is_curr=False, is_pct=False, inv=False, dark=False):
            if not en_cmp: return ""
            pct = 0 if v2==0 and v1==0 else (999999 if v2==0 else (v1-v2)/v2*100)
            v2s = f"$ {v2:,.2f}" if is_curr else (f"{v2:.2f}%" if is_pct else f"{v2:,.0f}")
            c = "#8E8CA7" if pct==0 else ("#22C55E" if (pct>0 and not inv) or (pct<0 and inv) else "#FF6475")
            arr, p_str = ("","0.0%") if pct==0 else (("↑" if pct>0 else "↓"), "+∞%" if pct==999999 else f"{abs(pct):.1f}%")
            return f"<div style='font-size:13px; color:{'rgba(255,255,255,0.7)' if dark else '#8E8CA7'}; margin-top:4px;'>vs {v2s} <span style='color:{c}; font-weight:700;'>{arr} {p_str}</span></div>"

        # KPI 卡片
        i_trf, c_trf = sum_de(['seo流量'], fc1), sum_de(['seo流量'], fc2)
        i_blg, c_blg = sum_de(['seoblog流量'], fc1), sum_de(['seoblog流量'], fc2)
        i_ins, c_ins = sum_de(['seo站内流量'], fc1), sum_de(['seo站内流量'], fc2)
        i_sit, c_sit = sum_de(['网站总流量'], fc1), sum_de(['网站总流量'], fc2)
        i_ga4, c_ga4 = sum_de(['ga4seo销售额'], fc1, True), sum_de(['ga4seo销售额'], fc2, True)
        i_sup, c_sup = sum_de(['supersetseo销售额'], fc1, True), sum_de(['supersetseo销售额'], fc2, True)
        i_ais, c_ais = sum_de(['aiassistant销售额'], fc1, True), sum_de(['aiassistant销售额'], fc2, True)
        i_ait, c_ait = sum_de(['aiassistant流量'], fc1), sum_de(['aiassistant流量'], fc2)
        
        br = df_de[df_de['Metric_Norm'].str.contains('跳出率', na=False)]
        i_br = pd.to_numeric(br[[c for c in fc1 if c in br.columns]].iloc[0].astype(str).str.replace('%',''), errors='coerce').mean() if not br.empty and fc1 else 0.0
        c_br = pd.to_numeric(br[[c for c in fc2 if c in br.columns]].iloc[0].astype(str).str.replace('%',''), errors='coerce').mean() if not br.empty and fc2 else 0.0

        st.markdown(f"""
<div class="soft-card"><h4 class="text-main" style="margin: 0 0 24px 0; display: flex; align-items: center;"><div class="icon-small bg-blue flex-center" style="justify-content:center;"><i class="fa-solid fa-filter"></i></div> Traffic Funnel Health</h4><div style="display: flex; justify-content: space-between; border-bottom: 2px dashed #F0F1F6; padding-bottom: 24px;">
<div class="funnel-item" style="padding-left: 0;"><p class="funnel-title"><i class="fa-solid fa-circle funnel-dot" style="color:#2D235C;"></i> SEO 流量</p><p class="funnel-value">{i_trf:,.0f}</p>{f_cmp(i_trf, c_trf)}</div>
<div class="funnel-item"><p class="funnel-title"><i class="fa-solid fa-circle funnel-dot" style="color:#42D2E6;"></i> SEO Blog 流量</p><p class="funnel-value">{i_blg:,.0f}</p>{f_cmp(i_blg, c_blg)}</div>
<div class="funnel-item"><p class="funnel-title"><i class="fa-solid fa-circle funnel-dot" style="color:#FF6475;"></i> SEO 站内流量</p><p class="funnel-value">{i_ins:,.0f}</p>{f_cmp(i_ins, c_ins)}</div>
<div class="funnel-item"><p class="funnel-title"><i class="fa-solid fa-circle funnel-dot" style="color:#FFB000;"></i> 网站总流量</p><p class="funnel-value">{i_sit:,.0f}</p>{f_cmp(i_sit, c_sit)}</div>
<div class="funnel-item"><p class="funnel-title"><i class="fa-solid fa-circle funnel-dot" style="color:#8E8CA7;"></i> 跳出率</p><p class="funnel-value">{i_br:.2f}%</p>{f_cmp(i_br, c_br, False, True, True)}</div>
</div></div>
<div class="soft-card"><h4 class="text-main" style="margin: 0 0 24px 0; display: flex; align-items: center;"><div class="icon-small bg-red flex-center" style="justify-content:center;"><i class="fa-solid fa-sack-dollar"></i></div> Sales Breakdown</h4><div style="display: flex; gap: 20px;">
<div class="inner-box box-deep" style="text-align: center;"><p class="box-label" style="justify-content: center; color:rgba(255,255,255,0.9);"><i class="fa-solid fa-circle" style="color:#FF6475; font-size:8px; margin-right:8px;"></i> GA4 SEO Sales</p><p class="box-value-white">$ {i_ga4:,.2f}</p>{f_cmp(i_ga4, c_ga4, True, False, False, True)}</div>
<div class="inner-box box-light" style="text-align: center;"><p class="box-label text-muted" style="justify-content: center;"><i class="fa-solid fa-circle" style="color:#FFB000; font-size:8px; margin-right:8px;"></i> Superset SEO Sales</p><p class="box-value-dark">$ {i_sup:,.2f}</p>{f_cmp(i_sup, c_sup, True)}</div>
</div></div>
""", unsafe_allow_html=True)
        
        ca, cg = st.columns(2)
        with ca:
            st.markdown(f'<div class="soft-card" style="height: 100%;"><p style="margin-bottom:12px; font-weight:700;"><span class="icon-small bg-purple flex-center" style="display:inline-flex; justify-content:center; margin-bottom:-4px;"><i class="fa-solid fa-robot"></i></span> AI Assistant</p><div style="display: flex; margin-top:16px;"><div class="inner-box box-deep"><p class="box-label" style="color:rgba(255,255,255,0.8);"><i class="fa-solid fa-circle" style="color:#FFB000; font-size:8px; margin-right:8px;"></i> AI Sales</p><p class="box-value-white">$ {i_ais:,.2f}</p>{f_cmp(i_ais, c_ais, True, False, False, True)}</div><div class="inner-box box-light"><p class="box-label text-muted"><i class="fa-solid fa-circle" style="color:#2D235C; font-size:8px; margin-right:8px;"></i> AI Traffic</p><p class="box-value-dark">{i_ait:,.0f}</p>{f_cmp(i_ait, c_ait)}</div></div></div>', unsafe_allow_html=True)
        with cg:
            st.markdown(f'<div class="soft-card" style="height: 100%;"><p style="margin-bottom:12px; font-weight:700;"><span class="icon-small bg-orange flex-center" style="display:inline-flex; justify-content:center; margin-bottom:-4px;"><i class="fa-brands fa-google"></i></span> Google Assets</p><div style="display: flex; margin-top:16px;"><div class="inner-box box-light"><p class="box-label text-muted"><i class="fa-solid fa-circle" style="color:#FFB000; font-size:8px; margin-right:8px;"></i> Indexing</p><p class="box-value-dark">-</p></div><div class="inner-box box-light"><p class="box-label text-muted"><i class="fa-solid fa-circle" style="color:#FF6475; font-size:8px; margin-right:8px;"></i> Backlinks</p><p class="box-value-dark">-</p></div><div class="inner-box box-light"><p class="box-label text-muted"><i class="fa-solid fa-circle" style="color:#42D2E6; font-size:8px; margin-right:8px;"></i> Domains</p><p class="box-value-dark">-</p></div></div></div>', unsafe_allow_html=True)

        # 图表模块
        st.markdown('<div class="soft-card" style="padding: 16px 24px; margin-bottom: 16px; border-radius: 16px;"><div class="flex-center"><div class="icon-small bg-red flex-center" style="justify-content:center; margin-bottom: 0;"><i class="fa-solid fa-chart-area"></i></div><span class="text-main" style="font-weight:700; font-size:16px;">Sales Trend Breakdown</span></div></div>', unsafe_allow_html=True)
        ss = st.multiselect("Sales", ['GA4 SEO销售额', 'Superset SEO销售额', 'AI Assistant 销售额'], default=['GA4 SEO销售额'], label_visibility="collapsed")
        fs = go.Figure()
        sc = {'GA4 SEO销售额': '#FF6475', 'Superset SEO销售额': '#FFB000', 'AI Assistant 销售额': '#8B5CF6'}
        for m in ss:
            k = 'ga4seo销售额' if m == 'GA4 SEO销售额' else ('aiassistant销售额' if m == 'AI Assistant 销售额' else 'supersetseo销售额')
            d1_a, v1 = get_agg_series(df_de, [k], fc1, freq)
            draw_trend(fs, d1_a, v1, f"{m} (Pri)" if en_cmp else m, sc[m], False, True)
            if en_cmp:
                d2_a, v2 = get_agg_series(df_de, [k], fc2, freq)
                draw_trend(fs, [f"P {j+1}" for j in range(max(len(v1), len(v2)))] if freq=='D' else d2_a, v2, f"{m} (Cmp)", sc[m], True)
        apply_layout(fs, "$"); st.plotly_chart(fs, use_container_width=True)
        
        st.markdown('<div class="soft-card" style="padding: 16px 24px; margin-bottom: 16px; margin-top: 20px; border-radius: 16px;"><div class="flex-center"><div class="icon-small bg-blue flex-center" style="justify-content:center; margin-bottom: 0;"><i class="fa-solid fa-chart-line"></i></div><span class="text-main" style="font-weight:700; font-size:16px;">Traffic Breakdown</span></div></div>', unsafe_allow_html=True)
        stt = st.multiselect("Traffic", ['SEO流量', 'SEO Blog 流量', 'SEO 站内流量', '网站总流量', 'AI Assistant 流量'], default=['SEO流量'], label_visibility="collapsed")
        ft = go.Figure()
        tc = {'SEO流量': '#2D235C', 'SEO Blog 流量': '#42D2E6', 'SEO 站内流量': '#FF6475', '网站总流量': '#FFB000', 'AI Assistant 流量': '#8B5CF6'}
        for m in stt:
            k = 'seoblog流量' if m == 'SEO Blog 流量' else ('seo站内流量' if m == 'SEO 站内流量' else m.replace(' ', '').lower())
            d1_a, v1 = get_agg_series(df_de, [k], fc1, freq)
            draw_trend(ft, d1_a, v1, f"{m} (Pri)" if en_cmp else m, tc[m], False, True)
            if en_cmp:
                d2_a, v2 = get_agg_series(df_de, [k], fc2, freq)
                draw_trend(ft, [f"P {j+1}" for j in range(max(len(v1), len(v2)))] if freq=='D' else d2_a, v2, f"{m} (Cmp)", tc[m], True)
        apply_layout(ft); st.plotly_chart(ft, use_container_width=True)

        # GSC & AI Cards
        if date_col_gsc and not df_gsc.empty:
            gsc_metrics = ['点击（GSC）', '点击（非品牌词点击）', '点击（Blog）', '点击（非Blog）', '点击（非品牌词非Blog）', '点击（非品牌词非Blog非utm）']
            gsc_c = ['#FF6475', '#42D2E6', '#FFB000', '#8B5CF6', '#2D235C', '#10B981']
            
            html = '<div class="soft-card"><h4 class="text-main" style="margin: 0 0 24px 0; display: flex; align-items: center;"><div class="icon-small bg-orange flex-center" style="justify-content:center;"><i class="fa-brands fa-google"></i></div> GSC Clicks Breakdown (Selected Interval)</h4><div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;">'
            for idx, m in enumerate(gsc_metrics):
                _, v1 = get_agg_series(df_gsc, [m], d_g1, 'M', is_row_based=False)
                _, v2 = get_agg_series(df_gsc, [m], d_g2, 'M', is_row_based=False) if en_cmp else ([], [0])
                s1, s2 = sum(v1) if v1 else 0, sum(v2) if v2 else 0
                html += f'<div class="inner-box box-light"><p class="box-label text-muted"><i class="fa-solid fa-circle" style="color:{gsc_c[idx]}; font-size:8px; margin-right:8px;"></i> {m}</p><p class="box-value-dark">{s1:,.0f}</p>{f_cmp(s1, s2)}</div>'
            st.markdown(html + '</div></div>', unsafe_allow_html=True)
            
            sm = st.multiselect("GSC Trends", gsc_metrics, default=['点击（GSC）'], label_visibility="collapsed")
            fg = go.Figure()
            for m in sm:
                idx = gsc_metrics.index(m)
                d1_a, v1 = get_agg_series(df_gsc, [m], d_g1, freq, is_row_based=False)
                draw_trend(fg, d1_a, v1, f"{m} (Pri)" if en_cmp else m, gsc_c[idx], False, True)
                if en_cmp:
                    d2_a, v2 = get_agg_series(df_gsc, [m], d_g2, freq, is_row_based=False)
                    draw_trend(fg, [f"P {j+1}" for j in range(max(len(v1), len(v2)))] if freq=='D' else d2_a, v2, f"{m} (Cmp)", gsc_c[idx], True)
            apply_layout(fg); st.plotly_chart(fg, use_container_width=True)

            g_tabs = st.tabs(gsc_metrics)
            for i, tb in enumerate(g_tabs):
                with tb:
                    m = gsc_metrics[i]
                    f1 = make_subplots(specs=[[{"secondary_y": True}]])
                    d1_a, v1_c = get_agg_series(df_gsc, [f"{m}_点击"], d_g1, freq, is_row_based=False)
                    _, v1_i = get_agg_series(df_gsc, [f"{m}_展示"], d_g1, freq, is_row_based=False)
                    draw_trend(f1, d1_a, v1_c, "点击次数 (Pri)" if en_cmp else "点击次数", '#42D2E6', False, False, True)
                    draw_trend(f1, d1_a, v1_i, "展示 (Pri)" if en_cmp else "展示", '#FF6475', False, False, False, True)
                    if en_cmp:
                        d2_a, v2_c = get_agg_series(df_gsc, [f"{m}_点击"], d_g2, freq, is_row_based=False)
                        _, v2_i = get_agg_series(df_gsc, [f"{m}_展示"], d_g2, freq, is_row_based=False)
                        xa = [f"P {j+1}" for j in range(max(len(v1_c), len(v2_c)))] if freq=='D' else d2_a
                        draw_trend(f1, xa, v2_c, "点击次数 (Cmp)", '#8E8CA7', True, False, True)
                        draw_trend(f1, xa, v2_i, "展示 (Cmp)", 'rgba(255,100,117,0.5)', True, False, False, True)
                    apply_layout(f1); st.plotly_chart(f1, use_container_width=True)

                    f2 = make_subplots(specs=[[{"secondary_y": True}]])
                    d1_a, v1_ct = get_agg_series(df_gsc, [f"{m}_点击率"], d_g1, freq, 'mean', False)
                    _, v1_po = get_agg_series(df_gsc, [f"{m}_排名"], d_g1, freq, 'mean', False)
                    draw_trend(f2, d1_a, v1_ct, "点击率 (%) (Pri)" if en_cmp else "点击率 (%)", '#22C55E')
                    draw_trend(f2, d1_a, v1_po, "排名 (Pri)" if en_cmp else "排名", '#8B5CF6', False, False, False, True, True)
                    if en_cmp:
                        d2_a, v2_ct = get_agg_series(df_gsc, [f"{m}_点击率"], d_g2, freq, 'mean', False)
                        _, v2_po = get_agg_series(df_gsc, [f"{m}_排名"], d_g2, freq, 'mean', False)
                        xa = [f"P {j+1}" for j in range(max(len(v1_ct), len(v2_ct)))] if freq=='D' else d2_a
                        draw_trend(f2, xa, v2_ct, "点击率 (Cmp)", 'rgba(34,197,94,0.5)', True)
                        draw_trend(f2, xa, v2_po, "排名 (Cmp)", 'rgba(139,92,246,0.5)', True, False, False, True, True)
                    apply_layout(f2); f2.update_yaxes(autorange="reversed", secondary_y=True); st.plotly_chart(f2, use_container_width=True)

        if date_col_ai and not df_ai.empty:
            ai_c = [("AI Performance（GSC）", ['aiperformance(gsc)'], '#8B5CF6'), ("AI Performance（非Blog）", ['aiperformance(非blog)'], '#42D2E6'), ("AI Performance（Blog）", ['aiperformance(blog)'], '#FF6475')]
            h_ai = '<div class="soft-card"><h4 class="text-main" style="margin: 0 0 24px 0; display: flex; align-items: center;"><div class="icon-small bg-purple flex-center" style="justify-content:center;"><i class="fa-solid fa-microchip"></i></div> AI Performance Breakdown (Selected Interval)</h4><div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;">'
            for nm, k, cx in ai_c:
                _, v1 = get_agg_series(df_ai, k, d_g1, 'M', is_row_based=False)
                _, v2 = get_agg_series(df_ai, k, d_g2, 'M', is_row_based=False) if en_cmp else ([], [0])
                s1, s2 = sum(v1) if v1 else 0, sum(v2) if v2 else 0
                h_ai += f'<div class="inner-box box-light"><p class="box-label text-muted"><i class="fa-solid fa-circle" style="color:{cx}; font-size:8px; margin-right:8px;"></i> {nm}</p><p class="box-value-dark">{s1:,.0f}</p>{f_cmp(s1, s2)}</div>'
            st.markdown(h_ai + '</div></div>', unsafe_allow_html=True)
            
            sai = st.multiselect("AI Trends", [c for c in df_ai.columns if c!=date_col_ai], default=[df_ai.columns[1]], label_visibility="collapsed")
            fai = go.Figure()
            cols = ['#8B5CF6', '#42D2E6', '#FF6475', '#FFB000', '#22C55E']
            for idx, m in enumerate(sai):
                cc = cols[idx%len(cols)]
                d1_a, v1 = get_agg_series(df_ai, [m], d_g1, freq, is_row_based=False)
                draw_trend(fai, d1_a, v1, f"{m} (Pri)" if en_cmp else m, cc, False, True)
                if en_cmp:
                    d2_a, v2 = get_agg_series(df_ai, [m], d_g2, freq, is_row_based=False)
                    draw_trend(fai, [f"P {j+1}" for j in range(max(len(v1), len(v2)))] if freq=='D' else d2_a, v2, f"{m} (Cmp)", cc, True)
            apply_layout(fai); st.plotly_chart(fai, use_container_width=True)
            
except Exception as e:
    st.error("Error occurred during rendering:")
    st.write(e)
