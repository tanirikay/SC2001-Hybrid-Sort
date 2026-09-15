import matplotlib.pyplot as plt
import math
#Import hybrid sort and random array here
#get_dataset(n) --> random array from (b)
#hybrid_sort(arr, s) --> sort algorithm from (a)
n_values = [1000,2000,5000,10000,20000,50000,100000,200000,500000,1000000,2000000,5000000,10000000]
S = 20
comparison_results = []
theoretical_retults = []
ratios = []

#----------------------
#   Experiment c(i)
#----------------------

for n in n_values:
    arr = get_dataset(n)
    comparison = hybrid_sort(arr, s)
    comparison_results.append(comparison)
    print("n =", n, "comparison =", comparison)

#Theoretical analysis of time complexity (n log n)
for n in n_values:
    #calculate n log2 n, log2 is used because merge sort split into 2 halves
    theoretical = n * math.log2(n)
    theoretical_retults.append(theoretical)

#Comparing empirical results with theoretical analysis
for i in range(len(n_values)):
    #if ratio is about '1', it shows that time complexity is (n log n)
    ratio = comparison_results[i]/theoretical_retults[i]
    ratios.append(ratio)
    print("n =",n_values[i] , f"ratio = {ratio:.2f}")



plt.plot(n_values,comparison_results,marker = "o",label = "Hybrid Sort")
plt.xscale("log")
plt.xlabel("Input Size n")
plt.ylabel("Number of Key Comparison")
plt.title(f"Key Comparison vs Input Size (S = {S})")

plt.legend()
plt.grid()
plt.savefig("part_c_i_.png")
plt.show()

#Part C(ii)

#Part C(iii)

#Part D