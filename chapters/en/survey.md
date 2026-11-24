# Reading two months of RUA research

These projects and author blogs appeared between 24 September and 24 November 2026. They can be read as three sets of experiments: supply better geometry, bring feedback closer to execution, or change the student’s training signal. Some projects address more than one question.
## Same model, different geometry?
**24 September · Robo-Harness K1.** Alongside the RGB-versus-K1 Astra comparison, the authors trained a 9B student on 107 teacher trajectories. It reached 44.2% on new initial states and 13.9% on held-out task conditions, versus 30.2% and 0% for their OpenVLA comparison. Changing a starting layout and changing a task condition stress different capabilities. Model and training procedure also differ in this comparison, so the first gap cannot all be attributed to geometry. [K1 paper](https://arxiv.org/abs/2609.29389)

**October · Astranomy.** The research blog publishes three policy roles and failure replays. Trace the first deviation: wrong object, incorrect closing direction or a slip in transit? The direct policy averaged 18.56 seconds per inference call. A geometric answer that looks wrong on arrival may have been accurate in the earlier image. [Authors’ experiments and replays](https://research.nvidia.com/labs/srl/projects/astranomy/)
## How many attempts did the code make? How old was the image?
**1 October · OpenRUA.** Claude Code / Opus 5 generated programs against native robot interfaces. The authors report 99.0% on CaP-Bench and 87.0% on LIBERO-PRO. **2 November · Behind the RoboDojo Boom** shows why code agents need explicit accounting. Its authors reconstructed 210 public traces from a different system, RoboDawn: 97 of 99 successes occurred after the native control-step limit. These are separate studies. Read the first for interface design and the second for how to audit the meaning of a completed episode. [OpenRUA paper](https://arxiv.org/abs/2610.02459) · [OpenRUA Team evaluation blog](https://openrua.ai/revisiting-rua)

**20 October · PACT-VLA.** This neighbouring line of work addresses the question of adding a larger model to check a running policy. It reuses the frozen policy to check candidates before commit. At a four-step delay, the authors report a 15.0-point gain over RTC on Kinetix and a 5.2-point gain over single-candidate asynchronous execution with GR00T N1.7 on LIBERO. Each gain belongs to its own benchmark and baseline. [PACT-VLA paper](https://arxiv.org/abs/2610.28019)
## Train the model or improve its interface?
**1 November paper, 3 November blog · uni-robot-agent.** The team standardizes tools and returns across open models, simulation and physical robots. Without privileged input, Qwen3.8-Flash-Next scored 31.39 on RoboDojo against a published 28.97 for Astra–RoboProbe. This is a benchmark score, and the two systems use different interfaces. For open students, a longer-term contribution is a common format for collecting traces for subsequent training. [Paper](https://arxiv.org/abs/2611.01560) · [Team blog](https://openrua.ai/uni-robot-agent)

**14 November · PEAR.** PEAR spends simulation resources on attempts and task rewards and learns end-effector actions. Guava invests in teacher demonstrations and failure recovery and learns the next tool call. Both can yield a locally deployable student. Moving a dataset from one setting to the other would require reconsidering action space, observation frequency and supervision. A count of robot hours alone cannot express that difference. [PEAR blog and open model](https://mit-han-lab.github.io/pear-blog/)

**Four things to find in the next paper.** Inspect a raw response to see whether it returns coordinates, a tool, code or a subgoal. Find the next observation to locate the feedback loop. Count actions and retries to recover the budget behind each success. Finally find a comparison that changes one component at a time. Together these details tell you what kind of system the paper built and which part is worth trying on another robot.

## Which comparisons answer the same question?

| Question | Closest reported comparison | What still varies together? |
|---|---|---|
| Does one model benefit from additional geometry? | K1, Astra with RGB at 61.1% and the perception package at 88.9% | Depth, anchors, measurements and grasp hypotheses enter together. |
| Can recovery experience help on new tasks? | Guava, 90.8% with perturbation traces versus 77.1% without on unseen tasks | The data mix changes. The optimal branch fraction for each task is unknown. |
| Does the commit strategy matter? | PACT-VLA, the same frozen policy from 60% to 82% across three real tasks | Candidate generation and pre-commit selection jointly define the intervention. |
| What does the local student gain? | Piper, 33/450 to 150/450 with the native criterion and executor fixed | It tests the whole SFT run. The contribution of each training trajectory type remains open. |

If most failures involve grasping the wrong object, start with target binding in K1 and the feedback schedule in Guava. If targeting is correct but corrections arrive only after hitting the rim, read about restaging in RPent and commit timing in PACT-VLA. Aggregate success identifies a problem worth investigating; the first failing layer tells you which paper might actually help.

[中文](../zh/survey.md) · [English](../en/survey.md)
