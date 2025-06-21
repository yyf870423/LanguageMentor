FROM python:3.10-slim

# 设置环境变量，防止 Python 生成 .pyc 文件，设置 UTF-8 locale
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

WORKDIR /app

# 安装依赖
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 拷贝项目文件
COPY src/ ./src/
COPY content/ ./content/
COPY prompts/ ./prompts/
COPY images/ ./images/
COPY README.md ./
COPY logs/ ./logs/

# 确保日志目录存在
RUN mkdir -p logs

EXPOSE 7860

CMD ["python", "src/main.py"] 