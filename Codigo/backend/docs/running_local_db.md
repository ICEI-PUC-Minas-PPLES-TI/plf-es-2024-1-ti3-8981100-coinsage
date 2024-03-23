# Dev guide: Running Local Database

1. Make sure your `backend/.env` file contains the following variables:
```Dockerfile
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=coinsage_db
DATABASE_USER=coinsage
DATABASE_PASSWORD=coinsage
```

2. On the folder `Codigos` run the following bash command:
```bash
docker compose --env-file ./backend/.env up
```

3. When the database is ready you will get something like this in your terminal log:
```bash
[+] Running 1/0
 ✔ Container coinsage_db  Created                                                                                                          0.0s
Attaching to coinsage_db
coinsage_db  |
coinsage_db  | PostgreSQL Database directory appears to contain a database; Skipping initialization
coinsage_db  |
coinsage_db  | 2024-03-23 16:09:40.724 UTC [1] LOG:  starting PostgreSQL 13.14 (Debian 13.14-1.pgdg120+2) on x86_64-pc-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit
coinsage_db  | 2024-03-23 16:09:40.727 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
coinsage_db  | 2024-03-23 16:09:40.727 UTC [1] LOG:  listening on IPv6 address "::", port 5432
coinsage_db  | 2024-03-23 16:09:40.735 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
coinsage_db  | 2024-03-23 16:09:40.749 UTC [27] LOG:  database system was shut down at 2024-03-23 16:09:26 UTC
coinsage_db  | 2024-03-23 16:09:40.763 UTC [1] LOG:  database system is ready to accept connections
```
4. Now you can run your fastAPI server and start developing! [Checkout out backend run local dev guide](./python_env.md) or [dev container guide](./dev_container.md)