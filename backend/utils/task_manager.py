"""
异步任务管理器

提供简单的线程池任务管理，用于处理视频缩略图生成等耗时操作。

作用：封装 ThreadPoolExecutor，提供任务状态跟踪、重试机制和回调功能
使用：从 utils.task_manager 导入 task_manager 单例，调用 submit() 提交任务

主要功能：
    1. 异步任务执行 - 在线程池中后台执行耗时操作
    2. 任务状态跟踪 - 实时查询任务状态（PENDING/RUNNING/COMPLETED/FAILED/CANCELLED）
    3. 自动重试机制 - 支持配置最大重试次数
    4. 完成回调 - 任务完成后执行自定义回调函数
    5. 任务取消 - 支持取消尚未开始执行的任务

适用场景：
    - 视频缩略图生成
    - 图片处理和压缩
    - 文件上传和处理
    - 邮件发送
    - 其他耗时且不需要立即返回结果的操作

线程安全：
    - 使用 threading.Lock 保护 tasks 字典的并发访问
    - 任务状态更新是原子操作
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
    """
    任务状态枚举
    
    定义任务在其生命周期中可能处于的各种状态。
    
    状态流转：
        PENDING -> RUNNING -> COMPLETED  (成功路径)
        PENDING -> RUNNING -> FAILED     (失败路径)
        PENDING -> CANCELLED             (取消路径)
    
    状态说明：
        PENDING   - 任务已提交，等待执行
        RUNNING   - 任务正在执行中
        COMPLETED - 任务成功完成
        FAILED    - 任务执行失败（已达到最大重试次数）
        CANCELLED - 任务已被取消
    """
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskInfo:
    """
    任务信息数据类
    
    存储任务的完整生命周期信息，包括状态、时间戳、结果和错误信息。
    使用 dataclass 简化数据对象的创建和管理。
    
    属性：
        task_id (str): 任务的唯一标识符（UUID）
        task_name (str): 任务的名称，用于日志和追踪
        status (TaskStatus): 当前任务状态，默认为 PENDING
        created_at (datetime): 任务创建时间
        started_at (Optional[datetime]): 任务开始执行时间，未开始时为 None
        completed_at (Optional[datetime]): 任务完成时间，未完成时为 None
        error (Optional[str]): 错误信息，任务失败时记录异常消息
        result (Optional[object]): 任务执行结果或 Future 对象
    
    使用示例：
        task_info = TaskInfo(
            task_id='uuid-123',
            task_name='generate_thumbnail'
        )
    """
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
    
    核心特性：
        - 基于 ThreadPoolExecutor 实现线程池管理
        - 支持任务重试机制（可配置最大重试次数）
        - 提供任务完成回调函数
        - 线程安全的任务状态管理
        - 支持任务取消（仅限未开始执行的任务）
    
    使用示例：
        from utils.task_manager import task_manager
        
        def my_task():
            # 耗时操作
            return result
        
        # 提交任务
        task_info = task_manager.submit(
            func=my_task,
            task_name='my_task',
            max_retries=2,
            callback=lambda task: print(f'Task {task.task_id} completed')
        )
        
        # 查询任务状态
        task_info = task_manager.get_task(task_info.task_id)
        print(task_info.status)
    
    注意事项：
        - 任务函数应该是线程安全的
        - 避免在任务中执行阻塞 I/O 操作（应使用异步 I/O）
        - 任务数量不应超过线程池容量的太多倍，否则会导致排队
    """

    def __init__(self, max_workers: int = 4):
        """
        初始化任务管理器
        
        Args:
            max_workers (int): 线程池的最大工作线程数，默认为 4
                - 建议设置为 CPU 核心数的 1-2 倍
                - 对于 I/O 密集型任务可以适当增加
                - 对于 CPU 密集型任务应该减少
        
        初始化内容：
            - 创建 ThreadPoolExecutor 实例
            - 初始化任务字典用于存储任务信息
            - 创建线程锁用于保护共享资源
        
        注意：
            - max_workers 不宜设置过大，否则会导致上下文切换开销增加
            - 应根据实际负载和服务器资源调整
        """
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
        提交异步任务到线程池执行
        
        将任务函数提交到线程池中异步执行，支持重试机制和完成回调。
        任务立即返回 TaskInfo 对象，实际执行在后台线程中进行。
        
        Args:
            func (Callable): 要执行的函数，应该是无参数的 callable 对象
                - 如果需要传递参数，可以使用 functools.partial 或 lambda
                - 函数应该是线程安全的
            task_name (str): 任务名称，用于日志记录和追踪，默认为 'unnamed_task'
                - 建议使用有意义的名称便于调试
            max_retries (int): 最大重试次数，默认为 0（不重试）
                - 设置为 0 表示失败后不重试
                - 设置为 N 表示最多重试 N 次（总共执行 N+1 次）
            callback (Optional[Callable]): 任务完成后的回调函数，可选
                - 接收 TaskInfo 对象作为参数
                - 无论任务成功还是失败都会调用
                - 回调中的异常会被捕获并记录，不会影响任务状态
        
        Returns:
            TaskInfo: 任务信息对象，包含 task_id 和初始状态
                - 可以通过 task_id 后续查询任务状态
                - result 字段保存了 Future 对象，可用于更高级的控制
        
        执行流程：
            1. 生成唯一的 task_id
            2. 创建 TaskInfo 对象并保存到 tasks 字典
            3. 提交内部包装函数到线程池
            4. 包装函数执行时会：
               a. 更新状态为 RUNNING
               b. 执行用户函数
               c. 如果成功，更新状态为 COMPLETED 并保存结果
               d. 如果失败且还有重试次数，重新执行
               e. 如果失败且达到最大重试次数，更新状态为 FAILED
               f. 执行回调函数（如果有）
        
        线程安全：
            - 任务提交和状态更新都使用了锁保护
            - 多个线程可以同时提交任务
        
        使用示例：
            # 简单任务
            task_info = task_manager.submit(
                func=lambda: process_video('video.mp4'),
                task_name='process_video'
            )
            
            # 带重试和回调的任务
            def on_complete(task):
                if task.status == TaskStatus.COMPLETED:
                    send_notification(f'Task {task.task_id} completed')
                else:
                    log_error(f'Task {task.task_id} failed: {task.error}')
            
            task_info = task_manager.submit(
                func=upload_file,
                task_name='upload_file',
                max_retries=3,
                callback=on_complete
            )
        
        注意：
            - 任务函数中的异常会被捕获，不会传播到调用者
            - 如果需要获取任务结果，应该通过回调或轮询 task_info.result
            - task_info.result 可能是 Future 对象（任务未完成时）或实际结果（任务完成后）
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

        # 提交到线程池执行
        # future 对象可以用于更高级的任务控制（如取消、超时等）
        future: Future = self.executor.submit(_execute_with_retry)
        task_info.result = future  # 保存 future 对象供外部查询

        return task_info

    def get_task(self, task_id: str) -> Optional[TaskInfo]:
        """
        获取任务信息
        
        根据任务 ID 查询任务的当前状态和相关信息。
        
        Args:
            task_id (str): 任务的唯一标识符
        
        Returns:
            Optional[TaskInfo]: 任务信息对象，如果任务不存在则返回 None
                - 返回的对象包含任务的最新状态
                - 如果任务已完成，result 字段包含执行结果
                - 如果任务失败，error 字段包含错误信息
        
        线程安全：
            - 使用锁保护 tasks 字典的读取操作
            - 返回的是 TaskInfo 对象的引用，后续状态变化会反映在该对象上
        
        使用示例：
            task_info = task_manager.get_task('uuid-123')
            if task_info:
                print(f'Status: {task_info.status}')
                print(f'Result: {task_info.result}')
            else:
                print('Task not found')
        
        注意：
            - 如果任务还在执行中，result 字段可能是 Future 对象
            - 应该在任务完成后才访问 result 获取实际结果
        """
        with self._lock:
            return self.tasks.get(task_id)

    def cancel_task(self, task_id: str) -> bool:
        """
        取消任务
        
        尝试取消指定 ID 的任务。只能取消尚未开始执行的任务（PENDING 状态）。
        如果任务已经在运行（RUNNING 状态），则无法取消。
        
        Args:
            task_id (str): 要取消的任务的唯一标识符
        
        Returns:
            bool: 是否成功取消
                - True: 任务成功取消
                - False: 任务不存在、已完成、已失败或已在运行中无法取消
        
        取消规则：
            - 只能取消 PENDING 状态的任务
            - RUNNING 状态的任务无法取消（因为已经开始执行）
            - COMPLETED、FAILED、CANCELLED 状态的任务无需取消
        
        线程安全：
            - 使用锁保护任务状态的检查和更新
            - 确保取消操作的原子性
        
        使用示例：
            task_info = task_manager.submit(long_running_task)
            
            # 如果发现任务不需要执行了，尝试取消
            if task_manager.cancel_task(task_info.task_id):
                print('Task cancelled successfully')
            else:
                print('Task cannot be cancelled (already running or completed)')
        
        注意：
            - 取消操作只对未来对象生效，如果任务已经开始执行则无效
            - 被取消的任务状态会更新为 CANCELLED
            - 取消操作不会触发回调函数
        """
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
        """
        关闭任务管理器
        
        优雅地关闭线程池，停止接受新任务并等待现有任务完成。
        通常在应用程序退出时调用。
        
        Args:
            wait (bool): 是否等待所有 pending 的任务执行完毕
                - True: 等待所有任务完成后才返回（默认）
                - False: 立即返回，未执行完的任务会被中断
        
        关闭流程：
            1. 记录关闭日志
            2. 调用 executor.shutdown() 关闭线程池
            3. 如果 wait=True，阻塞直到所有任务完成
            4. 释放线程资源
        
        使用示例：
            # 应用程序退出时
            import atexit
            atexit.register(task_manager.shutdown)
            
            # 或者手动关闭
            task_manager.shutdown(wait=True)
        
        注意：
            - 关闭后不能再提交新任务
            - 建议在应用程序退出时调用，确保资源正确释放
            - 如果 wait=False，可能导致任务执行不完整
        """
        logger.info("Shutting down TaskManager...")
        self.executor.shutdown(wait=wait)


# ==============================================================================
# 全局单例
# ==============================================================================
# 创建全局 TaskManager 单例，max_workers=3 适合大多数 Web 应用场景
# 
# 使用方式：
#     from utils.task_manager import task_manager
#     task_info = task_manager.submit(my_function)
#
# 配置建议：
#     - Web 应用：3-4 个工作线程（I/O 密集型）
#     - 数据处理：根据 CPU 核心数调整
#     - 高并发场景：可以考虑使用多个 TaskManager 实例
# ==============================================================================
task_manager = TaskManager(max_workers=3)
