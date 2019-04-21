-- IRM: Isidro Rivera Monjaras
-- 10/03/2019
-- Inicio de base de datos

-- creacion de extensión
CREATE TABLE IF NOT EXISTS api.users (
  email    text primary key check ( email ~* '^.+@.+\..+$' ),
  pass     text not null check (length(pass) < 512),
  role     name not null check (length(role) < 512)
);

-- --------------------------------------------------------
CREATE TYPE api.jwt_token AS (
  token text
);

CREATE OR REPLACE FUNCTION api.login(email text, pass text) 
  RETURNS api.jwt_token AS $$
DECLARE
  _mail TEXT;
  result api.jwt_token;
BEGIN
  IF (NOT api.user_role(email, pass)) THEN
    RAISE invalid_password using message = 'invalid user or password';
  END IF;
  SELECT sign(
      row_to_json(r), current_setting('app.jwt_secret')
    ) AS token
    FROM (
      SELECT  email, 
              pass,
              TRUE AS login, 
              extract(epoch from now() + '5 minutes'::INTERVAL)::INTEGER AS exp -- MINUTOS EN EL DIA1440
    ) r
    INTO result;
  RETURN result;
END;$$ 
LANGUAGE plpgsql SECURITY DEFINER;
REVOKE ALL PRIVILEGES ON FUNCTION api.login(email text, pass text) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION api.login(email text, pass text)  TO api_anon;

-- -----------------------------------------
CREATE OR REPLACE FUNCTION auth.check_token() 
  RETURNS VOID AS $$
DECLARE
  --_name  TEXT;
BEGIN
  IF (api.user_role(current_setting('request.jwt.claim.email', TRUE), 
                     current_setting('request.jwt.claim.pass' , TRUE))
      AND COALESCE(current_setting('request.jwt.claim.login' , TRUE), 'FALSE')::BOOLEAN) THEN
    SET LOCAL ROLE api_user;
    RETURN;
  END IF;
END;$$
LANGUAGE plpgsql;

-- -------------------------------------------
CREATE OR REPLACE FUNCTION api.encrypt_pass() 
  RETURNS TRIGGER AS $$
BEGIN
  IF (tg_op = 'INSERT' or NEW.pass <> OLD.pass) THEN
    NEW.pass = crypt(NEW.pass, gen_salt('bf'));
  END IF;
  RETURN NEW;
END
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS encrypt_pass on api.users;
CREATE TRIGGER encrypt_pass
  BEFORE INSERT OR UPDATE ON api.users
  FOR EACH ROW
  EXECUTE PROCEDURE api.encrypt_pass();

-- ----------------------------------------------------------------
CREATE OR REPLACE FUNCTION api.user_role(p_email text, p_pass text) 
RETURNS BOOLEAN AS $$

BEGIN
  PERFORM email FROM api.users
   WHERE email = p_email
     AND pass = crypt(p_pass, pass);
  RETURN FOUND;
END;$$
LANGUAGE plpgsql SECURITY DEFINER;
REVOKE ALL PRIVILEGES ON FUNCTION api.user_role(email text, pass text)  FROM PUBLIC;
GRANT EXECUTE ON FUNCTION api.user_role(email text, pass text)  TO api_anon;

-- Nuestra API tendrá un punto final, / todos, que provendrá de una tabla.
CREATE TABLE api.todos (
  id SERIAL PRIMARY KEY,
  done BOOLEAN NOT NULL DEFAULT FALSE,
  task TEXT NOT NULL,
  due timestamptz
);

INSERT INTO api.todos (task) VALUES
  ('finish tutorial 0'), ('pat self on back');

GRANT USAGE ON SCHEMA api TO api_user;
GRANT ALL ON api.todos TO api_user;
GRANT USAGE, SELECT ON sequence api.todos_id_seq TO api_user;

ALTER TABLE api.todos ENABLE ROW LEVEL SECURITY;
CREATE POLICY account_managers ON api.todos
    USING (current_user = 'api_user');
