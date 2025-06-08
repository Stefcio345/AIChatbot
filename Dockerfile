# 1. Use a full Linux image
FROM ubuntu:22.04
 
# 2. Install dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip wget curl unzip \
&& apt-get clean
 
# 3. Install Streamlit and other Python deps
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt
 
# 4. Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh && chmod +x /usr/local/bin/ollama
 
# 5. Set working directory
WORKDIR /app
 
# 6. Copy your app code
COPY . .
 
# 7. Copy the startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh
 
# 8. Expose ports
EXPOSE 80
EXPOSE 11434
 
# 9. Run the startup script
CMD ["/start.sh"]
