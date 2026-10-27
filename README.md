# Web de AGENT-SAM (estilo AIM-Zero)

Sitio estático de 6 páginas en español (raíz) y en inglés (`/en/`): Inicio, Equipo, Trabajo, Resultados, Participa y Prensa.
Diseño claro, sin degradados, con ilustraciones propias en SVG. Sin JavaScript.

## Publicar en GitHub Pages (mientras llega el servidor)

El repositorio incluye `.github/workflows/pages.yml`: en cada cambio en la rama `main`, GitHub genera la web y la publica. No hace falta subir `dist/`.

1. Crea un repositorio **público** en GitHub (por ejemplo `agent-sam`).
2. **Antes de subir nada**: Settings → Pages → Build and deployment → Source: **GitHub Actions**.
3. Sube este contenido a la rama `main`. Comprueba que se ha subido la carpeta oculta `.github/`.
4. En la pestaña **Actions**, espera a que termine «Publicar web» (unos 3 minutos). La web queda en `https://USUARIO.github.io/agent-sam/`.

Email de contacto: por defecto `jamal@uma.es`; se cambia en Settings → Secrets and variables → Actions → Variables → `CONTACT_EMAIL`.

**Cuando la web esté en agent-sam.uma.es**, evita tener dos copias indexadas: o bien desactiva Pages (Settings → Pages → Unpublish), o bien apunta el dominio a GitHub (Custom domain `agent-sam.uma.es` + registro DNS `CNAME` a `USUARIO.github.io`) y no uses el servidor. Las URL canónicas se ajustan solas al dominio que configure GitHub.

## Publicar en https://agent-sam.uma.es (servidor propio)

1. **Quitar la redirección actual.** Hoy `agent-sam.uma.es` responde con una redirección temporal (302) a la web de AIM-Zero. Hay que eliminarla en el servidor antes de subir esta web; si se mantiene, Google trata el dominio como un alias de otro proyecto.
2. Sube el contenido de `dist/` (incluido el archivo oculto `.htaccess`) a la raíz del sitio.
3. Comprueba que `https://agent-sam.uma.es/en/` carga, que `https://agent-sam.uma.es/no-existe` muestra la página 404 y que `http://` redirige a `https://`.
4. En **Google Search Console** añade la propiedad, verifica el dominio, envía `https://agent-sam.uma.es/sitemap.xml` y solicita la indexación de la portada y de `/en/`. Haz lo mismo en **Bing Webmaster Tools**.
5. Valida los datos estructurados de la portada y de `equipo.html` con la [Prueba de resultados enriquecidos](https://search.google.com/test/rich-results).

`.htaccess` (Apache) fuerza HTTPS y el dominio canónico, redirige `index.html` a la URL limpia, activa la compresión y la caché, y sirve la página 404. Si el servidor es **nginx**, pide a informática el equivalente:

```nginx
error_page 404 /404.html;
location = /index.html    { return 301 /; }
location = /en/index.html { return 301 /en/; }
gzip on; gzip_types text/css image/svg+xml application/xml application/manifest+json;
location ~* \.(svg|png|jpe?g|webp)$ { add_header Cache-Control "public, max-age=2592000"; }
```

## Para seguir mejorando el posicionamiento

- **Enlaces entrantes**: enlazad la web desde la página del grupo NEO, la ficha del proyecto en la UMA, ITIS Software, los perfiles de Google Scholar/ORCID del equipo, y una nota de prensa de la UMA.
- **Perfiles del equipo**: si añadís ORCID o Google Scholar de cada persona, se pueden incluir en los datos estructurados (`sameAs`), lo que ayuda a que Google asocie a cada investigador con el proyecto.
- **Contenido nuevo**: cada publicación, tesis o taller merece su entrada; las páginas con contenido real son las que captan búsquedas como «caminos escolares seguros» o «calor y movilidad».

## Generar

```bash
pip install jinja2 pillow playwright
python3 build.py --site-url https://EL-DOMINIO-REAL --email contacto@uma.es
```

Sube el contenido de `dist/` a la raíz del dominio.. Después, en Google Search Console, envía `https://DOMINIO/sitemap.xml`.

`--file-links` genera enlaces del tipo `index.html` en lugar de URLs limpias. Úsalo solo para previsualizar en servicios que no resuelven carpetas.

## Dónde se edita cada cosa

| Qué | Dónde |
|---|---|
| Todos los textos (es/en), títulos SEO, equipo, entregables, ofertas | `content.py` |
| Estructura y estilos | `templates/base.html` (común) y una plantilla por página |
| Ilustraciones | `illus.py` (se generan como SVG en `dist/img/`) |
| Fotos del equipo | `assets/team/<clave>.jpg` (cuadradas); la clave se indica en `TEAM` dentro de `content.py` |
| Logotipos | `assets/logos/` |

### Tareas habituales

- **Añadir una foto**: guarda `assets/team/alba.jpg` y cambia `None` por `"alba"` en la fila de Enrique Alba en `TEAM`.
- **Publicar un artículo**: hoy la página de resultados muestra «Aún no hay elementos publicados». Añade los elementos en `RESULTS`/`templates/results.html`, o pídeselo a Claude.
- **Abrir la convocatoria FPI**: cambia la etiqueta en `PARTICIPATE` → `fpi` → `tag` a `("Abierta", "open")` y añade el enlace a la convocatoria.
- **Sustituir una ilustración por una foto o imagen propia**: guarda el archivo en `dist/img/` con el mismo nombre (por ejemplo `t1-1.png`) y cambia la extensión en la plantilla.

## Financiación (obligatorio)

La referencia y los logotipos de MICIU y AEI aparecen arriba en todas las páginas, visibles sin desplazarse, y en el pie. El logotipo es el mismo que usa la web de AIM-Zero. Comprueba en vuestra resolución de concesión si hay que añadir «y por FEDER, UE» y el logotipo de la UE; en ese caso, edita `funding_text` en `content.py` y sustituye `assets/logos/logo-miciu-aei.png`.

## Logotipos de las instituciones (página de equipo)

Están en `assets/logos/partners/` y se configuran en `PARTNER_LOGOS` (`content.py`): archivo, altura mostrada, nombre y web.

| Logo | Origen | Licencia |
|---|---|---|
| Universidad de Málaga | Web de AIM-Zero (grupo NEO) | Logotipo institucional |
| MIT | Wikimedia Commons, «MIT Logo and Wordmark.svg» | Dominio público |
| Universidad de la República | Wikimedia Commons, «Logo UDELAR.png» | Dominio público |
| CONICET | Wikimedia Commons, «CONICET logo con letras.svg» | CC BY 2.5 AR |
| UNPA | Wikimedia Commons, «Unpa-logo.svg» | CC0 |
| Ministerio de Derechos Sociales, Consumo y Agenda 2030 | Wikimedia Commons | Dominio público |

Son marcas de cada institución: se usan para identificar a las entidades participantes. Si alguna institución os facilita su logotipo oficial en alta resolución, basta con sustituir el archivo con el mismo nombre.

## Fotos del equipo

Están en `assets/team/` (cuadradas, centradas en la cara). Origen de las incorporadas el 22/10/2026: perfil del grupo ALFA (MIT) para Una-May O’Reilly, MIT CSAIL Alliances para Erik Hemberg, ITIS Software (UMA) para Sergio Nesmachnow, LinkedIn para Ana Carolina Olivera y Agenda Pública para Irene Lebrusán. Conviene confirmar con cada persona que está conforme con la foto. La de Enrique Alba la facilitó el investigador principal.
