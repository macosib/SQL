CREATE TABLE IF NOT EXISTS EMPLOYEES (
ID SERIAL PRIMARY KEY,
DEPARTMENT VARCHAR(100) NOT NULL,
HEAD INTEGER NOT null,
FOREIGN KEY (HEAD)  REFERENCES EMPLOYEES (ID)
);