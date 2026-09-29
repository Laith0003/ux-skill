// Run this through Figma's plugin API, as the body of an async function (the way the
// plugin API tools run code), since it uses await and return at the top level; inside a
// plugin, wrap it in an async function first. It reads the file's own variables in the
// shape Figma's REST API returns for its local variables. Save the text it returns as
// variables.json and import that file into ux-skill as a Figma variables export.
// It only reads; nothing in the file changes.
const collections = await figma.variables.getLocalVariableCollectionsAsync();
const variables = await figma.variables.getLocalVariablesAsync();
const meta = {variableCollections: {}, variables: {}};
for (const c of collections) {
  meta.variableCollections[c.id] = {
    id: c.id, name: c.name, modes: c.modes.map((m) => ({modeId: m.modeId, name: m.name})),
    defaultModeId: c.defaultModeId, variableIds: c.variableIds.slice(),
    hiddenFromPublishing: c.hiddenFromPublishing, remote: c.remote,
  };
}
for (const v of variables) {
  meta.variables[v.id] = {
    id: v.id, name: v.name, variableCollectionId: v.variableCollectionId,
    resolvedType: v.resolvedType, valuesByMode: v.valuesByMode, scopes: v.scopes.slice(),
    description: v.description, hiddenFromPublishing: v.hiddenFromPublishing, remote: v.remote,
  };
}
return JSON.stringify({meta: meta});
