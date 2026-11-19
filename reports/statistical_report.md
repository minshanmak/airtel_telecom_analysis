# Airtel Telecom Analytics – Statistical Report

Significance level: α = 0.05. If p < 0.05, reject H₀; otherwise, fail to reject H₀.

## 1. Pre-offer daily data usage: Group A vs Group B

**Claim:** The two groups used the same amount of data before the offer.  
**H₀:** Both groups have the same true average daily data before May.  
**H₁:** The two averages differ.

F = 1.1108, p = 3.673e-08 (variances differ).  
Z = 0.5191, p = 0.6037.  
**Decision:** Fail to reject H₀.  
**Conclusion:** There is insufficient evidence that the groups differed in average daily data usage before the offer. The groups are considered balanced on this pre-offer measure.

## 2. A/B group smartphone-user proportion

**Claim:** Groups A and B have different proportions of smartphone users.  
**H₀:** Both groups have the same true smartphone-user proportion.  
**H₁:** The two proportions differ.

| ab_group | n | smart | prepaid |
|---|---:|---:|---:|
| A | 10996 | 9417 | 8575 |
| B | 11004 | 9554 | 8574 |

Z = 2.5457, p = 0.01091.  
**Decision:** Reject H₀.  
**Conclusion:** Smartphone-user proportions differ significantly between groups A and B.

## 3. A/B group prepaid proportion

**Claim:** Groups A and B have different proportions of prepaid subscribers.  
**H₀:** Both groups have the same true prepaid proportion.  
**H₁:** The two proportions differ.

Use the SQL output in Question 2.

Z = -0.1177, p = 0.9063.  
**Decision:** Fail to reject H₀.  
**Conclusion:** There is no statistically significant difference in prepaid proportions between groups A and B.

## 4. Pre-offer recharge revenue: Group A vs Group B

**Claim:** Both groups paid the same on average before the offer.  
**H₀:** Both groups have the same true average recharge revenue.  
**H₁:** The two average revenues differ.

F = 1.0512, p = 0.008866 (variances differ).  
Z = 1.3490, p = 0.1773.  
**Decision:** Fail to reject H₀.  
**Conclusion:** There is insufficient evidence of a difference in average pre-offer revenue between the groups.

## 5. A/B group customer-characteristic variance checks

**Claim:** Groups A and B have similar customer characteristics.  
**H₀:** The two groups have equal variances for each characteristic.  
**H₁:** The variances differ.

| Variable | F | P-value | Result |
|---|---:|---:|---|
| stated_arpu | 1.0668 | 0.0006932 | Variances differ |
| tenure_days | 1.0244 | 0.2061 | No significant difference |
| complaint_count | 1.0240 | 0.2128 | No significant difference |

**Conclusion:** Only stated ARPU shows a statistically significant variance difference between the two groups.

## 6. Daily data usage after the offer: Group A vs Group B

**Claim:** The offer raised daily data usage.  
**H₀:** Both groups have the same true average daily data after May.  
**H₁:** Group B's average is higher.

F = 0.6197, p = 8.402e-116 (variances differ).  
Z = -19.4496, p = 2.936e-84 (A minus B).  
**Decision:** Reject H₀.  
**Conclusion:** Group B has significantly higher average daily data usage after the offer, supporting the claim.

## 7. Churn after the offer: Group A vs Group B

**Claim:** The offer reduced churn.  
**H₀:** Both groups have the same true churn rate.  
**H₁:** Group B's churn rate is lower.
Z = 0.7937, p = 0.4274 (two-tailed).  
**Decision:** Fail to reject H₀ using the notebook's two-tailed test.  
**Conclusion:** This result does not show a statistically significant churn-rate difference. The directional claim requires a one-tailed test.

## 8. Revenue after the offer: Group A vs Group B

**Claim:** The offer raised revenue.  
**H₀:** Both groups paid the same amount on average.  
**H₁:** Group B paid more.


F = 1.0312, p = 0.1068.  
Z = 0.5927, p = 0.5534.  
**Decision:** Fail to reject H₀.  
**Conclusion:** There is insufficient evidence that group B paid more on average after the offer.

## 9. Prepaid vs Postpaid churn

**Claim:** Prepaid and postpaid subscribers churn at different rates.  
**H₀:** Both have the same true churn rate.  
**H₁:** The two rates differ.

| grp | n | k |
|---|---:|---:|
| Postpaid | 4851 | 785 |
| Prepaid | 17149 | 4441 |

Z = 14.0364, p = 9.333e-45.  
**Decision:** Reject H₀.  
**Conclusion:** Prepaid and postpaid subscribers have significantly different churn rates. Prepaid churn is higher.

## 10. Complaint status vs churn

**Claim:** Subscribers with an open ticket churn at a different rate from those who never complained.  
**H₀:** Both have the same true churn rate.  
**H₁:** The two rates differ.

| grp | n | k |
|---|---:|---:|
| all closed | 8689 | 2064 |
| never | 6631 | 1328 |
| open | 6680 | 1834 |

Z = 10.0684, p = 7.623e-24.  
**Decision:** Reject H₀.  
**Conclusion:** Open-ticket subscribers have a significantly different churn rate from subscribers who never complained.

## 11. Year-0 vs Year-3 subscriber churn

**Claim:** Year-0 and year-3 subscribers churn at different rates.  
**H₀:** They share one true churn rate.  
**H₁:** They do not.

| grp | n | k |
|---|---:|---:|
| 0 | 4610 | 1328 |
| 3 | 3374 | 632 |

Z = 10.3330, p = 4.995e-25.  
**Decision:** Reject H₀.  
**Conclusion:** Year-0 and year-3 subscribers have significantly different churn rates. Year-0 churn is higher.

## 12. Himachal Pradesh vs Punjab churn

**Claim:** Himachal Pradesh and Punjab subscribers churn at different rates.  
**H₀:** Both have the same true churn rate.  
**H₁:** The two rates differ.


| grp | n | k |
|---|---:|---:|
| Himachal Pradesh | 1247 | 417 |
| Punjab | 558 | 77 |


Z ≈ 7.884, p < 0.0001.  
**Decision:** Reject H₀.  
**Conclusion:** Churn rates differ significantly. Himachal Pradesh has the higher churn rate.

**Correction:** The notebook's original test arguments `z_prop2(408,1412,356,1284)` do not match the SQL output above. The test here uses the SQL counts.

## 13. Smartphone vs Feature Phone churn

**Claim:** Smartphone and feature-phone users churn at different rates.  
**H₀:** Both have the same true churn rate.  
**H₁:** The two rates differ.


| grp | n | k |
|---|---:|---:|
| Feature Phone | 3029 | 719 |
| Smartphone | 18971 | 4507 |


Z = 0.0241, p = 0.9807.  
**Decision:** Fail to reject H₀.  
**Conclusion:** There is no statistically significant difference in churn rates between smartphone and feature-phone users.

## 14. Gender vs average daily data usage

**Claim:** Male and female subscribers use different amounts of daily data.  
**H₀:** Both groups have the same true average daily data usage.  
**H₁:** The two averages differ.

F = 0.9315, p = 6.262e-177 (variances differ).  
Z = -7.2519, p = 4.109e-13.  
**Decision:** Reject H₀.  
**Conclusion:** Average daily data usage differs significantly by gender. The female group has the higher sample average.

## 15. Feature Phone vs Smartphone average daily data usage

**Claim:** Feature-phone and smartphone users have different average daily data usage.  
**H₀:** Both groups have the same true average daily data usage.  
**H₁:** The two averages differ.
F = 0.0268, p approximately 0 (variances differ).  
Z = -119.2400, p approximately 0.  
**Decision:** Reject H₀.  
**Conclusion:** Average daily data usage differs significantly between device types. Smartphone users have the higher sample average.
