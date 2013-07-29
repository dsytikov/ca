create table "candidats" (
  id integer primary key autoincrement,
  company TEXT(50) not null,
  data_check TEXT(10) not null,
  surname TEXT(30) not null,
  name TEXT(15) not null,
  patronymic TEXT(30) not null,
  bday TEXT(10),
  address TEXT(30),
  result_check TEXT(100),
  resolve TEXT(30)
);