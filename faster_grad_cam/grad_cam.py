import cv2
import time
import os
import numpy as np
from sklearn.externals import joblib
from tensorflow.lite.python.interpreter import Interpreter


def get_score_arc(pa_vector, test):
    # cosine similarity
    cos_similarity = cosine_similarity(test, pa_vector)

    return np.max(cos_similarity)


def cosine_similarity(x1, x2):
    if x1.ndim == 1:
        x1 = x1[np.newaxis]
    if x2.ndim == 1:
        x2 = x2[np.newaxis]
    x1_norm = np.linalg.norm(x1, axis=1)
    x2_norm = np.linalg.norm(x2, axis=1)
    cosine_sim = np.dot(x1, x2.T) / (x1_norm * x2_norm + 1e-10)
    return cosine_sim


def predict_faster_gradcam(
    channel, vector, img, kmeans, channel_weight, channel_adress
):
    channel_out = channel[0]

    # k-means and heat_map
    cluster_no = kmeans.predict(vector)
    cam = np.dot(
        channel_out[:, :, channel_adress[cluster_no[0]]], channel_weight[cluster_no[0]]
    )

    # nomalize
    cam = cv2.resize(cam, (img.shape[1], img.shape[0]), cv2.INTER_LINEAR)
    cam = np.maximum(cam, 0)
    cam = cam / cam.max()

    return cam


def get_x_y_limit(heatmap, thresh):
    map_ = np.where(heatmap > thresh)
    x_max = np.max(map_[1])
    x_min = np.min(map_[1])
    y_max = np.max(map_[0])
    y_min = np.min(map_[0])

    x_max = int(x_max)
    x_min = int(x_min)
    y_max = int(y_max)
    y_min = int(y_min)
    return x_min, y_min, x_max, y_max


def bounding_box(img, x_min, y_min, x_max, y_max):
    img = cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 5)
    return img


class FasterGradCam:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), "model")

        if os.path.exists(model_path):
            # load csv
            print("csv loading...")
            self.channel_weight = np.loadtxt(
                os.path.join(model_path, "channel_weight.csv"), delimiter=","
            )
            self.channel_adress = np.loadtxt(
                os.path.join(model_path, "channel_adress.csv"),
                delimiter=",",
                dtype="float",
            )
            self.channel_adress = self.channel_adress.astype(np.int)
            self.vector_pa = np.loadtxt(
                os.path.join(model_path, "vector_pa.csv"), delimiter=","
            )
            self.kmeans = joblib.load(os.path.join(model_path, "k-means.pkl.cmp"))

        else:
            print("Nothing model folder")

        self.interpreter = Interpreter(
            model_path=os.path.join(model_path, "weights_weight_quant.tflite")
        )
        try:
            self.interpreter.set_num_threads(4)
        except Exception as e:
            print(e)

        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        time.sleep(1)

    def process_image(
        self, image, hand_thresh=0.25, OD_thresh=0.8, input_size=96, like_OD=False
    ):
        # crop to square
        height = image.shape[0]
        width = image.shape[1]
        if width > height:
            dif = int((width - height) / 2)
            width_start = dif
            width_end = width - dif
            height_start = 0
            height_end = height
        else:
            dif = int((height - width) / 2)
            width_start = 0
            width_end = width
            height_start = dif
            height_end = height - dif
        image = image[height_start:height_end, width_start:width_end]

        img = cv2.resize(image, (input_size, input_size))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img / 255
        img = np.expand_dims(img, axis=0)
        img = img.astype(np.float32)
        self.interpreter.set_tensor(self.input_details[0]["index"], img)
        self.interpreter.invoke()
        channel_out = self.interpreter.get_tensor(self.output_details[0]["index"])
        test_vector = self.interpreter.get_tensor(self.output_details[1]["index"])

        score = get_score_arc(self.vector_pa, test_vector)

        if score < hand_thresh:
            hand = "gu"
            color = (255, 0, 0)
            heatmap = predict_faster_gradcam(
                channel_out,
                test_vector,
                image,
                self.kmeans,
                self.channel_weight,
                self.channel_adress,
            )
            if like_OD is True:
                x_min, y_min, x_max, y_max = get_x_y_limit(heatmap, OD_thresh)
                image = bounding_box(image, x_min, y_min, x_max, y_max)
            else:
                heatmap = cv2.applyColorMap(np.uint8(255 * heatmap), cv2.COLORMAP_JET)
                image = np.copy(cv2.addWeighted(heatmap, 0.5, image, 0.5, 2.2))

        else:
            hand = "pa"
            color = (0, 0, 255)

        return hand, color, score, image
