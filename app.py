
import streamlit as st
import pandas as pd
import pyproj
from io import BytesIO

st.set_page_config(page_title="Conversor Geográfico UTM <-> LatLong", layout="centered")

st.title("Conversor de Coordenadas Geográficas ↔️ UTM (Zona 24S)")

with st.sidebar:
    st.header("⚙️ Opções")
    opcao = st.radio("Escolha a direção da conversão:", ["Geográficas → UTM", "UTM → Geográficas"])

uploaded_file = st.file_uploader("📁 Envie seu arquivo CSV", type="csv", key="upload_csv_unico")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()

    if opcao == "Geográficas → UTM":
        if 'latitude' in df.columns and 'longitude' in df.columns:
            st.success("Convertendo latitude e longitude para UTM (Zona 24S)")
            proj_utm = pyproj.Transformer.from_crs("epsg:4326", "epsg:32724", always_xy=True)

            easting, northing = proj_utm.transform(df['longitude'].values, df['latitude'].values)
            df['UTM_E'] = [round(e, 2) for e in easting]
            df['UTM_N'] = [round(n, 2) for n in northing]

            st.dataframe(df[['latitude', 'longitude', 'UTM_E', 'UTM_N']])
            st.map(df[['latitude', 'longitude']].dropna())

        else:
            st.error("O arquivo deve conter as colunas 'latitude' e 'longitude'.")

    else:  # UTM → Geográficas
        if 'UTM_E' in df.columns and 'UTM_N' in df.columns:
            st.success("Convertendo UTM (Zona 24S) para latitude e longitude")
            proj_geo = pyproj.Transformer.from_crs("epsg:32724", "epsg:4326", always_xy=True)

            lon, lat = proj_geo.transform(df['UTM_E'].values, df['UTM_N'].values)
            df['longitude'] = [round(lon_, 6) for lon_ in lon]
            df['latitude'] = [round(lat_, 6) for lat_ in lat]

            st.dataframe(df[['UTM_E', 'UTM_N', 'latitude', 'longitude']])
            st.map(df[['latitude', 'longitude']].dropna())

        else:
            st.error("O arquivo deve conter as colunas 'UTM_E' e 'UTM_N'.")

    def converter_para_csv_bytes(df):
        buffer = BytesIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        return buffer

    csv_bytes = converter_para_csv_bytes(df)

    st.download_button(
        label="📥 Baixar CSV convertido",
        data=csv_bytes,
        file_name="coordenadas_convertidas.csv",
        mime="text/csv"
    )
