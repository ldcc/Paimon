nb=nb
cqhttp=go-cqhttp

paimon: abort-paimon
	$(nb) run >> logs/$(shell date +"%Y-%m-%d").log 2>&1 &
cqhttp: abort-cqhttp
	cd cqhttp && \
	chmod +x $(cqhttp) && \
	./$(cqhttp) > /dev/null 2>&1 &
start:
	make cqhttp
	make paimon
save:
	$(shell git add src/data/store)
	$(shell git commit -m "save stored data")
	$(shell git push)
upgrade: save
	git pull
	python3.8 -m pip install -r requirements.txt
	make start

abort-paimon:
	$(shell if [ -n "pgrep $(nb)" ]; then sudo pkill $(nb); fi)
abort-cqhttp:
	$(shell if [ -n "pgrep $(cqhttp)" ]; then sudo pkill $(cqhttp); fi)

abort: abort-cqhttp abort-paimon

.PHONY: save cqhttp upgrade start abort abort-paimon abort-cqhttp
