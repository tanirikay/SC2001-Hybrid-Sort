import gc 
import time 

import matplotlib.pyplot as plt
from hybrid_sort import generate_random_array, run_hybrid_sort, run_merge_sort

#----------------------
#   Experiment c(i)
#----------------------
n_values = [1000,2000,5000,10000,20000,50000,100000,200000,500000,1000000,2000000,5000000,10000000]
S = 20
comparison_results = []

print("----------------------")
print("   Experiment c(i)")
print("----------------------")
for n in n_values:
    arr = generate_random_array(n)
    comparison = run_hybrid_sort(arr, S)
    comparison_results.append(comparison)
    print("n =", n, "comparison =", comparison)

plt.plot(n_values,comparison_results,marker = "o",label = "Hybrid Sort")
plt.xscale("log")
plt.xlabel("Input Size n")
plt.ylabel("Number of Key Comparison")
plt.title(f"Key Comparison vs Input Size (S = {S})")

plt.legend()
plt.grid()
plt.savefig("part_c_i_.png")
plt.show()

#----------------------
#   Experiment c(ii)
#----------------------
n_value_ii = 100000
s_value = [1,2,5,10,20,50,100,200,500,1000]

comparison_results_ii = []

arr_ii = generate_random_array(n_value_ii)
print("----------------------")
print("   Experiment c(ii)")
print("----------------------")
for s_ii in s_value:
    comparsion_ii = run_hybrid_sort(arr_ii, s_ii)
    comparison_results_ii.append(comparsion_ii)
    print("S =", s_ii, "comparison =", comparsion_ii)

plt.plot(s_value, comparison_results_ii, marker="o")

plt.xlabel("Threshold S")
plt.ylabel("Number of Key Comparisons")
plt.title(f"Key Comparisons vs Threshold S (n = {n_value_ii})")

plt.grid()
plt.savefig("part_c_ii.png")
plt.show()
#----------------------
# Experiment c(iii): find the optimal S across different input sizes
#----------------------
# Comparisons alone are a bit misleading here: the fewest key comparisons
# always happens as S -> 1 (i.e. plain merge sort), because insertion
# sort's O(S^2) cost grows faster than the merge savings shrink. That's
# NOT the same as the fastest S in practice, because insertion sort's
# comparisons are individually cheaper (no recursive call / merge
# bookkeeping overhead). So "best performance" is judged here by CPU
# time, not comparison count - we plot both so you can show the
# discrepancy on a slide.
print("----------------------")
print(" Experiment c(iii)")
print("----------------------")
 
sizes_iii = [10000, 100000, 1000000]
s_values_iii = [1, 2, 5, 10, 20, 30, 50, 75, 100, 150, 200]
 
best_S_per_n = {}
# One sweep per size collects BOTH comparisons and time in the same pass,
# so we never re-sort the same (n, S) combination twice.
results_by_n = {}  # n -> (comparisons_list, time_list)
 
for n in sizes_iii:
    arr_iii = generate_random_array(n)
    comparisons_list = []
    time_list = []
    for s_iii in s_values_iii:
        gc.collect()
        t0 = time.perf_counter()
        comparison_iii = run_hybrid_sort(arr_iii, s_iii)
        t1 = time.perf_counter()
        comparisons_list.append(comparison_iii)
        time_list.append(t1 - t0)
        print("n =", n, "S =", s_iii, "comparison =", comparison_iii,
              "time =", round(t1 - t0, 4))
    results_by_n[n] = (comparisons_list, time_list)
    best_index = time_list.index(min(time_list))
    best_S_per_n[n] = s_values_iii[best_index]
 
# Plot 1: CPU time vs S, for each size
plt.figure()
for n in sizes_iii:
    _, time_list = results_by_n[n]
    plt.plot(s_values_iii, time_list, marker="o", label=f"n = {n}")
 
plt.xlabel("Threshold S")
plt.ylabel("CPU Time (seconds)")
plt.title("CPU Time vs Threshold S, for different input sizes")
plt.legend()
plt.grid()
plt.savefig("part_c_iii_time.png")
plt.show()
 
# Plot 2: comparisons vs S, for each size (reusing the SAME sweep - no
# re-sorting). This is what shows the "fewest comparisons" curve keeps
# favouring small S even though time does not - the discrepancy worth
# a slide of its own.
plt.figure()
for n in sizes_iii:
    comparisons_list, _ = results_by_n[n]
    plt.plot(s_values_iii, comparisons_list, marker="o", label=f"n = {n}")
 
plt.xlabel("Threshold S")
plt.ylabel("Number of Key Comparisons")
plt.title("Key Comparisons vs Threshold S, for different input sizes")
plt.legend()
plt.grid()
plt.savefig("part_c_iii_comparisons.png")
plt.show()
 
print()
print("Empirically best S per input size (by CPU time):")
for n, best_s in best_S_per_n.items():
    print("  n =", n, "-> best S =", best_s)
 
# Use the best S found for the largest tested size as our chosen
# "optimal" S to carry forward into Part D.
optimal_S = best_S_per_n[max(best_S_per_n)]
print("Chosen optimal S for Part D:", optimal_S)
 
#----------------------
# Part D: Hybrid Sort (optimal S) vs classic Merge Sort, n = 10,000,000
#----------------------
# A single timed run at n = 10,000,000 (which can take a minute or more)
# is unreliable: a garbage-collection pause or a moment of CPU
# throttling can shift the measurement by 10-40%, which is bigger than
# the real difference between the two algorithms. To get a trustworthy
# number we run several trials of EACH algorithm, INTERLEAVED (hybrid,
# classic, hybrid, classic, ...) so any drift over the course of the
# experiment affects both sides equally, with the garbage collector
# disabled during each timed block. We report the minimum time per
# algorithm, which is standard practice for microbenchmarks since noise
# can only slow a run down, never speed it up.
print("----------------------")
print(" Part D")
print("----------------------")
 
n_d = 10000000
arr_d = generate_random_array(n_d)
trials = 3
 
hybrid_times = []
classic_times = []
hybrid_comparison = None
classic_comparison = None
 
for trial in range(trials):
    gc.collect()
    gc.disable()
    t0 = time.perf_counter()
    hybrid_comparison = run_hybrid_sort(arr_d, optimal_S)
    t1 = time.perf_counter()
    gc.enable()
    hybrid_times.append(t1 - t0)
    print("[trial", trial + 1, "] Hybrid Sort   : comparison =", hybrid_comparison,
          "time =", round(t1 - t0, 2))
 
    gc.collect()
    gc.disable()
    t0 = time.perf_counter()
    classic_comparison = run_merge_sort(arr_d)
    t1 = time.perf_counter()
    gc.enable()
    classic_times.append(t1 - t0)
    print("[trial", trial + 1, "] Classic Merge : comparison =", classic_comparison,
          "time =", round(t1 - t0, 2))
 
hybrid_time_best = min(hybrid_times)
classic_time_best = min(classic_times)
 
print()
print("Hybrid Sort   (S =", optimal_S, "): comparisons =", hybrid_comparison,
      " best time =", round(hybrid_time_best, 2), "s  all times =",
      [round(t, 2) for t in hybrid_times])
print("Classic Merge Sort       : comparisons =", classic_comparison,
      " best time =", round(classic_time_best, 2), "s  all times =",
      [round(t, 2) for t in classic_times])
 
if hybrid_time_best < classic_time_best:
    print("=> Hybrid Sort is faster at n =", n_d)
else:
    print("=> Classic Merge Sort is faster at n =", n_d)
 
# Bar chart: key comparisons, hybrid vs classic
plt.figure()
plt.bar(["Hybrid Sort", "Classic Merge Sort"],
        [hybrid_comparison, classic_comparison],
        color=["tab:blue", "tab:orange"])
plt.ylabel("Number of Key Comparisons")
plt.title(f"Key Comparisons: Hybrid vs Classic Merge Sort (n = {n_d})")
plt.savefig("part_d_comparisons.png")
plt.show()
 
# Bar chart: CPU time, hybrid vs classic
plt.figure()
plt.bar(["Hybrid Sort", "Classic Merge Sort"],
        [hybrid_time_best, classic_time_best],
        color=["tab:blue", "tab:orange"])
plt.ylabel(f"CPU Time (seconds, best of {trials} trials)")
plt.title(f"CPU Time: Hybrid vs Classic Merge Sort (n = {n_d})")
plt.savefig("part_d_time.png")
plt.show()
 