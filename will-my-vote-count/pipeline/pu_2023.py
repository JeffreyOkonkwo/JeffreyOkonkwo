"""Summarise the CCIJ 2023 presidential polling-unit document audit by state."""
import pandas as pd, sys
SRC = './source/nigeria-2023-election/'
OUT = './data/'
CAT = {
 'exist and not blur': 'Readable result sheet',
 'not uploaded': 'Never uploaded',
 'blurred': 'Unreadable upload', 'blur_crowdsourcing': 'Unreadable upload', 'blur_crowdsourcing2': 'Unreadable upload',
 'wrong_election': 'Wrong document', 'collation_paper': 'Wrong document', 'irrelevant_picture': 'Wrong document',
 'selfie': 'Wrong document', 'blank_with_handwritten_text': 'Wrong document',
 'ec40g': 'Cancelled or no election', 'blank_cancellation': 'Cancelled or no election',
}
pu = pd.read_csv(SRC + 'AllPollingUnitsInfo.csv', usecols=['polling_unit_code','status','state_name','lga_name','lat','lng'])
pu['category'] = pu.status.map(CAT)
assert pu.category.notna().all(), pu[pu.category.isna()].status.unique()
pu['state_name'] = pu.state_name.str.title().replace({'Fct': 'FCT', 'Akwa Ibom': 'Akwa Ibom', 'Cross River': 'Cross River'})
sig = pd.read_csv(SRC + 'stamp_sig_missing.csv')
sig['missing_auth'] = 1
pu = pu.merge(sig[['polling_unit_code','missing_auth']].drop_duplicates('polling_unit_code'), on='polling_unit_code', how='left')
pu['missing_auth'] = pu.missing_auth.fillna(0).astype(int)
pu[['polling_unit_code','state_name','lga_name','status','category','missing_auth','lat','lng']].to_csv(OUT + 'pu_2023_documents.csv', index=False)
t = pu.pivot_table(index='state_name', columns='category', values='polling_unit_code', aggfunc='count', fill_value=0)
t['Polling units'] = t.sum(axis=1)
t['Missing signature or stamp'] = pu.groupby('state_name').missing_auth.sum()
t['Problem share'] = (t['Never uploaded'] + t['Unreadable upload'] + t['Wrong document']) / t['Polling units']
t = t.sort_values('Problem share', ascending=False)
t.to_csv(OUT + 'pu_2023_by_state.csv')
tot = pu.category.value_counts()
print(tot, '\nTotal', len(pu), '\nMissing auth', pu.missing_auth.sum())
print('Problem share national', round((tot['Never uploaded']+tot['Unreadable upload']+tot['Wrong document'])/len(pu),4))
print(t[['Polling units','Never uploaded','Unreadable upload','Wrong document','Problem share']].round(3).to_string())
