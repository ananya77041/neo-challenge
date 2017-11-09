from etl import get_latest_date, write_df_to_db
import os, json, datetime
import pandas as pd
from sqlalchemy import create_engine
from nose.tools import assert_equal

class TestDbFunctions(object):
    def setup(self):
        DB_HOST = os.environ['DB_HOST']
        DB_PORT = os.environ['DB_PORT']
        DB_USER = os.environ['DB_USER']
        DB_DB = 'test'
        DB_PASS = os.environ['DB_PASS']
        self.engine = create_engine('postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
                       DB_USER,
                       DB_PASS,
                       DB_HOST,
                       DB_PORT,
                       DB_DB))
        con = self.engine.connect()
        con.execute('CREATE SCHEMA IF NOT EXISTS nasa')
        con.execute('''
                    CREATE TABLE IF NOT EXISTS nasa.neo(
                        neo_reference_id BIGINT NOT NULL,
                        close_approach_date DATE,
                        name VARCHAR,
                        is_potentially_hazardous BOOLEAN,
                        miss_distance_km DOUBLE PRECISION,
                        PRIMARY KEY(neo_reference_id, close_approach_date)
                    );
                    ''')
        con.close()
        neo = {"neo_reference_id": [000000], 
               "close_approach_date": ['2017-01-01'],
               "name": ['blah'],
               "is_potentially_hazardous": [True],
               "miss_distance_km": [100000]}
        self.df = pd.DataFrame.from_dict(neo)

    def teardown(self):
        con = self.engine.connect()
        con.execute("DELETE FROM nasa.neo WHERE true")
        con.close()

    def test_get_latest_date_no_records(self):
        assert_equal(get_latest_date(self.engine), None)

    def test_get_latest_date_with_records(self):
        con = self.engine.connect()
        con.execute("INSERT INTO nasa.neo VALUES (000000, '2017-01-01', 'blah', True, 100000)")
        con.close()
        assert_equal(get_latest_date(self.engine), datetime.date(2017,1,1))

    def test_write_to_db(self):
        write_df_to_db(self.df, self.engine)
        con = self.engine.connect()
        result = con.execute('select count(*) from nasa.neo')
        con.close()
        assert_equal(result.first()[0], 1)
        
