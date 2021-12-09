DROP TABLE IF EXISTS Todolist;

create table Todolist
(
    id        int,
    username  string,
    board     string,
    task_name string,
    due_date  Date,
    priority  string,
    status    string
)
/*,

DROP TABLE IF EXISTS user;
create table user
(
    id       INTEGER not null
        primary key,
    username VARCHAR(15)
        unique,
    email    VARCHAR(50)
        unique,
    password VARCHAR(80)
);

*/