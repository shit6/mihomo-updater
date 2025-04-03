FROM python:3.9-slim

WORKDIR /app

# # 使用中国科技大学镜像源
# RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
#     sed -i 's/security.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
#     apt-get update && \
#     apt-get install -y --no-install-recommends gcc libc6-dev && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

# 配置pip使用清华源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 设置时区为上海时区
ENV TZ=Asia/Shanghai
# 安装tzdata并设置时区
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata && \
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY backend/requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制所有源文件
COPY backend/ .

# 复制默认配置文件到/tmp
COPY backend/config.yaml /tmp/

# 复制入口点脚本
COPY build/docker/backend/docker-entrypoint.sh ./

# 创建日志目录
RUN mkdir -p logs

# 确保启动脚本可执行
RUN chmod +x docker-entrypoint.sh

# 设置环境变量
ENV CONFIG_DIR=/config
ENV PYTHONUNBUFFERED=1

# 暴露端口
EXPOSE 5000

# 挂载点 - 配置文件和日志
VOLUME ["/config", "/app/logs", "/etc/mihomo"]

# 使用启动脚本
ENTRYPOINT ["/app/docker-entrypoint.sh"] 