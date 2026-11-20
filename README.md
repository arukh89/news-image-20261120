# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image summing up the world news of Friday 20 November 2026: Cyclone Akvan
makes landfall near Gopalpur, Odisha (300,000+ evacuated); COP31 closes in
Antalya; New Zealand reach 317–6 at lunch on day two in Wellington; World
Children's Day; Prabowo meets Xi in Shenzhen; Anthropic's record IPO is due to
close — plus a schematic world map, a numbers band and an eight-item "Also
today" index. Every shape and letter is drawn from code; no photograph or
downloaded artwork is used.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

That writes `out/entry.png`, a 1024 by 1024 PNG. To redraw the poster from
scratch, run `python3 render.py` (needs Pillow, build time only); it rewrites
`entry.png` in this directory. The grader runs only `main.py`, which copies the
committed image with the standard library alone, so two runs always write the
same bytes.

## Stories in the image (all verified as 20 November 2026)

- **Lead — Cyclone Akvan, Odisha:** Severe Cyclonic Storm Akvan crosses the
  coast near Gopalpur around noon IST (06:30 UTC), winds 90–100 km/h gusting
  to 110; 300,000+ evacuated, 423 rescue teams, 69 trains cancelled
  (India Meteorological Department bulletins; live updates, 20 Nov).
- **COP31 closes, Antalya:** final day for ~200 countries; fossil fuels and
  adaptation finance still unresolved, no major breakthrough expected (AFP).
- **Cricket, Wellington:** New Zealand 317–6 at lunch, day two — Glenn
  Phillips 118, Henry Nicholls 146* (AP, 20 Nov 00:27 UTC).
- **World Children's Day:** UNICEF theme "My day. My rights. My future.",
  37 years since the Convention on the Rights of the Child.
- **Shenzhen:** President Prabowo meets Xi Jinping in a bilateral today, plus
  the Indonesia–China Business Forum (scheduled 20 Nov).
- **Anthropic IPO due to close today:** priced at $83, about $1.5 trillion
  fully diluted; shares trade as ANT (deal due to close 20 Nov).

Deliberately excluded after date checks: stories first reported on 19 November
(Trump–Iran comments, Voyager 1 confirmation, Houthi strike on Riyadh's PIF
Tower, Russian strikes on Kyiv embassies, Anthropic's first trading day, the
Berlin Coalition of the Willing summit, the Han Duck-soo ruling, the APEC
leaders' meeting and trilateral declaration) and earlier (Hayabusa2, 17 Nov;
Gemini 4 Neon, 18 Nov; Modi–William–Kate meeting, 18 Nov).

---

<sub>Entered on [make.fun](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
