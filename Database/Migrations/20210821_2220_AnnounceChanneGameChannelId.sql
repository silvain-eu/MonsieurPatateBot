create table AnnounceChannel
(
    GuidId            string not null
        constraint AnnounceChannel_pk
            primary key,
    AnnounceChannelId string not null,
    GameMessageId text default null
);

create unique index AnnounceChannel_GuidId_AnnounceChannelId_uindex
    on AnnounceChannel (GuidId, AnnounceChannelId);