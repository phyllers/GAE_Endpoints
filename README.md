GAE_Endpoints
=============

Uses [Google Cloud Endpoints](https://cloud.google.com/appengine/docs/python/endpoints/) to create a simple greeting based api

Api Explorer [Here](https://isb-cgc.appspot.com/_ah/api/explorer)

TODO:
- Modify clients to use authorized endpoints

Endpoints:

- /fake_data : returns a test json object
- /rand_int : returns a random int from 1 to 1000
- /fake_treegraph_data : returns a fake tree of data to drive sample tree graph on demo site
- /fmdata : returns all sample feature matrix data that was given to us (10054 samples).
- /fmdata?{parameter}={value} : returns a filtered list of feature matrix data where the parameter=value for each record. If multiple parameters are given, they will be ANDed together.
- /fmdata/{sample_id} : given a sample id (e.g. TCGA-OR-A5J1-01), returns all feature matrix data we have for it.
- /fmdata_attr : returns a json object where the value for each key (attribute) is a string of a list of unique values in the database for that attribute.
- /fmattr: returns a json object of all attribute information that was embedded in the original feature names (i.e. C:CLIN:country:::::)