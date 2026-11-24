# Direct Policy：GPT 直接给出末端动作

把罐子往旁边挪两厘米，再给模型看一帧。它的下一条输出里，哪几个量应该随之变化？这个问题能把“模型直接控制机器人”拆成两种可检查的做法。
## 末端位姿里的六个量
末端执行器（end effector，EEF）在这里指夹爪。给出它在空间中的位置和朝向需要六个自由度，夹爪开合通常另给一个量。例如，要从上往下抓罐子，可以先发“到罐口上方、保持夹爪张开”，下一步下降，再闭合。前一句落实成数据，就要写清相对哪个坐标系、目标是绝对位置还是当前位置的增量、距离用米还是毫米。旋转还要约定表示方法。

一条典型链路是 **图像与指令 → 模型给末端目标 → 逆运动学求关节位置 → 控制器跟踪 → 再拍一帧**。中间有两个不同的反馈回路。关节控制器用编码器反馈减小跟踪误差；模型用新图像判断刚才那一步有没有推动任务。夹爪准确到达旧目标、罐子却被碰走，两个回路会同时给出看似相反、其实都正确的答案。

**Astranomy 把两层的责任划得很清楚。** 作者让 GPT-6 Astra 直接生成动作，也让它在有持续历史的代理环境中工作，或审阅由另一个模型提出的动作。在 RoboLab-120 上，三者分别得到 66.3%、74.8%、66.5%。代理比直接输出高 8.5 个百分点，但作者的消融发现，保留交互历史有用，额外增加工具没有显示进一步增益。若只摘最高分，很容易把“记得上次试过什么”误解为“工具越多越好”。[作者研究博客、提示与回放](https://research.nvidia.com/labs/srl/projects/astranomy/)
在 Astranomy 公开的一版 Direct 提示中，一行含八个量：基座坐标系中的三维位置、单位四元数和夹爪开关。策略一次提交 3–15 行绝对目标，本地按 15 Hz 执行，每行占一个控制间隔，再把新图像和实测位姿送回。瞄准点定义在夹爪法兰，规划指垫落点还要考虑偏移。这个例子还有一个容易忽略的细节：消息虽然通过函数调用提交，函数里装的仍是一串由 GPT 自己决定的位姿。因此判断是否属于 Direct Policy，应该读参数，而不能只看消息有没有工具名。[Astranomy 公开动作协议](https://research.nvidia.com/labs/srl/projects/astranomy/)

## 没有专家动作，能学到抓取吗？
**PEAR** 让一个 27B 推理模型在仿真中自行尝试。模型输出末端动作，仿真执行，任务奖励对轨迹给出学习信号。和行为克隆相比，它省去每一步该怎么动的专家标签，但要付出足够多的仿真尝试，还要确保奖励对应真正想要的行为。作者在 LIBERO 上从 1.6% 提高到 74.4%，在其真实双臂试验中从 0% 到 60%。这给“具身数据怎样训练大模型”提供了一个可复查的实例。闭源 GPT 的训练细节不能从一次机器人 API 演示反推出来。[PEAR 作者博客](https://mit-han-lab.github.io/pear-blog/)

**回到罐子。** 如果模型每次都向图像右边偏，先把模型发出的末端目标画回相机图像。投影已经偏了，应查视觉定位或坐标转换；投影正确但手没到，应查可达性和控制器。仅凭最后一帧“没抓到”无法区分两者。
## GPT 怎样把观察变成末端目标？
读图时先找浅绿色的决策和输出，再沿底部箭头看模型何时能纠偏。抓碗时，一种做法是先写出整段轨迹，执行结束再依据碗的位移重规划；另一种是每次只交一个目标，看过下一帧再走。两者的手都可能走到同一位置，但途中可以改变主意的次数不同。

### GPT 给出运动几何

**Language Models as Zero-Shot Trajectory Generators** · [作者原文](https://www.robot-learning.uk/language-models-trajectory-generators)

[![任务与感知接口 → GPT-4 编写轨迹函数 → 查询物体几何 计算密集位姿序列 → 机械臂跟踪轨迹](../../diagrams/zh/gpt4-trajectories.svg)](../../diagrams/zh/gpt4-trajectories.svg)

作者让 GPT-4 写出计算轨迹的 Python 函数。抓碗失败时，模型读到的是碗在执行期间的位置变化，这次证据促使它改变下一次的抓点。

**Astranomy · Direct** · [作者原文](https://research.nvidia.com/labs/srl/projects/astranomy/)

[![图像、位姿 与任务 → GPT-6 Astra → 绝对末端位姿 与夹爪序列 → 本地控制器 驱动机械臂](../../diagrams/zh/astranomy-direct.svg)](../../diagrams/zh/astranomy-direct.svg)

以作者公开的一版提示为例，模型一次写出 3–15 行绝对目标。罐子如果被碰走，下一次查询才会把偏差反映到新目标里。

**RoboProbe · An Unexpected Robot Policy** · [作者原文](https://arxiv.org/html/2609.24170v1#S3)

[![三路图像、状态 指令与剩余步数 → GPT-6 Astra 读笔记与调用历史 → move_eef 指定双臂目标分量 → 逆运动学与 关节控制](../../diagrams/zh/roboprobe.svg)](../../diagrams/zh/roboprobe.svg)

工具允许只更新部分目标分量，模型也可结束回合。一个动作写成函数调用，运动的几何目标依然由 GPT 决定。

**LLM-LIBERO · From Reasoning to Action** · [作者原文](https://irvlutd.github.io/LLM-LIBERO/)

[![前后两轮双视角 与机器人状态 → GPT 等通用模型 → move_to 填写末端目标 → 适配器展开为 多个仿真控制步](../../diagrams/zh/llm-libero.svg)](../../diagrams/zh/llm-libero.svg)

这里只有一个运动入口，另有完成和放弃。一次模型调用可占用多个控制步，因此比较推理频率时要分清调用次数和仿真步数。

### 开放推理模型的同类接口

**PEAR · Qwen3.8-27B** · [作者原文](https://mit-han-lab.github.io/pear-blog/)

[![多视角图像 手臂状态与任务 → 27B 推理模型 读取回合历史 → 文本末端目标 → 逆运动学与控制器 驱动机械臂](../../diagrams/zh/pear.svg)](../../diagrams/zh/pear.svg)

接口与 Astranomy Direct 都落在末端目标上。PEAR 的区别在训练端，仿真任务成败提供强化学习信号，推理时直接从观察给出下一步位姿。

[中文](../zh/routes.md) · [English](../en/routes.md)
