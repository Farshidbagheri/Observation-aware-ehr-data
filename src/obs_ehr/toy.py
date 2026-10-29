"""Known-truth *synthetic* potential outcomes: unit tests only, NOT clinical sepsis data."""
from __future__ import annotations
import random

def generate_toy(n:int=1000,seed:int=2026)->list[dict]:
    rng=random.Random(seed)
    records=[]
    for i in range(n):
        x=rng.uniform(-2.0,2.0)                  # hypothetical patient severity
        u=rng.gauss(0,0.2)                      # shared intrinsic outcome variability
        risk_early=min(.99,max(.01,.3+.14*x+u*.10))
        risk_delayed=min(.99,max(.01,risk_early+.09+.03*x))
        # Continuous potential outcomes are *risk probabilities*; never actual observed mortalities.
        p_early=risk_early;p_delayed=risk_delayed
        observed_delay=1 if rng.random() < 1/(1+2.71828**(-x)) else 0
        records.append({"id":i,"severity":round(x,5),"observed_delay":observed_delay,
                        "observed_risk":p_delayed if observed_delay else p_early,
                        "potential_risk_early":p_early,"potential_risk_delayed":p_delayed,
                        "true_delay_effect":p_delayed-p_early,"synthetic_ground_truth":True})
    return records
