// MathJax configuration for pymdownx.arithmatex in "generic" mode.
//
// arithmatex generic mode emits \(...\) for inline and \[...\] for block math,
// so the delimiters below must match. This file only configures MathJax and
// re-typesets after instant navigation -- the library itself is loaded from
// the CDN entry in extra_javascript, which must come AFTER this file.
//
// Kept byte-identical in every repo -- edit it in context/style/javascripts/
// and re-copy, never edit a repo copy directly.

window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true,
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex",
  },
};

// With navigation.instant the theme swaps page content via XHR, so MathJax's
// own DOMContentLoaded typesetting never runs again. Re-typeset each time.
if (window.document$ && typeof window.document$.subscribe === "function") {
  window.document$.subscribe(() => {
    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.startup.output.clearCache();
      window.MathJax.typesetClear();
      window.MathJax.texReset();
      window.MathJax.typesetPromise();
    }
  });
}
