
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta,timezone
from typing import Optional
import os

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")# 定义一个类
                
# JWT配置
SECRET_KEY = os.getenv("JWT_SECRET_KEY","your-secret-key-for-development")  # 在生产环境中应该使用环境变量
    
ALGORITHM = "HS256"
    
ACCESS_TOKEN_EXPIRE_MINUTES = 300
  

class PasswordUtils:
    """密码工具类"""
    
    @staticmethod
    def hash_password(password: str) -> str: # -> 返回值类型
        """加密密码"""
        return pwd_context.hash(password) 
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return pwd_context.verify(plain_password,hashed_password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):# data: dict - 要编码到令牌中的数据
                                      # expires_delta: Optional[timedelta] - 可选的过期时间增量
        """创建JWT访问令牌"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc)+ expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp":expire})
        encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str):
        """验证JWT令牌"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None
    @staticmethod
    def get_username_from_token(token:str):
        """从令牌中获取用户名"""
        payload = PasswordUtils.verify_token(token)
        if payload:
            return payload.get("sub") # sub是标准JWT字段，表示subject（主体）
        return None
        

