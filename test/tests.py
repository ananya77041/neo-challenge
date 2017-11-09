from etl import parse_raw_data_to_df, make_neo_request
import json
from nose.tools import assert_equal

class TestProcessingFunctions(object):
    def setup(self):
        self.api_key = "DEMO_KEY"
        self.start_date = '2017-01-01'
        self.end_date = '2017-01-02'
        self.raw_data = '''
                        {
                            "near_earth_objects": {
                                "2017-01-01": [
                                    {
                                        "name": "blah",
                                        "neo_reference_id": "000000",
                                        "is_potentially_hazardous_asteroid": true,
                                        "close_approach_data": [
                                            {
                                                "close_approach_date": "2017-01-01",
                                                "miss_distance": {
                                                    "kilometers": "100000"
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        }
                        '''

    def test_parse_raw_data_to_df(self):
        df = parse_raw_data_to_df(json.loads(self.raw_data))
        print df.ix[0]
        assert_equal(len(df.index), 1)
        assert_equal(df.ix[0].neo_reference_id, "000000")
        assert_equal(df.ix[0]["name"], "blah")
        assert_equal(df.ix[0].is_potentially_hazardous, True)
        assert_equal(df.ix[0].miss_distance_km, "100000")
        assert_equal(df.ix[0].close_approach_date, "2017-01-01")

    def test_make_neo_request(self):
        data = make_neo_request(self.start_date, self.end_date, self.api_key)
        assert_equal(data["element_count"], 16)
        assert_equal(len(data["near_earth_objects"]), 2)

        
