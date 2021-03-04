importData:
	mv ~/Downloads/accountActivityExport.csv ./data

scrape:
	python3 scraper.py

worker:
	python3 worker.py