ARCHIVO DE CONFIGURACIÓN PostgREST
==================================

##### Archivo conf
>db-uri = "postgres://authenticator:1326011c3c01d5ca57fbb5741673c72d@localhost:5432/test_motor"
>db-schema = "api"
>db-anon-role = "api_anon"
>jwt-secret = "cfe0c52ed3745166b28f3a8cebadd7b1"
>pre-request = "auth.check_token"

##### Configura PostREST
crea archivo sudo vi /etc/nginx/api.conf

*Configuracuión nginx*

```javascript
# upstream configuration
upstream postgrest {
  server localhost:3000;
  keepalive 64;
}
server {
  listen localhost:4000;
  server_name api;

  location /api/ {
    default_type  application/json;
    proxy_hide_header Content-Location;
    add_header Content-Location  /api/$upstream_http_content_location;
    proxy_set_header  Connection "";
    proxy_http_version 1.1;
    proxy_pass http://postgrest/;
  }
}
```
*Creacion de trigger para actualizar*

```sql
CREATE OR REPLACE FUNCTION public.notify_ddl_postgrest()
  RETURNS event_trigger
 LANGUAGE plpgsql
  AS $$
BEGIN
  NOTIFY ddl_command_end;
END;
$$;
CREATE EVENT TRIGGER ddl_postgrest ON ddl_command_end
   EXECUTE PROCEDURE public.notify_ddl_postgrest();
```

Descargar el proyecto pg_listen:https://github.com/begriffs/pg_listen
segir los pasos descritos en el readme para instalación y enseguida ejecutar

```bash
pg_listen <db-uri> ddl_command_end "killall -SIGUSR1 postgrest"
```
#### Creando Daemonizing

Crear archivo sudo vi /etc/systemd/system/postgrest.service
```bash
[Unit]
Description=REST API for any Postgres database
After=postgresql.service

[Service]
ExecStart=/bin/postgrest /etc/postgrest/config
ExecReload=/bin/kill -SIGUSR1 $MAINPID

[Install]
WantedBy=multi-user.target
```

CONFIGURACIÓN DE BASE
=====================
```sql
CREATE EXTENSION pgcrypto; -- solo si es necesario
CREATE EXTENSION pgjwt;

CREATE SCHEMA api;
CREATE SCHEMA auth;

CREATE ROLE apienticator NOINHERIT login password '1326011c3c01d5ca57fbb5741673c72d';
CREATE ROLE api_anon NOTLOGIN;
CREATE ROLE api_user NOTLOGIN;

/*
db-uri = "postgres://apienticator:1326011c3c01d5ca57fbb5741673c72d@<host>:5432/<base>"
*/

GRANT api_anon TO apienticator;
GRANT api_user TO api_anon;
GRANT usage ON SCHEMA api TO api_user;
GRANT usage ON SCHEMA auth TO api_user;

SET db = motor_test;
ALTER DATABASE motor_test SET "app.jwt_secret" TO 'cfe0c52ed3745166b28f3a8cebadd7b1';
\i <ruta>/db_ini.sql
```

