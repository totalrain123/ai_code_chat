# Cursor Cloud Agent

一个基于 **Vue 3 + Vite**（前端）和 **FastAPI**（后端）的云端智能开发助手项目。

## 本地运行

### 1) 启动后端

```bash
pip install -r requirements.txt
python app.py
```

后端默认地址：`http://localhost:8000`

### 2) 启动前端

```bash
npm install
npm run dev
```

前端默认地址：`http://localhost:3000`

## 环境变量

在仓库根目录创建 `.env` 并填写模型相关密钥（示例见项目中的 `.env` 文件模板）。

前端可选变量：

- `VITE_API_BASE_URL`：后端 API 地址（默认 `/api`）

后端可选变量：

- `CORS_ORIGINS`：允许跨域来源，多个用逗号分隔。默认 `*`

## 发布（GitHub Pages）

仓库已配置工作流：`.github/workflows/deploy-frontend.yml`

- 推送到 `master` 或 `cursor/**` 分支会自动构建并发布前端到 GitHub Pages
- 也支持手动触发（`workflow_dispatch`）

建议在仓库 Settings -> Variables 中配置：

- `VITE_API_BASE_URL`：你的后端线上地址，例如 `https://your-api.example.com/api`

发布后页面地址通常为：

`https://<你的GitHub用户名>.github.io/<仓库名>/`

