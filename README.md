# Faster-Grad-Cam

This project is for Machine Learning in Computer Vision Project. 

## Install

It is recommanded to use miniconda for python version control and poetry for dependency management.

```
conda create -n faster_grad_cam python=3.8
conda activate -n faster_grad_cam
pip install git+https://github.com/guozhenyu2zj/Faster_Grad_Cam_Package
```
Or you can download whl to install in release page.

## Build

If you want to build from source, you can do that as follows:
```
conda create -n faster_grad_cam python=3.8
conda activate -n faster_grad_cam
pip install build
git clone https://github.com/guozhenyu2zj/Faster_Grad_Cam_Package
cd Faster_Grad_Cam_Package
python -m build
```
After finishing building, you can install the whl directly:
```
cd dist
pip install faster_grad_cam-0.1.0-py3-none-any.whl
```


## Usage

Just enter "faster_grad_cam" for running the program. This program will use your camera to read image. Only show a image for testing if there is no camera available.

## Contributing

Guo Zhenyu(guozhenyu2zj@gmail.com)

## License

MIT © Richard McRichface