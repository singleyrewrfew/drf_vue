"""
异步任务管理器

提供简单的线程池任务管理，用于处理视频缩略图生成等耗时操作。
"""
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, Future
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskInfo:
    """任务信息"""
    task_id: str
    task_name: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    result: Optional[object] = None


class TaskManager:
    """
    简易任务管理器

    使用线程池执行异步任务，提供任务状态跟踪和回调机制。
    适用于视频缩略图生成、文件处理等耗时操作。
    """

    def __init__(self, max_workers: int = 4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.tasks: dict[str, TaskInfo] = {}
        self._lock = threading.Lock()
        logger.info(f"TaskManager initialized with {max_workers} workers")

    def submit(
        self,
        func: Callable,
        task_name: str = "unnamed_task",
        max_retries: int = 0,
        callback: Optional[Callable[[TaskInfo], None]] = None
    ) -> TaskInfo:
        """
        提交异步任务

        Args:
            func: 要执行的函数
            task_name: 任务名称（用于日志和追踪）
            max_retries: 最大重试次数
            callback: 任务完成后的回调函数

        Returns:
            TaskInfo: 任务信息对象
        """
        task_id = str(uuid.uuid4())
        task_info = TaskInfo(task_id=task_id, task_name=task_name)

        with self._lock:
            self.tasks[task_id] = task_info

        logger.info(f"[TaskManager] Submitting task '{task_name}' (ID: {task_id})")

        def _execute_with_retry():
            retries = 0
            while retries <= max_retries:
                try:
                    with self._lock:
                        task_info.status = TaskStatus.RUNNING
                        task_info.started_at = datetime.now()

                    logger.debug(f"[TaskManager] Executing task '{task_name}' (attempt {retries + 1})")
                    result = func()

                    with self._lock:
                        task_info.status = TaskStatus.COMPLETED
                        task_info.completed_at = datetime.now()
                        task_info.result = result

                    logger.info(f"[TaskManager] Task '{task_name}' completed successfully")

                    if callback:
                        try:
                            callback(task_info)
                        except Exception as e:
                            logger.error(f"[TaskManager] Callback error: {e}")

                    return result

                except Exception as e:
                    retries += 1
                    logger.warning(
                        f"[TaskManager] Task '{task_name}' failed (attempt {retries}/{max_retries + 1}): {e}"
                    )

                    if retries > max_retries:
                        with self._lock:
                            task_info.status = TaskStatus.FAILED
                            task_info.completed_at = datetime.now()
                            task_info.error = str(e)

                        logger.error(f"[TaskManager] Task '{task_name}' failed after {retries} attempts")

                        if callback:
                            try:
                                callback(task_info)
                            except Exception as cb_error:
                                logger.error(f"[TaskManager] Callback error: {cb_error}")

                        raise

        # 提交到线程池
        future: Future = self.executor.submit(_execute_with_retry)
        task_info.result = future  # 保存 future 对象供外部查询

        return task_info

    def get_task(self, task_id: str) -> Optional[TaskInfo]:
        """获取任务信息"""
        with self._lock:
            return self.tasks.get(task_id)

    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        with self._lock:
            task_info = self.tasks.get(task_id)
            if not task_info:
                return False

            if task_info.status in (TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED):
                return False

            if isinstance(task_info.result, Future):
                cancelled = task_info.result.cancel()
                if cancelled:
                    task_info.status = TaskStatus.CANCELLED
                    logger.info(f"[TaskManager] Task '{task_info.task_name}' cancelled")
                return cancelled

            return False

    def shutdown(self, wait: bool = True):
        """关闭任务管理器"""
        logger.info("Shutting down TaskManager...")
        self.executor.shutdown(wait=wait)


# 全局单例
task_manager = TaskManager(max_workers=3)
