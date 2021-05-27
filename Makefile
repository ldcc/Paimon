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
upgrade:
	git add src/data/store
	git commit -m "save stored data"
	git push
	make update
update:
	git pull
	python3.8 -m pip install -r requirements.txt
	make start

abort-paimon:
	$(shell if [ -n "pgrep $(nb)" ]; then sudo pkill $(nb); fi)
abort-cqhttp:
	$(shell if [ -n "pgrep $(cqhttp)" ]; then sudo pkill $(cqhttp); fi)

abort: abort-cqhttp abort-paimon

.PHONY: cqhttp upgrade update start abort abort-paimon abort-cqhttp
