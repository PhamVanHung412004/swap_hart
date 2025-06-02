from package import (
    mediapipe,
    dataclass
)

@dataclass
class Model:
    BaseOptions : mediapipe  = mediapipe.tasks.BaseOptions
    SelfieSegmenter : mediapipe = mediapipe.tasks.vision.ImageSegmenter
    SelfieSegmenterOptions : mediapipe = mediapipe.tasks.vision.ImageSegmenterOptions
    VisionRunningMode : mediapipe = mediapipe.tasks.vision.RunningMode

