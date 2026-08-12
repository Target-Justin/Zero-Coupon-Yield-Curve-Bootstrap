import pandas as pd
from scripts.cashflow import generate_cashflows
from scripts.dirty_price import generate_dirty_prices
from scripts.bootstrap import generate_discount_factors
from scripts.zero_rates import generate_zero_coupon_curve
from scripts.quantlib.bootstrap_quantlib import generate_quantlib_zero_coupon_curve
from scripts.bootstrap_validation import compare_zero_coupon

bonds_df = pd.read_csv("data/raw/dataset.csv")

bonds_df["Maturity"] = pd.to_datetime(bonds_df["Maturity"])
bonds_df["EvaluationDate"] = pd.to_datetime(bonds_df["EvaluationDate"])
bonds_df["AccrualStartDate"] = pd.to_datetime(bonds_df["AccrualStartDate"])
bonds_df["IssueDate"] = pd.to_datetime(bonds_df["IssueDate"])

cashflow = generate_cashflows(bonds_df)
cashflow.to_csv("data/processed/cashflow.csv", index = False)

dirty_price = generate_dirty_prices(bonds_df)
dirty_price.to_csv("data/processed/dirty_price.csv", index = False)

discount_factor = generate_discount_factors(cashflow, dirty_price)
discount_factor.to_csv("data/processed/discount_factor.csv", index = False)

zero_rate = generate_zero_coupon_curve(discount_factor, bonds_df.loc[0, "EvaluationDate"])
zero_rate.to_csv("results/zero_rate.csv", index = False)

quantlib_zero_rate = generate_quantlib_zero_coupon_curve(bonds_df)
quantlib_zero_rate.to_csv("results/quantlib/quantlib_zero_rate.csv", index = False)

comparison_with_quantlib_bootstrap = compare_zero_coupon(quantlib_zero_rate, zero_rate)
comparison_with_quantlib_bootstrap.to_csv("results/comparison_with_quantlib_bootstrap.csv", index = False)