import { z } from "zod";

export const GetDevtoolsUrlSchema = z.object({
  pageId: z.string().optional(),
});

export default {
  GetDevtoolsUrlSchema,
};
