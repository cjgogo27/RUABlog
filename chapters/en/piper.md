# Teaching a 4B student to choose tools

With the original executor H₀ fixed, we can ask where the student started, what distillation added and how much of the teacher's capability remains out of reach. All three bars use the TERM revision's native task criterion (N-SR), over fifteen tasks with thirty scenes each.
## Three models on the same endpoint

| H₀ | N-SR |
|---|---:|
| Qwen Base | 33/450 · 7.33% |
| Qwen SFT | 150/450 · 33.33% |
| GPT-6 Astra | 311/450 · 69.11% |

The student gained **117 completions, or 26.00 percentage points**. It still trailed the teacher by **161 completions, or 35.78 points**, under the same scene and execution budgets. The teacher comparison uses native task success. The manuscript supplies its aggregate, so the per-task table shows the two student checkpoints.


**Native successes out of 30 per cell**

| Task | Qwen Base | Qwen SFT |
| --- | --- | --- |
| Pick up carrot | 0 | 3 |
| Tomato near potato | 0 | 6 |
| Lemon in bin | 0 | 1 |
| Push pot | 4 | 18 |
| Reverse cube stack | 0 | 1 |
| Reverse apple/juice order | 23 | 19 |
| Bin and tray | 0 | 0 |
| Set table | 0 | 0 |
| Can in bin | 0 | 14 |
| Apple/juice order | 0 | 17 |
| Remove cube from tray | 0 | 3 |
| Push basket | 5 | 28 |
| Close drawer | 0 | 4 |
| Shell game | 1 | 14 |
| Red objects in basket | 0 | 22 |

The seven demonstration-source tasks rose from 6/210 to 102/210. The other eight went from 27/240 to 48/240. Of 117 additional successes, 96 came from source tasks. Basket pushing and collecting red objects improved substantially. Reverse ordering lost four scenes. Bin and tray and setting the table remained at zero. Those last three tasks would be my first choices for failure replay to distinguish missing skills, misunderstood goals and execution errors.
## What was supervised in 1,041 records?

- **Base** · Initial image → Teacher call → Actual feedback
- **Branch** · Parent checkpoint → Perturbation → New decision
- **Training** · Align images → Supervise replies → Qwen3.5-4B

We fine-tuned the language component of Qwen3.5-4B for three epochs on 667 base trajectories and 374 recovery branches, freezing the vision encoder and aligner. Base runs begin at the task reset. A branch inherits visible history and starts from a perturbed parent checkpoint. Prefixes may therefore recur. Video metadata covers 759 records and 21.48 hours. Imputing the remaining 282 by task and trajectory kind gives about 28.9 simulated execution hours, counting only the new segment of each branch.

A loader once kept the raw tool calls in the archive but failed to expose the expected fields to training. We preserved the original assistant text and checked the actual loss-bearing content and image order. The frozen export included 27 records marked rejected in review. This checkpoint measures training on that export. A cleaned-data comparison would require another run.

The weights updated here belong to the open student. A closed GPT service saw the task images and generated teacher calls. A robot image in a request tells us nothing about whether its provider used it for weight updates. The recent PEAR study in the survey illustrates an alternative training signal supplied by the simulator.
## Three failures traced back to execution
**How far is the finger from the object?** Four contact points on a coarse finger box were roughly 19–26 mm from the original CAD. Replacing the box with a CAD convex hull removed a source of spurious contact, while a real fingertip can still collide with a cup wall. For red-object grasping, we also traced a roughly 5.4 mm lateral drift to a fingertip offset computed before the approach angle changed. A correct tool name cannot compensate for a stale transform.

**Why does the juice slip after lifting?** The original asset compiled to about 0.138 g. Increasing its mass exposed cases that reached their target pose but lost the load on the way up. For collection we sampled 70–140 g for container and contents and inherited the parent's mass on recovery branches. This is a simulation assumption that can be checked by weighing the real object.

**Is the rightmost cup the one we checked earlier?** Moving one cup changes the ordering. Two spatial descriptions can also yield nearly identical segmentation masks. Remembering previously inspected locations helps, although another observation costs a decision. In one recorded scene the base model used all 25 calls while the cube remained on the table. The student lifted it about 14.1 cm after 14 calls. That replay explains a particular success. The aggregate for the student is 14/30.

[中文](../zh/piper.md) · [English](../en/piper.md)
