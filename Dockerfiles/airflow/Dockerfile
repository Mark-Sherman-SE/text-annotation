FROM apache/airflow:2.4.2-python3.10
USER root
WORKDIR /home/airflow
RUN cd $AIRFLOW_USER_HOME_DIR
CMD ["bash"]
ENV NVARCH=x86_64
ENV NV_CUDA_CUDART_VERSION=11.6.55-1
ENV NV_CUDA_COMPAT_PACKAGE=cuda-compat-11-6
RUN apt-get update -y
RUN apt-get install -y --no-install-recommends gnupg2 curl ca-certificates
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A4B469963BF863CC
#RUN curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/${NVARCH}/7fa2af80.pub | apt-key add - && echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/${NVARCH} /" > /etc/apt/sources.list.d/cuda.list && echo "deb https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu2004/${NVARCH} /" > /etc/apt/sources.list.d/nvidia-ml.list && apt-get purge --autoremove -y curl && rm -rf /var/lib/apt/lists/* # buildkit
RUN curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/${NVARCH}/7fa2af80.pub | apt-key add - && echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/${NVARCH} /" > /etc/apt/sources.list.d/cuda.list && apt-get purge --autoremove -y curl && rm -rf /var/lib/apt/lists/* # buildkit
ENV CUDA_VERSION=11.6.2
RUN apt-get update && apt-get install -y --no-install-recommends cuda-cudart-11-6=${NV_CUDA_CUDART_VERSION} ${NV_CUDA_COMPAT_PACKAGE} && ln -s cuda-11.6 /usr/local/cuda && rm -rf /var/lib/apt/lists/* # buildkit
RUN echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf && echo "/home/airflow/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf # buildkit
ENV PATH=/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV LD_LIBRARY_PATH=/usr/local/nvidia/lib:/usr/local/nvidia/lib64
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility
ENV NVIDIA_REQUIRE_CUDA=cuda>=11.6 brand=tesla,driver>=418,driver<419 brand=tesla,driver>=450,driver<451 brand=tesla,driver>=470,driver<471 brand=unknown,driver>=470,driver<471 brand=nvidia,driver>=470,driver<471 brand=nvidiartx,driver>=470,driver<471 brand=geforce,driver>=470,driver<471 brand=geforcertx,driver>=470,driver<471 brand=quadro,driver>=470,driver<471 brand=quadrortx,driver>=470,driver<471 brand=titan,driver>=470,driver<471 brand=titanrtx,driver>=470,driver<471
ENV NV_CUDA_LIB_VERSION=11.6.2-1
ENV NV_NVTX_VERSION=11.6.124-1
ENV NV_LIBNPP_VERSION=11.6.3.124-1
ENV NV_LIBNPP_PACKAGE="libnpp-11-6=11.6.3.124-1"
ENV NV_LIBCUSPARSE_VERSION=11.7.2.124-1
ENV NV_LIBCUBLAS_PACKAGE_NAME=libcublas-11-6
ENV NV_LIBCUBLAS_VERSION=11.9.2.110-1
ENV NV_LIBCUBLAS_PACKAGE="libcublas-11-6=11.9.2.110-1"
ENV NV_LIBNCCL_PACKAGE_NAME=libnccl2
ENV NV_LIBNCCL_PACKAGE_VERSION=2.12.10-1
ENV NCCL_VERSION=2.12.10-1
ENV NV_LIBNCCL_PACKAGE="libnccl2=2.12.10-1+cuda11.6"
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends cuda-libraries-11-6=${NV_CUDA_LIB_VERSION} ${NV_LIBNPP_PACKAGE} cuda-nvtx-11-6=${NV_NVTX_VERSION} libcusparse-11-6=${NV_LIBCUSPARSE_VERSION} ${NV_LIBCUBLAS_PACKAGE} ${NV_LIBNCCL_PACKAGE} && rm -rf /var/lib/apt/lists/* # buildkit
RUN apt-mark hold ${NV_LIBCUBLAS_PACKAGE_NAME} ${NV_LIBNCCL_PACKAGE_NAME} # buildkit
ENV NV_CUDNN_VERSION=8.4.0.27
ENV NV_CUDNN_PACKAGE_NAME=libcudnn8
ENV NV_CUDNN_PACKAGE="libcudnn8=8.4.0.27-1+cuda11.6"
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends ${NV_CUDNN_PACKAGE} && apt-mark hold ${NV_CUDNN_PACKAGE_NAME} && rm -rf /var/lib/apt/lists/* # buildkit
RUN apt-get update && apt-get install -y --no-install-recommends ${NV_CUDNN_PACKAGE} && apt-mark hold ${NV_CUDNN_PACKAGE_NAME} && rm -rf /var/lib/apt/lists/* # buildkit
ENV PATH=/home/airflow/.local/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin AIRFLOW_UID=50000 AIRFLOW_USER_HOME_DIR=/home/airflow AIRFLOW_HOME=/opt/airflow
#ARG TARGETARCH
#RUN TARGETARCH=amd64 /bin/sh -c apt-get update && apt-get install -y --no-install-recommends gnupg2 curl ca-certificates && curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/debian11/${NVARCH}/3bf863cc.pub | apt-key add - && echo "deb https://developer.download.nvidia.com/compute/cuda/repos/debian11/${NVARCH} /" > /etc/apt/sources.list.d/cuda.list && apt-get purge --autoremove -y curl && rm -rf /var/lib/apt/lists/* # buildkit
#ENV CUDA_VERSION=11.6.2
#RUN TARGETARCH=amd64 /bin/sh -c apt-get update && apt-get install -y --no-install-recommends cuda-cudart-11-6=${NV_CUDA_CUDART_VERSION} ${NV_CUDA_COMPAT_PACKAGE}  && ln -s cuda-11.6 /usr/local/cuda && rm -rf /var/lib/apt/lists/* # buildkit
#RUN TARGETARCH=amd64 /bin/sh -c echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf && echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf # buildkit
#ENV PATH=/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
#ENV LD_LIBRARY_PATH=/usr/local/nvidia/lib:/usr/local/nvidia/lib64
#ENV NVIDIA_VISIBLE_DEVICES=all
#ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility
CMD []
WORKDIR /opt/airflow
RUN cd $AIRFLOW_HOME
COPY requirements.txt .
COPY download_nltk_data.py .
USER airflow
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r requirements.txt
CMD [ "python", "./download_nltk_data.py" ]
