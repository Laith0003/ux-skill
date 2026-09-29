/**
 * shot-names.mjs - how verify-responsive.mjs names its screenshots.
 * Kept apart so tests can import the names without starting the verifier.
 */
import { relative, isAbsolute } from 'node:path';

/**
 * The page part of a screenshot name: a file's path under the working folder
 * (or its full path outside it), or a URL's host and path, without the
 * extension, as lowercase words joined by dashes. en/index.html and
 * ar/index.html give en-index and ar-index.
 */
export function pageSlug(target, cwd = process.cwd()) {
  let host = '';
  let name = String(target || 'page');
  const web = /^(https?):\/\/([^/?#]+)([^?#]*)/i.exec(name);
  if (web) { host = web[2]; name = web[3]; }
  else {
    name = name.replace(/^file:\/\//i, '');
    const rel = isAbsolute(name) ? relative(cwd, name) : name;
    name = rel.startsWith('..') ? name : rel;
  }
  name = name.replace(/\/+$/, '').replace(/\.[a-z0-9]+$/i, '');
  const slug = (host + '/' + name).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
  return slug || 'page';
}

/** The screenshot file name for one page at one width. */
export function shotName(target, width, cwd = process.cwd()) {
  return 'verify-' + pageSlug(target, cwd) + '-' + width + '.png';
}
