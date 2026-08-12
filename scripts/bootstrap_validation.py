import pandas as pd
import matplotlib.pyplot as plt

def compare_zero_coupon(quantlib_zero_coupon : pd.DataFrame, zero_coupon : pd.DataFrame) -> pd.DataFrame:
    """Compare the from-scratch and QuantLib zero-coupon curves.

    Args:
        quantlib_zero_coupon: DataFrame containing the QuantLib results.
        zero_coupon: DataFrame containing the from-scratch bootstrap results.

    Returns:
        DataFrame containing the comparison and differences between both curves.
    """

    quantlib_zero_coupon["Maturity"] = pd.to_datetime(quantlib_zero_coupon["Maturity"])
    zero_coupon["Maturity"] = pd.to_datetime(zero_coupon["Maturity"])

    comparison = pd.merge(quantlib_zero_coupon, zero_coupon, on=["Bond", "Maturity"], how="inner")

    comparison["DiscountFactor_Diff"] = (comparison["DiscountFactor"] - comparison["QLDiscountFactor"])
    comparison["ZeroCouponRate_Diff"] = (comparison["ZeroCouponRate"] - comparison["QLZeroCouponRate"])
    comparison["ZeroCouponRatePct_Diff"] = ((comparison["ZeroCouponRatePct"] - comparison["QLZeroCouponRatePct"])) * 100

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        comparison["Maturity"],
        comparison["QLDiscountFactor"],
        marker="o",
        label="QuantLib discount factor"
    )

    ax.plot(
        comparison["Maturity"],
        comparison["DiscountFactor"],
        marker="x",
        linestyle="--",
        label="Discount factor"
    )

    ax.set_title("Comparison of discount factors")
    ax.set_xlabel("Maturity")
    ax.set_ylabel("Discount Factor")

    ax.grid(True, alpha=0.3)
    ax.legend()

    fig.autofmt_xdate()
    plt.tight_layout()
    plt.savefig("results/comparison_of_discountfactor.png", dpi=300, bbox_inches="tight")
    plt.show()

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        comparison["Maturity"],
        comparison["QLZeroCouponRatePct"],
        marker="o",
        label="QuantLib zero coupon rate pct"
    )

    ax.plot(
        comparison["Maturity"],
        comparison["ZeroCouponRatePct"],
        marker="x",
        linestyle="--",
        label="Zero coupon rate pct"
    )

    ax.set_title("Comparison of zero coupon rate")
    ax.set_xlabel("Maturity")
    ax.set_ylabel("Zero coupon rate (%)")

    ax.grid(True, alpha=0.3)
    ax.legend()

    fig.autofmt_xdate()
    plt.tight_layout()
    plt.savefig("results/zero_coupon_rate_curve.png", dpi=300, bbox_inches="tight")
    plt.show()

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.axhline(
        y=0,
        linestyle="--",
        linewidth=1
    )

    ax.plot(
        comparison["Maturity"],
        comparison["ZeroCouponRatePct_Diff"],
        marker="o"
    )

    ax.set_title(
        "Spread between zero coupon rate "
        "(Zero coupon rate - QuantLib zero coupon rate)"
    )

    ax.set_xlabel("Maturity")
    ax.set_ylabel("Spread (basis points)")

    ax.grid(True, alpha=0.3)

    fig.autofmt_xdate()
    plt.tight_layout()
    plt.savefig("results/spread_btw_zero_coupon_rate.png", dpi=300, bbox_inches="tight")
    plt.show()

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.axhline(
        y=0,
        linestyle="--",
        linewidth=1
    )

    ax.plot(
        comparison["Maturity"],
        comparison["DiscountFactor_Diff"],
        marker="o"
    )

    ax.set_title(
        "Spread between discount factor"
        "(Discount factor - QuantLib discount factor)"
    )

    ax.set_xlabel("Maturity")
    ax.set_ylabel("Difference in discount factor")

    ax.grid(True, alpha=0.3)

    fig.autofmt_xdate()
    plt.tight_layout()
    plt.savefig("results/spread_btw_discount_factor.png", dpi=300, bbox_inches="tight")
    plt.show()

    return comparison