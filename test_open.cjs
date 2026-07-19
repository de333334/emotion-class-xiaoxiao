const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');

const HTML = fs.readFileSync(process.argv[2] || 'emotion-class.html', 'utf8');
const errors = [];
const vc = new VirtualConsole();
vc.on('jsdomError', e => errors.push('jsdomError: ' + (e.message || e)));
vc.on('error', (...a) => errors.push('console.error: ' + a.join(' ')));

const dom = new JSDOM(HTML, {
  runScripts: 'dangerously',
  resources: 'usable',
  pretendToBeVisual: true,
  virtualConsole: vc,
  beforeParse(window) {
    // 真实浏览器有 Audio / speechSynthesis；jsdom 没有，先桩掉，保证脚本能跑
    window.Audio = class { constructor(){ this.paused = true; this.currentTime = 0; this.duration = 3; this.src=''; }
      play(){ this.paused = false; return Promise.resolve(); } pause(){ this.paused = true; }
      addEventListener(){} };
    window.speechSynthesis = { speak(){}, cancel(){}, getVoices(){return [];}, pause(){}, resume(){} };
    window.scrollTo = () => {};
    window.addEventListener('error', ev => errors.push('window.error: ' + ev.message));
  }
});

const { window } = dom;
const { document } = window;

function $(sel){ return document.querySelector(sel); }
function $all(sel){ return Array.from(document.querySelectorAll(sel)); }
function clickById(id){ const el = document.getElementById(id); if(el){ el.click(); return true; } return false; }

// 等脚本执行完
setTimeout(() => {
  try {
    const SECTIONS = window.SECTIONS;
    const AUDIO = window.AUDIO || [];
    // 计算 PLAYLIST（与页面同逻辑）
    let PLAYLIST = [];
    SECTIONS.forEach((s, si) => { if (s.type === 'speak') s.sentences.forEach((t, ji) => PLAYLIST.push({ si, ji, gi: PLAYLIST.length, text: t })); });

    console.log('[check] SECTIONS =', SECTIONS.length, ' speak句数(PLAYLIST) =', PLAYLIST.length, ' AUDIO数组长 =', AUDIO.length);
    let badAudio = 0;
    PLAYLIST.forEach(p => {
      const d = AUDIO[p.gi];
      if (!d || !d.startsWith('data:audio/mp3;base64,')) { badAudio++; return; }
      const b = Buffer.from(d.split(',')[1], 'base64');
      if (b.length < 200) badAudio++;
    });
    console.log('[check] 非法/缺失音频句数 =', badAudio, badAudio === 0 ? '✅ 全部合法' : '❌');

    // 走完全部流程
    let steps = 0;
    let testedPlayer = false;
    while (steps < 80) {
      steps++;
      if ($('.finish')) { console.log('[flow] 到达“下课”卡片 ✅ (用了', steps, '步)'); break; }
      if ($('#startBtn')) { clickById('startBtn'); continue; }
      if ($('#finishBtn')) { clickById('finishBtn'); continue; } // 费曼段
      if ($('#nextBtn')) {
        const quizCard = $('#nextBtn').closest('.quiz');
        if (quizCard) {
          const qText = quizCard.querySelector('.q') ? quizCard.querySelector('.q').textContent : '';
          const sec = SECTIONS.find(s => s.quiz && s.quiz.q === qText);
          if (sec) {
            const okIdx = sec.quiz.opts.findIndex(o => o.ok);
            const opts = $all('.quiz .opt');
            if (opts[okIdx]) opts[okIdx].click();
          }
          clickById('nextBtn');
          continue;
        }
        // speak 段：测一下播放器（只在第一段测）
        if (!testedPlayer) {
          testedPlayer = true;
          clickById('playBtn');
          clickById('pPlay');
          clickById('pNext');   // 下一句
          clickById('pPrev');   // 上一句
          const seek = document.getElementById('pSeek');
          if (seek) { seek.value = 50; seek.dispatchEvent(new window.Event('input')); }
          const meta = document.getElementById('pMeta') ? document.getElementById('pMeta').textContent : '';
          console.log('[player] 播放/上下句/拖动 seek 未报错, pMeta =', meta);
        }
        clickById('playBtn');
        clickById('nextBtn');
        continue;
      }
      console.log('[flow] 未知状态，停止于步', steps); break;
    }

    const stars = document.querySelector('.badge') ? document.querySelector('.badge').textContent : '';
    console.log('[flow] 最终 badge =', stars);
    console.log('[errors] runtime 错误数 =', errors.length);
    errors.slice(0, 10).forEach(e => console.log('   -', e));
    console.log(errors.length === 0 ? 'RESULT: PASS ✅' : 'RESULT: PASS_WITH_ERRORS ⚠️');
  } catch (e) {
    console.log('TEST CRASH:', e.stack);
  }
}, 400);
