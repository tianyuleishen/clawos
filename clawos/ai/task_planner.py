# 🦞 Task Planner - 任务规划器

"""
任务规划 - 智能任务分解和执行

功能:
- 任务分解
- 依赖分析
- 执行计划生成
- 执行监控
"""

import asyncio
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from collections import deque
import uuid
import time

class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"      # 等待
    RUNNING = "running"     # 运行中
    COMPLETED = "completed" # 完成
    FAILED = "failed"       # 失败
    CANCELLED = "cancelled" # 取消
    SKIPPED = "skipped"     # 跳过


class TaskPriority(Enum):
    """任务优先级"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


@dataclass
class Task:
    """任务"""
    id: str
    name: str
    description: str
    action: str           # 要执行的命令/动作
    status: TaskStatus
    priority: TaskPriority
    dependencies: List[str]  # 依赖的任务ID
    depends_on_me: List[str] # 依赖我的任务ID
    created_at: float
    started_at: float = None
    completed_at: float = None
    result: Any = None
    error: str = None
    retry_count: int = 0
    max_retries: int = 3
    estimated_duration: float = 0.0  # 预估时间(秒)
    actual_duration: float = 0.0
    
    # 元数据
    metadata: Dict = field(default_factory=dict)


@dataclass
class TaskPlan:
    """任务计划"""
    id: str
    name: str
    description: str
    tasks: List[Task]
    created_at: float
    started_at: float = None
    completed_at: float = None
    status: TaskStatus = TaskStatus.PENDING
    total_duration: float = 0.0
    success_count: int = 0
    failed_count: int = 0
    
    # 元数据
    metadata: Dict = field(default_factory=dict)


@dataclass
class ExecutionResult:
    """执行结果"""
    task_id: str
    success: bool
    result: Any
    error: str
    duration: float
    timestamp: float


class TaskPlanner:
    """任务规划器"""
    
    def __init__(self):
        self.plans: Dict[str, TaskPlan] = {}
        self.executors: Dict[str, Callable] = {}
        print("✅ Task Planner 已加载")
    
    # ============ 任务创建 ============
    
    def create_task(
        self,
        name: str,
        action: str,
        description: str = "",
        priority: TaskPriority = TaskPriority.MEDIUM,
        dependencies: List[str] = None,
        estimated_duration: float = 0.0,
        metadata: Dict = None
    ) -> Task:
        """创建任务
        
        Args:
            name: 任务名称
            action: 执行动作
            description: 描述
            priority: 优先级
            dependencies: 依赖的任务ID列表
            estimated_duration: 预估时间
            metadata: 元数据
        
        Returns:
            Task: 创建的任务
        """
        return Task(
            id=str(uuid.uuid4())[:8],
            name=name,
            description=description,
            action=action,
            status=TaskStatus.PENDING,
            priority=priority,
            dependencies=dependencies or [],
            depends_on_me=[],
            created_at=time.time(),
            estimated_duration=estimated_duration,
            metadata=metadata or {}
        )
    
    # ============ 计划创建 ============
    
    def create_plan(
        self,
        name: str,
        description: str = "",
        tasks: List[Task] = None,
        metadata: Dict = None
    ) -> TaskPlan:
        """创建任务计划
        
        Args:
            name: 计划名称
            description: 描述
            tasks: 初始任务列表
            metadata: 元数据
        
        Returns:
            TaskPlan: 创建的计划
        """
        plan = TaskPlan(
            id=str(uuid.uuid4())[:8],
            name=name,
            description=description,
            tasks=tasks or [],
            created_at=time.time(),
            metadata=metadata or {}
        )
        
        self.plans[plan.id] = plan
        
        # 建立依赖关系
        self._build_dependencies(plan)
        
        return plan
    
    def _build_dependencies(self, plan: TaskPlan):
        """建立任务依赖关系"""
        # 创建依赖映射
        task_map = {task.id: task for task in plan.tasks}
        
        for task in plan.tasks:
            task.depends_on_me = []
            
            # 检查依赖
            for dep_id in task.dependencies:
                if dep_id in task_map:
                    task_map[dep_id].depends_on_me.append(task.id)
    
    # ============ 智能任务分解 ============
    
    async def decompose(
        self,
        goal: str,
        nlu_result = None
    ) -> TaskPlan:
        """智能分解任务
        
        Args:
            goal: 用户目标
            nlu_result: NLU解析结果
        
        Returns:
            TaskPlan: 任务计划
        """
        tasks = []
        
        # 根据意图分解任务
        if nlu_result:
            intent = nlu_result.primary_intent
            
            if intent.type.value.startswith("launch"):
                # 启动应用
                app_name = intent.slots.get("app_name", "unknown")
                tasks.append(self.create_task(
                    name=f"启动{app_name}",
                    action=f"launch_app:{app_name}",
                    description=f"启动应用程序 {app_name}",
                    priority=TaskPriority.HIGH
                ))
            
            elif intent.type.value.startswith("close"):
                # 关闭应用
                app_name = intent.slots.get("app_name", "unknown")
                tasks.append(self.create_task(
                    name=f"关闭{app_name}",
                    action=f"close_app:{app_name}",
                    description=f"关闭应用程序 {app_name}",
                    priority=TaskPriority.MEDIUM
                ))
            
            elif intent.type.value in ["open_url", "search_web"]:
                # 打开URL或搜索
                url = intent.slots.get("url", "")
                if url:
                    tasks.append(self.create_task(
                        name="打开网页",
                        action=f"open_url:{url}",
                        description=f"打开网址 {url}",
                        priority=TaskPriority.HIGH
                    ))
            
            elif intent.type == IntentType.SCREENSHOT:
                # 截图
                tasks.append(self.create_task(
                    name="屏幕截图",
                    action="screenshot",
                    description="截取当前屏幕",
                    priority=TaskPriority.LOW
                ))
            
            elif intent.type == IntentType.CALCULATE:
                # 计算
                expression = intent.slots.get("expression", "")
                tasks.append(self.create_task(
                    name="执行计算",
                    action=f"calculate:{expression}",
                    description=f"计算 {expression}",
                    priority=TaskPriority.MEDIUM
                ))
            
            else:
                # 默认: 对话任务
                tasks.append(self.create_task(
                    name="处理请求",
                    action=f"chat:{goal}",
                    description=f"处理用户请求: {goal}",
                    priority=TaskPriority.MEDIUM
                ))
        else:
            # 默认处理
            tasks.append(self.create_task(
                name="处理请求",
                action=f"chat:{goal}",
                description=f"处理用户请求: {goal}",
                priority=TaskPriority.MEDIUM
            ))
        
        # 创建计划
        return self.create_plan(
            name=f"任务: {goal[:50]}",
            description=f"自动分解的任务计划: {goal}",
            tasks=tasks
        )
    
    # ============ 任务执行 ============
    
    async def execute_plan(
        self, 
        plan_id: str,
        on_task_start: Callable[[Task], None] = None,
        on_task_complete: Callable[[Task, ExecutionResult], None] = None,
        on_plan_complete: Callable[[TaskPlan], None] = None
    ) -> TaskPlan:
        """执行任务计划
        
        Args:
            plan_id: 计划ID
            on_task_start: 任务开始回调
            on_task_complete: 任务完成回调
            on_plan_complete: 计划完成回调
        
        Returns:
            TaskPlan: 执行完成的计划
        """
        if plan_id not in self.plans:
            raise ValueError(f"计划不存在: {plan_id}")
        
        plan = self.plans[plan_id]
        plan.started_at = time.time()
        plan.status = TaskStatus.RUNNING
        
        # 拓扑排序确定执行顺序
        execution_order = self._topological_sort(plan)
        
        # 执行每个任务
        for task_id in execution_order:
            task = next((t for t in plan.tasks if t.id == task_id), None)
            if not task:
                continue
            
            # 检查是否被跳过
            if task.status == TaskStatus.SKIPPED:
                continue
            
            # 执行任务
            result = await self._execute_task(task, plan)
            
            # 回调
            if on_task_start:
                on_task_start(task)
            
            if on_task_complete:
                on_task_complete(task, result)
        
        plan.completed_at = time.time()
        plan.total_duration = plan.completed_at - plan.started_at
        plan.status = TaskStatus.COMPLETED if plan.failed_count == 0 else TaskStatus.FAILED
        
        # 计划完成回调
        if on_plan_complete:
            on_plan_complete(plan)
        
        return plan
    
    async def _execute_task(self, task: Task, plan: TaskPlan) -> ExecutionResult:
        """执行单个任务"""
        start_time = time.time()
        task.started_at = start_time
        task.status = TaskStatus.RUNNING
        
        try:
            # 获取执行器
            executor = self.executors.get(task.action.split(':')[0])
            
            if executor:
                # 执行
                result = await executor(task)
                task.result = result
                task.status = TaskStatus.COMPLETED
                task.success_count += 1
            else:
                # 模拟执行
                await asyncio.sleep(0.1)
                task.result = {"action": task.action, "status": "simulated"}
                task.status = TaskStatus.COMPLETED
                task.success_count += 1
            
        except Exception as e:
            task.error = str(e)
            task.retry_count += 1
            
            if task.retry_count < task.max_retries:
                # 重试
                task.status = TaskStatus.PENDING
            else:
                task.status = TaskStatus.FAILED
                task.failed_count += 1
        
        finally:
            task.completed_at = time.time()
            task.actual_duration = task.completed_at - task.started_at
        
        return ExecutionResult(
            task_id=task.id,
            success=task.status == TaskStatus.COMPLETED,
            result=task.result,
            error=task.error,
            duration=task.actual_duration,
            timestamp=time.time()
        )
    
    def _topological_sort(self, plan: TaskPlan) -> List[str]:
        """拓扑排序 (确定执行顺序)"""
        # 构建依赖图
        graph = {task.id: task.depends_on_me for task in plan.tasks}
        
        # 计算入度
        in_degree = {task.id: 0 for task in plan.tasks}
        for task in plan.tasks:
            for dep in task.dependencies:
                if dep in in_degree:
                    in_degree[task.id] += 1
        
        # 优先级排序
        priority_queue = deque()
        for task_id, degree in in_degree.items():
            if degree == 0:
                priority_queue.append(task_id)
        
        result = []
        
        while priority_queue:
            # 按优先级排序
            tasks_in_queue = [(self._get_task(plan, tid).priority.value, tid) for tid in priority_queue]
            tasks_in_queue.sort(key=lambda x: -x[0])  # 高优先级在前
            
            _, current = tasks_in_queue[0]
            priority_queue.remove(current)
            
            result.append(current)
            
            # 更新入度
            for task in plan.tasks:
                if current in task.dependencies:
                    in_degree[task.id] -= 1
                    if in_degree[task.id] == 0:
                        priority_queue.append(task.id)
        
        return result
    
    def _get_task(self, plan: TaskPlan, task_id: str) -> Task:
        """获取任务"""
        return next((t for t in plan.tasks if t.id == task_id), None)
    
    # ============ 执行器注册 ============
    
    def register_executor(self, name: str, executor: Callable):
        """注册执行器
        
        Args:
            name: 执行器名称
            executor: 执行函数
        """
        self.executors[name] = executor
    
    # ============ 计划管理 ============
    
    def get_plan(self, plan_id: str) -> Optional[TaskPlan]:
        """获取计划"""
        return self.plans.get(plan_id)
    
    def list_plans(self) -> List[TaskPlan]:
        """列出所有计划"""
        return list(self.plans.values())
    
    def cancel_plan(self, plan_id: str) -> bool:
        """取消计划"""
        if plan_id in self.plans:
            plan = self.plans[plan_id]
            for task in plan.tasks:
                if task.status == TaskStatus.RUNNING:
                    task.status = TaskStatus.CANCELLED
            plan.status = TaskStatus.CANCELLED
            return True
        return False
    
    def delete_plan(self, plan_id: str):
        """删除计划"""
        if plan_id in self.plans:
            del self.plans[plan_id]
    
    # ============ 状态查询 ============
    
    def get_plan_status(self, plan_id: str) -> Dict:
        """获取计划状态"""
        plan = self.plans.get(plan_id)
        if not plan:
            return None
        
        return {
            "plan_id": plan.id,
            "name": plan.name,
            "status": plan.status.value,
            "total_tasks": len(plan.tasks),
            "completed_tasks": sum(1 for t in plan.tasks if t.status == TaskStatus.COMPLETED),
            "failed_tasks": sum(1 for t in plan.tasks if t.status == TaskStatus.FAILED),
            "pending_tasks": sum(1 for t in plan.tasks if t.status == TaskStatus.PENDING),
            "total_duration": plan.total_duration,
            "created_at": datetime.fromtimestamp(plan.created_at).isoformat(),
            "started_at": datetime.fromtimestamp(plan.started_at).isoformat() if plan.started_at else None,
        }
    
    def get_task_status(self, plan_id: str, task_id: str) -> Dict:
        """获取任务状态"""
        plan = self.plans.get(plan_id)
        if not plan:
            return None
        
        task = self._get_task(plan, task_id)
        if not task:
            return None
        
        return {
            "task_id": task.id,
            "name": task.name,
            "status": task.status.value,
            "priority": task.priority.name,
            "duration": task.actual_duration,
            "retry_count": task.retry_count,
            "error": task.error,
        }
    
    # ============ 便捷方法 ============
    
    async def plan_and_execute(
        self,
        goal: str,
        nlu_result = None
    ) -> TaskPlan:
        """规划和执行
        
        Args:
            goal: 用户目标
            nlu_result: NLU解析结果
        
        Returns:
            TaskPlan: 执行完成的计划
        """
        # 分解任务
        plan = await self.decompose(goal, nlu_result)
        
        # 执行
        await self.execute_plan(plan.id)
        
        return plan


# 导入IntentType (循环导入避免)
import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace')
from clawos.ai.nlu import IntentType

# 便捷函数
async def plan_task(goal: str, nlu_result = None) -> TaskPlan:
    """规划任务"""
    planner = TaskPlanner()
    return await planner.decompose(goal, nlu_result)

async def execute_plan(plan_id: str) -> TaskPlan:
    """执行计划"""
    planner = TaskPlanner()
    return await planner.execute_plan(plan_id)

# 测试代码
if __name__ == "__main__":
    async def test():
        print("📋 任务规划器测试")
        
        planner = TaskPlanner()
        
        # 创建任务
        print("\n1. 创建任务...")
        task1 = planner.create_task(
            name="打开浏览器",
            action="launch_app:chrome",
            description="启动Chrome浏览器",
            priority=TaskPriority.HIGH
        )
        task2 = planner.create_task(
            name="搜索内容",
            action="search:AI助手",
            description="搜索AI助手相关信息",
            dependencies=[task1.id],
            priority=TaskPriority.MEDIUM
        )
        task3 = planner.create_task(
            name="关闭浏览器",
            action="close_app:chrome",
            description="关闭Chrome浏览器",
            dependencies=[task2.id],
            priority=TaskPriority.LOW
        )
        
        # 创建计划
        print("\n2. 创建计划...")
        plan = planner.create_plan(
            name="浏览和搜索",
            description="自动化的网页浏览任务",
            tasks=[task1, task2, task3]
        )
        print(f"   计划ID: {plan.id}")
        print(f"   任务数: {len(plan.tasks)}")
        
        # 拓扑排序
        order = planner._topological_sort(plan)
        print(f"   执行顺序: {order}")
        
        # 智能分解测试
        print("\n3. 智能分解...")
        from clawos.ai.nlu import IntentType
        mock_nlu = type('MockNLU', (), {
            'primary_intent': type('MockIntent', (), {
                'type': IntentType.LAUNCH_APP,
                'slots': {'app_name': 'Chrome'}
            })()
        })()
        
        simple_plan = await planner.decompose("打开Chrome浏览器", mock_nlu)
        print(f"   分解任务数: {len(simple_plan.tasks)}")
        
        print("\n✅ 测试完成")
    
    asyncio.run(test())
