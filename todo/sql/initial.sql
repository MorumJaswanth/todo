--userlist: username, name, id, email, pswrd

DROP TABLE IF EXISTS userlist;
DROP TABLE IF EXISTS user_;

CREATE TABLE userlist(
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	username TEXT UNIQUE NOT NULL,
	email TEXT UNIQUE NOT NULL,
	pswrd TEXT NOT NULL);

--user: id, taskname, taskdescription, deadline, deadline_time, status, userid

CREATE TABLE user_(
	id SERIAL PRIMARY KEY,
	taskname text,
	taskdescription text,
	deadline DATE,
	deadline_time TIME,
	status TEXT,
	userid integer references userlist(id));
