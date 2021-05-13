nb=nb
cqhttp=go-cqhttp

paimon:
	$(nb) run > /dev/null 2>&1 &
cqhttp:
	cd cqhttp && \
	rm -rf data/leveldb && \
	chmod +x $(cqhttp) && \
	./$(cqhttp) > /dev/null 2>&1 &
upgrade: abort cqhttp
	git pull
	make abort
	make cqhttp
	make paimon
abort:
	$(shell if [ -n "pgrep $(nb)" ]; then pkill $(nb); fi)
	$(shell if [ -n "pgrep $(cqhttp)" ]; then pkill $(cqhttp); fi)

.PHONY: cqhttp upgrade abort
