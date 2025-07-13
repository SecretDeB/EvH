#!/usr/bin/env python3
# bloom-filter compression-inflation plot
#
# ─────────────────────────────────────────────────────────
#   BF bits  m  = -(n · ln p) / (ln 2)²
#   BF bytes     = m / 8
#   raw bytes per item = 1  (8-bit items)
#   Inflation ratio    = BF bytes / (n · 1)
# ─────────────────────────────────────────────────────────

import math
import matplotlib
matplotlib.use("Agg")                 # off-screen backend
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# parameters
# ------------------------------------------------------------
n_items = 10_000                       # number of elements
p_vals  = [1e-4, 1e-3, 1e-2] + [i/10 for i in range(1, 11)]   # 0.0001 … 1.0

# ------------------------------------------------------------
# compute BF bytes-per-raw-byte for each p
# ------------------------------------------------------------
inflation = []
for p in p_vals:
    m_bits   = -(n_items * math.log(p)) / (math.log(2) ** 2)  # optimal m
    bf_bytes = m_bits / 8
    inflation.append(bf_bytes / n_items)                      # raw-bytes = n_items

# ------------------------------------------------------------
# plotting
# ------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 6))      # 9 in wide × 6 in tall

ax.plot(p_vals, inflation, marker='o', color='#FFA500', lw=2)

# red point where p = 1
idx_one = p_vals.index(1.0)
ax.scatter([p_vals[idx_one]], [inflation[idx_one]], color='red', s=60, zorder=3)

# horizontal reference at y = 1
ax.axhline(1, ls='--', lw=1.4, color='#E09B00')


# ─── axes & grid ──────────────────────────────────────────
ax.set_xlabel('False-positive rate $p$', fontweight='bold', fontsize=14)
ax.set_ylabel('BF bytes ÷ raw byte',     fontweight='bold', fontsize=14)
# ax.set_title('Bloom Filter Compression Inflation', fontsize=16, pad=10)
ax.set_xlim(0, 1.0)
ax.set_ylim(0, 2.5)
ax.tick_params(labelsize=12)

# ticks: keep all, hide labels where p < 0.1
ax.set_xticks(p_vals)
ax.set_xticklabels(['' if p < 0.1 else f'{p:g}' for p in p_vals], rotation=40, ha='right')

ax.set_yticks([0, 0.5, 1, 1.5, 2, 2.5])

ax.grid(ls=':', linewidth=0.6, alpha=0.7)

plt.tight_layout()
plt.savefig('bf_compression_inflation.png', dpi=300)
plt.close()
