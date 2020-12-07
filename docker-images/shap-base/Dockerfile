FROM tensorflow/tensorflow:latest-gpu-py3-jupyter

RUN pip install keras pandas scikit-learn matplotlib numpy scipy h5py imblearn gpyopt python-telegram-bot shap 

EXPOSE 8888

WORKDIR /storage

CMD jupyter notebook --port=8888 --allow-root --ip=0.0.0.0 --NotebookApp.token='' --NotebookApp.password=''



