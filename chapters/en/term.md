# Our Piper project: collecting demonstrations, distilling a student and repairing tools

This is our implementation of the Agentic Policy route on Piper. GPT-6 Astra used tools in simulation. We saved observations, calls and actual returns as multi-turn trajectories, then trained a local Qwen3.5-4B. Three checks guided the work: what reached the loss, how much teacher capability transferred, and which failures belonged to the executor.
## How a recovery becomes a training example
In Guava the teacher first attempts a normal task. The system saves an intermediate checkpoint, perturbs the object or grasp, then lets the teacher continue from the new image and actual return. Training conditions on instruction, images and history and supervises the next teacher call. The deployed student uses the same interface. On eight unseen tasks, omitting perturbation trajectories gave 77.1% versus 90.8% with them. On seven seen tasks the corresponding values were 81.9% and 82.9%. That is a reason to measure familiar and changed conditions separately when evaluating recovery data. [Guava training and ablation](https://guava-harness.github.io/)

Our Piper pipeline also used tool interactions to train Qwen3.5-4B. The export comprised 667 base trajectories and 374 recovery branches, or 1,041 records. We froze the visual encoder and aligner and fine-tuned the language component for three epochs. Video metadata covers 21.48 simulated execution hours over 759 records; imputing the rest by task and record type gives about 28.9 hours. A branch inherits its parent conversation, so only its new segment contributes to duration. The export included 27 records marked rejected in review; those records entered this checkpoint.
## Which distillation results can be read side by side?
| Each project’s own fifteen-task simulation | Base Qwen3.5-4B | Distilled student | Respective teacher |
|---|---:|---:|---:|
| Guava, reported, 450 scenes | 22.2% | 87.1% | GPT-5.4, 90.4% |
| Piper, TERM native criterion, 450 scenes | 7.33% (33) | 33.33% (150) | GPT-6 Astra, 69.11% (311) |

Each row supports a **within-system comparison**. Guava gained 64.9 points and approached its teacher. Piper gained 26.00 points and remained 35.78 points behind its teacher. The robots, teachers, tool adaptations and training data differ. Even the starting scores differ substantially, so the difference between the two students cannot be assigned to a training method. In a separate three-task timing study, Guava reported 42.10 versus 5.64 seconds of cumulative model requests per episode for GPT-5.4 and local Guava-4B. Robot motion is outside that timing. [Guava results and latency definitions](https://guava-harness.github.io/)

Of the 117 additional native successes on Piper, 96 came from the seven demonstration-source tasks, and 21 from the other eight. Basket pushing rose from 5/30 to 28/30, can placement from 0/30 to 14/30, and setting the table stayed at 0/30. The total captures transfer from demonstration; the distribution tells us which skills to investigate next.
## From the tool trace to the fingertips

**A Piper debugging example.** On a red-object approach, the path changed its tilt while the fingertip offset was still computed at the previous orientation. Descent drifted sideways by roughly 5.4 mm. Asking the model to identify the object again would not correct it. The requested target, chosen orientation and measured fingertip path together locate the error inside the tool. The same logic applies to program evaluation: one generated loop can represent ten physical attempts.

## If a tool rescues the grasp, what should the student imitate?
ASPIRE stores validated program repairs. TERM also asks whether experience from a repaired executor transfers to a student. Suppose the student requests a grasp at the old location and the executor refreshes localization and corrects the path. Log the student’s request, the corrected execution and the new observation separately. Labelling the old image with the executor’s corrected coordinates would use information from the future.

TERM first fixes the student while varying the tools, then performs rejection-sampling fine-tuning (RFT) on verified student traces with reconstructable targets. Restoring the original executor at test time checks what survived in the weights. In the revision’s verifier comparison table, the frozen SFT student goes from 28.89% to 41.11% when changing executors. Students trained on two sources of traces and both tested on the original executor score 39.33% and 46.44%. These are manuscript V-SR comparisons, distinct from native success above. The author confirms the approach has been validated; the November 17 archive still labels these verifier figures constructed and does not include complete per-scene replay. The useful experimental detail is which component each contrast holds fixed.

One concrete lesson from our training pipeline is to inspect what the loader actually returns. The archived JSON contained tool calls, but one loader version failed to pass their content into the supervised field. We aligned assistant text, images, arguments and loss masks before interpreting the student as learning which tool to call after an observation.

[中文](../zh/term.md) · [English](../en/term.md)
