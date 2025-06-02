from package import (
    streamlit as st,
    cv2,
    numpy as np,
    NDArray,
    Optional,
    base64,
    io,
    Image
)
from get_hart import Get_object

def check_button_update_image(check_button_selection : bool) -> bool:
    return True if (check_button_selection != None) else False

class Update_Image:
    def __init__(self, title : str) -> None:
        '''
        title : Nội dung của nút tải ảnh lên
        init_button_update_image : khởi tạo nút bấm tải ảnh
        '''
        self.__title : str = title.upper()
        self.__init_button_update_image : bool = st.file_uploader(self.__title, type=["png", "jpg", "jpeg"])
    
    def check(self) -> bool: # check xem nút đấy đã bấm hay chưa
        return True if (check_button_update_image(self.__init_button_update_image)) else False
    
    def get_infor_button_update_image(self) -> Optional[st.runtime.uploaded_file_manager.UploadedFile]:
        return self.__init_button_update_image
        
st.set_page_config(layout="wide")

# Chia thành 2 cột: trái và phải
col_one, col_two, col_three = st.columns([1, 1, 1])

hair_rgba = None
target = None

with col_one:
    update_image_col1 = Update_Image("Bạn hãy chọn ảnh mà bạn muốn lấy tóc")
    if (update_image_col1.check()):
        up_check_one = update_image_col1.get_infor_button_update_image()
        file_bytes = np.asarray(bytearray(up_check_one.read()), dtype=np.uint8)
        image : NDArray[np.int32] = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)  # Đọc ảnh OpenCV
        image_new : NDArray[np.int32] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        hair_rgba = Get_object(image_new).image_hart()

        # Chuyển sang PIL.Image
        image_pil = Image.fromarray(image_new)
        
        # Encode base64
        buffered = io.BytesIO()
        image_pil.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        # HTML hiển thị ảnh bên trong khung
        st.markdown(f"""
        <div style="border: 2px solid #888; padding: 10px; margin-bottom: 10px; height: auto;">
            <img src="data:image/png;base64,{img_base64}" style="width:100%; height:auto;" />
        </div>
        """, unsafe_allow_html=True)

with col_two:
    update_image_col2 = Update_Image("Bạn hãy chọn ảnh mà bạn muốn đổi tóc")
    if (update_image_col2.check()):
        up_check_one = update_image_col2.get_infor_button_update_image()
        file_bytes = np.asarray(bytearray(up_check_one.read()), dtype=np.uint8)
        image : NDArray[np.int32] = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)  # Đọc ảnh OpenCV
        image_new : NDArray[np.int32] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        target = image_new

        # Chuyển sang PIL.Image
        image_pil = Image.fromarray(image_new)
        
        # Encode base64
        buffered = io.BytesIO()
        image_pil.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        # HTML hiển thị ảnh bên trong khung
        st.markdown(f"""
        <div style="border: 2px solid #888; padding: 10px; margin-bottom: 10px; height: auto;">
            <img src="data:image/png;base64,{img_base64}" style="width:100%; height:auto;" />
        </div>
        """, unsafe_allow_html=True)

with col_three:
    st.write("")  # tạo khoảng trắng phía trên cho thẳng hàng
    st.write("")
    st.write("")
    if (st.button("Ghép tóc",use_container_width=True)):
        st.write("")  # tạo khoảng trắng phía trên cho thẳng hàng
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        # st.write("")
    
        print(type(hair_rgba))
        print(type(target))
        # if (type(hair_rgba) != None and target != None):
        if (type(hair_rgba) == np.ndarray and type(target) == np.ndarray):
            # Chuyển sang PIL.Image

            # --- Tạo ảnh tóc BGR và mask ---
            gray = cv2.cvtColor(hair_rgba, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

            center = (target.shape[1] // 2, target.shape[0] // 4)  # Ở giữa, hơi cao (đỉnh đầu)
            
            # --- Ghép bằng seamlessClone ---
            output = cv2.seamlessClone(hair_rgba, target, mask, center, cv2.MIXED_CLONE)

            image_pil = Image.fromarray(output)
            
            # Encode base64
            buffered = io.BytesIO()
            image_pil.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            # HTML hiển thị ảnh bên trong khung
            st.markdown(f"""
            <div style="border: 2px solid #888; padding: 10px; margin-bottom: 10px; height: auto;">
                <img src="data:image/png;base64,{img_base64}" style="width:100%; height:auto;" />
            </div>
            """, unsafe_allow_html=True)

    ...

# '''

# '''
# with col_two:

#     # Đọc ảnh
#     if (up_check_one != None):
#         file_bytes = np.asarray(bytearray(up_check_one.read()), dtype=np.uint8)
#         image : NDArray[np.int32] = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)  # Đọc ảnh OpenCV
#         image_new : NDArray[np.int32] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#         # print(image_cv)
#         with st.container():
#             st.markdown("""
#             <div style="border: 2px solid #888; padding: 0px; margin-bottom: 10px; height: auto;">
#             """, unsafe_allow_html=True)
#             st.image(image_new, use_container_width=True)
#             st.markdown("</div>", unsafe_allow_html=True)


# oke_check_one1 : bool = False
# up_check_one1 = None

# with col_for:
#     update_image1 = Update_Image("Bạn hãy chọn ảnh tóc mà bạn muốn lấy")
#     if (update_image1.check()):
#         oke_check_one1 : bool = True
#         up_check_one1 = update_image1.get_infor_button_update_image()

# with col_three:
#     # Đọc ảnh
#     if (up_check_one1 != None):
#         file_bytes = np.asarray(bytearray(up_check_one1.read()), dtype=np.uint8)
#         image1 : NDArray[np.int32] = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)  # Đọc ảnh OpenCV
#         image_new1 : NDArray[np.int32] = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)

#         # print(image_cv)
#         with st.container():
#             st.markdown("""
#             <div style="border: 2px solid #888; padding: 0px; margin-bottom: 10px; height: auto;">
#             """, unsafe_allow_html=True)
#             st.image(image_new1, use_container_width=True)
#             st.markdown("</div>", unsafe_allow_html=True)

# '''
