#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera la web de AGENT-SAM (estilo AIM-Zero) en ./dist

    python3 build.py --site-url https://DOMINIO --email contacto@uma.es

Opciones:
    --file-links   enlaces con nombre de archivo (index.html) en vez de URLs limpias;
                   útil para previsualizar en servicios que no resuelven carpetas.
Requiere: Python 3.9+, jinja2, Pillow y Playwright (solo para rasterizar
la imagen social y el favicon).
"""
import argparse
import datetime as dt
import json
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from PIL import Image

import content as C
import illus

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
ASSETS = ROOT / "assets"
MONTHS_ES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def warn(m):
    print("  ⚠ ", m)


def initials(name):
    parts = [p for p in name.replace("Prof.", "").replace("Dra.", "").replace("Dr.", "").split() if p[:1].isupper()]
    return (parts[0][0] + parts[-1][0]) if len(parts) > 1 else parts[0][0]


def page_files(lang):
    return {k: (es if lang == "es" else en) for k, es, en in C.PAGES}


def public_url(site, lang, key):
    f = page_files(lang)[key]
    prefix = "/" if lang == "es" else "/en/"
    return site + prefix + ("" if f == "index.html" else f)


def jsonld(lang, key, site, url_self, seo_title, seo_desc, updated_iso, email):
    c = C.COMMON[lang]
    page = {"@type": "WebPage", "@id": url_self + "#webpage", "url": url_self, "name": seo_title, "description": seo_desc,
            "inLanguage": lang, "isPartOf": {"@id": site + "/#website"}, "about": {"@id": site + "/#project"}, "dateModified": updated_iso}
    graph = [page]
    if key != "home":
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": c["nav"]["home"], "item": public_url(site, lang, "home")},
            {"@type": "ListItem", "position": 2, "name": c["nav"][key], "item": url_self}]})
    if key == "home":
        uma = {"@type": "CollegeOrUniversity", "@id": site + "/#uma", "name": "Universidad de Málaga", "url": "https://www.uma.es/"}
        neo = {"@type": "ResearchOrganization", "@id": site + "/#neo", "name": "NEO — Networking and Emerging Optimization", "url": "https://neo.lcc.uma.es/", "parentOrganization": {"@id": site + "/#uma"}}
        aei = {"@type": "GovernmentOrganization", "@id": site + "/#aei", "name": "Agencia Estatal de Investigación", "url": "https://www.aei.gob.es/"}
        miciu = {"@type": "GovernmentOrganization", "@id": site + "/#miciu", "name": "Ministerio de Ciencia, Innovación y Universidades", "url": "https://www.ciencia.gob.es/"}
        aff = {"uma": {"@id": site + "/#neo"}, "mit": {"@type": "ResearchOrganization", "name": "MIT CSAIL"},
               "udelar": {"@type": "CollegeOrUniversity", "name": "Universidad de la República"},
               "uncuyo": {"@type": "ResearchOrganization", "name": "ICB CONICET – UNCuyo"},
               "unpa": {"@type": "CollegeOrUniversity", "name": "Universidad Nacional de la Patagonia Austral – UACO"},
               "social": {"@type": "GovernmentOrganization", "name": "Ministerio de Derechos Sociales, Consumo y Agenda 2030"}}
        pi = {"@type": "Person", "@id": site + "/#pi", "name": "Jamal Toutouh El Alamin", "affiliation": {"@id": site + "/#neo"},
              "jobTitle": "Investigador principal" if lang == "es" else "Principal investigator", "image": site + "/img/team/toutouh.jpg", "url": "https://www.jamal.es/", "sameAs": ["https://www.jamal.es/"]}
        project = {"@type": "ResearchProject", "@id": site + "/#project", "name": "AGENT-SAM",
                   "alternateName": ["Agentic Generative Evolutionary Networks for Safe and Active Mobility", "Redes Evolutivas Generativas Agénticas para una Movilidad Segura y Activa"],
                   "identifier": C.PROJECT_ID, "description": seo_desc, "url": public_url(site, lang, "home"), "logo": site + "/apple-touch-icon.png",
                   "parentOrganization": {"@id": site + "/#neo"}, "funder": [{"@id": site + "/#aei"}, {"@id": site + "/#miciu"}],
                   "funding": {"@type": "MonetaryGrant", "identifier": C.PROJECT_ID, "funder": {"@id": site + "/#aei"},
                               "amount": {"@type": "MonetaryAmount", "value": C.FUNDING_EUR, "currency": "EUR"}},
                   "areaServed": [{"@type": "City", "name": "Málaga"}, {"@type": "City", "name": "Melilla"}],
                   "founder": {"@id": site + "/#pi"},
                   "member": [pi] + [{"@type": "Person", "name": n, "affiliation": aff[g]} for _, n, _, _, g in C.TEAM]}
        if email:
            project["email"] = email
        site_node = {"@type": "WebSite", "@id": site + "/#website", "url": site + "/", "name": "AGENT-SAM", "inLanguage": ["es", "en"], "publisher": {"@id": site + "/#uma"}}
        graph += [site_node, project, uma, neo, aei, miciu]
    if key == "team":
        aff_names = {"uma": "Universidad de Málaga", "mit": "MIT CSAIL", "udelar": "Universidad de la República",
                     "uncuyo": "ICB CONICET – UNCuyo", "unpa": "Universidad Nacional de la Patagonia Austral – UACO",
                     "social": "Ministerio de Derechos Sociales, Consumo y Agenda 2030"}
        people = [{"@type": "Person", "@id": site + "/#pi", "name": "Jamal Toutouh El Alamin",
                   "jobTitle": "Investigador principal" if lang == "es" else "Principal investigator",
                   "image": site + "/img/team/toutouh.jpg", "url": "https://www.jamal.es/", "sameAs": ["https://www.jamal.es/"], "affiliation": {"@type": "CollegeOrUniversity", "name": "Universidad de Málaga"},
                   "memberOf": {"@id": site + "/#project"}}]
        for photo, n, _, _, g in C.TEAM:
            node = {"@type": "Person", "name": n, "affiliation": {"@type": "Organization", "name": aff_names[g]}, "memberOf": {"@id": site + "/#project"}}
            if photo:
                node["image"] = f"{site}/img/team/{photo}.jpg"
            people.append(node)
        page["mainEntity"] = {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": pp} for i, pp in enumerate(people)]}
    if key == "press":
        graph.append({"@type": "FAQPage", "inLanguage": lang, "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in C.PRESS[lang]["faq"]]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def rasterize(dist):
    """Imagen para redes sociales y favicons a partir de los SVG (Playwright)."""
    from playwright.sync_api import sync_playwright
    hero = (dist / "img/hero.svg").read_text(encoding="utf-8")
    logo = illus.logo_mark(64)
    cards = {
        "es": ("Caminos escolares seguros frente al cambio climático", "Inteligencia artificial para que ir al colegio, al campus o al centro de salud siga siendo seguro con calor, inundaciones y contaminación."),
        "en": ("Climate-safe routes to school, campus and care", "Artificial intelligence to keep everyday trips safe in heat waves, floods and pollution."),
    }
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        for lang, (title, sub) in cards.items():
            pg.set_content(f"""<html><body style="margin:0;width:1200px;height:630px;background:#F4F7F6;font-family:'DejaVu Sans',Arial,sans-serif">
            <div style="position:absolute;inset:28px;background:#fff;border:2px solid #DCE7E4;border-radius:28px;display:flex;align-items:center;gap:32px;padding:36px;box-sizing:border-box">
              <div style="flex:1">
                <div style="display:flex;align-items:center;gap:14px;margin-bottom:26px">{logo}<span style="font-weight:700;font-size:34px;color:#14212A">AGENT-SAM</span></div>
                <div style="font-weight:700;font-size:44px;line-height:1.15;color:#0B6E69">{title}</div>
                <div style="font-size:22px;line-height:1.4;color:#55626B;margin-top:16px">{sub}</div>
                <div style="margin-top:22px;font-size:17px;color:#55626B">PID2025-174277OA-I00 · Universidad de Málaga</div>
              </div>
              <div style="width:520px;border-radius:20px;overflow:hidden;border:1px solid #E5ECEA">{hero.replace('width="720" height="480"', 'width="520" height="347"')}</div>
            </div></body></html>""")
            pg.screenshot(path=str(dist / f"img/og-{lang}.png"))
        for size, name in ((180, "apple-touch-icon.png"), (32, "favicon-32.png")):
            pg.set_viewport_size({"width": size, "height": size})
            pg.set_content(f'<html><body style="margin:0;background:#fff">{illus.logo_mark(size)}</body></html>')
            pg.screenshot(path=str(dist / name), omit_background=False)
        b.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site-url", default="https://agent-sam.uma.es")
    ap.add_argument("--email", default="")
    ap.add_argument("--file-links", action="store_true")
    ap.add_argument("--cname", default="", help="dominio propio para GitHub Pages (crea dist/CNAME)")
    a = ap.parse_args()
    site = a.site_url.rstrip("/")
    # Ruta base (p. ej. /agent-sam en https://usuario.github.io/agent-sam): la usan la 404 y el manifiesto
    from urllib.parse import urlparse
    root = urlparse(site).path.rstrip("/") + "/"
    print("Construyendo para", site)
    if "agent-sam.uma.es" in site:
        warn("dominio de ejemplo: usa --site-url con el dominio real")
    if not a.email:
        warn("sin email de contacto: los botones de contacto no se mostrarán (--email)")

    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "img/team").mkdir(parents=True)
    (DIST / "en").mkdir()

    # Ilustraciones
    for k, f in illus.ALL.items():
        (DIST / f"img/{k}.svg").write_text(f(), encoding="utf-8")
    (DIST / "favicon.svg").write_text(illus.logo_mark(), encoding="utf-8")

    # Logotipos (2x la altura mostrada)
    def logo(src, out, h):
        im = Image.open(ASSETS / "logos" / src)
        im = im.convert("RGBA")
        w = round(im.width * h / im.height)
        im = im.resize((w, h), Image.LANCZOS)
        im.quantize(colors=96, method=Image.Quantize.FASTOCTREE).save(DIST / "img" / out, optimize=True)
    logo("logo-miciu-aei.png", "logo-miciu-aei.png", 68)
    logo("logo-uma.png", "logo-uma.png", 68)
    logo("logo-neo.png", "logo-neo.png", 68)

    # Logotipos de las instituciones participantes
    (DIST / "img/partners").mkdir(parents=True, exist_ok=True)
    logo_w = {}
    for k, *_ in C.PARTNER_LOGOS:
        src = ASSETS / "logos/partners" / f"{k}.png"
        shutil.copy(src, DIST / "img/partners" / f"{k}.png")
        logo_w[k] = Image.open(src).width

    # Fotos
    pi = Image.open(ASSETS / "team/toutouh.jpg").convert("RGB")
    pi.save(DIST / "img/team/toutouh.jpg", quality=82, optimize=True, progressive=True)
    pi.save(DIST / "img/team/toutouh.webp", quality=80, method=6)
    for photo, *_ in C.TEAM:
        if photo:
            Image.open(ASSETS / f"team/{photo}.jpg").convert("RGB").resize((192, 192), Image.LANCZOS).save(DIST / f"img/team/{photo}.jpg", quality=82, optimize=True)

    rasterize(DIST)

    env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=False, trim_blocks=True, lstrip_blocks=True)
    env.globals["initials"] = initials
    today = dt.date.today()
    data = {"home": C.HOME, "team": C.TEAM_PAGE, "work": C.WORK, "results": C.RESULTS, "participate": C.PARTICIPATE, "press": C.PRESS}

    for lang in ("es", "en"):
        files = page_files(lang)
        other = "en" if lang == "es" else "es"
        ofiles = page_files(other)
        base = "" if lang == "es" else "../"

        def href(key, _f=files):
            f = _f[key]
            return f if (a.file_links or f != "index.html") else "./"

        for key in files:
            title, desc = C.SEO[lang][key]
            if len(title) > 65:
                warn(f"[{lang}/{key}] título largo ({len(title)})")
            if not 110 <= len(desc) <= 165:
                warn(f"[{lang}/{key}] descripción de {len(desc)} caracteres")
            of = ofiles[key]
            if lang == "es":
                other_href = "en/" + ("" if (of == "index.html" and not a.file_links) else of)
            else:
                other_href = "../" + ("" if (of == "index.html" and not a.file_links) else of)
            url_self = public_url(site, lang, key)
            label = f"{today.day} de {MONTHS_ES[today.month - 1]} de {today.year}" if lang == "es" else today.strftime("%-d %B %Y")
            html = env.get_template(f"{key}.html").render(
                c=C.COMMON[lang], t=data[key][lang], page=key, pages=C.PAGES, team=C.TEAM, base=base, href=href,
                other_href=other_href, logo=illus.logo_mark(40), email=a.email,
                partner_logos=C.PARTNER_LOGOS, logo_w=logo_w, seo_title=title, seo_desc=desc, site_url=site, url_self=url_self, robots="index, follow, max-image-preview:large, max-snippet:-1", alt=C.ALT[lang],
                url_es=public_url(site, "es", key), url_en=public_url(site, "en", key),
                funding_text=C.COMMON[lang]["funding_text"].format(id=C.PROJECT_ID),
                jsonld=jsonld(lang, key, site, url_self, title, desc, today.isoformat(), a.email),
                year=today.year, updated_iso=today.isoformat(), updated_label=label,
            )
            out = DIST / ("" if lang == "es" else "en") / files[key]
            out.write_text(html, encoding="utf-8")

    # Página 404 (se sirve en cualquier ruta: enlaces absolutos desde la raíz)
    c404 = C.COMMON["es"]
    html = env.get_template("404.html").render(
        c=c404, t={}, page=None, pages=C.PAGES, team=C.TEAM, base=root, href=lambda k: root + ("" if page_files("es")[k] == "index.html" else page_files("es")[k]),
        other_href=root + "en/", logo=illus.logo_mark(40), email=a.email,
        seo_title=c404["notfound_title"] + " · AGENT-SAM", seo_desc=c404["notfound_text"], site_url=site, url_self=site + "/",
        url_es=site + "/", url_en=site + "/en/", robots="noindex, follow", alt={},
        funding_text=c404["funding_text"].format(id=C.PROJECT_ID),
        jsonld=json.dumps({"@context": "https://schema.org", "@type": "WebPage", "name": c404["notfound_title"]}, ensure_ascii=False),
        year=today.year, updated_iso=today.isoformat(), updated_label=f"{today.day} de {MONTHS_ES[today.month - 1]} de {today.year}",
    )
    (DIST / "404.html").write_text(html, encoding="utf-8")

    (DIST / "site.webmanifest").write_text(json.dumps({
        "name": "AGENT-SAM", "short_name": "AGENT-SAM", "lang": "es", "start_url": root, "display": "browser",
        "background_color": "#F4F7F6", "theme_color": "#FFFFFF",
        "icons": [{"src": root + "apple-touch-icon.png", "sizes": "180x180", "type": "image/png"}, {"src": root + "favicon.svg", "sizes": "any", "type": "image/svg+xml"}],
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    host = site.split("://", 1)[1]
    (DIST / ".htaccess").write_text(f"""# Configuración para Apache (servidores de la UMA). Si el servidor no es Apache, este archivo se ignora.
# Ver README: el equivalente para nginx está allí.
Options -Indexes
DirectoryIndex index.html
ErrorDocument 404 /404.html
AddDefaultCharset utf-8
AddType image/svg+xml .svg
AddType application/manifest+json .webmanifest

<IfModule mod_rewrite.c>
  RewriteEngine On
  # Forzar HTTPS y el dominio canónico
  RewriteCond %{{HTTPS}} off [OR]
  RewriteCond %{{HTTP_HOST}} !^{host.replace('.', '\\.')}$ [NC]
  RewriteRule ^(.*)$ https://{host}/$1 [R=301,L]
  # /index.html y /en/index.html -> URL limpia (evita contenido duplicado)
  RewriteCond %{{THE_REQUEST}} \\s/+(en/)?index\\.html[\\s?] [NC]
  RewriteRule ^(en/)?index\\.html$ /$1 [R=301,L]
</IfModule>

<IfModule mod_headers.c>
  Header always set Strict-Transport-Security "max-age=31536000"
  Header always set X-Content-Type-Options "nosniff"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  <FilesMatch "\\.(svg|png|jpe?g|webp|ico)$">
    Header set Cache-Control "public, max-age=2592000"
  </FilesMatch>
  <FilesMatch "\\.(html|xml|txt|webmanifest)$">
    Header set Cache-Control "public, max-age=3600"
  </FilesMatch>
</IfModule>

<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css text/plain text/xml application/xml image/svg+xml application/manifest+json application/ld+json
</IfModule>
""", encoding="utf-8")

    # GitHub Pages: sin Jekyll (sirve tal cual) y dominio propio opcional
    (DIST / ".nojekyll").write_text("", encoding="utf-8")
    if a.cname:
        (DIST / "CNAME").write_text(a.cname.strip() + "\n", encoding="utf-8")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {site}/sitemap.xml\n", encoding="utf-8")
    rows = []
    for key, _, _ in C.PAGES:
        alts = "".join(f'    <xhtml:link rel="alternate" hreflang="{h}" href="{public_url(site, l, key)}"/>\n' for h, l in (("es", "es"), ("en", "en"), ("x-default", "es")))
        for lang in ("es", "en"):
            rows.append(f"  <url>\n    <loc>{public_url(site, lang, key)}</loc>\n    <lastmod>{today.isoformat()}</lastmod>\n{alts}  </url>\n")
    (DIST / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "".join(rows) + "</urlset>\n", encoding="utf-8")
    print("Listo →", DIST)


if __name__ == "__main__":
    main()
