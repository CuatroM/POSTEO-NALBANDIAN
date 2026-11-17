# Posteo automático en Instagram — Alexis Nalbandian

Publica en el Instagram de **Alexis Nalbandian**, por la API oficial de Meta, los posts que se cargan
en la carpeta `posts/`. Es la misma conexión que POSTEO-CLABUTOR, pero con su propia cuenta y
sus propios secretos: no se mezcla con Clabutor.

## Bases de datos
- **SINCRO PRODUCTOS FEMA BASE:** el proceso *Actualizar productos FEMA* lee de BaseLinker
  (solo lectura) costo y stock de INVENTARIO COMPLETO FEMA 2026 MATIAS y los guarda en
  `datos/productos_fema.csv`. Corre todos los días a las 7:20 (Argentina) o a mano.
- **FRASES COMERCIALES INDUSTRIA:** `frases/FRASES-COMERCIALES-INDUSTRIA.md`.

## Cómo cargar un post
1. Dentro de `posts/` creá una carpeta por post, con la fecha a partir de la cual se puede publicar: `2026-11-20-amoladora`.
2. Adentro:
   - **Post simple:** una imagen `.jpg`.
   - **Carrusel:** de 2 a 10 `.jpg`, en orden alfabético (`1.jpg`, `2.jpg`, ...).
   - **Reel:** un video `.mp4`.
   - **Historias:** si el nombre de la carpeta contiene `historia`, cada `.jpg` (1080×1920) se publica como historia.
   - **`texto.txt`:** texto del post con hashtags (máx. 2200 caracteres).
3. Commit. Listo.

Las carpetas que empiezan con `_` se ignoran. Las publicadas quedan en `publicados.txt`.

## Cuándo publica
- **Automático:** lunes, miércoles y viernes a las 10:00 (Argentina), un post por vez.
- **A mano:** *Actions* → *Publicar en Instagram* → *Run workflow* (con o sin nombre de carpeta).

## Secretos (Settings → Secrets and variables → Actions)

| Nombre | Valor |
| --- | --- |
| `IG_TOKEN` | Token de **página** de Facebook (empieza con `EAA`) de la página vinculada al Instagram de Alexis Nalbandian. No vence si sale de un token de usuario de larga duración. |
| `IG_USER_ID` | ID de la cuenta de Instagram. Si no lo sabés, poné cualquier número: el primer *Run workflow* lo muestra en el log ("cuenta de Instagram disponible: IG_USER_ID=…"). |
| `BL_TOKEN` | Token de API de BaseLinker (el mismo de sync-baselinker). |
| `GH_PAT` | Solo si se usa un token de Instagram (`IGAA…`), para renovarlo. Con token de página no hace falta. |

### Sacar el token de página
1. En la app de Meta (developers.facebook.com → tu app → *Herramientas* → *Explorador de la API Graph*),
   elegí la app, **Obtener token de acceso de usuario** con los permisos
   `instagram_basic`, `instagram_content_publish`, `pages_show_list`, `pages_read_engagement`, `business_management`,
   iniciando sesión con el Facebook que administra la página de Alexis Nalbandian.
2. Pasalo a larga duración en el *Depurador de tokens* → **Extender token de acceso**.
3. Con ese token, en el Explorador consultá `me/accounts`: el `access_token` de la página de Alexis Nalbandian es el `IG_TOKEN`.
