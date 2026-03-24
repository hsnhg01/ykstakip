import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time
import plotly.express as px
import random
import os

# 1. AYARLAR VE TASARIM
st.set_page_config(page_title="Hasan Hüseyin 10K Pro", layout="wide", page_icon="⚖️")

st.markdown("""
<style>

/* GENEL */
.stApp {
    background: radial-gradient(circle at top left, #0f172a, #020617);
    color: #f1f5f9;
    font-family: 'Segoe UI', sans-serif;
}

/* HERO */
.hero-section {
    background: linear-gradient(135deg, #1d4ed8, #7c3aed);
    padding: 35px;
    border-radius: 30px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 0 40px rgba(124,58,237,0.6);
    backdrop-filter: blur(12px);
}

/* METRIC KART */
.metric-box {
    background: rgba(30,41,59,0.6);
    padding: 15px;
    border-radius: 15px;
    border: 1px solid rgba(59,130,246,0.5);
    box-shadow: 0 0 15px rgba(59,130,246,0.3);
    text-align: center;
    font-weight: bold;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #1e293b);
}

/* BUTONLAR */
.stButton>button {
    border-radius: 15px;
    padding: 10px 20px;
    font-weight: bold;
    border: none;
    background: linear-gradient(90deg, #3b82f6, #7c3aed);
    color: white;
    transition: 0.3s ease-in-out;
    box-shadow: 0 0 15px rgba(59,130,246,0.6);
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 25px rgba(124,58,237,0.8);
}

/* INPUT */
.stTextInput>div>div>input,
.stNumberInput input,
.stSelectbox>div>div>div {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 12px !important;
}

/* TAB */
.stTabs [data-baseweb="tab"] {
    font-size: 18px;
    font-weight: 600;
    padding: 10px;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg,#3b82f6,#7c3aed);
    border-radius: 12px;
    color: white !important;
}

/* XP BAR */
.xp-bar {
    background: #1e293b;
    border-radius: 20px;
    height: 22px;
    width: 100%;
    margin: 12px 0;
    box-shadow: inset 0 0 10px rgba(0,0,0,0.6);
}

.xp-fill {
    background: linear-gradient(90deg, #facc15, #fb923c);
    height: 22px;
    border-radius: 20px;
    text-align: center;
    color: black;
    font-weight: bold;
    font-size: 12px;
    box-shadow: 0 0 15px rgba(251,146,60,0.7);
}

/* DATA EDITOR */
[data-testid="stDataEditor"] {
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 0 25px rgba(59,130,246,0.3);
}

/* ALT FOOTER */
.footer {
    text-align: right;
    opacity: 0.4;
    font-size: 11px;
    margin-top: 60px;
}

</style>
""", unsafe_allow_html=True)

# VERİ FONKSİYONLARI (KORUNAN YAPI)
def veri_yukle(dosya, sutunlar):
    try: 
        df = pd.read_csv(dosya)
        if len(df.columns) != len(sutunlar): return pd.DataFrame(columns=sutunlar)
        return df
    except: return pd.DataFrame(columns=sutunlar)

def guvenli_plan_yukle(dosya, beklenen_sutunlar):
    if not os.path.exists(dosya): return pd.DataFrame(columns=beklenen_sutunlar)
    try:
        df = pd.read_csv(dosya)
        if len(df.columns) != len(beklenen_sutunlar): return pd.DataFrame(columns=beklenen_sutunlar)
        return df
    except: return pd.DataFrame(columns=beklenen_sutunlar)

# 2. VERİLERİ ÇEK VE XP HESAPLA
# Sütunları yeni özelliklere göre güncelledik (Hata almamak için eski dosyaları bir kez silmen gerekebilir)
c_sutunlar = ["Tarih", "Ders", "Süre (dk)", "Not", "XP"]
d_sutunlar = ["Tarih", "Tür", "Branş Dağılımı", "Toplam Net", "Süre (dk)", "Analiz", "Hata Nedeni"]
k_sutunlar = ["Ders", "Konu", "Tamamlandı", "Bitirme Tarihi"]

df_calisma = veri_yukle("yks_verileri.csv", c_sutunlar)
df_deneme = veri_yukle("yks_deneme.csv", d_sutunlar)
df_konu = veri_yukle("yks_konu_takip.csv", k_sutunlar)

# XP Hesaplama
toplam_xp = (df_calisma["XP"].sum() if not df_calisma.empty else 0) + (df_deneme["Toplam Net"].sum() * 10 if not df_deneme.empty else 0)
gunluk_xp = df_calisma[df_calisma["Tarih"] == datetime.now().strftime("%d/%m")]["XP"].sum() if not df_calisma.empty else 0
xp_hedef = 500
xp_oran = min(gunluk_xp / xp_hedef, 1.0)

# 3. SIDEBAR (YENİ EKİPmanLAR)
with st.sidebar:
    st.title("🎖️ COMMANDER")
    st.write(f"**Hasan Hüseyin (Elite EA)**")
    st.metric("Toplam Tecrübe (XP)", int(toplam_xp))
    st.write(f"Günlük XP Hedefi: {int(gunluk_xp)}/{xp_hedef}")
    st.markdown(f'<div class="xp-bar"><div class="xp-fill" style="width:{xp_oran*100}%">{int(xp_oran*100)}%</div></div>', unsafe_allow_html=True)
    
    st.divider()
    # Yaratıcı Özellik: Şanslı Bilgi
    if st.button("🎲 Şanslı Bilgi Al"):
        bilgiler = [
            "💡 Edebiyat: Servetifünun'un en önemli şairi Tevfik Fikret'tir.",
            "💡 Matematik: Türev, bir fonksiyonun değişim hızıdır.",
            "💡 Tarih: 1. TBMM 23 Nisan 1920'de açılmıştır.",
            "💡 Coğrafya: Türkiye'nin en uzun kıyı şeridi Ege Bölgesi'ndedir.",
            "💡 Edebiyat: Saf şiir anlayışının temsilcileri arasında Ahmet Haşim yer alır."
        ]
        st.info(random.choice(bilgiler))

    # Hayalet Rakip
    if not df_calisma.empty:
        ortalama = df_calisma["Süre (dk)"].mean()
        st.write(f"👤 **Hayalet Rakip:** {int(ortalama)} dk/gün")
        if gunluk_xp > (ortalama * 2): st.success("🔥 Kendi rekorunu kırıyorsun!")

# 4. ÜST PANEL
yks_tarihi = datetime(2026, 6, 20, 10, 0, 0)
simdi = datetime.now()
kalan = yks_tarihi - simdi

st.markdown(f"""
    <div class="hero-section">
        <h1 style='margin:0;'>HASAN HÜSEYİN v6.0</h1>
        <p style='font-size:18px; opacity:0.9;'>🎯</p>
        <p style='font-family:monospace; color:#fbbf24; font-size:20px;'>{simdi.strftime('%H:%M:%S')} | YKS'ye {kalan.days} GÜN KALDI</p>
    </div>
    """, unsafe_allow_html=True)

branslar = ["TYT Türkçe", "TYT Matematik", "TYT Sosyal", "TYT Fen", "AYT Edebiyat", "AYT Matematik", "AYT Tarih", "AYT Coğrafya"]
tab1, tab2, tab_plan, tab3, tab4 = st.tabs(["⚡ ODAK MODU", "🏆 DENEME MERKEZİ", "📅 HAFTALIK PLAN", "✅ KONU TAKİBİ", "📈 ANALİZ"])

# --- TAB 1: ODAK MODU ---
with tab1:
    st.subheader("⏱️ Çalışma Modu")
    c1, c2 = st.columns([1, 1])
    with c1:
        ders_k = st.selectbox("Ders Seç", branslar, key="odak_ders")
        if 'active' not in st.session_state: st.session_state.active = False
        if not st.session_state.active:
            if st.button("▶️ BAŞLAT", use_container_width=True):
                st.session_state.start = time.time(); st.session_state.active = True; st.rerun()
        else:
            if st.button("⏹️ BİTİR VE KAYDET", use_container_width=True):
                gecen = round((time.time() - st.session_state.start) / 60, 1)
                st.session_state.last_s = gecen; st.session_state.active = False; st.session_state.ask_note = True; st.rerun()
            st.warning(f"⚡ {ders_k} üzerine odaklanıyorsun...")
    with c2:
        if st.session_state.get('ask_note', False):
            n_k = st.text_input(f"✅ {st.session_state.last_s} dk bitti. Bugün neler yaptın?")
            if st.button("Kayıt Defterine Ekle"):
                kazanilan_xp = st.session_state.last_s * 2
                yeni = {"Tarih": datetime.now().strftime("%d/%m"), "Ders": ders_k, "Süre (dk)": st.session_state.last_s, "Not": n_k, "XP": kazanilan_xp}
                df_calisma = pd.concat([df_calisma, pd.DataFrame([yeni])], ignore_index=True)
                df_calisma.to_csv("yks_verileri.csv", index=False); st.session_state.ask_note = False; st.rerun()
    st.divider()
    edit_cal = st.data_editor(df_calisma, use_container_width=True, num_rows="dynamic", hide_index=True)
    if not edit_cal.equals(df_calisma): edit_cal.to_csv("yks_verileri.csv", index=False)

# --- TAB 2: DENEME MERKEZİ ---
with tab2:
    st.subheader("📊 Deneme Sonuç Analizi")
    d_tur = st.selectbox("Deneme Türü", ["Genel TYT Denemesi", "Genel AYT Denemesi", "Branş Denemesi"])
    with st.container():
        top_net = 0.0; dagilim = ""; top_sure = 0
        # TYT / AYT Seçenekleri senin orijinal mantığında kaldı...
        if d_tur == "Genel TYT Denemesi":
            c1, c2, c3, c4 = st.columns(4)
            tr_d = c1.number_input("TR D", 0, 40); tr_y = c1.number_input("TR Y", 0, 40)
            tr_net = tr_d - (tr_y * 0.25); c1.markdown(f"<div class='metric-box'>{tr_net} Net</div>", unsafe_allow_html=True)
            mt_d = c2.number_input("MAT D", 0, 40); mt_y = c2.number_input("MAT Y", 0, 40)
            mt_net = mt_d - (mt_y * 0.25); c2.markdown(f"<div class='metric-box'>{mt_net} Net</div>", unsafe_allow_html=True)
            ss_d = c3.number_input("SOS D", 0, 20); ss_y = c3.number_input("SOS Y", 0, 20)
            ss_net = ss_d - (ss_y * 0.25); c3.markdown(f"<div class='metric-box'>{ss_net} Net</div>", unsafe_allow_html=True)
            fn_d = c4.number_input("FEN D", 0, 20); fn_y = c4.number_input("FEN Y", 0, 20)
            fn_net = fn_d - (fn_y * 0.25); c4.markdown(f"<div class='metric-box'>{fn_net} Net</div>", unsafe_allow_html=True)
            top_net = tr_net + mt_net + ss_net + fn_net
            dagilim = f"TR:{tr_net}|MT:{mt_net}|SS:{ss_net}|FN:{fn_net}"
            top_sure = st.number_input("Toplam Süre (dk)", value=165)
        elif d_tur == "Genel AYT Denemesi":
            c1, c2, c3, c4 = st.columns(4)
            am_d = c1.number_input("MAT D", 0, 40); am_y = c1.number_input("MAT Y", 0, 40)
            am_net = am_d - (am_y * 0.25); c1.markdown(f"<div class='metric-box'>{am_net} Net</div>", unsafe_allow_html=True)
            ed_d = c2.number_input("EDB D", 0, 24); ed_y = c2.number_input("EDB Y", 0, 24)
            ed_net = ed_d - (ed_y * 0.25); c2.markdown(f"<div class='metric-box'>{ed_net} Net</div>", unsafe_allow_html=True)
            t_d = c3.number_input("TAR D", 0, 10); t_y = c3.number_input("TAR Y", 0, 10)
            t_net = t_d - (t_y * 0.25); c3.markdown(f"<div class='metric-box'>{t_net} Net</div>", unsafe_allow_html=True)
            cg_d = c4.number_input("COĞ D", 0, 6); cg_y = c4.number_input("COĞ Y", 0, 6)
            cg_net = cg_d - (cg_y * 0.25); c4.markdown(f"<div class='metric-box'>{cg_net} Net</div>", unsafe_allow_html=True)
            top_net = am_net + ed_net + t_net + cg_net
            dagilim = f"MAT:{am_net}|EDB:{ed_net}|TAR:{t_net}|COĞ:{cg_net}"
            top_sure = st.number_input("Toplam Süre (dk)", value=180)
        elif d_tur == "Branş Denemesi":
            c1, c2, c3, c4 = st.columns(4)
            br = c1.selectbox("Branş", branslar)
            d = c2.number_input("D", 0); y = c3.number_input("Y", 0)
            top_sure = c4.number_input("Süre (dk)", 0)
            top_net = d - (y * 0.25); dagilim = f"{br}: {top_net} Net"

        st.markdown(f"### 🏆 Toplam Sonuç: <span style='color:#fbbf24;'>{top_net:.2f} Net</span>", unsafe_allow_html=True)
        hata_n = st.selectbox("Hata Nedeni?", ["Bilgi Eksikliği", "Dikkat Hatası", "Süre Yetmedi", "İşlem Hatası"])
        analiz = st.text_area("Hasan Hüseyin'in Notu")
        
        if st.button("Denemeyi Analize Kaydet", use_container_width=True):
            yeni = {"Tarih": datetime.now().strftime("%d/%m"), "Tür": d_tur, "Branş Dağılımı": dagilim, "Toplam Net": top_net, "Süre (dk)": top_sure, "Analiz": analiz, "Hata Nedeni": hata_n}
            df_deneme = pd.concat([df_deneme, pd.DataFrame([yeni])], ignore_index=True)
            df_deneme.to_csv("yks_deneme.csv", index=False); st.rerun()
    st.divider()
    st.data_editor(df_deneme, use_container_width=True, num_rows="dynamic", hide_index=True)

# --- TAB: HAFTALIK PLAN (TAMAMEN KORUNDU) ---
with tab_plan:
    st.subheader("📅 Haftalık Çalışma Programın")
    c_set = st.columns(5)
    h1 = c_set[0].text_input("1. Periyot", "08:00-10:00")
    h2 = c_set[1].text_input("2. Periyot", "10:30-12:30")
    h3 = c_set[2].text_input("3. Periyot", "13:30-15:30")
    h4 = c_set[3].text_input("4. Periyot", "16:00-18:00")
    h5 = c_set[4].text_input("5. Periyot", "20:00-22:00")

    plan_sutunlar = ["Tarih/Gün", h1, h2, h3, h4, h5, "⏱️ Toplam Saat", "Günün Notu"]
    df_plan = guvenli_plan_yukle("yks_haftalik_plan.csv", plan_sutunlar)
    
    if df_plan.empty:
        baslangic = datetime(2026, 2, 23)
        gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        tarih_listesi = [f"{(baslangic + timedelta(days=i)).strftime('%d.%m')} {gunler[i%7]}" for i in range(14)]
        df_plan = pd.DataFrame(columns=plan_sutunlar)
        df_plan["Tarih/Gün"] = tarih_listesi
        df_plan = df_plan.fillna("")

    df_plan.columns = plan_sutunlar 
    edit_plan = st.data_editor(df_plan, use_container_width=True, hide_index=True, key="h_plan_editor")
    if not edit_plan.equals(df_plan):
        edit_plan.to_csv("yks_haftalik_plan.csv", index=False)
        st.toast("Plan Kaydedildi! ✅")

# --- TAB 3: KONU TAKİBİ ---
with tab3:
    st.subheader("✅ Eşit Ağırlık Konu Listesi")
    if df_konu.empty:
        ea_mufredat = [("AYT Edebiyat", "Şiir Bilgisi"), ("AYT Matematik", "Logaritma"), ("AYT Tarih", "Milli Mücede")]
        df_konu = pd.DataFrame([{"Ders": x[0], "Konu": x[1], "Tamamlandı": False, "Bitirme Tarihi": "-"} for x in ea_mufredat])
    edit_konu = st.data_editor(df_konu, use_container_width=True, num_rows="dynamic", hide_index=True)
    if not edit_konu.equals(df_konu): edit_konu.to_csv("yks_konu_takip.csv", index=False)
    biten = edit_konu[edit_konu["Tamamlandı"] == True].shape[0]
    toplam = len(edit_konu); st.progress(biten/toplam if toplam > 0 else 0)

# --- TAB 4: ANALİZ (GELİŞTİRİLDİ) ---
with tab4:
    if not df_deneme.empty:
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(px.line(df_deneme, x="Tarih", y="Toplam Net", color="Tür", markers=True, template="plotly_dark", title="Net Gelişimi"), use_container_width=True)
        with c2:
            st.plotly_chart(px.pie(df_deneme, names="Hata Nedeni", template="plotly_dark", title="Neden Kaçırıyoruz?", hole=0.3), use_container_width=True)
    
    if not df_calisma.empty:
        st.divider()
        st.plotly_chart(px.bar(df_calisma, x="Ders", y="Süre (dk)", color="Ders", template="plotly_dark", title="Ders Bazlı Toplam Çalışma"), use_container_width=True)

st.markdown("<div style='text-align: right; opacity: 0.3; font-size: 10px; margin-top:50px;'>Hasan Hüseyin v6.0 Commander | Elite Edition</div>", unsafe_allow_html=True)
time.sleep(1)
st.rerun()
