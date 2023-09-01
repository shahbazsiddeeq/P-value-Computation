import pandas as pd
import statsmodels.api as sm
from matplotlib import pyplot as plt 
import numpy as np
from statsmodels.stats.multitest import multipletests
# Load the genotype data and phenotype data
genotype_data = pd.read_csv("geotype.csv")
phenotype_data = pd.read_csv("phenotype.csv")
# Merge genotype and phenotype data based on the sample IDs
data = pd.merge(genotype_data, phenotype_data, on="sampleid")
# Create a design matrix for the fixed effects (genotypes and other covariates)
X = data[["SNP1", "SNP2", "SNP3", "SNP4"]]
X = sm.add_constant(X)  # Add a constant column for the intercept
# Create the dependent variable (phenotype)
y = data["trait"]

lin_model = sm.OLS(y, X)
result = lin_model.fit()
print(result.summary())

# Extract p-values
p_values = result.pvalues[1:]  # Exclude the constant term

# Correct for multiple testing (optional)
adjusted_p_values = multipletests(p_values, method="bonferroni")[1]

# Print the results
association_results_df = pd.DataFrame({"SNP": X.columns[1:],
                                       "P_Value": p_values,
                                       "Adjusted_P_Value": adjusted_p_values})

print(association_results_df)

plt.figure(figsize=(10, 6))
# Generate numeric values for the x-axis
x_values = range(len(association_results_df['SNP']))
# Plot the SNPs on the x-axis and p-values on the y-axis
plt.scatter(association_results_df['SNP'], -np.log10(association_results_df['P_Value']), color='blue', label='p-value')
plt.xticks(x_values, association_results_df['SNP'], rotation=45, ha='right')
# Add labels and title
plt.xlabel('SNPs')
plt.ylabel('-log10(p-value)')
plt.title('P-values of SNPs')
# Add a horizontal line at significance level (optional)
significance_level = -np.log10(0.05)
plt.axhline(y=significance_level, color='red', linestyle='dashed', label='Significance Level (p=0.05)')
# Add the p-value as text next to each point (optional)
for x, y, p_value in zip(x_values, -np.log10(association_results_df['P_Value']), association_results_df['P_Value']):
    plt.text(x, y, f'{p_value:.3f}', ha='center', va='bottom', fontsize=10)
# Show the legend
plt.legend()
# Display the plot
plt.tight_layout()
plt.show()
