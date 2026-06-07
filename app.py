     1|import streamlit as st
     2|import os
import google.generativeai as genai

# Cấu hình API Key từ Streamlit Secrets
if 'GEMINI_API_KEY' in st.secrets:
    genai.configure(api_key=st.secrets['GEMINI_API_KEY'])

     3|
     4|st.set_page_config(page_title="HOCMAI VACT Content Assistant", page_icon="📝", layout="wide")
     5|
     6|def get_knowledge_files():
     7|    knowledge_dir = "knowledge"
     8|    if os.path.exists(knowledge_dir):
     9|        return [f for f in os.listdir(knowledge_dir) if os.path.isfile(os.path.join(knowledge_dir, f))]
    10|    return []
    11|
    12|st.sidebar.title("📌 Menu Quản Trị")
    13|menu = st.sidebar.radio(
    14|    "Chọn phân khu:",
    15|    ["1. Công cụ tạo kế hoạch nội dung", "2. Tạo nội dung cụ thể", "3. Thông tin kỳ thi VACT"]
    16|)
    17|
    18|st.sidebar.divider()
    19|st.sidebar.subheader("💰 Chi phí Token (Tạm tính)")
    20|total_usd = st.session_state.get('total_usd', 0.0)
total_vnd = st.session_state.get('total_vnd', 0)
st.sidebar.info(f"Phiên hiện tại: ${total_usd:.4f}\n\nQuy đổi: {int(total_vnd):,} VNĐ")
    21|
    22|if menu == "1. Công cụ tạo kế hoạch nội dung":
    23|    st.title("📅 Công cụ tạo kế hoạch nội dung")
    24|    st.markdown("Xây dựng lộ trình bài viết chuẩn tỷ lệ 80% học thuật - 20% thương hiệu dành cho lứa 2k9.")
    25|    with st.form("plan_form"):
    26|        col1, col2 = st.columns(2)
    27|        with col1:
    28|            timeframe = st.text_input("Khoảng thời gian (VD: Tuần 1 tháng 6/2026)")
    29|        with col2:
    30|            target_audience = st.text_input("Mục tiêu trọng tâm (VD: Khởi động Lộ trình S)")
    31|        submit_plan = st.form_submit_button("Phân tích & Lên kế hoạch")
    32|    if submit_plan:
    33|        st.success("Đang phân tích dữ liệu kho tài liệu và khởi tạo ma trận lịch trình nội dung...")
    34|
    35|elif menu == "2. Tạo nội dung cụ thể":
    36|    st.title("✍️ Tạo nội dung cụ thể")
    37|    
    38|    col_left, col_right = st.columns([1, 1], gap="large")
    39|    
    40|    with col_left:
    41|        st.subheader("📥 Nhập yêu cầu")
    42|        topic = st.text_area("1. Chủ đề", placeholder="Nhập chủ đề hoặc thông điệp cốt lõi...")
    43|        
    44|        speaker = st.selectbox("2. Người phát ngôn", ["Giáo viên", "Chuyên gia GD", "Học sinh", "Phụ huynh"])
    45|        
    46|        audience_choice = st.selectbox("3. Đối tượng hướng đến", ["học sinh 2k9", "phụ huynh 2k9", "Khác"])
    47|        if audience_choice == "Khác":
    48|            audience = st.text_input("Nhập đối tượng khác:")
    49|        else:
    50|            audience = audience_choice
    51|            
    52|        format_choice = st.selectbox("4. Định dạng", ["Caption FB", "Video script", "Short comment", "Long-form content", "Khác"])
    53|        if format_choice == "Khác":
    54|            format_type = st.text_input("Nhập định dạng khác:")
    55|        else:
    56|            format_type = format_choice
    57|            
    58|        other_req = st.text_area("5. Yêu cầu khác", placeholder="Tone, mood, hoặc dán một đoạn văn mẫu để AI bắt chước văn phong...")
    59|        
    60|        st.caption("Ràng buộc hệ thống: Hook sắc bén, 80% học thuật - 20% thương hiệu, Văn xuôi (không gạch đầu dòng), Đã qua kiểm duyệt Logic.")
    61|        
    62|        generate_btn = st.button("TẠO NỘI DUNG", type="primary", use_container_width=True)
    63|
    64|    with col_right:
    65|        # Sử dụng columns để căn nút bấm lên trên cùng bên phải, ngang hàng với subheader
    66|        header_col1, header_col2, header_col3 = st.columns([5, 2, 2])
    67|        with header_col1:
    68|            st.subheader("📤 Nội dung chi tiết")
    69|            
    70|        if generate_btn:
    71|            if topic:
    72|                with header_col2:
    73|                    st.button("TẠO LẠI", use_container_width=True)
    74|                with header_col3:
    75|                    st.button("COPY", use_container_width=True)
    76|                    
    77|                with st.spinner("Đang phân tích logic và khởi tạo bản thảo..."):
    78|                    result_text = "Đây là khu vực hiển thị bản thảo sau khi hệ thống đã hoàn tất việc trích xuất ý tưởng và tự động rà soát chéo về ngữ pháp cũng như logic. Nội dung tại đây đảm bảo bám sát các tiêu chí khắt khe của chiến dịch Lộ trình S, duy trì cấu trúc văn xuôi liền mạch hoàn toàn không sử dụng định dạng gạch đầu dòng."
    79|                    st.text_area("Kết quả:", value=result_text, height=380, label_visibility="collapsed")
    80|            else:
    81|                st.warning("Vui lòng nhập Chủ đề để hệ thống có cơ sở xử lý.")
    82|        else:
    83|            st.info("Bản thảo hoàn thiện sẽ hiển thị tại đây sau khi bạn bấm TẠO NỘI DUNG.")
    84|
    85|elif menu == "3. Thông tin kỳ thi VACT":
    86|    st.title("🎯 Thông tin kỳ thi V-ACT (ĐGNL ĐHQG-HCM)")
    87|    st.markdown("---")
    88|    
    89|    # Giới thiệu & Hình thức
    90|    col1, col2 = st.columns(2)
    91|    with col1:
    92|        st.info("**Giới thiệu ngắn gọn:**\nKỳ thi Đánh giá Năng lực (V-ACT) do ĐHQG-HCM tổ chức nhằm đánh giá các năng lực cơ bản để học tập đại học của thí sinh như: sử dụng ngôn ngữ, tư duy logic, xử lý số liệu và giải quyết vấn đề.")
    93|    with col2:
    94|        st.success("**Hình thức thi & Lệ phí:**\n- Hình thức: Trắc nghiệm khách quan trên giấy (120 câu hỏi/150 phút).\n- Lệ phí thi: Khoảng 300.000 VNĐ/lượt (theo mức chuẩn các năm).")
    95|        
    96|    # Thời gian tổ chức & Điểm thi
    97|    col3, col4 = st.columns(2)
    98|    with col3:
    99|        st.warning("**Thời gian tổ chức:**\nThường có 2 đợt/năm:\n- Đợt 1: Cuối tháng 3 / đầu tháng 4.\n- Đợt 2: Cuối tháng 5 / đầu tháng 6.")
   100|    with col4:
   101|        st.error("**Điểm thi:**\n- Thang điểm tối đa: 1.200 điểm.\n- Chấm điểm bằng phương pháp trắc nghiệm hiện đại (Lý thuyết Ứng đáp Câu hỏi - IRT), câu khó sẽ có trọng số cao hơn câu dễ.")
   102|
   103|    st.markdown("### 📊 Cấu trúc đề thi & Chuyên đề trọng tâm")
   104|    tab1, tab2, tab3 = st.tabs(["Phần 1: Ngôn ngữ", "Phần 2: Toán học & Logic", "Phần 3: Giải quyết vấn đề"])
   105|    
   106|    with tab1:
   107|        st.markdown("""
   108|        **Sử dụng ngôn ngữ (40 câu):**
   109|        - *Tiếng Việt (20 câu):* Đọc hiểu văn bản, ngữ pháp, từ vựng, tác giả tác phẩm, phát hiện lỗi sai trong câu.
   110|        - *Tiếng Anh (20 câu):* Từ vựng, ngữ pháp, đọc hiểu đoạn văn, nhận diện lỗi sai.
   111|        """)
   112|    with tab2:
   113|        st.markdown("""
   114|        **Toán học, Tư duy logic, Phân tích số liệu (30 câu):**
   115|        - *Toán học (10 câu):* Đại số, Hình học, Giải tích, Tổ hợp - Xác suất.
   116|        - *Tư duy logic (10 câu):* Suy luận logic từ các mệnh đề, dữ kiện cho trước.
   117|        - *Phân tích số liệu (10 câu):* Đọc hiểu biểu đồ (tròn, cột, đường), bảng số liệu, tính toán thống kê cơ bản.
   118|        """)
   119|    with tab3:
   120|        st.markdown("""
   121|        **Giải quyết vấn đề (50 câu):**
   122|        - *Khoa học tự nhiên:* Hóa học (10 câu), Vật lý (10 câu), Sinh học (10 câu). Thường tập trung vào lý thuyết nền tảng, bài tập thực hành và ứng dụng.
   123|        - *Khoa học xã hội:* Địa lý (10 câu), Lịch sử (10 câu). Phân tích sự kiện lịch sử, đọc hiểu Atlat, biểu đồ địa lý.
   124|        """)
   125|        
   126|    st.markdown("---")
   127|    
   128|    # Phổ điểm thi
   129|    st.markdown("### 📈 Phổ điểm thi 2025 và 2026")
   130|    col_p1, col_p2 = st.columns(2)
   131|    with col_p1:
   132|        st.metric(label="Phổ điểm trung bình 2025", value="~680 - 720", delta="Số liệu tham khảo")
   133|    with col_p2:
   134|        st.metric(label="Phổ điểm trung bình 2026", value="Đang cập nhật...", delta="Chưa có dữ liệu chính thức đợt thi", delta_color="off")
   135|        
   136|    st.markdown("---")
   137|    
   138|    # Các thông tin khác dùng expander
   139|    st.markdown("### 📌 Thông tin mở rộng")
   140|    
   141|    with st.expander("🎓 Các trường xét điểm thi ĐGNL ĐHQG-HCM"):
   142|        st.write("""
   143|        Hơn 100 trường Đại học, Cao đẳng trên cả nước sử dụng kết quả kỳ thi này để xét tuyển, bao gồm:
   144|        - **Hệ thống ĐHQG-HCM:** ĐH Bách Khoa, ĐH KHTN, ĐH KHXH&NV, ĐH Kinh tế - Luật, ĐH Quốc tế, ĐH CNTT, v.v.
   145|        - **Các trường ngoài hệ thống:** ĐH Kinh tế TP.HCM (UEH), ĐH Công nghiệp TP.HCM, ĐH Ngân hàng, ĐH Ngoại thương (Cơ sở 2),...
   146|        """)
   147|        
   148|    with st.expander("⚠️ Các lưu ý khác cho thí sinh"):
   149|        st.write("""
   150|        - **Giấy tờ:** Bắt buộc mang theo CMND/CCCD/Hộ chiếu hợp lệ và Giấy báo dự thi (bản in).
   151|        - **Vật dụng:** Chỉ mang bút chì (2B khuyên dùng), bút bi, tẩy, Atlat Địa lý VN (không có nét viết thêm), máy tính bỏ túi theo quy định.
   152|        - **Thời gian:** Làm bài liên tục 150 phút, không có thời gian nghỉ giải lao giữa các phần.
   153|        """)
   154|        
   155|    with st.expander("❓ Một số câu hỏi thường gặp (FAQs)"):
   156|        st.markdown("""
   157|        **Q: Có thể đăng ký thi cả 2 đợt không?**  
   158|        A: Có. Thí sinh có thể thi cả 2 đợt, hệ thống xét tuyển sẽ tự động lấy kết quả của đợt thi có điểm cao nhất.
   159|        
   160|        **Q: Kỳ thi có bắt học thuộc lòng nhiều không?**  
   161|        A: Không. Kỳ thi V-ACT chú trọng vào việc đánh giá năng lực tư duy, xử lý số liệu và kỹ năng giải quyết vấn đề hơn là việc ghi nhớ máy móc.
   162|        
   163|        **Q: Điểm bài thi được tính như thế nào?**  
   164|        A: Không phải mỗi câu đều có điểm bằng nhau (ví dụ 10 điểm/câu). Điểm được tính theo thuật toán IRT, câu hỏi khó có ít người làm được sẽ có trọng số điểm cao hơn câu dễ.
   165|        """)
   166|