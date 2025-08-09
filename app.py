import streamlit as st
import pandas as pd
import pyproj

st.set_page_config(page_title="Conversor de Coordenadas", layout="wide", initial_sidebar_state="collapsed")

# ====================== HEADER + NAV (RESPONSIVO) ======================
st.markdown(f"""
<style>
:root{
  --brand:#1e8c3a; --brand-light:#34c759; --brand-dark:#0d5c26;
  --text:#fff; --shadow:0 10px 30px rgba(0,0,0,.18); --radius:14px;
}
[data-testid="stHeader"]{visibility:hidden;}
section.main > div.block-container{position:relative;z-index:1;padding-top:120px;padding-bottom:16px;}

.custom-header{
  position:fixed; inset:0 0 auto 0; width:100%;
  color:var(--text); padding:10px 20px;
  font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Tahoma,sans-serif;
  background:linear-gradient(135deg,var(--brand) 0%,var(--brand-light) 100%);
  border-bottom:1px solid rgba(255,255,255,.15);
  box-shadow:inset 0 -1px 0 rgba(255,255,255,.06), var(--shadow);
  z-index:100000; -webkit-backdrop-filter:saturate(120%) blur(4px); backdrop-filter:saturate(120%) blur(4px);
  overflow:visible;
}

/* TOP BAR */
.header-top{display:flex;align-items:center;justify-content:space-between;gap:16px;}
.logo-title{display:flex;align-items:center;gap:10px;min-width:0;}
.logo-title img{height:36px;width:auto;display:block;}
.header-title{font-size:16px;line-height:1.3;text-shadow:0 1px 0 rgba(0,0,0,.15);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}

/* NAV (desktop) */
.nav{display:flex;justify-content:center;align-items:center;gap:16px;flex-wrap:wrap;z-index:100001;}
.btn-chip{
  color:var(--text)!important;text-decoration:none!important;font-weight:600;
  padding:10px 16px;border-radius:999px;display:inline-flex;align-items:center;gap:8px;
  background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.22);
  box-shadow:inset 0 0 0 1px rgba(255,255,255,.06);
  transition:transform .15s ease, background .2s ease, border-color .2s ease; position:relative;
}
.btn-chip:hover{transform:translateY(-1px);background:rgba(255,255,255,.14);border-color:rgba(255,255,255,.32);}

/* Caret (chevron) com espaçamento */
.dropdown{position:relative;display:inline-block;}
.dropdown > a.btn-chip{padding-right:16px;}
.dropdown > a .caret{
  display:inline-block;width:10px;height:10px;margin-left:10px;
  border-right:2px solid #fff;border-bottom:2px solid #fff;
  transform:translateY(-1px) rotate(45deg);transition:transform .25s ease;opacity:.9;
}
.dropdown:hover > a .caret,.dropdown.open > a .caret{transform:translateY(-1px) rotate(-135deg);}

/* Submenu (desktop) */
.dropdown-content{
  display:none;position:absolute;left:0;top:100%;min-width:220px;background:var(--brand-light);
  border:1px solid rgba(255,255,255,.18);border-radius:var(--radius);padding:8px;margin-top:2px;
  box-shadow:var(--shadow);z-index:100002;-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);
}
.dropdown:hover > .dropdown-content,.dropdown.open > .dropdown-content{display:block;}
.dropdown-content a{
  color:var(--text)!important;text-decoration:none!important;position:relative;display:flex;align-items:center;gap:10px;
  padding:12px;border-radius:10px;font-weight:600;transition:background .18s ease, transform .12s ease;
}
.dropdown-content a:hover{background:rgba(255,255,255,.16);transform:translateX(2px);}

/* ===== MOBILE ===== */
.hamburger{display:none;}

@media (max-width:768px){
  section.main > div.block-container{padding-top:140px;} /* mais espaço pq o menu pode abrir */
  .logo-title img{height:28px;}
  .header-title{font-size:15px;}

  /* mostra botão hambúrguer e esconde nav padrão */
  .hamburger{
    display:inline-flex;align-items:center;justify-content:center;
    width:40px;height:40px;border-radius:10px;border:1px solid rgba(255,255,255,.22);
    background:rgba(255,255,255,.08);cursor:pointer;user-select:none;
  }
  .hamburger span{
    display:block;width:18px;height:2px;background:#fff;position:relative;
  }
  .hamburger span::before,.hamburger span::after{
    content:"";position:absolute;left:0;width:18px;height:2px;background:#fff;
  }
  .hamburger span::before{top:-6px;}
  .hamburger span::after{top:6px;}

  /* Nav vira painel vertical */
  .nav{display:none;position:absolute;left:0;right:0;top:100%;padding:10px 12px;gap:10px;}
  .nav.is-open{display:flex;flex-direction:column;align-items:stretch;}
  .btn-chip{width:100%;justify-content:flex-start;}
  /* Submenu no mobile: posicionamento estático e largura total */
  .dropdown{width:100%;}
  .dropdown-content{position:static;display:none;margin-top:8px;min-width:unset;border-radius:12px;}
  .dropdown.open > .dropdown-content{display:block;}
}
</style>

<div class="custom-header">
  <div class="header-top">
    <div class="logo-title">
      <img src="https://i.ibb.co/Kp64sjfH/LUPA.png" alt="Logo">
      <div class="header-title">🌐 Conversor de Coordenadas</div>
    </div>
    <button class="hamburger" aria-label="Abrir menu" title="Menu">
      <span></span>
    </button>
    <div class="nav" id="topNav">
      <div class="dropdown">
        <a href="#" class="dropdown-toggle btn-chip">📸 Vinculadas <span class="caret"></span></a>
        <div class="dropdown-content">
          <a href="https://www.cogerh.com.br/" target="_blank" rel="noopener">🏢 COGERH</a>
          <a href="https://www.sohidra.ce.gov.br/" target="_blank" rel="noopener">💧 SOHIDRA</a>
          <a href="https://www.funceme.br/" target="_blank" rel="noopener">🌦️ FUNCEME</a>
        </div>
      </div>
      <a href="https://www.facebook.com/seuusuario" target="_blank" rel="noopener" class="btn-chip">📘 Facebook</a>
      <a href="https://wa.me/5588999999999" target="_blank" rel="noopener" class="btn-chip">💬 WhatsApp</a>
    </div>
  </div>
</div>

<script>
// Toggle do hambúrguer (mobile) + dropdown
document.addEventListener('click', function(e){
  const burger = e.target.closest('.hamburger');
  const nav = document.getElementById('topNav');
  const toggle = e.target.closest('.dropdown-toggle');
  const openedDropdowns = document.querySelectorAll('.dropdown.open');

  // hamburguer
  if (burger){
    e.preventDefault();
    nav.classList.toggle('is-open');
    // fecha dropdowns quando fecha o painel
    if (!nav.classList.contains('is-open')){
      openedDropdowns.forEach(dd=>dd.classList.remove('open'));
    }
    return;
  }

  // clique fora: fecha painel e dropdowns (apenas em mobile)
  if (!e.target.closest('.custom-header')){
    nav?.classList.remove('is-open');
    openedDropdowns.forEach(dd=>dd.classList.remove('open'));
    return;
  }

  // dropdown
  if (toggle){
    e.preventDefault();
    const parent = toggle.closest('.dropdown');
    openedDropdowns.forEach(dd=>{ if (dd!==parent) dd.classList.remove('open');});
    parent.classList.toggle('open');
  }
});
</script>
""", unsafe_allow_html=True)




# ====================== TÍTULO ======================
st.markdown(
    "<h1 style='text-align:center;margin-bottom:4px;'>📍 Conversor de Coordenadas</h1>"
    "<p style='text-align:center;color:gray;margin-top:0;'>Transforme dados entre latitude/longitude, UTM e GMS</p>",
    unsafe_allow_html=True
)

# ====================== CONTROLES ======================
with st.container():
    st.markdown('<div class="controls-bar">', unsafe_allow_html=True)
    st.markdown('<div class="controls-title">⚙️ Opções</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1.1, 1.2, 2.2])
    with c1:
        modo = st.selectbox(
            "Modo de Conversão",
            ["📁 Arquivo CSV", "⌨️ Entrada Manual"],
            index=0,
            key="modo_conv"
        )
    with c2:
        opcao = st.selectbox(
            "Tipo de Conversão",
            ["🌍 Geográficas → UTM", "📐 UTM → Geográficas", "🧭 GMS → Geográficas"],
            index=0,
            key="tipo_conv"
        )
    with c3:
        st.caption("Use os menus para escolher como quer converter. O resultado aparece abaixo.")
    st.markdown('</div>', unsafe_allow_html=True)

# ====================== LÓGICA PRINCIPAL ======================
if modo == "📁 Arquivo CSV":
    st.markdown("### 📄 Envie seu arquivo CSV")
    uploaded_file = st.file_uploader(
        "Escolha um arquivo com os nomes de colunas adequados",
        type="csv",
        key="upload_csv_unico"
    )

    if opcao == "🌍 Geográficas → UTM":
        st.info("Seu arquivo deve conter as colunas: `latitude` e `longitude` (em graus decimais).")
    elif opcao == "📐 UTM → Geográficas":
        st.info("Seu arquivo deve conter as colunas: `UTM_E` e `UTM_N` (em metros, Zona 24S).")
    elif opcao == "🧭 GMS → Geográficas":
        st.info("Seu CSV deve conter as colunas: `lat_grau`, `lat_min`, `lat_seg`, `lat_dir`, `lon_grau`, `lon_min`, `lon_seg`, `lon_dir`.")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip()

        if st.button("🔄 Converter Arquivo", key="btn_convert_arquivo"):
            if opcao == "🌍 Geográficas → UTM" and "latitude" in df.columns and "longitude" in df.columns:
                zone = int((df['longitude'].iloc[0] + 180) / 6) + 1
                hemisphere = "south" if df['latitude'].iloc[0] < 0 else "north"
                proj_utm = pyproj.Transformer.from_crs(
                    "epsg:4326", f"+proj=utm +zone={zone} +{hemisphere}", always_xy=True
                )
                easting, northing = proj_utm.transform(df['longitude'].values, df['latitude'].values)
                df['UTM_E'] = [round(e, 2) for e in easting]
                df['UTM_N'] = [round(n, 2) for n in northing]
                st.dataframe(df[['latitude', 'longitude', 'UTM_E', 'UTM_N']], use_container_width=True)
                st.map(df[['latitude', 'longitude']].dropna())
                st.download_button("📥 Baixar arquivo convertido", df.to_csv(index=False).encode("utf-8"), "convertido.csv", "text/csv")

            elif opcao == "📐 UTM → Geográficas" and "UTM_E" in df.columns and "UTM_N" in df.columns:
                proj_geo = pyproj.Transformer.from_crs("epsg:32724", "epsg:4326", always_xy=True)
                lon, lat = proj_geo.transform(df['UTM_E'].values, df['UTM_N'].values)
                df['longitude'] = [round(lon_, 6) for lon_ in lon]
                df['latitude'] = [round(lat_, 6) for lat_ in lat]
                st.dataframe(df[['latitude', 'longitude', 'UTM_E', 'UTM_N']], use_container_width=True)
                st.map(df[['latitude', 'longitude']].dropna())
                st.download_button("📥 Baixar arquivo convertido", df.to_csv(index=False).encode("utf-8"), "convertido.csv", "text/csv")

            elif opcao == "🧭 GMS → Geográficas":
                need = ['lat_grau','lat_min','lat_seg','lat_dir','lon_grau','lon_min','lon_seg','lon_dir']
                if all(col in df.columns for col in need):
                    def gms_to_decimal(grau, minuto, segundo, direcao):
                        decimal = grau + minuto / 60 + segundo / 3600
                        if direcao in ['S', 'W']: decimal *= -1
                        return decimal
                    df['latitude'] = df.apply(lambda r: gms_to_decimal(r['lat_grau'], r['lat_min'], r['lat_seg'], r['lat_dir']), axis=1)
                    df['longitude'] = df.apply(lambda r: gms_to_decimal(r['lon_grau'], r['lon_min'], r['lon_seg'], r['lon_dir']), axis=1)
                    st.dataframe(df[['latitude','longitude']], use_container_width=True)
                    st.map(df[['latitude','longitude']].dropna())
                    st.download_button("📥 Baixar arquivo convertido", df.to_csv(index=False).encode("utf-8"), "convertido.csv", "text/csv")

else:
    if opcao == "🌍 Geográficas → UTM":
        lat = st.number_input("Latitude (graus decimais)", format="%.6f", key="lat_dec")
        lon = st.number_input("Longitude (graus decimais)", format="%.6f", key="lon_dec")
        if st.button("Converter", key="btn_geo_to_utm"):
            zone = int((lon + 180) / 6) + 1
            hemisphere = "south" if lat < 0 else "north"
            proj_utm = pyproj.Transformer.from_crs("epsg:4326", f"+proj=utm +zone={zone} +{hemisphere}", always_xy=True)
            e, n = proj_utm.transform(lon, lat)
            st.success(f"Resultado UTM — Zona {zone}/{'S' if hemisphere == 'south' else 'N'}:")
            st.write(f"📍 UTM_E: **{round(e, 2)}**  |  UTM_N: **{round(n, 2)}**")
            st.map(pd.DataFrame({'latitude': [lat], 'longitude': [lon]}))

    elif opcao == "📐 UTM → Geográficas":
        e = st.number_input("UTM_E (metros)", format="%.2f", key="utm_e")
        n = st.number_input("UTM_N (metros)", format="%.2f", key="utm_n")
        if st.button("Converter", key="btn_utm_to_geo"):
            proj_geo = pyproj.Transformer.from_crs("epsg:32724", "epsg:4326", always_xy=True)
            lon, lat = proj_geo.transform(e, n)
            st.success("Resultado em Coordenadas Geográficas:")
            st.write(f"🌍 Latitude: **{round(lat, 6)}**  |  Longitude: **{round(lon, 6)}**")
            st.map(pd.DataFrame({'latitude': [lat], 'longitude': [lon]}))

    elif opcao == "🧭 GMS → Geográficas":
        g_lat_deg = st.number_input("Latitude - Graus", value=0, key="lat_grau")
        g_lat_min = st.number_input("Latitude - Minutos", value=0, key="lat_min")
        g_lat_sec = st.number_input("Latitude - Segundos", value=0.0, key="lat_seg")
        g_lat_dir = st.selectbox("Direção da Latitude", ["N", "S"], key="lat_dir")
        g_lon_deg = st.number_input("Longitude - Graus", value=0, key="lon_grau")
        g_lon_min = st.number_input("Longitude - Minutos", value=0, key="lon_min")
        g_lon_sec = st.number_input("Longitude - Segundos", value=0.0, key="lon_seg")
        g_lon_dir = st.selectbox("Direção da Longitude", ["E", "W"], key="lon_dir")
        if st.button("Converter para Decimal", key="btn_gms_to_geo"):
            latitude = g_lat_deg + g_lat_min / 60 + g_lat_sec / 3600
            if g_lat_dir == "S": latitude *= -1
            longitude = g_lon_deg + g_lon_min / 60 + g_lon_sec / 3600
            if g_lon_dir == "W": longitude *= -1
            st.success("Coordenadas Decimais:")
            st.write(f"🌍 Latitude: **{round(latitude, 6)}**  |  Longitude: **{round(longitude, 6)}**")
            st.map(pd.DataFrame({'latitude': [latitude], 'longitude': [longitude]}))













