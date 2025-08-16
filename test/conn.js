import os from "os";
import path from "path";
import fs from "fs";

// get program data path
function getProgramDataPath(appname = null) {
  const platform = process.platform; // 'win32', 'darwin', 'linux'

  let base;
  if (platform === "win32") {
    base = process.env.PROGRAMDATA || "C:\\ProgramData";
  } else if (platform === "darwin") {
    base = path.join(os.homedir(), "Library", "Application Support");
  } else {
    base = path.join(os.homedir(), ".local", "share");
  }

  return appname ? path.join(base, appname) : base;
}

// use function
const appPath = getProgramDataPath("ProdDash");

// load config
function loadCfg(filePath) {
  const raw = fs.readFileSync(filePath, "utf-8");
  return JSON.parse(raw);
}

const cfg = loadCfg(path.join(appPath, "app_cfg.json"));

console.log(cfg.port);
