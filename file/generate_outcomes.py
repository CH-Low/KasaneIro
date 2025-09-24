import pandas as pd
from itertools import product

# --- Dominoes ---
dominoes = [
    ('RR', ('R','R')),
    ('RB', ('R','B')),
    ('RY', ('R','Y')),
    ('BY', ('B','Y')),
    ('BB', ('B','B')),
    ('YY', ('Y','Y')),
]

# --- Build adjacency pairs for 3x3 ---
pairs = []
rows, cols = 3,3
for r in range(rows):
    for c in range(cols):
        i = r*cols + c
        if c+1 < cols:   # right neighbor
            j = r*cols + (c+1)
            pairs.append((i,j))
        if r+1 < rows:   # down neighbor
            j = (r+1)*cols + c
            pairs.append((i,j))

print("Adjacent pairs (should be 12):", len(pairs))

# --- Color merge mapping ---
def merge_colors(s):
    """Return final visible color after stacking tokens in a cell"""
    if not s: return "'W'"
    if s == {'R'}: return "'R'"
    if s == {'B'}: return "'B'"
    if s == {'Y'}: return "'Y'"
    if s == {'R','B'}: return "'P'"   # Purple
    if s == {'R','Y'}: return "'O'"   # Orange
    if s == {'B','Y'}: return "'G'"   # Green
    return ''  # shouldn't happen (more than 2 tokens not allowed)

# --- Symmetry helpers (rotations & reflections of 3x3) ---
def transform(layout, kind):
    """Return transformed layout as tuple of 9"""
    L = list(layout)
    if kind == "rot90":   # rotate 90 clockwise
        return tuple([L[6],L[3],L[0],
                      L[7],L[4],L[1],
                      L[8],L[5],L[2]])
    if kind == "rot180":
        return tuple([L[8],L[7],L[6],
                      L[5],L[4],L[3],
                      L[2],L[1],L[0]])
    if kind == "rot270":
        return tuple([L[2],L[5],L[8],
                      L[1],L[4],L[7],
                      L[0],L[3],L[6]])
    if kind == "flipH":   # horizontal flip
        return tuple([L[2],L[1],L[0],
                      L[5],L[4],L[3],
                      L[8],L[7],L[6]])
    if kind == "flipV":   # vertical flip
        return tuple([L[6],L[7],L[8],
                      L[3],L[4],L[5],
                      L[0],L[1],L[2]])
    if kind == "flipD1":  # main diagonal
        return tuple([L[0],L[3],L[6],
                      L[1],L[4],L[7],
                      L[2],L[5],L[8]])
    if kind == "flipD2":  # anti-diagonal
        return tuple([L[8],L[5],L[2],
                      L[7],L[4],L[1],
                      L[6],L[3],L[0]])
    return tuple(L)

def canonical(layout):
    """Return canonical representative of layout under dihedral group (8 symmetries)"""
    variants = []
    base = tuple(layout)
    variants.append(base)
    variants.append(transform(base,"rot90"))
    variants.append(transform(base,"rot180"))
    variants.append(transform(base,"rot270"))
    variants.append(transform(base,"flipH"))
    variants.append(transform(base,"flipV"))
    variants.append(transform(base,"flipD1"))
    variants.append(transform(base,"flipD2"))
    return min(variants)

# --- Coverage check ---
def check_coverage(counts, allow_center_empty=False):
    if allow_center_empty:
        if counts[4] != 0:   # center must be uncovered
            return False
        return all(counts[i] > 0 for i in range(9) if i != 4)
    else:
        return all(counts[i] > 0 for i in range(9))

# --- Main enumeration ---
def enumerate_unique_layouts(require_center_empty=False):
    unique_layouts = set()
    pair_indices = list(range(len(pairs)))
    total_checked = 0

    for assign in product(pair_indices, repeat=len(dominoes)):  # 12^6 ~ 3M
        total_checked += 1
        counts = [0]*9
        valid = True
        for di, pair_idx in enumerate(assign):
            a,b = pairs[pair_idx]
            counts[a] += 1
            counts[b] += 1
            if counts[a] > 2 or counts[b] > 2:
                valid = False
                break
        if not valid:
            continue
        if not check_coverage(counts, allow_center_empty=require_center_empty):
            continue
        # build cell sets
        cell_sets = [set() for _ in range(9)]
        for di, pair_idx in enumerate(assign):
            a,b = pairs[pair_idx]
            _, halves = dominoes[di]
            c1, c2 = halves
            cell_sets[a].add(c1)
            cell_sets[b].add(c2)
        labels = [merge_colors(s) for s in cell_sets]
        # normalize by symmetry
        unique_layouts.add(canonical(labels))

    return unique_layouts, total_checked

# --- Run both scenarios ---
all_filled, checked1 = enumerate_unique_layouts(require_center_empty=False)
center_empty, checked2 = enumerate_unique_layouts(require_center_empty=True)

print("Assignments checked:", checked1 + checked2)
print("Unique outcomes (all filled, sym-reduced):", len(all_filled))
print("Unique outcomes (center empty, sym-reduced):", len(center_empty))

# --- Save ---
# df_all = pd.DataFrame(list(all_filled), columns=[f'c{i}' for i in range(9)])
# df_center = pd.DataFrame(list(center_empty), columns=[f'c{i}' for i in range(9)])
# df_all.to_csv("final_unique_outcomes_all_filled.csv", index=False)
# df_center.to_csv("final_unique_outcomes_center_empty.csv", index=False)

def save_csv_with_bracket(layouts, filename):
    with open(filename, "w") as f:
        for row in layouts:
            f.write(",".join(row) + "]\n")
            
save_csv_with_bracket(all_filled, "final_unique_outcomes_all_filled.csv")
save_csv_with_bracket(center_empty, "final_unique_outcomes_center_empty.csv")
            
print("Files written: final_unique_outcomes_all_filled.csv, final_unique_outcomes_center_empty.csv")
