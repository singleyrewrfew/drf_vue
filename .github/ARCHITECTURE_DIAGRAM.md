# GitHub Actions 自动化部署架构图

## 🏗️ 整体架构

```mermaid
graph TB
    A[开发者推送代码] --> B{GitHub}
    B --> C[GitHub Actions]
    C --> D{工作流类型}
    
    D -->|backend/**| E[后端部署工作流]
    D -->|frontend/**| F[前端部署工作流]
    D -->|其他| G[CI/CD 流水线]
    
    E --> H[运行测试]
    H --> I{测试通过?}
    I -->|是| J[SSH 连接服务器]
    I -->|否| K[停止部署]
    
    J --> L[上传代码]
    L --> M[安装依赖]
    M --> N[数据库迁移]
    N --> O[重启 Gunicorn]
    O --> P[部署完成]
    
    F --> Q[构建前端]
    Q --> R[上传构建产物]
    R --> S[设置权限]
    S --> T[重启 Nginx]
    T --> P
    
    G --> U[运行测试]
    G --> V[构建前端]
    G --> W[代码质量检查]
    U --> X[生成报告]
    V --> X
    W --> X
```

## 🔄 后端部署流程

```mermaid
sequenceDiagram
    participant Dev as 开发者
    participant GH as GitHub
    participant GA as GitHub Actions
    participant Server as 你的服务器
    
    Dev->>GH: git push origin main
    GH->>GA: 触发 deploy-backend.yml
    GA->>GA: 运行测试套件
    GA->>Server: SSH 连接
    Server-->>GA: 连接成功
    GA->>Server: rsync 上传代码
    GA->>Server: pip install -r requirements.txt
    GA->>Server: python manage.py migrate
    GA->>Server: python manage.py collectstatic
    GA->>Server: systemctl restart drf_vue_backend
    Server-->>GA: 服务重启成功
    GA->>GH: 部署成功通知
    GH->>Dev: 显示部署状态 ✅
```

## 🎨 前端部署流程

```mermaid
sequenceDiagram
    participant Dev as 开发者
    participant GH as GitHub
    participant GA as GitHub Actions
    participant Server as 你的服务器
    
    Dev->>GH: git push origin main
    GH->>GA: 触发 deploy-frontend.yml
    GA->>GA: npm ci (frontend)
    GA->>GA: npm run build (PC)
    GA->>GA: npm ci (mobile)
    GA->>GA: npm run build (Mobile)
    GA->>GA: npm ci (front)
    GA->>GA: npm run build (Admin)
    GA->>Server: SSH 连接
    GA->>Server: rsync 上传 dist/
    Server-->>GA: 上传完成
    GA->>Server: chown www-data:www-data
    GA->>Server: systemctl restart nginx
    Server-->>GA: Nginx 重启成功
    GA->>GH: 部署成功通知
    GH->>Dev: 显示部署状态 ✅
```

## 🛠️ 技术栈架构

```mermaid
graph LR
    subgraph "客户端"
        A1[PC 浏览器]
        A2[移动浏览器]
        A3[后台管理界面]
    end
    
    subgraph "Nginx (80/443)"
        B1[静态文件服务]
        B2[反向代理]
        B3[移动端检测]
    end
    
    subgraph "应用层"
        C1[Gunicorn :8001]
        C2[Django + DRF]
    end
    
    subgraph "数据层"
        D1[(PostgreSQL)]
        D2[Redis Cache]
        D3[Media Files]
    end
    
    A1 --> B1
    A2 --> B1
    A3 --> B1
    
    B2 --> C1
    C1 --> C2
    
    C2 --> D1
    C2 --> D2
    C2 --> D3
```

## 📊 CI/CD 流水线

```mermaid
graph LR
    A[代码提交] --> B{分支判断}
    
    B -->|PR/develop| C[CI Pipeline]
    B -->|main/master| D[CD Pipeline]
    
    C --> E[单元测试]
    C --> F[构建测试]
    C --> G[代码质量]
    E --> H{全部通过?}
    F --> H
    G --> H
    H -->|是| I[允许合并]
    H -->|否| J[拒绝合并]
    
    D --> K[运行测试]
    K --> L{测试通过?}
    L -->|是| M[部署到生产]
    L -->|否| N[停止部署]
    M --> O[健康检查]
    O --> P{检查通过?}
    P -->|是| Q[部署完成 ✅]
    P -->|否| R[自动回滚 ↩️]
```

## 🔐 安全架构

```mermaid
graph TB
    subgraph "GitHub"
        A[代码仓库]
        B[Secrets 存储]
        C[Actions Runner]
    end
    
    subgraph "传输层"
        D[SSH 加密通道]
        E[HTTPS/TLS]
    end
    
    subgraph "服务器"
        F[Nginx]
        G[Firewall/UFW]
        H[Gunicorn]
        I[Django]
        J[(Database)]
    end
    
    B -.->|注入环境变量| C
    C ==>|SSH 私钥认证| D
    D --> G
    G --> F
    F -->|反向代理| H
    H --> I
    I --> J
    
    style B fill:#f9f,stroke:#333,stroke-width:4px
    style D fill:#bbf,stroke:#333,stroke-width:2px
    style G fill:#f96,stroke:#333,stroke-width:2px
```

## 📁 目录结构映射

```mermaid
graph TB
    subgraph "GitHub 仓库"
        A1[.github/workflows/]
        A2[backend/]
        A3[frontend/]
        A4[mobile/]
        A5[front/]
    end
    
    subgraph "服务器 /home/DRF_VUE/drf_vue/backend"
        B1[config/settings.py]
        B2[apps/*]
        B3[venv/]
        B4[media/]
        B5[staticfiles/]
    end
    
    subgraph "服务器 /home/front"
        C1[dist/ - PC 端]
        C2[dist_mobile/ - 移动端]
        C3[dist_backend/ - 后台管理]
    end
    
    subgraph "系统服务"
        D1[/etc/systemd/system/drf_vue_backend.service]
        D2[/etc/nginx/nginx.conf]
        D3[/var/log/gunicorn/]
        D4[/var/log/nginx/]
    end
    
    A2 -->|rsync| B1
    A2 -->|rsync| B2
    A3 -->|npm build| C1
    A4 -->|npm build| C2
    A5 -->|npm build| C3
    
    B1 -.->|Gunicorn| D1
    C1 -.->|Nginx serve| D2
    B4 -.->|Nginx serve| D2
    
    D1 -.->|日志| D3
    D2 -.->|日志| D4
```

## 🚦 部署决策树

```mermaid
graph TD
    A[代码变更] --> B{变更类型?}
    
    B -->|后端代码| C[修改 backend/**]
    B -->|前端代码| D[修改 frontend/**]
    B -->|配置文件| E[修改 .github/**]
    B -->|文档| F[修改 docs/**]
    
    C --> G[触发后端部署]
    D --> H[触发前端部署]
    E --> I[触发 CI/CD]
    F --> J[仅运行 CI]
    
    G --> K{主分支?}
    H --> K
    I --> K
    
    K -->|是 main/master| L[执行部署]
    K -->|否| M[仅运行测试]
    
    L --> N{测试通过?}
    N -->|是| O[部署到生产 ✅]
    N -->|否| P[停止并告警 ❌]
    
    M --> Q[生成测试报告 📊]
```

## 🔄 回滚策略

```mermaid
sequenceDiagram
    participant Admin as 管理员
    participant GH as GitHub
    participant Server as 服务器
    
    Admin->>GH: 发现生产问题
    Admin->>GH: 触发回滚工作流
    GH->>Server: SSH 连接
    Server-->>GH: 连接成功
    GH->>Server: git checkout <previous_commit>
    GH->>Server: systemctl restart drf_vue_backend
    Server-->>GH: 回滚完成
    GH->>Admin: 回滚成功通知 ✅
    
    Note over Admin,Server: 通常在 2-5 分钟内完成回滚
```

## 📈 监控架构

```mermaid
graph LR
    subgraph "应用层"
        A1[Django App]
        A2[Nginx]
        A3[Gunicorn]
    end
    
    subgraph "日志收集"
        B1[Error Logs]
        B2[Access Logs]
        B3[System Logs]
    end
    
    subgraph "监控系统"
        C1[Prometheus]
        C2[Grafana]
        C3[Alert Manager]
    end
    
    subgraph "通知渠道"
        D1[Email]
        D2[Slack]
        D3[钉钉]
    end
    
    A1 --> B1
    A2 --> B2
    A3 --> B3
    
    B1 --> C1
    B2 --> C1
    B3 --> C1
    
    C1 --> C2
    C1 --> C3
    
    C3 --> D1
    C3 --> D2
    C3 --> D3
```

## 🎯 性能优化流程

```mermaid
graph TB
    A[用户请求] --> B{Nginx}
    
    B -->|静态文件| C[直接返回]
    B -->|API 请求| D[Gunicorn]
    
    C --> E{缓存命中?}
    E -->|是| F[返回缓存 ✅]
    E -->|否| G[从磁盘读取]
    
    D --> H{Django Cache}
    H -->|命中| I[返回缓存数据 ✅]
    H -->|未命中| J[查询数据库]
    
    J --> K[(PostgreSQL)]
    K --> L[序列化数据]
    L --> M[存入缓存]
    M --> N[返回响应]
    
    G --> O[压缩传输]
    N --> O
    O --> P[用户收到响应]
    
    style F fill:#9f9
    style I fill:#9f9
```

## 🔧 故障排查流程

```mermaid
graph TD
    A[网站无法访问] --> B{检查什么?}
    
    B -->|服务状态| C[systemctl status]
    B -->|日志| D[tail -f logs]
    B -->|网络| E[curl/ping]
    
    C --> F{服务运行?}
    F -->|否| G[启动服务]
    F -->|是| H[检查配置]
    
    D --> I{有错误?}
    I -->|是| J[根据错误修复]
    I -->|否| K[检查依赖服务]
    
    E --> L{能连通?}
    L -->|否| M[检查防火墙/网络]
    L -->|是| N[检查应用层]
    
    G --> O[验证修复]
    H --> O
    J --> O
    K --> O
    M --> O
    N --> O
    
    O --> P{问题解决?}
    P -->|是| Q[✅ 完成]
    P -->|否| R[🔍 深入排查]
```

---

**提示：** 这些图表使用 Mermaid 语法，可以在支持 Mermaid 的 Markdown 编辑器中查看（如 GitHub、GitLab、VS Code 等）。
