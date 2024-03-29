import os, sys, re, csv, time

from tools import log, get_html_android

##
#TODO:
# - Warn by email or SMS on fail
# - Save les data dans une DB au lieu des csv
##

def save_data(val, det, con):
	if not os.path.exists('data_igraal'): os.mkdir('data_igraal')
	with open(f'data_igraal/{slug}.csv', 'a+', newline='') as f:
		f.write(f'[{time.strftime("%d/%m/%Y-%H:%M")}]{value}\n')
		wr = csv.writer(f, quoting=csv.QUOTE_ALL)
		wr.writerow(details)
		wr.writerow(conditions)

unlock_screen()
html = get_html_android('https://fr.igraal.com/selection/?s=publishDate')

if 'yohan' not in html:
	log('User is not connected ', verbose=True)
	sys.exit()

selection_du_jour = re.search(r'Classement des offres(.*?)data-ig-redir-position=10', html, re.MULTILINE | re.DOTALL).group(0)
tops_slug = re.findall(r'data-ig-redir-urlname=(.*?) ', selection_du_jour)
print(f'Scrap {len(tops_slug)} links')
for slug in tops_slug:
	print(slug)
	html = get_html_android(f'https://fr.igraal.com/codes-promo/{slug}')
	main_cashback = re.search(r'data-ig-cashback-block(.*?)see conditions', html, re.MULTILINE | re.DOTALL).group(0)

	value = re.search(r'merchant-first-cb__title.*?>(.*?)<', main_cashback).group(1).strip()
	print(value)
	details = re.findall(r'merchant-first-cb__list-item>(.*?)<', main_cashback)
	print(details)
	conditions = re.findall(r'mr-xxs-2.*?<span>(.*?)</span>', main_cashback)
	print(conditions)

	save_data(value, details, conditions)

unlock_screen(lock=True)