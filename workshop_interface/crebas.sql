/*==============================================================*/
/* DBMS name:      PostgreSQL 8                                 */
/* Created on:     25/01/2025 6:53:43 p. m.                     */
/*==============================================================*/


drop index EMPLEADO_PK;

drop table EMPLEADO;

/*==============================================================*/
/* Table: EMPLEADO                                              */
/*==============================================================*/
create table EMPLEADO (
   CODEMPLEADO          VARCHAR(4)           not null,
   NOMEMPLEADO          VARCHAR(30)          not null,
   APELLEMPLEADO        VARCHAR(30)          not null,
   "USER"               VARCHAR(5)           not null,
   PASSWORD             VARCHAR(5)           not null,
   constraint PK_EMPLEADO primary key (CODEMPLEADO)
);

/*==============================================================*/
/* Index: EMPLEADO_PK                                           */
/*==============================================================*/
create unique index EMPLEADO_PK on EMPLEADO (
CODEMPLEADO
);

