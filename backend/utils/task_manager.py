"""
异步任务管理器

提供后台任务的监控、重试和状态追踪功能
"""
import logging
import threading
import time
from typing import Callable, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import traceback

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = 'pending'      # 等待执行
    RUNNING = 'running'      # 正在执行
    SUCCESS = 'success'      # 执行成功
    FAILED = 'failed'        # 执行失败
    RETRYING = 'retrying'    # 正在重试


@dataclass
class TaskInfo:
    """任务信息数据类"""
    task_id: str
    task_name: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    result: Any = None
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            'task_id': self.task_id,
            'task_name': self.task_name,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'error_message': self.error_message,
            'retry_count': self.retry_count,
            'max_retries': self.max_retries,
            'has_result': self.result is not None
        }


class AsyncTaskManager:
    """
    异步任务管理器
    
    功能：
    1. 任务状态追踪
    2. 自动重试机制
    3. 错误日志记录
    4. 任务历史管理
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        self.tasks: Dict[str, TaskInfo] = {}
        self.active_threads: Dict[str, threading.Thread] = {}
        self.max_history = 100  # 最多保留的历史任务数
    
    def submit(
        self,
        func: Callable,
        args: tuple = (),
        kwargs: dict = None,
        task_name: str = None,
        max_retries: int = 3,
        callback: Callable = None
    ) -> str:
        """
        提交异步任务
        
        Args:
            func: 要执行的函数
            args: 位置参数
            kwargs: 关键字参数
            task_name: 任务名称（可选）
            max_retries: 最大重试次数
            callback: 完成后的回调函数
            
        Returns:
            str: 任务 ID
        """
        import uuid
        
        task_id = str(uuid.uuid4())[:8]
        task_name = task_name or func.__name__
        
        task_info = TaskInfo(
            task_id=task_id,
            task_name=task_name,
            max_retries=max_retries
        )
        
        self.tasks[task_id] = task_info
        
        thread = threading.Thread(
            target=self._execute_task,
            args=(func, args, kwargs or {}, task_info, callback),
            daemon=True,
            name=f"Task-{task_id}"
        )
        
        self.active_threads[task_id] = thread
        thread.start()
        
        logger.info(f"Task submitted: {task_id} ({task_name})")
        return task_id
    
    def _execute_task(
        self,
        func: Callable,
        args: tuple,
        kwargs: dict,
        task_info: TaskInfo,
        callback: Callable = None
    ):
        """
        执行任务（包含重试逻辑）
        
        Args:
            func: 要执行的函数
            args: 位置参数
            kwargs: 关键字参数
            task_info: 任务信息
            callback: 完成后的回调函数
        """
        while task_info.retry_count <= task_info.max_retries:
            try:
                # 更新状态为运行中
                task_info.status = TaskStatus.RUNNING
                task_info.started_at = datetime.now()
                
                logger.debug(f"Task {task_info.task_id} started execution")
                
                # 执行任务
                result = func(*args, **kwargs)
                
                # 执行成功
                task_info.status = TaskStatus.SUCCESS
                task_info.result = result
                task_info.completed_at = datetime.now()
                
                logger.info(f"Task {task_info.task_id} completed successfully")
                
                # 调用回调函数
                if callback:
                    try:
                        callback(task_info)
                    except Exception as e:
                        logger.error(f"Callback error for task {task_info.task_id}: {e}")
                
                return
                
            except Exception as e:
                task_info.retry_count += 1
                error_msg = f"{type(e).__name__}: {str(e)}"
                
                if task_info.retry_count <= task_info.max_retries:
                    # 需要重试
                    task_info.status = TaskStatus.RETRYING
                    task_info.error_message = f"Retry {task_info.retry_count}/{task_info.max_retries}: {error_msg}"
                    
                    logger.warning(
                        f"Task {task_info.task_id} failed, retrying "
                        f"({task_info.retry_count}/{task_info.max_retries}): {error_msg}"
                    )
                    
                    # 等待指数退避时间
                    wait_time = 2 ** (task_info.retry_count - 1)  # 1s, 2s, 4s...
                    time.sleep(wait_time)
                else:
                    # 达到最大重试次数，标记为失败
                    task_info.status = TaskStatus.FAILED
                    task_info.error_message = f"Failed after {task_info.retry_count} attempts: {error_msg}"
                    task_info.completed_at = datetime.now()
                    
                    logger.error(
                        f"Task {task_info.task_id} failed permanently: {error_msg}\n"
                        f"{traceback.format_exc()}"
                    )
                    
                    # 调用失败的回调
                    if callback:
                        try:
                            callback(task_info)
                        except Exception:
                            pass
                    
                    break
        
        # 清理活跃线程记录
        with self._lock:
            self.active_threads.pop(task_info.task_id, None)
        
        # 清理旧的历史记录
        self._cleanup_history()
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """
        获取任务状态
        
        Args:
            task_id: 任务 ID
            
        Returns:
            任务状态字典，不存在返回 None
        """
        task_info = self.tasks.get(task_id)
        if task_info:
            return task_info.to_dict()
        return None
    
    def is_task_running(self, task_id: str) -> bool:
        """
        检查任务是否正在运行
        
        Args:
            task_id: 任务 ID
            
        Returns:
            是否正在运行
        """
        task_info = self.tasks.get(task_id)
        if task_info:
            return task_info.status in [TaskStatus.PENDING, TaskStatus.RUNNING, TaskStatus.RETRYING]
        return False
    
    def _cleanup_history(self):
        """清理历史记录，保留最近的任务"""
        if len(self.tasks) > self.max_history:
            # 按创建时间排序，删除最老的任务
            sorted_tasks = sorted(
                self.tasks.items(),
                key=lambda x: x[1].created_at
            )
            
            tasks_to_remove = len(self.tasks) - self.max_history
            for task_id, _ in sorted_tasks[:tasks_to_remove]:
                self.tasks.pop(task_id, None)
            
            logger.debug(f"Cleaned up {tasks_to_remove} old task records")
    
    def get_all_tasks(self, limit: int = 20) -> list:
        """
        获取所有任务（按创建时间倒序）
        
        Args:
            limit: 返回数量限制
            
        Returns:
            任务列表
        """
        sorted_tasks = sorted(
            self.tasks.values(),
            key=lambda x: x.created_at,
            reverse=True
        )
        return [task.to_dict() for task in sorted_tasks[:limit]]


# 全局任务管理器实例
task_manager = AsyncTaskManager()


def async_task(func: Callable = None, max_retries: int = 3, task_name: str = None):
    """
    异步任务装饰器
    
    用法：
        @async_task
        def my_function():
            pass
        
        @async_task(max_retries=5, task_name="My Custom Task")
        def another_function():
            pass
    """
    def decorator(f):
        from functools import wraps
        
        @wraps(f)
        def wrapper(*args, **kwargs):
            return task_manager.submit(
                func=f,
                args=args,
                kwargs=kwargs,
                max_retries=max_retries,
                task_name=task_name
            )
        
        return wrapper
    
    if func:
        return decorator(func)
    return decorator
