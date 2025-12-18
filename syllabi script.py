import extraction_script

depts = ['GOV', 'LIN', 'ENG', 'SOC', 'ANT', 'RHE', 'HIS',
         'PSY', 'GEO', 'LAH', 'PHL', 'ECO']
data = extraction_script.main(depts)
print(data)