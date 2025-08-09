import streamlit as st
import pandas as pd
import pyproj
from streamlit.components.v1 import html

# Configuração inicial da página
st.set_page_config(page_title="Conversor de Coordenadas", layout="wide")

# ---------------------- DETECÇÃO DE DISPOSITIVO MOBILE ----------------------
def check_mobile():
    """Detecta se o usuário está em um dispositivo móvel"""
    # JavaScript para detectar mobile e enviar para o Python
    mobile_js = """
    <script>
    function isMobile() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || 
               (window.innerWidth <= 800);
    }
    
    // Verifica ao carregar e quando a janela é redimensionada
    function checkMobile() {
        const isMobileDevice = isMobile();
        if (isMobileDevice) {
            window.parent.document.querySelector('iframe').contentWindow.postMessage('mobile', '*');
        } else {
            window.parent.document.querySelector('iframe').contentWindow.postMessage('desktop', '*');
        }
    }
    
    checkMobile();
    window.addEventListener('resize', checkMobile);
    </script>
    """
    
    # Componente para receber a mensagem do JavaScript
    callback_js = """
    <script>
    window.addEventListener('message', function(event) {
        if (event.data === 'mobile') {
            Streamlit.setComponentValue('mobile');
        } else if (event.data === 'desktop') {
            Streamlit.setComponentValue('desktop');
        }
    });
    </script>
    """
    
    # Executa os scripts
    html(mobile_js + callback_js, height=0, width=0)
    
    # Valor padrão até que o JavaScript seja executado
    if 'is_mobile' not in st.session_state:
        st.session_state.is_mobile = False

check_mobile()

# ---------------------- HEADER RESPONSIVO ----------------------
st.markdown(f"""
    <style>
    :root {{
        --brand: #fcb205;
        --brand-light: #ffd84f;
        --brand-dark: #c98b00;
        --accent: #ffffff;
        --text: #ffffff;
        --shadow: 0 10px 30px rgba(0,0,0,0.18);
        --radius: 14px;
    }}

    [data-testid="stHeader"] {{
        visibility: hidden;
    }}

    .custom-header {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        color: var(--text);
        padding: 12px 16px;
        font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Tahoma, sans-serif;
        background: linear-gradient(135deg, var(--brand) 0%, var(--brand-light) 100%);
        border-bottom: 1px solid rgba(255,255,255,.15);
        box-shadow: inset 0 -1px 0 rgba(255,255,255,.06), var(--shadow);
        z-index: 1000;
        overflow: visible;
        -webkit-backdrop-filter: saturate(120%) blur(4px);
        backdrop-filter: saturate(120%) blur(4px);
    }}

    section.main > div.block-container {{
        padding-top: 120px;
    }}

    .header-top {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
        font-weight: 700;
    }}

    .header-title {{
        font-size: clamp(14px, 4vw, 16px);
        letter-spacing: .2px;
        text-align: center;
        line-height: 1.4;
        text-shadow: 0 1px 0 rgba(0,0,0,.15);
        width: 100%;
    }}

    .nav {{
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
        width: 100%;
    }}

    .nav a, .nav .dropdown > a {{
        color: var(--text);
        text-decoration: none;
        font-weight: 600;
        padding: 6px 10px;
        border-radius: 999px;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        transition: all .15s ease;
        font-size: clamp(12px, 3vw, 14px);
    }}

    .dropdown {{
        position: relative;
    }}

    .dropdown-content {{
        display: none;
        position: absolute;
        left: 0;
        top: 100%;
        min-width: 180px;
        background: rgba(252, 178, 5, 0.95);
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: var(--radius);
        padding: 6px;
        margin-top: 4px;
        box-shadow: var(--shadow);
        z-index: 1001;
        -webkit-backdrop-filter: blur(8px);
        backdrop-filter: blur(8px);
    }}

    /* Estilos para mobile */
    @media (max-width: 768px) {{
        .custom-header {{
            padding: 10px 12px;
        }}
        
        .header-top {{
            gap: 6px;
        }}
        
        .nav {{
            gap: 6px;
        }}
        
        .nav a, .nav .dropdown > a {{
            padding: 5px 8px;
            font-size: 13px;
        }}
        
        .dropdown-content {{
            min-width: 160px;
            font-size: 13px;
        }}
    }}

    /* Estilos para telas muito pequenas (smartphones) */
    @media (max-width: 480px) {{
        .header-title {{
            font-size: 13px;
        }}
        
        .nav {{
            flex-direction: column;
            align-items: stretch;
            gap: 4px;
        }}
        
        .nav a, .nav .dropdown > a {{
            justify-content: center;
            padding: 6px;
        }}
        
        .dropdown {{
            width: 100%;
        }}
        
        .dropdown-content {{
            width: 100%;
            min-width: unset;
        }}
    }}
    </style>

    <div class="custom-header">
        <div class="header-top">
            <div class="header-title">🌐 Conversor de Coordenadas</div>
            <div class="nav">
                <div class="dropdown">
                    <a href="#" class="dropdown-toggle">
                        📸 Vinculadas
                        <span class="caret">▾</span>
                    </a>
                    <div class="dropdown-content">
                        <a href="https://www.cogerh.com.br/" target="_blank">🏢 COGERH</a>
                        <a href="https://www.sohidra.ce.gov.br/" target="_blank">💧 SOHIDRA</a>
                        <a href="https://www.funceme.br/" target="_blank">🌦️ FUNCEME</a>
                    </div>
                </div>
                <a href="https://www.facebook.com/seuusuario" target="_blank">📘 Facebook</a>
                <a href="https://wa.me/5588999999999" target="_blank">💬 WhatsApp</a>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ---------------------- TÍTULO PRINCIPAL ----------------------
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: clamp(1.5rem, 4vw, 2.2rem);
        margin-bottom: 0.5rem;
    }
    .main-subtitle {
        text-align: center;
        color: gray;
        font-size: clamp(0.9rem, 3vw, 1rem);
        margin-bottom: 2rem;
    }
    </style>
    <h1 class="main-title">📍 Conversor de Coordenadas</h1>
    <p class="main-subtitle">Transforme dados entre latitude/longitude, UTM e GMS</p>
    """,
    unsafe_allow_html=True
)

# ---------------------- CONTROLES PRINCIPAIS ----------------------
with st.container():
    st.markdown("""
    <style>
    .controls-bar {
        margin-bottom: 1.5rem;
    }
    .controls-title {
        font-size: clamp(1rem, 3vw, 1.2rem);
        margin-bottom: 0.8rem;
        font-weight: 600;
    }
    @media (max-width: 768px) {
        .stSelectbox, .stNumberInput, .stTextInput {
            width: 100% !important;
        }
        .stButton button {
            width: 100%;
        }
    }
    </style>
    <div class="controls-bar">
        <div class="controls-title">⚙️ Opções</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Layout responsivo baseado no tipo de dispositivo
    if st.session_state.get('is_mobile', False):
        # Layout para mobile (vertical)
        modo = st.selectbox("Modo de Conversão", ["📁 Arquivo CSV", "⌨️ Entrada Manual"], index=0)
        opcao = st.selectbox("Tipo de Conversão", [
            "🌍 Geográficas → UTM",
            "📐 UTM → Geográficas",
            "🧭 GMS → Geográficas"
        ], index=0)
        st.caption("Use os menus para escolher como quer converter. O resultado aparece abaixo.")
    else:
        # Layout para desktop (horizontal)
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

# ---------------------- LÓGICA DE CONVERSÃO ----------------------
if modo == "📁 Arquivo CSV":
    st.markdown("### 📄 Envie seu arquivo CSV")
    uploaded_file = st.file_uploader("Escolha um arquivo com os nomes de colunas adequados", type="csv", key="upload_csv")
    
    # Mensagens informativas baseadas no tipo de conversão
    if opcao == "🌍 Geográficas → UTM":
        st.info("Seu arquivo deve conter as colunas: `latitude` e `longitude` (em graus decimais).")
    elif opcao == "📐 UTM → Geográficas":
        st.info("Seu arquivo deve conter as colunas: `UTM_E` e `UTM_N` (em metros, Zona 24S).")
    elif opcao == "🧭 GMS → Geográficas":
        st.info("Seu CSV deve conter as colunas: `lat_grau`, `lat_min`, `lat_seg`, `lat_dir`, `lon_grau`, `lon_min`, `lon_seg`, `lon_dir`.")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip()

        if st.button("🔄 Converter Arquivo", key="convert_file"):
            try:
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
                        
                        # Exibição responsiva dos resultados
                        st.markdown("### 📊 Resultados da Conversão")
                        st.dataframe(df[['latitude', 'longitude', 'UTM_E', 'UTM_N']])
                        
                        st.markdown("### 🗺️ Visualização no Mapa")
                        st.map(df[['latitude', 'longitude']].dropna())
                        
                        # Botão de download
                        csv = df.to_csv(index=False).encode("utf-8")
                        st.download_button(
                            "📥 Baixar arquivo convertido", 
                            csv, 
                            "coordenadas_convertidas.csv", 
                            "text/csv",
                            key="download_csv_geo_utm"
                        )

                elif opcao == "📐 UTM → Geográficas":
                    if "UTM_E" in df.columns and "UTM_N" in df.columns:
                        proj_geo = pyproj.Transformer.from_crs("epsg:32724", "epsg:4326", always_xy=True)
                        lon, lat = proj_geo.transform(df['UTM_E'].values, df['UTM_N'].values)
                        df['longitude'] = [round(lon_, 6) for lon_ in lon]
                        df['latitude']  = [round(lat_, 6) for lat_ in lat]
                        
                        st.markdown("### 📊 Resultados da Conversão")
                        st.dataframe(df[['latitude', 'longitude', 'UTM_E', 'UTM_N']])
                        
                        st.markdown("### 🗺️ Visualização no Mapa")
                        st.map(df[['latitude', 'longitude']].dropna())
                        
                        csv = df.to_csv(index=False).encode("utf-8")
                        st.download_button(
                            "📥 Baixar arquivo convertido", 
                            csv, 
                            "coordenadas_convertidas.csv", 
                            "text/csv",
                            key="download_csv_utm_geo"
                        )

                elif opcao == "🧭 GMS → Geográficas":
                    need = ['lat_grau','lat_min','lat_seg','lat_dir','lon_grau','lon_min','lon_seg','lon_dir']
                    if all(col in df.columns for col in need):
                        def gms_to_decimal(grau, minuto, segundo, direcao):
                            decimal = grau + minuto / 60 + segundo / 3600
                            if direcao in ['S', 'W']: decimal *= -1
                            return decimal
                            
                        df['latitude'] = df.apply(lambda r: gms_to_decimal(r['lat_grau'], r['lat_min'], r['lat_seg'], r['lat_dir']), axis=1)
                        df['longitude'] = df.apply(lambda r: gms_to_decimal(r['lon_grau'], r['lon_min'], r['lon_seg'], r['lon_dir']), axis=1)
                        
                        st.markdown("### 📊 Resultados da Conversão")
                        st.dataframe(df[['latitude','longitude'] + need])
                        
                        st.markdown("### 🗺️ Visualização no Mapa")
                        st.map(df[['latitude','longitude']].dropna())
                        
                        csv = df.to_csv(index=False).encode("utf-8")
                        st.download_button(
                            "📥 Baixar arquivo convertido", 
                            csv, 
                            "coordenadas_convertidas.csv", 
                            "text/csv",
                            key="download_csv_gms_geo"
                        )
            except Exception as e:
                st.error(f"Ocorreu um erro durante a conversão: {str(e)}")

else:  # Modo de entrada manual
    if opcao == "🌍 Geográficas → UTM":
        st.markdown("### ✏️ Entrada Manual de Coordenadas")
        
        # Layout responsivo para inputs
        if st.session_state.get('is_mobile', False):
            lat = st.number_input("Latitude (graus decimais)", format="%.6f", key="lat_input_mobile")
            lon = st.number_input("Longitude (graus decimais)", format="%.6f", key="lon_input_mobile")
        else:
            col1, col2 = st.columns(2)
            with col1:
                lat = st.number_input("Latitude (graus decimais)", format="%.6f", key="lat_input_desktop")
            with col2:
                lon = st.number_input("Longitude (graus decimais)", format="%.6f", key="lon_input_desktop")
        
        if st.button("Converter", key="convert_geo_utm"):
            try:
                zone = int((lon + 180) / 6) + 1
                hemisphere = "south" if lat < 0 else "north"
                proj_utm = pyproj.Transformer.from_crs(
                    "epsg:4326",
                    f"+proj=utm +zone={zone} +{hemisphere}",
                    always_xy=True
                )
                e, n = proj_utm.transform(lon, lat)
                
                st.success(f"**Resultado UTM** — Zona {zone}/{'S' if hemisphere == 'south' else 'N'}:")
                st.markdown(f"""
                - 📍 **UTM_E (Este):** `{round(e, 2)}`
                - 📍 **UTM_N (Norte):** `{round(n, 2)}`
                """)
                
                st.markdown("### 🗺️ Localização no Mapa")
                st.map(pd.DataFrame({'latitude': [lat], 'longitude': [lon]}))
            except Exception as e:
                st.error(f"Erro na conversão: {str(e)}")

    elif opcao == "📐 UTM → Geográficas":
        st.markdown("### ✏️ Entrada Manual de Coordenadas UTM")
        
        if st.session_state.get('is_mobile', False):
            e = st.number_input("UTM_E (metros)", format="%.2f", key="e_input_mobile")
            n = st.number_input("UTM_N (metros)", format="%.2f", key="n_input_mobile")
        else:
            col1, col2 = st.columns(2)
            with col1:
                e = st.number_input("UTM_E (metros)", format="%.2f", key="e_input_desktop")
            with col2:
                n = st.number_input("UTM_N (metros)", format="%.2f", key="n_input_desktop")
        
        if st.button("Converter", key="convert_utm_geo"):
            try:
                proj_geo = pyproj.Transformer.from_crs("epsg:32724", "epsg:4326", always_xy=True)
                lon, lat = proj_geo.transform(e, n)
                
                st.success("**Resultado em Coordenadas Geográficas:**")
                st.markdown(f"""
                - 🌍 **Latitude:** `{round(lat, 6)}`
                - 🌍 **Longitude:** `{round(lon, 6)}`
                """)
                
                st.markdown("### 🗺️ Localização no Mapa")
                st.map(pd.DataFrame({'latitude': [lat], 'longitude': [lon]}))
            except Exception as e:
                st.error(f"Erro na conversão: {str(e)}")

    elif opcao == "🧭 GMS → Geográficas":
        st.markdown("### ✏️ Entrada Manual de Coordenadas em Graus, Minutos e Segundos")
        
        if st.session_state.get('is_mobile', False):
            st.markdown("**Latitude**")
            g_lat_deg = st.number_input("Graus", min_value=0, max_value=90, key="lat_deg_mobile")
            g_lat_min = st.number_input("Minutos", min_value=0, max_value=59, key="lat_min_mobile")
            g_lat_sec = st.number_input("Segundos", min_value=0.0, max_value=59.999, format="%.3f", key="lat_sec_mobile")
            g_lat_dir = st.selectbox("Direção", ["N", "S"], key="lat_dir_mobile")
            
            st.markdown("**Longitude**")
            g_lon_deg = st.number_input("Graus", min_value=0, max_value=180, key="lon_deg_mobile")
            g_lon_min = st.number_input("Minutos", min_value=0, max_value=59, key="lon_min_mobile")
            g_lon_sec = st.number_input("Segundos", min_value=0.0, max_value=59.999, format="%.3f", key="lon_sec_mobile")
            g_lon_dir = st.selectbox("Direção", ["E", "W"], key="lon_dir_mobile")
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Latitude**")
                g_lat_deg = st.number_input("Graus", min_value=0, max_value=90, key="lat_deg_desktop")
                g_lat_min = st.number_input("Minutos", min_value=0, max_value=59, key="lat_min_desktop")
                g_lat_sec = st.number_input("Segundos", min_value=0.0, max_value=59.999, format="%.3f", key="lat_sec_desktop")
                g_lat_dir = st.selectbox("Direção", ["N", "S"], key="lat_dir_desktop")
            
            with col2:
                st.markdown("**Longitude**")
                g_lon_deg = st.number_input("Graus", min_value=0, max_value=180, key="lon_deg_desktop")
                g_lon_min = st.number_input("Minutos", min_value=0, max_value=59, key="lon_min_desktop")
                g_lon_sec = st.number_input("Segundos", min_value=0.0, max_value=59.999, format="%.3f", key="lon_sec_desktop")
                g_lon_dir = st.selectbox("Direção", ["E", "W"], key="lon_dir_desktop")
        
        if st.button("Converter para Decimal", key="convert_gms_geo"):
            try:
                latitude = g_lat_deg + g_lat_min / 60 + g_lat_sec / 3600
                if g_lat_dir == "S": latitude *= -1

                longitude = g_lon_deg + g_lon_min / 60 + g_lon_sec / 3600
                if g_lon_dir == "W": longitude *= -1

                st.success("**Coordenadas Decimais:**")
                st.markdown(f"""
                - 🌍 **Latitude:** `{round(latitude, 6)}`
                - 🌍 **Longitude:** `{round(longitude, 6)}`
                """)
                
                st.markdown("### 🗺️ Localização no Mapa")
                st.map(pd.DataFrame({'latitude': [latitude], 'longitude': [longitude]}))
            except Exception as e:
                st.error(f"Erro na conversão: {str(e)}")

# ---------------------- RODAPÉ ----------------------
st.markdown("""
<style>
.footer {
    text-align: center;
    padding: 1rem;
    margin-top: 2rem;
    color: #666;
    font-size: 0.9rem;
    border-top: 1px solid #eee;
}
</style>
<div class="footer">
    © 2023 Conversor de Coordenadas | Desenvolvido para Quixeramobim-CE
</div>
""", unsafe_allow_html=True)
