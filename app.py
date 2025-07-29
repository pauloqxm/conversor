import streamlit as st
import pandas as pd
import pyproj
from io import BytesIO

st.set_page_config(page_title="Conversor UTM ↔️ Geográfica", layout="wide")

st.markdown(
    "<h1 style='text-align: center;'>📍 Conversor de Coordenadas</h1>"
    "<p style='text-align: center; color: gray;'>Transforme dados entre latitude/longitude, UTM e GMS</p>",
    unsafe_allow_html=True
)

with st.sidebar:
    st.image("https://img.icons8.com/emoji/96/compass-emoji.png", width=64)
    st.header("⚙️ Opções")
    modo = st.radio("Modo de Conversão:", ["📁 Arquivo CSV", "⌨️ Entrada Manual"])
    opcao = st.radio("Tipo de Conversão:", ["🌍 Geográficas → UTM", "📐 UTM → Geográficas", "🧭 GMS → Geográficas"])

st.markdown("---")

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

        if opcao == "🌍 Geográficas → UTM":
            if 'latitude' in df.columns and 'longitude' in df.columns:
                zone = int((df['longitude'].mean() + 180) / 6) + 1
                hemisphere = "south" if df['latitude'].mean() < 0 else "north"
                proj_utm = pyproj.Transformer.from_crs("epsg:4326", f"+proj=utm +zone={zone} +south" if hemisphere == "south" else f"+proj=utm +zone={zone} +north", always_xy=True)
                easting, northing = proj_utm.transform(df['longitude'].values, df['latitude'].values)
                df['UTM_E'] = [round(e, 2) for e in easting]
                df['UTM_N'] = [round(n, 2) for n in northing]
                st.dataframe(df[['latitude', 'longitude', 'UTM_E', 'UTM_N']])
                st.map(df[['latitude', 'longitude']].dropna())
        elif opcao == "📐 UTM → Geográficas":
            if 'UTM_E' in df.columns and 'UTM_N' in df.columns:
                proj_geo = pyproj.Transformer.from_crs("epsg:32724", "epsg:4326", always_xy=True)
                lon, lat = proj_geo.transform(df['UTM_E'].values, df['UTM_N'].values)
                df['longitude'] = [round(lon_, 6) for lon_ in lon]
                df['latitude'] = [round(lat_, 6) for lat_ in lat]
                st.dataframe(df[['UTM_E', 'UTM_N', 'latitude', 'longitude']])
                st.map(df[['latitude', 'longitude']].dropna())

else:
    if opcao == "🌍 Geográficas → UTM":
        st.markdown("### ✏️ Entrada Manual de Coordenadas")
        lat = st.number_input("Latitude (graus decimais)", format="%.6f")
        lon = st.number_input("Longitude (graus decimais)", format="%.6f")
        if st.button("Converter"):
            zone = int((lon + 180) / 6) + 1
            hemisphere = "south" if lat < 0 else "north"
            proj_utm = pyproj.Transformer.from_crs("epsg:4326", f"+proj=utm +zone={zone} +south" if hemisphere == "south" else f"+proj=utm +zone={zone} +north", always_xy=True)
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
            if g_lat_dir == "S":
                latitude *= -1

            longitude = g_lon_deg + g_lon_min / 60 + g_lon_sec / 3600
            if g_lon_dir == "W":
                longitude *= -1

            st.success("Coordenadas Decimais:")
            st.write(f"🌍 Latitude: **{round(latitude, 6)}**  |  Longitude: **{round(longitude, 6)}**")
            st.map(pd.DataFrame({'latitude': [latitude], 'longitude': [longitude]}))
