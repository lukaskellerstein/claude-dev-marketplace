---
description: Analyze documentation health and provide score
---

# Documentation Health Score

Analyze documentation completeness and quality with a 0-100 health score.

## Task

You are tasked with analyzing the project's documentation health and providing a comprehensive score with actionable recommendations.

## Health Score Calculation

The documentation health score (0-100) is calculated across multiple dimensions:

### 1. Completeness (35 points)

**README.md (10 points)**
- Exists: 3 points
- Has description: 1 point
- Has installation instructions: 2 points
- Has usage examples: 2 points
- Has contributing link: 1 point
- Has license: 1 point

**CHANGELOG.md (5 points)**
- Exists: 2 points
- Follows Keep a Changelog format: 2 points
- Is up-to-date (updated in last 3 months): 1 point

**CONTRIBUTING.md (5 points)**
- Exists: 2 points
- Has development setup: 1 point
- Has PR process: 1 point
- Has code standards: 1 point

**API Documentation (10 points)** (if API exists)
- API docs exist: 4 points
- Has endpoint documentation: 3 points
- Has authentication docs: 2 points
- Has OpenAPI spec: 1 point

**Architecture Documentation (5 points)**
- Architecture docs exist: 2 points
- Has diagrams: 2 points
- Has ADRs: 1 point

### 2. Code Documentation (20 points)

**Inline Documentation**
- Public APIs documented: 8 points
- Classes/Modules documented: 6 points
- Complex functions documented: 6 points

### 3. Quality (25 points)

**Markdown Quality (10 points)**
- No markdown lint errors: 5 points
- Consistent formatting: 3 points
- Proper heading hierarchy: 2 points

**Link Health (8 points)**
- No broken internal links: 4 points
- No dead external links: 4 points

**Content Quality (7 points)**
- Examples are working: 3 points
- Up-to-date version numbers: 2 points
- No spelling errors: 2 points

### 4. Accessibility (10 points)

**Image Accessibility**
- Images have alt text: 3 points
- Diagrams are clear: 2 points

**Navigation**
- Has table of contents (if needed): 2 points
- Cross-references work: 3 points

### 5. Maintenance (10 points)

**Freshness**
- Docs updated in last 30 days: 4 points
- Docs match current code version: 3 points
- No outdated information: 3 points

## Health Score Ranges

- **90-100**: Excellent - Production-ready documentation
- **75-89**: Good - Solid documentation with minor gaps
- **60-74**: Fair - Acceptable but needs improvement
- **40-59**: Poor - Significant gaps, needs attention
- **0-39**: Critical - Documentation severely lacking

## Analysis Process

### 1. File Discovery

Scan the project for documentation:

```
Scanning for documentation...
✓ Found README.md
✓ Found CHANGELOG.md
✓ Found CONTRIBUTING.md
✓ Found docs/architecture/
✓ Found docs/api/
⊙ Missing LICENSE file
```

### 2. Content Analysis

Analyze each file:

```
Analyzing README.md...
✓ Has project description
✓ Has installation instructions
✓ Has usage examples
⊙ Missing screenshots
✗ No contributing link

Analyzing CHANGELOG.md...
✓ Follows Keep a Changelog format
✓ Latest entry: 2024-11-15 (2 days ago)
⊙ Some entries lack issue references

Analyzing code documentation...
Scanning 243 files...
✓ 89% of public APIs documented
⊙ 12% of classes lack docstrings
✗ 3 files with no documentation
```

### 3. Quality Checks

Run quality validations:

```
Checking documentation quality...
✓ Markdown: 2 minor style issues
✓ Links: All internal links valid
⚠ Links: 3 external links return 404
✓ Examples: 95% working (2 outdated)
✓ Versions: Consistent across docs
```

### 4. Calculate Score

Calculate the health score:

```markdown
# Documentation Health Score: 78/100

## Grade: Good ⭐⭐⭐⭐☆

Your documentation is solid with some areas for improvement.
```

## Health Report

Generate a comprehensive health report:

```markdown
# Documentation Health Report

Generated: 2024-11-16 18:45:00
Project: My Awesome Project
Version: 2.1.0

## Overall Health Score: 78/100

Grade: **Good** ⭐⭐⭐⭐☆

## Breakdown

### Completeness: 29/35 (83%)

✓ README.md: 9/10
  ✓ Exists and complete
  ⊙ Missing: Screenshots

✓ CHANGELOG.md: 5/5
  ✓ Up-to-date and well-formatted

✓ CONTRIBUTING.md: 4/5
  ⊙ Missing: Commit message conventions

✓ API Documentation: 8/10
  ✓ Comprehensive endpoint docs
  ⊙ Missing: Rate limiting documentation

⊙ Architecture Documentation: 3/5
  ✓ Has overview and diagrams
  ✗ Missing: ADRs

### Code Documentation: 17/20 (85%)

✓ Public APIs: 7/8 (89% documented)
✓ Classes/Modules: 5/6 (83% documented)
✓ Complex Functions: 5/6 (81% documented)

### Quality: 20/25 (80%)

✓ Markdown Quality: 8/10
  ✓ Clean, consistent formatting
  ⊙ 2 minor lint warnings

✓ Link Health: 6/8
  ✓ All internal links valid
  ⚠ 3 dead external links

✓ Content Quality: 6/7
  ✓ Examples working
  ⊙ 2 outdated code samples

### Accessibility: 8/10 (80%)

✓ Images: 3/3 (all have alt text)
✓ Navigation: 5/7
  ✓ Good cross-referencing
  ⊙ README could use TOC

### Maintenance: 8/10 (80%)

✓ Freshness: 8/10
  ✓ Recent updates (2 days ago)
  ✓ Version numbers current

## Strengths

1. ✓ Comprehensive README with all essential sections
2. ✓ Well-maintained CHANGELOG following best practices
3. ✓ Strong code documentation coverage (85%+)
4. ✓ No broken internal links
5. ✓ Good markdown quality

## Areas for Improvement

### High Priority

1. ✗ Create Architecture Decision Records (ADRs)
   Impact: +2 points
   Effort: Medium
   Action: Run `/adr` for each major decision

2. ⚠ Fix 3 dead external links
   Impact: +2 points
   Effort: Low
   Action: Update or remove dead links

3. ⊙ Add commit message conventions to CONTRIBUTING.md
   Impact: +1 point
   Effort: Low
   Action: Document Conventional Commits usage

### Medium Priority

4. ⊙ Add table of contents to README
   Impact: +1 point
   Effort: Low
   Action: Auto-generate TOC

5. ⊙ Update 2 outdated code examples
   Impact: +1 point
   Effort: Low
   Action: Review and test examples

6. ⊙ Add screenshots to README
   Impact: +1 point
   Effort: Medium
   Action: Capture key features

### Low Priority

7. ⊙ Document rate limiting in API docs
   Impact: +1 point
   Effort: Low

8. ⊙ Fix 2 minor markdown lint warnings
   Impact: +1 point
   Effort: Very low

## Quick Wins

These changes will boost your score quickly:

1. Fix 3 dead external links → +2 points (5 minutes)
2. Add TOC to README → +1 point (2 minutes)
3. Fix markdown lint warnings → +1 point (5 minutes)

Total quick wins: +4 points → Score would be 82/100 (Good)

## Recommendations by Role

### For Developers

- Document public APIs as you write them
- Update examples when changing functionality
- Run `/validate-docs` before releases

### For Maintainers

- Create ADRs for architectural decisions
- Keep CHANGELOG up-to-date
- Review documentation quarterly

### For Contributors

- Check CONTRIBUTING.md before starting
- Update docs with code changes
- Add examples for new features

## Metrics

### Documentation Coverage

- Files: 23 documented, 2 missing docs
- Public APIs: 89% documented (45/50)
- Classes: 83% documented (25/30)
- Functions: 81% documented (97/120)

### Documentation Age

- Last updated: 2 days ago
- Oldest doc: 45 days ago (still current)
- Update frequency: Weekly

### Link Health

- Total links: 127
- Internal: 89 (100% working)
- External: 38 (92% working, 3 dead)

## Trends

Compare with previous assessment (30 days ago):

- Overall score: 78/100 (+5 from last month) ↑
- Completeness: 83% (+8%) ↑
- Code docs: 85% (+2%) ↑
- Quality: 80% (unchanged) →
- Maintenance: 80% (+5%) ↑

## Next Actions

1. Run `/adr` to create missing ADRs
2. Fix dead external links in CONTRIBUTING.md
3. Add TOC to README: run auto-TOC generator
4. Update outdated code examples
5. Schedule monthly doc review

## Goal

Target score: 90/100 (Excellent)
Estimated effort: 2-3 hours
Timeline: Next sprint

## CI/CD Integration

Set up automated health checks:

```yaml
# .github/workflows/doc-health.yml
name: Documentation Health

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly
  push:
    paths:
      - '**.md'
      - 'docs/**'

jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check Documentation Health
        run: claude /doc-health
      - name: Fail if score < 70
        run: |
          score=$(get_health_score)
          if [ $score -lt 70 ]; then
            echo "Documentation health score too low: $score"
            exit 1
          fi
```
```

## Output

Generate comprehensive health report with:
- Overall score (0-100)
- Grade and rating
- Detailed breakdown by category
- Strengths and weaknesses
- Prioritized recommendations
- Quick wins for easy improvements
- Metrics and trends
- Actionable next steps
