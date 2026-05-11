let id;

function insertMetaDates() {
  const frontmatter = app.site.cache.cache[app.currentFilepath].frontmatter;
  if (!frontmatter) {
    return;
  }

  const created = frontmatter["created"]?.replaceAll("-", "/");
  const updated = frontmatter["updated"]?.replaceAll("-", "/");
  if (!created && !updated) {
    return;
  }

  const frontmatterEl = document.querySelector(".frontmatter");
  if (!frontmatterEl) {
    return;
  }

  frontmatterEl.insertAdjacentHTML(
    "afterend",
    `
<div style="display: flex; justify-content: end; gap: 3px;">
    <a href="#${created}" class="tag" target="_blank" rel="noopener">
        Created:${created}
    </a>
    <a href="#${updated}" class="tag" target="_blank" rel="noopener">
        Updated:${updated}
    </a>
</div>
`
  );

  clearInterval(id);
}

const onChangeDOM = (mutationsList, observer) => {
  for (let mutation of mutationsList) {
    if (
      mutation.type === "childList" &&
      mutation.addedNodes[0]?.className === "page-header"
    ) {
      clearInterval(id);
      id = setInterval(insertMetaDates, 50);
    }
  }
};

const targetNode = document.querySelector(
  ".markdown-preview-sizer.markdown-preview-section"
);
const observer = new MutationObserver(onChangeDOM);
observer.observe(targetNode, { childList: true, subtree: true });
id = setInterval(insertMetaDates, 50);