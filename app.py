import streamlit as st
import pandas as pd
import pyproj
from io import BytesIO

st.set_page_config(page_title="Conversor Geográfico", layout="centered")

st.title("Conversor de Coordenadas Geográficas para UTM (Zona 24S)")

uploaded_file = st.file_uploader("📁 Envie seu arquivo CSV com colunas 'latitude' e 'longitude'", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if 'latitude' in df.columns and 'longitude' in df.columns:
        st.success("Arquivo lido com sucesso!")

        proj_utm = pyproj.Transformer.from_crs("epsg:4326", "epsg:32724", always_xy=True)

        # Converte todas as coordenadas
        easting, northing = proj_utm.transform(df['longitude'].values, df['latitude'].values)

        df['UTM_E'] = easting
        df['UTM_N'] = northing

        st.subheader("Visualização dos dados convertidos:")
        st.dataframe(df[['latitude', 'longitude', 'UTM_E', 'UTM_N']])

        # Botão para download
        def converter_para_csv_bytes(df):
            buffer = BytesIO()
            df.to_csv(buffer, index=False)
            buffer.seek(0)
            return buffer

        csv_bytes = converter_para_csv_bytes(df)

        st.download_button(
            label="📥 Baixar CSV com UTM",
            data=csv_bytes,
            file_name="coordenadas_utm_z24s.csv",
            mime="text/csv"
        )
    else:
        st.error("O arquivo deve conter as colunas 'latitude' e 'longitude'")
