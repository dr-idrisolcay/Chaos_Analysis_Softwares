import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from io import BytesIO


# Lyapunov üstelini hesaplayan fonksiyon
def lyapunov_exponent(time_series, delta=1e-8):
    n = len(time_series)
    lambda_lyapunov = np.zeros(n)

    for i in range(1, n):
        perturbed_series = time_series[i-1] + delta
        distance = abs(perturbed_series - time_series[i])
        
        if distance > 0:
            lambda_lyapunov[i] = np.log(distance / delta)
    
    return np.mean(lambda_lyapunov), lambda_lyapunov

# Veriyi doğrulayan fonksiyon (Ön işleme adımı)
def validate_and_preprocess_data(df):
    if df.isnull().values.any():
        raise ValueError("Data contains missing values.")
    if len(df.columns) == 0:
        raise ValueError("No valid time series found in the input data.")
    return df

# Zaman serisi üzerinde Lyapunov hesaplama ve sonuçları döndürme
def analyze_time_series(df):
    results = []
    for col in df.columns:
        time_series = df[col].values
        lyapunov_value, lyapunov_series = lyapunov_exponent(time_series)
        is_chaotic = "Evet" if lyapunov_value > 0 else "Hayır"
        results.append({
            "Seri İsmi": col,
            "Lyapunov Üsteli": lyapunov_value,
            "Kaotik mi ?": is_chaotic,
            "Lyapunov Series": lyapunov_series
        })
    return results

# Zaman serisi ve Lyapunov üstel serisi grafiği çizimi
def plot_time_series_and_lyapunov(results, df):
    for result in results:
        series_name = result["Seri İsmi"]
        time_series = df[series_name].values
        lyapunov_series = result["Lyapunov Series"]
        
        # Zaman serisi grafiği
        plt.figure(figsize=(10, 4))
        plt.plot(time_series, label='Time Series')
        plt.title(f"Time Series: {series_name}")
        plt.xlabel("Time Steps")
        plt.ylabel("Value")
        plt.legend()
        st.pyplot(plt)

        # Lyapunov üstel serisi grafiği
        plt.figure(figsize=(10, 4))
        plt.plot(lyapunov_series, color='orange', label='Lyapunov Üsteli Series')
        plt.title(f"Lyapunov Üsteli Series: {series_name}")
        plt.xlabel("Time Steps")
        plt.ylabel("Lyapunov Üsteli")
        plt.legend()
        st.pyplot(plt)

# PDF raporu oluşturma
def create_pdf_report(results):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Başlık
    pdf.set_font("Arial", size=16, style='B')
    pdf.cell(200, 10, txt="Lyapunov Üsteli and Kaos Analiz Raporu", ln=True, align="C")

    # Sonuçları PDF'e yazma
    pdf.set_font("Arial", size=12)
    for result in results:
        series_name = result["Seri İsmi"]
        lyapunov_value = result["Lyapunov Üsteli"]
        is_chaotic = result["Kaotik mi ?"]
        
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Series: {series_name}", ln=True)
        pdf.cell(200, 10, txt=f"Lyapunov Üsteli: {lyapunov_value:.4f}", ln=True)
        pdf.cell(200, 10, txt=f"Kaotik mi ?: {is_chaotic}", ln=True)

    # PDF içeriğini bellekte `BytesIO`ya kaydetme
    pdf_output = BytesIO()
    pdf_output.write(pdf.output(dest='S').encode('latin1'))  # PDF içeriğini dize olarak kaydet ve BytesIO'ya ekle
    pdf_output.seek(0)  # İndirme işlemi için başlangıca getir

    return pdf_output

# Streamlit uygulaması başlıyor
st.header("Lyapunov Üstelinin Hesaplanması")

# CSV dosyası yükleme
uploaded_file = st.file_uploader("CSV dosyasını yükleyiniz", type="csv")

# Dosya yüklendiyse analiz işlemlerini gerçekleştirme
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.write("Uploaded Data:")
    st.write(df)

    # Veriyi doğrulama
    try:
        df = validate_and_preprocess_data(df)
    except ValueError as e:
        st.error(f"Data validation error: {e}")
        st.stop()

    # Lyapunov üstel analizi
    results = analyze_time_series(df)

    # Sonuçları tablo olarak gösterme
    summary_df = pd.DataFrame({
        "Seri İsmi": [result["Seri İsmi"] for result in results],
        "Lyapunov Üsteli": [result["Lyapunov Üsteli"] for result in results],
        "Kaotik mi ?": [result["Kaotik mi ?"] for result in results]
    })
    
    st.write("Lyapunov Üsteli and Kaotik Sonuçları:")
    st.write(summary_df)

    # Grafiksel gösterim
    plot_time_series_and_lyapunov(results, df)

    # PDF rapor oluşturma ve indirme butonu
    pdf_data = create_pdf_report(results)
    st.download_button(
        label="PDF Dosyasını İndir",
        data=pdf_data,
        file_name="lyapunov_report.pdf",
        mime="application/pdf"
    )
