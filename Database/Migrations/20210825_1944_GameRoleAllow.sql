create table GameRoleAllow
(
	GameId int not null
		constraint GameRoleAllow_Game_id_fk
			references Game,
	RoleId TEXT,
	constraint GameRoleAllow_pk
		primary key (GameId, RoleId)
);

