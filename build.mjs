// Mesmo build do build.py, em Node — é este que o Cloudflare Pages roda.
//   node build.mjs
// fonte.html + marca.svg -> sabonaria.html (artifact) e sabonaria-site/ (o site)
import { readFileSync, writeFileSync, mkdirSync, copyFileSync, statSync } from "node:fs";

const fonte = readFileSync("fonte.html", "utf8");
const marca = readFileSync("marca.svg", "utf8");
if (!fonte.includes("__MARCA_SVG__")) {
  console.error("fonte.html nao tem o marcador __MARCA_SVG__");
  process.exit(1);
}
const saida = fonte.replace("__MARCA_SVG__", () => marca);

writeFileSync("sabonaria.html", saida);

const i = saida.indexOf('<div class="marca">');
const cab = readFileSync("cabeca.html", "utf8");
mkdirSync("sabonaria-site", { recursive: true });
writeFileSync(
  "sabonaria-site/index.html",
  cab + saida.slice(0, i) + "</head>\n<body>\n" + saida.slice(i) + "\n</body>\n</html>\n"
);
for (const f of ["icon-180.png", "icon-192.png", "icon-512.png", "manifest.webmanifest"]) {
  copyFileSync(f, "sabonaria-site/" + f);
}
console.log(
  "artifact: " + Math.round(saida.length / 1024) + " KB | site: " +
  Math.round(statSync("sabonaria-site/index.html").size / 1024) + " KB"
);
