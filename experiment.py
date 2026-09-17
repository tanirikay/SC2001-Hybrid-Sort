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
#   Experiment c(iii)
#----------------------

#Part D