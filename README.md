# 教育数据智能问数 Agent

面向教育培训场景的自然语言问数系统。用户可以直接提问报名人数、收入、完课率、课程和校区等经营问题，系统通过 LangGraph 编排检索、SQL 生成、只读校验和执行，并在工作台中实时展示处理过程、结果表格、图表和 SQL。

## 项目亮点

- **自然语言问数**：将教育业务问题转换为可执行的 MySQL 查询。
- **三路元数据召回**：使用 Qdrant 召回字段和指标，使用 Elasticsearch 召回业务枚举值。
- **可追溯 Agent 流程**：关键词提取、字段/指标/值召回、元数据合并、SQL 生成、校验、修正和执行均通过 SSE 返回状态。
- **只读安全执行**：SQL 执行前检查单条语句、查询类型和危险操作，拒绝写入、删除和结构变更操作。
- **可演示前端**：React + Vite 问数工作台，支持示例问题、实时进度、结果表格、趋势图、SQL 展示和查询记录。

## 技术栈

后端：Python 3.12、FastAPI、LangGraph、LangChain、MySQL、Qdrant、Elasticsearch、SSE、Docker。

前端：React、Vite、Recharts、Lucide React。

模型：支持 SiliconFlow 或其他 OpenAI 兼容接口。密钥只从环境变量读取，不写入代码和 Git。

## 系统流程

```text
自然语言问题
    -> 关键词提取
    -> 字段 / 指标 / 枚举值召回
    -> 元数据合并与过滤
    -> SQL 生成
    -> 只读校验与错误修正
    -> MySQL 执行
    -> 表格与图表结果
```

## 目录结构

```text
app/                    后端 Agent、API、客户端、仓储和服务
conf/                   应用配置和元数据配置
docker/                 MySQL、ES、Qdrant 等依赖配置
frontend/               React/Vite 前端源码
tests/                  后端单元测试
main.py                 FastAPI 生产入口
```

## 环境变量

项目支持两种命名方式。推荐直接使用已有的通用变量：

```text
API_KEY=你的模型密钥
BASE_URL=https://api.siliconflow.cn/v1
MODEL=deepseek-ai/DeepSeek-V4-Flash
```

也支持：

```text
SILICONFLOW_API_KEY=你的模型密钥
SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1
SILICONFLOW_MODEL=deepseek-ai/DeepSeek-V4-Flash
```

不要把真实密钥写入 `README.md`、源代码、截图或 Git 提交。`.env` 文件已被 Git 忽略。

## 启动方式

### 1. 启动基础设施

```powershell
docker compose -f docker/docker-compose.yaml up -d
```

确认 MySQL、Elasticsearch、Qdrant 和 Embedding 容器处于运行状态。

### 2. 初始化元数据

```powershell
.\.venv\Scripts\python.exe -m app.scripts.build_meta_knowledge
```

必须使用模块方式运行，避免 Python 找不到 `app` 包。

### 3. 构建前端

首次运行或修改前端代码后执行：

```powershell
npm install
npm run build
```

构建产物位于 `frontend/dist`，由 FastAPI 自动托管。

### 4. 启动完整应用

在 PyCharm 中直接运行项目根目录的 `main.py`，然后打开 `http://localhost:8000`。

接口文档：`http://localhost:8000/docs`

只调试前端时可以执行：

```powershell
npm run dev
```

## 推荐演示问题

当前演示数据时间范围为 2026 年 1 月至 3 月，推荐使用：

- 2026 年 1 月至 3 月各校区的报名人数和收入是多少？
- 2026 年 1 月至 3 月完课率变化情况？
- 各课程的报名人数排名如何？
- 学生和成人学员的报名收入对比？

## API 示例

```powershell
curl.exe -N -X POST http://localhost:8000/api/query `
  -H "Content-Type: application/json" `
  -d '{"query":"各课程的报名人数排名如何？"}'
```

接口以 `text/event-stream` 返回 `progress`、`result`、`done` 和 `error` 事件。

## 验证

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m compileall -q app main.py
npm run build
```

系统只允许执行单条只读 SQL。没有配置模型密钥时，健康检查和文档页面仍可启动，但实际问数会返回配置错误。
