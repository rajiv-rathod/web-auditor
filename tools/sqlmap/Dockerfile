FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install SQLMap
RUN git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git /opt/sqlmap

# Set working directory
WORKDIR /opt/sqlmap

# Make sqlmap executable
RUN chmod +x sqlmap.py

# Create symlink for easier access
RUN ln -s /opt/sqlmap/sqlmap.py /usr/local/bin/sqlmap

# Create scan directory
RUN mkdir -p /scans

# Set entrypoint
ENTRYPOINT ["python", "sqlmap.py"]