/*==============================================================*/
/* DBMS name:      PostgreSQL 8                                 */
/* Created on:     4/02/2025 5:58:10 p. m.                      */
/*==============================================================*/


/*==============================================================*/
/* Table: BARRIO                                                */
/*==============================================================*/
create table BARRIO (
   CODBARRIO            VARCHAR(6)           not null,
   CODPAIS              VARCHAR(3)           not null,
   CODCIUDAD            VARCHAR(6)           not null,
   NOMBARRIO            VARCHAR(40)          not null,
   constraint PK_BARRIO primary key (CODBARRIO)
);

/*==============================================================*/
/* Index: BARRIO_PK                                             */
/*==============================================================*/
create unique index BARRIO_PK on BARRIO (
CODBARRIO
);

/*==============================================================*/
/* Index: RELATIONSHIP_14_FK                                    */
/*==============================================================*/
create  index RELATIONSHIP_14_FK on BARRIO (
CODPAIS,
CODCIUDAD
);

/*==============================================================*/
/* Table: CATEGORIA                                             */
/*==============================================================*/
create table CATEGORIA (
   IDCATE               VARCHAR(4)           not null,
   NOMCATE              VARCHAR(30)          not null,
   DESCATE              VARCHAR(50)          not null,
   constraint PK_CATEGORIA primary key (IDCATE)
);

/*==============================================================*/
/* Index: CATEGORIA_PK                                          */
/*==============================================================*/
create unique index CATEGORIA_PK on CATEGORIA (
IDCATE
);

/*==============================================================*/
/* Table: CIUDAD                                                */
/*==============================================================*/
create table CIUDAD (
   CODPAIS              VARCHAR(3)           not null,
   CODCIUDAD            VARCHAR(6)           not null,
   NOMCIUDAD            VARCHAR(30)          not null,
   constraint PK_CIUDAD primary key (CODPAIS, CODCIUDAD)
);

/*==============================================================*/
/* Index: CIUDAD_PK                                             */
/*==============================================================*/
create unique index CIUDAD_PK on CIUDAD (
CODPAIS,
CODCIUDAD
);

/*==============================================================*/
/* Index: RELATIONSHIP_15_FK                                    */
/*==============================================================*/
create  index RELATIONSHIP_15_FK on CIUDAD (
CODPAIS
);

/*==============================================================*/
/* Table: CLIENTE                                               */
/*==============================================================*/
create table CLIENTE (
   RUTCLI               VARCHAR(3)           not null,
   NOMCLI               VARCHAR(40)          not null,
   constraint PK_CLIENTE primary key (RUTCLI)
);

/*==============================================================*/
/* Index: CLIENTE_PK                                            */
/*==============================================================*/
create unique index CLIENTE_PK on CLIENTE (
RUTCLI
);

/*==============================================================*/
/* Table: DETALLEVENTA                                          */
/*==============================================================*/
create table DETALLEVENTA (
   NOVENTA              INT8                 not null,
   ITEM                 INT2                 not null,
   IDPRO                VARCHAR(6)           not null,
   PRECIO               NUMERIC(5,1)         not null,
   CANTIDAD             INT8                 not null,
   DESCUENTO            INT8                 null,
   PRECIOTOTAL          NUMERIC(5,2)         not null,
   constraint PK_DETALLEVENTA primary key (NOVENTA, ITEM)
);

/*==============================================================*/
/* Index: DETALLEVENTA_PK                                       */
/*==============================================================*/
create unique index DETALLEVENTA_PK on DETALLEVENTA (
NOVENTA,
ITEM
);

/*==============================================================*/
/* Index: RELATIONSHIP_4_FK                                     */
/*==============================================================*/
create  index RELATIONSHIP_4_FK on DETALLEVENTA (
IDPRO
);

/*==============================================================*/
/* Index: RELATIONSHIP_6_FK                                     */
/*==============================================================*/
create  index RELATIONSHIP_6_FK on DETALLEVENTA (
NOVENTA
);

/*==============================================================*/
/* Table: DIRECCION                                             */
/*==============================================================*/
create table DIRECCION (
   IDDIR                INT8                 not null,
   RUTPRO               VARCHAR(3)           null,
   RUTCLI               VARCHAR(3)           null,
   CODBARRIO            VARCHAR(6)           not null,
   constraint PK_DIRECCION primary key (IDDIR)
);

/*==============================================================*/
/* Index: DIRECCION_PK                                          */
/*==============================================================*/
create unique index DIRECCION_PK on DIRECCION (
IDDIR
);

/*==============================================================*/
/* Index: RELATIONSHIP_9_FK                                     */
/*==============================================================*/
create  index RELATIONSHIP_9_FK on DIRECCION (
RUTPRO
);

/*==============================================================*/
/* Index: RELATIONSHIP_10_FK                                    */
/*==============================================================*/
create  index RELATIONSHIP_10_FK on DIRECCION (
RUTCLI
);

/*==============================================================*/
/* Index: RELATIONSHIP_13_FK                                    */
/*==============================================================*/
create  index RELATIONSHIP_13_FK on DIRECCION (
CODBARRIO
);

/*==============================================================*/
/* Table: EMPLEADO                                              */
/*==============================================================*/
create table EMPLEADO (
   CODEMPLEADO          VARCHAR(4)           not null,
   NOMEMPLEADO          VARCHAR(30)          not null,
   APELLEMPLEADO        VARCHAR(30)          not null,
   USUARIO               VARCHAR(5)           not null,
   CONTRASENA             VARCHAR(5)           not null,
   constraint PK_EMPLEADO primary key (CODEMPLEADO)
);

/*==============================================================*/
/* Index: EMPLEADO_PK                                           */
/*==============================================================*/
create unique index EMPLEADO_PK on EMPLEADO (
CODEMPLEADO
);

/*==============================================================*/
/* Table: PAIS                                                  */
/*==============================================================*/
create table PAIS (
   CODPAIS              VARCHAR(3)           not null,
   NOMPAIS              VARCHAR(30)          not null,
   constraint PK_PAIS primary key (CODPAIS)
);

/*==============================================================*/
/* Index: PAIS_PK                                               */
/*==============================================================*/
create unique index PAIS_PK on PAIS (
CODPAIS
);

/*==============================================================*/
/* Table: PARTEDIR                                              */
/*==============================================================*/
create table PARTEDIR (
   IDPARDIRE            VARCHAR(4)           not null,
   DESPARDIRE           VARCHAR(30)          not null,
   constraint PK_PARTEDIR primary key (IDPARDIRE)
);

/*==============================================================*/
/* Index: PARTEDIR_PK                                           */
/*==============================================================*/
create unique index PARTEDIR_PK on PARTEDIR (
IDPARDIRE
);

/*==============================================================*/
/* Table: PRECIO                                                */
/*==============================================================*/
create table PRECIO (
   IDPRECIO             INT8                 not null,
   IDPRO                VARCHAR(6)           not null,
   FECHAPRECIO          DATE                 not null,
   VALORPRECIO          INT8                 not null,
   constraint PK_PRECIO primary key (IDPRECIO)
);

/*==============================================================*/
/* Index: PRECIO_PK                                             */
/*==============================================================*/
create unique index PRECIO_PK on PRECIO (
IDPRECIO
);

/*==============================================================*/
/* Index: RELATIONSHIP_3_FK                                     */
/*==============================================================*/
create  index RELATIONSHIP_3_FK on PRECIO (
IDPRO
);

/*==============================================================*/
/* Table: PRODUCTO                                              */
/*==============================================================*/
create table PRODUCTO (
   IDPRO                VARCHAR(6)           not null,
   IDCATE               VARCHAR(4)           not null,
   RUTPRO               VARCHAR(3)           not null,
   NOMPRO               VARCHAR(30)          not null,
   STOCK                INT8                 not null,
   constraint PK_PRODUCTO primary key (IDPRO)
);

/*==============================================================*/
/* Index: PRODUCTO_PK                                           */
/*==============================================================*/
create unique index PRODUCTO_PK on PRODUCTO (
IDPRO
);

/*==============================================================*/
/* Index: RELATIONSHIP_1_FK                                     */
/*==============================================================*/
create  index RELATIONSHIP_1_FK on PRODUCTO (
IDCATE
);

/*==============================================================*/
/* Index: RELATIONSHIP_2_FK                                     */
/*==============================================================*/
create  index RELATIONSHIP_2_FK on PRODUCTO (
RUTPRO
);

/*==============================================================*/
/* Table: PROVEEDOR                                             */
/*==============================================================*/
create table PROVEEDOR (
   RUTPRO               VARCHAR(3)           not null,
   NOMPRO               VARCHAR(30)          not null,
   TELPRO               INT8                 not null,
   PAGPRO               VARCHAR(50)          not null,
   constraint PK_PROVEEDOR primary key (RUTPRO)
);

/*==============================================================*/
/* Index: PROVEEDOR_PK                                          */
/*==============================================================*/
create unique index PROVEEDOR_PK on PROVEEDOR (
RUTPRO
);

/*==============================================================*/
/* Table: TELEFONO                                              */
/*==============================================================*/
create table TELEFONO (
   IDTEL                INT8                 not null,
   RUTCLI               VARCHAR(3)           not null,
   CODPAIS              VARCHAR(3)           not null,
   NUMEROTEL            VARCHAR(15)           not null,
   constraint PK_TELEFONO primary key (IDTEL)
);

/*==============================================================*/
/* Index: TELEFONO_PK                                           */
/*==============================================================*/
create unique index TELEFONO_PK on TELEFONO (
IDTEL
);

/*==============================================================*/
/* Index: RELATIONSHIP_8_FK                                     */
/*==============================================================*/
create  index RELATIONSHIP_8_FK on TELEFONO (
RUTCLI
);

/*==============================================================*/
/* Index: RELATIONSHIP_16_FK                                    */
/*==============================================================*/
create  index RELATIONSHIP_16_FK on TELEFONO (
CODPAIS
);

/*==============================================================*/
/* Table: VALORDIR                                              */
/*==============================================================*/
create table VALORDIR (
   IDPARDIRE            VARCHAR(4)           not null,
   IDDIR                INT8                 not null,
   VALOR                INT2                 not null,
   constraint PK_VALORDIR primary key (IDPARDIRE, IDDIR)
);

/*==============================================================*/
/* Index: VALORDIR_PK                                           */
/*==============================================================*/
create unique index VALORDIR_PK on VALORDIR (
IDPARDIRE,
IDDIR
);

/*==============================================================*/
/* Index: RELATIONSHIP_11_FK                                    */
/*==============================================================*/
create  index RELATIONSHIP_11_FK on VALORDIR (
IDDIR
);

/*==============================================================*/
/* Index: RELATIONSHIP_12_FK                                    */
/*==============================================================*/
create  index RELATIONSHIP_12_FK on VALORDIR (
IDPARDIRE
);

/*==============================================================*/
/* Table: VENTA                                                 */
/*==============================================================*/
create table VENTA (
   NOVENTA              INT8                 not null,
   CODEMPLEADO          VARCHAR(4)           not null,
   RUTCLI               VARCHAR(3)           not null,
   FECVENTA             DATE                 not null,
   constraint PK_VENTA primary key (NOVENTA)
);

/*==============================================================*/
/* Index: VENTA_PK                                              */
/*==============================================================*/
create unique index VENTA_PK on VENTA (
NOVENTA
);

/*==============================================================*/
/* Index: RELATIONSHIP_5_FK                                     */
/*==============================================================*/
create  index RELATIONSHIP_5_FK on VENTA (
CODEMPLEADO
);

/*==============================================================*/
/* Index: RELATIONSHIP_7_FK                                     */
/*==============================================================*/
create  index RELATIONSHIP_7_FK on VENTA (
RUTCLI
);

alter table BARRIO
   add constraint FK_BARRIO_RELATIONS_CIUDAD foreign key (CODPAIS, CODCIUDAD)
      references CIUDAD (CODPAIS, CODCIUDAD)
      on delete restrict on update restrict;

alter table CIUDAD
   add constraint FK_CIUDAD_RELATIONS_PAIS foreign key (CODPAIS)
      references PAIS (CODPAIS)
      on delete restrict on update restrict;

alter table DETALLEVENTA
   add constraint FK_DETALLEV_RELATIONS_PRODUCTO foreign key (IDPRO)
      references PRODUCTO (IDPRO)
      on delete restrict on update restrict;

alter table DETALLEVENTA
   add constraint FK_DETALLEV_RELATIONS_VENTA foreign key (NOVENTA)
      references VENTA (NOVENTA)
      on delete restrict on update restrict;

alter table DIRECCION
   add constraint FK_DIRECCIO_RELATIONS_CLIENTE foreign key (RUTCLI)
      references CLIENTE (RUTCLI)
      on delete restrict on update restrict;

alter table DIRECCION
   add constraint FK_DIRECCIO_RELATIONS_BARRIO foreign key (CODBARRIO)
      references BARRIO (CODBARRIO)
      on delete restrict on update restrict;

alter table DIRECCION
   add constraint FK_DIRECCIO_RELATIONS_PROVEEDO foreign key (RUTPRO)
      references PROVEEDOR (RUTPRO)
      on delete restrict on update restrict;

alter table PRECIO
   add constraint FK_PRECIO_RELATIONS_PRODUCTO foreign key (IDPRO)
      references PRODUCTO (IDPRO)
      on delete restrict on update restrict;

alter table PRODUCTO
   add constraint FK_PRODUCTO_RELATIONS_CATEGORI foreign key (IDCATE)
      references CATEGORIA (IDCATE)
      on delete restrict on update restrict;

alter table PRODUCTO
   add constraint FK_PRODUCTO_RELATIONS_PROVEEDO foreign key (RUTPRO)
      references PROVEEDOR (RUTPRO)
      on delete restrict on update restrict;

alter table TELEFONO
   add constraint FK_TELEFONO_RELATIONS_PAIS foreign key (CODPAIS)
      references PAIS (CODPAIS)
      on delete restrict on update restrict;

alter table TELEFONO
   add constraint FK_TELEFONO_RELATIONS_CLIENTE foreign key (RUTCLI)
      references CLIENTE (RUTCLI)
      on delete restrict on update restrict;

alter table VALORDIR
   add constraint FK_VALORDIR_RELATIONS_DIRECCIO foreign key (IDDIR)
      references DIRECCION (IDDIR)
      on delete restrict on update restrict;

alter table VALORDIR
   add constraint FK_VALORDIR_RELATIONS_PARTEDIR foreign key (IDPARDIRE)
      references PARTEDIR (IDPARDIRE)
      on delete restrict on update restrict;

alter table VENTA
   add constraint FK_VENTA_RELATIONS_EMPLEADO foreign key (CODEMPLEADO)
      references EMPLEADO (CODEMPLEADO)
      on delete restrict on update restrict;

alter table VENTA
   add constraint FK_VENTA_RELATIONS_CLIENTE foreign key (RUTCLI)
      references CLIENTE (RUTCLI)
      on delete restrict on update restrict;

