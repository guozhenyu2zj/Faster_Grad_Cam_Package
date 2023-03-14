import time
import streamlit as st
import numpy as np
from streamlit_webrtc import webrtc_streamer
import cv2
from PIL import Image
import av
from grad_cam import FasterGradCam


def open_camera():
    st.session_state["open_camera"] = True


def back_to_home():
    st.session_state["open_camera"] = False
    st.session_state["open_from_local"] = False


def open_from_local():
    st.session_state["open_from_local"] = True


def check_validation(name, password):
    if name == "admin" and password == "admin":
        st.session_state["log_in"] = True
        st.session_state["current_user"] = {
            "Name": "admin",
            "Description": "Administrator for this system.",
            "Phone": "000",
        }


def show_open_camera_page():
    webrtc_streamer(key="example", video_frame_callback=video_frame_callback)
    st.sidebar.button("Back", "back_to_home_button", on_click=back_to_home)


def show_open_from_local_page():
    upload = st.file_uploader("Select a picture from local")
    st.sidebar.button("Back", "back_to_home_button", on_click=back_to_home)
    if upload:
        image = np.array(Image.open(upload)).astype(np.uint8)
        hand, color, score, result = grad_cam.process_image(
            image, hand_thresh=hand_thresh, OD_thresh=OD_thresh, like_OD=mode
        )
        height = result.shape[0]
        width = result.shape[1]
        offset = 30
        cv2.putText(
            result,
            "{0} {1:.1f} Score".format(hand, score),
            (width - 4 * offset, height - offset),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            1,
            cv2.LINE_AA,
        )
        # print(result.shape)
        st.image(result)


def show_log_in_page():
    st.title("Faster Grad Cam Demo")
    st.sidebar.button(
        "Open From Local", "open_from_local_button", on_click=open_from_local
    )
    st.sidebar.button("Open From Camera", "open_camera_button", on_click=open_camera)


def video_frame_callback(frame):
    t1 = time.time()
    img = frame.to_ndarray(format="bgr24")
    hand, color, score, result = grad_cam.process_image(
        img, hand_thresh=hand_thresh, OD_thresh=OD_thresh, like_OD=mode
    )
    elapsedTime = time.time() - t1
    fps = "{:.0f} FPS".format(1 / elapsedTime)
    height = result.shape[0]
    width = result.shape[1]
    offset = 30
    cv2.putText(
        result,
        "{0} {1:.1f} Score".format(hand, score),
        (width - 4 * offset, height - offset),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        result,
        fps,
        (offset, offset),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        1,
        cv2.LINE_AA,
    )
    return av.VideoFrame.from_ndarray(result, format="bgr24")


if "faster_grad_cam" not in st.session_state:
    print("Init faster grad cam...")
    grad_cam = FasterGradCam()
    st.session_state["faster_grad_cam"] = grad_cam
    print("Finished initialization.")

grad_cam = st.session_state["faster_grad_cam"]
hand_thresh = st.sidebar.slider(
    "Hand Thresh", 0.0, 1.0, 0.25, 0.01, key="hand_thresh_slider"
)
OD_thresh = st.sidebar.slider("OD Thresh", 0.0, 1.0, 0.8, 0.01, key="od_thresh_slider")
mode_str = st.sidebar.radio("Mode", ("Grad Cam", "OD"))
mode = False if mode_str == "Grad Cam" else True

if "open_from_local" not in st.session_state:
    st.session_state["open_from_local"] = False
    st.session_state["upload"] = None

if "open_camera" not in st.session_state:
    st.session_state["open_camera"] = False

if (
    st.session_state["open_camera"] is False
    and st.session_state["open_from_local"] is False
):
    show_log_in_page()
elif st.session_state["open_camera"] is True:
    show_open_camera_page()
elif st.session_state["open_from_local"] is True:
    show_open_from_local_page()
