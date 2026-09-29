# -*- coding: utf-8 -*-
"""Gera as duas saidas a partir da fonte unica.

    python3 build.py

  fonte.html + marca.svg  ->  sabonaria.html        (versao artifact do claude.ai)
                          ->  sabonaria-site/       (o que vai para o Cloudflare Pages)

Com --icones, tambem regera icone.svg e os PNGs a partir da marca
(precisa de playwright: python3 build.py --icones).
"""
import io, os, re, shutil, sys

fonte = io.open('fonte.html', encoding='utf-8').read()
marca = io.open('marca.svg', encoding='utf-8').read()
if '__MARCA_SVG__' not in fonte:
    sys.exit('fonte.html nao tem o marcador __MARCA_SVG__')
saida = fonte.replace('__MARCA_SVG__', marca)

io.open('sabonaria.html', 'w', encoding='utf-8').write(saida)

i = saida.index('<div class="marca">')
cab = io.open('cabeca.html', encoding='utf-8').read()
if not os.path.isdir('sabonaria-site'):
    os.mkdir('sabonaria-site')
io.open('sabonaria-site/index.html', 'w', encoding='utf-8').write(
    cab + saida[:i] + '</head>\n<body>\n' + saida[i:] + '\n</body>\n</html>\n')
for f in ('icon-180.png', 'icon-192.png', 'icon-512.png', 'manifest.webmanifest'):
    shutil.copy(f, 'sabonaria-site/' + f)

print('artifact: %d KB | site: %d KB' % (
    len(saida) // 1024, os.path.getsize('sabonaria-site/index.html') // 1024))


def icones():
    """Refaz icone.svg e os PNGs: raios + sol + barco, sem a agua e sem o nome."""
    s = marca[:marca.index('<g id="nome"')] + '</svg>'
    a = s.index('<path id="agua"')
    s = s[:a] + s[s.index('/><', a) + 2:]
    vb = '108 200 1285 1285'
    s = re.sub(r'<svg[^>]*>',
               '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"'
               ' viewBox="%s" fill="#26221F">' % vb, s, count=1)
    p = vb.split()
    s = s.replace('</defs>', '</defs><rect x="%s" y="%s" width="%s" height="%s" fill="#F2EEE9"/>'
                  % tuple(p), 1)
    io.open('icone.svg', 'w', encoding='utf-8').write(s)
    io.open('.icone-prev.html', 'w', encoding='utf-8').write(
        '<!doctype html><meta charset=utf-8>'
        '<style>html,body{margin:0;padding:0}svg{display:block;width:100vw;height:100vh}</style>' + s)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        for n in (512, 192, 180):
            pg = b.new_page(viewport={'width': n, 'height': n})
            pg.goto('file://' + os.path.abspath('.icone-prev.html'))
            pg.wait_for_timeout(400)
            pg.screenshot(path='icon-%d.png' % n)
            pg.close()
        b.close()
    os.remove('.icone-prev.html')
    print('icones refeitos')


if '--icones' in sys.argv:
    icones()
