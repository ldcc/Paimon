nb=nb
cqhttp=go-cqhttp

paimon: abort-paimon
	$(nb) run >> logs/$(shell date +"%Y-%m-%d").log 2>&1 &
cqhttp: abort-cqhttp
	cd cqhttp && \
	rm -rf data/leveldb && \
	chmod +x $(cqhttp) && \
	./$(cqhttp) > /dev/null 2>&1 &
upgrade:
	git pull
	python3.8 -m pip install -r requirements.txt
	make cqhttp
	make paimon

abort-paimon:
	$(shell if [ -n "pgrep $(nb)" ]; then sudo pkill $(nb); fi)
abort-cqhttp:
	$(shell if [ -n "pgrep $(cqhttp)" ]; then sudo pkill $(cqhttp); fi)

abort: abort-cqhttp abort-paimon

.PHONY: cqhttp upgrade abort abort-paimon abort-cqhttp
