# How does a model response move a fingertip?

A red can sits beside a bin. Two systems might agree that the can should be picked up first. The distinction becomes concrete at the next step. What exactly must each system hand the robot?
## Where does the action come from?

- **EEF targets** · RGB + instruction → GPT → Target poses → IK
- **Tool calls** · RGB + feedback → GPT → Tool + arguments → Execute & return
- **Hierarchy** · Observation → Subgoal → VLA → Action chunk

**End-effector targets (EEF).** A model can specify position, orientation and gripper opening relative to the base, sometimes for several future points. A local controller solves inverse kinematics and interpolates. To replay the request, we need the coordinate frame, distance units, rotation convention and target time. The left edge of an image can correspond to quite different base-frame directions after a camera change.

**Tool calls.** Our Piper agent can look up a target, align with it, grasp it and request a move. Each call returns an actual observation or execution result. One decision can span many control steps. That convenience has a specific failure mode. If localization binds a potato to the name “tomato”, an accurate controller can grasp precisely the wrong object.
## What does a tool-call comparison establish?
Astranomy compared three interfaces on RoboLab-120. Direct action generation reached 66.3%, an agent with persistent context reached 74.8%, and reviewing proposals from another policy reached 66.5%. Their ablations found value in interaction history and no further gain attributable to adding tools in that agentic setting. The 8.5-point difference therefore has several moving parts. We have yet to isolate the EEF-versus-tools choice on matched Piper scenes and budgets. [Astranomy study](https://research.nvidia.com/labs/srl/projects/astranomy/)

Guava asks a complementary question. Under LIBERO-PRO initial-position changes, GPT-5.4 scored 45%, base Qwen 6% and Guava-4B 41%. One interface supports teacher demonstrations and local student deployment. In a separate three-task timing study, cumulative model-request time per episode was 42.10 seconds for the teacher and 5.64 for the student. Robot motion and perception take additional time. [Guava results and timing definitions](https://guava-harness.github.io/)
## When could GPT interrupt a VLA?
A VLA can propose a chunk of actions. By the time GPT reviews it, the fingers may already be touching the cup. Our proposed experiment would version each observation and action queue, let the reviewer cancel only the uncommitted suffix, and replan from a fresh image. Fast stops and joint limits remain local. Alongside success, we would measure the age of each accepted suggestion, unnecessary interruptions and elapsed time. [Real-Time Chunking](https://www.pi.website/download/real_time_chunking.pdf)

ENPIRE closes a loop across episodes by resetting the scene, executing, verifying and refining the policy. Its showcased 99% is pass@8 on the selected tasks, with up to eight feedback-conditioned retries per subtask. Subtracting that percentage from our single-attempt SR would conflate policy quality with recovery budget. [ENPIRE retry definition](https://research.nvidia.com/labs/gear/enpire/)

[中文](../zh/routes.md) · [English](../en/routes.md)
