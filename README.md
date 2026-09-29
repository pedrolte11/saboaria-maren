# Saboaria Maren

Calculadora de custo e preço dos sabonetes artesanais do **Maren Ateliê**.
Site estático, sem framework e sem servidor.

No ar: <https://saboaria-maren.pages.dev>

## Arquivos

| Arquivo | O que é |
|---|---|
| `fonte.html` | **A fonte única.** Todo o CSS, HTML e JavaScript do app. O logo entra no lugar do marcador `__MARCA_SVG__`. É o único arquivo que se edita à mão. |
| `marca.svg` | O logo do Maren Ateliê, em vetor, com os grupos animáveis (`agua`, `sol`, `raios`, `barco`, `nome`). Praticamente nunca muda. |
| `cabeca.html` | O `<head>` do site publicado (meta tags, manifest, ícones). |
| `build.mjs` | Build em Node. **É este que o Cloudflare Pages roda.** |
| `build.py` | Mesmo build em Python, para rodar na mão. Com `--icones`, regera `icone.svg` e os PNGs a partir da marca (precisa de playwright). |
| `icon-180/192/512.png` | Ícones do PWA, derivados da marca. |
| `manifest.webmanifest` | Manifesto do PWA. |

Saídas do build (não versionadas):

- `sabonaria-site/` — o que vai para o ar.
- `sabonaria.html` — versão para o artifact do claude.ai, sem `<head>` próprio.

## Como gerar

```bash
node build.mjs      # ou: python3 build.py
```

Sem dependências nos dois casos. Os dois geram bytes idênticos.

## Publicação

O Cloudflare Pages está ligado neste repositório:

- **Comando de build:** `node build.mjs`
- **Diretório de saída:** `sabonaria-site`

Cada push na `main` publica sozinho.

## Como os dados da usuária funcionam

Ficam no **localStorage** do navegador, na chave `saboaria.v1`, mais uma cópia
automática num arquivo `.json` que ela escolhe (File System Access API) — a
orientação é salvar dentro da pasta do Google Drive ou do OneDrive.

**localStorage é por endereço.** Trocar o domínio do site significa exportar o
backup no endereço antigo e restaurar no novo.

## Regras de cálculo, em uma linha cada

- **Custo por grama:** `(ingredientes + trabalho do lote) ÷ peso total da massa`.
- **Custo de um sabonete:** `custo por grama × peso dele + embalagem individual + trabalho por unidade`.
- A massa é rateada **por peso** entre os formatos; a embalagem é por formato.
- **Preço:** `custo × (1 + x/100)` no modo "% sobre o custo", ou `custo × x` no modo "multiplicar".
- **Kit:** soma dos itens (cada sabonete entra pelo custo cheio dele) + trabalho de
  montagem; o preço segue a mesma regra acima.

## Histórico

- **ago/2026** — primeira versão: formatos múltiplos por massa, marca e animação do logo, modo escuro.
- **set/2026** — estoque, rastreio de lote, lote proporcional, ordenação da despensa.
- **set/2026** — migração do Netlify para o Cloudflare Pages.
- **29/set/2026** — entra a aba **Kits**; saem **Estoque** e **Proporcional** a pedido da usuária.
  O código dessas duas telas continua no arquivo, sem chamada, e os dados antigos
  (`insumo.estoque`, `receita.produzida`, `receita.consumido`) seguem intactos no backup.
