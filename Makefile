app=lemon
cqhttp=go-cqhttp

$(app): abort-$(app)
	docker run -dp 0.0.0.0:6000:6000 -v $(PWD)/src/data/store:/app/src/data/store --name $(app) $(app):latest
cqhttp: abort-cqhttp
	cd cqhttp && \
	chmod +x $(cqhttp) && \
	./$(cqhttp) > /dev/null 2>&1 &
start:
	make cqhttp
	make $(app)
commit:
	git add src/data/store
	git commit -m 'save stored'
	git stash
	git stash drop
	git pull origin master
	git push origin master
upgrade:
	make commit
	git pull origin master
	docker build -t $(app):latest .
	make $(app)

abort: abort-cqhttp abort-$(app)
abort-$(app):
	if [ -n "`docker ps -a | grep $(app)`" ]; then docker container rm `docker stop $(app)` > /dev/null; fi
abort-cqhttp:
	if [ -n "`pgrep $(cqhttp)`" ]; then sudo pkill $(cqhttp); fi

.PHONY: cqhttp upgrade start abort abort-$(app) abort-cqhttp
