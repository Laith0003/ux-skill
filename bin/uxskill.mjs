#!/usr/bin/env node
/**
 * ux-skill — Node wrapper that delegates to the Python engine.
 *
 * Resolution order:
 *   1. `python3 -m engine.cli.main`      (if `engine/` is sibling to this script,
 *                                          i.e. running from the repo)
 *   2. `uxskill` console script           (if installed via pip)
 *   3. `pipx run uxskill`                 (no Python install on path; one-shot)
 *
 * Designed so a Cursor / Windsurf user with no Python can still `npx uxskill init`
 * and it auto-bootstraps via `pipx`.
 */
import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const repoRoot = resolve(__dirname, "..");
const engineDir = resolve(repoRoot, "engine");

const args = process.argv.slice(2);

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

  // 2. Pip-installed console script
  if (await which("uxskill")) {
    process.exit(await spawnPromise("uxskill", args));
  }

  // 3. pipx run uxskill (one-shot install)
  if (await which("pipx")) {
    process.exit(await spawnPromise("pipx", ["run", "uxskill", ...args]));
  }

  // 4. python3 -m pip install --user uxskill (last resort)
  if (await which("python3")) {
    console.error("ux-skill: bootstrapping via `pip install --user uxskill`...");
    const installCode = await spawnPromise("python3",
      ["-m", "pip", "install", "--user", "--quiet", "uxskill"]);
    if (installCode === 0 && (await which("uxskill"))) {
      process.exit(await spawnPromise("uxskill", args));
    }
  }

  console.error(
    "ux-skill: could not find a Python runtime. Install Python 3.9+ or run:\n" +
    "  pipx install uxskill\n" +
    "or visit https://uxskill.laithjunaidy.com for help."
  );
  process.exit(1);
}

main().catch((err) => {
  console.error("ux-skill: fatal error:", err);
  process.exit(1);
});
