paimon:
	python3.8 bot.py > /dev/null 2>&1 &
go-cqhttp:
	cd cqhttp && \
	./go-cqhttp > /dev/null 2>&1 &
upgrade:
	pkill python3.8
	git pull
	make paimon
