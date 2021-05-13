py_prog=python3.8
cqhttp=go-cqhttp

paimon:
	$(py_prog) bot.py > /dev/null 2>&1 &
cqhttp:
	cd cqhttp && \
	rm -rf data/leveldb && \
	chmod +x $(cqhttp) && \
	./$(cqhttp) > /dev/null 2>&1 &
upgrade: abort cqhttp
	git pull
	make abort
	make paimon
abort:
	$(shell if [ -n "pgrep $(py_prog)" ]; then pkill $(py_prog); fi)
	$(shell if [ -n "pgrep $(cqhttp)" ]; then pkill $(cqhttp); fi)

.PHONY: cqhttp upgrade abort
