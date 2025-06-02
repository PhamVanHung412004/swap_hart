from package import (
    mediapipe as mp,
    cv2,
    numpy as np,
    NDArray,
    Path

)

from init_model import Model

path_model = Path(__file__).parent / "hair_segmenter.tflite"

options : Model = Model.SelfieSegmenterOptions(
    base_options=Model.BaseOptions(model_asset_path=str(path_model)),
    running_mode=Model.VisionRunningMode.IMAGE,  # hoặc VIDEO, LIVE_STREAM
    output_category_mask=True
)

class Get_object:
    def __init__(self, image : NDArray[np.int32]) -> None:
        '''
        image : ảnh muốn lấy tóc
        '''
        self.image : NDArray[np.int32] = image
    def image_hart(self) -> NDArray[np.int32]:
        with Model.SelfieSegmenter.create_from_options(options) as segmenter:
            # Chuyển ảnh từ BGR (OpenCV) sang RGB, tạo mp.Image
            mp_image : cv2 = mp.Image(image_format=mp.ImageFormat.SRGB,
                            data=cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))

            # Chạy segmentation
            result = segmenter.segment(mp_image)

            # Lấy category mask kết quả
            category_mask = result.category_mask

            # Chuyển category_mask thành numpy array đúng cách
            mask = category_mask.numpy_view()  # Use numpy_view() instead of np.array

            # Tạo ảnh nền và ảnh mặt nạ với màu sắc tùy chọn
            BG_COLOR : tuple = (192, 192, 192)  # màu nền xám
            MASK_COLOR : tuple = (255, 255, 255)  # màu trắng cho vùng mask

            fg_image : NDArray[np.int32] = np.zeros(self.image.shape, dtype=np.uint8)
            fg_image[:] = MASK_COLOR

            bg_image : NDArray[np.int32] = np.zeros(self.image.shape, dtype=np.uint8)
            bg_image[:] = BG_COLOR

            # Tạo điều kiện để chọn pixel từ mặt nạ
            condition : NDArray[np.int32] = np.stack((mask,) * 3, axis=-1) > 0.2

            # Kết hợp ảnh mặt nạ và ảnh nền
            output_image : NDArray[np.int32] = np.where(condition, fg_image, bg_image)

            _, binary_mask = cv2.threshold(output_image, 200, 255, cv2.THRESH_BINARY)
            if len(binary_mask.shape) == 3:
                binary_mask : NDArray[np.int32] = cv2.cvtColor(binary_mask, cv2.COLOR_BGR2GRAY)
            
            #chuyển sang 3 kênh
            mask_3ch : NDArray[np.int32] = cv2.cvtColor(binary_mask, cv2.COLOR_GRAY2BGR)

            hair_only : NDArray[np.int32] = cv2.bitwise_and(self.image, mask_3ch)

            hair_only : NDArray[np.int32] = cv2.bitwise_and(self.image, mask_3ch)
            return hair_only
        
# def main():
#     path = r"E:\get_hart\Untitled2.png"
#     image = cv2.imread(path)
#     image_new = Get_object(image).image_hart()
#     cv2.imshow("Segmentation result", image_new)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# main()
