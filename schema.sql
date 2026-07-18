create table  if not exists trips(
    id integer primary key autoincrement,
    destination text not null,
    country text not null,
    travel_type text not null check (travel_type in ('Solo','Friends','Family','Business','Other')),
    estimated_budget real not null,
    status text not null default 'Planned' check(status in ('Planned','Completed')),
    rating integer check(rating between 1 and 5),
    experience_notes text ,
    created_at text not null default current_timestamp
);

create table if not exists places_to_visit(
    id integer primary key autoincrement,
    trip_id integer not null,
    place_name text not null,
    visited integer not null default 0,
    foreign key (trip_id) references trips(id) on delete cascade
);

create table if not exists planning_notes(
    id integer primary key autoincrement,
    trip_id integer not null,
    note_text text not null,
    created_at text not null default current_timestamp,
    foreign key (trip_id) references trips(id) on delete cascade
);

create table if not exists expenses(
    id integer primary key autoincrement,
    trip_id integer not null,
    category text not null  check(category in ('Flight','Hotel','Food','Shopping','Transport','Other')),
    amount real not null,
    description text ,
    expense_date text not null ,
    foreign key (trip_id)  references trips(id) on delete cascade
);