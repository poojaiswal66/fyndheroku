create table faculty(
id number PRIMARY KEY,
name VARCHAR2(10) NOT NULL,
password VARCHAR2(10) NOT NULL,
admin boolean NOT NULL
);

create table student(
studentid NUMBER PRIMARY KEY,
name VARCHAR2(10) NOT NULL,
email VARCHAR2(15),
phone NUMBER,
address VARCHAR2(20),
marks NUMBER,
fees NUMBER
)