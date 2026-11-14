// Review data and arithmetic are independent of the UI and export renderer.
export const MODES = ['systematic', 'scoping', 'narrative'];
export const COUNT_PATTERN = /\(\s*n\s*=\s*[^)]*\)/g;
export const MAX_COUNT = 1_000_000_000;
export const ORIGINAL_FOOTNOTES = '*Consider, if feasible to do so, reporting the number of records identified from each database or register searched (rather than the total number across all databases/registers).\n**If automation tools were used, indicate how many records were excluded by a human and how many were excluded by automation tools.\n\nSource: Page MJ, et al. BMJ 2021;372:n71. doi: 10.1136/bmj.n71.\nThis work is licensed under CC BY 4.0. To view a copy of this license, visit https://creativecommons.org/licenses/by/4.0/';

export const MODE_INFO = {
  systematic: { short: 'PRISMA 2020' },
  scoping: { short: 'PRISMA-ScR adaptation'},
  narrative: { short: 'Narrative adaptation'}
};

export function createReview(mode = 'systematic') {
  const narrative = mode === 'narrative';
  const texts = {
    dbHeader: 'Identification of studies via databases and registers',
    otherHeader: 'Identification of studies via other methods',
    phaseIdentification: 'Identification', phaseScreening: 'Screening', phaseIncluded: 'Included',
    dbSources: 'Records identified from*:\nDatabases (n = )\nRegisters (n = )',
    removed: 'Records removed before screening:\nDuplicate records removed  (n = )\nRecords marked as ineligible by automation tools (n = )\nRecords removed for other reasons (n = )',
    otherSources: 'Records identified from:\nWebsites (n = )\nOrganisations (n = )\nCitation searching (n = )\netc.',
    screened: 'Records screened\n(n = )', excluded: 'Records excluded**\n(n = )',
    sought: 'Reports sought for retrieval\n(n = )', notRetrieved: 'Reports not retrieved\n(n = )',
    assessed: 'Reports assessed for eligibility\n(n = )',
    dbReasons: 'Reports excluded:\nReason 1 (n = )\nReason 2 (n = )\nReason 3 (n = )\netc.',
    otherSought: 'Reports sought for retrieval\n(n = )', otherNotRetrieved: 'Reports not retrieved\n(n = )',
    otherAssessed: 'Reports assessed for eligibility\n(n = )',
    otherReasons: 'Reports excluded:\nReason 1 (n = )\nReason 2 (n = )\nReason 3 (n = )\netc.',
    included: 'Studies included in review\n(n = )\nReports of included studies\n(n = )',
    footnotes: ORIGINAL_FOOTNOTES
  };
  if (mode === 'scoping') {
    texts.dbHeader = 'Identification of sources of evidence via databases and registers';
    texts.otherHeader = 'Identification of sources of evidence via other methods';
    texts.included = 'Sources of evidence included in review\n(n = )';
    texts.footnotes = ORIGINAL_FOOTNOTES + '\nAdapted for scoping reviews: Tricco AC, et al. PRISMA-ScR. Ann Intern Med. 2018;169:467–473. doi: 10.7326/M18-0850.';
  }
  if (narrative) {
    Object.assign(texts, {
      dbHeader: 'Identification of literature',
      dbSources: 'Records identified from:\nDatabases (n = )\nOther sources (n = )',
      removed: 'Records removed before screening:\nDuplicate records removed (n = )\nRecords removed for other reasons (n = )',
      excluded: 'Records excluded\n(n = )',
      sought: 'Full-text articles sought for retrieval\n(n = )',
      notRetrieved: 'Full-text articles not retrieved\n(n = )',
      assessed: 'Full-text articles assessed for relevance\n(n = )',
      dbReasons: 'Full-text articles excluded:\nReason 1 (n = )\nReason 2 (n = )\nReason 3 (n = )\netc.',
      included: 'Articles included in narrative review\n(n = )',
      footnotes: 'Literature-selection diagram adapted from the PRISMA 2020 structure. This is not an official PRISMA or SANRA template.\nPRISMA source: Page MJ, et al. BMJ 2021;372:n71. doi: 10.1136/bmj.n71. CC BY 4.0: https://creativecommons.org/licenses/by/4.0/\nSearch-description guidance: Baethge C, Goldbeck-Wood S, Mertens S. SANRA. Res Integr Peer Rev. 2019;4:5. doi: 10.1186/s41073-019-0064-8.'
    });
  }
  return {
    mode, texts, values: {}, showOther: !narrative, fontSize: 18, nextId: 1,
    groups: {
      dbSources: narrative ? ['databases', 'narrativeOther'] : ['databases', 'registers'],
      removed: narrative ? ['duplicates', 'removedOther'] : ['duplicates', 'automation', 'removedOther'],
      otherSources: ['websites', 'organisations', 'citations'],
      dbReasons: ['dbReason1', 'dbReason2', 'dbReason3'],
      otherReasons: ['otherReason1', 'otherReason2', 'otherReason3']
    }
  };
}

export function boxesFor(review) {
  return {
    dbSources: { title: 'Records identified', keys: review.groups.dbSources, add: 'source' },
    removed: { title: 'Removed before screening', keys: review.groups.removed },
    otherSources: { title: 'Records identified', keys: review.groups.otherSources, add: 'source' },
    screened: { title: 'Records screened', keys: ['screened'] },
    excluded: { title: 'Records excluded', keys: ['excluded'] },
    sought: { title: 'Sought for retrieval', keys: ['sought'] },
    notRetrieved: { title: 'Not retrieved', keys: ['notRetrieved'] },
    assessed: { title: review.mode === 'narrative' ? 'Assessed for relevance' : 'Assessed for eligibility', keys: ['assessed'] },
    dbReasons: { title: 'Excluded with reasons', keys: review.groups.dbReasons, add: 'reason' },
    otherSought: { title: 'Sought for retrieval', keys: ['otherSought'] },
    otherNotRetrieved: { title: 'Not retrieved', keys: ['otherNotRetrieved'] },
    otherAssessed: { title: 'Assessed for eligibility', keys: ['otherAssessed'] },
    otherReasons: { title: 'Excluded with reasons', keys: review.groups.otherReasons, add: 'reason' },
    included: { title: review.mode === 'systematic' ? 'Studies & reports' : review.mode === 'scoping' ? 'Sources of evidence' : 'Articles in the review', keys: review.mode === 'systematic' ? ['studies', 'includedReports'] : ['includedReports'] }
  };
}

export const CALCULATED_KEYS = ['screened', 'sought', 'assessed', 'otherSought', 'otherAssessed', 'includedReports'];
const hasValue = v => typeof v === 'number' && Number.isFinite(v);
const addNullable = values => values.some(hasValue) ? values.reduce((sum, v) => sum + (hasValue(v) ? v : 0), 0) : null;

export function calculate(review) {
  const values = {};
  const expected = {};
  const root = key => values[key] = hasValue(review.values[key]) ? review.values[key] : null;
  Object.values(review.groups).flat().forEach(root);
  ['excluded', 'notRetrieved', 'otherNotRetrieved', 'studies'].forEach(root);
  const sumGroup = id => addNullable(review.groups[id].map(key => values[key]));
  const subtract = (parent, deductions) => parent === null ? null : parent - (deductions ?? 0);
  const derived = (key, result) => {
    expected[key] = result;
    return values[key] = hasValue(review.values[key]) ? review.values[key] : result;
  };
  const identified = sumGroup('dbSources');
  derived('screened', subtract(identified, sumGroup('removed')));
  derived('sought', subtract(values.screened, values.excluded));
  derived('assessed', subtract(values.sought, values.notRetrieved));
  derived('otherSought', sumGroup('otherSources'));
  derived('otherAssessed', subtract(values.otherSought, values.otherNotRetrieved));
  const dbIncluded = subtract(values.assessed, sumGroup('dbReasons'));
  const otherIncluded = review.showOther ? subtract(values.otherAssessed, sumGroup('otherReasons')) : null;
  derived('includedReports', addNullable([dbIncluded, otherIncluded]));
  return { values, expected, identified, dbIncluded, otherIncluded };
}

export function countLabel(text, index) {
  const segments = text.split(COUNT_PATTERN);
  const prefix = segments[index] || '';
  const lines = prefix.trim().split('\n').filter(Boolean);
  return (lines.at(-1) || `Count ${index + 1}`).replace(/:$/, '').trim();
}

export function populateText(text, keys, values) {
  let index = 0;
  return text.replace(COUNT_PATTERN, match => {
    const value = values[keys[index++]];
    return value === null || value === undefined ? '(n = )' : `(n = ${value})`;
  });
}

export function addGroupRow(review, group) {
  if (!review.groups[group] || review.groups[group].length >= 40) return false;
  const isReason = group.endsWith('Reasons');
  const key = `custom${review.nextId++}`;
  const number = review.groups[group].length + 1;
  const line = `${isReason ? `Reason ${number}` : 'Additional source'} (n = )`;
  const text = review.texts[group];
  review.texts[group] = /\netc\.\s*$/.test(text) ? text.replace(/\netc\.\s*$/, `\n${line}\netc.`) : text + '\n' + line;
  review.groups[group].push(key);
  return true;
}

export function removeGroupRow(review, group, index) {
  const keys = review.groups[group];
  if (!keys || keys.length <= 1 || index < 0 || index >= keys.length) return false;
  // Remove the line containing this count marker. Preserve any custom surrounding prose.
  let count = 0;
  review.texts[group] = review.texts[group].split('\n').map(line => line.replace(COUNT_PATTERN, match => count++ === index ? '\u0000' : match)).filter(line => !line.includes('\u0000')).join('\n');
  delete review.values[keys[index]];
  keys.splice(index, 1);
  return true;
}

export function validate(review, result = calculate(review)) {
  const notices = [];
  const boxes = boxesFor(review);
  const activeIds = ['dbSources','removed','screened','excluded','sought','notRetrieved','assessed','dbReasons','included'];
  if (review.showOther) activeIds.push('otherSources','otherSought','otherNotRetrieved','otherAssessed','otherReasons');
  for (const id of activeIds) {
    const box = boxes[id];
    const matches = review.texts[id].match(COUNT_PATTERN) || [];
    if (matches.length !== box.keys.length) notices.push({ level: 'warning', text: `${box.title}: the wording contains ${matches.length} count markers for ${box.keys.length} counts. Use one (n = ) marker per count, in order.` });
    box.keys.forEach((key, index) => {
      const label = countLabel(review.texts[id], index);
      const value = result.values[key];
      if (value < 0) notices.push({ level: 'error', text: `${label} calculates to ${value}. Check the upstream counts and exclusions.` });
      if (CALCULATED_KEYS.includes(key) && hasValue(review.values[key]) && hasValue(result.expected[key]) && review.values[key] !== result.expected[key]) {
        notices.push({ level: 'warning', text: `${label} is manually set to ${value}; the upstream calculation gives ${result.expected[key]}.` });
      }
    });
  }
  if (result.dbIncluded !== null && result.dbIncluded < 0) notices.push({ level: 'error', text: 'Exclusion reasons in the main route exceed the number assessed for eligibility.' });
  if (review.showOther && result.otherIncluded !== null && result.otherIncluded < 0) notices.push({ level: 'error', text: 'Exclusion reasons in the other-methods route exceed the number assessed for eligibility.' });
  if (review.mode === 'systematic' && result.values.includedReports > 0 && result.values.studies === null) notices.push({ level: 'warning', text: 'Enter the number of unique included studies. Reports can describe the same study, so this count is not calculated.' });
  return notices;
}

export function sanitizeReview(raw, mode) {
  const clean = createReview(mode);
  if (!raw || typeof raw !== 'object' || Array.isArray(raw)) return clean;
  if (raw.texts && typeof raw.texts === 'object') for (const key of Object.keys(clean.texts)) {
    if (typeof raw.texts[key] === 'string') clean.texts[key] = raw.texts[key].slice(0, 12000);
  }
  const used = new Set();
  if (raw.groups && typeof raw.groups === 'object') for (const group of Object.keys(clean.groups)) {
    const keys = raw.groups[group];
    if (Array.isArray(keys) && keys.length && keys.length <= 40 && keys.every(key => typeof key === 'string' && (clean.groups[group].includes(key) || /^custom\d{1,6}$/.test(key))) && keys.every(key => !used.has(key)) && new Set(keys).size === keys.length) {
      clean.groups[group] = [...keys];
    }
    clean.groups[group].forEach(key => used.add(key));
  }
  const allowed = [...Object.values(clean.groups).flat(), ...CALCULATED_KEYS, 'excluded','notRetrieved','otherNotRetrieved','studies'];
  if (raw.values && typeof raw.values === 'object') for (const key of allowed) {
    if (Number.isSafeInteger(raw.values[key]) && raw.values[key] >= 0 && raw.values[key] <= MAX_COUNT) clean.values[key] = raw.values[key];
  }
  clean.fontSize = Number.isFinite(raw.fontSize) ? Math.min(26, Math.max(12, raw.fontSize)) : 18;
  clean.showOther = mode !== 'narrative' && raw.showOther !== false;
  // Reconstruct the next free ID rather than trusting imported metadata.
  clean.nextId = Math.max(0, ...allowed.filter(key => /^custom\d+$/.test(key)).map(key => Number(key.slice(6)))) + 1;
  return clean;
}

export function createProject() {
  return { version: 1, activeMode: 'systematic', reviews: Object.fromEntries(MODES.map(mode => [mode, createReview(mode)])) };
}

export function parseProject(text) {
  const raw = JSON.parse(text);
  if (!raw || raw.version !== 1 || !MODES.includes(raw.activeMode) || !raw.reviews || typeof raw.reviews !== 'object') throw new Error('Choose a PRISMA Flowchart project saved by this app.');
  return { version: 1, activeMode: raw.activeMode, reviews: Object.fromEntries(MODES.map(mode => [mode, sanitizeReview(raw.reviews[mode], mode)])) };
}
