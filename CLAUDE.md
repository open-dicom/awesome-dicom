# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

An [awesome list](https://awesome.re) of DICOM resources, published as `open-dicom/awesome-dicom`. The whole
product is `readme.md`, plus `archive.md` for projects that have left it; `contributing.md` holds the inclusion
rules. The only code is the CI under `.github/` (added in #38).

## Checking the list

- `npx awesome-lint` from the repo root runs the linter. The Lint workflow runs it on every PR that touches the
  list, with full history (its repo-age rule needs it) and `github_token` (lowercase) for the GitHub API.
- `python3 .github/scripts/check_list_structure.py readme.md` checks for duplicated entries and headings and for
  entries out of alphabetical order. Run it after any merge or rebase that touches `readme.md`; the Lint workflow
  runs it too.
- Scheduled workflows: `links.yml` (lychee, Mondays) and `staleness.yml` (`find_stale_entries.py`, first of the
  month). Each keeps one tracking issue current through `update_report_issue.sh`, and each also runs on PRs that
  change it, without touching issues. A full local run of `find_stale_entries.py` needs a `GITHUB_TOKEN`; without
  one, GitHub allows 60 API requests an hour, enough to test it on a small file.
- `find_stale_entries.py` exits 0 (clear), 3 (found problems) or 2 (couldn't finish); Python's own 1 means it
  crashed. Each workflow maps its tool's exit code to a status word (`passed`, `found-problems`, anything else =
  failed) for `update_report_issue.sh`. In `links.yml`, lychee runs in a read-only job (its binary is downloaded
  unverified) and a second job with `issues: write` runs only the issue script; both issue steps run only on main.
- GitHub pauses scheduled workflows after 60 days without commits; re-enable them from the Actions tab.
- `.github/staleness-exceptions.txt` lists repositories kept on purpose despite two years without commits
  (dicomParser), with a reason each. `.lycheeignore` lists hosts the link check skips: dicom.nema.org resets
  every connection from GitHub's runners, so check its links by hand.

## `readme.md` merges never conflict

`.gitattributes` sets `readme.md merge=union`. When both sides change the same region, git keeps both sides' lines
instead of reporting a conflict. The result looks clean but can contain duplicated entries, a duplicated section
heading, or entries out of order: commit 82f5216 removed duplicated OnkoDICOM and MRIcroGL entries left by one
such merge. Run the checks above after merging, and preview a merge with `git merge-tree` before doing it.

## Structure of `readme.md`

- Top-level sections, in order: Datasets, Hosted Tools, Learning Resources, Libraries, Tools, Related Lists and
  Contributing. awesome-lint's `awesome-toc` rule requires Related Lists and Contributing to stay out of Contents.
  The source citation for the intro is a GFM footnote at the very bottom.
- The structure is a hybrid. The sorting rule: **a library is something you use in your own code, and a tool is
  something you run.** Each project is listed once, where most people would look for it:
  - A package you can both import and run goes by what it is built for. Built for one of the Tools tasks: that task,
    even if its README calls it a library (dicom2nifti, deid, wsidicomizer, dcmqi). Otherwise a library: toolkits
    (DCMTK, dcm4che, pydicom, pynetdicom, python-gdcm, libdicom) and clients and SDKs (dicomweb-client, idc-index,
    MONAI Deploy App SDK). A package with no command line or app is a library (dcmjs-codecs). A "task" can be a
    field: PlatiPy, importable but with a CLI and built mainly for radiotherapy, sits under Radiation Therapy.
  - Related Lists qualify by curation activity: entries added in the last two years. A commit that only fixes
    formatting doesn't count.
  - A viewer you run is a tool. A viewer component you embed (DWV, NiiVue, Cornerstone3D) is a library.
  - **Datasets** has `###` groups: Research Collections and Test Files.
  - **Libraries** are grouped by language (`###`): C#, C and C++, Go, Java, JavaScript, Python, R and Rust. There
    is no `####` level.
  - **Tools** are grouped by task (`###`): Conversion, De-identification, Dose Monitoring, File Management,
    Gateways and Routing, Radiation Therapy, Research Platforms, Servers and PACS, Validation and Viewers. Only
    Viewers has a `####` level (Desktop and Web). A tool whose language matters to run it says so in its
    description ("MATLAB tool").
  - **Learning Resources** has `###` groups: The Standard, Guides and Tutorials, Books and Community. Never leave an
    empty heading.
  - Judgment call already made: innolitics/dicom-standard sits under The Standard although it is a pip package.
- The Contents list is maintained by hand and covers the `##` sections plus their `###` subsections. A new section
  of either level needs a Contents line. Slugs: C# is `#c`, and C and C++ is `#c-and-c`. The
  `<!-- omit in toc -->` comments keep the title and Contents heading out of the list.
- Hosted Tools has a privacy note under its intro about PHI and connecting hosted viewers to institutional
  DICOMweb servers. Keep it there.
- Link every entry straight to its repository. The old `tinyurl.com` workaround for awesome-lint's duplicate-link
  rule (65db92c) is gone since #35. If that rule fires again, put `<!--lint ignore double-link-->` above the entry
  rather than adding a redirect.
- DCMTK, GDCM, Orthanc, FSLeyes, Kaapana and Stone Web Viewer link to GitHub mirrors that their maintainers run.
  Their canonical repositories live outside GitHub, and the reviews of #35 and #37 kept the mirrors on purpose, so
  don't switch them. OpenREM and Plastimatch have no GitHub mirror and link GitLab.

## `archive.md`

Projects that are archived, deprecated, or have had no commits on their default branch for about two years move
from `readme.md` to the table in `archive.md`, with the reason, the month of the last commit and the month they
were archived. Widely used projects that are stable rather than abandoned (such as dicomParser) stay in the list.
Every entry removed from `readme.md` must land in `archive.md` or have a named successor in the list.

## Entry rules

From `contributing.md`, plus the format the list already uses:

- Format: `- [Name](url) - Description.`, with the description capitalized and ending in a period. A public demo
  goes before the final period as `([demo](url))`.
- The bar is deliberately light, so that new and small projects get exposure. A library or tool needs to be about
  DICOM, open source with a license, with a README or repository page that explains install and usage or links to
  docs that do (XNAT passes through its repository's website link), and maintained or stable. #37 left out
  espadon (no README or repository) and Kheops (no root README and no website link).
- **Libraries** and **Tools** must be open source and link to their source code: the repository, or the page that
  distributes source archives when there is none (PixelMed, dicom3tools).
- **Hosted Tools** are free tools and services hosted online with no installation or account; their source need
  not be public.
- Descriptions are one sentence that says what the resource does, without repeating the name. Leave out pricing,
  licensing offers and marketing claims. Hosted Tools may add a sentence on whether files leave the computer, and
  each dataset ends with `Access: ...`.
- Spellings: DICOMweb, JavaScript, Node.js, NIfTI, web-based, 3D, DICOM RT, Go.
- Keep entries in alphabetical order (case-insensitive) within each group of Libraries, Tools, Hosted Tools and
  Related Lists. Datasets and Learning Resources are not sorted.
- Contributors should state any affiliation with what they add in the PR description.

## Handling contributor PRs

When a contributor PR needs edits, the maintainers fix it themselves rather than waiting on the author. Instead
of pushing to contributor forks, merge each contributor's PR head into a maintainer branch, add fix commits on
top, open one PR, and merge it with **Create a merge commit**. GitHub then marks every folded-in PR as merged and
the authors keep credit (#34 did this for #26, #28, #30 and #31).

Never squash-merge such a PR, or a PR that creates a section other open PRs build on: the dependent PRs then
re-add the heading when they merge, and the union merge driver keeps both copies.

GitHub holds workflow runs on a first-time contributor's PR until a maintainer approves them (the run shows
"action_required"). Approve the Lint run so the PR gets checked; it runs with a read-only token.

## Header illustration and `media/`

Added in #40.

- `media/awesome-dicom.svg` is the header illustration, and `media/social-preview.svg` is the 1280×640 social card.
  The SVGs are the sources. The PNGs beside them are exports, so re-export both after any change:
  - `npx -y @resvg/resvg-js-cli@2.6.2-beta.1 --fit-width 1440 media/awesome-dicom.svg media/awesome-dicom.png`
  - `npx -y @resvg/resvg-js-cli@2.6.2-beta.1 media/social-preview.svg media/social-preview.png`
- A layout script kept outside the repository writes both SVGs. Change the art there rather than editing path
  data by hand. The social card's text is outlined, and the script derives the SVG's `<title>` from the tagline
  so the two stay the same.
- **The readme's first line is a comment that must stay first.** awesome-lint counts a centered image in the
  readme's first node as the list's heading, and then fails on the `# Awesome DICOM` title with "List can only have
  one heading". It only looks at the first node.
- GitHub has no API for the social preview. After the card changes, someone has to upload
  `media/social-preview.png` in Settings → General → Social preview.
- The art is original and must stay clear of the DICOM logo and NEMA's branding, which are NEMA trademarks. No
  AI-generated image is committed: the main list rejects fully AI-generated PRs.
