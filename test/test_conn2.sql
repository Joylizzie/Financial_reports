create table if not exists accounts (
	acct_name varchar(25),
	amt float
	)
	;
INSERT INTO accounts (acct_name, amt)
VALUES
    ('bob', 3),
    ('jack', 4)
;

