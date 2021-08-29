drop index Game_emoticon_uindex;

create unique index Game_emoticon_uindex
    on Game (guildId,emoticon);