#!/usr/bin/env python3
"""
Simple Classical Motif Analysis for Serengeti Food Web

This script runs classical (non-quantum) motif detection on the 
Serengeti mammal food web data.

Usage:
    python3 run_classical_analysis.py

The QOMIC paper (Ngo et al. 2024) compares quantum vs classical methods.
This implements the classical baseline for comparison.

Classical method: Enumerate all motif instances (including overlaps)
Quantum method: Find optimal non-overlapping motif sets (QOMIC)
"""

import json
from collections import defaultdict

# Common names for Serengeti mammals
COMMON_NAMES = {
    'ACIJUB': 'Cheetah', 'AEPMEL': 'Impala', 'ALCBUS': 'Hartebeest',
    'CANAUR': 'Golden jackal', 'CANMES': 'Black-backed jackal',
    'CARCAR': 'Caracal', 'CONTAU': 'Wildebeest', 'CROCRO': 'Spotted hyena',
    'DAMKOR': 'Topi', 'EQUBUR': 'Plains zebra', 'GAZGRA': "Grant's gazelle",
    'GAZTHO': "Thomson's gazelle", 'GIRCAM': 'Giraffe', 'HETBRU': 'Bush hyrax',
    'HIPAMP': 'Hippopotamus', 'KOBELL': 'Waterbuck', 'LEPSER': 'Serval',
    'LOXAFR': 'African elephant', 'LYCPIC': 'African wild dog',
    'MADKIR': "Kirk's dik-dik", 'OUROUR': 'Oribi', 'PANLEO': 'Lion',
    'PANPAR': 'Leopard', 'PAPANU': 'Olive baboon', 'PEDCAP': 'Springhare',
    'PHAAET': 'Warthog', 'PROCAP': 'Rock hyrax', 'REDRED': 'Reedbuck',
    'RHAPUM': 'Four-striped grass mouse', 'SYNCAF': 'African buffalo',
    'TAUORY': 'Common eland', 'TRASCR': 'Bushbuck'
}

def load_interactions(filepath='serengeti_predation_REAL.csv'):
    """Load predator-prey interactions from CSV."""
    interactions = []
    adj = defaultdict(set)  # predator -> set of prey
    
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#') or line.startswith('Predator'):
                continue
            parts = line.strip().split(',')
            if len(parts) >= 2:
                pred, prey = parts[0], parts[1]
                interactions.append((pred, prey))
                adj[pred].add(prey)
    
    return interactions, adj

def find_cascades(adj, exclude_self_loops=True):
    """
    Find CASCADE motifs: A → B → C
    
    A cascade represents a trophic chain where energy flows
    from prey C through intermediate predator B to top predator A.
    """
    cascades = []
    
    for a in adj:
        for b in adj[a]:
            if b in adj:
                for c in adj[b]:
                    # Exclude trivial cases
                    if exclude_self_loops and (c == a or c == b or a == b):
                        continue
                    cascades.append((a, b, c))
    
    return cascades

def find_ffls(adj, exclude_self_loops=True):
    """
    Find FEED-FORWARD LOOP motifs: A→B, B→C, A→C
    
    An FFL in ecology represents omnivory - a predator that
    feeds at multiple trophic levels.
    """
    ffls = []
    
    for a in adj:
        for b in adj[a]:
            if b in adj:
                for c in adj[b]:
                    if c in adj[a]:
                        if exclude_self_loops and (a == b or b == c or a == c):
                            continue
                        ffls.append((a, b, c))
    
    return ffls

def find_bifans(adj):
    """
    Find BIFAN motifs: Two predators share two prey
    A→C, A→D, B→C, B→D
    
    Bifans represent apparent competition - prey species that
    indirectly affect each other through shared predators.
    """
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
    
    return bifans

def get_name(code):
    """Get readable name for species code."""
    return COMMON_NAMES.get(code, code)

def main():
    print("=" * 70)
    print("CLASSICAL MOTIF ANALYSIS - Serengeti Food Web")
    print("=" * 70)
    print("\nThis is the classical (non-quantum) baseline method.")
    print("QOMIC uses quantum optimization to find non-overlapping motifs.\n")
    
    # Load data
    print("Loading data...")
    interactions, adj = load_interactions()
    print(f"  Loaded {len(interactions)} predator-prey interactions")
    print(f"  {len(adj)} unique predators")
    
    # Find motifs
    print("\n" + "-" * 70)
    print("DETECTING MOTIFS (Classical Enumeration)")
    print("-" * 70)
    
    # Cascades
    cascades = find_cascades(adj, exclude_self_loops=True)
    print(f"\n1. CASCADES (A→B→C): {len(cascades)} found")
    print("   Ecological meaning: Trophic chains / energy flow")
    if cascades:
        print("   Examples:")
        for a, b, c in cascades[:5]:
            print(f"      {get_name(a)} → {get_name(b)} → {get_name(c)}")
    
    # FFLs
    ffls = find_ffls(adj, exclude_self_loops=True)
    print(f"\n2. FEED-FORWARD LOOPS (A→B, B→C, A→C): {len(ffls)} found")
    print("   Ecological meaning: Omnivory patterns")
    if ffls:
        print("   Examples:")
        for a, b, c in ffls[:3]:
            print(f"      {get_name(a)} eats both {get_name(b)} and {get_name(c)}")
            print(f"      ({get_name(b)} also eats {get_name(c)})")
    
    # Bifans
    bifans = find_bifans(adj)
    print(f"\n3. BIFANS (shared predation): {len(bifans)} found")
    print("   Ecological meaning: Apparent competition")
    if bifans:
        print("   Examples:")
        for a, b, c, d in bifans[:3]:
            print(f"      {get_name(a)} & {get_name(b)} both eat {get_name(c)} & {get_name(d)}")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    total = len(cascades) + len(ffls) + len(bifans)
    print(f"""
    Cascades:  {len(cascades):>6}
    FFLs:      {len(ffls):>6}
    Bifans:    {len(bifans):>6}
    ─────────────────
    TOTAL:     {total:>6}
    
    Note: Classical method counts ALL instances (with overlaps).
    QOMIC quantum method finds optimal NON-OVERLAPPING sets.
    """)
    
    # Keystone analysis
    print("=" * 70)
    print("KEYSTONE SPECIES (by motif participation)")
    print("=" * 70)
    
    participation = defaultdict(int)
    
    for a, b, c in cascades:
        participation[a] += 1
        participation[b] += 1
        participation[c] += 1
    
    for a, b, c in ffls:
        participation[a] += 1
        participation[b] += 1
        participation[c] += 1
    
    for a, b, c, d in bifans:
        participation[a] += 1
        participation[b] += 1
        participation[c] += 1
        participation[d] += 1
    
    top_species = sorted(participation.items(), key=lambda x: -x[1])[:10]
    
    print(f"\n{'Rank':<5} {'Species':<30} {'Motif Count':<12}")
    print("-" * 50)
    for i, (code, count) in enumerate(top_species, 1):
        print(f"{i:<5} {get_name(code):<30} {count:<12}")
    
    # Export results
    results = {
        'method': 'classical_enumeration',
        'motif_counts': {
            'cascades': len(cascades),
            'ffls': len(ffls),
            'bifans': len(bifans),
            'total': total
        },
        'keystone_species': [(code, get_name(code), count) for code, count in top_species],
        'note': 'Classical method counts overlapping motifs. QOMIC finds non-overlapping optimal sets.'
    }
    
    with open('classical_motif_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: classical_motif_results.json")
    
    return results

if __name__ == '__main__':
    main()
