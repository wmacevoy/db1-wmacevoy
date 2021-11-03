import csvimport
import config
import sample
import location
import collector

def test_csvimport_row():
    db=config.DB_TEST_NAME
    sample.drop_sample_table(db)
    sample.create_sample_table(db)
    location.drop_location_table(db)
    location.create_location_table(db)
    collector.drop_collector_table(db)
    collector.create_collector_table(db)
    location.insert_location({'name':'uc', 'latitude': 3, 'longitude': 17 },db)
    (sampleId, collectorId, locationId) = csvimport.createRecord({
        'timestamp': '2023-11-02T16:16:14',
        'collector': 'testme', 
        'location': 'uc', 
        'covidPPM': 32.3}
        ,db)
    if sampleId != 1 or collectorId != 1 or locationId != 1:
        raise ValueError('missing rows after insert.')

