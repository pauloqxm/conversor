
import streamlit as st
import pandas as pd
import pyproj
from io import BytesIO

st.set_page_config(page_title="Conversor UTM ↔️ Geográfica", layout="wide")

st.markdown(
    "<h1 style='text-align: center;'>📍 Conversor de Coordenadas</h1>"
    "<p style='text-align: center; color: gray;'>Transforme seus dados entre latitude/longitude e UTM (Zona 24S)</p>",
    unsafe_allow_html=True
)

with st.sidebar:
    st.image("https://img.icons8.com/emoji/96/compass-emoji.png", width=64)
    st.header("⚙️ Opções")
    modo = st.radio("Modo de Conversão:", ["📁 Arquivo CSV", "⌨️ Entrada Manual"])
    opcao = st.radio("Tipo de Conversão:", ["🌍 Geográficas → UTM", "📐 UTM → Geográficas"])
    st.markdown("---")

if modo == "📁 Arquivo CSV":
    st.markdown("### 📄 Envie seu arquivo CSV")
    uploaded_file = st.file_uploader("Escolha um arquivo com os nomes de colunas adequados", type="csv", key="upload_csv_unico")

    if opcao == "🌍 Geográficas → UTM":
        st.info("Seu arquivo deve conter as colunas: `latitude` e `longitude` (em graus decimais).")
    else:
        st.info("Seu arquivo deve conter as colunas: `UTM_E` e `UTM_N` (em metros, Zona 24S).")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip()

        aba1, aba2 = st.tabs(["📄 Tabela Convertida", "🗺️ Mapa Visual"])

        if opcao == "🌍 Geográficas → UTM":
            if 'latitude' in df.columns and 'longitude' in df.columns:
                proj_utm = pyproj.Transformer.from_crs("epsg:4326", "epsg:32724", always_xy=True)
                easting, northing = proj_utm.transform(df['longitude'].values, df['latitude'].values)
                df['UTM_E'] = [round(e, 2) for e in easting]
                df['UTM_N'] = [round(n, 2) for n in northing]

                with aba1:
                    st.success("Conversão concluída com sucesso.")
                    st.dataframe(df[['latitude', 'longitude', 'UTM_E', 'UTM_N']])
                with aba2:
                    st.map(df[['latitude', 'longitude']].dropna())
            else:
                st.error("❌ O arquivo não contém as colunas necessárias: 'latitude' e 'longitude'.")
        else:
            if 'UTM_E' in df.columns and 'UTM_N' in df.columns:
                proj_geo = pyproj.Transformer.from_crs("epsg:32724", "epsg:4326", always_xy=True)
                lon, lat = proj_geo.transform(df['UTM_E'].values, df['UTM_N'].values)
                df['longitude'] = [round(lon_, 6) for lon_ in lon]
                df['latitude'] = [round(lat_, 6) for lat_ in lat]

                with aba1:
                    st.success("Conversão concluída com sucesso.")
                    st.dataframe(df[['UTM_E', 'UTM_N', 'latitude', 'longitude']])
                with aba2:
                    st.map(df[['latitude', 'longitude']].dropna())
            else:
                st.error("❌ O arquivo não contém as colunas necessárias: 'UTM_E' e 'UTM_N'.")

        def converter_para_csv_bytes(df):
            buffer = BytesIO()
            df.to_csv(buffer, index=False)
            buffer.seek(0)
            return buffer

        st.download_button(
            label="📥 Baixar CSV convertido",
            data=converter_para_csv_bytes(df),
            file_name="coordenadas_convertidas.csv",
            mime="text/csv"
        )

else:
    st.markdown("### ✏️ Entrada Manual de Coordenadas")

    if opcao == "🌍 Geográficas → UTM":
        lat = st.number_input("Latitude (graus decimais)", format="%.6f")
        lon = st.number_input("Longitude (graus decimais)", format="%.6f")

        if st.button("Converter"):
            proj_utm = pyproj.Transformer.from_crs("epsg:4326", "epsg:32724", always_xy=True)
            e, n = proj_utm.transform(lon, lat)
            st.success(f"Resultado UTM (Zona 24S):")
            st.write(f"📍 UTM_E: **{round(e, 2)}**  |  UTM_N: **{round(n, 2)}**")

    else:
        e = st.number_input("UTM_E (metros)", format="%.2f")
        n = st.number_input("UTM_N (metros)", format="%.2f")

        if st.button("Converter"):
            proj_geo = pyproj.Transformer.from_crs("epsg:32724", "epsg:4326", always_xy=True)
            lon, lat = proj_geo.transform(e, n)
            st.success("Resultado em Coordenadas Geográficas:")
            st.write(f"🌍 Latitude: **{round(lat, 6)}**  |  Longitude: **{round(lon, 6)}**")
