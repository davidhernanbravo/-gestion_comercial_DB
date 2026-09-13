ROLES

Administrador: Va a poder manejar todo el sistema y cambiarlo. Modo Dios. Pero no influye en facturación.
Gerente: Administra la marcha del negocio y las finanzas, supervisa al admin y a los empleados.
Empleados:
    Empleado compras: CRUD proveedores, CRUD stock.
    Empleado venta: CRUD clientes, emite factura (incide en stock).

1. Admin: Crea la clase gerente, crea los clases de empleados: compra y venta (herencia).
2. Gerente: se encarga de Deletear, proveedores, productos del stock, clientes, facturas emitidas y empleados. Crea nuevos provedores, productos del stock, clientes y empleados.
3. Empleado Compra: Carga algunos proveedores, Genera la orden de compra de productos del stock, no puede Borrar productos del stock (es función de gerente).
4. Empleado Ventas: Carga algunos clientes, Genera la orden de venta de productos del stock (crea la factura), no puede Borrar facturas emitidas (es función de gerente).