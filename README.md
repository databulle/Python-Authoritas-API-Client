# Authoritas SERPs API - Python client

A quick client to use Auhtoritas SERPs API in Python.  
Have a look here: <https://www.authoritas.com/keyword-ranking-api/>.  


## Setup

These scripts have been tested with Python 3.7.0  
I recommend using [pyenv](https://github.com/pyenv/pyenv) or any other virtual environment manager.  

To install dependencies, simply run:  

```
pip install -r requirements.txt  
```

## Usage

Two steps:  

1. send queries to the API  
2. ask for results  

### Sending queries

Using the `send_queries.py` script, you'll be able to send your list of queries to Authoritas SERPs API quite simply.   
Put your queries into a simple text file (one query per line) and use this command:  

```
python send_queries.py --input your_queries.txt  
```

Each query will be sent to the API and the corresponding job id will be saved into a CSV file.  

The script offers multiple options:  
- `-i` or `--input`: the mandatory input file (one query per line)  
- `-o` or `--output`: a basename to create your output file (default: `queries`)  
- `--sep`: output CSV separator (default is ";")  
- `-n` or `--nb_res`: number of results to fetch (default: 10)  
- `-s` or `--search_engine` the search engine to use (choose between `google`, `bing`, `yahoo`, `yandex` and `baidu`, default is `google`)  
- `-r` or `--region`: the search engine region (choose between `global`, `fr`, `gb`, `us` or `es`, default is `global`)  
- `-l` or `--language`: the search engine language (choose between `en`, `fr` or `es`, default is `en`)  
- `-u` or `--user_agent`: the type of device to use (choose between `pc`, `mac`, `tablet`, `ipad`, `iphone` and `mobile`, default is `pc`)  
- `--no_cache`: to force the API not to use cached results (default: False)  
- `-d` or `--delay`: the delay in seconds between requests (default: 2)  

### Getting results

Use the `get_results.py` script to fetch results from jobs:  
```
python get_results.py --input job_ids.csv  
```

The script will fetch results for each `jid` and save SEO results to a CSV file, containing for each result in a SERP:  
- the query,  
- the job id,
- the job status,
- the result position,  
- the page,  
- the url, 
- the result title.  

Other data is available through the API, check [the docs](http://docs.authoritas.com/serps/) for more details.  

Here is a list of available script options:  
- `-i` or `--input`: a CSV file containing a `query` and a `jid` columns (using `send_queries.py` output is easiest)  
- `--input_sep`: specify an input CSV separator (default is ";")  
- `-o` or `--output`: a basename to create your output file (default is `results`)  
- `--sep`: output CSV separator (default is ";")  
- `-d` or `--delay` the delay in seconds between requests (default: 2)   


