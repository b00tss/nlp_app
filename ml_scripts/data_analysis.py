import pandas as pd
from pandas_profiling import ProfileReport

raw_data = pd.read_csv("data/data.csv", names=["msg"], header=None, ) #nrows=90)
prof = ProfileReport(raw_data, title="Profile Report",  minimal=True)
prof.to_file(output_file='outputprofile.html')
