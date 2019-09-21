from scipy.stats import chi2_contingency
from scipy.stats import chi2

# Game on 327
#          Ctrl, V1, V2, V3
# Game       15   5   8  10
# Not Game   55  37  41  33

# Game on 544
#          Ctrl, V1, V2, V3
# Game       9   3   3  6
# Not Game   30  34  41  32         
table = [[15, 5, 8, 10],
         [70-15, 42-5, 49-8, 43-10]]

table1 = [[9, 3, 3, 6], [30, 34, 41, 32]]
stat, p, dof, expected = chi2_contingency(table1)
print('* Degree of Freedom: %d' % dof)

# 解释结果
prob = 0.95
critical = chi2.ppf(prob, dof)
print('* Accept Probability = %.3f' % prob)
print('* Critical = %.3f' % critical)

print('* Interpretation as follows:')
print('- Chi^2 = %.3f' % stat)
print('- P-val = %.3f' % p)
if abs(stat) >= critical:
    print('- Dependent (reject H0)')
else:
    print('- Independent (fail to reject H0)')

alpha = 1.0 - prob
if p <= alpha:
    print('- p-value(%.2f) <= %.2f, dependent (reject H0)' % (p, alpha))
else:
    print('- p-value(%.2f) > %.2f, independent (fail to reject H0)' % (p, alpha))
