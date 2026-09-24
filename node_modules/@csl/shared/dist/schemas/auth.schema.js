"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.LoginSchema = exports.RegisterStudentSchema = void 0;
const zod_1 = require("zod");
exports.RegisterStudentSchema = zod_1.z.object({
    first_name: zod_1.z.string().trim().min(1, 'First name is required').max(100),
    last_name: zod_1.z.string().trim().min(1, 'Last name is required').max(100),
    email: zod_1.z.string().trim().email('Invalid email address').toLowerCase(),
    password: zod_1.z.string().min(8, 'Password must be at least 8 characters long'),
    student_identifier: zod_1.z.string().trim().min(1, 'Student ID / Identifier is required').max(50),
    batch_id: zod_1.z.string().uuid('Invalid batch ID').optional()
});
exports.LoginSchema = zod_1.z.object({
    email: zod_1.z.string().trim().email('Invalid email address').toLowerCase(),
    password: zod_1.z.string().min(1, 'Password is required')
});
//# sourceMappingURL=auth.schema.js.map