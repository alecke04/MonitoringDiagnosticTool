import numpy as np
from scipy import stats

def analyse(data : list[float]) -> list[float]:
    # Convert input to a numpy array
    data = np.array(data)

    # Basic statistics
    mean = np.mean(data)
    median = np.median(data)
    std_dev = np.std(data)

    # 90% Confidence Interval
    confidence = 0.90
    sem = stats.sem(data)

    ci_low, ci_high = stats.t.interval(confidence, len(data) - 1, loc=mean, scale=sem)

    return [ mean.item(), median.item(), std_dev.item(), ci_low.item(),  ci_high.item() ]