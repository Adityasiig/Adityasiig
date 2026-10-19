# Flow / Profile design

This rebuild is for the GitHub profile README in `Adityasiig/Adityasiig`.
The separately linked Gotham portfolio website is a separate repository.

The supplied visual reference inspired the whole composition: a dark silhouette,
luminous flowing ribbons, generous space, silver-white surfaces, and restrained
serif typography. The README has a new introduction, project gallery, system
diagram, toolkit, experiments, and contact section. Existing project links and
career details were carried forward from the previous README.

## Files

- `../README.md`: the profile GitHub renders.
- `../github-profile-assets/flow/`: self-contained local PNG and SVG assets.
- `hero-art.jpg`: generated hero artwork before typography.
- `hero.html`: editable desktop and mobile hero layouts.
- `build-profile.cjs`: generates the section graphics, project graphics, diagram,
  footer, hero screenshots, and local preview.
- `preview.css`: a local approximation of GitHub's native Markdown styles.
- `../preview/index.html`: a standalone local preview with a theme toggle.

GitHub owns the surrounding page background, fonts, table borders, and link
colors. The README uses supported Markdown/HTML and local artwork; it has no
custom CSS dependency, external font request, JavaScript, or statistics service.
The preview controls and CSS are only part of the local preview.

`picture` sources serve larger text and alternate layouts on screens up to 600px.
GitHub's public Markdown renderer was checked with a generic, content-free
`picture` sample and preserved both the media query and source. The full profile
was checked locally. Native project descriptions remain selectable text, images
have descriptive alt text, and the system diagram has a text alternative.

## Rebuild

From the repository root, with Node.js available:

```sh
npm install --no-save --package-lock=false sharp playwright marked
npx playwright install chromium
node design/build-profile.cjs
```

For an existing runtime, `PROFILE_NODE_MODULES` can point to its `node_modules`
directory. `PROFILE_BROWSER_PATH` can point to an installed Chromium browser.
These overrides are optional; no machine-specific paths are built into the files.

Open `preview/index.html` in a browser. The build also saves desktop, mobile,
and dark screenshots in `preview/`. The generated README assets can be used on
GitHub without installing or running anything.

## Hero artwork provenance

Generated with the built-in imagegen tool using the user-supplied image as a
visual reference. Typography was added through the native HTML hero layout.
The final project asset is `../github-profile-assets/flow/hero.png`, with a mobile
variant alongside it. The editable background is `hero-art.jpg`.

## Dark mode

`hero-art-dark.jpg` is the user's supplied dark wallpaper, copied directly
without regenerating or altering its pixels. `hero.html?theme=dark` places it in
the existing cover layout, rotates it upright with CSS, and switches the cover
text to light gray. Desktop and mobile exports are `hero-dark.png` and
`hero-mobile-dark.png`.

The build also emits `-dark.svg` variants of the section headers, project cards,
and system diagram. Their geometry, typography, and content match the light
versions; only the palette changes. The footer has matching light and dark
variants on desktop and mobile. All images follow the selected theme.

The profile uses `prefers-color-scheme: dark` sources in `picture` elements,
with mobile dark sources before desktop dark sources. Light images remain the
fallback. The local preview's theme button also updates picture media queries
so the preview changes artwork as well as the surrounding background.

The build checks desktop and mobile in both themes, verifies every selected
image belongs to the correct theme, and checks the preview's theme toggle.

Original light artwork generation prompt:

> Use case: stylized-concept. Asset type: wide hero background for a GitHub
> profile README. Input image 1 is a visual reference for the subject,
> monochrome palette, silky flowing energy, fine-art atmosphere. Create a NEW
> landscape composition in 16:9. On the right third, an upright small black
> silhouette of a Krishna-inspired figure, seen from behind, curly hair with a
> small peacock feather, flowing draped garments, suspended peacefully in vast
> luminous silver-white ribbons and wisps of clouds. Quiet, powerful,
> transcendental. White silk ribbons spiral around the figure with beautifully
> detailed filaments, sculptural light, soft photographic grain. Strictly
> monochrome pearl white, silver, mist gray and deep black. Keep the left 55
> percent mostly luminous pale ivory with subtle wisps and spacious empty space
> for separately composited dark typography. The figure must be fully visible
> and occupy about 45 percent of image height, near x=78 percent. Editorial art,
> sophisticated and restrained, faithful to the reference's intricate flowing
> light and silhouetted figure. No text, letters, interface, logos, watermarks
> or border.
