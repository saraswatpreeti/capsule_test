import pandas as pd
import numpy as np
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

test_file=pd.read_csv('./debugoutput_final.tsv', sep='\t', index_col=False, names=["Utterance", "count", "GT","hypothesis"], header=0)
#print(test_file.head())
#test_file.set_axis(['utterance', 'count', 'GT', 'hypothesis'], axis=1, inplace=True)
#print(test_file.columns)
#print(test_file.head())
#define conditions
test_file=test_file[test_file['GT'].notna()]
test_file['hypothesis'].fillna('unhandled', inplace=True)
test_file=test_file.loc[test_file['count']>10]
conditions = [test_file['GT'] == test_file['hypothesis']]
#define choices
choices = ['Passed']

#create new column in DataFrame that displays results of comparisons
test_file['diff'] = np.select(conditions, choices, default='Failed')

passed=test_file.loc[test_file['diff']=='Passed']
passed.to_csv('./passed.tsv', sep='\t', encoding='utf-8', index=False)
failed=test_file.loc[test_file['diff']=='Failed']
failed.to_csv('./failed.tsv', sep='\t', encoding='utf-8', index=False)

#calculate frequency_weighted accuracy:
test_file['Weight'] = test_file['count']/test_file['count'].sum()
test_file['accuracy'] = 1.0*(test_file["GT"] == test_file["hypothesis"])
test_file['WeightedAccuracy'] = test_file['Weight'] * test_file['accuracy']
data=[test_file.shape[0],passed.shape[0],failed.shape[0], (test_file['accuracy'].mean())*100, (1-test_file['accuracy'].mean())*100,(test_file['WeightedAccuracy'].sum())*100,(1-test_file['WeightedAccuracy'].sum())*100]
Stats_cols=['Total_test_cases','Passed','Failed', 'uniform_weighted_accuracy', 'uniform_weighted_error', 'Frequency_weighted_accuracy','Frequency_weighted_error']
df = pd.DataFrame(index=Stats_cols)
df['summary_statistics']=data
df.to_csv('./Summary_stats.tsv', sep='\t', encoding='utf-8', header=None)
df.to_html('./Summary_stats.html')
