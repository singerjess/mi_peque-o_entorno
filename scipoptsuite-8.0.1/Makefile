build:
	docker build -f scip.dockerfile -t scip:latest .

run:
	docker run -d --name scip scip:latest

clean:
	docker stop $$(docker ps -a -q) && docker rm $$(docker ps -a -q)

exec:
	docker exec -ti scip scip
