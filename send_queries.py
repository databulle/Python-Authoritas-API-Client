import requests
import time
import hmac
import hashlib
import base64
import json
import argparse
import csv

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input', type=str, required=True,
					help='Input file (one query per line).')
	parser.add_argument('-o', '--output', type=str, default='queries',
					help='Output file basename (default: queries).')
	parser.add_argument('--sep', type=str, default=';',
					help='Output CSV separator (default: ";").')
	parser.add_argument('-n', '--nb_res', type=int, default=10,
					help='Number of results to fetch (default: 10).')
	parser.add_argument('-r', '--region', type=str, default='global',
					choices=['global','fr','gb','us','es'],
					help='Region (default: global).')
	parser.add_argument('-l', '--language', type=str, default='en',
					choices=['en','fr','es'],
					help='Language (default: en).')
	parser.add_argument('-s', '--search_engine', type=str, default='google',
					choices=['google','bing','yahoo','yandex','baidu'],
					help='Search Engine (default: google).')
	parser.add_argument('-u', '--user_agent', type=str, default='pc',
					choices=['pc','mac','tablet','ipad','iphone','mobile'],
					help='User Agent choice (default: pc).')
	parser.add_argument('--no_cache', action='store_true', default=False,
					help='Do not use query cache (default: False).')
	parser.add_argument('-d', '--delay', type=int, default=2,
					help='Delay in seconds between requests (default: 2).')
	args = parser.parse_args()

	# Get API settings from config.ini file
	config = configparser.ConfigParser()
	config.read('config.ini')
	host = config.get('AUTHORITAS_API','host')
	private_key = config.get('AUTHORITAS_API','private_key')
	public_key = config.get('AUTHORITAS_API','public_key')
	salt = config.get('AUTHORITAS_API','salt')

	kws = list()
	# Read list of requests
	with open(args.input,'r') as file:
		for line in file.readlines():
			kws.append(str.strip(line))
		file.close()


	# Output name
	timestr = time.strftime("%Y%m%d-%H%M%S")
	filename = args.output + "-" + timestr + ".csv"

	output_headers = ['query','jid']
	with open(filename,'w',newline='') as file:
		writer = csv.DictWriter(file, fieldnames=output_headers, delimiter=args.sep)
		writer.writeheader()
		file.close()

	for kw in kws:
		# Generate a unix timestamp to insert into headers
		now = int(time.time())

		# Generate headers
		hash_data = "{}{}{}".format(now, public_key, salt)
		hashed = hmac.new(private_key.encode("utf-8"), hash_data.encode("utf-8"), hashlib.sha256).hexdigest()
		headers = {
			'accept': "application/json", 
			'Authorization': "KeyAuth publicKey={} hash={} ts={}".format(public_key,hashed,now)
		}

		# Request body
		body = {
			"search_engine":args.search_engine,
			"region":args.region,
			"language":args.language,
			"max_results":args.nb_res,
			"phrase":kw
		}
		if args.no_cache:
			body['use_cache'] = False

		url = '{}/search_results/'.format(host)
		r = requests.post(url, data=json.dumps(body), headers=headers)
		with open(filename,'a',newline='') as file:
			writer = csv.DictWriter(file, fieldnames=output_headers, delimiter=args.sep)
			writer.writerow({
				'query': kw,
				'jid': r.json().get('jid')
			})
			file.close()
		print('Request {} created (jid: {}).'.format(kw,r.json().get('jid')))
		time.sleep(args.delay)