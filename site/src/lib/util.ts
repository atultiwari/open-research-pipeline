// Small shared helpers for labels, links and scoring.
import type { CollectionEntry } from 'astro:content';

export const REPO = 'atultiwari/open-research-pipeline';
export const REPO_URL = `https://github.com/${REPO}`;

export const AREA_LABEL: Record<string, string> = {
  'computational-pathology': 'Computational pathology',
  'gastro-hepatology': 'Gastro & hepatology AI',
  'clinical-data-llm': 'Clinical data & LLMs',
  'healthcare-cybersecurity': 'Healthcare cybersecurity',
};

export const STATUS_ORDER = [
  'new', 'approved', 'protocol', 'analysis', 'drafting', 'preprint', 'submitted', 'published', 'parked', 'rejected',
] as const;

export const TIER_LABEL: Record<string, string> = {
  laptop: 'Laptop', colab: 'Colab', runpod: 'RunPod GPU', api: 'API',
};

export const ACCESS_LABEL: Record<string, string> = {
  open: 'Open', 'free-registration': 'Free registration', credentialed: 'Credentialed',
};

const ACCESS_RANK = { open: 0, 'free-registration': 1, credentialed: 2 } as const;
type Access = keyof typeof ACCESS_RANK;

/** Join a site-relative path onto the configured base (e.g. "/open-research-pipeline/"). */
export function url(path = ''): string {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  const clean = path.replace(/^\//, '');
  if (!clean) return `${base}/`;
  return /[#?]|\.\w+$/.test(clean) ? `${base}/${clean}` : `${base}/${clean.replace(/\/?$/, '/')}`;
}

export const editUrl = (repoPath: string) => `${REPO_URL}/edit/main/${repoPath}`;
export const viewUrl = (repoPath: string) => `${REPO_URL}/blob/main/${repoPath}`;

export const isVerify = (v: unknown): boolean => typeof v === 'string' && /\bverify\b/i.test(v);

export const headline = (s: CollectionEntry<'studies'>['data']) => s.scores.feasibility * s.scores.novelty;

/** Most restrictive access level across a study's datasets. */
export function studyAccess(
  study: CollectionEntry<'studies'>['data'],
  datasets: Map<string, CollectionEntry<'datasets'>['data']>,
): Access {
  return study.datasets.reduce<Access>((worst, d) => {
    const a = (datasets.get(d.id)?.access ?? 'open') as Access;
    return ACCESS_RANK[a] > ACCESS_RANK[worst] ? a : worst;
  }, 'open');
}

export const isUrl = (v: unknown): v is string => typeof v === 'string' && /^https?:\/\//.test(v);
