<!-- markdownlint-disable MD033 MD041 -->
<h1 align="center">
    expyriments
</h1>

<p align="center">
    <strong>Organize, run, track and share experiments & data.</strong>
</p>

<p align="center">
    <a href="https://pypi.org/project/expyriments/" title="PyPi Version"><img src="https://img.shields.io/pypi/v/expyriments?color=green&style=flat"></a>
    <a href="https://pypi.org/project/expyriments/" title="Python Version"><img src="https://img.shields.io/badge/Python-3.6%2B-blue&style=flat"></a>
    <a href="https://github.com/ml-tooling/expyriments/actions?query=workflow%3Abuild-pipeline" title="Build status"><img src="https://img.shields.io/github/workflow/status/ml-tooling/expyriments/build-pipeline?style=flat"></a>
    <a href="https://github.com/ml-tooling/expyriments/blob/main/LICENSE" title="Project License"><img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat"></a>
    <a href="https://gitter.im/ml-tooling/expyriments" title="Chat on Gitter"><img src="https://badges.gitter.im/ml-tooling/expyriments.svg"></a>
    <a href="https://twitter.com/mltooling" title="ML Tooling on Twitter"><img src="https://img.shields.io/twitter/follow/mltooling.svg?label=follow&style=social"></a>
</p>

<p align="center">
  <a href="#getting-started">Getting Started</a> •
  <a href="#features">Features</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#support--feedback">Support</a> •
  <a href="#contribution">Contribution</a> •
  <a href="https://github.com/ml-tooling/expyriments/releases">Changelog</a>
</p>

_TODO_

## Highlights

_TODO_

## Getting Started

### Installation

> _Requirements: Python 3.6+._

```bash
pip install expyriments
```

### Usage

_TODO_

## Support & Feedback

This project is maintained by [Benjamin Räthlein](https://twitter.com/raethlein), [Lukas Masuch](https://twitter.com/LukasMasuch), and [Jan Kalkan](https://www.linkedin.com/in/jan-kalkan-b5390284/). Please understand that we won't be able to provide individual support via email. We also believe that help is much more valuable if it's shared publicly so that more people can benefit from it.

| Type                     | Channel                                              |
| ------------------------ | ------------------------------------------------------ |
| 🚨&nbsp; **Bug Reports**       | <a href="https://github.com/ml-tooling/expyriments/issues?utf8=%E2%9C%93&q=is%3Aopen+is%3Aissue+label%3Abug+sort%3Areactions-%2B1-desc+" title="Open Bug Report"><img src="https://img.shields.io/github/issues/ml-tooling/expyriments/bug.svg?label=bug"></a>                                 |
| 🎁&nbsp; **Feature Requests**  | <a href="https://github.com/ml-tooling/expyriments/issues?q=is%3Aopen+is%3Aissue+label%3Afeature+sort%3Areactions-%2B1-desc" title="Open Feature Request"><img src="https://img.shields.io/github/issues/ml-tooling/expyriments/feature.svg?label=feature%20request"></a>                                 |
| 👩‍💻&nbsp; **Usage Questions**   |   <a href="https://stackoverflow.com/questions/tagged/ml-tooling" title="Open Question on Stackoverflow"><img src="https://img.shields.io/badge/stackoverflow-ml--tooling-orange.svg"></a> <a href="https://gitter.im/ml-tooling/expyriments" title="Chat on Gitter"><img src="https://badges.gitter.im/ml-tooling/expyriments.svg"></a> |
| 🗯&nbsp; **General Discussion** | <a href="https://gitter.im/ml-tooling/expyriments" title="Chat on Gitter"><img src="https://badges.gitter.im/ml-tooling/expyriments.svg"></a> <a href="https://twitter.com/mltooling" title="ML Tooling on Twitter"><img src="https://img.shields.io/twitter/follow/mltooling.svg?style=social"></a>|
| ❓&nbsp; **Other Requests** | <a href="mailto:team@mltooling.org" title="Email ML Tooling Team"><img src="https://img.shields.io/badge/email-ML Tooling-green?logo=mail.ru&logoColor=white"></a> |

## Features

_TODO_

## Documentation

### CLI Interface

_TODO_

### Python Client

_TODO_

## Contribution

- Pull requests are encouraged and always welcome. Read our [contribution guidelines](https://github.com/ml-tooling/expyriments/tree/main/CONTRIBUTING.md) and check out [help-wanted](https://github.com/ml-tooling/expyriments/issues?utf8=%E2%9C%93&q=is%3Aopen+is%3Aissue+label%3A"help+wanted"+sort%3Areactions-%2B1-desc+) issues.
- Submit Github issues for any [feature request and enhancement](https://github.com/ml-tooling/expyriments/issues/new?assignees=&labels=feature&template=02_feature-request.md&title=), [bugs](https://github.com/ml-tooling/expyriments/issues/new?assignees=&labels=bug&template=01_bug-report.md&title=), or [documentation](https://github.com/ml-tooling/expyriments/issues/new?assignees=&labels=documentation&template=03_documentation.md&title=) problems.
- By participating in this project, you agree to abide by its [Code of Conduct](https://github.com/ml-tooling/expyriments/blob/main/.github/CODE_OF_CONDUCT.md).
- The [development section](#development) below contains information on how to build and test the project after you have implemented some changes.

## Development

> _**Requirements**: [Docker](https://docs.docker.com/get-docker/) and [Act](https://github.com/nektos/act#installation) are required to be installed on your machine to execute the build process._

To simplify the process of building this project from scratch, we provide build-scripts - based on [universal-build](https://github.com/ml-tooling/universal-build) - that run all necessary steps (build, check, test, and release) within a containerized environment. To build and test your changes, execute the following command in the project root folder:

```bash
act -b -j build
```

Refer to our [contribution guides](https://github.com/ml-tooling/expyriments/blob/main/CONTRIBUTING.md#development-instructions) for more detailed information on our build scripts and development process.

---

Licensed **MIT**. Created and maintained with ❤️&nbsp; by developers from Berlin.
