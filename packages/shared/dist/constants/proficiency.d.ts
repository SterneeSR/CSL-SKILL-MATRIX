export type ProficiencyLevel = 'FOUNDATIONAL' | 'DEVELOPING' | 'PROFICIENT' | 'ADVANCED';
export declare const PROFICIENCY_THRESHOLDS: {
    readonly FOUNDATIONAL: {
        readonly min: 0;
        readonly max: 49.99;
        readonly label: "Foundational";
    };
    readonly DEVELOPING: {
        readonly min: 50;
        readonly max: 69.99;
        readonly label: "Developing";
    };
    readonly PROFICIENT: {
        readonly min: 70;
        readonly max: 84.99;
        readonly label: "Proficient";
    };
    readonly ADVANCED: {
        readonly min: 85;
        readonly max: 100;
        readonly label: "Advanced";
    };
};
export declare const SKILL_COMPLETION_THRESHOLD = 70;
//# sourceMappingURL=proficiency.d.ts.map