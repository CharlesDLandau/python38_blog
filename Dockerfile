FROM python:3.8.0rc1

RUN mkdir /code
RUN pip install jupyterlab mypy

VOLUME code
WORKDIR /code
RUN pip freeze >> requirements.txt

EXPOSE 8888:8888

# Can be run as docker run -p 8888:8888 -it --rm -v $(PWD):/code --name dev <img_tag>
ENTRYPOINT ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]