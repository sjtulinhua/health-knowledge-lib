# Health & Fitness Knowledge Library - Backend

权威医疗健康与运动科学资料检索系统 MVP

## 技术栈

- **框架**: FastAPI
- **向量数据库**: ChromaDB
- **LLM**: Gemini API
- **数据库**: SQLite (MVP)

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
cp .env.example .env
# 编辑 .env 填入 GEMINI_API_KEY

# 启动服务
uvicorn app.main:app --reload
```

## API 文档

启动服务后访问: http://localhost:8000/docs
