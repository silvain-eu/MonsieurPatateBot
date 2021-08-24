create table Game
(
    id                   integer not null
        constraint Game_pk
            primary key autoincrement,
    name                 text    not null,
    guildId              text    not null,
    categoryId           text,
    memberIdCreate       text    not null,
    dateCreate           text    not null,
    roleId               text,
    memberUsernameCreate text    not null,
    emoticon             text    not null
);

create unique index Game_guildId_roleId_uindex
    on Game (guildId, roleId);

create unique index Game_name_guildId_uindex
    on Game (name, guildId);

create unique index Game_emoticon_uindex
    on Game (emoticon);

