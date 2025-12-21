import extraction_script
import pandas as pd

# depts = ['GOV', 'LIN', 'E', 'SOC', 'ANT', 'RHE', 'HIS',
#          'PSY', 'GEO', 'LAH', 'PHL', 'ECO']
# # Fall = 9, Spring = 2, Summer = 6
# data = extraction_script.main(depts, '2025', '9')
# print(data)

# cola_12 = data.to_csv('cola_12.csv', index=False)

depts = {'Architecture': ['ARC', 'ARI', 'CRP', 'LAR', 'U D', 'UDN'],
         'Business': ['ACC', 'B A', 'BAX', 'D S', 'FIN', 'HCT', 'I B', 'LEB', 'MAN', 'MIS', 'MKT', 'O M', 'R E', 'R M', 'STC'],
         'Civic Leadership': ['CIV'],
         'Communication': ['ADV', 'CLD', 'CMS', 'COM', 'CSD', 'J', 'P L', 'P R', 'RTF', 'SLH'],
         'Education': ['ALD', 'EDA', 'EDC', 'EDP', 'EDU', 'ELP', 'FLE', 'HED', 'KIN', 'PED', 'SED', 'SME'],
         'Engineering': ['ARE', 'ASE', 'BME', 'C E', 'CHE', 'COE', 'E E', 'E M', 'E S', 'ECE', 
                         'ENM', 'EVE', 'G E', 'M E', 'MSE',  'NE', 'ORI', 'PGE', 'SSE'],
         'Fine Arts': ['AED', 'AET', 'ARH', 'ART', 'BSN', 'CLA', 'CON', 'D B', 'DES', 'DRS', 
                       'ENS', 'EUP', 'F A', 'F H', 'FLU', 'GUI', 'HAR', 'ITD','MRT', 'MBU', 'MUS', 'OBE', 
                       'OPR', 'ORG', 'PER', 'PIA', 'PRF', 'REC', 'SAX', 'T D', 'TBA', 'TRO', 
                       'TRU', 'V C', 'VAS', 'VIA', 'VIB', 'VIO', 'VOI'],
         'Geosciences': ['EEE', 'EER', 'EVS', 'GEO'],
         'Information': ['I', 'INF', 'ISP'],
         'Liberal Arts': ['AAS', 'AAR', 'AFR', 'AFS', 'AHC', 'ANT', 'AMS', 'ANS', 'ARA', 'ARY', 'ASL', 'BEN', 
                          'C L', 'CGS', 'CHI', 'CLS', 'CRW', 'CTI', 'CZ', 'DAN', 'DCH', 'E', 'ECO', 'ESL', 'EUS', 
                          'F C', 'FNH', 'FR', 'GER', 'GK', 'GOV', 'GRC', 'GRG', 'GSD', 'H S', 
                          'HDO', 'HEB', 'HIN', 'HIS', 'HMN', 'IRG', 'ITC', 'ITL', 'ILA', 'ISL', 'J S', 
                          'JPN', 'KOR', 'L A', 'LAH', 'LAL', 'LAS', 'LAT', 'LIN', 'LTC', 'MAL', 'MAS', 
                          'MDV', 'MEL', 'MES', 'M S', 'N S', 'NOR', 'PHL', 'POL', 'POR', 'PPE', 'PRC', 
                          'PRS', 'PSH', 'PSY', 'R S', 'REE', 'RHE', 'ROM', 'RUS', 'RIM', 'S C', 
                          'S S', 'SAL', 'SAN', 'SCA', 'SEL', 'SLA', 'SOC', 'SPC', 'SPN', 'SUS', 
                          'STS', 'SWA', 'SWE', 'T C', 'TAM', 'TEL', 'TUR', 'UGS', 'URB', 'URD', 'UTL', 'UKR', 
                          'VTN', 'WCV', 'WGS', 'WRT', 'YID', 'YOR'],
         'Natural Sciences': ['A I', 'AST', 'BCH', 'BIO', 'C S', 'CAM', 'CH', 'CSE', 'H E', 'HDF', 
                              'INB', 'M', 'ACF', 'MBS', 'MED', 'MLS', 'MNS', 'MOL', 'MST', 'NEU', 'NSC', 
                              'NTR', 'P S', 'PBH', 'PHY', 'SCI', 'SDS', 'SSB', 'SSC', 'STA', 'STM', 
                              'TXA', 'UTS'],
         'Nursing': ['N'],
         'Pharmacy': ['PHM', 'PHR', 'PGS'],
         'Public Affairs': ['P A'],
         'Social Work': ['S W', 'PSF']}

for col, dept in depts.items():
    print('Processing:', col)
    for yr in ['9', '2', '6']:
        if yr == '9':
            fall_data = extraction_script.main(dept, '2024', '9')
        elif yr == '2':
            spring_data = extraction_script.main(dept, '2025', '2')
        else:
            summer_data = extraction_script.main(dept, '2025', '6')
    data = pd.concat([fall_data, spring_data, summer_data])
    data['School'] = col
    data.to_csv(f'{col} Syllabi.csv', index=False)
    