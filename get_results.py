import requests
import time
import hmac
import hashlib
import base64
import json
import argparse
import csv
import configparser

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input', type=str, required=True,
					help='Input CSV file (needs columns query and jid).')
	parser.add_argument('--input_sep', type=str, default=';',
					help='Input CSV separator (default: ";").')
	parser.add_argument('-o', '--output', type=str, default='results',
					help='Output file basename (default: results).')
	parser.add_argument('--sep', type=str, default=';',
					help='Output CSV separator (default: ";").')
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

	# Output name
	timestr = time.strftime("%Y%m%d-%H%M%S")
	filename = args.output + "-" + timestr + ".csv"
	output_headers = ['query','jid','status','position','page','url','title']
	with open(filename,'w',newline='') as output_file:
		writer = csv.DictWriter(output_file, fieldnames=output_headers, delimiter=args.sep)
		writer.writeheader()
		output_file.close()

	with open(args.input,'r') as input_file:
		reader = csv.DictReader(input_file, delimiter=args.input_sep)
		for row in reader:
			kw = row['query']
			jid = row['jid']

			# Generate a unix timestamp to insert into headers
			now = int(time.time())

			# Generate headers
			hash_data = "{}{}{}".format(now, public_key, salt)
			hashed = hmac.new(private_key.encode("utf-8"), hash_data.encode("utf-8"), hashlib.sha256).hexdigest()
			headers = {
				'accept': "application/json", 
				'Authorization': "KeyAuth publicKey={} hash={} ts={}".format(public_key,hashed,now)
			}
			url = '{}/search_results/{}'.format(host,jid)
			
			# Get data
			r = requests.get(url, headers=headers)

			with open(filename,'a',newline='') as output_file:
				writer = csv.DictWriter(output_file, fieldnames=output_headers, delimiter=args.sep)

				if r.status_code == 200:
					try:
						response = json.loads(r.content)['response']['results']

						for key in response['organic'].keys():
							writer.writerow({
								'query': kw,
								'jid': jid,
								'status': 'ok',
								'position': key,
								'page': response['organic'][key]['page_number'],
								'url': response['organic'][key]['url'],
								'title': response['organic'][key]['title'],
							})
						print('Query "{}" OK (jid: {}).'.format(kw,jid))
					# Some '200-OK' responses don't have real data
					except KeyError:
						writer.writerow({
							'query': kw,
							'jid': jid,
							'status': 'error',
						})
						print('Error for query "{}" (jid: {}).'.format(kw,jid))	
				else:
					writer.writerow({
						'query': kw,
						'jid': jid,
						'status': r.status_code,
						})
					print('Error for query "{}" (jid: {}).'.format(kw,jid))	
				output_file.close()
			time.sleep(args.delay)
		input_file.close()
