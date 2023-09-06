create table works (
    post_id integer not null primary key,
    chat_id integer not null,
    content text not null,
    expires text default 'never',
    finished integer not null default 0
);