---
description: Convert external documents to markdown
---

# Convert Document to Markdown

Convert document to markdown: $ARGUMENTS

## Arguments

- **file-path** (required): Path to document file

## Supported Formats

- Word (.docx)
- PDF (.pdf)
- PowerPoint (.pptx)
- Excel (.xlsx)
- HTML (.html)
- Images (with OCR)

## Examples

- `/convert-doc ./legacy/design-doc.docx`
- `/convert-doc ./specs/api.pdf`
- `/convert-doc ./data/spreadsheet.xlsx`
- `/convert-doc ./presentation/slides.pptx`

## Task

You are tasked with converting an external document to markdown format using the MarkItDown MCP server.

### Argument Parsing

Parse $ARGUMENTS to extract:
1. **File path** (required) - the document to convert

Validate that the file:
- Exists and is accessible
- Has a supported file extension
- Is not empty

## Conversion Process

### 1. File Analysis

Analyze the input file:
- Check file type and extension
- Verify file size (warn if very large)
- Detect document structure

### 2. Use MarkItDown MCP

Invoke the MarkItDown MCP server to convert the file:

```javascript
// Use the markitdown_convert tool
const result = await markitdown_convert({
  file_path: filePath
});
```

### 3. Format Preservation

The converter will attempt to preserve:
- **Text formatting** (bold, italic, headers)
- **Tables** (converted to markdown tables)
- **Lists** (ordered and unordered)
- **Images** (converted to markdown image references)
- **Links** (preserved as markdown links)
- **Code blocks** (if detected)

### 4. Post-Processing

After conversion, improve the markdown:
- Fix heading hierarchy (ensure proper levels)
- Clean up excessive whitespace
- Normalize table formatting
- Add language specifiers to code blocks
- Fix broken links or image references
- Apply markdown best practices

### 5. Output Handling

Present the converted content and ask the user:

```markdown
Conversion complete! The document has been converted to markdown.

Preview (first 100 lines):
[Show preview of converted content]

Would you like to:
1. Save to a file (default: same name with .md extension)
2. Copy to clipboard
3. Display full content
4. Save with custom filename

What would you like to do?
```

## Format-Specific Handling

### Word Documents (.docx)

- Preserve document structure (headings, paragraphs)
- Convert tables to markdown tables
- Extract images and save separately
- Handle comments as markdown notes
- Preserve formatting (bold, italic, code)

### PDF Documents (.pdf)

- Extract text content
- Attempt to preserve structure
- Handle multi-column layouts
- Extract images if possible
- Note: Complex PDFs may need manual cleanup

### PowerPoint (.pptx)

- Convert each slide to a section
- Slide title becomes heading
- Bullet points preserved
- Speaker notes as blockquotes
- Images extracted

### Excel (.xlsx)

- Convert sheets to markdown tables
- Each sheet becomes a section
- Preserve formulas as code blocks
- Handle multiple sheets

### HTML (.html)

- Convert HTML to clean markdown
- Remove unnecessary markup
- Preserve semantic structure
- Clean up inline styles

### Images (with OCR)

- Perform OCR to extract text
- Generate markdown with extracted text
- Include original image as reference

## Best Practices

- Validate the converted output
- Check for formatting issues
- Verify links and references
- Test tables render correctly
- Ensure code blocks are properly formatted

## Error Handling

Handle common errors:
- File not found
- Unsupported format
- Conversion failure
- Empty output
- Encoding issues

Provide helpful error messages:

```
Error: File not found at './specs/api.pdf'
Please check the file path and try again.

Error: Unsupported file format '.doc'
Supported formats: .docx, .pdf, .pptx, .xlsx, .html, images

Error: Conversion failed - file may be corrupted
Try opening the file manually to verify it's valid.
```

## Output

Generate markdown content from the converted document and:
1. Display preview
2. Offer to save to file
3. Provide cleanup suggestions if needed
4. Report any conversion issues or limitations

## Example Output

```markdown
✓ Successfully converted './legacy/design-doc.docx' to markdown

File: design-doc.md
Size: 15.2 KB
Headings: 12
Tables: 3
Images: 5

Preview:
# System Design Document

## Overview

This document describes the architecture...

[Rest of content]

Save to './legacy/design-doc.md'? [Y/n]
```
