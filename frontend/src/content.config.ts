import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// TODO: Load switches from backend
const switchCollection = defineCollection({
  loader: glob({ pattern: '**/[^_]*.md', base: "./src/data/switches" }),
  schema: () =>
    z.object({
      id: z.string(),
      name: z.string(),
      content: z.string(),
    }),
});

export const collections = {
  switches: switchCollection,
};
