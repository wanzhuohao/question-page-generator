// 验证图形渲染输出
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, '..', 'assets', 'template.html'), 'utf-8');
const scriptContent = html.match(/<script>([\s\S]*)<\/script>/)[1];

// 提取所有需要的函数（用更宽松的正则）
const functions = [
  'renderQuestionText',
  'renderShape',
  'renderGridShape',
  'renderTriangleShape',
  'renderSquareShape',
  'normalizeAnswer',
  'onShapeInput',
];

let code = '';
functions.forEach(name => {
  // 匹配 "function name(...) { ... }" 到下一个 "// ======" 或文件结束
  const re = new RegExp('function ' + name + '\\([\\s\\S]*?\\n\\}\\n', 'm');
  const m = scriptContent.match(re);
  if (m) code += m[0] + '\n';
  else console.log('WARNING: 未提取到 ' + name);
});

// 执行提取的代码
eval(code);

// 测试 normalizeAnswer
console.log('=== normalizeAnswer 测试 ===');
const testCases = [
  { type: 'hundredChart', answer: '["34"]' },
  { type: 'triangle', answer: '["7","5","6"]' },
  { type: 'square', answer: '["7","5","3","5"]' },
  { type: 'add', answer: '19' },
];
testCases.forEach(t => {
  normalizeAnswer(t);
  console.log(`${t.type}: "${t.answer}"`);
});

// 测试 renderQuestionText (shape 类型)
console.log('\n=== renderQuestionText (shape) ===');
const shapeTexts = [
  { type: 'hundredChart', expr: '{"rows":3,...}' },
  { type: 'triangle', expr: '{"target":10,...}' },
  { type: 'square', expr: '{"target":10,...}' },
];
shapeTexts.forEach(t => {
  console.log(`${t.type}: "${renderQuestionText(t)}"`);
});

// 测试 renderShape
console.log('\n=== renderShape 验证 ===\n');

// 百数表
const hcData = JSON.stringify({
  rows: 3, cols: 3,
  cellMap: { '0,0': '23', '0,1': '24', '0,2': '25', '1,0': '33', '1,2': '35', '2,0': '43', '2,1': '44', '2,2': '45' },
  hiddenKeys: ['1,1']
});
console.log('百数表 (grid):');
console.log(renderShape({ type: 'hundredChart', expr: hcData }, 0));
console.log();

// 三角形
const triData = JSON.stringify({
  target: 10,
  vals: { A: 1, B: 2, C: 3, AB: 7, BC: 5, AC: 6 },
  shown: ['A', 'B', 'C'],
  hidden: ['AB', 'BC', 'AC']
});
console.log('三角形:');
console.log(renderShape({ type: 'triangle', expr: triData }, 0));
console.log();

// 方形
const sqData = JSON.stringify({
  target: 10,
  vals: { A: 1, B: 2, C: 3, D: 4, AB: 7, BC: 5, CD: 3, DA: 5 },
  shown: ['A', 'B', 'C', 'D'],
  hidden: ['AB', 'BC', 'CD', 'DA']
});
console.log('方形:');
console.log(renderShape({ type: 'square', expr: sqData }, 0));
