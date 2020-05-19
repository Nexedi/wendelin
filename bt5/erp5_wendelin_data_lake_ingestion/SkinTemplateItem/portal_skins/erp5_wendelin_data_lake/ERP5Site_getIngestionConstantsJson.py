import json
portal = context.getPortalObject()
dict = {'invalid_suffix':portal.DataLake_getIngestionReferenceDictionary()['invalid_suffix'],
        'split_end_suffix':portal.DataLake_getIngestionReferenceDictionary()['split_end_suffix'],
        'single_end_suffix':portal.DataLake_getIngestionReferenceDictionary()['single_end_suffix'],
        'split_first_suffix':portal.DataLake_getIngestionReferenceDictionary()['split_first_suffix'],
        'none_extension':portal.DataLake_getIngestionReferenceDictionary()['none_extension'],
        'reference_separator':portal.DataLake_getIngestionReferenceDictionary()['reference_separator'],
        'complex_files_extensions':portal.DataLake_getIngestionReferenceDictionary()['complex_files_extensions'],
        'reference_length':portal.DataLake_getIngestionReferenceDictionary()['reference_length'],
        'invalid_chars':portal.DataLake_getIngestionReferenceDictionary()['invalid_chars'],
        }
return json.dumps(dict)
