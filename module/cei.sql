-- Obtener el nombre del empleado
tSELECT nomempleado FROM empleado WHERE codempleado = %s;

-- Obtener el número de factura más alto
tSELECT MAX(noventa) FROM venta;

-- Obtener el nombre del cliente
tSELECT nomcli FROM cliente WHERE rutcli = %s;

-- Buscar producto por nombre
tSELECT idpro, nompro, stock FROM producto WHERE nompro ILIKE %s;

-- Obtener el precio más reciente del producto
tSELECT valorprecio FROM precio WHERE idpro = %s ORDER BY fechaprecio DESC LIMIT 1;

-- Insertar una nueva venta
tINSERT INTO venta (noventa, codempleado, rutcli, fecventa) VALUES (%s, %s, %s, %s);

-- Insertar detalle de venta
tINSERT INTO detalleventa (noventa, item, idpro, precio, cantidad, descuento, preciototal) VALUES (%s, %s, %s, %s, %s, %s, %s);

-- Actualizar stock del producto
tUPDATE producto SET stock = stock - %s WHERE idpro = %s;

-- Verificar credenciales de usuario
tSELECT codempleado, nomempleado FROM empleado WHERE usuario=%s AND contrasena=%s;

-- Insertar un nuevo empleado
tINSERT INTO empleado (codempleado, nomempleado, apellido, usuario, contrasena) VALUES (%s, %s, %s, %s, %s);