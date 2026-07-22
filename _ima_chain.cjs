const { spawnSync } = require('child_process');
const fs = require('fs');

const NODE = 'C:/Users/90630/.workbuddy/binaries/node/versions/22.22.2/node.exe';
const SKILL = 'C:/Users/90630/.workbuddy/skills/ima-skills__skillhub';
const FILE = 'C:/Users/90630/WorkBuddy/automation-2026-07-13-12-02-24/情绪管理-晓晓老师课堂笔记_20260722.md';
const KB = 'pm8-1404_EPGkcfBKDri-wPiUpjUHUjqokpiC7NvFo8=';
const FNAME = '情绪管理-晓晓老师课堂笔记_20260722.md';
const FSIZE = fs.statSync(FILE).size;

function run(script, args) {
  const r = spawnSync(NODE, [script, ...args], { encoding: 'utf8', maxBuffer: 1 << 26 });
  if (r.status !== 0) {
    console.log('STEP FAILED:', script, 'exit', r.status);
    console.log('stderr:', (r.stderr || '').slice(0, 800));
    process.exit(1);
  }
  return r.stdout;
}

// 1) create_media
const createBody = JSON.stringify({
  file_name: FNAME, file_size: FSIZE, content_type: 'text/markdown',
  knowledge_base_id: KB, file_ext: 'md'
});
console.log('[1] create_media ...');
const createOut = run(SKILL + '/ima_api.cjs', ['openapi/wiki/v1/create_media', createBody]);
const createData = JSON.parse(createOut).data;
const mediaId = createData.media_id;
const c = createData.cos_credential;
console.log('    media_id =', mediaId);

// 2) cos-upload
console.log('[2] cos-upload ...');
run(SKILL + '/knowledge-base/scripts/cos-upload.cjs', [
  '--file', FILE,
  '--secret-id', c.secret_id,
  '--secret-key', c.secret_key,
  '--token', c.token,
  '--bucket', c.bucket_name,
  '--region', c.region,
  '--cos-key', c.cos_key,
  '--content-type', 'text/markdown',
  '--start-time', String(c.start_time),
  '--expired-time', String(c.expired_time),
  '--timeout', '120000'
]);
console.log('    cos-upload OK');

// 3) add_knowledge
const addBody = JSON.stringify({
  media_type: 7, media_id: mediaId, title: FNAME,
  knowledge_base_id: KB,
  file_info: { cos_key: c.cos_key, file_size: FSIZE, file_name: FNAME }
});
console.log('[3] add_knowledge ...');
const addOut = run(SKILL + '/ima_api.cjs', ['openapi/wiki/v1/add_knowledge', addBody]);
console.log('    add_knowledge ->', addOut.trim().slice(0, 300));
console.log('DONE ✅');
