# TKCAM project page

Project page for **TKCAM: Text and Keyframe to Camera Trajectory Generation**.

Paper: [arXiv:2610.11105](https://arxiv.org/abs/2610.11105) · Code: [TKCAM](https://github.com/linearalgebrayhz/TKCAM)

The live page is published at [linearalgebrayhz.github.io/projects/TKCAM/](https://linearalgebrayhz.github.io/projects/TKCAM/). This repository contains the source page. A copy of the page lives at projects/TKCAM/ in the [personal website repository](https://github.com/linearalgebrayhz/linearalgebrayhz.github.io) so GitHub Pages can serve the requested URL.

## Content

- index.html: page content and citation metadata
- static/css/tkcam.css: page styling
- static/js/tkcam.js: BibTeX copy button
- static/images/paper/: figures rendered from the preprint
- static/pdfs/TKCAM_preprint.pdf: archived local snapshot; the page's Paper link points to the canonical arXiv version

The page works as a static site. To preview it locally, serve this directory with any HTTP server. Internal asset paths are relative, so the same files work at the repository root or under /projects/TKCAM/.

## Publishing

Keep this repository and the personal site copy in sync when changing the page. Copy index.html and static/ to projects/TKCAM/ in the personal website repository, then deploy that repository through GitHub Pages. The separate repository's default project-site URL is /TKCAM-project-page/, which is not the chosen canonical URL.

## Credits

The repository was created from the [Academic Project Page Template](https://github.com/eliahuhorwitz/Academic-project-page-template), whose page structure draws on [Nerfies](https://nerfies.github.io/). The current TKCAM layout and styles were rewritten for this project. Research figures belong to the paper authors.
