# In Time / 时差 — Selected Projects in Six Temporal Dimensions

Working page for the *In Time / 时差* proposal (Venice Architecture Biennale 2027, China Pavilion), Protopolis Lab, NYU Shanghai.

`index.html` is a self-contained page: 40 candidate projects grouped into six temporal dimensions (Material, Ecological, Cultural, Maintenance, Financial, Technological), each with a link to its source, an image, and a "time-section profile" glyph showing how strongly each of the six dimensions is present in that project.

- `in-time-assets/` — one image per project (`<id>.jpg`), pulled from the linked source pages. A `<id>b.jpg` is an alternate view kept for later selection.
- `build/venice_build.py` — regenerates `index.html` from `build/venice_pool.json` (the project dossier) and `build/venice_images.json` (image sources). Run `python3 build/venice_build.py <folder-containing-in-time-assets> index.html`.

This is a working document for the curatorial team; project images belong to their credited sources and are linked back to them on each card.
