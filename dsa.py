import pprint
import sqlite3
conn = sqlite3.connect('logistic_company.sqlite')
c = conn.cursor()

c.execute('''drop table if exists cars''')
c.execute('''drop table if exists courier''')
c.execute('''drop table if exists cargos''')
c.execute('''drop table if exists products''')
c.execute('''drop table if exists orders''')
c.execute('''drop table if exists customers''')

c.execute('''create table if not exists customers (
    id_customer integer,
    name varchar(30),
    phone numeric(11),
    constraint PK_customers_id_customer primary key(id_customer)
)''')

c.execute('''create table if not exists products (
    id_product integer,
    name text not null,
    price int not null,
    weight numeric(4,2) not null,
    constraint PK_products_id_product primary key (id_product)
)''')

c.execute('''create table if not exists orders (
    id_order integer,
    id_product int,
    id_customer int,
    weight numeric(4,2) not null,
    total_price int,
    status text,
    constraint PK_orders_id_order primary key (id_order),
    constraint Fk_orders_id_product foreign key (id_product) references products (id_product),
    constraint Fk_orders_id_customer foreign key (id_customer) references customers (id_customer),
    constraint CK_orders_status check(status in ('в сборке','в пути','доставленно'))
)''')

c.execute('''create table if not exists cargos (
    id_cargo int,
    id_orders int,
    weight numeric(4,2),
    constraint PK_cargos_id_cargo_id_orders primary key (id_cargo,id_orders),
    constraint Fk_cargo_id_orders foreign key (id_orders) references orders (id_order),
    constraint CK_cargo_weight check(weight > 0)
)''')

c.execute('''create table if not exists courier (
    id_courier integer not null,
    id_car int,
    name varchar(30),
    phone varchar(12),
    constraint PK_courier_id_courier Primary key(id_courier),
    constraint FK_courier_id_car foreign key (id_car) references cars (id_car)
)''')

c.execute('''create table if not exists cars (
    id_car integer,
    lifting_capacity numeric(4,2) not null,
    id_cargos int,
    availability text check(availability in ("Не доступен","Доступен")),
    constraint PK_cars_id_car primary key (id_car),
    constraint Fk_cars_id_cargos foreign key (id_cargos) references cargos (id_cargo),
    constraint CK_lifting_capacity Check(lifting_capacity > 100)
)''')

c.execute(''' insert into cargos (id_cargo, id_orders, weight) values (1,1, null), (1,4, null) ''')
conn.commit()
