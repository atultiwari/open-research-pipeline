// Content collections. These zod schemas mirror schema/*.schema.json, so an invalid entry fails the build.
import { defineCollection } from 'astro:content';
import { glob, file } from 'astro/loaders';
import { z } from 'astro/zod';
import { parse } from 'yaml';

const AREAS = ['computational-pathology', 'gastro-hepatology', 'clinical-data-llm', 'healthcare-cybersecurity'] as const;
const STATUSES = ['new', 'approved', 'protocol', 'analysis', 'drafting', 'preprint', 'submitted', 'published', 'parked', 'rejected'] as const;

const slug = z.string().regex(/^[a-z0-9]+(-[a-z0-9]+)*$/, 'kebab-case slug');
const score = z.number().int().min(1).max(5);
const urlOrVerify = z.string().regex(/^(https?:\/\/\S+|verify)$/, 'URL or "verify"');
const dateish = z.union([z.string(), z.date()]).transform((d) => (d instanceof Date ? d.toISOString().slice(0, 10) : d));

const studies = defineCollection({
  loader: glob({ pattern: '*/study.yaml', base: '../studies', generateId: ({ data }) => String(data.id) }),
  schema: z.strictObject({
    id: slug,
    legacy_id: z.string().optional(),
    title: z.string().min(10),
    area: z.enum(AREAS),
    tags: z.array(z.string()),
    status: z.enum(STATUSES),
    status_history: z.array(z.strictObject({ status: z.enum(STATUSES), date: dateish, note: z.string().optional() })).min(1),
    source: z.strictObject({
      type: z.enum(['preprint', 'journal', 'code', 'dataset', 'model']),
      title: z.string(),
      authors: z.string().optional(),
      venue: z.string().optional(),
      date: dateish.optional(),
      url: urlOrVerify,
      doi: z.string().regex(/^(10\.\d{4,9}\/\S+|verify)$/).optional(),
      arxiv_id: z.string().regex(/^(\d{4}\.\d{4,5}(v\d+)?|verify)$/).optional(),
      code_url: urlOrVerify.optional(),
      code_licence: z.string().optional(),
      code_note: z.string().optional(),
    }),
    datasets: z.array(z.strictObject({ id: slug, role: z.enum(['development', 'external-validation', 'benchmark']) })),
    study_type: z.string(),
    reporting_guideline: z.string(),
    novelty_delta: z.string().min(20),
    compute: z.strictObject({ tier: z.enum(['laptop', 'colab', 'runpod', 'api']), estimate: z.string() }),
    est_weeks: z.number().int().min(1).max(104),
    scores: z.strictObject({ feasibility: score, novelty: score, fit: score.nullable() }),
    risks: z.array(z.string()),
    access_actions: z.array(z.string()),
    candidate_journals: z.array(slug),
    links: z
      .strictObject({
        protocol: z.string().optional(),
        repo: z.string().optional(),
        preprint: z.string().optional(),
        journal_submission: z.string().optional(),
      })
      .optional(),
    added_at: dateish,
    added_by: z.enum(['atul', 'scout', 'claude-code']),
    run_id: z.string().optional(),
    last_reviewed: dateish.optional(),
  }),
});

// replication.md, extension.md, protocol.md and notes.md; id is "<slug>/<doc>".
const studyDocs = defineCollection({
  loader: glob({ pattern: '*/{replication,extension,protocol,notes}.md', base: '../studies' }),
  schema: z.object({ enriched: z.boolean().optional() }),
});

const datasets = defineCollection({
  loader: glob({ pattern: '*.yaml', base: '../datasets', generateId: ({ data }) => String(data.id) }),
  schema: z.strictObject({
    id: slug,
    name: z.string(),
    url: z.string().url(),
    alt_urls: z.array(z.string().url()).optional(),
    doi: z.string().optional(),
    modality: z.string(),
    organ_or_domain: z.string(),
    size: z.string().optional(),
    access: z.enum(['open', 'free-registration', 'credentialed']),
    licence: z.string(),
    licence_notes: z.string().optional(),
    institution_country: z.string().optional(),
    labels: z.string().optional(),
    citation: z.string().optional(),
    notes: z.string().optional(),
    last_checked: dateish.optional(),
  }),
});

const readYaml = (key: string) => (text: string) => {
  const rows = (parse(text)?.[key] ?? []) as Array<Record<string, unknown>>;
  return rows.map((r, i) => ({ id: String(r.id ?? `row-${i}`), ...r }));
};

const journals = defineCollection({
  loader: file('../journals/journals.yaml', { parser: readYaml('journals') }),
  schema: z.strictObject({
    id: slug,
    name: z.string(),
    publisher: z.string(),
    areas: z.array(z.enum(AREAS)).min(1),
    free_route: z.string(),
    first_decision: z.string().optional(),
    acceptance_to_online: z.string().optional(),
    fits: z.string().optional(),
    url: urlOrVerify,
    indexing: z.string().optional(),
    verify_flags: z.array(z.string()).optional(),
    notes: z.string().optional(),
    last_checked: dateish,
  }),
});

const excludedJournals = defineCollection({
  loader: file('../journals/journals.yaml', { parser: readYaml('excluded') }),
  schema: z.object({ name: z.string(), reason: z.string(), source: z.string().optional() }),
});

const preprints = defineCollection({
  loader: file('../journals/preprints.yaml', { parser: readYaml('servers') }),
  schema: z.object({
    name: z.string(),
    url: z.string().url(),
    best_for: z.string(),
    time_to_post: z.string().optional(),
    watch_for: z.string().optional(),
  }),
});

export const collections = { studies, studyDocs, datasets, journals, excludedJournals, preprints };
