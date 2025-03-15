# 阶段1: 构建阶段
FROM node:16-alpine as builder

# 设置工作目录
WORKDIR /app

# 使用淘宝镜像加速
RUN npm config set registry https://registry.npmmirror.com

# 首先只复制package.json和package-lock.json（如果存在）
COPY package*.json ./

# 安装依赖
RUN npm ci || npm install

# 复制所有源代码
COPY . .

# 构建前端项目
RUN npm run build

# 阶段2: 运行阶段 - 使用轻量级nginx来提供静态文件
FROM nginx:alpine

# 复制nginx配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 从构建阶段复制构建结果
COPY --from=builder /app/dist /usr/share/nginx/html

# 暴露80端口
EXPOSE 80

# 启动nginx
CMD ["nginx", "-g", "daemon off;"] 