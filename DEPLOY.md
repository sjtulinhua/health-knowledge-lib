# 🚀 部署指南 (Deployment Guide)

本项目采用前后端分离架构，推荐以下免费部署方案：

- **前端 (Frontend)**: 部署到 [Vercel](https://vercel.com/) (Next.js 官方平台)
- **后端 (Backend)**: 部署到 [Render](https://render.com/) (支持 Python 服务的免费平台)

---

## 第一步：部署后端 (Render)

我们需要先部署后端，因为前端需要后端的 API 地址。

1.  **注册/登录**: 访问 [dashboard.render.com](https://dashboard.render.com/) 并使用 GitHub 账号登录。
2.  **创建服务**:
    - 点击 **"New +"** 按钮 -> 选择 **"Blueprint"**。
    - 连接你的 GitHub 仓库 `health-knowledge-lib`。
    - Render 会自动读取仓库里的 `render.yaml` 配置文件。
3.  **配置密钥**:
    - 在配置页面，你会看到 `GEMINI_API_KEY` 的输入框。
    - 填入你的 Google Gemini API Key。
4.  **点击 Apply**:
    - 等待几分钟，部署完成后，你会在左上角看到一个 URL（例如 `https://health-knowledge-backend.onrender.com`）。
    - **复制这个网址**，下一步要用。

---

## 第二步：部署前端 (Vercel)

1.  **注册/登录**: 访问 [vercel.com](https://vercel.com/) 并使用 GitHub 账号登录。
2.  **导入项目**:
    - 点击 **"Add New..."** -> **"Project"**。
    - 选择 `health-knowledge-lib` 仓库并点击 **Import**。
3.  **配置项目 (重要)**:
    - **Framework Preset**: 保持 `Next.js`。
    - **Root Directory**: 点击 Edit，选择 `frontend` 文件夹。
    - **Environment Variables**:
        - 展开环境变量设置。
        - Key: `NEXT_PUBLIC_API_URL`
        - Value: **你在第一步获得的后端网址** (注意：网址末尾不要带斜杠 `/`)。
4.  **点击 Deploy**:
    - 等待构建完成。完成后你会获得一个 `https://health-knowledge-lib.vercel.app` 之类的网址。

---

## 🎉 完成！

现在你就可以通过 Vercel 提供的网址访问你的应用了。

### 常见问题
- **后端冷启动**: Render 的免费实例如果长时间没有人用会自动休眠。下次访问时可能需要等待 30-50 秒才能唤醒，这是正常现象。
- **CORS 错误**: 如果前端报错 API 连接失败，请检查后端的 `main.py` 中的 CORS 设置（目前已设置为允许所有来源 `["*"]`，这适用于开发和演示）。
