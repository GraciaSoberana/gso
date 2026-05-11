```
// Update Publish Files.md
<%*
const dv = app.plugins.plugins["dataview"].api;
const filename = "Arraigados en Cristo y Su evangelio";
const query = `
TABLE WITHOUT ID sequence AS " ", file.link AS "Título"
FROM #Ministerial/Discipulado 
WHERE type = "discipulado" AND series = [[Arraigados en Cristo y Su evangelio]]
SORT sequence ASC`;

const tFile = tp.file.find_tfile(filename);
const queryOutput = await dv.queryMarkdown(query);

// write query output to file
await app.vault.modify(tFile, queryOutput.value);
%>
```