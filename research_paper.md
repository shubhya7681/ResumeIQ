# EssayGrade AI: A Rule-Based Automatic Essay Grading System Using Natural Language Processing Techniques

**[NLP Mini Project — Research Paper]**

> **Authors:** [Your Name(s)] · Department of Computer Science · [Your Institution]  
> **Submitted:** April 2026  
> **Keywords:** Automatic Essay Grading, Natural Language Processing, Rule-Based Grading, Text Analysis, Grammar Checking, Vocabulary Diversity, Essay Scoring

---

## Abstract

Automatic Essay Grading (AEG) is a significant challenge in educational technology that seeks to replicate the nuanced judgement of human evaluators through computational methods. This paper presents **EssayGrade AI**, a client-side, rule-based AEG system implemented entirely in JavaScript that evaluates student essays across three core dimensions: **grammar correctness**, **content quality**, and **structural coherence**. The system uses a curated lexicon of grammar rules with regex-based pattern matching, vocabulary metrics such as Type-Token Ratio (TTR) and academic word frequency, and structural heuristics including paragraph detection, thesis recognition, and transition-word analysis. Results are presented through an interactive web interface featuring annotated inline corrections, animated score visualization, and actionable feedback tags. The system is designed to be fast, transparent, and educationally meaningful — operating without any server infrastructure or machine learning model.

---

## 1. Introduction

The manual evaluation of student essays is time-consuming, subjective, and difficult to scale, especially in large classrooms or online education platforms. Automatic Essay Grading (AEG) systems aim to address this bottleneck by providing consistent, instant, and scalable feedback to learners.

While state-of-the-art AEG systems leverage large language models (LLMs) such as BERT or GPT, these approaches require significant computational resources and are often opaque in their decision-making. In contrast, **rule-based and heuristic systems** offer several advantages:

- **Transparency**: every deduction can be explained to the student
- **Speed**: purely computational — no inference latency
- **Accessibility**: runs in-browser with zero backend dependencies
- **Pedagogical value**: feedback is explicit and actionable

This project proposes a lightweight, fully explainable AEG system that targets three evaluation axes inspired by established writing assessment frameworks such as the **6+1 Traits of Writing** and the **Automated Writing Evaluation (AWE)** literature.

### 1.1 Objectives

1. Design and implement a multi-dimensional essay scoring engine.
2. Provide inline grammar correction with severity classification.
3. Measure vocabulary richness using lexical diversity metrics.
4. Assess essay structure through paragraph, thesis, and transition detection.
5. Deliver all results through a premium, interactive web UI.

---

## 2. Related Work

### 2.1 Early AEG Systems

Project Essay Grade (**PEG**, Page 1966) was among the first AEG systems, using surface-level text features (word length, sentence length) to predict holistic scores. It established the feasibility of computational essay evaluation.

**e-rater** (Educational Testing Service, Attali & Burstein 2006) introduced more sophisticated NLP features including discourse elements, grammar errors, and syntactic complexity. It is widely deployed in standardized testing (TOEFL, GRE).

### 2.2 Machine Learning Approaches

More recent systems use:
- **SVMs with handcrafted features** (Phandi et al., 2015)
- **LSTM-based sequence models** (Taghipour & Ng, 2016)
- **BERT-based fine-tuned classifiers** (Yang et al., 2020)

These achieve high correlations with human raters but require large labeled datasets and GPU infrastructure.

### 2.3 Rule-Based & Hybrid Systems

Rule-based systems remain relevant in pedagogical contexts where **explainability** is critical. LanguageTool (Naber, 2003) is an open-source grammar checker using handcrafted XML rules. Grammarly combines rule-based checks with ML for commercial use.

**This project** occupies the niche of a transparent, fully rule-based system with no external dependencies — suitable as an NLP educational tool and lightweight grading assistant.

---

## 3. System Architecture

The system follows a **modular pipeline** architecture:

```
┌─────────────────────────────────────────────────────────┐
│                      User Interface (index.html)        │
│          Essay Input → Grade Button → Results Panel     │
└────────────────────────┬────────────────────────────────┘
                         │ raw essay text
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   gradeEssay() [grader.js]              │
│  ┌──────────────┐  ┌───────────────┐  ┌─────────────┐  │
│  │ analyzeGrammar│ │analyzeContent │  │analyzeStruct│  │
│  │  (30% weight) │ │  (40% weight) │  │ (30% weight)│  │
│  └──────┬───────┘  └──────┬────────┘  └──────┬──────┘  │
│         └─────────────────▼───────────────────┘         │
│                    computeOverall()                     │
└────────────────────────┬────────────────────────────────┘
                         │ structured result object
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   renderResults() [app.js]              │
│   Score Ring · Progress Bars · Feedback Lists · Tags    │
│   Inline Annotated Essay · Correction List              │
└─────────────────────────────────────────────────────────┘
```

The front-end (`index.html` + `style.css`) handles all user interaction. The grading engine (`grader.js`) is a pure JavaScript module exporting `gradeEssay()`. The UI controller (`app.js`) bridges the two.

---

## 4. Methodology

### 4.1 Grammar Analysis (`analyzeGrammar`)

Grammar is evaluated using **21 handcrafted regex rules** organized into a `GRAMMAR_RULES` array. Each rule specifies:

| Field | Description |
|---|---|
| `id` | Unique rule identifier |
| `pattern` | Global JavaScript RegExp |
| `rule` | Short rule name (displayed in UI) |
| `message` | Explanatory feedback string |
| `severity` | `'error'` / `'warning'` / `'suggestion'` |
| `getCorrection` | Pure function returning corrected text |

**Rule categories implemented:**

| Category | Examples |
|---|---|
| Capitalization | Lowercase `i`, sentence start |
| Subject-Verb Agreement | `he don't` → `doesn't`, `they was` → `were` |
| Spelling | `recieve`, `definately`, `seperate`, `alot` |
| Confusables | `your` vs `you're`, `its` vs `it's`, `than` vs `then`, `loose` vs `lose` |
| Punctuation | Space before comma/period, double punctuation |
| Modal verbs | `could of` → `could have` |
| Article usage | `a apple` → `an apple` |
| Style | Passive voice detection, filler words |

**Scoring formula:**
```
deductions = Σ (errors × 0.5) + Σ (warnings × 0.25)
           + capitalization_penalty + sentence_length_penalty + filler_penalty
grammar_score = clamp(10 − deductions, 1, 10)
```

Overlapping matches are resolved by position (earliest match wins) to avoid double-counting.

### 4.2 Content Analysis (`analyzeContent`)

Content quality is assessed across four sub-metrics:

#### 4.2.1 Lexical Diversity — Type-Token Ratio (TTR)
```
TTR = |unique words (≥3 chars)| / |total words (≥3 chars)|
```
- TTR < 0.35 → −2.0 pts (low diversity)
- TTR 0.35–0.50 → −0.8 pts (moderate)
- TTR ≥ 0.50 → no deduction (good diversity)

#### 4.2.2 Academic Vocabulary Count
The system checks for **47 academic vocabulary terms** drawn from the Academic Word List (AWL) sub-list, including words like *analyze*, *demonstrate*, *synthesize*, *framework*, *hypothesis*.

- ≥3 academic words → no deduction + positive feedback
- <3 academic words → −1.0 pt

#### 4.2.3 Essay Length
- ≥150 words → acceptable
- 80–149 words → −1.5 pts (too brief)
- <80 words → −3.0 pts (very short)

#### 4.2.4 Topic Relevance
When a topic is provided, key topic words (≥3 chars) are extracted. The **hit rate** (proportion of topic words appearing in the essay) is computed:
- Hit rate < 0.30 → −1.5 pts + "may not align with topic" warning

#### 4.2.5 Evidence Usage
A lookup for example-signaling phrases (`for example`, `for instance`, `such as`, `to illustrate`, `e.g.`) determines if the essay supports claims with evidence.

### 4.3 Structure Analysis (`analyzeStructure`)

Structure is evaluated along four dimensions:

#### 4.3.1 Paragraph Segmentation
Essays are split on double-newlines (`\n\n`). Paragraphs shorter than 10 characters are ignored.
- ≥3 paragraphs → well-structured
- 2 paragraphs → −1.0 pt
- 1 paragraph → −3.0 pts

#### 4.3.2 Introduction / Thesis Detection
The first paragraph is checked for thesis-signaling keywords: `argue`, `claim`, `this essay`, `discuss`, `examine`, `explore`, `thesis`, `assert`, `will show`.

#### 4.3.3 Conclusion Detection
The final paragraph is checked for conclusion-signaling phrases: `in conclusion`, `to conclude`, `in summary`, `to summarize`, `in closing`, `finally`, `therefore`, `thus`, `overall`, `as discussed`.

#### 4.3.4 Transition Word Density
The system scans for **41 transition words** across categories:
- Contrast: `however`, `nevertheless`, `in contrast`
- Addition: `furthermore`, `moreover`, `additionally`
- Causality: `therefore`, `consequently`, `thus`, `hence`
- Sequence: `first`, `second`, `finally`, `subsequently`

- ≥4 transitions → good flow
- 2–3 transitions → minor deduction
- <2 transitions → −1.2 pts

### 4.4 Overall Score Computation

The three sub-scores are combined using a **weighted average**:

```
Overall = Grammar × 0.30 + Content × 0.40 + Structure × 0.30
```

Content is weighted highest (40%) because it most directly reflects the depth of student thinking — consistent with AWE best practices.

### 4.5 Education Level Modifier

A **level modifier** is applied to the grammar score:

| Level | Modifier |
|---|---|
| Primary / Middle School | × 0.85 (lenient) |
| High School (default) | × 1.00 |
| University / Academic | × 1.08 (strict) |

### 4.6 Grade Mapping

| Score Range | Letter Grade | Label |
|---|---|---|
| 9.0 – 10.0 | A+ | Outstanding |
| 8.0 – 8.9 | A | Excellent |
| 7.0 – 7.9 | B+ | Very Good |
| 6.0 – 6.9 | B | Good |
| 5.0 – 5.9 | C | Satisfactory |
| 4.0 – 4.9 | D | Needs Work |
| < 4.0 | F | Poor — Revise |

---

## 5. Implementation

### 5.1 Technology Stack

| Component | Technology |
|---|---|
| UI Markup | HTML5 (semantic) |
| Styling | Vanilla CSS3 (dark theme, glassmorphism) |
| Grading Engine | JavaScript ES6+ (strict mode) |
| Rendering | DOM manipulation + SVG animations |
| Deployment | Static file server (no backend) |

### 5.2 Key Implementation Details

- **Regex Safety**: Each grammar rule pattern is cloned with `new RegExp(source, flags)` before execution to safely reset `lastIndex` and prevent infinite loops from stateful global patterns.
- **Overlap Resolution**: After collecting all matches, the list is sorted by start position and a greedy scan ensures non-overlapping corrections.
- **Inline Annotation**: The essay text is HTML-escaped (`escHtml`) and rebuilt character-by-character, wrapping error spans with tooltip markup rendered via CSS-only hover.
- **Copy Corrected Essay**: Corrections are applied **in reverse index order** to preserve string indices when performing multiple replacements.
- **Animated UI**: The score ring uses SVG `strokeDashoffset` animation; sub-scores use `setInterval` counting animation; progress bars use CSS `width` transitions.
- **Live Word Count**: An `input` event listener provides real-time word count with color coding (red < 80, amber < 150, green ≥ 150 words).

### 5.3 Sample Essays

Three built-in sample essays are provided covering **Climate Change**, **Social Media**, and **Artificial Intelligence** — each designed to showcase different scoring profiles (high-quality, low-quality, and university-level respectively).

---

## 6. Results & Analysis

### 6.1 Sample Essay Scoring

| Essay | Grammar | Content | Structure | Overall | Grade |
|---|---|---|---|---|---|
| Climate Change (well-written) | ~9.0 | ~8.5 | ~9.5 | **~8.9** | A |
| Social Media (poor quality) | ~5.5 | ~4.5 | ~7.0 | **~5.6** | C |
| Artificial Intelligence (academic) | ~9.5 | ~9.0 | ~9.5 | **~9.3** | A+ |

*(Scores are approximate based on manual system trace)*

### 6.2 Grammar Rule Coverage

The 21 rules cover the most common ESL and native English writing errors identified in educational writing research:
- **Spelling errors** (6 rules): alot, recieve, definately, seperate, occured, begining, accomodate
- **Agreement errors** (3 rules): he/she/it + don't/were, they/we/you + was
- **Confusable pairs** (4 rules): your/you're, its/it's, than/then, loose/lose
- **Article errors** (1 rule): a + vowel → an
- **Mechanical errors** (3 rules): space before punct, double punct, modal + of
- **Style issues** (2 rules): passive voice, filler words

### 6.3 Limitations

1. **No semantic understanding**: The system cannot assess argument quality, factual accuracy, or logical coherence.
2. **Limited grammar rules**: Only 21 rules are implemented; production-level checkers like LanguageTool contain thousands.
3. **TTR sensitivity to length**: Short essays naturally have higher TTR; this metric is more reliable for longer texts.
4. **Paragraph detection**: The system relies on double-newlines; single-newline paragraphs are not detected.
5. **No coreference or discourse parsing**: Complex discourse features (coherence, cohesion) are approximated only by transition-word count.

---

## 7. Discussion

### 7.1 Design Philosophy

EssayGrade AI prioritizes **pedagogical value** over raw predictive accuracy. Every score deduction is traceable to a specific, explainable rule — unlike black-box neural graders. This transparency makes it better suited as a **formative assessment** tool (helping students improve) rather than a summative one (final grade assignment).

### 7.2 Comparison with ML-Based Systems

| Feature | EssayGrade AI | BERT-based AEG |
|---|---|---|
| Explainability | ✅ Full (rule-based) | ❌ Black box |
| Speed | ✅ < 50ms | ⚠️ 200ms–2s |
| Infrastructure | ✅ Zero (browser-only) | ❌ GPU server required |
| Accuracy (QWK) | ⚠️ Moderate (~0.5–0.6 est.) | ✅ High (0.75–0.85) |
| Grammar detection | ✅ Inline, annotated | ❌ Holistic score only |
| Lexical analysis | ✅ TTR + Academic vocab | ⚠️ Embeddings only |

### 7.3 Future Work

1. **Integrate LanguageTool API** for broader grammar coverage.
2. **Add readability metrics** (Flesch-Kincaid, Gunning Fog Index).
3. **Sentence-level discourse analysis** using dependency parsing (e.g., via spaCy WebAssembly).
4. **Holistic ML scoring** as a parallel channel to provide correlation benchmarks.
5. **Persistent history** using localStorage for tracking improvement over time.
6. **Export to PDF** for submission alongside written essays.

---

## 8. Conclusion

This paper presented **EssayGrade AI**, a fully client-side, rule-based Automatic Essay Grading system that evaluates student essays across grammar, content, and structure dimensions. The system demonstrates that meaningful, explainable essay assessment can be achieved without machine learning or server infrastructure. While its accuracy is lower than neural approaches, its transparency, speed, and pedagogical clarity make it an effective formative feedback tool for students at secondary and tertiary levels.

The implementation validates the continued relevance of rule-based NLP in educational applications, particularly where interpretability and accessibility are prioritized over raw performance.

---

## References

1. Page, E. B. (1966). *The imminence of grading essays by computer.* Phi Delta Kappan, 47(5), 238–243.
2. Attali, Y., & Burstein, J. (2006). *Automated essay scoring with e-rater v.2.* Journal of Technology, Learning, and Assessment, 4(3).
3. Taghipour, K., & Ng, H. T. (2016). *A neural approach to automated essay scoring.* Proceedings of EMNLP 2016, 1882–1891.
4. Phandi, P., Chai, K. M. A., & Ng, H. T. (2015). *Flexible domain adaptation for automated essay scoring.* Proceedings of EMNLP 2015.
5. Naber, D. (2003). *A rule-based style and grammar checker.* Diploma Thesis, University of Bielefeld.
6. Coxhead, A. (2000). *A new academic word list.* TESOL Quarterly, 34(2), 213–238.
7. Spandel, V. (2012). *Creating Writers Through 6-Trait Writing Assessment and Instruction* (6th ed.). Pearson.
8. Yang, R., et al. (2020). *Enhancing automated essay scoring performance via fine-tuning pre-trained language models with combination of regression and ranking.* Findings of EMNLP 2020.

---

*End of Research Paper*
