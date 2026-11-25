import { copyFileSync, mkdirSync, readFileSync, chmodSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = "/output";
const target = join(outDir, "entry.png");

const buf = readFileSync(src);
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!buf.subarray(0, 8).equals(pngMagic)) {
  throw new Error("entry.png is not a whole PNG");
}
if (buf.length > 1048576) {
  throw new Error("entry.png exceeds the 1 MiB gate");
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, target);
// chmod on the FILE only (never on /output itself): the collector reads
// the file as another user, so 0o644 is the gate-safe mode.
chmodSync(target, 0o644);
console.log(`wrote ${target} (${buf.length} bytes)`);
