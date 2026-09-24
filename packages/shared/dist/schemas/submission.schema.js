"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.CreateSubmissionSchema = void 0;
const zod_1 = require("zod");
exports.CreateSubmissionSchema = zod_1.z.object({
    submission_url_or_file: zod_1.z.string().trim().min(1, 'Submission content or link is required'),
    notes: zod_1.z.string().trim().max(1000, 'Notes cannot exceed 1000 characters').optional()
});
//# sourceMappingURL=submission.schema.js.map