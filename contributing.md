# Contribution Guidelines

Please note that this project is released with a
[Contributor Code of Conduct](code-of-conduct.md). By participating in this
project you agree to abide by its terms.

---

## What can be listed

New and small projects are welcome. A library or tool can be added if it:

- Is about DICOM: it reads, writes, sends, stores, routes, converts, displays, validates, organizes or de-identifies DICOM data.
- Is open source, with a license, and the entry links to its source repository.
- Has a README that explains how to install and use it.
- Is maintained, or is stable and still works.

Datasets, Learning Resources and Hosted Tools need to be about DICOM and currently available. Related Lists are curated lists in neighboring fields that are useful to people working with DICOM.

If you are affiliated with what you are adding, say so in the pull request description.

## Where it goes

- **Libraries** are packages you use in your own code. They are grouped by language.
- **Tools** are applications and command-line tools you run. They are grouped by task: Conversion, De-identification, File Management, Gateways and Routing, Radiation Therapy, Research Platforms, Servers and PACS, Validation, and Viewers.
- **Hosted Tools** are free tools without public source that run in the browser and need no installation or account.
- **Datasets** hold DICOM data, and **Learning Resources** help people understand the standard and work with it.

List each project once, in the place where most people would look for it:

- A general-purpose toolkit, such as DCMTK or pydicom, is a library, even if it ships command-line utilities.
- A project built for one task goes under that task in Tools, even if you can also import it. For example, dicom2nifti goes under Conversion.
- A viewer you run is a tool. A viewer component you embed in your own app, such as DWV, is a library.

If no section fits, add one with the new entry. Add a line for a new `##` or `###` section in Contents. Related Lists and Contributing stay out of Contents.

## How to write an entry

- Use the format `- [Name](link) - Description.`
- Write one sentence that says what the project does. Don't repeat the project's name, and leave out pricing, licensing offers and marketing claims.
  - A Hosted Tool may add a sentence saying whether files leave the computer.
  - A dataset ends with how to get access, for example `Access: open.`
- If the project has a public demo, add it before the final period: `([demo](link))`. A dataset can link its browsing portal the same way: `([portal](link))`.
- Spell these terms as shown: DICOMweb, JavaScript, Node.js, NIfTI, web-based, 3D, DICOM RT and Go.
- Keep entries in alphabetical order within Libraries, Tools, Hosted Tools and Related Lists. Datasets and Learning Resources aren't sorted, so add new entries at the end of their group.
- Use correct grammar, and follow the style of the entries around yours.

## Archive

Projects that are archived, deprecated, or have had no commits on their default branch for about two years move to the [archive](archive.md), with the reason and the date. Projects that are widely used and stable rather than abandoned can stay in the list. If an archived project becomes active again, open a pull request to move it back.

## Updating your PR

If the maintainers notice anything that we'd like changed, we may ask you to
edit your PR before we merge it, or make small fixes ourselves. There's no
need to open a new PR, just edit the existing one. If you're not sure how to
do that,
[here is a guide](https://github.com/RichardLitt/knowledge/blob/master/github/amending-a-commit-guide.md)
on the different ways you can update your PR so that we can merge it.

Thank you for your suggestions!
