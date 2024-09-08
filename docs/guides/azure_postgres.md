# 📘 Guía: Configuración de una Base de Datos PostgreSQL en Azure

## Descripción

Esta guía proporciona instrucciones paso a paso para crear una base de datos PostgreSQL en Microsoft Azure, abarcando desde su configuración inicial hasta la conexión de la base de datos en un cliente PostgreSQL.

---

## 🛠️ Requisitos Previos

Antes de comenzar, asegúrate de tener lo siguiente:

- **Cuenta de Microsoft Azure** – Regístrate [aquí](https://azure.microsoft.com/es-es/free/) si aún no tienes una cuenta.
- **Cliente PostgreSQL** – Puede ser pgAdmin u otro cliente para gestionar bases de datos PostgreSQL.

---

## 🔑 Paso 1: Iniciar sesión en el Portal de Azure

1. Abre el [Portal de Azure](https://portal.azure.com/) en tu navegador.
2. Inicia sesión con tus credenciales de cuenta de Azure.

![login](https://github.com/user-attachments/assets/41f1324c-7050-4db9-9aa9-c1dbe981f0a8)

---

## 🗂️ Paso 2: Navegar a "*Crear una Base de Datos PostgreSQL*"

En el Portal de Azure, ve a **Crear un recurso** > **Bases de datos** > **Azure Database for PostgreSQL**.

![navegacion](https://github.com/user-attachments/assets/a368809e-f781-4cfb-b0f9-7526db20b83c)

---

## 🏗️ Paso 3: Crear una Base de Datos PostgreSQL

1. En la pantalla de **Crear Base de Datos PostgreSQL**, llena los siguientes detalles:
    - **Suscripción**: Selecciona tu suscripción.
    - **Grupo de Recursos**:
        - Si no tienes un grupo de recursos, haz clic en ***Crear nuevo*** y proporciona un nombre descriptivo.
        - Si ya tienes un grupo de recursos, selecciónalo del menú desplegable.
    - **Nombre del servidor**: Elige un nombre único global para tu servidor.
    - **Región**: Selecciona la región preferida (elige una cercana a ti para un mejor rendimiento).
    - **Versión**: Elige la versión de PostgreSQL (recomendado: 13 o superior).
    - **Tipo de carga de trabajo**: Elige *Desarrollo*
  
    ![first](https://github.com/user-attachments/assets/24b47df6-cdf4-431d-9ca4-624a38e8bfb2)
    
2. Ahora dirigete a la sección de **Configurar servidor**. Allí es recomendado ajustar las configuraciones a las siguientes:
    - **Compute tier**: Flexible, ideal para cargas de trabajo que no requieren un uso de CPU completo y continuo.
    - **Tamaño de proceso**: Standard_B1ms (1 núcleo virtual, 2 memoria GiB, 640 IOPS máxima).
    - **Nivel de rendimiento**: P6 (240 iops)
    
    ![configurar](https://github.com/user-attachments/assets/156d3cff-0c09-46cc-a414-722f636fcae9)
    
3. En *Autenticación*, escoge ***Autenticación de PostgreSQL*** como **Método de autenticación** y establece el **Nombre de Usuario Administrador** y la **Contraseña**.
4. Haz clic en **Siguiente: Redes >**.

---

## 🔒 Paso 4: Configurar las Reglas de Firewall

1. Una vez que estés en la sección de ***Redes*** dirigete a **Reglas de Firewall**.
2. Añade una nueva **Regla de Firewall** para permitir el acceso a tu base de datos:
    - **Nombre**: Asigna un nombre a la regla.
    - **IP de Inicio/IP de Finalización**: Puedes permitir el acceso desde tu IP actual o habilitar el acceso desde todas las IPs (*ten cuidado si permites acceso desde todas las IPs*).
3. Haz clic en **Revisar y Crear** y luego en ***Crear***.

![redes](https://github.com/user-attachments/assets/ef020cbc-d25a-4da6-bd1e-18046b2b1ec4)

---

## ⚙️ Paso 5: Conectar a la Base de Datos PostgreSQL

Puedes conectarte a la base de datos PostgreSQL usando tu cliente favorito (por ejemplo, pgAdmin o psql).

1. En tu cliente PostgreSQL, proporciona los siguientes detalles de conexión:
    - **Host**: El nombre del servidor (ej. `tu_servidor.postgres.database.azure.com`).
    - **Puerto**: 5432.
    - **Nombre de Usuario**: El nombre de usuario administrador (ej. `postgres`).
    - **Contraseña**: La contraseña que estableciste al crear la base de datos.
    - **Nombre de la Base de Datos**: `postgres` (*base de datos por defecto o cualquier otra que crees después*).
2. Prueba la conexión y empieza a gestionar tu base de datos PostgreSQL.

![pgadmin](https://github.com/user-attachments/assets/15177cbd-aa52-4bb7-9ebd-a508a3f5177d)

---

## 🎉 Conclusión

Has creado con éxito una base de datos PostgreSQL en Azure y te has conectado a ella utilizando un cliente PostgreSQL. Recuerda monitorear el rendimiento regularmente y gestionar los costos de manera eficiente.
