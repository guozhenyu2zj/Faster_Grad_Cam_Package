# Faster-Grad-Cam

This project is for Machine Learning in Computer Vision Project. 

## Create development environment

It is recommanded to use miniconda for python version control and poetry for dependency management.

```
conda create -n faster_grad_cam python=3.8
conda activate -n faster_grad_cam
pip install poetry
poetry install
```
Then install pre-commit hook with flake8 and black:
```
pre-commit install
```

## Deploy by docker
If you just want to use the demo, you can deploy it by docker:
```
docker run -dp 8501:8501 ahahaha2333/faster_grad_cam:v6.0
```
Then you can use the demo by web ui:
```
localhost:8501
```


## Contributing

Guo Zhenyu(guozhenyu2zj@gmail.com)

## License

MIT © Richard McRichface
