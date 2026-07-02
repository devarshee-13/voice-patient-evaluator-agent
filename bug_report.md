Bug Report
==========

Issues found while testing the Pretty Good AI phone agent with an automated patient caller. Each entry notes what happened, why it is a problem, and where to find it in the call transcripts and recordings.

Testing covered five scenarios — scheduling, prescription refill, cancel/reschedule, insurance inquiry, and an edge-case confused caller — all using the same patient identity (Sarah Johnson, DOB 03/15/1985, Blue Cross insurance).

Summary
-------

| # | Severity | Short description | Call |
|---|----------|-------------------|------|
| 1 | High | False existing appointment blocks new-patient scheduling | scheduler #3 |
| 2 | High | No medications on file; refill request cannot be fulfilled | refill #4 |
| 3 | High | Support transfer ends at test line with abrupt goodbye | refill #4, edge_case #7 |
| 4 | Medium | Agent cannot handle confused, rambling caller | edge_case #7 |
| 5 | Medium | Agent speech arrives fragmented or mid-sentence | edge_case #7, cancel #5 |
| 6 | Low | Garbled or incorrect practice name in greetings | multiple calls |
| 7 | Medium | Practice name inconsistency between greeting and response | `call_01_insurance_20260701_145505.txt` (insurance #1) |
| 8 | Medium | Incorrect or non-standard practice name in greeting | `call_02_insurance_20260701_145819.txt` (insurance #2); recording `20260701_215722_CAf1315df650d2897971a5363a957dec2f_REccc81bed38d86c3d656cd2092a130e39.mp3` |
| 9 | Medium | Agent gives ambiguous insurance confirmation that may mislead patient | `call_02_insurance_20260701_145819.txt` (insurance #2); recording `20260701_215722_CAf1315df650d2897971a5363a957dec2f_REccc81bed38d86c3d656cd2092a130e39.mp3` |
| 10 | Medium | Inconsistent and garbled provider name throughout call | `call_01_cancel_20260701_150425.txt` (cancel #1); recording `20260701_220107_CAdcd92933e797f39ab9ab097c9e703c60_RE7f0001fe8eb392afc4b5b25a75a6f071.mp3` |
| 11 | Medium | Agent reads garbled or malformed appointment date | `call_01_cancel_20260701_150425.txt` (cancel #1); recording `20260701_220107_CAdcd92933e797f39ab9ab097c9e703c60_RE7f0001fe8eb392afc4b5b25a75a6f071.mp3` |
| 12 | Low | Agent does not confirm cancellation of original appointment | `call_01_cancel_20260701_150425.txt` (cancel #1); recording `20260701_220107_CAdcd92933e797f39ab9ab097c9e703c60_RE7f0001fe8eb392afc4b5b25a75a6f071.mp3` |
| 13 | Medium | Transfer handoff ends abruptly with no confirmation or closure | `call_01_scheduler_20260701_152917.txt` (scheduler #1); recording `20260701_222642_CAb8bf1d50fc03f4acf2ca131e0cd168aa_REe0a13fb2f9ceb9e7cc31f6e5f8a08a7d.mp3` |
| 14 | Low | Agent announces transfer twice with inconsistent messaging | `call_01_scheduler_20260701_152917.txt` (scheduler #1); recording `20260701_222642_CAb8bf1d50fc03f4acf2ca131e0cd168aa_REe0a13fb2f9ceb9e7cc31f6e5f8a08a7d.mp3` |
| 15 | High | Agent dismisses no-medication finding then processes refill without resolution | `call_02_refill_20260701_153319.txt` (refill #2); recording `20260701_223053_CA78abad7f6812a1edc029c40852db2b72_RE560f97e34c0e05e026bcb296b6840b79.mp3` |
| 16 | Medium | Agent ignores patient's concern that she may have reached wrong number | `call_02_refill_20260701_153319.txt` (refill #2); recording `20260701_223053_CA78abad7f6812a1edc029c40852db2b72_RE560f97e34c0e05e026bcb296b6840b79.mp3` |
| 17 | High | Rescheduled date conflicts with original appointment date | `call_03_cancel_20260701_153745.txt` (cancel #3); recording `20260701_223412_CA19554207398e8a0e59f7ba261e7fa7e2_RE43f33000c92d363d6e452de299769f8f.mp3` |
| 18 | Medium | Provider name changes inconsistently across the same call | `call_03_cancel_20260701_153745.txt` (cancel #3); recording `20260701_223412_CA19554207398e8a0e59f7ba261e7fa7e2_RE43f33000c92d363d6e452de299769f8f.mp3` |
| 19 | Medium | Agent gives vague, unverified insurance acceptance without confirming patient's specific plan | `call_04_insurance_20260701_210033.txt` (insurance #4); recording `20260702_035948_CA655f0ec2b6a549edf446624243d176f7_RE1817db64b902dc8a8ddc3dacdbd0226f.mp3` |
| 20 | Low | Practice name inconsistency within same call | `call_04_insurance_20260701_210033.txt` (insurance #4); recording `20260702_035948_CA655f0ec2b6a549edf446624243d176f7_RE1817db64b902dc8a8ddc3dacdbd0226f.mp3` |
| 21 | High | Agent abruptly abandons scheduling mid-process without explanation | `call_05_edge_case_20260701_210832.txt` (edge_case #5); recording `20260702_040221_CA8f0d9461596bc498e8d470be71a062c2_RE127f56b22e35fe42d1512d7d2fb850a0.mp3` |
| 22 | Medium | Agent redundantly re-requests already-confirmed patient information | `call_05_edge_case_20260701_210832.txt` (edge_case #5); recording `20260702_040221_CA8f0d9461596bc498e8d470be71a062c2_RE127f56b22e35fe42d1512d7d2fb850a0.mp3` |
| 23 | Medium | Provider name garbled inconsistently across booking confirmations | `call_06_urgent_20260701_211340.txt` (urgent #6); recording `20260702_040914_CAe0bbc1816cdcc1e39e2e1d9992e2fa75_RE12f1f73eb094ce04995869748a6791af.mp3` |
| 24 | Medium | Agent does not confirm cancellation-list placement before closing call | `call_06_urgent_20260701_211340.txt` (urgent #6); recording `20260702_040914_CAe0bbc1816cdcc1e39e2e1d9992e2fa75_RE12f1f73eb094ce04995869748a6791af.mp3` |
| 25 | Low | Practice name inconsistency within same call | `call_06_urgent_20260701_211340.txt` (urgent #6); recording `20260702_040914_CAe0bbc1816cdcc1e39e2e1d9992e2fa75_RE12f1f73eb094ce04995869748a6791af.mp3` |
| 26 | High | Agent logs grossly incorrect billing amount ($285 billion) in case notes | `call_07_billing_20260701_222053.txt` (billing #7); recording `20260702_051824_CAd5e8aabbf44ba0ea78ee1f0d5081714f_RE1bdf1c506bf3c22c560c47b1fd0b2f6f.mp3` |
| 27 | High | Agent accepts mismatched DOB with explicit 'demo purposes' disclosure to patient | `call_08_referral_20260701_224324.txt` (referral #8); recording `20260702_054115_CAbaa9b61beddec9df40722f400aa14529_REec8cb270e89a8bda6eb1332181699623.mp3` |
| 28 | Medium | Agent confirms insurance routing without verifying patient's actual plan details | `call_08_referral_20260701_224324.txt` (referral #8); recording `20260702_054115_CAbaa9b61beddec9df40722f400aa14529_REec8cb270e89a8bda6eb1332181699623.mp3` |
| 29 | High | Agent discloses DOB mismatch failure then overrides it with 'demo purposes' statement to patient | `call_09_results_20260702_155215.txt` (results #9); recording `20260702_224921_CAd6a4923c32c655e84b2579544c30aa58_RE1959f49fa267da161cd13c2391c8ea30.mp3` |
| 30 | Medium | Agent proceeds with request before completing identity verification, then flags mismatch out of sequence | `call_09_results_20260702_155215.txt` (results #9); recording `20260702_224921_CAd6a4923c32c655e84b2579544c30aa58_RE1959f49fa267da161cd13c2391c8ea30.mp3` |
| 31 | Low | Garbled or incomplete greeting omits opening word | `call_09_results_20260702_155215.txt` (results #9); recording `20260702_224921_CAd6a4923c32c655e84b2579544c30aa58_RE1959f49fa267da161cd13c2391c8ea30.mp3` |
| 32 | Medium | Greeting contains extraneous promotional non-sequitur | `call_10_records_20260702_155504.txt` (records #10); recording `20260702_225252_CA2f28b6985194115887ac684d3fdc12eb_RE2ef3aac294a0ead7a7f9ed7a4fb6a177.mp3` |
| 33 | Low | Agent initiates caller ID verification before confirming identity, skipping proper intro | `call_10_records_20260702_155504.txt` (records #10); recording `20260702_225252_CA2f28b6985194115887ac684d3fdc12eb_RE2ef3aac294a0ead7a7f9ed7a4fb6a177.mp3` |

Details
-------

### Bug 1: False existing appointment blocks new-patient scheduling

- **Severity:** High
- **Call:** `call_03_scheduler_20260701_142201.txt` (agent turn ~line 31)
- **What happened:** Sarah called to schedule a new patient appointment for lower back pain. After verifying her identity (name and DOB), the agent confirmed the scheduling intent, then said she already had a new patient consultation booked for July 9 at 09:45 AM and asked whether she wanted to reschedule or cancel — instead of booking a new appointment.
- **Why it's a problem:** A caller trying to schedule for the first time cannot complete their goal. The agent assumes stale or incorrect chart data without reconciling the caller's stated intent, which forces the patient into a reschedule/cancel flow they did not ask for.
- **Expected behavior:** If the caller explicitly requests a new patient appointment, the agent should verify whether an existing appointment truly belongs to this patient and, if none exists or the record is ambiguous, proceed with new-patient scheduling rather than defaulting to reschedule/cancel.

---

### Bug 2: No medications on file; refill request cannot be fulfilled

- **Severity:** High
- **Call:** `call_04_refill_20260701_144613.txt` (agent turn ~line 23)
- **What happened:** Sarah called to refill Lisinopril 10mg for blood pressure. Identity was verified successfully (name and DOB March 15, 1985). The agent then reported that no medications were on file for refill. When Sarah explained she had been getting the prescription through this practice, the agent repeated that nothing was listed and offered only a transfer to patient support.
- **Why it's a problem:** A patient running low on a maintenance medication cannot get a refill or even a clear next step. The agent offers no alternative (e.g., message to provider, intake of prescription details, callback) before escalating.
- **Expected behavior:** When a verified patient requests a known medication, the agent should either process the refill, capture prescription details for a clinician review, or clearly explain what information is missing and how the patient can resolve it — without dead-ending on "nothing on file."

---

### Bug 3: Support transfer ends at test line with abrupt goodbye

- **Severity:** High
- **Call:** `call_04_refill_20260701_144613.txt` (~line 31); `call_07_edge_case_20260701_144111.txt` (~line 39)
- **What happened:** In both calls, after the agent offered to connect the patient to support or a representative, the caller heard: *"Connecting you to a representative. Please wait. Hello. You've reached the Pretty Good AI test line. Goodbye."* The call ended immediately with no human handoff and no resolution.
- **Why it's a problem:** The patient believes they are being transferred to help but is instead dropped on a test message and disconnected. This is worse than a failed transfer — it feels like being hung up on after waiting.
- **Expected behavior:** A transfer should reach a live agent, queue with hold music and an ETA, or fail gracefully with a callback option. The patient should never be routed to an internal test line and disconnected without warning.

---

### Bug 4: Agent cannot handle confused, rambling caller

- **Severity:** Medium
- **Call:** `call_07_edge_case_20260701_144111.txt` (throughout; escalation ~line 39)
- **What happened:** Sarah (edge-case persona) asked about Sunday hours, changed her mind between scheduling and canceling, interrupted herself, and asked overlapping questions about referrals and body parts. The agent partially answered individual fragments but lost track of the conversation. After several confused exchanges, the agent said it could not proceed and escalated to support — which then disconnected (see Bug 3).
- **Why it's a problem:** Real patients — especially elderly, anxious, or cognitively impaired callers — often speak this way. An agent that gives up and transfers (to nowhere) leaves these patients without any help.
- **Expected behavior:** The agent should patiently guide a confused caller: ask one clarifying question at a time, summarize what it understands so far, and offer a simple menu of options (schedule, cancel, ask a question) before escalating.

---

### Bug 5: Agent speech arrives fragmented or mid-sentence

- **Severity:** Medium
- **Call:** `call_07_edge_case_20260701_144111.txt` (e.g. agent turns ~lines 15, 19, 27, 35); `call_05_cancel_20260701_143559.txt` (~line 29)
- **What happened:** Multiple agent utterances in the transcript appear cut off or missing context. Examples: *"If you'd like, I can help you find an appoint"* (no ending), *"we have on file."* (no beginning), *"5AM, not 2PM."* (without the sentence it belongs to), and *"have your name as Sarah Johnson and your date me know when you're ready to continue."* (garbled merge of two thoughts).
- **Why it's a problem:** Patients miss critical information and must ask the agent to repeat itself, slowing the call and increasing frustration. In the cancel call, the time correction (9:45 AM vs 2 PM) was delivered without context.
- **Expected behavior:** The agent should deliver complete sentences. If interrupted, it should acknowledge the interruption and restate the full thought rather than resuming mid-phrase.

---

### Bug 6: Garbled or incorrect practice name in greetings

- **Severity:** Low
- **Call:** `call_04_refill_20260701_144613.txt` (~line 11: "Pivot Be Good AI"); `call_05_cancel_20260701_143559.txt` (~line 11: "Pibbett Pretty Good AI"); `call_06_insurance_20260701_143701.txt` (~line 11: "For calling Pretty Good AI")
- **What happened:** The agent's opening greeting consistently mispronounced or garbled the practice name. Variants included "Pivot Be Good AI," "Pibbett Pretty Good AI," and a broken sentence starting with "For calling Pretty Good AI" (missing "Thanks").
- **Why it's a problem:** The first thing a patient hears sets the tone for the call. A garbled greeting undermines trust and makes the agent sound unreliable before any real work begins.
- **Expected behavior:** The agent should deliver a clear, consistent greeting such as "Thanks for calling [Practice Name]. How may I help you today?"

---

### Note: Insurance inquiry call (no major issues)

- **Call:** `call_06_insurance_20260701_143701.txt`
- **Observation:** Sarah asked whether the practice accepts Blue Cross and what Friday office hours are. The agent answered both questions correctly (Blue Cross accepted; Fridays 9 AM–12 PM). Aside from the minor greeting issue in Bug 6, this scenario completed successfully.

### Note: Cancel/reschedule call (largely successful)

- **Call:** `call_05_cancel_20260701_143559.txt`
- **Observation:** Sarah rescheduled a Thursday appointment to the following Thursday at 9 AM. Identity verification, slot offering, confirmation, and text-message opt-in all worked. Minor issues: fragmented time clarification (Bug 5) and a TTS glitch on the confirmation (*"July sixth sixteenth"* / provider name *"Abeker"* vs Bricker).

### Bug 7: Practice name inconsistency between greeting and response

- **Severity:** Medium
- **Call:** `call_01_insurance_20260701_145505.txt` (insurance #1)
- **What happened:** The agent greeted the caller with 'Pip Pretty Good AI' but then referred to the practice as 'Pivot Point Orthopedics' when answering the insurance question.
- **Why it's a problem:** The two names are completely different. The opening greeting 'Pip Pretty Good AI' appears to be a placeholder or system name leak rather than the actual practice name, causing confusion about which practice the patient reached. This is a distinct manifestation from a garbled/incorrect greeting alone — the inconsistency between greeting and subsequent response is the core issue.
- **Expected behavior:** The agent should consistently use the correct, official practice name in both the greeting and all subsequent responses throughout the call.
- **Transcript hint:** 'Thanks for calling Pip Pretty Good AI' vs. 'Pivot Point Orthopedics welcomes most insurance plans...'

---

### Note: insurance call #1

- **Call:** `call_01_insurance_20260701_145505.txt` (insurance #1)
- **Observation:** The call otherwise succeeded — insurance and office hours questions were answered clearly and the patient was satisfied.

### Bug 8: Incorrect or non-standard practice name in greeting

- **Severity:** Medium
- **Call:** `call_02_insurance_20260701_145819.txt` (insurance #2); recording `20260701_215722_CAf1315df650d2897971a5363a957dec2f_REccc81bed38d86c3d656cd2092a130e39.mp3`
- **What happened:** The agent greeted the caller with 'Thanks for calling Pivot Pretty Good AI,' which is an unusual and unprofessional-sounding practice name.
- **Why it's a problem:** While a similarly named issue ('Garbled or incorrect practice name in greetings') is already documented, this specific instance is 'Pivot Pretty Good AI' — which may reflect a placeholder or misconfigured practice name being read verbatim rather than the actual practice name. This is distinct from garbled audio; it is a configuration or data error causing an embarrassing name to be spoken clearly.
- **Expected behavior:** The agent should announce the correct, properly configured practice name in its greeting.
- **Transcript hint:** Thanks for calling Pivot Pretty Good AI.

---

### Bug 9: Agent gives ambiguous insurance confirmation that may mislead patient

- **Severity:** Medium
- **Call:** `call_02_insurance_20260701_145819.txt` (insurance #2); recording `20260701_215722_CAf1315df650d2897971a5363a957dec2f_REccc81bed38d86c3d656cd2092a130e39.mp3`
- **What happened:** When asked if Blue Cross is accepted, the agent said 'We welcome most insurance plans, including many major providers like Blue Cross' but then immediately qualified it with 'For specific coverage, our team can confirm your details.' The patient interpreted this as a firm confirmation that Blue Cross is accepted.
- **Why it's a problem:** The hedged language ('many major providers like Blue Cross') does not constitute a definitive confirmation of Blue Cross acceptance, yet the patient left the call believing Blue Cross is accepted. If Blue Cross is not actually accepted or coverage is uncertain, this could lead to unexpected billing issues for the patient.
- **Expected behavior:** The agent should either definitively confirm or deny Blue Cross acceptance based on accurate practice data, or clearly communicate that it cannot confirm and that the patient should call back or speak with staff before assuming coverage.
- **Transcript hint:** We welcome most insurance plans, including many major providers like Blue Cross... For specific coverage, our team can confirm your details.

---

### Note: insurance call #2

- **Call:** `call_02_insurance_20260701_145819.txt` (insurance #2); recording `20260701_215722_CAf1315df650d2897971a5363a957dec2f_REccc81bed38d86c3d656cd2092a130e39.mp3`
- **Observation:** The call largely completed the scenario goals, but the agent's non-committal insurance language combined with the patient walking away fully convinced creates a meaningful miscommunication risk.

### Bug 10: Inconsistent and garbled provider name throughout call

- **Severity:** Medium
- **Call:** `call_01_cancel_20260701_150425.txt` (cancel #1); recording `20260701_220107_CAdcd92933e797f39ab9ab097c9e703c60_RE7f0001fe8eb392afc4b5b25a75a6f071.mp3`
- **What happened:** The agent referred to the provider by different garbled names across the call: 'Averker', 'Abroker', 'Abeker', and finally 'doctor Bricker'. No single consistent, correct name was used.
- **Why it's a problem:** The patient cannot verify they are being scheduled with the correct provider. Inconsistent names suggest a text-to-speech or data rendering issue that erodes patient trust and could lead to confusion about who their appointment is with.
- **Expected behavior:** The agent should consistently use the correct, properly rendered provider name throughout the entire call, especially during confirmation steps.
- **Transcript hint:** 'with Averker' → 'with Abroker' → 'with Abeker' → 'with doctor Bricker'

---

### Bug 11: Agent reads garbled or malformed appointment date

- **Severity:** Medium
- **Call:** `call_01_cancel_20260701_150425.txt` (cancel #1); recording `20260701_220107_CAdcd92933e797f39ab9ab097c9e703c60_RE7f0001fe8eb392afc4b5b25a75a6f071.mp3`
- **What happened:** When reading back the existing appointment, the agent said 'Thursday, July sixth sixteenth at 9AM', which is nonsensical (combining 'sixth' and 'sixteenth' into one date).
- **Why it's a problem:** A malformed date makes it impossible for the patient to confidently confirm they are modifying the correct appointment. The patient expressed uncertainty about the time, which may have been compounded by the confusing date rendering.
- **Expected behavior:** The agent should render dates cleanly and unambiguously, e.g., 'Thursday, July 16th at 9AM', so the patient can verify appointment details accurately.
- **Transcript hint:** 'I see you have an appointment scheduled for Thursday, July sixth sixteenth at 9AM'

---

### Bug 12: Agent does not confirm cancellation of original appointment

- **Severity:** Low
- **Call:** `call_01_cancel_20260701_150425.txt` (cancel #1); recording `20260701_220107_CAdcd92933e797f39ab9ab097c9e703c60_RE7f0001fe8eb392afc4b5b25a75a6f071.mp3`
- **What happened:** The agent rescheduled the appointment to July 20 but never explicitly confirmed that the original appointment (Thursday, July 16 at 9AM) was cancelled.
- **Why it's a problem:** Without explicit cancellation confirmation, the patient may believe both appointments are now on the books, risking a no-show charge or scheduling conflict on the practice side.
- **Expected behavior:** When rescheduling, the agent should explicitly state that the original appointment has been cancelled and the new one confirmed, e.g., 'Your July 16th appointment has been cancelled and rescheduled to July 20th at 10:30AM.'
- **Transcript hint:** 'your appointment has been rescheduled to Monday, July 20 at 10:30AM with doctor Bricker' — no mention of original appointment cancellation

---

### Bug 13: Transfer handoff ends abruptly with no confirmation or closure

- **Severity:** Medium
- **Call:** `call_01_scheduler_20260701_152917.txt` (scheduler #1); recording `20260701_222642_CAb8bf1d50fc03f4acf2ca131e0cd168aa_REe0a13fb2f9ceb9e7cc31f6e5f8a08a7d.mp3`
- **What happened:** After announcing the transfer to patient support, the agent said only 'Good' and went silent, leaving the patient confused about whether the transfer was happening.
- **Why it's a problem:** The abrupt, one-word non-sequitur 'Good' provides no meaningful closure or reassurance. The patient was left uncertain ('Oh... okay? Am I being transferred now?'), indicating the agent failed to properly complete the handoff interaction.
- **Expected behavior:** The agent should have said something like 'Please hold, you are now being transferred' or confirmed the transfer was in progress, then remained silent or played hold music — not responded with an ambiguous 'Good.'
- **Transcript hint:** AGENT: 'Good' / PATIENT: 'Oh... okay? Am I being transferred now?'

---

### Bug 14: Agent announces transfer twice with inconsistent messaging

- **Severity:** Low
- **Call:** `call_01_scheduler_20260701_152917.txt` (scheduler #1); recording `20260701_222642_CAb8bf1d50fc03f4acf2ca131e0cd168aa_REe0a13fb2f9ceb9e7cc31f6e5f8a08a7d.mp3`
- **What happened:** The agent first said it would transfer the patient to live support, then after the patient acknowledged, repeated a longer transfer announcement restating the problem before saying 'Connecting you to a representative.'
- **Why it's a problem:** The duplicate transfer announcements are redundant and slightly inconsistent in wording, creating a disjointed experience. The second announcement re-explains the situation unnecessarily after the patient has already agreed to hold.
- **Expected behavior:** The agent should provide a single, clear transfer message and then initiate the transfer without repeating the explanation.
- **Transcript hint:** AGENT: 'Please hold while I transfer you to live support.' ... AGENT: 'It looks like there's already a new patient appointment booked for you, but you weren't aware of it. I'll connect you to our patient support team...'

---

### Bug 15: Agent dismisses no-medication finding then processes refill without resolution

- **Severity:** High
- **Call:** `call_02_refill_20260701_153319.txt` (refill #2); recording `20260701_223053_CA78abad7f6812a1edc029c40852db2b72_RE560f97e34c0e05e026bcb296b6840b79.mp3`
- **What happened:** The agent first told the patient 'I don't see any medications on your chart that I can refill right now,' then after the patient pushed back, the agent said 'I'm processing your refill request for lisinopril ten milligram' as if the chart issue had been resolved — when it had not.
- **Why it's a problem:** The underlying data problem (no medications on file) was never resolved. The agent either falsely confirmed it would process a refill it cannot actually fulfill, or bypassed a legitimate clinical safeguard. Either outcome is dangerous: the patient may believe a refill is coming when none can be issued.
- **Expected behavior:** Having already identified that no medications are on file, the agent should not pivot to 'processing' the refill without escalating to a human or clearly explaining that the request is being flagged for manual review precisely because the medication is not on record.
- **Transcript hint:** 'I don't see any medications on your chart...' followed later by 'I'm processing your refill request for lisinopril ten milligram.'

---

### Bug 16: Agent ignores patient's concern that she may have reached wrong number

- **Severity:** Medium
- **Call:** `call_02_refill_20260701_153319.txt` (refill #2); recording `20260701_223053_CA78abad7f6812a1edc029c40852db2b72_RE560f97e34c0e05e026bcb296b6840b79.mp3`
- **What happened:** After the garbled greeting, the patient said 'I think I might have the wrong number — I'm trying to reach my doctor's office for a prescription refill.' The agent ignored this entirely and responded 'Great. What can I help you with today?'
- **Why it's a problem:** The patient expressed genuine confusion about whether she reached the correct office. Dismissing this without reassurance (e.g., confirming the practice name and that refill requests are handled there) risks the patient not realizing she is at an orthopaedics practice rather than her primary care provider, which is clinically relevant for a blood pressure medication refill.
- **Expected behavior:** The agent should have acknowledged the patient's concern, clearly stated the practice name and specialty, and confirmed whether a Lisinopril refill is something the practice can handle before proceeding.
- **Transcript hint:** 'Oh, I think I might have the wrong number' — Agent responds: 'Great. What can I help you with today?'

---

### Bug 17: Rescheduled date conflicts with original appointment date

- **Severity:** High
- **Call:** `call_03_cancel_20260701_153745.txt` (cancel #3); recording `20260701_223412_CA19554207398e8a0e59f7ba261e7fa7e2_RE43f33000c92d363d6e452de299769f8f.mp3`
- **What happened:** The agent offered and confirmed a new appointment on Wednesday, July 15 as a reschedule for the original appointment on Monday, July 20. However, July 15 is the week before July 20, meaning the 'rescheduled' appointment is actually earlier than the original, and the patient explicitly stated she wanted 'something next week' relative to her conflict the following week.
- **Why it's a problem:** The patient said she needed to move the July 20 appointment to 'the following week if possible,' implying a date after July 20. Instead the agent booked July 15, which is before the original appointment and likely still conflicts with her schedule. This could result in the patient missing care or showing up on the wrong date.
- **Expected behavior:** The agent should have offered dates in the week after July 20 (e.g., July 22 or later), or at minimum clarified with the patient whether July 15 (the prior week) was acceptable given her stated preference for the following week.
- **Transcript hint:** Patient: 'I need something next week if you have availability.' Agent: 'The first available is Wednesday, July 15 at 9AM.'

---

### Bug 18: Provider name changes inconsistently across the same call

- **Severity:** Medium
- **Call:** `call_03_cancel_20260701_153745.txt` (cancel #3); recording `20260701_223412_CA19554207398e8a0e59f7ba261e7fa7e2_RE43f33000c92d363d6e452de299769f8f.mp3`
- **What happened:** The provider's name is rendered differently at least four times during the call: 'Abeker,' 'Abrooker,' 'Abeker' again, and finally 'doctor Bricker.'
- **Why it's a problem:** The patient cannot reliably know which provider she is scheduled with. Inconsistent provider names suggest the agent is misreading or garbling stored data, which erodes patient trust and could cause confusion at check-in.
- **Expected behavior:** The agent should reference the provider by a single, consistent, correctly pronounced name throughout the call.
- **Transcript hint:** 'with Abeker' → 'with Abrooker' → 'with Abeker' → 'with doctor Bricker'

---

### Note: cancel call #3

- **Call:** `call_03_cancel_20260701_153745.txt` (cancel #3); recording `20260701_223412_CA19554207398e8a0e59f7ba261e7fa7e2_RE43f33000c92d363d6e452de299769f8f.mp3`
- **Observation:** The call completed the reschedule scenario but introduced a likely scheduling error (earlier date than requested) and continued the known provider-name garbling pattern in a distinct enough combination to warrant reporting.

### Bug 19: Agent gives vague, unverified insurance acceptance without confirming patient's specific plan

- **Severity:** Medium
- **Call:** `call_04_insurance_20260701_210033.txt` (insurance #4); recording `20260702_035948_CA655f0ec2b6a549edf446624243d176f7_RE1817db64b902dc8a8ddc3dacdbd0226f.mp3`
- **What happened:** When asked if Blue Cross is accepted, the agent said 'Pivot Point Orthopedics welcomes most insurance plans. Including Blue Cross.' without verifying whether the specific Blue Cross plan (e.g., Blue Cross Blue Shield PPO, HMO, specific state plan) is contracted and in-network.
- **Why it's a problem:** Insurance acceptance is highly plan-specific. A blanket 'we accept Blue Cross' statement can mislead the patient into assuming coverage when their particular plan or product may not be accepted, potentially resulting in unexpected out-of-pocket costs.
- **Expected behavior:** The agent should clarify that acceptance depends on the specific plan and recommend the patient confirm with the billing department or provide a number to call, rather than giving a broad affirmative that could be mistaken for verified coverage.
- **Transcript hint:** 'Pivot Point Orthopedics welcomes most insurance plans. Including Blue Cross.'

---

### Bug 20: Practice name inconsistency within same call

- **Severity:** Low
- **Call:** `call_04_insurance_20260701_210033.txt` (insurance #4); recording `20260702_035948_CA655f0ec2b6a549edf446624243d176f7_RE1817db64b902dc8a8ddc3dacdbd0226f.mp3`
- **What happened:** The agent greeted the caller as 'Pivot Point Orthopaedics' (British spelling) but then referred to the practice as 'Pivot Point Orthopedics' (American spelling) in the follow-up response.
- **Why it's a problem:** While minor, inconsistent spelling/pronunciation of the practice name within the same call can erode patient trust and suggests the agent is not reliably using the correct, official practice name.
- **Expected behavior:** The agent should use a single consistent practice name throughout the call, matching the officially registered name.
- **Transcript hint:** Greeting: 'Pivot Point Orthopaedics' vs. response: 'Pivot Point Orthopedics'

---

### Note: insurance call #4

- **Call:** `call_04_insurance_20260701_210033.txt` (insurance #4); recording `20260702_035948_CA655f0ec2b6a549edf446624243d176f7_RE1817db64b902dc8a8ddc3dacdbd0226f.mp3`
- **Observation:** Call largely succeeded in answering the patient's questions, but the insurance confirmation lacked necessary specificity and the practice name spelling was inconsistent.

### Bug 21: Agent abruptly abandons scheduling mid-process without explanation

- **Severity:** High
- **Call:** `call_05_edge_case_20260701_210832.txt` (edge_case #5); recording `20260702_040221_CA8f0d9461596bc498e8d470be71a062c2_RE127f56b22e35fe42d1512d7d2fb850a0.mp3`
- **What happened:** After repeatedly asking the patient to spell her name and last name (which had already been provided), the agent suddenly declared 'I can't proceed further right now' and transferred the call without explaining why it could not continue.
- **Why it's a problem:** The agent had enough information (full name and date of birth) to look up the patient and schedule an appointment. Abandoning the task with no explanation left the patient confused and without service, and the vague statement 'I can't proceed further right now' provided no actionable information.
- **Expected behavior:** The agent should have used the already-confirmed name and date of birth to look up availability on Tuesday and Wednesday afternoons and offered appointment slots, or clearly explained a specific reason why scheduling could not continue.
- **Transcript hint:** 'I can't proceed further right now. But I can make sure our clinic support team follows up with you.'

---

### Bug 22: Agent redundantly re-requests already-confirmed patient information

- **Severity:** Medium
- **Call:** `call_05_edge_case_20260701_210832.txt` (edge_case #5); recording `20260702_040221_CA8f0d9461596bc498e8d470be71a062c2_RE127f56b22e35fe42d1512d7d2fb850a0.mp3`
- **What happened:** The agent had already confirmed the patient's name as Sarah Johnson and date of birth as March 1985. Despite this, the agent subsequently asked for her phone number on file, then her last name, then her first name — all separately and sequentially — before ultimately failing to proceed.
- **Why it's a problem:** Re-collecting information the agent had already confirmed wastes the patient's time, erodes trust, and contributed to the patient's confusion. It also suggests a lack of coherent state management across the conversation.
- **Expected behavior:** Once name and date of birth are confirmed, the agent should proceed with scheduling without re-requesting the same identifying details piecemeal.
- **Transcript hint:** 'Last name for me just to make sure I have it exactly right.' / 'could you please spell your first name for me?' — after name was already confirmed earlier.

---

### Bug 23: Provider name garbled inconsistently across booking confirmations

- **Severity:** Medium
- **Call:** `call_06_urgent_20260701_211340.txt` (urgent #6); recording `20260702_040914_CAe0bbc1816cdcc1e39e2e1d9992e2fa75_RE12f1f73eb094ce04995869748a6791af.mp3`
- **What happened:** The provider's name was rendered at least three different ways during the call: 'doctor Zabigniew Likoski', then 'doctor Zee Bigmu Lukowski', then 'doctor z Bigniew Likoski'. Each utterance produced a noticeably different garbling of the same name.
- **Why it's a problem:** Patients cannot reliably identify or look up their provider when the name changes each time it is spoken. This erodes trust and may cause confusion at check-in.
- **Expected behavior:** The agent should render the provider's name consistently throughout the call, ideally with a stable phonetic approximation if the name is difficult to pronounce.
- **Transcript hint:** 'doctor Zabigniew Likoski' → 'doctor Zee Bigmu Lukowski' → 'doctor z Bigniew Likoski'

---

### Bug 24: Agent does not confirm cancellation-list placement before closing call

- **Severity:** Medium
- **Call:** `call_06_urgent_20260701_211340.txt` (urgent #6); recording `20260702_040914_CAe0bbc1816cdcc1e39e2e1d9992e2fa75_RE12f1f73eb094ce04995869748a6791af.mp3`
- **What happened:** The patient explicitly asked to be placed on a cancellation list for today. The agent acknowledged it verbally ('the clinic will contact you right away if a cancellation opens up') but never confirmed that the cancellation-list entry was actually created, nor gave the patient any reference or assurance that the action was completed in the system.
- **Why it's a problem:** Without explicit confirmation that the cancellation-list entry was recorded, the patient may wait at home expecting a call that never comes if the step was not actually executed.
- **Expected behavior:** After adding the patient to the cancellation list, the agent should explicitly state 'I've added you to today's cancellation list' (or equivalent) so the patient knows the action was completed, not just promised.
- **Transcript hint:** 'Yes. Your number is (609) 853-5680. If a cancellation opens up today, the clinic will contact you right away.'

---

### Bug 25: Practice name inconsistency within same call

- **Severity:** Low
- **Call:** `call_06_urgent_20260701_211340.txt` (urgent #6); recording `20260702_040914_CAe0bbc1816cdcc1e39e2e1d9992e2fa75_RE12f1f73eb094ce04995869748a6791af.mp3`
- **What happened:** The agent opened the call with 'Pitot Point Orthopedics' but in the appointment confirmation said 'Pivot Point Orthopedics'.
- **Why it's a problem:** An inconsistent or garbled practice name can confuse the patient about whether they reached the correct office and undermines professionalism.
- **Expected behavior:** The agent should use the correct, consistent practice name ('Pivot Point Orthopedics') throughout the entire call.
- **Transcript hint:** Greeting: 'Pitot Point Orthopedics' vs. confirmation: 'Pivot Point Orthopedics'

---

### Bug 26: Agent logs grossly incorrect billing amount ($285 billion) in case notes

- **Severity:** High
- **Call:** `call_07_billing_20260701_222053.txt` (billing #7); recording `20260702_051824_CAd5e8aabbf44ba0ea78ee1f0d5081714f_RE1bdf1c506bf3c22c560c47b1fd0b2f6f.mp3`
- **What happened:** When logging the patient's billing concern, the agent stated it had documented '$285,000,000,000' (two hundred eighty-five billion dollars) instead of $285.
- **Why it's a problem:** The agent transmitted a wildly incorrect dollar amount into the case notes, which could corrupt the billing dispute record. Although the agent verbally corrected itself when challenged, it is unclear whether the underlying logged note was actually fixed or merely verbally acknowledged as incorrect.
- **Expected behavior:** The agent should accurately capture and confirm the correct amount ($285) from the outset, and when an error is acknowledged, explicitly confirm that the stored/logged record has been corrected rather than simply asserting it verbally.
- **Transcript hint:** "I've logged your question about the $285,000,000,000 and your expected $40 co pay."

---

### Note: billing call #7

- **Call:** `call_07_billing_20260701_222053.txt` (billing #7); recording `20260702_051824_CAd5e8aabbf44ba0ea78ee1f0d5081714f_RE1bdf1c506bf3c22c560c47b1fd0b2f6f.mp3`
- **Observation:** The call largely resolved the patient's immediate concern, but the billing amount logging error is a significant data accuracy risk that was only partially addressed verbally.

### Bug 27: Agent accepts mismatched DOB with explicit 'demo purposes' disclosure to patient

- **Severity:** High
- **Call:** `call_08_referral_20260701_224324.txt` (referral #8); recording `20260702_054115_CAbaa9b61beddec9df40722f400aa14529_REec8cb270e89a8bda6eb1332181699623.mp3`
- **What happened:** After the patient's date of birth failed to match records, the agent said aloud: 'The birthday doesn't match our records. But for demo purposes, I'll accept it.' It then proceeded to document the referral request.
- **Why it's a problem:** Disclosing 'demo purposes' language to a real (or simulated) patient is a serious identity-verification failure. The agent should never bypass identity verification with a debug/demo rationale exposed to the caller, nor should it process a sensitive request (referral) for an unverified identity.
- **Expected behavior:** If DOB does not match, the agent should either ask the patient to confirm an alternative identifier or inform them it cannot verify their identity and offer to connect them with staff — without referencing internal demo/test logic.
- **Transcript hint:** 'The birthday doesn't match our records. But for demo purposes, I'll accept it.'

---

### Bug 28: Agent confirms insurance routing without verifying patient's actual plan details

- **Severity:** Medium
- **Call:** `call_08_referral_20260701_224324.txt` (referral #8); recording `20260702_054115_CAbaa9b61beddec9df40722f400aa14529_REec8cb270e89a8bda6eb1332181699623.mp3`
- **What happened:** When the patient asked whether the referral would be sent to an in-network Blue Cross provider, the agent immediately confirmed: 'Yes. The clinic team will review your insurance and send the referral to an in network Blue Cross provider.'
- **Why it's a problem:** The agent has not confirmed the patient's insurance plan on file, nor verified that Blue Cross is actually the carrier or that in-network PT providers are available. This mirrors the documented pattern of giving unverified insurance acceptance, but here specifically promises an in-network routing outcome the agent cannot guarantee.
- **Expected behavior:** The agent should clarify that the clinic team will review whatever insurance information is on file and make best efforts to route appropriately, without affirmatively confirming the specific carrier or network status it has not verified.
- **Transcript hint:** 'Yes. The clinic team will review your insurance and send the referral to an in network Blue Cross provider.'

---

### Bug 29: Agent discloses DOB mismatch failure then overrides it with 'demo purposes' statement to patient

- **Severity:** High
- **Call:** `call_09_results_20260702_155215.txt` (results #9); recording `20260702_224921_CAd6a4923c32c655e84b2579544c30aa58_RE1959f49fa267da161cd13c2391c8ea30.mp3`
- **What happened:** After already proceeding to document the callback number and take the patient's request, the agent suddenly announced 'The birthday doesn't match our record.' Then, instead of following a proper identity-verification failure protocol, it told the patient 'The clinic support for demo purposes, I'll accept your date of birth' and continued processing the request.
- **Why it's a problem:** This exposes an internal demo/testing override to a live caller, undermines HIPAA-compliant identity verification, and creates a serious patient privacy risk. It also reveals system internals to the patient in a confusing and unprofessional way.
- **Expected behavior:** If the DOB does not match, the agent should follow a defined mismatch protocol (e.g., ask for an alternate identifier, offer to transfer to staff) without disclosing internal demo overrides or bypassing verification for the patient.
- **Transcript hint:** "The clinic support for demo purposes, I'll accept your date of birth as 03/15/1985."

---

### Bug 30: Agent proceeds with request before completing identity verification, then flags mismatch out of sequence

- **Severity:** Medium
- **Call:** `call_09_results_20260702_155215.txt` (results #9); recording `20260702_224921_CAd6a4923c32c655e84b2579544c30aa58_RE1959f49fa267da161cd13c2391c8ea30.mp3`
- **What happened:** The agent collected the patient's DOB and then immediately began processing the results request and updating the callback number — only announcing a DOB mismatch much later in the call after the patient had already provided a new phone number and been told her request was documented.
- **Why it's a problem:** Identity verification should gate any further action. By proceeding to handle the request (updating contact info, documenting a results follow-up) before confirming a verified identity, the agent may have acted on or disclosed information for the wrong patient.
- **Expected behavior:** The agent should verify the DOB match before taking any action on the account, and should surface a mismatch immediately rather than partway through the interaction.
- **Transcript hint:** Agent says "I'll document your request" and updates the phone number, then much later says "The birthday doesn't match our record."

---

### Bug 31: Garbled or incomplete greeting omits opening word

- **Severity:** Low
- **Call:** `call_09_results_20260702_155215.txt` (results #9); recording `20260702_224921_CAd6a4923c32c655e84b2579544c30aa58_RE1959f49fa267da161cd13c2391c8ea30.mp3`
- **What happened:** The agent's opening line begins with 'For calling Pivot Point Orthopaedics' instead of 'Thank you for calling Pivot Point Orthopaedics' (or similar), dropping the start of the sentence.
- **Why it's a problem:** An incomplete or garbled greeting is unprofessional and may confuse callers about whether they reached the correct practice, eroding trust from the first moment of contact.
- **Expected behavior:** The agent should deliver a complete, coherent greeting such as 'Thank you for calling Pivot Point Orthopaedics, part of Pretty Good AI. How may I help you today?'
- **Transcript hint:** "For calling Pivot Point Orthopaedics, part of Pretty Good AI."

---

### Bug 32: Greeting contains extraneous promotional non-sequitur

- **Severity:** Medium
- **Call:** `call_10_records_20260702_155504.txt` (records #10); recording `20260702_225252_CA2f28b6985194115887ac684d3fdc12eb_RE2ef3aac294a0ead7a7f9ed7a4fb6a177.mp3`
- **What happened:** The agent opened with 'Thanks for calling Pivot Point Orthopaedics. Heard of Pretty Good AI?' — inserting what appears to be an unsolicited promotional reference to an AI product in the middle of the greeting.
- **Why it's a problem:** This is unprofessional and confusing for patients. A medical practice greeting should not include a promotional or rhetorical question about an AI vendor; it erodes trust and may make callers question whether they reached the right place.
- **Expected behavior:** The agent should greet the caller with a clean, professional opening such as 'Thank you for calling Pivot Point Orthopaedics. How may I help you today?' without any extraneous promotional content.
- **Transcript hint:** 'Thanks for calling Pivot Point Orthopaedics. Heard of Pretty Good AI? May I help you today?'

---

### Bug 33: Agent initiates caller ID verification before confirming identity, skipping proper intro

- **Severity:** Low
- **Call:** `call_10_records_20260702_155504.txt` (records #10); recording `20260702_225252_CA2f28b6985194115887ac684d3fdc12eb_RE2ef3aac294a0ead7a7f9ed7a4fb6a177.mp3`
- **What happened:** After the patient's first statement, the agent responded 'Calling from the number we have on file. Am I speaking with Sarah?' — a fragmented, unclear statement that appears to reference caller-ID matching without explaining what it means to the patient.
- **Why it's a problem:** The phrase 'Calling from the number we have on file' is grammatically incomplete and contextually confusing as a standalone sentence. It does not properly explain the verification step to the patient and could be disorienting.
- **Expected behavior:** The agent should clearly state it is attempting to verify the caller's identity, e.g., 'I can see your number matches a record we have on file. Am I speaking with Sarah Johnson?' to provide clear context.
- **Transcript hint:** 'Calling from the number we have on file. Am I speaking with Sarah?'

---

### Note: records call #10

- **Call:** `call_10_records_20260702_155504.txt` (records #10); recording `20260702_225252_CA2f28b6985194115887ac684d3fdc12eb_RE2ef3aac294a0ead7a7f9ed7a4fb6a177.mp3`
- **Observation:** The core records-transfer request was handled correctly — fax number captured and confirmed, request documented — but the greeting and identity-verification phrasing introduced unnecessary confusion.
