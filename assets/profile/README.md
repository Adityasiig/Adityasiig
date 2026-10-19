# Profile assets

Generated, not hand drawn. Everything here comes from one 5x7 dot font
and one tiled dot field, which is why the hero, the section rules and
the footer share a language with the portfolio and the Glyph Matrix
toys instead of looking like three separate things.

Palette is the portfolio's: pure black, white, `#d71921` red, and the
same greys. No gradients.

Constraints these are built to:

- No scripts, no external references, no web fonts. GitHub serves
  README images through camo, which strips all three, so anything
  relying on them renders blank.
- An opaque black background rect on every asset. Without it they look
  broken on GitHub's light theme.
- The background field is one `<pattern>` rather than ~1800 circles.
  Same picture, 8KB instead of 78KB.
- Section rules inset to 70px to line up with the hero's margin.
