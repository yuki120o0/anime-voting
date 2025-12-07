# api/index.py
import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入你的FastAPI应用
try:
    from main import app
    print("✅ 成功导入FastAPI应用")
except ImportError as e:
    print(f"❌ 导入应用失败: {e}")
    raise

# Vercel需要这个handler
from mangum import Mangum
handler = Mangum(app, lifespan="off")

# 本地测试
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
