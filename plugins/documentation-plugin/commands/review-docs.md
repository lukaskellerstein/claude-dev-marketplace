---
description: Review and score documentation quality with detailed feedback and improvement recommendations
---

Perform a comprehensive review of project documentation with quality scoring and actionable recommendations.

## Process

Follow these steps:

1. **Discover Documentation**: Find all documentation files
   - README.md
   - CHANGELOG.md
   - API documentation
   - Architecture docs
   - ADRs
   - Code comments and docstrings
   - Contributing guides
   - Any other .md files

2. **Launch Documentation Reviewer**: Use the `documentation-plugin:documentation-reviewer` agent to:
   - Assess coverage (what's documented vs. what should be)
   - Verify accuracy (is information correct and current?)
   - Evaluate clarity (is it easy to understand?)
   - Check examples (do they work and are they helpful?)
   - Review structure (is it well-organized?)
   - Assess completeness (are edge cases covered?)
   - Evaluate accessibility (is it inclusive and readable?)
   - Check maintainability (is it easy to keep updated?)

3. **Calculate Scores**: Generate quantitative scores for:
   - Overall documentation health (0-10)
   - Individual dimension scores
   - Weighted overall score
   - Grade (A+, A, B, C, D, F)

4. **Generate Report**: Create detailed review report with:
   - Executive summary
   - Detailed scores by dimension
   - Strengths and weaknesses
   - Critical issues requiring immediate attention
   - Improvement recommendations
   - Prioritized action plan

## Output

Present a comprehensive documentation review including:

### Executive Summary
```
Overall Score: 7.8/10 (B)

Documentation Health: Good

Key Strengths:
- Comprehensive API documentation with examples
- Well-structured README with clear installation steps
- Active CHANGELOG following Keep a Changelog format

Critical Issues:
- Missing architecture documentation
- No troubleshooting guide in README
- Several broken links in API docs

Top 3 Recommendations:
1. Create architecture documentation with diagrams
2. Add troubleshooting section to README
3. Fix broken links and update outdated examples
```

### Detailed Scores

```markdown
| Dimension        | Score | Grade | Weight | Weighted |
|------------------|-------|-------|--------|----------|
| Coverage         | 7/10  | B     | 20%    | 1.40     |
| Accuracy         | 8/10  | B+    | 20%    | 1.60     |
| Clarity          | 8/10  | B+    | 15%    | 1.20     |
| Examples         | 9/10  | A     | 15%    | 1.35     |
| Structure        | 7/10  | B     | 10%    | 0.70     |
| Completeness     | 6/10  | C     | 10%    | 0.60     |
| Accessibility    | 8/10  | B+    | 5%     | 0.40     |
| Maintainability  | 7/10  | B     | 5%     | 0.35     |
| **TOTAL**        | **7.8/10** | **B** | **100%** | **7.60** |
```

### Findings by Category

#### Coverage (7/10)
**What's Documented:**
- ✓ Installation and setup
- ✓ API reference
- ✓ Basic usage examples
- ✓ Configuration options

**What's Missing:**
- ✗ Architecture documentation
- ✗ Troubleshooting guide
- ✗ Advanced usage scenarios
- ✗ Performance tuning guide

#### Accuracy (8/10)
**Strengths:**
- API documentation matches current codebase
- Code examples are mostly current
- Dependencies are up-to-date

**Issues:**
- Authentication example uses deprecated method
- Database connection string format is outdated
- One broken example in WebSocket section

#### Clarity (8/10)
**Strengths:**
- Clear, concise language
- Good use of headings
- Logical flow

**Issues:**
- Some technical jargon not defined
- Could benefit from more context in places
- Passive voice used in several sections

#### Examples (9/10)
**Strengths:**
- Comprehensive examples throughout
- Real-world scenarios covered
- Code is well-formatted and commented
- Multiple language examples provided

**Issues:**
- One example doesn't handle errors
- Could add more edge case examples

#### Structure (7/10)
**Strengths:**
- Clear table of contents
- Logical organization
- Good use of sections

**Issues:**
- README is getting too long, consider splitting
- Some inconsistent heading levels
- Could improve cross-referencing

#### Completeness (6/10)
**Strengths:**
- Core functionality well documented
- Basic error scenarios covered

**Issues:**
- Edge cases not fully documented
- Missing performance considerations
- Security best practices not covered
- No migration guides

#### Accessibility (8/10)
**Strengths:**
- Good heading structure
- Most images have alt text
- Inclusive language used

**Issues:**
- A few images missing alt text
- Some code blocks missing language labels
- Could improve contrast in examples

#### Maintainability (7/10)
**Strengths:**
- Documentation in version control
- Close to code
- Regular updates

**Issues:**
- No automated validation
- Some manual sections prone to drift
- Unclear ownership for some docs

### Issues by Priority

#### Critical (Fix Immediately)
1. **Broken Authentication Example**
   - Impact: Users cannot authenticate successfully
   - Location: README.md, line 145
   - Fix: Update to use OAuth2 instead of deprecated API keys
   - Effort: Small

2. **Missing Architecture Documentation**
   - Impact: Difficult for new developers to understand system
   - Location: docs/ directory
   - Fix: Create architecture overview with diagrams
   - Effort: Large

#### High Priority (Fix Soon)
3. **Outdated Database Connection String**
   - Impact: Users may have connection issues
   - Location: CONFIGURATION.md
   - Fix: Update to current format
   - Effort: Small

4. **No Troubleshooting Guide**
   - Impact: Users struggle with common issues
   - Location: README.md
   - Fix: Add troubleshooting section with common issues
   - Effort: Medium

#### Medium Priority (Plan to Fix)
5. **Missing Advanced Usage Examples**
   - Impact: Users can't learn advanced features
   - Fix: Add advanced usage section
   - Effort: Medium

6. **Inconsistent Heading Levels**
   - Impact: Navigation and structure unclear
   - Fix: Normalize heading hierarchy
   - Effort: Small

#### Low Priority (Nice to Have)
7. **Add More Visual Diagrams**
   - Impact: Better understanding of concepts
   - Fix: Add more Mermaid diagrams
   - Effort: Medium

8. **Improve Code Comments**
   - Impact: Better code understanding
   - Fix: Add more inline documentation
   - Effort: Large

### Recommendations

For each major issue, provide:

**1. Create Architecture Documentation**
- **Current State**: No architecture documentation exists
- **Impact**: New team members struggle to understand system design
- **Recommendation**: Create docs/architecture/ with:
  - System overview diagram
  - Component diagrams
  - Key sequence flows
  - Data model
  - ADRs for major decisions
- **Effort**: 2-3 days
- **Priority**: High
- **Benefit**: Significantly improves onboarding and system understanding

**2. Fix Broken Authentication Example**
- **Current State**: README shows deprecated authentication method
- **Impact**: Users cannot successfully authenticate
- **Recommendation**: Update README lines 145-160 to show OAuth2 flow
- **Effort**: 1 hour
- **Priority**: Critical
- **Benefit**: Unblocks users immediately

[Continue for other recommendations...]

### Improvement Plan

#### Week 1 (Critical Fixes)
- [ ] Fix broken authentication example
- [ ] Update database connection string format
- [ ] Fix broken links in API documentation
- [ ] Validate all code examples

#### Weeks 2-3 (High Priority)
- [ ] Create architecture documentation with diagrams
- [ ] Add troubleshooting section to README
- [ ] Document error handling patterns
- [ ] Add migration guides

#### Month 2 (Medium Priority)
- [ ] Add advanced usage examples
- [ ] Improve code documentation
- [ ] Normalize heading structure
- [ ] Add performance tuning guide

#### Ongoing (Low Priority)
- [ ] Add more diagrams
- [ ] Improve accessibility
- [ ] Set up automated validation
- [ ] Regular review and updates

### Comparison to Best Practices

**Industry Standards**
- Keep a Changelog: ✓ Following
- Semantic Versioning: ✓ Following
- OpenAPI Spec: ✓ Following
- Markdown Best Practices: ~ Mostly following

**Similar Projects**
Compared to top 3 similar projects:
- Your project: 7.8/10
- Project A: 8.5/10 (better architecture docs)
- Project B: 7.2/10 (fewer examples)
- Project C: 8.0/10 (better troubleshooting)

**Documentation Maturity Level**
Current: Level 3 (Good) - Comprehensive docs with some gaps
Target: Level 4 (Excellent) - Complete, maintained, exemplary

## Usage Scenarios

### Review All Documentation
```
/review-docs

Perform comprehensive review of all project documentation
with detailed scoring and improvement recommendations
```

### Review Specific Documentation
```
/review-docs

Review only the API documentation in docs/api/ and provide
feedback on completeness and accuracy
```

### Quick Health Check
```
/review-docs

Quick documentation health check focusing on critical issues
and highest priority improvements
```

### Compare to Standards
```
/review-docs

Review documentation and compare to industry best practices
and similar projects in the ecosystem
```

## Review Dimensions

### Coverage (20%)
Are all necessary topics documented?

### Accuracy (20%)
Is information correct and up-to-date?

### Clarity (15%)
Is it easy to understand?

### Examples (15%)
Are examples sufficient and working?

### Structure (10%)
Is it well-organized?

### Completeness (10%)
Are edge cases covered?

### Accessibility (5%)
Is it inclusive and readable?

### Maintainability (5%)
Is it easy to keep updated?

## Best Practices Applied

- **Comprehensive**: Review all documentation types
- **Quantitative**: Provide numerical scores
- **Actionable**: Give specific recommendations
- **Prioritized**: Order by impact and effort
- **Constructive**: Focus on improvement
- **Evidence-Based**: Reference specific examples
- **Comparative**: Compare to standards
- **Structured**: Organize findings clearly

## Quality Checklist

Review includes:
- [ ] Overall score and grade
- [ ] Detailed scores by dimension
- [ ] Executive summary
- [ ] Findings by category
- [ ] Issues prioritized by severity
- [ ] Specific recommendations with effort estimates
- [ ] Improvement plan with timeline
- [ ] Comparison to best practices
- [ ] Before/after examples where helpful

Provide a comprehensive, actionable documentation review that enables immediate improvements.
