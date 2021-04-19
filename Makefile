paimon:
	python3.8 bot.py > /dev/null 2>&1 &

upgrade:
	pkill python3.8
	git pull
	make paimon
