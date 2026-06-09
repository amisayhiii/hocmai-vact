import streamlit as st
import os
import google.generativeai as genai

# Cấu hình API Key từ Streamlit Secrets
if 'GEMINI_API_KEY' in st.secrets:
    genai.configure(api_key=st.secrets['GEMINI_API_KEY'])


st.set_page_config(page_title="HOCMAI VACT Content Assistant", page_icon="📝", layout="wide")


def generate_gemini_content(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Lỗi khi gọi API: {str(e)}"

def get_knowledge_files():
    knowledge_dir = "knowledge"
    if os.path.exists(knowledge_dir):
        return [f for f in os.listdir(knowledge_dir) if os.path.isfile(os.path.join(knowledge_dir, f))]
    return []

st.sidebar.title("📌 Menu Quản Trị")
menu = st.sidebar.radio(
    "Chọn phân khu:",
    ["1. Lên ý tưởng nội dung", "2. Tạo nội dung cụ thể", "3. Thông tin kỳ thi VACT"]
)

# st.sidebar.divider()
# st.sidebar.subheader("💰 Chi phí Token (Tạm tính)")
# total_usd = st.session_state.get('total_usd', 0.0)
# total_vnd = st.session_state.get('total_vnd', 0)
# st.sidebar.info(f"Phiên hiện tại: ${total_usd:.4f}\n\nQuy đổi: {int(total_vnd):,} VNĐ")

if menu == "1. Lên ý tưởng nội dung":
    st.title("📅 Lên ý tưởng nội dung")
    st.markdown("Xây dựng lộ trình bài viết chuẩn tỷ lệ 80% học thuật - 20% thương hiệu dành cho lứa 2k9.")
    with st.form("plan_form"):
        col1, col2 = st.columns(2)
        with col1:
            timeframe = st.text_input("Khoảng thời gian (VD: Tuần 1 tháng 6/2026)")
        with col2:
            target_audience = st.text_input("Mục tiêu trọng tâm (VD: Khởi động Lộ trình S)")
        submit_plan = st.form_submit_button("Phân tích & Lên kế hoạch")
    if submit_plan:
        if not timeframe or not target_audience:
            st.warning("Vui lòng nhập đủ Khoảng thời gian và Mục tiêu trọng tâm!")
        else:
            with st.spinner("Đang phân tích dữ liệu kho tài liệu và khởi tạo ma trận lịch trình nội dung..."):
                prompt = f"Lập kế hoạch nội dung truyền thông cho kỳ thi VACT. Thời gian: {timeframe}. Mục tiêu: {target_audience}. Yêu cầu: Tỷ lệ 80% học thuật - 20% thương hiệu dành cho lứa 2k9."
                st.session_state['plan_result'] = generate_gemini_content(prompt)
                
    if 'plan_result' in st.session_state:
        st.markdown("### Kết quả kế hoạch:")
        st.write(st.session_state['plan_result'])

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
        
        st.caption("Ràng buộc hệ thống: Hook sắc bén, 80% học thuật - 20% thương hiệu, Đã qua kiểm duyệt Logic.")
        
        generate_btn = st.button("TẠO NỘI DUNG", type="primary", use_container_width=True)

    with col_right:
        # Sử dụng columns để căn nút bấm lên trên cùng bên phải, ngang hàng với subheader
        header_col1, header_col2, header_col3 = st.columns([5, 2, 2])
        with header_col1:
            st.subheader("📤 Nội dung chi tiết")
            
        if generate_btn:
            if topic:
                with st.spinner("Đang phân tích logic và khởi tạo bản thảo qua Gemini..."):
                    prompt = f"Hãy viết một nội dung truyền thông với các tiêu chí sau:\n1. Chủ đề: {topic}\n2. Người phát ngôn: {speaker}\n3. Đối tượng hướng đến: {audience}\n4. Định dạng: {format_type}\n5. Yêu cầu khác: {other_req}\n\nRàng buộc: Hook sắc bén, 80% học thuật - 20% thương hiệu."
                    st.session_state['content_result'] = generate_gemini_content(prompt)
            else:
                st.warning("Vui lòng nhập Chủ đề để hệ thống có cơ sở xử lý.")
                
        if 'content_result' in st.session_state:
            with header_col2:
                if st.button("TẠO LẠI", use_container_width=True):
                    with st.spinner("Đang tạo lại bản thảo..."):
                        prompt = f"Hãy viết một nội dung truyền thông với các tiêu chí sau:\n1. Chủ đề: {topic}\n2. Người phát ngôn: {speaker}\n3. Đối tượng hướng đến: {audience}\n4. Định dạng: {format_type}\n5. Yêu cầu khác: {other_req}\n\nRàng buộc: Hook sắc bén, 80% học thuật - 20% thương hiệu."
                        st.session_state['content_result'] = generate_gemini_content(prompt)
                        st.rerun()
            with header_col3:
                # Copy button is mainly visual in Streamlit without custom components, 
                # but users can copy from the text_area
                st.button("COPY", use_container_width=True)
                
            st.text_area("Kết quả:", value=st.session_state['content_result'], height=380, label_visibility="collapsed")
        else:
            st.info("Bản thảo hoàn thiện sẽ hiển thị tại đây sau khi bạn bấm TẠO NỘI DUNG.")

elif menu == "3. Thông tin kỳ thi VACT":
    st.title("🎯 Thông tin kỳ thi V-ACT (ĐGNL ĐHQG-HCM)")
    st.markdown("---")
    
    # Giới thiệu & Hình thức
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Giới thiệu ngắn gọn:**\nKỳ thi Đánh giá Năng lực (V-ACT) do ĐHQG-HCM tổ chức nhằm đánh giá các năng lực cơ bản để học tập đại học của thí sinh như: sử dụng ngôn ngữ, tư duy logic, xử lý số liệu và giải quyết vấn đề.")
    with col2:
        st.success("**Hình thức thi & Lệ phí:**\n- Hình thức: Trắc nghiệm khách quan trên giấy (120 câu hỏi/150 phút).\n- Lệ phí thi: Khoảng 300.000 VNĐ/lượt (theo mức chuẩn các năm).")
        
    # Thời gian tổ chức & Điểm thi
    col3, col4 = st.columns(2)
    with col3:
        st.warning("**Thời gian tổ chức:**\nThường có 2 đợt/năm:\n- Đợt 1: Cuối tháng 3 / đầu tháng 4.\n- Đợt 2: Cuối tháng 5 / đầu tháng 6.")
    with col4:
        st.error("**Điểm thi:**\n- Thang điểm tối đa: 1.200 điểm.\n- Chấm điểm bằng phương pháp trắc nghiệm hiện đại (Lý thuyết Ứng đáp Câu hỏi - IRT), câu khó sẽ có trọng số cao hơn câu dễ.")

    st.markdown("### 📊 Cấu trúc đề thi & Chuyên đề trọng tâm")
    tab1, tab2, tab3 = st.tabs(["Phần 1: Ngôn ngữ", "Phần 2: Toán học & Logic", "Phần 3: Giải quyết vấn đề"])
    
    with tab1:
        st.markdown("""
        **Sử dụng ngôn ngữ (40 câu):**
        - *Tiếng Việt (20 câu):* Đọc hiểu văn bản, ngữ pháp, từ vựng, tác giả tác phẩm, phát hiện lỗi sai trong câu.
        - *Tiếng Anh (20 câu):* Từ vựng, ngữ pháp, đọc hiểu đoạn văn, nhận diện lỗi sai.
        """)
    with tab2:
        st.markdown("""
        **Toán học, Tư duy logic, Phân tích số liệu (30 câu):**
        - *Toán học (10 câu):* Đại số, Hình học, Giải tích, Tổ hợp - Xác suất.
        - *Tư duy logic (10 câu):* Suy luận logic từ các mệnh đề, dữ kiện cho trước.
        - *Phân tích số liệu (10 câu):* Đọc hiểu biểu đồ (tròn, cột, đường), bảng số liệu, tính toán thống kê cơ bản.
        """)
    with tab3:
        st.markdown("""
        **Giải quyết vấn đề (50 câu):**
        - *Khoa học tự nhiên:* Hóa học (10 câu), Vật lý (10 câu), Sinh học (10 câu). Thường tập trung vào lý thuyết nền tảng, bài tập thực hành và ứng dụng.
        - *Khoa học xã hội:* Địa lý (10 câu), Lịch sử (10 câu). Phân tích sự kiện lịch sử, đọc hiểu Atlat, biểu đồ địa lý.
        """)
        
    st.markdown("---")
    
    # Phổ điểm thi
    st.markdown("### 📈 Phổ điểm thi 2025 và 2026")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.metric(label="Phổ điểm trung bình 2025", value="~680 - 720", delta="Số liệu tham khảo")
    with col_p2:
        st.metric(label="Phổ điểm trung bình 2026", value="Đang cập nhật...", delta="Chưa có dữ liệu chính thức đợt thi", delta_color="off")
        
    st.markdown("---")
    
    # Các thông tin khác dùng expander
    st.markdown("### 📌 Thông tin mở rộng")
    
    with st.expander("🎓 Các trường xét điểm thi ĐGNL ĐHQG-HCM"):
        st.write("""
        Hơn 100 trường Đại học, Cao đẳng trên cả nước sử dụng kết quả kỳ thi này để xét tuyển, bao gồm:
        - **Hệ thống ĐHQG-HCM:** ĐH Bách Khoa, ĐH KHTN, ĐH KHXH&NV, ĐH Kinh tế - Luật, ĐH Quốc tế, ĐH CNTT, v.v.
        - **Các trường ngoài hệ thống:** ĐH Kinh tế TP.HCM (UEH), ĐH Công nghiệp TP.HCM, ĐH Ngân hàng, ĐH Ngoại thương (Cơ sở 2),...
        """)
        
    with st.expander("⚠️ Các lưu ý khác cho thí sinh"):
        st.write("""
        - **Giấy tờ:** Bắt buộc mang theo CMND/CCCD/Hộ chiếu hợp lệ và Giấy báo dự thi (bản in).
        - **Vật dụng:** Chỉ mang bút chì (2B khuyên dùng), bút bi, tẩy, Atlat Địa lý VN (không có nét viết thêm), máy tính bỏ túi theo quy định.
        - **Thời gian:** Làm bài liên tục 150 phút, không có thời gian nghỉ giải lao giữa các phần.
        """)
        
    with st.expander("❓ Một số câu hỏi thường gặp (FAQs)"):
        st.markdown("""
        **Q: Có thể đăng ký thi cả 2 đợt không?**  
        A: Có. Thí sinh có thể thi cả 2 đợt, hệ thống xét tuyển sẽ tự động lấy kết quả của đợt thi có điểm cao nhất.
        
        **Q: Kỳ thi có bắt học thuộc lòng nhiều không?**  
        A: Không. Kỳ thi V-ACT chú trọng vào việc đánh giá năng lực tư duy, xử lý số liệu và kỹ năng giải quyết vấn đề hơn là việc ghi nhớ máy móc.
        
        **Q: Điểm bài thi được tính như thế nào?**  
        A: Không phải mỗi câu đều có điểm bằng nhau (ví dụ 10 điểm/câu). Điểm được tính theo thuật toán IRT, câu hỏi khó có ít người làm được sẽ có trọng số điểm cao hơn câu dễ.
        """)
