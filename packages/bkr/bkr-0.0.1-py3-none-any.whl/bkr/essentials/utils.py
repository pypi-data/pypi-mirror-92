def map_range(val, low1, high1, low2, high2):
	return round(low2 + (high2 - low2) * (val - low1) / (high1 - low1), 3)