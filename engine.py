def suitability_score(crop, farm):
    score = 100

    if not crop["soil_ph_min"] <= farm["ph"] <= crop["soil_ph_max"]:
        score -= 25

    water_rank = {
        "Low": 1,
        "Medium": 2,
        "High": 3
    }

    if water_rank[crop["water_need"]] > water_rank[farm["water"]]:
        score -= 30

    total_cost = crop["cost_per_acre"] * farm["area"]

    if total_cost > farm["budget"]:
        score -= 40

    return max(score, 0)


def evaluate_crop(crop, farm):
    area = farm["area"]

    suitability = suitability_score(crop, farm)

    yield_adjustment = suitability / 100

    expected_yield = (
        crop["yield_per_acre"]
        * area
        * yield_adjustment
    )

    expected_revenue = (
        expected_yield
        * crop["price_per_kg"]
    )

    production_cost = (
        crop["cost_per_acre"]
        * area
    )

    nominal_profit = expected_revenue - production_cost

    risk_penalty = max(nominal_profit, 0) * crop["risk"]

    risk_adjusted_profit = nominal_profit - risk_penalty

    return {
        "crop": crop["crop"],
        "yield": expected_yield,
        "revenue": expected_revenue,
        "cost": production_cost,
        "profit": nominal_profit,
        "risk_adjusted_profit": risk_adjusted_profit,
        "score": suitability
    }


def explain_crop(crop, farm):
    reasons = []

    if crop["water_need"] == "Low":
        reasons.append("Requires relatively low water.")

    if crop["cost_per_acre"] * farm["area"] <= farm["budget"]:
        reasons.append("Fits within the available budget.")

    if crop["soil_ph_min"] <= farm["ph"] <= crop["soil_ph_max"]:
        reasons.append("Your soil pH falls within the suitable range.")

    if crop["risk"] < 0.15:
        reasons.append("Has comparatively lower modeled production risk.")

    return reasons
