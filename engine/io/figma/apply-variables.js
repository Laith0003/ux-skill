// Run this through Figma's plugin API in the file the variables belong to. PAYLOAD,
// defined above, lists collections, each with its modes and its variables; a variable
// holds one value per mode, a literal or {alias: "collection:variable"}.
// Collections, modes and variables are matched by name, so a second run updates the
// same variables in place. Nothing is ever deleted. A variable that already exists with
// another type is left as it is and listed under conflicts, and so is every value that
// would point at it. When PAYLOAD.mode is "extend", the payload holds only additions:
// a collection it names must already be in the file (unless it is marked new), and an
// existing collection is never renamed and never gets a mode.
const extend = PAYLOAD.mode === "extend";
const collections = await figma.variables.getLocalVariableCollectionsAsync();
const local = await figma.variables.getLocalVariablesAsync();
const result = {created: 0, updated: 0, aliased: 0, conflicts: []};
const nameOf = {};
for (const c of collections) nameOf[c.id] = c.name;
const byKey = {};
for (const v of local) {
  const key = nameOf[v.variableCollectionId] + ":" + v.name;
  if (v.variableCollectionId in nameOf && !(key in byKey)) byKey[key] = v;
}
const left = {};
const shown = (key) => key.replace(":", "/");
const plans = [];
for (const spec of PAYLOAD.collections) {
  let col = collections.find((c) => c.name === spec.name);
  const count = spec.variables.length;
  const them = count === 1 ? "its 1 variable was" : "its " + count + " variables were";
  if (!col && extend && !spec.new) {
    result.conflicts.push(spec.name + " is not a collection in this file, so " + them +
      " not written; export the variables of this file again and repeat the extension");
    for (const v of spec.variables) left[spec.name + ":" + v.name] = true;
    continue;
  }
  if (!col) {
    col = figma.variables.createVariableCollection(spec.name);
    collections.push(col);
    nameOf[col.id] = spec.name;
    col.renameMode(col.modes[0].modeId, spec.modes[0]);
  }
  const modeIds = {};
  const missing = [];
  for (const name of spec.modes) {
    const mode = col.modes.find((m) => m.name === name);
    if (mode) { modeIds[name] = mode.modeId; continue; }
    if (extend && !spec.new) { missing.push(name); continue; }
    try { modeIds[name] = col.addMode(name); } catch (e) { missing.push(name); }
  }
  if (missing.length) {
    const fix = extend ? "export the variables of this file again and repeat the extension"
      : "add the mode in Figma (a plan can limit the modes of a collection) and run this again";
    result.conflicts.push(spec.name + " has no mode " + missing.join(", ") + ", so " + them +
      " not written; " + fix);
    for (const v of spec.variables) left[spec.name + ":" + v.name] = true;
    continue;
  }
  const written = [];
  for (const v of spec.variables) {
    const key = spec.name + ":" + v.name;
    let variable = byKey[key];
    if (variable && variable.resolvedType !== v.type) {
      result.conflicts.push(shown(key) + " is a " + variable.resolvedType +
        " in this file, not a " + v.type + "; it was left as it is, so rename one of the two");
      left[key] = true;
      continue;
    }
    if (variable) {
      result.updated += 1;
    } else {
      variable = figma.variables.createVariable(v.name, col, v.type);
      byKey[key] = variable;
      result.created += 1;
    }
    variable.scopes = v.scopes;
    variable.hiddenFromPublishing = v.hidden;
    variable.description = v.description || "";
    written.push([v, variable]);
  }
  plans.push({spec: spec, modeIds: modeIds, written: written});
}
for (const plan of plans) {
  for (const [v, variable] of plan.written) {
    const key = plan.spec.name + ":" + v.name;
    for (const mode of plan.spec.modes) {
      if (!(mode in v.values)) continue;
      let value = v.values[mode];
      const alias = value !== null && typeof value === "object" && "alias" in value;
      if (alias) {
        const target = left[value.alias] ? null : byKey[value.alias];
        if (!target) {
          const why = left[value.alias] ? "which was not written" : "which is not in this file";
          result.conflicts.push(shown(key) + " aliases " + shown(value.alias) + " in the mode " +
            mode + ", " + why + ", so that mode keeps its value; fix " + shown(value.alias) +
            " and run this again");
          continue;
        }
        value = figma.variables.createVariableAlias(target);
      }
      try {
        variable.setValueForMode(plan.modeIds[mode], value);
        if (alias) result.aliased += 1;
      } catch (e) {
        result.conflicts.push(shown(key) + " could not take its value in the mode " + mode +
          " (" + e.message + "); set it in Figma");
      }
    }
  }
}
return result;
