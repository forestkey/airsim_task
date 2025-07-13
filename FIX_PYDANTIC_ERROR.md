# 修复 Pydantic 错误

## 错误原因
您遇到的错误是因为 Pydantic v2 将 `BaseSettings` 移到了独立的 `pydantic-settings` 包中。

## 解决步骤

在激活的 Python 环境中运行：

```bash
cd backend
pip install pydantic-settings==2.1.0
```

或者重新安装所有依赖：

```bash
cd backend
pip install -r requirements.txt
```

## 验证修复

运行以下命令测试：
```bash
python -c "from pydantic_settings import BaseSettings; print('Success!')"
```

如果显示 "Success!"，则修复成功。

## 启动服务

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

修复已经完成，代码和依赖文件都已更新。 