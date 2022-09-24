from tools import *
import csv

##
#TODO:
#organiser les données pour être exploité par un plugin ? sqlite ?
##

def save_data(val, det, con):
	with open(f'data/{slug}.csv', 'a+', newline='') as f:
		f.write(f'[{time.strftime("%d/%m/%Y-%H:%M")}]{value}\n')
		wr = csv.writer(f, quoting=csv.QUOTE_ALL)
		wr.writerow(details)
		wr.writerow(conditions)

html = get_html('https://fr.igraal.com/selection/', 5)
selection_du_jour = re.search(r'Classement des offres(.*?)data-ig-redir-position=10', html, re.MULTILINE | re.DOTALL).group(0)

top_10_slug = re.findall(r'data-ig-redir-urlname=(.*?) ', selection_du_jour)
for slug in top_10_slug:
	html = get_html(f'https://fr.igraal.com/codes-promo/{slug}', 5)

	main_cashback = re.search(r'data-ig-cashback-block(.*?)see conditions', html, re.MULTILINE | re.DOTALL).group(0)

	value = re.search(r'merchant-first-cb__title.*?>(.*?)<', main_cashback).group(1).strip()
	print(value)
	details = re.findall(r'merchant-first-cb__list-item">(.*?)</li', main_cashback)
	print(details)
	conditions = re.findall(r'mr-xxs-2.*?<span>(.*?)</span>', main_cashback)
	print(conditions)
