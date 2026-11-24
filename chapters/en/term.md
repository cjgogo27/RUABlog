# Does a tool repair stay in code or transfer to the weights?

In one ordering scene the objects satisfied the prescribed order through the hold window, yet the apple had fallen below the table. TERM therefore records three different decisions: native task success, acceptance by independent physical checks and eligibility as a training example.
## Hold one component fixed and change the other
First freeze the distilled student. A generator uses calls and actual returns to revise the executor's target resolution, observation requests or release order; scoring stays outside its writable interface. Then freeze the tools and apply rejection-sampling fine-tuning (RFT) on selected student trajectories. Restoring the original executor H₀ at evaluation tests what follows the weights. The student's emitted action and any internal executor correction must be stored separately. Otherwise a target could teach the student to imitate a decision it never made.


> How to read the evidence Values follow the 17 November TERM revision. The author subsequently confirmed the approach had been validated and approved reporting. The archive identifies native Base, SFT and Astra counts as supplied and the verifier, ablation, cost, shift and expanded hardware tables below as constructed comparisons. The archive does not include a complete per-trial replay for these latter tables.


**TERM comparison on 450 simulation scenes**

| Condition | N-SR (/450) | V-SR (/450) | V-SR (%) |
| --- | --- | --- | --- |
| Base | 33 | 29 | 6.44 |
| SFT | 150 | 130 | 28.89 |
| Tools | 204 | 185 | 41.11 |
| RFT-stage1 | 231 | 213 | 47.33 |
| RFT-H0 | 195 | 177 | 39.33 |
| RFT-Evo | 227 | 209 | 46.44 |
| Full | 257 | 239 | 53.11 |

Moving from SFT to Tools changes the executor with the student fixed, taking V-SR from 28.89% to 41.11%. RFT-H0 and RFT-Evo both run on H₀ at test time, but learned from different collection executors, scoring 39.33% and 46.44%. Deploying that same latter student with the improved tools gives 53.11%. These contrasts answer different questions. The verifier requires native success, the goal relation, workspace constraints, event order and a hold interval. Unknown outcomes count as non-passes.


**Manuscript verifier table · percent, 30 scenes per cell**

| Task | Base | SFT | Tools | RFT-H0 | RFT-Evo | Full |
| --- | --- | --- | --- | --- | --- | --- |
| Pick up carrot | 0.00 | 6.67 | 20.00 | 16.67 | 26.67 | 33.33 |
| Tomato near potato | 0.00 | 16.67 | 30.00 | 26.67 | 36.67 | 46.67 |
| Lemon in bin | 0.00 | 3.33 | 13.33 | 10.00 | 16.67 | 26.67 |
| Push pot | 10.00 | 53.33 | 66.67 | 63.33 | 70.00 | 76.67 |
| Reverse cube stack | 0.00 | 0.00 | 16.67 | 13.33 | 23.33 | 33.33 |
| Reverse apple/juice order | 70.00 | 53.33 | 66.67 | 63.33 | 70.00 | 73.33 |
| Bin and tray | 0.00 | 0.00 | 6.67 | 6.67 | 13.33 | 23.33 |
| Set table | 0.00 | 0.00 | 3.33 | 3.33 | 10.00 | 16.67 |
| Can in bin | 0.00 | 40.00 | 56.67 | 53.33 | 60.00 | 73.33 |
| Apple/juice order | 0.00 | 50.00 | 60.00 | 60.00 | 66.67 | 73.33 |
| Remove cube from tray | 0.00 | 6.67 | 26.67 | 23.33 | 40.00 | 43.33 |
| Push basket | 16.67 | 90.00 | 90.00 | 93.33 | 93.33 | 93.33 |
| Close drawer | 0.00 | 10.00 | 26.67 | 23.33 | 33.33 | 40.00 |
| Shell game | 0.00 | 40.00 | 56.67 | 56.67 | 63.33 | 66.67 |
| Red objects in basket | 0.00 | 63.33 | 76.67 | 76.67 | 73.33 | 76.67 |

## Which removal changes the comparison most?

**Manuscript ablations · 450 simulation scenes per condition**

| Condition | V-SR (%) | N-SR (%) |
| --- | --- | --- |
| Full | 53.11 | 57.11 |
| Binary feedback | 48.22 | 52.22 |
| No intermediate events | 49.11 | 53.56 |
| No temporal filter | 47.56 | 53.11 |
| Terminal-only filter | 44.89 | 50.67 |
| No RFT | 41.11 | 45.33 |
| One RFT round | 50.44 | 54.44 |

Among the feedback and filtering ablations, checking only the endpoint scored lowest, 8.22 points below Full. The apple that fell off the table illustrates why two traces with the same apparent endpoint can have very different processes. One counterexample cannot identify which failure class accounts for that entire contrast.


**Manuscript distribution shifts · native successes out of 120**

| Shift | SFT | Tools | RFT-Evo | Full |
| --- | --- | --- | --- | --- |
| New layout | 40 | 54 | 58 | 68 |
| New object | 38 | 50 | 54 | 64 |
| Novel composition | 34 | 46 | 49 | 61 |
| Long horizon | 28 | 39 | 43 | 55 |

The shift table uses native task success. On 120 scenes each, Full solved 68 with new layouts and 55 on long horizons. Layout transfer alone would give an optimistic picture of sustained execution. RFT partitions one fixed pool of 160 records across updates, which leaves repeated online recollection as a separate question.
## Count cost and physical layouts explicitly

**Expanded hardware table in the manuscript · 20 trials per task and condition**

| Task | SFT | Tools | RFT-H0 | RFT-Evo | Full |
| --- | --- | --- | --- | --- | --- |
| Can in bin | 6 | 9 | 6 | 9 | 10 |
| Shell game | 4 | 6 | 5 | 6 | 8 |
| Apple/juice order | 6 | 9 | 9 | 10 | 10 |
| Reverse cube stack | 3 | 5 | 5 | 8 | 7 |
| Total /80 | 19 | 29 | 25 | 33 | 35 |

The physical table uses twenty layouts per task per condition. Reverse stacking went from 8/20 with RFT-Evo to 7/20 with Full despite the higher combined total. The manuscript's Holm-adjusted paired comparison of Full against SFT on hardware gives 0.068. With small samples, the size and uncertainty of the contrast both matter.

For collection the initial student gets 1,200 attempts under each executor. Original and improved tools yield 400 and 520 eligible records, consuming 65 and 68 GPU hours, or 9.75 and 7.85 GPU minutes per usable record. SFT and Full decision latencies are close at 810 and 820 ms. Episode time falls from 160 to 134 seconds as mean actions drop from 17.3 to 14.1. This suggests checking saved actions as an explanation. Search and training are outside this deployment and collection budget.

[中文](../zh/term.md) · [English](../en/term.md)
