#!/usr/bin/env node
/**
 * ux-skill — Node wrapper that delegates to the Python engine.
 *
 * Resolution order:
 *   1. `python3 -m engine.cli.main`      (if `engine/` is sibling to this script,
 *                                          i.e. running from the repo)
 *   2. `uxskill` console script           (if installed via pip, same version)
 *   3. `pipx run --spec uxskill==X`        (no Python install on path; one-shot)
 *   4. `pip install --user uxskill==X`     (last resort)
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

  // 4. python3 -m pip install --user, pinned (last resort)
  if (await which("python3")) {
    console.error(`ux-skill: bootstrapping via \`pip install --user uxskill==${version}\`...`);
    const installCode = await spawnPromise("python3",
      ["-m", "pip", "install", "--user", "--quiet", `uxskill==${version}`]);
    if (installCode === 0 && (await which("uxskill"))) {
      process.exit(await spawnPromise("uxskill", args));
    }
  }

  console.error(
    "ux-skill: could not find a Python runtime. Install Python 3.9+ or run:\n" +
    `  pipx install uxskill==${pythonSpec()}\n` +
    "or visit https://uxskill.laithjunaidy.com for help."
  );
  process.exit(1);
}

if (process.argv[1] && import.meta.url === pathToFileURL(realpathSync(process.argv[1])).href) {
  main().catch((err) => {
    console.error("ux-skill: fatal error:", err);
    process.exit(1);
  });
}
