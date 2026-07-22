# Data

Place your spatial analysis data here:
- Floor plan JSON files
- Room connectivity CSV files
- Site boundary GeoJSON files
- Building facade images

## Format

Room data should follow this structure:
`json
{
  \"name\": \"Room Name\",
  \"area\": 100,
  \"type\": \"public|private|circulation\",
  \"connections\": [0, 1, 2],
  \"level\": 0
}
`
"@ | Out-File -FilePath "C:\Users\12275\Documents\Codex\2026-07-22\neng\outputs\github\Arch-Spatial-Intelligence\data\README.md" -Encoding UTF8

# docs 占位
@"
# Documentation

## Methodology

### Space Syntax Analysis
The spatial analyzer uses graph-theoretic methods to compute:
- **Connectivity**: Number of direct connections per space
- **Integration**: How integrated a space is in the overall system
- **Choice**: How likely a space is to be passed through

### Facade Classification
Computer vision analysis of building facades:
- Architectural style matching
- Window-to-wall ratio computation
- Symmetry and regularity analysis

### Report Generation
Automated report generation in Markdown format:
- Spatial metrics summary
- Design comparison tables
- Facade analysis results

## Output Format

Reports are generated as Markdown files that can be:
- Viewed directly on GitHub
- Exported to PDF
- Embedded in portfolio documentation
