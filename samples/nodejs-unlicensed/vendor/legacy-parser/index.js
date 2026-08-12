/**
 * legacy-parser: a stand-in for a package that declares no license.
 * Its package.json has no license field, so the SBOM reports the license as unidentified.
 */

function parseGreeting(text) {
  return String(text).trim().toUpperCase();
}

module.exports = {parseGreeting};
