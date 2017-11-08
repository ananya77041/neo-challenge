import json, requests
import argparse
from sqlalchemy import create_engine
import pandas as pd
import datetime
from date_utilities import forward_date_range
import sys, logging

with open('./db_config.json', 'rb') as db_config_file:
    DB_CONFIG = json.loads(db_config_file.read())

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

url = 'https://api.nasa.gov/neo/rest/v1/feed'

'''
Returns date of latest record, or None if no records in the DB.
'''
def get_latest_date(engine):
    conn = engine.connect()
    result = conn.execute('select max(close_approach_date) from nasa.neo')
    val = result.first()[0]
    conn.close()
    if val:
        latest_date = val
    else:
        latest_date = None
    return latest_date

'''
Makes a single request to the NASA NEO API given start and end dates
and an API key.
'''
def make_neo_request(start_date, end_date, api_key):
    params = {
        'start_date': start_date,
        'end_date': end_date,
        'api_key': api_key
    }
    try:
        resp = requests.get(url=url, params=params)
    except Exception as e:
        logging.error(e)
        logging.error("Could not make API request for {} to {} using key {}!".format(
                      start_date, end_date, api_key))
    data = json.loads(resp.text)
    return data

'''
Converts JSON data into a Pandas DataFrame.
'''
def parse_raw_data_to_df(json_data):
    neos = {}
    for date in json_data['near_earth_objects']:
        for neo in json_data['near_earth_objects'][date]:
            neos[neo['neo_reference_id']] = {
                'close_approach_date': neo['close_approach_data'][0]['close_approach_date'],
                'name': neo['name'],
                'is_potentially_hazardous': neo['is_potentially_hazardous_asteroid'],
                'miss_distance_km': neo['close_approach_data'][0]['miss_distance']['kilometers']
            }
    df = pd.DataFrame.from_dict(neos).T
    df.reset_index(inplace=True)
    df.columns = ['neo_reference_id', 
                  'close_approach_date',
                  'is_potentially_hazardous',
                  'miss_distance_km',
                  'name']
    return df

'''
Writes DataFrame to DB.
'''
def write_df_to_db(df, engine):
    df.to_sql(name=DB_CONFIG['TABLE'], con=engine, if_exists='append', schema='nasa', index=False)

'''
Calculates date ranges to query the API, retrieves records, and writes to DB.
'''
def run(start_date, db_user, db_password, api_key):
    engine = create_engine('postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
                       db_user,
                       db_password,
                       DB_CONFIG['HOST'],
                       DB_CONFIG['PORT'],
                       DB_CONFIG['DB']))

    latest_date = get_latest_date(engine)
    if latest_date:
        start_date = latest_date.strftime('%Y-%m-%d')
    if start_date:
        end_date = datetime.datetime.today().strftime('%Y-%m-%d')
        if start_date != end_date:
            date_ranges = forward_date_range(start_date, end_date, 7)
            for date_range in date_ranges:
                try:
                    logging.info('Making request for {} to {}...'.format(date_range[0], date_range[1]))
                    data = make_neo_request(date_range[0], date_range[1], api_key)
                    df = parse_raw_data_to_df(data)
                    write_df_to_db(df, engine)
                    logging.info('Data for {} to {} written to DB!'.format(date_range[0], date_range[1]))
                except Exception as e:
                    logging.error(e)
                    logging.error('Data for {} to {} could not be retrieved!'.format(date_range[0], date_range[1]))
                    continue
            return 0
    else:
        sys.exit('Please provide a start date as there are currently no records.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--start-date", "-s",
                        type=str,
                        required=False,
                        help="Date from which to start retrieving data")
    parser.add_argument("--db-user", "-u",
                        type=str,
                        required=True,
                        help='User for database')
    parser.add_argument("--db-password", "-p",
                        type=str,
                        required=True,
                        help='Password for database')
    parser.add_argument("--api-key", "-k",
                        type=str,
                        required=True,
                        help='NASA API Key')
    args = parser.parse_args()
    run(args.start_date, args.db_user, args.db_password, args.api_key)
