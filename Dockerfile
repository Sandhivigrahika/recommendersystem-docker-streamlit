# Use miniconda base image
FROM continuumio/miniconda3

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Create environment and install dependencies
RUN conda create -n recsys-env python=3.11 -y \
    && conda install -n recsys-env -c conda-forge scikit-surprise pandas requests -y \
    && conda run -n recsys-env pip install streamlit

# Activate environment and run Streamlit
CMD ["conda", "run", "--no-capture-output", "-n", "recsys-env", "streamlit", "run", "streamapp.py", "--server.port=8501", "--server.address=0.0.0.0"]