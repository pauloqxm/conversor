import streamlit as st
import pandas as pd
import pyproj

st.set_page_config(page_title="Conversor de Coordenadas", layout="wide")

# ---------------------- HEADER + MENU SUSPENSO ----------------------
st.markdown(f"""
    <style>
    /* Esconde o header nativo do Streamlit */
    [data-testid="stHeader"] {{
        visibility: hidden;
    }}

    /* Cabeçalho fixo */
    .custom-header {{
        position: fixed;
        top: 0; left: 0;
        width: 100%;
        background-color: #04a5c9;
        color: white;
        padding: 10px 24px;
        font-family: Tahoma, sans-serif;
        border-bottom: 3px solid #fad905;
        z-index: 100000;
        overflow: visible;         /* deixa o submenu sair do header */
        pointer-events: auto;
    }}

    /* Garante espaço para o conteúdo abaixo do header */
    section.main > div.block-container {{
        position: relative;
        z-index: 1;
        padding-top: 100px;        /* ajuste se seu header ficar maior/menor */
    }}

    /* Título + menu centralizados */
    .header-top {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
        font-weight: bold;
    }}

    .header-title {{
        font-size: 14px;
        text-align: center;
        line-height: 1.4;
    }}

    /* Barra de navegação centralizada */
    .nav {{
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 24px;
        position: relative;
        z-index: 100000;
    }}
    .nav a, .nav .dropdown > a {{
        color: white;
        text-decoration: none;
        font-weight: 600;
        padding: 6px 8px;
        border-radius: 4px;
        position: relative;
    }}
    .nav a:hover {{ background: rgba(0,0,0,0.1); }}

    /* Dropdown */
    .dropdown {{
        position: relative;
        display: inline-block;
    }}
    .dropdown > a {{
        cursor: pointer;
        padding-bottom: 12px;     /* mais área e encosta no submenu (anti-gap) */
    }}

    /* Seta branca indicando que é suspenso */
    .dropdown > a::after {{
        content: "▼";
        font-size: 10px;
        margin-left: 6px;
        color: white;
        position: relative;
        top: -1px;
    }}

    /* Submenu: encostado no botão, sem gap */
    .dropdown-content {{
        display: none;
        position: absolute;
        left: 0;
        top: 95%;                /* cola no gatilho */
        background-color: #04a5c9;
        min-width: 180px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        border: 1px solid #038fb0;
        border-radius: 6px;
        padding: 6px 0;
        z-index: 100001;
        pointer-events: auto;
        white-space: nowrap;
    }}

    /* “Ponte” anti-gap: mantém hover ao descer o mouse */
    .dropdown-content::before {{
        content: "";
        position: absolute;
        top: -10px;              /* sobe 10px acima do submenu */
        left: 0;
        right: 0;
        height: 10px;            /* espessura da ponte */
        background: transparent;
    }}

    /* Abre no hover (desktop) */
    .dropdown:hover > .dropdown-content {{ display: block; }}
    /* Abre no clique (mobile/apoio) */
    .dropdown.open > .dropdown-content {{ display: block; }}

    .dropdown-content a {{
        color: white;
        text-decoration: none;
        display: block;
        padding: 8px 12px;
        font-weight: 500;
    }}
    .dropdown-content a:hover {{
        background: rgba(0,0,0,0.12);
    }}
    </style>

    <div class="custom-header">
        <div class="header-top">
            <div class="header-title">🔎 Você Fiscaliza | Quixeramobim - Ceará</div>
            <div class="nav">
                <div class="dropdown">
                    <a href="#" class="dropdown-toggle">📸 Vinculadas</a>
                    <div class="dropdown-content">
                        <a href="https://www.cogerh.com.br/" target="_blank">COGERH</a>
                        <a href="https://www.sohidra.ce.gov.br/" target="_blank">SOHIDRA</a>
                        <a href="https://www.funceme.br/" target="_blank">FUNCEME</a>
                    </div>
                </div>
                <a href="https://www.facebook.com/seuusuario" target="_blank">📘 Facebook</a>
                <a href="https://wa.me/5588999999999" target="_blank">💬 WhatsApp</a>
            </div>
        </div>
    </div>

    <script>
    // Suporte a clique: útil no mobile e como fallback ao hover
    window.addEventListener('DOMContentLoaded', function() {{
        const toggles = document.querySelectorAll('.dropdown-toggle');
        toggles.forEach(function(tg) {{
            tg.addEventListener('click', function(e) {{
                e.preventDefault();
                e.stopPropagation();
                const parent = this.closest('.dropdown');
                document.querySelectorAll('.dropdown.open').forEach(function(dd) {{
                    if (dd !== parent) dd.classList.remove('open');
                }});
                parent.classList.toggle('open');
            }});
        }});
        document.addEventListener('click', function() {{
            document.querySelectorAll('.dropdown.open').forEach(function(dd) {{
                dd.classList.remove('open');
            }});
        }});
    }});
    </script>
""", unsafe_allow_html=True)


# ---------------------- TÍTULO ----------------------

st.markdown(
    "<h1 style='text-align: center;'>📍 Conversor de Coordenadas</h1>"
    "<p style='text-align: center; color: gray;'>Transforme dados entre latitude/longitude, UTM e GMS</p>",
    unsafe_allow_html=True
)

# ---------------------- CONTROLES (SUBSTITUINDO O SIDEBAR) ----------------------
with st.container():
    st.markdown('<div class="controls-bar">', unsafe_allow_html=True)
    st.markdown('<div class="controls-title">⚙️ Opções</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1.1, 1.2, 2.2])

    with c1:
        modo = st.selectbox("Modo de Conversão", ["📁 Arquivo CSV", "⌨️ Entrada Manual"], index=0)
    with c2:
        opcao = st.selectbox("Tipo de Conversão", [
            "🌍 Geográficas → UTM",
            "📐 UTM → Geográficas",
            "🧭 GMS → Geográficas"
        ], index=0)
    with c3:
        st.caption("Use os menus para escolher como quer converter. O resultado aparece abaixo.")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- LÓGICA PRINCIPAL ----------------------
if modo == "📁 Arquivo CSV":
    st.markdown("### 📄 Envie seu arquivo CSV")
    uploaded_file = st.file_uploader("Escolha um arquivo com os nomes de colunas adequados", type="csv", key="upload_csv_unico")

    if opcao == "🌍 Geográficas → UTM":
        st.info("Seu arquivo deve conter as colunas: `latitude` e `longitude` (em graus decimais).")
    elif opcao == "📐 UTM → Geográficas":
        st.info("Seu arquivo deve conter as colunas: `UTM_E` e `UTM_N` (em metros, Zona 24S).")
    elif opcao == "🧭 GMS → Geográficas":
        st.info("Seu CSV deve conter as colunas: `lat_grau`, `lat_min`, `lat_seg`, `lat_dir`, `lon_grau`, `lon_min`, `lon_seg`, `lon_dir`.")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip()

        if st.button("🔄 Converter Arquivo"):
            if opcao == "🌍 Geográficas → UTM":
                if "latitude" in df.columns and "longitude" in df.columns:
                    zone = int((df['longitude'].iloc[0] + 180) / 6) + 1
                    hemisphere = "south" if df['latitude'].iloc[0] < 0 else "north"
                    proj_utm = pyproj.Transformer.from_crs(
                        "epsg:4326",
                        f"+proj=utm +zone={zone} +{hemisphere}",
                        always_xy=True
                    )
                    easting, northing = proj_utm.transform(df['longitude'].values, df['latitude'].values)
                    df['UTM_E'] = [round(e, 2) for e in easting]
                    df['UTM_N'] = [round(n, 2) for n in northing]
                    st.dataframe(df[['latitude', 'longitude', 'UTM_E', 'UTM_N']])
                    st.map(df[['latitude', 'longitude']].dropna())
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button("📥 Baixar arquivo convertido", csv, "convertido.csv", "text/csv")

            elif opcao == "📐 UTM → Geográficas":
                if "UTM_E" in df.columns and "UTM_N" in df.columns:
                    proj_geo = pyproj.Transformer.from_crs("epsg:32724", "epsg:4326", always_xy=True)
                    lon, lat = proj_geo.transform(df['UTM_E'].values, df['UTM_N'].values)
                    df['longitude'] = [round(lon_, 6) for lon_ in lon]
                    df['latitude']  = [round(lat_, 6) for lat_ in lat]
                    st.dataframe(df[['latitude', 'longitude', 'UTM_E', 'UTM_N']])
                    st.map(df[['latitude', 'longitude']].dropna())
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button("📥 Baixar arquivo convertido", csv, "convertido.csv", "text/csv")

            elif opcao == "🧭 GMS → Geográficas":
                need = ['lat_grau','lat_min','lat_seg','lat_dir','lon_grau','lon_min','lon_seg','lon_dir']
                if all(col in df.columns for col in need):
                    def gms_to_decimal(grau, minuto, segundo, direcao):
                        decimal = grau + minuto / 60 + segundo / 3600
                        if direcao in ['S', 'W']: decimal *= -1
                        return decimal
                    df['latitude'] = df.apply(lambda r: gms_to_decimal(r['lat_grau'], r['lat_min'], r['lat_seg'], r['lat_dir']), axis=1)
                    df['longitude'] = df.apply(lambda r: gms_to_decimal(r['lon_grau'], r['lon_min'], r['lon_seg'], r['lon_dir']), axis=1)
                    st.dataframe(df[['latitude','longitude']])
                    st.map(df[['latitude','longitude']].dropna())
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button("📥 Baixar arquivo convertido", csv, "convertido.csv", "text/csv")

else:
    if opcao == "🌍 Geográficas → UTM":
        st.markdown("### ✏️ Entrada Manual de Coordenadas")
        lat = st.number_input("Latitude (graus decimais)", format="%.6f")
        lon = st.number_input("Longitude (graus decimais)", format="%.6f")
        if st.button("Converter"):
            zone = int((lon + 180) / 6) + 1
            hemisphere = "south" if lat < 0 else "north"
            proj_utm = pyproj.Transformer.from_crs(
                "epsg:4326",
                f"+proj=utm +zone={zone} +{hemisphere}",
                always_xy=True
            )
            e, n = proj_utm.transform(lon, lat)
            st.success(f"Resultado UTM — Zona {zone}/{'S' if hemisphere == 'south' else 'N'}:")
            st.write(f"📍 UTM_E: **{round(e, 2)}**  |  UTM_N: **{round(n, 2)}**")
            st.map(pd.DataFrame({'latitude': [lat], 'longitude': [lon]}))

    elif opcao == "📐 UTM → Geográficas":
        st.markdown("### ✏️ Entrada Manual de Coordenadas")
        e = st.number_input("UTM_E (metros)", format="%.2f")
        n = st.number_input("UTM_N (metros)", format="%.2f")
        if st.button("Converter"):
            proj_geo = pyproj.Transformer.from_crs("epsg:32724", "epsg:4326", always_xy=True)
            lon, lat = proj_geo.transform(e, n)
            st.success("Resultado em Coordenadas Geográficas:")
            st.write(f"🌍 Latitude: **{round(lat, 6)}**  |  Longitude: **{round(lon, 6)}**")
            st.map(pd.DataFrame({'latitude': [lat], 'longitude': [lon]}))

    elif opcao == "🧭 GMS → Geográficas":
        st.markdown("### ✏️ Entrada Manual de Coordenadas em Graus, Minutos e Segundos")
        g_lat_deg = st.number_input("Latitude - Graus", value=0)
        g_lat_min = st.number_input("Latitude - Minutos", value=0)
        g_lat_sec = st.number_input("Latitude - Segundos", value=0.0)
        g_lat_dir = st.selectbox("Direção da Latitude", ["N", "S"])

        g_lon_deg = st.number_input("Longitude - Graus", value=0)
        g_lon_min = st.number_input("Longitude - Minutos", value=0)
        g_lon_sec = st.number_input("Longitude - Segundos", value=0.0)
        g_lon_dir = st.selectbox("Direção da Longitude", ["E", "W"])

        if st.button("Converter para Decimal"):
            latitude = g_lat_deg + g_lat_min / 60 + g_lat_sec / 3600
            if g_lat_dir == "S": latitude *= -1

            longitude = g_lon_deg + g_lon_min / 60 + g_lon_sec / 3600
            if g_lon_dir == "W": longitude *= -1

            st.success("Coordenadas Decimais:")
            st.write(f"🌍 Latitude: **{round(latitude, 6)}**  |  Longitude: **{round(longitude, 6)}**")
            st.map(pd.DataFrame({'latitude': [latitude], 'longitude': [longitude]}))








