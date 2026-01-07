# Quantum Computing for Biodiversity Conservation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18157621.svg)](https://doi.org/10.5281/zenodo.18157621)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

**Technology Readiness Assessment by [Science Live](https://sciencelive4all.org)**

---

## Main Finding

> **Quantum computing methods for biodiversity network analysis are technically feasible but do not yet provide practical advantages over classical methods for current ecological dataset sizes.**

---

## What We Did

### The Question

Can quantum computing methods improve biodiversity research? To find out, we:

1. **Conducted a PRISMA scoping review** of quantum computing + biodiversity literature
2. **Selected 2 relevant papers** from 283 included studies
3. **Used 1 paper** (QOMIC) for practical implementation — the other was a review with no implementable method
4. **Applied the quantum method** to an ecological food web dataset

### Papers Selected from PRISMA Review

| Paper | DOI | Confidence | Used | Reason |
|-------|-----|------------|------|--------|
| **QOMIC** (Ngo et al. 2024) | [10.1093/bioadv/vbae208](https://doi.org/10.1093/bioadv/vbae208) | 0.9 | ✅ Yes | Quantum optimization for network motifs — implementable method |
| **Quantum Ecology Review** (2024) | [10.48550/arXiv.2504.03866](https://doi.org/10.48550/arXiv.2504.03866) | 0.7 | ❌ No | Review/perspective paper — no implementable method |

### The Adaptation

We took the **QOMIC method**, which uses quantum optimization to find network motifs in **gene regulatory networks**, and applied it to **ecological food webs**.

| Original (QOMIC) | Our Adaptation |
|------------------|----------------|
| Gene regulatory network | Food web network |
| Transcription factors → Genes | Predators → Prey |
| Bifan = shared gene regulation | Bifan = shared predation (apparent competition) |

### The Test Dataset

We used the **Serengeti food web** from [Baskerville et al. 2011](https://doi.org/10.1371/journal.pcbi.1002321) — a well-documented ecological network with 161 species and 592 feeding links.

> ⚠️ **Note:** The Baskerville paper was **not** part of the PRISMA review. It's a pure ecology paper (no quantum computing). We selected it separately as a suitable test dataset for applying the quantum method.

### The Result

Both quantum (QAOA) and classical methods found the **same optimal solution**. At current ecological dataset sizes (~15 qubits), there is **no quantum advantage**.

---

## PRISMA Scoping Review

| Stage | Count |
|-------|------:|
| Records identified | 1,649 |
| Records screened (ASReview) | 569 |
| Records included | 283 |
| Papers selected | **2** |
| Papers used for implementation | **1** (QOMIC) |

The review searched for papers at the intersection of **quantum computing** and **biodiversity**. Most included papers were about quantum algorithms or ecological modeling — but very few actually applied quantum methods to biodiversity problems.

Of the 2 selected papers:
- **QOMIC** — Provides implementable QAOA algorithm for network motif identification
- **arXiv review** — Perspective paper discussing potential applications, but no code/method to implement

### Selection Process

AI-assisted PICO screening using:
- **Tool:** Science Live PICOScreener
- **Model:** Ollama qwen2.5:14b (local LLM)
- **PICO criteria:** [Nanopub RAvk9pmoZ2Ibe...](https://w3id.org/np/RAvk9pmoZ2IberoDe7zUWV0bVithiy6CnbSG5y06YuKM0)

---

## Quick Start

```bash
# Clone
git clone https://github.com/annefou/quantum-biodiversity.git
cd quantum-biodiversity

# Environment
conda create -n qbio python=3.11 -y
conda activate qbio
pip install -r requirements.txt

# Run
python src/run_classical_analysis.py
python src/run_quantum_bifans.py
```

---

## Repository Structure

```
quantum-biodiversity/
├── README.md
├── LICENSE
├── CITATION.cff
├── requirements.txt
├── data/
│   ├── serengeti_species.csv      # 161 species
│   └── serengeti_predation.csv    # 85 mammal predation links
├── src/
│   ├── run_classical_analysis.py  # Motif enumeration + statistics
│   └── run_quantum_bifans.py      # QAOA quantum simulation
└── results/
    ├── classical_motif_results.json
    └── quantum_bifan_results.json
```

---

## Data

### Source

Serengeti food web from [Baskerville et al. (2011)](https://doi.org/10.1371/journal.pcbi.1002321) — selected separately as test dataset (NOT from PRISMA review).

### Files

**serengeti_species.csv** — 161 species (129 plants, 23 herbivores, 9 carnivores)

| Column | Description |
|--------|-------------|
| Code | 6-letter species code |
| Scientific_Name | Latin binomial |
| Trophic_Role | plant, herbivore, carnivore |

**serengeti_predation.csv** — 85 mammal predation links (30 species, 9 predators)

| Column | Description |
|--------|-------------|
| Predator_Code | 6-letter predator code |
| Prey_Code | 6-letter prey code |
| Predator_Species | Scientific name |
| Prey_Species | Scientific name |

---

## Method

### Network Motifs

A **bifan motif** is two predators that share two prey species:

```
Predator A    Predator B
    ↘    ╲  ╱    ↙
         ╳
    ↙    ╱  ╲    ↘
  Prey 1      Prey 2
```

In ecology, this represents **apparent competition** — predators indirectly affect each other through shared prey resources.

### QOMIC Approach

The [QOMIC method](https://doi.org/10.1093/bioadv/vbae208) finds the maximum set of **non-overlapping** motifs:

1. Enumerate all candidate bifan motifs
2. Formulate as QUBO (Quadratic Unconstrained Binary Optimization)
3. Solve with QAOA (Quantum Approximate Optimization Algorithm)

### Our Implementation

- **Framework:** Qiskit 1.2.4
- **Algorithm:** QAOA with p=2 layers
- **Optimizer:** COBYLA
- **Qubits:** 15 (one per candidate bifan)

---

## Results

### Statistical Significance

| Metric | Value |
|--------|-------|
| Bifans in real network | 629 |
| Random network mean | 589.3 |
| p-value | **0.023** |

**Interpretation:** Serengeti predators share prey species **more than expected by chance**, indicating ecological structuring through apparent competition.

### Quantum vs Classical

| Method | Qubits | Optimal | Runtime |
|--------|--------|---------|---------|
| Classical (exact) | 15 | 3 bifans | milliseconds |
| QAOA (quantum) | 15 | 3 bifans | seconds |

**Both methods find the same answer.** No quantum advantage at this scale.

### Selected Non-overlapping Bifans

1. Cheetah & Lion → Warthog & Impala
2. Golden jackal & Spotted hyena → Grant's gazelle & Wildebeest  
3. Caracal & African wild dog → Kirk's dik-dik & Grass mouse

---

## Technology Readiness Conclusion

| Aspect | Finding |
|--------|---------|
| **Feasibility** | ✅ Quantum methods can be adapted for ecological networks |
| **Advantage** | ❌ No practical benefit at current scales (~15 qubits) |
| **Break-even** | ~1000+ variables estimated |

### Recommendations

1. **Continue monitoring** quantum hardware developments
2. **Use classical methods** for current biodiversity applications  
3. **Prepare large-scale datasets** (1000+ species networks) for future quantum readiness

---

## Nanopublications

| Type | URI |
|------|-----|
| Study Assessment | [RAlN5rGFTlXaw...](https://w3id.org/np/RAlN5rGFTlXawYWAMdSDMm2SfTh8mfsN9Jhx-Oh7yXR-4) |
| PICO Criteria | [RAvk9pmoZ2Ibe...](https://w3id.org/np/RAvk9pmoZ2IberoDe7zUWV0bVithiy6CnbSG5y06YuKM0) |
| Science Live Space | [quantum-biodiversity-review](https://w3id.org/spaces/sciencelive/quantum-biodiversity-review) |

---

## Requirements

```
qiskit==1.2.4
qiskit-aer==0.15.1
qiskit-algorithms==0.3.0
qiskit-optimization==0.6.1
numpy>=1.24.0
```

---

## License

- **Code:** MIT License  
- **Data:** CC-BY 4.0 (derived from [Baskerville et al. 2011](https://doi.org/10.1371/journal.pcbi.1002321))

---

## Citation

```bibtex
@software{fouilloux2026quantum,
  author       = {Fouilloux, Anne},
  title        = {Quantum Computing for Biodiversity: Technology Readiness Assessment},
  year         = {2026},
  publisher    = {GitHub},
  url          = {https://github.com/annefou/quantum-biodiversity},
  doi          = {10.5281/zenodo.18157621}
}
```

---

## References

1. **QOMIC (quantum method):** Ngo DKD et al. (2024) Quantum optimization for motif identification in networks. *Bioinformatics Advances*. [DOI: 10.1093/bioadv/vbae208](https://doi.org/10.1093/bioadv/vbae208)

2. **Quantum ecology review:** (2024) Addressing ecological challenges from a quantum computing perspective. *arXiv*. [DOI: 10.48550/arXiv.2504.03866](https://doi.org/10.48550/arXiv.2504.03866)

3. **Serengeti food web (data):** Baskerville EB et al. (2011) Spatial food webs in the Serengeti. *PLOS Computational Biology*. [DOI: 10.1371/journal.pcbi.1002321](https://doi.org/10.1371/journal.pcbi.1002321)

4. **QAOA algorithm:** Farhi E et al. (2014) A Quantum Approximate Optimization Algorithm. [arXiv:1411.4028](https://arxiv.org/abs/1411.4028)

---

## Contact

**Anne Fouilloux** — ORCID: [0000-0002-1784-2920](https://orcid.org/0000-0002-1784-2920)

---

*Part of the [Science Live](https://sciencelive4all.org) technology monitoring initiative*
