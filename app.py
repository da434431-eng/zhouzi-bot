import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="Zhou Shuren (Zhouzi)", page_icon="📚")

# CSS để bot trông thân thiện hơn
st.markdown("""
<style>
    .stChatMessage { border-radius: 15px; }
    .stApp { background-color: #f0f2f6; }
</style>
""", unsafe_allow_html=True)

# --- KHỞI TẠO BỘ NÃO (Dán API KEY của bạn vào đây) ---
# Lưu ý: Khi chạy thực tế trên Streamlit, mình sẽ dùng Secrets cho bảo mật.
API_KEY = "ĐIỀN_MÃ_API_CỦA_BẠN_VÀO_ĐÂY" 
genai.configure(api_key=API_KEY)

# --- THIẾT LẬP NHÂN VẬT ZHOUZI ---
SYSTEM_INSTRUCTION = """
Bạn là Zhou Shuren, biệt danh Zhouzi. 
Phong cách: Bí ẩn nhưng vui vẻ, dễ tính, kiên nhẫn, hay cười, thích chọc ghẹo nhẹ nhàng.
Ngôn ngữ: Tiếng Việt tự nhiên, như một người bạn thực sự. Dùng 'Zhouzi' và 'cậu/bạn'.

Nhiệm vụ:
1. Hỗ trợ học tập: Tóm tắt, gợi ý ý tưởng, lập lịch học (Timeline cụ thể).
2. Dạy tiếng Trung: Hướng dẫn từ vựng, ngữ pháp.
3. Kiểm tra bài: Tạo trắc nghiệm. 
   - QUY TẮC ĐẶC BIỆT: Không dùng từ 'Sai/Đúng'. Hãy gợi ý nếu sai. 
   - Nếu người dùng sai quá 5 câu trong 1 lần kiểm tra, hãy trêu ghẹo cực kỳ dễ thương (Vd: 'Ây da, 5 bông hoa rụng rồi kìa, não cá vàng rớt đâu rồi, đi uống nước cho tỉnh rồi Zhouzi giảng lại nè!').
4. Khuyến khích: Luôn đặt câu hỏi gợi mở để người dùng tự tìm đáp án.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_INSTRUCTION
)

# --- QUẢN LÝ TRÍ NHỚ (Session State) ---
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
if "error_count" not in st.session_state:
    st.session_state.error_count = 0

# --- GIAO DIỆN NGƯỜI DÙNG ---
st.title("🏯 Trạm Tri Thức của Zhouzi")
st.write("*Tớ là Zhou Shuren, nhưng cứ gọi tớ là Zhouzi cho thân thuộc nhé!*")

# Hiển thị lịch sử chat
for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Ô nhập nội dung
if prompt := st.chat_input("Hôm nay cậu muốn học gì cùng Zhouzi nào?"):
    # Hiển thị tin nhắn người dùng
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot phản hồi
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        # Logic tính điểm sai (Đây là ví dụ, bạn có thể tinh chỉnh)
        if "tôi trả lời là" in prompt.lower() or "đáp án của mình" in prompt.lower():
             # Trong thực tế, AI sẽ tự phân tích qua context, ở đây mình giả lập logic trêu ghẹo
             pass

        full_response = st.session_state.chat_session.send_message(prompt)
        response_placeholder.markdown(full_response.text)

# Nút đặt lại mục tiêu (Bên hông)
with st.sidebar:
    st.image("https://api.dicebear.com/7.x/avataaars/svg?seed=Zhouzi", width=100)
    st.subheader("Trạm của Zhouzi")
    st.info("Zhouzi sẽ luôn nhớ lộ trình học của cậu nếu cậu kể cho tớ nghe!")
    if st.button("Xóa trí nhớ/Làm mới"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()
