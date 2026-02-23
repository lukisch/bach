import { de } from './de.js';
import { en } from './en.js';
import type { Translations } from './types.js';

type Lang = 'de' | 'en';
const langs: Record<Lang, Translations> = { de, en };
let current: Lang = (['de', 'en'].includes(process.env.CC_LANGUAGE || '')
  ? process.env.CC_LANGUAGE as Lang : 'de');

export function t(): Translations { return langs[current]; }
export function setLanguage(lang: Lang) { current = lang; }
export function getLanguage(): Lang { return current; }
export type { Lang, Translations };
