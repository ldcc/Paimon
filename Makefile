app=lemon
cqhttp=go-cqhttp
export py_ver=3.9

$(app): abort-$(app)
	docker run -dp 0.0.0.0:6000:6000 \
				-v $(PWD)/src/data/store:/app/src/data/store \
				-v $(PWD)/src/data/auth:/app/src/data/auth \
				--name $(app) $(app):latest
cqhttp: abort-cqhttp
	cd cqhttp && \
	chmod +x $(cqhttp) && \
	./$(cqhttp) > /dev/null 2>&1 &
start:
	make cqhttp
	make $(app)
commit:
	git add src/data
	if [ -n "`git status | grep 'Changes to be committed'`" ]; then \
  		git commit -m 'save stored'; \
	fi
	git add .
	if [ -z "`git stash | grep 'No local changes to save'`" ]; then git stash drop; fi
	git pull origin master
	if [ -z "`git status | grep 'is up to date'`" ]; then git push origin master; fi
upgrade:
	make commit
	if [ -z "`docker images | grep python | grep $(py_ver)`" ]; then docker pull python:$(py_ver); fi
	docker build -t $(app):latest .
	make start

abort: abort-cqhttp abort-$(app)
abort-$(app):
	if [ -n "`docker ps -a | grep $(app)`" ]; then docker rm `docker stop $(app)`; fi
abort-cqhttp:
	if [ -n "`pgrep $(cqhttp)`" ]; then kill `pgrep $(cqhttp)`; fi

.PHONY: cqhttp upgrade start abort abort-$(app) abort-cqhttp
