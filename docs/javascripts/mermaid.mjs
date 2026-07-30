import mermaid from "https://unpkg.com/mermaid@10.9.3/dist/mermaid.esm.min.mjs";

const FONT = '"Inter", Arial, Helvetica, sans-serif';

const LIGHT = {
  background: "#ffffff",
  primaryColor: "#ffffff",
  primaryBorderColor: "#00528c",
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
  nodeBorder: "#00528c",
  nodeTextColor: "#333333",
  clusterBkg: "#f7f7f7",
  clusterBorder: "#bdbfc0",
  titleColor: "#333333",
  edgeLabelBackground: "#ffffff",
  actorBkg: "#ffffff",
  actorBorder: "#00528c",
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
      actorFontSize: 14,
      messageFontSize: 14,
      noteFontSize: 14,
    },
  };
}

function currentScheme() {
  return document.body.getAttribute("data-md-color-scheme") || "default";
}

const SOURCE = new WeakMap();

let lastScheme = null;

let generation = 0;

async function render(force) {
  const nodes = document.querySelectorAll("pre.mermaid, .mermaid");
  if (!nodes.length) return;

  const scheme = currentScheme();
  if (!force && scheme === lastScheme) {
    const fresh = [...nodes].filter((n) => !SOURCE.has(n));
    if (!fresh.length) return;
  }

  const myGeneration = ++generation;

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
  }

  if (myGeneration !== generation) return;
  lastScheme = scheme;
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => render(true), {
    once: true,
  });
} else {
  render(true);
}

new MutationObserver((records) => {
  for (const record of records) {
    if (record.attributeName === "data-md-color-scheme") {
      render(true);
      return;
    }
  }
}).observe(document.body, { attributes: true });

if (window.document$ && typeof window.document$.subscribe === "function") {
  window.document$.subscribe(() => render(true));
}

window.mermaid = mermaid;
