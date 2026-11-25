@st.cache_data(ttl=300)
def load_and_clean_data():
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT4KTuYQtC6xsRIwgWLDK9aJUhqmKDmUg4XmMxbsKadyj4QSRM9GNvDjyYz7z8vzKj8nohA7a8ukiLz/pub?gid=0&single=true&output=csv"
    bust_url = f"{csv_url}&_t={int(datetime.now().timestamp())}"
    
    df_raw = pd.read_csv(bust_url, header=None)
    
    # 1. 动态在 A 列定位 Callie DE 区块起始行（不再写死 iloc[21]）
    col0 = df_raw.iloc[:, 0].astype(str).str.strip()
    col0_norm = col0.str.replace(' ', '', regex=False).str.lower()
    de_matches = col0_norm[col0_norm.str.contains('calliede', na=False) | (col0_norm == 'de')].index.tolist()
    if not de_matches:
        st.warning("⚠️ 在总表 A 列中未找到 'Callie DE' 标题行，请检查表格是否取消发布或改名。")
        return pd.DataFrame(columns=['Metric', 'Metric_Norm'])
    start_idx = de_matches[0]

    # 2. 自动判断哪一行是日期行（先查 Callie DE 当前行，再查下一行，最后兜底用第 1 行）
    def count_valid_dates(row_vals):
        cnt = 0
        for v in row_vals[1:]:
            if pd.isna(v):
                continue
            s = str(v).strip()
            if not s or s.lower() == 'nan' or s.isdigit():
                continue
            try:
                dt = pd.to_datetime(s, errors='raise')
                if 2020 <= dt.year <= 2035:
                    cnt += 1
            except Exception:
                pass
        return cnt

    if count_valid_dates(df_raw.iloc[start_idx]) >= 3:
        header_idx = start_idx
        data_start = start_idx + 1
    elif start_idx + 1 < len(df_raw) and count_valid_dates(df_raw.iloc[start_idx + 1]) >= 3:
        header_idx = start_idx + 1
        data_start = start_idx + 2
    else:
        header_idx = 0
        data_start = start_idx + 1

    # 3. 动态找到下一个站点（如 Callie ES / Callie IT）作为结束行
    end_idx = len(df_raw)
    for r in range(data_start, len(df_raw)):
        val_norm = col0_norm.iloc[r]
        if val_norm.startswith('callie') and 'calliede' not in val_norm:
            end_idx = r
            break

    raw_columns = list(df_raw.iloc[header_idx])
    df_de = df_raw.iloc[data_start:end_idx].copy()
    
    clean_columns = []
    for i, col in enumerate(raw_columns):
        if i == 0:
            clean_columns.append("Metric")
        else:
            col_str = str(col).strip()
            if pd.isna(col) or col_str == '' or col_str.lower() == 'nan':
                clean_columns.append(f"空列_{i}")
            elif col_str in clean_columns:
                clean_columns.append(f"{col_str}_重复_{i}")
            else:
                clean_columns.append(col_str)
                
    df_de.columns = clean_columns
    df_de.reset_index(drop=True, inplace=True)
    df_de['Metric'] = df_de['Metric'].astype(str).str.strip()
    df_de['Metric_Norm'] = df_de['Metric'].str.replace(' ', '', regex=False).str.lower()
    df_de = df_de[df_de['Metric'].notna() & (df_de['Metric'] != '') & (df_de['Metric'].str.lower() != 'nan')]
    cols_to_keep = [c for c in df_de.columns if "空列_" not in c]
    return df_de[cols_to_keep]
