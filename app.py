import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET
from io import BytesIO

st.title("📄 Trích xuất hóa đơn XML")

uploaded_files = st.file_uploader("📤 Tải lên hóa đơn XML", type="xml", accept_multiple_files=True)

if uploaded_files:
    data = []

    for uploaded_file in uploaded_files:
        tree = ET.parse(uploaded_file)
        root = tree.getroot()

        kyhieu_mauso = root.findtext(".//KHMSHDon")
        kyhieu_hoadon = root.findtext(".//KHHDon")
        so_hoadon = root.findtext(".//SHDon")

        # Chuyển ngày hóa đơn sang dd/MM/yyyy
        ngay_hoadon_raw = root.findtext(".//NLap")
        if ngay_hoadon_raw:
            ngay_hoadon = pd.to_datetime(ngay_hoadon_raw).strftime("%d/%m/%Y")
        else:
            ngay_hoadon = ""

        ten_benban = root.findtext(".//NBan/Ten")
        mst_benban = root.findtext(".//NBan/MST")
        stk_benban = root.findtext(".//NBan/STKNHang")

        tong_tien = root.findtext(".//TToan/TgTCThue")

        data.append({
            "Tên file": uploaded_file.name,
            "Mã số thuế bên bán": mst_benban,
            "Tên bên bán": ten_benban,
            "Số tài khoản bên bán": stk_benban,
            "Ký hiệu mẫu số HĐ": kyhieu_mauso,
            "Ký hiệu hóa đơn": kyhieu_hoadon,
            "Số hóa đơn": so_hoadon,
            "Ngày hóa đơn": ngay_hoadon,
            "Số tiền hóa đơn (chưa VAT)": tong_tien
        })

    df = pd.DataFrame(data)
    st.dataframe(df)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    st.download_button(
        label="📥 Tải file Excel",
        data=output.getvalue(),
        file_name="ThongTinHoaDon.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("📤 Vui lòng upload file hóa đơn XML")
