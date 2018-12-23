
certificate:
	(ll server.crt && ll server.key) || \\
	openssl req -new -x509 -nodes -newkey rsa:1024 -keyout server.key -out server.crt -days 3650

build: certificate
	docker-compose build
