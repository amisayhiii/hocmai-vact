import streamlit as st
import os

st.set_page_config(page_title="HOCMAI VACT Content Assistant", page_icon="📝", layout="wide")

def get_knowledge_files():
    knowledge_dir = "knowledge"
    if os.path.exists(knowledge_dir):
        return [f for f in os.listdir(knowledge_dir) if os.path.isfile(os.path.join(knowledge_dir, f))]
    return []

st.sidebar.title("📌 Menu Quản Trị")
menu = st.sidebar.radio(
    "Chọn phân khu:",
    ["1. Công cụ tạo kế hoạch nội dung", "2. Tạo nội dung cụ thể", "3. Tài liệu về kỳ thi"]
)

st.sidebar.divider()
st.sidebar.subheader("💰 Chi phí Token (Tạm tính)")
st.sidebar.info("Phiên hiện tại: $0.00\n\nQuy đổi: 0 VNĐ")

if menu == "1. Công cụ tạo kế hoạch nội dung":
    st.title("📅 Công cụ tạo kế hoạch nội dung")
    st.markdown("Xây dựng lộ trình bài viết chuẩn tỷ lệ 80% học thuật - 20% thương hiệu dành cho lứa 2k9.")
    with st.form("plan_form"):
        col1, col2 = st.columns(2)
        with col1:
            timeframe = st.text_input("Khoảng thời gian (VD: Tuần 1 tháng 6/2026)")
        with col2:
            target_audience = st.text_input("Mục tiêu trọng tâm (VD: Khởi động Lộ trình S)")
        submit_plan = st.form_submit_button("Phân tích & Lên kế hoạch")
    if submit_plan:
        st.success("Đang phân tích dữ liệu kho tài liệu và khởi tạo ma trận lịch trình nội dung...")

elif menu == "2. Tạo nội dung cụ thể":
    st.title("✍️ Tạo nội dung cụ thể")
    
    col_left, col_right = st.columns([1, 1], gap="large")
    
    with col_left:
        st.subheader("📥 Nhập yêu cầu")
        topic = st.text_area("1. Chủ đề", placeholder="Nhập chủ đề hoặc thông điệp cốt lõi...")
        
        speaker = st.selectbox("2. Người phát ngôn", ["Giáo viên", "Chuyên gia GD", "Học sinh", "Phụ huynh"])
        
        audience_choice = st.selectbox("3. Đối tượng hướng đến", ["học sinh 2k9", "phụ huynh 2k9", "Khác"])
        if audience_choice == "Khác":
            audience = st.text_input("Nhập đối tượng khác:")
        else:
            audience = audience_choice
            
        format_choice = st.selectbox("4. Định dạng", ["Caption FB", "Video script", "Short comment", "Long-form content", "Khác"])
        if format_choice == "Khác":
            format_type = st.text_input("Nhập định dạng khác:")
        else:
            format_type = format_choice
            
        other_req = st.text_area("5. Yêu cầu khác", placeholder="Tone, mood, hoặc dán một đoạn văn mẫu để AI bắt chước văn phong...")
        
        st.caption("Ràng buộc hệ thống: Hook sắc bén, 80% học thuật - 20% thương hiệu, Văn xuôi (không gạch đầu dòng), Đã qua kiểm duyệt Logic.")
        
        generate_btn = st.button("TẠO NỘI DUNG", type="primary", use_container_width=True)

    with col_right:
        # Sử dụng columns để căn nút bấm lên trên cùng bên phải, ngang hàng với subheader
        header_col1, header_col2, header_col3 = st.columns([5, 2, 2])
        with header_col1:
            st.subheader("📤 Nội dung chi tiết")
            
        if generate_btn:
            if topic:
                with header_col2:
                    st.button("TẠO LẠI", use_container_width=True)
                with header_col3:
                    st.button("COPY", use_container_width=True)
                    
                with st.spinner("Đang phân tích logic và khởi tạo bản thảo..."):
                    result_text = "Đây là khu vực hiển thị bản thảo sau khi hệ thống đã hoàn tất việc trích xuất ý tưởng và tự động rà soát chéo về ngữ pháp cũng như logic. Nội dung tại đây đảm bảo bám sát các tiêu chí khắt khe của chiến dịch Lộ trình S, duy trì cấu trúc văn xuôi liền mạch hoàn toàn không sử dụng định dạng gạch đầu dòng."
                    st.text_area("Kết quả:", value=result_text, height=380, label_visibility="collapsed")
            else:
                st.warning("Vui lòng nhập Chủ đề để hệ thống có cơ sở xử lý.")
        else:
            st.info("Bản thảo hoàn thiện sẽ hiển thị tại đây sau khi bạn bấm TẠO NỘI DUNG.")

elif menu == "3. Tài liệu về kỳ thi":
    st.title("📚 Tài liệu về kỳ thi & Chi phí")
    files = get_knowledge_files()
    if files:
        st.write("### Danh sách tài liệu hiện có")
        for f in files:
            st.markdown(f"- `{f}`")
    else:
        st.info("Chưa có tài liệu nào trong thư mục `knowledge`.")
    st.divider()
    st.write("### 📊 Báo cáo tiêu thụ Token")
    st.write("Hệ thống sẽ cập nhật tự động chi phí sử dụng AI tại đây dựa trên tỷ giá $1 = 27,000 VNĐ.")