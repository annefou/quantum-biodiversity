#!/usr/bin/env python3
"""
QOMIC Quantum Simulation - Bifan Motifs (FIXED VERSION)
Serengeti Food Web

Install requirements:
    pip install qiskit==1.2.4 qiskit-aer==0.15.1 qiskit-algorithms==0.3.0 qiskit-optimization==0.6.1
"""

import numpy as np
from collections import defaultdict
from itertools import combinations
import warnings
warnings.filterwarnings('ignore')

from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms import QAOA, NumPyMinimumEigensolver
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import Sampler  # This works with qiskit 1.2.4

print("="*70)
print("QOMIC QUANTUM SIMULATION - BIFAN MOTIFS")
print("Serengeti Food Web - Non-overlapping Apparent Competition Patterns")
print("="*70)

COMMON_NAMES = {
    'ACIJUB': 'Cheetah', 'AEPMEL': 'Impala', 'ALCBUS': 'Hartebeest',
    'CANAUR': 'Golden jackal', 'CANMES': 'Black-backed jackal',
    'CARCAR': 'Caracal', 'CONTAU': 'Wildebeest', 'CROCRO': 'Spotted hyena',
    'DAMKOR': 'Topi', 'EQUBUR': 'Plains zebra', 'GAZGRA': "Grant's gazelle",
    'GAZTHO': "Thomson's gazelle", 'GIRCAM': 'Giraffe', 'HETBRU': 'Bush hyrax',
    'KOBELL': 'Waterbuck', 'LEPSER': 'Serval', 'LYCPIC': 'African wild dog',
    'MADKIR': "Kirk's dik-dik", 'OUROUR': 'Oribi', 'PANLEO': 'Lion',
    'PANPAR': 'Leopard', 'PHAAET': 'Warthog', 'PROCAP': 'Rock hyrax', 
    'REDRED': 'Reedbuck', 'RHAPUM': 'Grass mouse', 'SYNCAF': 'Buffalo',
    'TAUORY': 'Eland', 'TRASCR': 'Bushbuck'
}

def get_name(code):
    return COMMON_NAMES.get(code, code)

# Load data
print("\n[1] Loading data and finding bifan motifs...")

import os
data_file = 'serengeti_predation_REAL.csv'
if not os.path.exists(data_file):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(script_dir, 'serengeti_predation_REAL.csv')

adj = defaultdict(set)
with open(data_file, 'r') as f:
    for line in f:
        if line.startswith('#') or line.startswith('Predator'):
            continue
        parts = line.strip().split(',')
        if len(parts) >= 2:
            adj[parts[0]].add(parts[1])

# Find bifans
bifans = []
predators = list(adj.keys())
for i, a in enumerate(predators):
    for b in predators[i+1:]:
        shared = adj[a] & adj[b]
        if len(shared) >= 2:
            shared_list = list(shared)
            for j, c in enumerate(shared_list):
                for d in shared_list[j+1:]:
                    bifans.append((a, b, c, d))

print(f"    Found {len(bifans)} bifan motifs total")

# Select diverse subset
selected = []
used_pred_pairs = set()
for bifan in bifans:
    pred_pair = tuple(sorted([bifan[0], bifan[1]]))
    if pred_pair not in used_pred_pairs and len(selected) < 10:
        selected.append(bifan)
        used_pred_pairs.add(pred_pair)

for bifan in bifans:
    if bifan not in selected and len(selected) < 15:
        selected.append(bifan)

bifans = selected
n_motifs = len(bifans)

print(f"    Selected {n_motifs} bifans for quantum optimization\n")
print("    Bifan motifs (predator pair → prey pair):")
for i, (a, b, c, d) in enumerate(bifans):
    print(f"      B{i}: ({get_name(a)}, {get_name(b)}) → ({get_name(c)}, {get_name(d)})")

# Find overlaps
print(f"\n[2] Building QUBO...")
def motifs_overlap(m1, m2):
    return len(set(m1) & set(m2)) > 0

overlaps = []
for i in range(n_motifs):
    for j in range(i+1, n_motifs):
        if motifs_overlap(bifans[i], bifans[j]):
            overlaps.append((i, j))

print(f"    {n_motifs} variables, {len(overlaps)} overlap constraints")

# Build QUBO
qp = QuadraticProgram("serengeti_bifans")
for i in range(n_motifs):
    qp.binary_var(f"x{i}")

linear = {f"x{i}": -1 for i in range(n_motifs)}
PENALTY = 10
quadratic = {(f"x{i}", f"x{j}"): PENALTY for i, j in overlaps}
qp.minimize(linear=linear, quadratic=quadratic)

# Classical solution
print(f"\n[3] Classical (exact) solution...")
classical_solver = NumPyMinimumEigensolver()
classical_result = MinimumEigenOptimizer(classical_solver).solve(qp)
classical_selected = [i for i in range(n_motifs) if classical_result.x[i] > 0.5]
print(f"    Found {len(classical_selected)} non-overlapping bifans")

# QAOA solution - FIXED VERSION
print(f"\n[4] QAOA quantum simulation...")
print(f"    Qubits: {n_motifs}")
print(f"    QAOA layers: 2")

try:
    # Use the standard Sampler from qiskit.primitives
    sampler = Sampler()
    qaoa = QAOA(sampler=sampler, optimizer=COBYLA(maxiter=100), reps=2)
    qaoa_result = MinimumEigenOptimizer(qaoa).solve(qp)
    quantum_selected = [i for i in range(n_motifs) if qaoa_result.x[i] > 0.5]
    print(f"    ✓ Found {len(quantum_selected)} non-overlapping bifans (QAOA)")
    qaoa_success = True
except Exception as e:
    print(f"    ✗ QAOA failed: {e}")
    quantum_selected = []
    qaoa_success = False

# Results
print("\n" + "="*70)
print("RESULTS")
print("="*70)

def check_valid(selected, motifs):
    if not selected:
        return True
    for i, j in combinations(selected, 2):
        if motifs_overlap(motifs[i], motifs[j]):
            return False
    return True

print(f"\n{'Method':<15} {'Count':<10} {'Valid':<10} {'Motifs'}")
print("-"*65)
print(f"{'Classical':<15} {len(classical_selected):<10} {'✓' if check_valid(classical_selected, bifans) else '✗':<10} {classical_selected}")
if qaoa_success:
    print(f"{'QAOA':<15} {len(quantum_selected):<10} {'✓' if check_valid(quantum_selected, bifans) else '✗':<10} {quantum_selected}")

print("\n" + "-"*65)
print("CLASSICAL SOLUTION:")
print("-"*65)
for i in classical_selected:
    a, b, c, d = bifans[i]
    print(f"  B{i}: {get_name(a)} & {get_name(b)} → {get_name(c)} & {get_name(d)}")

if qaoa_success and quantum_selected:
    print("\n" + "-"*65)
    print("QAOA QUANTUM SOLUTION:")
    print("-"*65)
    for i in quantum_selected:
        a, b, c, d = bifans[i]
        print(f"  B{i}: {get_name(a)} & {get_name(b)} → {get_name(c)} & {get_name(d)}")

print("\n" + "="*70)
print("COMPLETE")
print("="*70)

import json
results = {
    'classical': {'count': len(classical_selected), 'selected': classical_selected},
    'qaoa': {'count': len(quantum_selected), 'selected': quantum_selected, 'success': qaoa_success}
}
with open('quantum_bifan_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print("Results saved to: quantum_bifan_results.json")
