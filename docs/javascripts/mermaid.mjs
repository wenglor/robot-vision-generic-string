// Site-wide mermaid config, shared by every diagram so individual pages don't
// need a %%{init}%% directive.
//
// Kept byte-identical in every repo -- edit it in context/style/javascripts/
// and re-copy, never edit a repo copy directly.
//
// WHY COLORS LIVE HERE AND NOT IN CSS
// -----------------------------------
// mermaid emits a <style> block per diagram, scoped by a unique generated id:
//
//     #mermaid-1785304363602 .actor-line { stroke: grey; }
//
// That is an ID selector (specificity 1-1-0), so it beats any class-based rule
// we could write in wenglor.css (0-2-0) no matter the stylesheet order. The
// only reliable way to control those colors is to feed mermaid's own
// themeVariables, which is what generates that block in the first place.
//
// The theme DOES ship rules that consume its --md-mermaid-* variables, but it
// injects them as mermaid `themeCSS` only through its built-in mermaid
// integration. This site loads mermaid itself (so it can set layout options
// the theme doesn't expose -- see `sequence` below), so that path never runs.
//
// WHY WE DON'T USE ZENSICAL'S BUILT-IN MERMAID INTEGRATION
// -------------------------------------------------------
// Zensical ships one (theme bundle: `mermaid.initialize(...)` + `mermaid.render`),
// so loading mermaid ourselves looks redundant. It isn't -- two blockers:
//
//   1. No config surface. Zensical exposes only the superfences custom fence
//      (see its config.py); there is no option for mermaid settings. Its
//      initialize() call hardcodes `sequence: {actorFontSize/messageFontSize/
//      noteFontSize: "16px"}` and sets NO actorMargin.
//   2. Closed shadow root. It renders each diagram into
//      `attachShadow({mode: "closed"})`, so neither wenglor.css nor any
//      stylesheet of ours can reach inside to correct anything.
//
// (1) is not cosmetic: 16px messageFontSize overflows the fixed 50x20px
// alt/loop/opt fragment label box -- see the `sequence` comment below. The
// generic-string protocol diagrams use alt/else, loop, and opt, so those labels
// would render broken, and (2) means it could not be patched from CSS.
//
// Re-evaluate only if Zensical gains real mermaid config options AND drops the
// closed shadow root. Until then this file stays.
//
// Values below are the wenglor Corporate Design primary colors:
//   wenglor blue #00619e | Deep Dark Gray #333333 | Dark Gray #74787b
//   Light Gray   #bdbfc0 | Lightest Gray  #eaeaea
//
// Pinned to an exact patch, matching how CI pins zensical: an unpinned CDN
// specifier (`mermaid@10`) lets a mermaid release change published diagrams
// with no commit in these repos. Bump deliberately.
import mermaid from "https://unpkg.com/mermaid@10.9.3/dist/mermaid.esm.min.mjs";

const FONT = '"Inter", Arial, Helvetica, sans-serif';

// Light scheme -- CD colors on white.
const LIGHT = {
  background: "#ffffff",
  primaryColor: "#ffffff",
  primaryBorderColor: "#00619e",
  primaryTextColor: "#333333",
  secondaryColor: "#eaeaea",
  secondaryBorderColor: "#bdbfc0",
  secondaryTextColor: "#333333",
  tertiaryColor: "#eaeaea",
  tertiaryBorderColor: "#bdbfc0",
  tertiaryTextColor: "#333333",
  lineColor: "#74787b",
  textColor: "#333333",
  mainBkg: "#ffffff",
  nodeBorder: "#00619e",
  nodeTextColor: "#333333",
  clusterBkg: "#f7f7f7",
  clusterBorder: "#bdbfc0",
  titleColor: "#333333",
  edgeLabelBackground: "#ffffff",
  // Sequence diagrams
  actorBkg: "#ffffff",
  actorBorder: "#00619e",
  actorTextColor: "#333333",
  actorLineColor: "#74787b",
  signalColor: "#333333",
  signalTextColor: "#333333",
  labelBoxBkgColor: "#ffffff",
  labelBoxBorderColor: "#74787b",
  labelTextColor: "#333333",
  loopTextColor: "#333333",
  noteBkgColor: "#eaeaea",
  noteBorderColor: "#bdbfc0",
  noteTextColor: "#333333",
  activationBkgColor: "#eaeaea",
  activationBorderColor: "#74787b",
  sequenceNumberColor: "#ffffff",
};

// Dark scheme -- pure white panels glare on a near-black page, so use the
// elevated surface color and the dark-safe brand tint (#6fb3e0) that clears
// AA contrast. Mirrors the [data-md-color-scheme=slate] block in wenglor.css.
const DARK = {
  background: "#1b2229",
  primaryColor: "#1b2229",
  primaryBorderColor: "#6fb3e0",
  primaryTextColor: "#e3e6e8",
  secondaryColor: "#2a323a",
  secondaryBorderColor: "#4a5560",
  secondaryTextColor: "#e3e6e8",
  tertiaryColor: "#2a323a",
  tertiaryBorderColor: "#4a5560",
  tertiaryTextColor: "#e3e6e8",
  lineColor: "#9aa0a6",
  textColor: "#e3e6e8",
  mainBkg: "#1b2229",
  nodeBorder: "#6fb3e0",
  nodeTextColor: "#e3e6e8",
  clusterBkg: "#222a32",
  clusterBorder: "#4a5560",
  titleColor: "#e3e6e8",
  edgeLabelBackground: "#1b2229",
  actorBkg: "#1b2229",
  actorBorder: "#6fb3e0",
  actorTextColor: "#e3e6e8",
  actorLineColor: "#9aa0a6",
  signalColor: "#e3e6e8",
  signalTextColor: "#e3e6e8",
  labelBoxBkgColor: "#1b2229",
  labelBoxBorderColor: "#9aa0a6",
  labelTextColor: "#e3e6e8",
  loopTextColor: "#e3e6e8",
  noteBkgColor: "#2a323a",
  noteBorderColor: "#4a5560",
  noteTextColor: "#e3e6e8",
  activationBkgColor: "#2a323a",
  activationBorderColor: "#9aa0a6",
  sequenceNumberColor: "#0d1117",
};

function configFor(scheme) {
  return {
    startOnLoad: false,
    theme: "base",
    themeVariables: {
      fontFamily: FONT,
      fontSize: "16px",
      ...(scheme === "slate" ? DARK : LIGHT),
    },
    flowchart: {
      useMaxWidth: true,
      htmlLabels: true,
      curve: "basis",
    },
    sequence: {
      actorMargin: 120,
      useMaxWidth: true,
      // mermaid draws loop/opt/alt/par fragment labels ("loop", "opt", ...) in
      // a fixed 50x20px box (labelBoxWidth/labelBoxHeight aren't configurable)
      // and sizes that label text from messageFontSize -- the site's larger
      // 16px default overflows that fixed box, so keep it smaller here. This
      // also affects arrow/message text (mermaid ties both to the same
      // option), so keep note/actor text at the same size for consistency.
      actorFontSize: 14,
      messageFontSize: 14,
      noteFontSize: 14,
    },
  };
}

function currentScheme() {
  return document.body.getAttribute("data-md-color-scheme") || "default";
}

// Cache each diagram's source: mermaid replaces the element's text content
// with rendered SVG on the first pass, so a re-render (dark-mode toggle, or
// instant navigation returning to a cached page) would have nothing to parse.
const SOURCE = new WeakMap();

let lastScheme = null;

// mermaid.run() is async. navigation.instant can swap in a new page's DOM
// before a previous render finishes -- the theme replaces page content via XHR
// rather than a full reload, so a stale in-flight render can still be running
// when the user has already navigated elsewhere. If that stale run is left to
// resolve against the nodes it captured, it mutates whatever now sits in that
// DOM position instead of the diagram it was meant for.
//
// generation is bumped on every render() call. Nodes are only handed to
// mermaid.run() one page's worth at a time, and the result is discarded --
// never applied back to lastScheme/SOURCE bookkeeping -- if a newer render()
// has since started. This can't undo work mermaid's internals already did to
// the DOM mid-flight, but it stops a stale run's *outcome* from being treated
// as authoritative, and the very next legitimate render() (always triggered
// by document$ on the new page) re-renders every node from its cached
// SOURCE text regardless, overwriting any stale leftovers.
let generation = 0;

async function render(force) {
  const nodes = document.querySelectorAll("pre.mermaid, .mermaid");
  if (!nodes.length) return;

  const scheme = currentScheme();
  if (!force && scheme === lastScheme) {
    // Same scheme -- only render diagrams we haven't touched yet.
    const fresh = [...nodes].filter((n) => !SOURCE.has(n));
    if (!fresh.length) return;
  }

  const myGeneration = ++generation;

  // themeVariables are baked in at initialize() time, so re-initialize before
  // re-rendering for the new scheme.
  mermaid.initialize(configFor(scheme));

  for (const node of nodes) {
    if (!SOURCE.has(node)) {
      SOURCE.set(node, node.textContent || "");
    } else {
      node.textContent = SOURCE.get(node);
    }
    node.removeAttribute("data-processed");
  }

  try {
    await mermaid.run({ nodes, suppressErrors: true });
  } catch {
    // suppressErrors already swallows parse errors; this covers anything else.
  }

  if (myGeneration !== generation) return; // superseded -- don't commit
  lastScheme = scheme;
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => render(true), {
    once: true,
  });
} else {
  render(true);
}

// Re-render when the color scheme changes, so diagrams follow the dark/light
// toggle. The theme flips data-md-color-scheme on <body>.
new MutationObserver((records) => {
  for (const record of records) {
    if (record.attributeName === "data-md-color-scheme") {
      render(true);
      return;
    }
  }
}).observe(document.body, { attributes: true });

// With navigation.instant the theme swaps page content via XHR instead of a
// full document load, so DOMContentLoaded never fires again.
if (window.document$ && typeof window.document$.subscribe === "function") {
  window.document$.subscribe(() => render(true));
}

window.mermaid = mermaid;
