nb=nb
cqhttp=go-cqhttp

paimon:
	$(nb) run >> logs/$(shell date +"%Y-%m-%d").log 2>&1 &
cqhttp:
	cd cqhttp && \
	rm -rf data/leveldb && \
	chmod +x $(cqhttp) && \
	./$(cqhttp) > /dev/null 2>&1 &
upgrade: abort cqhttp
	git pull
	python3.8 -m pip install -r requirements.txt
	make abort
	make cqhttp
	make paimon
abort:
	$(shell if [ -n "pgrep $(nb)" ]; then sudo pkill $(nb); fi)
	$(shell if [ -n "pgrep $(cqhttp)" ]; then sudo pkill $(cqhttp); fi)

.PHONY: cqhttp upgrade abort
