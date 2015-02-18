# Matt Cotter's Carleton College Senior Economics Project

# Set Up
- install all requirements (`pip install -r requirements.txt`)
- download the PSID data (see `/psid/fam1984/.gitignore` and `/psid/fam2011er/.gitignore`)
- start MongoDB (`mongod`)
- process the ncs data:
    + `python bls/ncs_data_clean.py`
- process the psid data:
    + `python psid/make_csvs.py`
- run all analysis:
    + `python full_1984.py`
    + `python full_2011.py`
- to clean up all results `./clean-results`

#Runnable code (check for must run as main):

## ATS
- [ ] `dest_counter.py.py`

## BLS
- [x] `ncs_data_clean.py`

## PSID
- [ ] `industry_codes.py`
- [x] `make_csvs.py`
- [ ] `vars_to_cols.py`
- [ ] `vars_to_csv.py`

## top level
- [x] `full_1984.py`
- [x] `full_2011.py`
- [ ] `industry_to_days.py`
