# Data

Serengeti food web data extracted from Baskerville et al. (2011).

## Source

Baskerville EB, Dobson AP, Bedford T, Allesina S, Anderson TM, Pascual M (2011)
**Spatial Food Webs in Highly Variable Environments.**
*PLOS Computational Biology* 7(12): e1002321.
https://doi.org/10.1371/journal.pcbi.1002321

## Files

### serengeti_species.csv

161 species in the Serengeti ecosystem.

| Column | Description |
|--------|-------------|
| Code | 6-letter species code |
| Scientific_Name | Latin binomial |
| Trophic_Role | plant, herbivore, or carnivore |

**Counts:**
- 129 plants
- 23 herbivores  
- 9 carnivores

### serengeti_predation.csv

85 mammal-mammal predation links.

| Column | Description |
|--------|-------------|
| Predator_Code | 6-letter predator code |
| Prey_Code | 6-letter prey code |
| Predator_Species | Predator scientific name |
| Prey_Species | Prey scientific name |

**Network stats:**
- 30 mammal species
- 9 predator species
- 85 directed edges

## License

CC-BY 4.0 (derived from original CC-BY publication)

## Original Data

The full dataset (592 links including plants) is in the original publication's
Supporting Information Tables S1 and S2.
