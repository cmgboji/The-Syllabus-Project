import extraction_script
import pandas as pd

depts = ['GOV', 'LIN', 'E', 'SOC', 'ANT', 'RHE', 'HIS',
         'PSY', 'GEO', 'LAH', 'PHL', 'ECO']
# Fall = 9, Spring = 2, Summer = 6
data = extraction_script.main(depts, '2025', '9')
print(data)

cola_12 = data.to_csv('cola_12.csv', index=False)