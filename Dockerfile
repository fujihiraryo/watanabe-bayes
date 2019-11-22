FROM jupyter/datascience-notebook
RUN pip install jupyterlab
RUN jupyter serverextension enable --py jupyterlab
