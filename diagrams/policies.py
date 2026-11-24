"""Bilingual figure definitions. Each column is a node, or two parallel nodes.

Use '|' between languages and '~' for a line break. Return arrows are
(source column, destination column, label) and attach to the lower node.
Columns are zero-based. A leading '*' highlights a decision or representation.
"""
from dataclasses import dataclass


@dataclass
class Figure:
    key: str
    name: str
    url: str
    columns: list
    loops: list
    caption: str


DIRECT = [
    Figure("gpt4-trajectories", "Language Models as Zero-Shot Trajectory Generators",
           "https://www.robot-learning.uk/language-models-trajectory-generators",
           ["任务与感知接口|Task and~perception API", "*GPT-4~编写轨迹函数|*GPT-4 writes~trajectory code", "查询物体几何~计算密集位姿序列|Query geometry~compute EEF poses", "机械臂跟踪轨迹|Arm tracks~the trajectory"],
           [(3, 1, "执行后回传物体的三维跟踪记录；失败时重规划|Tracked 3D object motion lets GPT-4 assess and replan")],
           "作者让 GPT-4 写出计算轨迹的 Python 函数。抓碗失败时，模型读到的是碗在执行期间的位置变化，这次证据促使它改变下一次的抓点。|GPT-4 writes Python that computes the trajectory itself. In the bowl example, tracked object motion reveals a failed grasp and prompts a different grasp point on the next attempt."),
    Figure("astranomy-direct", "Astranomy · Direct",
           "https://research.nvidia.com/labs/srl/projects/astranomy/",
           ["图像、位姿~与任务|Views, pose~and task", "*GPT-6 Astra|*GPT-6 Astra",
            "*绝对末端位姿~与夹爪序列|*Absolute EEF poses~and gripper states", "本地控制器~驱动机械臂|Local controller~moves arm"],
           [(3, 0, "一段执行后，读取新图像与实测位姿|Read images and measured pose after the chunk")],
           "以作者公开的一版提示为例，模型一次写出 3–15 行绝对目标。罐子如果被碰走，下一次查询才会把偏差反映到新目标里。|In one published prompt the model writes 3–15 absolute targets per call. If the can shifts, the next query can revise the targets."),
    Figure("roboprobe", "RoboProbe · An Unexpected Robot Policy", "https://arxiv.org/html/2609.24170v1#S3",
           ["三路图像、状态~指令与剩余步数|Three views, state,~goal and budget", "*GPT-6 Astra~读笔记与调用历史|*GPT-6 Astra reads~notes and history", "*move_eef~指定双臂目标分量|*move_eef sets~arm target fields", "逆运动学与~关节控制|IK and~joint control"],
           [(3, 1, "运动结果、新观察写回；保留最近两轮图像|Append motion results and keep the latest two image turns")],
           "工具允许只更新部分目标分量，模型也可结束回合。一个动作写成函数调用，运动的几何目标依然由 GPT 决定。|The model may update a subset of target dimensions or end the episode. Although a function call carries the motion, GPT chooses its geometric target."),
    Figure("llm-libero", "LLM-LIBERO · From Reasoning to Action", "https://irvlutd.github.io/LLM-LIBERO/",
           ["前后两轮双视角~与机器人状态|Two recent views~per camera and state", "*GPT 等通用模型|*GPT or another~frontier model", "*move_to~填写末端目标|*move_to specifies~an EEF target", "适配器展开为~多个仿真控制步|Adapter expands~to controller steps"],
           [(3, 0, "动作后再观察；任务成败由 LIBERO 判定|Observe again after motion; LIBERO checks task success")],
           "这里只有一个运动入口，另有完成和放弃。一次模型调用可占用多个控制步，因此比较推理频率时要分清调用次数和仿真步数。|There is one motion command alongside done and give_up. A single call can consume several control steps, so model queries and simulator steps measure different things."),
    Figure("pear", "PEAR · Qwen3.8-27B", "https://mit-han-lab.github.io/pear-blog/",
           ["多视角图像~手臂状态与任务|Camera views,~arm state and task", "*27B 推理模型~读取回合历史|*27B reasoner~reads history",
            "*文本末端目标|*EEF target as text", "逆运动学与控制器~驱动机械臂|IK and controller~move arm"],
           [(3, 1, "新观察与本轮动作写入对话历史|Append the action and new observation to history")],
           "接口与 Astranomy Direct 都落在末端目标上。PEAR 的区别在训练端，仿真任务成败提供强化学习信号，推理时直接从观察给出下一步位姿。|PEAR and Astranomy Direct both emit EEF targets. PEAR learns this interface through task-outcome rewards in simulation and predicts the next pose from observations at deployment."),
]

AGENTIC = [
    Figure("saycan", "SayCan", "https://say-can.github.io/",
           [["指令与已选技能|Task and skill history", "机器人当前状态|Current robot state"],
            ["语言模型~给技能相关性打分|LM scores skill~relevance", "价值函数~给可行性打分|Value scores skill~feasibility"],
            "*分数相乘~选最高分技能|*Multiply scores~and select skill", "执行已训练的~技能策略|Execute selected~skill policy"],
           [(3, 0, "更新状态并记录所选技能，再选下一项|Update state and skill history before the next choice")],
           "候选技能先定好。即使语言模型认为“抓罐”最符合任务，当前状态的可行性分数也可以让另一项技能胜出。|The skill vocabulary is fixed. A grasp can be a good linguistic continuation and still lose to another skill when its feasibility in the current state is low."),
    Figure("guava", "Guava", "https://guava-harness.github.io/",
           ["图像、夹爪状态~与交互历史|Image, gripper~state and history", "*教师或~Guava-4B|*Teacher or~Guava-4B",
            "*一个工具名~及其参数|*One tool name~and arguments", "感知或操作工具~在环境中执行|Perception or~manipulation tool"],
           [(3, 1, "工具返回图像、状态与执行反馈，模型再决定|Tool evidence returns to the model for its next call")],
           "一次对齐只说明工具完成了对齐。模型在下一轮可以读反馈，再决定是否闭合夹爪。教师采集与学生部署使用同一组工具。|An alignment result only establishes alignment. The model reads the return before it can decide to close the gripper. Teacher and student share the tool interface."),
    Figure("k1", "Robo-Harness K1", "https://arxiv.org/abs/2609.29389",
           ["图像与任务|Image and task", "*VLM 发起~几何查询|*VLM queries~scene geometry", "标定深度、锚点~与抓取假设|Calibrated depth,~anchors and grasps",
            "*VLM 据此选择~通用运动|*VLM selects a~generic motion", "机械臂执行|Arm executes"],
           [(4, 0, "动作后再观察；锚点可跨查询引用|Observe again; anchors can be referenced across queries")],
           "几何查询本身可以不移动手臂。抓取前，模型可以引用同一个视觉锚点，检查尺度或深度，再决定怎么接近。|A geometry query can leave the arm still. The agent can refer to the same visual anchor, inspect size or depth, and only then choose an approach."),
    Figure("astranomy-agentic", "Astranomy · Agentic", "https://research.nvidia.com/labs/srl/projects/astranomy/",
           ["图像、任务~与机器人状态|Views, task~and robot state", "*Astra 持续会话~可用检查工具|*Persistent session~with optional tools",
            "*末端目标~与执行步数|*EEF target~and step count", "控制器执行|Controller acts"],
           [(3, 1, "观察和执行记录进入同一会话|Observations and actions accumulate in the same session")],
           "图中取末端控制配置。它与 Direct 共用相似的动作表达，关键变化是决策会话保留此前尝试，代理还可以按需检查图像或计算几何。|This is the EEF configuration. It retains a geometric action interface, while the decision session persists across attempts and can inspect images or run calculations."),
    Figure("code-as-policies", "Code as Policies", "https://code-as-policies.github.io/",
           ["指令与 API 示例|Instruction and~API examples", "*代码语言模型|*Code-generating LM", "*Python 策略~循环与条件|*Python policy~loops and tests", "感知 API~与控制原语|Perception APIs~and control calls"],
           [(3, 2, "感知值回到程序|Read sensor values")],
           "生成程序可以反复读取检测结果，直到满足条件才调用下一步。这样的反馈循环在本地程序内运行，每次判断都可复用已经写好的代码。|The generated program can query a detector until a condition holds. This feedback runs inside the program and reuses the same code at each check."),
    Figure("voxposer", "VoxPoser", "https://voxposer.github.io/",
           [["指令 → 模型写出~目标与约束代码|Task → LM writes~spatial constraints", "场景 → 视觉定位~与三维重建|Scene → grounded~3D observations"],
            "*合成三维值图|*Compose 3D~value maps", "运动规划器~求末端轨迹|Motion planner~solves trajectory", "机械臂执行|Arm executes"],
           [(3, 0, "新观察更新场景几何，重新计算值图与轨迹|Refresh scene geometry, then recompute maps and motion")],
           "“接近把手”和“远离杯子”可各写成一张图。两图合成后由规划器求动作，场景变化时可以重算几何而复用同一段代码。|Approach the handle and avoid the cup can be represented as separate maps. A planner acts on their composition; updated geometry can reuse the same program."),
    Figure("aspire", "ASPIRE", "https://research.nvidia.com/labs/gear/aspire/",
           ["任务与已验证技能|Task and~retrieved skills", "*编码代理~编写或修订程序|*Coding agent~writes or repairs",
            "执行策略程序~调用机器人 API|Run policy code~via robot APIs", "检查多模态记录~复跑验证|Inspect traces~and validate fixes", "*保存可复用技能|*Save validated~skill"],
           [(3, 1, "失败回溯到程序|Repair using the trace"),(4, 0, "新任务检索已验证的技能|Retrieve validated skills for future tasks")],
           "两条回路作用于不同时间。一次失败的视觉和调用记录帮助修改当前程序；通过复测的修复可进入技能库，供以后的任务检索。|The two returns operate at different times. A trace can repair the current program. A validated repair can enter the skill library for retrieval on a later task."),
    Figure("openrua", "OpenRUA", "https://arxiv.org/abs/2610.02459",
           ["任务与 ROS 2 文档|Task and~ROS 2 docs", "*终端中的~代码代理|*Coding agent~in a terminal", "读传感器文件~编写控制程序|Read sensor files~write control code", "调用原生 ROS 2~接口执行|Execute via~native ROS 2"],
           [(3, 1, "读取新传感器文件和终端结果|Read new sensor files and terminal outputs")],
           "这里交给代理的是带文档的工作区。采用哪段观察程序、发哪个 ROS 2 命令、怎样组织重试，均由代理在工作区中安排。|The interface is a documented workspace. The agent organizes observation scripts, ROS 2 commands and retries using its terminal."),
    Figure("uni-robot-agent", "uni-robot-agent", "https://arxiv.org/abs/2611.01560",
           ["任务、相机图像~与状态|Task, images~and robot state", "*开放权重模型|*Open-weight~model",
            "统一工具接口~感知、代码与动作|Shared tools for~vision, code, action", "仿真或真机后端|Simulation or~physical backend"],
           [(3, 1, "统一格式的观察和结果返回模型|Common observations and tool results return to the model")],
           "OpenRUA 从原生 ROS 2 起步，这项工作统一了不同后端的工具协议。论文的无深度实例中，代理用多视角像素、相机参数和自写代码三角定位。|OpenRUA starts from native ROS 2. This work standardizes tools across backends. In a no-depth example, the agent triangulates from multiple views using calibration and its own code."),
]

CASE = [
    Figure("piper-term", "Piper · TERM", "", ["学生的一次~工具请求|Student issues~a tool request",
           "*工具执行与纠偏~记录实际动作|*Tool executes~and logs corrections", "核验结果~对齐监督标签|Verify result~and align labels",
           "*筛选轨迹~微调学生|*Fine-tune on~retained traces", "切回原工具~评测学生|Evaluate student~with original tools"],
           [], "这里画的是跨轨迹的训练与评测流程。把学生的请求、工具实际执行的动作和事后观察分开记录，才能检查提升是否随学生权重保留下来。|This is the cross-episode training and evaluation path. Logging the request, executed action and later observation separately makes it possible to test what persists in the student weights."),
]
