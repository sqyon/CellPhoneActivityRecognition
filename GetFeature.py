import numpy as np
import tsfresh
import pandas as pd
import math

def running_mean(l, N=4):
	sum = 0
	result = [0 for x in l]
	for i in range(0, N):
		sum = sum + l[i]
		result[i] = sum / (i + 1)
	for i in range(N, len(l)):
		sum = sum - l[i - N] + l[i]
		result[i] = sum / N
	return result


def getfeature(avqueue, ahqueue):
	fea = []
	avrange = tsfresh.feature_extraction.feature_calculators.maximum(pd.Series(avqueue)) - tsfresh.feature_extraction.feature_calculators.minimum(pd.Series(avqueue))
	ahrange = tsfresh.feature_extraction.feature_calculators.maximum(pd.Series(ahqueue)) - tsfresh.feature_extraction.feature_calculators.minimum(pd.Series(ahqueue))
	fea.append(math.fabs(avrange))
	fea.append(math.fabs(ahrange))
	fea.append(tsfresh.feature_extraction.feature_calculators.mean_abs_change(pd.Series(avqueue)))
	fea.append(tsfresh.feature_extraction.feature_calculators.mean_abs_change(pd.Series(ahqueue)))
	fea.append(tsfresh.feature_extraction.feature_calculators.standard_deviation(pd.Series(avqueue)))
	fea.append(tsfresh.feature_extraction.feature_calculators.standard_deviation(pd.Series(ahqueue)))
	fea.append(tsfresh.feature_extraction.feature_calculators.abs_energy(pd.Series(avqueue)))
	fea.append(tsfresh.feature_extraction.feature_calculators.abs_energy(pd.Series(ahqueue)))
	fea.append(tsfresh.feature_extraction.feature_calculators.cid_ce(pd.Series(avqueue), normalize=False))
	fea.append(tsfresh.feature_extraction.feature_calculators.cid_ce(pd.Series(ahqueue), normalize=False))
	fftav = list(tsfresh.feature_extraction.feature_calculators.fft_aggregated(pd.Series(avqueue),
	                                                                           param=[{'aggtype': 'centroid'},
	                                                                                  {'aggtype': 'variance'},
	                                                                                  {'aggtype': 'skew'},
	                                                                                  {'aggtype': 'kurtosis'}]))
	fftah = list(tsfresh.feature_extraction.feature_calculators.fft_aggregated(pd.Series(ahqueue),
	                                                                           param=[{'aggtype': 'centroid'},
	                                                                                  {'aggtype': 'variance'},
	                                                                                  {'aggtype': 'skew'},
	                                                                                  {'aggtype': 'kurtosis'}]))
	fea.append(fftav[0][1])
	fea.append(fftah[0][1])
	fea.append(fftav[1][1])
	fea.append(fftah[1][1])
	fea.append(fftav[2][1])
	fea.append(fftah[2][1])
	fea.append(fftav[3][1])
	fea.append(fftah[3][1])
	fea.append(tsfresh.feature_extraction.feature_calculators.variance(pd.Series(avqueue)))
	fea.append(tsfresh.feature_extraction.feature_calculators.variance(pd.Series(ahqueue)))
	return fea
