--Insercciones en la base de datos

--Ingresar Colombia como pais
insert into pais(codpais, nompais) values ('57', 'Colombia');

--Ingresar diferentes ciudades
insert into ciudad(codpais, codciudad, nomciudad) values ('57', '01', 'Bogotá');
insert into ciudad(codpais, codciudad, nomciudad) values ('57', '02', 'Medellín');
insert into ciudad(codpais, codciudad, nomciudad) values ('57', '03', 'Cali');

--Ingresar diferentes barrios
insert into barrio(codbarrio, codpais, codciudad, nombarrio) values ('PL', '57', '01', 'Palermo');
insert into barrio(codbarrio, codpais, codciudad, nombarrio) values ('BO', '57', '01', 'Bosa');
insert into barrio(codbarrio, codpais, codciudad, nombarrio) values ('CH', '57', '01', 'Chapinero');

--Ingresar las partes de las direcciones
insert into partedir(idpardire, despardire) values ('Cl', 'Calle');
insert into partedir(idpardire, despardire) values ('Cr', 'Carrera');
insert into partedir(idpardire, despardire) values ('Dg', 'Diagonal');
insert into partedir(idpardire, despardire) values ('Av', 'Avenida');
insert into partedir(idpardire, despardire) values ('In', 'Interior');
insert into partedir(idpardire, despardire) values ('Ap', 'Apto');

--Ingresar categorias
insert into categoria(idcate, nomcate, descate) values ('Al', 'Alimentos', 'Comida, Verduras, Vegetales');
insert into categoria(idcate, nomcate, descate) values ('As', 'Aseo', 'Higiene, Cocina, Casa');
insert into categoria(idcate, nomcate, descate) values ('Li', 'Licores', 'Alcohol, Vino, Cerveza');

--Ingresar proveedores cada uno con su dirección
-- proveedor 1
insert into proveedor (rutPro, nomPro, telPro, pagPro) values ('001', 'Almacenes Exito', 987654321, 'www.almacenesexito.com');
insert into direccion (iddir, rutpro, codbarrio) values (001, '001', 'BO');
insert into valordir(idpardire, iddir, valor) values ('Cl', 001, '65');
-- proveedor 2
insert into proveedor (rutpro, nompro, telpro, pagpro) values ('002', 'supermercados jumbo', 312456789, 'www.jumbo.com');
insert into direccion (iddir, rutpro, codbarrio) values (002, '002', 'BO');
insert into valordir (idpardire, iddir, valor) values ('Cl', 002, 120), ('Ap', 002, 301);
-- proveedor 3
insert into proveedor (rutpro, nompro, telpro, pagpro) values ('003', 'tienda olímpica', 320987654, 'www.olimpica.com');
insert into direccion (iddir, rutpro, codbarrio) values (003, '003', 'PL');
insert into valordir (idpardire, iddir, valor) values ('Cr', 003, 52), ('In', 003, 2);
-- proveedor 4
insert into proveedor (rutpro, nompro, telpro, pagpro) values ('004', 'Makro', 301123456, 'www.makro.com');
insert into direccion (iddir, rutpro, codbarrio) values (004, '004', 'CH');
insert into valordir (idpardire, iddir, valor) values ('Cl', 004, 88);
-- proveedor 5
insert into proveedor (rutpro, nompro, telpro, pagpro) values ('005', 'd1 tiendas', 315678234, 'www.tiendasd1.com');
insert into direccion (iddir, rutpro, codbarrio) values (005, '005', 'CH');
insert into valordir (idpardire, iddir, valor) values ('Dg', 005, 27), ('In', 005, 3);

--Ingresar clientes cada uno con su direccion y 2 telefonos
-- cliente 1
insert into cliente (rutcli, nomcli) values ('001', 'panaderia buen gusto');
insert into direccion (iddir, rutcli, codbarrio) values (006, '001', 'PL');
insert into valordir (idpardire, iddir, valor) values ('Av', 006, 30);
insert into telefono (idtel, rutcli, codpais, numerotel) values (3016574522, '001', '57', '3016574522');
insert into telefono (idtel, rutcli, codpais, numerotel) values (3014444522, '001', '57', '3014444522');
-- cliente 2
insert into cliente (rutcli, nomcli) values ('002', 'supermercado el ahorro');
insert into direccion (iddir, rutcli, codbarrio) values (007, '002', 'BO');
insert into valordir (idpardire, iddir, valor) values ('Cl', 007, 45);
insert into telefono (idtel, rutcli, codpais, numerotel) values (3112233445, '002', '57', '3112233445');
insert into telefono (idtel, rutcli, codpais, numerotel) values (3209988776, '002', '57', '3209988776');
-- cliente 3
insert into cliente (rutcli, nomcli) values ('003', 'ferreteria la union');
insert into direccion (iddir, rutcli, codbarrio) values (008, '003', 'CH');
insert into valordir (idpardire, iddir, valor) values ('Cr', 008, 18);
insert into telefono (idtel, rutcli, codpais, numerotel) values (3145678923, '003', '57', '3145678923');
insert into telefono (idtel, rutcli, codpais, numerotel) values (3156789012, '003', '57', '3156789012');
-- cliente 4
insert into cliente (rutcli, nomcli) values ('004', 'carniceria los primos');
insert into direccion (iddir, rutcli, codbarrio) values (009, '004', 'PL');
insert into valordir (idpardire, iddir, valor) values ('Av', 009, 12);
insert into telefono (idtel, rutcli, codpais, numerotel) values (3167890123, '004', '57', '3167890123');
insert into telefono (idtel, rutcli, codpais, numerotel) values (3178901234, '004', '57', '3178901234');
-- cliente 5
insert into cliente (rutcli, nomcli) values ('005', 'papeleria el estudiante');
insert into direccion (iddir, rutcli, codbarrio) values (010, '005', 'BO');
insert into valordir (idpardire, iddir, valor) values ('Dg', 010, 22);
insert into telefono (idtel, rutcli, codpais, numerotel) values (3189012345, '005', '57', '3189012345');
insert into telefono (idtel, rutcli, codpais, numerotel) values (3190123456, '005', '57', '3190123456');

--Registrar 3 empleados
insert into empleado (codempleado, nomempleado, apellempleado, "USER", password) values ('01', 'Andrea', 'Martinez', 'andma', '12345');
insert into empleado (codempleado, nomempleado, apellempleado, "USER", password) values ('02', 'Luis', 'Diaz', 'lucho', '72489');
insert into empleado (codempleado, nomempleado, apellempleado, "USER", password) values ('03', 'Alegria', 'Fernandez', 'algfe', '16245');

--Ingresar 3 productos por cada categoria cada uno con 3 precios
-- producto 1 (alimento)
insert into producto (idpro, idcate, rutpro, nompro, stock) values ('0001', 'Al', '001', 'sardina', 1000);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0001, '0001', '2025-02-02', 4800);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0002, '0001', '2025-02-03', 4900);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0003, '0001', '2025-02-04', 4950);
-- producto 2 (alimento)
insert into producto (idpro, idcate, rutpro, nompro, stock) values ('0003', 'Al', '003', 'lentejas', 1200);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0007, '0003', '2025-02-02', 3500);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0008, '0003', '2025-02-03', 3600);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0009, '0003', '2025-02-04', 3700);
-- producto 3 (alimento)
insert into producto (idpro, idcate, rutpro, nompro, stock) values ('0004', 'Al', '004', 'harina de maíz', 900);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0010, '0004', '2025-02-02', 2800);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0011, '0004', '2025-02-03', 2900);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0012, '0004', '2025-02-04', 3000);
-- producto 4 (aseo)
insert into producto (idpro, idcate, rutpro, nompro, stock) values ('0005', 'As', '005', 'jabón de baño', 500);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0013, '0005', '2025-02-02', 2500);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0014, '0005', '2025-02-03', 2600);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0015, '0005', '2025-02-04', 2700);
-- producto 5 (aseo)
insert into producto (idpro, idcate, rutpro, nompro, stock) values ('0006', 'As', '001', 'detergente en polvo', 700);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0016, '0006', '2025-02-02', 5400);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0017, '0006', '2025-02-03', 5500);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0018, '0006', '2025-02-04', 5600);
-- producto 6 (aseo)
insert into producto (idpro, idcate, rutpro, nompro, stock) values ('0007', 'As', '001', 'cloro', 600);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0019, '0007', '2025-02-02', 3200);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0020, '0007', '2025-02-03', 3300);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0021, '0007', '2025-02-04', 3400);
-- producto 7 (licores)
insert into producto (idpro, idcate, rutpro, nompro, stock) values ('0008', 'Li', '001', 'vodka premium', 500);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0022, '0008', '2025-02-02', 22000);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0023, '0008', '2025-02-03', 22500);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0024, '0008', '2025-02-04', 23000);
-- producto 8 (licores)
insert into producto (idpro, idcate, rutpro, nompro, stock) values ('0009', 'Li', '001', 'ron añejo', 300);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0025, '0009', '2025-02-02', 18000);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0026, '0009', '2025-02-03', 18500);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0027, '0009', '2025-02-04', 19000);
-- producto 9 (licores)
insert into producto (idpro, idcate, rutpro, nompro, stock) values ('0010', 'Li', '001', 'tequila reposado', 400);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0028, '0010', '2025-02-02', 25000);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0029, '0010', '2025-02-03', 25500);
insert into precio (idprecio, idpro, fechaprecio, valorprecio) values (0030, '0010', '2025-02-04', 26000);












