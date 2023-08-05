create table "{ns}".formula (
  id serial primary key,
  name text not null,
  text text not null,
  metadata jsonb
);

create unique index "ix_{ns}_formula_name" on "{ns}".formula (name);
