# Quantum Computing for Biodiversity Conservation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18157621.svg)](https://doi.org/10.5281/zenodo.18157621)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

**Technology Readiness Assessment by [Science Live](https://sciencelive.io)**

---

## Main Finding

> **Quantum computing methods for biodiversity network analysis are technically feasible but do not yet provide practical advantages over classical methods for current ecological dataset sizes.**

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

## PRISMA Scoping Review

| Stage | Count |
|-------|------:|
| Records identified | 1,649 |
| Records screened (ASReview) | 569 |
| Records included | 283 |
| Papers selected for case study | **2** |

### Selected Papers

| Paper | Purpose | DOI |
|-------|---------|-----|
| **QOMIC** (Ngo et al. 2024) | Quantum method | [10.1093/bioadv/vbae208](https://doi.org/10.1093/bioadv/vbae208) |
| **Serengeti Food Web** (Baskerville et al. 2011) | Ecological data | [10.1371/journal.pcbi.1002321](https://doi.org/10.1371/journal.pcbi.1002321) |

### Selection Process

AI-assisted PICO screening using:
- **Tool:** Science Live PICOScreener
- **Model:** Ollama qwen2.5:14b (local LLM)
- **PICO criteria:** [Nanopub RAvk9pmoZ2Ibe...](https://w3id.org/np/RAvk9pmoZ2IberoDe7zUWV0bVithiy6CnbSG5y06YuKM0)

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
│   └── serengeti_predation.csv    # 85 predation links
├── src/
│   ├── run_classical_analysis.py  # Motif enumeration + statistics
│   └── run_quantum_bifans.py      # QAOA quantum simulation
└── results/
    ├── classical_motif_results.json
    └── quantum_bifan_results.json
```

---

## Data

Serengeti food web from [Baskerville et al. (2011)](https://doi.org/10.1371/journal.pcbi.1002321).

### serengeti_species.csv

| Column | Description |
|--------|-------------|
| Code | 6-letter species code |
| Scientific_Name | Latin binomial |
| Trophic_Role | plant, herbivore, carnivore |

**Counts:** 129 plants, 23 herbivores, 9 carnivores

### serengeti_predation.csv

| Column | Description |
|--------|-------------|
| Predator_Code | 6-letter predator code |
| Prey_Code | 6-letter prey code |
| Predator_Species | Scientific name |
| Prey_Species | Scientific name |

**Network:** 30 mammals, 9 predators, 85 edges

---

## Methodology

### Network Motifs

**Bifan motif:** Two predators sharing two prey species (apparent competition)

```
Predator A    Predator B
    ↘    ╲  ╱    ↙
         ╳
    ↙    ╱  ╲    ↘
  Prey 1      Prey 2
```

### QUBO Formulation

Non-overlapping bifan selection as optimization:
- **Objective:** Maximize selected bifans
- **Constraint:** No two bifans share species
- **Method:** Quadratic Unconstrained Binary Optimization

### Quantum Algorithm

- **Algorithm:** QAOA (Quantum Approximate Optimization Algorithm)
- **Depth:** p=2
- **Optimizer:** COBYLA
- **Framework:** Qiskit 1.2.4
- **Qubits:** 15

---

## Results

### Statistical Significance

| Metric | Value |
|--------|-------|
| Bifans in real network | 629 |
| Random network mean | 589.3 |
| p-value | **0.023** |

**Interpretation:** Predators share prey more than expected by chance.

### Quantum vs Classical Comparison

| Method | Qubits | Optimal | Runtime |
|--------|--------|---------|---------|
| Classical (exact) | 15 | 3 bifans | ms |
| QAOA (quantum) | 15 | 3 bifans | seconds |

**Conclusion:** Same result, no quantum advantage at this scale.

### Selected Non-overlapping Bifans

1. Cheetah & Lion → Warthog & Impala
2. Golden jackal & Spotted hyena → Grant's gazelle & Wildebeest
3. Caracal & African wild dog → Kirk's dik-dik & Grass mouse

---

## Technology Readiness Assessment

| Aspect | Finding |
|--------|---------|
| **Feasibility** | ✅ Quantum methods work on ecological networks |
| **Advantage** | ❌ No practical benefit at current scales |
| **Break-even** | ~1000+ variables estimated |

### Recommendations

1. Continue monitoring quantum hardware developments
2. Use classical methods for current biodiversity applications
3. Prepare large-scale datasets (1000+ species) for future quantum readiness

---

## Nanopublications

All findings are documented as nanopublications in the Science Live space.

| Type | URI |
|------|-----|
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
- **Data:** CC-BY 4.0 (derived from Baskerville et al. 2011)

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

1. Ngo DKD et al. (2024) QOMIC: Quantum optimization for motif identification. *Bioinformatics Advances*. [DOI: 10.1093/bioadv/vbae208](https://doi.org/10.1093/bioadv/vbae208)

2. Baskerville EB et al. (2011) Spatial food webs in the Serengeti. *PLOS Computational Biology*. [DOI: 10.1371/journal.pcbi.1002321](https://doi.org/10.1371/journal.pcbi.1002321)

3. Farhi E et al. (2014) A Quantum Approximate Optimization Algorithm. [arXiv:1411.4028](https://arxiv.org/abs/1411.4028)

---

## Contact

**Anne Fouilloux**  
ORCID: [0000-0002-1784-2920](https://orcid.org/0000-0002-1784-2920)

---

*Part of the [Science Live](https://sciencelive4all.org) technology monitoring initiative*
