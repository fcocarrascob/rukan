// Las fórmulas: KaTeX vendoreado en visor/vendor/katex/, renderizado al cargar
// cada página (Material navega sin recargar, por eso document$ y no DOMContentLoaded).
// La coma decimal dentro del LaTeX se escribe {,} como en los memos.
document$.subscribe(({ body }) => {
  renderMathInElement(body, {
    delimiters: [
      { left: "$$", right: "$$", display: true },
      { left: "$", right: "$", display: false },
      { left: "\\(", right: "\\)", display: false },
      { left: "\\[", right: "\\]", display: true },
    ],
    throwOnError: false,
  });
});
