// Site-wide mermaid config, shared by every diagram so individual pages don't
// need a %%{init}%% directive. Colors/fonts are controlled separately via
// --md-mermaid-* CSS custom properties in docs/css/wenglor.css, since
// mkdocs-material's own injected theme CSS always overrides themeVariables
// colors set here -- this file only needs to cover what CSS can't reach.
import mermaid from "https://unpkg.com/mermaid@10/dist/mermaid.esm.min.mjs";

mermaid.initialize({
  startOnLoad: true,
  theme: "base",
  sequence: {
    actorMargin: 120,
    // mermaid draws loop/opt/alt/par fragment labels ("loop", "opt", ...) in a
    // fixed 50x20px box (labelBoxWidth/labelBoxHeight aren't configurable) and
    // sizes that label text from messageFontSize -- the site's larger 16px
    // default overflows that fixed box, so keep it smaller here. This also
    // affects arrow/message text (mermaid ties both to the same option), so
    // keep note/actor text at the same size for visual consistency.
    actorFontSize: 14,
    messageFontSize: 14,
    noteFontSize: 14,
  },
});

window.mermaid = mermaid;
