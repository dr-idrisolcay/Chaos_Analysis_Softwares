import streamlit as st

st.sidebar.image("img/Chaos_Analysis.jpg", caption="'Çin'de kelebek kanat çırptığında Atlantik'te fırtına çıkar.' (James Gleick)", use_column_width=True)
st.header("Uygulanan Kaos Analiz Yazılım Formülleri")


# Lyapunov üstel hesaplamaları için Türkçe değişkenler
st.subheader("1-Lyapunov Üsteli")

# İki sütun oluştur
col1, col2 = st.columns(2)

# Birinci sütuna formülleri yaz
with col1:
    st.latex(r"\lambda_i = \ln\left(\frac{|x_{i-1} + \delta - x_i|}{\delta}\right)")  # Anlık Lyapunov üstel formülü
    st.latex(r"\lambda_{\text{lyapunov}} = \frac{1}{N} \sum_{i=1}^{N} \lambda_i")  # Ortalama Lyapunov üstel formülü

# İkinci sütuna açıklamaları yaz
with col2:
    st.write("### Değişken Açıklamaları")
    st.write("""
    - **λₖ**: Anlık Lyapunov üstel değeri  
    - **λₗ**: Ortalama Lyapunov üstel değeri  
    - **xₖ**: \(k\)-inci zamandaki nokta  
    - **xₖ₋₁**: Bir önceki zamandaki nokta  
    - **δ**: Başlangıçta iki noktadan alınan küçük uzaklık  
    - **N**: Toplam örnek sayısı  
    """)

