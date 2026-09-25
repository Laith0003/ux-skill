#!/usr/bin/env node
/**
 * ux-skill: Node wrapper that delegates to the Python engine.
 *
 * Resolution order:
 *   1. `python3 -m engine.cli.main`      (if `engine/` is sibling to this script,
 *                                          i.e. running from the repo)
 *   2. `uxskill` console script           (if installed via pip, same version)
 *   3. `pipx run --spec uxskill==X`        (no Python install on path; one-shot)
 *   4. `pip install --user uxskill==X`     (last resort), then the engine
 *                                          through that same python3, once it
 *                                          reports version X (see ENGINE)
 *
 * X is this package's own version in Python form (4.0.0-beta.1 is 4.0.0b1).
 * npm ships only bin/, and pip skips pre-releases unless pinned, so without
 * the pin an npm beta would run the last stable Python release.
 *
 * Designed so a Cursor / Windsurf user with no Python can still `npx uxskill init`
 * and it auto-bootstraps via `pipx`.
 */
import { spawn } from "node:child_process";
import { existsSync, readFileSync, realpathSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const repoRoot = resolve(__dirname, "..");
const engineDir = resolve(repoRoot, "engine");

const args = process.argv.slice(2);

const PRE = { alpha: "a", beta: "b", rc: "rc" };

/** This package's version in the form pip expects (4.0.0-beta.1 is 4.0.0b1). */
export function pythonSpec(npmVersion) {
  const version = npmVersion ??
    JSON.parse(readFileSync(resolve(repoRoot, "package.json"), "utf8")).version;
  const m = /^(\d+\.\d+\.\d+)(?:-(alpha|beta|rc)\.(\d+))?$/.exec(version);
  if (!m) throw new Error(`package.json version ${version} is not in a form pip can match`);
  return m[2] ? `${m[1]}${PRE[m[2]]}${m[3]}` : m[1];
}

function capture(cmd, argv) {
  return new Promise((resolvePromise) => {
    let out = "";
    const child = spawn(cmd, argv, { stdio: ["ignore", "pipe", "ignore"] });
    child.stdout.on("data", (d) => { out += d; });
    child.on("error", () => resolvePromise(""));
    child.on("close", () => resolvePromise(out));
  });
}

function spawnPromise(cmd, argv, options = {}) {
  return new Promise((resolvePromise) => {
    const child = spawn(cmd, argv, { stdio: "inherit", ...options });
    child.on("error", () => resolvePromise(127));
    child.on("close", (code) => resolvePromise(code ?? 0));
  });
}

// Runs the installed engine's CLI. `python3 -m` would put the working
// folder first on sys.path, so a project with its own top-level engine/
// package would run in place of ours. This takes those entries off first;
// the working folder itself is unchanged, so a relative --out still lands
// in the project.
const ENGINE = [
  "import os, sys",
  "here = os.path.realpath(os.getcwd())",
  "sys.path[:] = [p for p in sys.path if p and os.path.realpath(p) != here]",
  "sys.argv[0] = 'uxskill'",
  "from engine.cli.main import cli",
  "sys.exit(cli())",
].join("\n");

async function which(cmd) {
  return await spawnPromise(process.platform === "win32" ? "where" : "which",
    [cmd], { stdio: "ignore" }).then((code) => code === 0);
}

async function main() {
  // 1. Local repo dev mode
  if (existsSync(engineDir)) {
    const code = await spawnPromise("python3", ["-m", "engine.cli.main", ...args], {
      cwd: repoRoot,
      env: { ...process.env, PYTHONPATH: repoRoot }
    });
    if (code !== 127) process.exit(code);
  }

  const version = pythonSpec();

  // 2. Pip-installed console script, only when it is this version
  if (await which("uxskill")) {
    const installed = await capture("uxskill", ["--version"]);
    if (installed.trim().endsWith(` ${version}`)) {
      process.exit(await spawnPromise("uxskill", args));
    }
  }

  // 3. pipx run, pinned to this version (one-shot install)
  if (await which("pipx")) {
    process.exit(await spawnPromise("pipx",
      ["run", "--spec", `uxskill==${version}`, "uxskill", ...args]));
  }

  // 4. python3 -m pip install --user, pinned (last resort). Then run the
  // engine through the same python3, once it reports this version: a
  // `uxskill` found on PATH may be an older install that still comes first.
  const pinned = `uxskill==${version}`;
  if (!(await which("python3"))) {
    console.error(
      "ux-skill: no Python runtime found (python3 is not on PATH). Install Python 3.10+, " +
      `then run:\n  pipx install ${pinned}\n` +
      "or visit https://uxskill.laithjunaidy.com for help."
    );
    process.exit(1);
  }
  console.error(`ux-skill: bootstrapping via \`python3 -m pip install --user ${pinned}\`...`);
  const installCode = await spawnPromise("python3",
    ["-m", "pip", "install", "--user", "--quiet", pinned]);
  if (installCode !== 0) {
    console.error(
      `ux-skill: pip could not install ${pinned} (exit code ${installCode}); pip's own ` +
      "message is above. Install it yourself, then run the command again:\n" +
      `  pipx install ${pinned}\n` +
      `or, inside a virtual environment:\n  pip install ${pinned}`
    );
    process.exit(1);
  }
  const loaded = (await capture("python3", ["-c", ENGINE, "--version"])).trim();
  if (!loaded.endsWith(` ${version}`)) {
    console.error(
      `ux-skill: pip installed ${pinned}, but python3 loads ` +
      `${loaded ? `"${loaded}"` : "no uxskill engine"}, so the command was not run. ` +
      `Install it where it runs on its own, then run the command again:\n  pipx install ${pinned}`
    );
    process.exit(1);
  }
  process.exit(await spawnPromise("python3", ["-c", ENGINE, ...args]));
}

if (process.argv[1] && import.meta.url === pathToFileURL(realpathSync(process.argv[1])).href) {
  main().catch((err) => {
    console.error("ux-skill: fatal error:", err);
    process.exit(1);
  });
}
