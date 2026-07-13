---
url: "https://www.wifa.uni-leipzig.de/institut-fuer-wirtschaftsinformatik/professuren/professur-insbesondere-softwareentwicklung/studium/lehrveranstaltungen/sep"
title: "Universität Leipzig: Software Engineering Project"
---

Representatives from industry, administration and academia present various topics for software engineering projects that are relevant in a practical or research context. They provide necessary information about the application domain, inform about special requirements or constraints for the expected project outcome and outline the desired project goals.

Participants organize themselves into teams and work on a project as a team. Following the usual meetings in software development projects, you report regularly on the progress of the project as well as any problems that arise.

## Projects 2026

### [BE-terna: Planning Solution WebApp](https://www.wifa.uni-leipzig.de/institut-fuer-wirtschaftsinformatik/professuren/professur-insbesondere-softwareentwicklung/studium/lehrveranstaltungen/sep\#collapse909293)

## Planning as a web application with D365 Finance/SCM integration (OData)

## Introduction

Together with the students, we would like to realize a standalone “Planning Solution” web application. The app supports hierarchical corporate planning (plan creation, line generation, comparison values, top-down distributions, bottom-up roll-ups, review/approval, export/posting).

The solution is ERP-agnostic at runtime but integrates with **Dynamics 365 Finance / Supply Chain Management (F&O/SCM)** via **OData** to read reference/comparison data and write back approved plan figures.

## Goal

A **deliverable prototype** of the Planning Solution WebApp that:

- Implements the core planning workflows end-to-end on hierarchical structures.
- Imports comparison data from D365 F&O/SCM (read).
- Exports approved plan figures back to D365 F&O/SCM (write).
- Demonstrates traceability (change log per action) and data consistency (sum of children equals parent, rounding/rest handling).

## Prerequisites and Requirements

Students should bring:

- Affinity for web technologies; basic **TypeScript/JavaScript, HTML, CSS**.
- Experience with a modern SPA framework (e.g., **React**, **Vue**, or **Angular**).
- Basic understanding of **REST**, **JSON**, and authentication (OAuth2/Azure AD).
- Nice to have: experience with **OData**, **Azure**, testing (unit/E2E), and Git workflows.

## Technologies

The project is **technology-open**. The list below is **indicative** and may be adapted by the student team.

|     |     |     |
| --- | --- | --- |
| **Name** | **Module** | **Description** |
| TypeScript | Common | Primary language for web app and services |
| React / Vue / Angular | App | SPA framework for UI (tree grid, inline editing, variance views) |
| Node.js (Express/Fastify) or Python (FastAPI) | API | Thin API for plan CRUD and OData façades |
| Azure AD | Identity | OAuth2/OpenID Connect for authentication |
| OData v4 | Intregration | Read/write to D365 F&O/SCM Data Entities |
| Jest / Vitest + Playwright | Testing | Unit and end-to-end tests |
| GitHub / Azure DevOps | CI | Version control, CI workflows (build, test) |
| JSON (Object Storage optional) | Data | Internal persistence for plan payloads and exports |

## Project Method

**Working mode**

- Iterative, weekly increments.
- All work tracked as issues on a shared board (GitHub Projects or Azure DevOps Boards).

**Work items**

- Types: Feature, Task, Bug, Spike.
- Fields: Title, Description, Acceptance Criteria, Assignee.

**Workflow**

- Columns: Backlog → Ready → In Progress → Review/Test → Done.
- DoR: user value + acceptance criteria defined.
- DoD: code merged, tests green, lint/format OK, minimal docs updated.

**Cadence**

- Weekly planning (select small, valuable items).
- Weekly demo (show working software; capture feedback).

## Task Flow (per work item)

| Step | Description |
| --- | --- |
| Backlog | Unplanned item awaiting refinement and scheduling |
| Open | Planned/estimated for the active sprint |
| In progress | Currently implemented |
| Review | Completed and under peer review/testing |
| Finished | Accepted and done |

## Project milestones

Plan and implement the following milestones with the students (details refined during planning):

- **M1: Planning domain scaffold**

Plan object, hierarchical nodes, minimal UI to create a plan and navigate levels.
- **M2: Line generation from layout**

Generate node structures and editable key figures per level.
- **M3: Import comparison data (read OData)**

Pull historical/previous-year values from D365 F&O/SCM; show variances.
- **M4: Distribute & roll-up logic**

Top-down allocation with rounding/rest correction; bottom-up aggregation; invariants enforced.
- **M5: Review & approval**

Validation checks, status flow (Draft → InReview → Approved), write protection.
- **M6: Export / write-back (OData)**

Produce posting/export package and upsert approved values into D365 F&O/SCM.
- **M7: Traceability & tests**

Change log per action; Golden-Master scenarios; unit/E2E tests green.

## Location / Where to work

The project can be executed fully **remote** using the university’s collaboration tools or mutually agreed channels. On-site sessions/workshops can be arranged as needed

## Misc

- Students may use their preferred stack as long as the **goal** and **milestones** are met.
- Provided reference materials: **.al source code** of the BC extension and a **demo video** explaining the functional workflows (serve as authoritative functional reference).
- In terms of copyright, the source code written by the students as part of the project remains with BE-terna GmbH.

### [CCC Software GmbH: New module imaso® maintenance](https://www.wifa.uni-leipzig.de/institut-fuer-wirtschaftsinformatik/professuren/professur-insbesondere-softwareentwicklung/studium/lehrveranstaltungen/sep\#collapse909295)

## Extension of an existing industrial software solution with a personnel planning module

## Introduction

Together with participating students, ccc software gmbh intends to design and implement a new module for its existing maintenance software imaso® maintenance.

imaso® maintenance is a web-based application that supports customers in managing planned maintenance activities, technical services, downtimes, and related operational processes.

The project will be conducted using the Kanban method, enabling continuous delivery, transparent workflows, and flexible prioritization in a real-world industrial software environment.

## Goal

The objective of the project is to design and implement a personnel planning module that is seamlessly integrated into the existing imaso® maintenance software.

The module should support the planning, allocation, and overview of personnel resources in relation to maintenance and service activities, while adhering to existing architectural and quality standards.

## Prerequisites and Requirements

Students participating in the project should demonstrate an affinity for web technologies.

**Required knowledge:**

- Basic knowledge of **HTML5, CSS,** and **JavaScript**
- General understanding of web application development
- Basic knowledge of C#

**Advantageous knowledge:**

- Experience with **MVVM/MVC frameworks**, preferably **Angular**
- Basic understanding of **software design patterns**
- Familiarity with version control systems (e.g. Git)

## Technologies

The project includes various web and server technologies. The programming language is predominantly TypeScript, Angular and C#.

| Name | Module | Description |
| --- | --- | --- |
| TypeScript | Common | Programming language, super set of JavaScript |
| Angular | Frontend | Client-side MVVC framework |
| C# | Backend | Server-side development |
| Node.js | Tooling | Runtime environment |
| Entity Framework | Backend | ORM for database access |
| Azure DevOps | CI | Continuous integration and build pipelines |
| Git | Version Control | Collaborative source code management |

The project follows the Kanban methodology, focusing on continuous flow, transparency of work, and incremental delivery of value.

Instead of fixed-length sprints, work items are continuously planned, prioritized, and pulled into development based on team capacity. This allows a flexible response to changing requirements and individual learning speeds.

ccc software gmbh supports the students in applying Kanban principles and best practices throughout the project.

Kanban Principles Applied:

- Visualization of all work items on a Kanban board
- Limitation of work in progress (WIP)
- Continuous prioritization and delivery
- Focus on flow efficiency and quality
- Regular review and improvement of the workflow

Each task goes through the following intermediate steps:

| Step | Description |
| --- | --- |
| Backlog | Unplanned task that has to be discussed and scheduled in the planning appointment |
| ToDo | Planned and estimated tasks in the active sprint |
| In progress | Tasks that are currently being implemented |
| In Review | Completed tasks that have an open pull request and are waiting to be checked |
| Done | Fully completed and reviewed tasks, that have been merged to develop |
| Completed | Fully completed and reviewed tasks, that have been merged to release |

## Project milestones

The following milestones will be jointly planned and implemented with the students:

**Milestone 1: Project Setup & Analysis**

- Introduction to imaso® maintenance architecture
- Requirement analysis for the personnel planning module
- Technical onboarding (Git, Azure DevOps, development environment)
- Initial product backlog creation

**Milestone 2: Concept & UI Design**

- Definition of core use cases and user roles
- UX/UI concepts for personnel planning
- Data model and interface design
- Review and approval of technical and functional concepts

**Milestone 3: Core Feature Development**

- **Feature A:** Personnel availability and qualification management
- **Feature B:** Assignment of personnel to shifts/maintenance tasks
- **Feature C:** Calendar and overview views for personnel planning

**Milestone 4: Integration & Optimization**

- Integration into existing imaso® maintenance workflows
- Performance and usability improvements
- Error handling and validation
- Continuous refinement based on feedback

**Milestone 5: Testing & Final Delivery**

- Functional and integration testing
- Documentation of implemented features
- Final review and project presentation
- Handover of completed module

The exact functional requirements will be elaborated collaboratively with the students during the project.

## Location / Where to work

Our office is located in Musikviertel Leipzig. The project itself can be carried out completely remotely. We offer software such as Microsoft Teams for communication free of charge. For mutual coordination ccc software gmbh will be happy to provide the appropriate premises for occational planning appointments.

## Misc

- The project is subject to confidentiality.
- Remote work is guaranteed via VPN.
- In terms of copyright, the source code written by the students as part of the project remains with ccc software gmbh.

### [Eclipse: Analyzer Component for Assessing Maintenance and Quality](https://www.wifa.uni-leipzig.de/institut-fuer-wirtschaftsinformatik/professuren/professur-insbesondere-softwareentwicklung/studium/lehrveranstaltungen/sep\#collapse909298)

## Design and Implementation of an Analyzer Component for the Open Source Review Toolkit (ORT) that Evaluates Maintenance Status and Quality Metrics of Open Source Dependencies

## Introduction

Open Source Software (OSS) components are pervasive in modern industrial software development, often composing the majority of a system’s codebase. While these components bring efficiency and innovation, they also introduce risks related to licensing, security vulnerabilities, and long-term sustainability. Comprehensive insights into dependency quality and health are therefore crucial for effective software governance.

The Open Source Review Toolkit (ORT) is an open-source suite of tools used for software composition analysis (SCA), particularly focusing on license compliance, dependency identification, and vulnerability analysis. ORT’s Analyzer component identifies dependencies and gathers metadata about them — such as license information and source locations — to feed further compliance and policy evaluations.

While ORT already provides rich information about licensing and known vulnerabilities, there is limited automated support for assessing the quality, maintenance activity, and health of OSS dependencies. An open issue (Issue #3317: \[9\]) in the ORT issue tracker explicitly calls for extending ORT to advise about the quality and health of an open source project or dependency package — e.g., by integrating metrics beyond vulnerabilities, such as project activity and sustainability indicators. At the same time, initiatives such as the OpenSSF Scorecard provide an externally maintained framework for evaluating OSS project health and best practices, generating an automated score that reflects a range of indicators related to security and maintenance. This project aims to bridge the gap between ORT’s capabilities and these external quality and maintenance metrics by implementing a new Analyzer component within ORT that enriches Software Bill of Materials (SBOM) outputs with maintenance and quality scores from external sources such as OpenSSF Scorecard.

### Current State of Discussion

Issue #3317 discusses extending ORT’s Advisor or Analyzer capabilities to include health metrics beyond vulnerabilities. Suggested data sources include:

\- OpenSSF Scorecard (https://github.com/ossf/scorecard)

\- CHAOSS community metrics (https://chaoss.community)

\- Ecosyste.ms OSS dataset (https://ecosyste.ms)

\- End-of-life data from endoflife.date (https://endoflife.date)

The issue proposes adding a new Advisor capability such as HEALTH, but no implementation currently exists.

## Goal

The primary goal of this project is to design and implement an extension to the ORT Analyzer that automatically assesses the maintenance and quality status of open source components identified in an SBOM.

The resulting component will:

1. **Collect quality and maintenance metrics** for OSS components from external data providers (e.g., OpenSSF Scorecard).
2. **Enrich the ORT analysis results** with structured quality indicators that can be consumed by downstream ORT tools such as Evaluator or reporting modules.
3. **Align with community needs**, as documented in the ORT issue tracker, by supporting health-related insights beyond security vulnerabilities.

## Prerequisites and Requirements

As the project is about extending the Open Source Review Toolkit students should use Kotlin as programming language. Additionally, a basic understanding of software composition in general is beneficial to understand the motivation behind the project. A possible starting point could be a Linux Foundation Training on that topic \[7\].

As the ORT tool provides packaging as a docker image \[6\], it helps to have a basic understanding of using docker and container technology in general.

Students should have:

- Understanding of software engineering and dependency management.
- Experience with REST APIs, JSON/YAML, and working with open source tools.
- Familiarity with build tools and version control (e.g., Git).
- (Helpful) Knowledge of Kotlin or Java for extending ORT.

## Technologies

| Name | Purpose |
| --- | --- |
| Open Source Review Toolkit (ORT) | Core analysis platform for SCA and SBOM generation. (oss-review-toolkit.github.io) |
| OpenSSF Scorecard | Source of automated project health and best-practice metrics.(openssf.org) |
| GitHub API / External Metadata Providers | Data sources for repository activity and metadata. |
| SON, YAML, Kotlin/Java | Data formats and implementation languages for the new Analyzer. |

## Project organization

This project follows an agile, incremental approach:

- Kick-off and problem scoping
- Design and prototyping in iterations
- Regular synchronization with the academic supervisor
- Documentation of results and artifacts

It should use SCRUM as the agile framework and adjust it to the specific circumstances of the task and project team at hand.

## Project milestones

The following milestones should be planned and implemented with the students:

1. **Initial Setup and Exploration:** Set up ORT environment and execute basic analyses.
2. **Quality Metric Specification:** Formalize which metrics to collect and how to represent them.
3. **Analyzer Extension Prototype:** Implement a working prototype that fetches and maps external metrics.
4. **Integration and Evaluation:** Integrate with ORT output formats and run on real repositories.
5. **Final Reporting:** Document design, implementation, and evaluation results.

The exact requirements and user stories are worked out as part of the project work together with the students.

## Location / Where to work

Inherent to an Open-Source project is its distributed nature. So, the project itself is carried out remotely. The team can decide on communication channels. If required, the project contact person can arrange a video conferencing solution for the meetings. The student team and contact person may also arrange face-to-face meetings if it is needed. The contact person is in Berlin. If the meetings are in Leipzig, appropriate rooms at Leipzig University need to be organized. Otherwise, the contact person can arrange a meeting space in Berlin.

## Misc

- The students are required to provide their development equipment
- The project is not subject to confidentiality
- It is assumed that the code developed by the students will be published as open source, thus it might be required to sign some Contributor Agreements upfront.

## Resources

\[1\] [chaoss.community](https://chaoss.community/)

\[2\] [opensource.org/licenses](https://opensource.org/licenses)

\[3\] [github.com/Open-Source-Compliance/Go-Dummy](https://github.com/Open-Source-Compliance/Go-Dummy)

\[4\] [github.com/org-metaeffekt/metaeffekt-examples](https://github.com/org-metaeffekt/metaeffekt-examples)

\[5\] [oss-review-toolkit.org/ort/](http://oss-review-toolkit.org/ort/)

\[6\] [oss-review-toolkit.org/ort/docs/getting-started/installation](http://oss-review-toolkit.org/ort/docs/getting-started/installation)

\[7\] [training.linuxfoundation.org/training/introduction-to-open-source-license-compliance-management-lfc193/](https://training.linuxfoundation.org/training/introduction-to-open-source-license-compliance-management-lfc193/)

\[8\] [openssf.org/projects/scorecard/](https://openssf.org/projects/scorecard/)

\[9\] [github.com/oss-review-toolkit/ort/issues/3317](https://github.com/oss-review-toolkit/ort/issues/3317)

### [Finatix: Software Compliance Tool](https://www.wifa.uni-leipzig.de/institut-fuer-wirtschaftsinformatik/professuren/professur-insbesondere-softwareentwicklung/studium/lehrveranstaltungen/sep\#collapse909348)

## Feature development of an existing tool

## Introduction

To comply with Information Security Regulations software that is installed upon systems has to be monitored and managed efficiently. With our Software Compliance Tool we are addressing the recognition and the classification of newly installed software to enable timely responses to the installation of unauthorized software across any of the controlled systems.

The core functionality of the tool involves the comparison of comprehensive lists detailing all installed software against a catalogue of classified applications. Any software not yet classified requires assessment by the Information Security Officer (ISO), who will categorize it into one of three distinct classifications: Whitelist, Blacklist, or Limited.

At present, the tool exists in a rudimentary form, possessing only basic functionalities necessary for compliance. Although these features are operational, there is significant room for enhancement.

Primary objectives are:

1. **Reducing Manual Workload:** Streamlining processes, enhance automation, and provide information to minimize the manual effort required for software classification and monitoring. This objective will be addressed in the MVP.
2. **Enhancing User Experience:** Improving the tool’s interface and overall user interaction to facilitate more efficient workflows for our team.

In summary, we envision a sophisticated tool that will not only ensure compliance but also optimize our Information Security operations.

## Goal

The result of the project should be a deliverable update for the Software Compliance Tool which provides new improvements to the tool.

## Prerequisites and Requirements

You should have an affinity for web technologies. Basic knowledge of the programming languages Python, JavaScript, CSS, and HTML5 are prerequisites for development. Furthermore, basic knowledge of software design patterns is useful to better understand the frameworks themselves.

Please bring **your own laptop** for working on this project.

## Location / Where to work

Our office is located downtown Leipzig. The project itself can be carried out remotely, except the first kickoff meeting and the last retrospective. Those will be meetings in person in our office.

For mutual coordination, Finatix GmbH will be happy to provide the appropriate premises for planning appointments.

## Project milestones

The following milestones should be planned and implemented as the MVP (Minimal Viable Product) of the project:

- **Feature 1: Alerting**
  - As an ISO (Information Security Officer), I want to be alerted when new software is waiting to be categorized, to be able to categorize the software as soon as possible.
  - As a member of the IT-infrastructure team, I want to be alerted in an adequate (fast, medium of alerting, information provided) way, when blacklisted software was installed, to timely start the process of removing the software from the device.
- **Feature 2: Meaningful information is provided for software that awaits evaluation**
  - As an ISO, I want to be able to view as much relevant information about the software that needs to be evaluated, to make an informed decision with as little manual research as possible.

If there is time left, the following features and improvements can be defined and implemented:

- Feature 3: Improvements of UI/UX
- Feature 4: Improvements of automation
- Feature 5: Generation of metrics for evaluation of the process
- Feature 5: Generation of Compliance Reports

The exact requirements are worked out together with you and your team.

For each feature a conception, a layout (UI/UX) plan, the implementation, and testing has to be done.

## Technologies

The project includes various web and server technologies. The programming language is predominantly Python.

| Name | Used for | Description |
| --- | --- | --- |
| Python | Backend & Frontend | Main programming language used in the project. |
| Pytest | Backend & Frontend | Automated Python tests |
| Fastapi | Backend | Python web-framework used for backend. |
| Sqlite | Backend | Simple database for prototyping and small projects |
| Flask | Frontend | Python web-framework used for frontend. |
| Jinja | Frontend | HTML templating language used by flask. |
| HTML | Frontend | Used as part of the jinja templates |
| CSS | Frontend | CSS stylesheet |
| Java Script | Frontend | Scripting language for the web |
| GitHub | Version Management | Git Forge for collaborating with git |
| Discord | Communication | Communication platform for this Project |

## How we work

In our customer projects, we primarily follow the agile method "SCRUM". This means we organize our work into so-called sprints, during which we regularly plan tasks, implement and review them, and later inspect together what went well during implementation and what could be improved. At the end of a sprint the product should be updated in a way that is beneficial to it. The sprint duration — usually between one and four weeks — is decided by the team or customer. Since we require a biweekly review, we recommend a duration of 2 weeks.

We recommend following this agile principle, as it promotes transparency, continuous improvement, and efficient collaboration within your team. At the same time, you are free to adapt the framework to the specific needs of your project. You and your team decide how you work best and organize yourselves during each sprint.

The following events take place during a sprint:

| Component | Description |
| --- | --- |
| Daily | Daily meetings where team members synchronize their progress and identify any obstacles. |
| Sprint Planning | Joint appointment where the team decides what work will be completed during the upcoming Sprint. It involves breaking down tasks, estimating effort, and defining the Sprint Goal. |
| Sprint Review | Joint appointment to present the completed tasks and to gather feedback from stakeholders |
| Sprint Retrospective | Review of past sprints and a joint appointment to improve implementation and organization of the team |

The only requirements we have are the following:

- Kickoff Meeting: The project begins with an in-person kickoff meeting at our office. During this meeting, we will discuss everything that is needed to get started. Key topics include how you want to organize your work, the schedule for weekly meetings, available knowledge, and areas where support is needed. Access to the technologies will be checked, and the first feature will be discussed and planned.
- Task & Progress Tracking: Project progress is documented and evaluated in a task and planning tool such as Trello.
- Version Control: The project is developed collaboratively using Git for version management.
- Code Quality & Collaboration: With the help of code reviews, you independently ensure high code quality and learn from each other at the same time.
- Continuous Integration & Testing: Developers themselves must ensure that the software is always executable. Deliverable software status should be achieved at the end of each sprint. Each task in the sprint goes through the following intermediate steps:

| Step | Description |
| --- | --- |
| Backlog | Unplanned task that must be discussed and scheduled in the planning appointment. |
| Open | Planned and estimated tasks in the active sprint |
| In progress | Tasks that are currently being implemented |
| Review | Completed tasks that need to be checked again |
| Done | Fully completed and reviewed tasks |

- Biweekly Reviews: Every two weeks, there will be a review meeting with the Finatix stakeholders to provide regular feedback and exchange insights.
- Final Presentation & Retrospective: At the end of the project, there will be a final presentation of results and a retrospective review of the entire project. To conclude the project together, we would like to hold these two meetings in person at our office.

Throughout the project, you will be mentored by developers from Finatix GmbH. They are available to provide guidance and support. Based on our experience with previous projects, we recommend having a brief weekly meeting with the mentors to discuss any challenges or assistance needed — either in person or remotely, depending on what works best for your team.

## Misc

- We use our Finatix GitHub. You only need an own account, so we can add you to our group and repository.
- The project is not subject to confidentiality.
- Remote work is possible.
- Rooms in our office can be used with prior registration.
- In terms of copyright, the source code written by the students as part of the project remains with Finatix GmbH.

### [Gisa: Centralized Master Data Manager for Test Data v2](https://www.wifa.uni-leipzig.de/institut-fuer-wirtschaftsinformatik/professuren/professur-insbesondere-softwareentwicklung/studium/lehrveranstaltungen/sep\#collapse909395)

## SAP Cloud-based application development assisted by AI

## Introduction

Together with the students, we, GISA GmbH, would like to use the state-of-the-art AI provided by SAP to create a new web application, consisting of a backend and a frontend, in the SAP Business Technology Platform (BTP). The app should be able to generate and manage master data entries, such as business partners and addresses, for testing purposes in multiple connected SAP systems. It is intended to make the daily work of SAP consultants and developers easier, as both regularly need test data.

Compared to the previous version we would like to encourage the students to use the generative and explanatory capabilities of SAP’s AI Joule during the project. The idea is to start at the same point as version 1, with the idea, and to gather data from the students for the following criteria:

- Usability und support during the configuration process (setup of the BTP, the services and their configuration and linking as well as the understanding of them)
- Support while learning to develop with the proprietary SAP frameworks (CAP)
- Support during the productive development process (from mock-up to app and during the adaptation of previously created artefacts)

The collection of this information should help us to get a first glance at the usability and viability of the usage of the currently available features of SAP Joule during the development inside the BTP for CAP projects. Furthermore, we would like to get a hint on the benefits of using SAP Joule for the development with SAP’s proprietary language ABAP inside the BTP. The processing of the collected information will not be part of the project.

The entire product development process from conception to delivery is mapped. We organize the project using tools of agile project management, like Kanban. For this purpose, meetings for planning and review with the students are scheduled. The students also have the opportunity to meet in a "Daily" to resolve blockades and to share their current progress with the rest of the team. We provide appropriate video conference software (Microsoft Teams). Besides these key points, the students organize themselves using sprints.

## Goal

The resulting web application should:

- Support the creation of multiple master data entities, like business partners, addresses and connection objects.
- Create the master data inside a connected SAP system using a provided OData API.
- Use pools of person names, street names, town names, … during the creation of new master data entries that look like real data.
- Be able to create the data in mass.
- Track the created master entries for multiple connected SAP systems in an own database.
- Be able to copy generated entries from one into another SAP system.
- Provide an UI to show the generated data as well as to manage the generation process.
- Optional: Can delete the previously generated data from the SAP system.

## Prerequisites and Requirements

The students should have an affinity for web technologies. Basic knowledge of the programming language JavaScript (NodeJS) as well as SQL (this should apply to at least one of the students) is a prerequisite for development. Basic knowledge of database modelling would be an advantage.

## Technologies

The project includes various web and server technologies, mostly introduced by SAP. The programming language is predominantly JavaScript.

| Name | Module | Description |
| --- | --- | --- |
| CAP | Framework | Proprietary framework for rapid prototyping of services based on entities |
| Fiori Elements | UI | Super set of the SAP UI5 framework to create HTML5 applications |
| Git | Version control | Tool to manage and distribute source code |

We work in the project according to the agile method Kanban. This means that we split the labour into several work items, which are then tracked in a Kanban Board according to their status.

Each task goes through the following intermediate stages:

| Status | Description |
| --- | --- |
| Backlog | Unplanned task that has to be discussed and scheduled |
| Open | Planned and estimated tasks |
| In progress | Tasks that are currently being implemented |
| Review | Completed tasks that need to be tested |
| Finished | Fully completed and reviewed tasks |

The requirements are discussed and planned in joint planning meetings. The students organize themselves, e.g. through regular coordination meetings (Daily).

The version management Git helps the students to develop together on the project.

## Project milestones

The following milestones should be planned and implemented with the students:

- Backend Service:
  - Data Pool
  - Entity Creation Service
  - Entity Tracking
- UI

The exact requirements are worked out together with the students.

## Location / Where to work

Our offices are located in downtown Leipzig or in Halle. The project itself can be carried out completely remotely. We offer software, such as Microsoft Teams, for communication free of charge.

For mutual coordination GISA GmbH will be happy to provide the appropriate premises for status and planning appointments.

## Misc

- Technology and work equipment such as test equipment, software or laptops can be borrowed.
- The project is not subject to confidentiality.
- In terms of copyright, the source code written by the students as part of the project and the IP remains with GISA GmbH.

### [LAPWE: A patient-wayfinding-system](https://www.wifa.uni-leipzig.de/institut-fuer-wirtschaftsinformatik/professuren/professur-insbesondere-softwareentwicklung/studium/lehrveranstaltungen/sep\#collapse909397)

## Improving the patient-wayfinding-system and smart archive.

## Introduction

Together with the students, we, the LAPWE-Team, would like to further develop our smart system for family doctors that consists of several elements. All build to improve the flow of Information and data a family doctors business has to deal with. The difference to other systems is the approach to develop a system around the patient instead of concentrating on subtasks.

The entire product development process from conception to delivery is mapped. We organize the project with Scrumban. For this purpose, the planning & review meetings as well as retrospectives with the students are scheduled. The students also have the opportunity to meet in the "Daily" to vote on a daily basis.

## Goal

The result of the project should be an improved version different elements of the system. We can offer a variety of different tasks to work on, based on the existing expertise and interest of the students. Depending on the tasks worked on, the results could be an improved working archive, thanks to benchmarked local LLM’s, a better web application for patients, an improved website or improved automations.

## Prerequisites and Requirements

The students should have basic knowledge of at least one of the programming languages Java, Python, TypeScript or HTML. Basic knowledge of docker (swarm), OpenAPI and/or PostgreSQL would be an advantage. Furthermore, basic knowledge of software design patterns and/or benchmark automation is useful. We are able to assign tasks that are suitable for the software stack the students bring with them.

## Technologies

The project includes various web and server technologies. The programming languages are predominantly Java, TypeScript, Python or HTML.

We work in the project according to the agile method Scrumban. This means that we plan our tasks with the necessary appointments and then look together to see how well the implementation went. The duration of a task is decided with the students and can be between 1 and 2 weeks. Our contacts support you in adhering to the guidelines.

The following Scrumban components are used in the project:

- Tasks – what we want to achieve
- Planning - task requirements are discussed, estimated and planned
- Meetings – dynamically arranged when necessary
- Review - joint appointment to present the completed tasks
- Retrospective - dynamically arranged when necessary to improve implementation and organization

The students organize themselves during their work-time, e.g. through coordination meetings or direct messages to team members. In a locally hosted task and planning software the progress of the tasks is documented and evaluated.

The version management "Git" helps all members to develop together on the project. With the help of code reviews (pull requests), the students independently ensure high code quality and learn from each other at the same time.

In the Forgejo Runner, the software versions are automatically checked for quality (linting), tested and built. Developers themselves have to ensure that the software is always executable. A deliverable software status should be achieved at the end of each finished task.

Each task goes through the following intermediate steps:

- Backlog - task that has to be discussed and scheduled in a planning appointment
- Open - planned and estimated tasks
- In progress - tasks that are currently being implemented
- Ready for review - completed tasks that need to be checked
- Reviewed - fully completed and reviewed tasks

## Project milestones

Are highly dependent on the timeline of the project.

The following milestones could be planned and implemented with the students:

- improved Website for our patient-wayfinding-system
- Webapp with Tutorials for MA’s
- improved benchmarking
- benchmarking of new local models
- improvement of existing services (OCR, diagnose extraction, ICD-Code assignment, summarizer, logging)
- feature development (document classification, automated workflows, user/rights system, new summerize options, ability to ask free text questions about patients and many more)

The exact requirements are worked out together with the students.

## Location / Where to work

Our offices are located in Leipzig and Elstertrebnitz. The project itself can be carried out completely remotely. We offer software for communication free of charge. For mutual coordination we will be happy to provide the appropriate premises for s and planning appointments.

## Misc

- Technology and work equipment such as test equipment and software are provided. Students must bring their own laptops.
- The project is subject to confidentiality – presentations and discussions within the context of university and between the students are permitted.
- Remote work is guaranteed.
- Rooms in our office can be used with prior registration.
- In terms of copyright, the source code written by the students as part of the project remains with LAPWE.

### [MID: AI-Assisted Onboarding and Intuitive Diagram Modeling](https://www.wifa.uni-leipzig.de/institut-fuer-wirtschaftsinformatik/professuren/professur-insbesondere-softwareentwicklung/studium/lehrveranstaltungen/sep\#collapse909401)

## Exploring modern UX/UI patterns and AI-assisted workflows for next-generation modeling software through design and prototyping

## Introduction

MID GmbH develops Innovator, a comprehensive enterprise modeling tool supporting various diagram types including UML, BPMN, ArchiMate, and custom notations. With the growing adoption of AI technologies and evolving user expectations for intuitive software experiences, there is a strategic need to explore how modern UX/UI design patterns and AI-assisted workflows can enhance the modeling experience.

This project aims to design and prototype a next-generation user interface for diagram modeling that combines intelligent onboarding with lower entry barriers, AI-assisted modeling that provides contextual suggestions, and modern interaction patterns aligned with contemporary design standards.

The goal is to create an independent research prototype that explores innovative approaches to modeling software UX. This prototype will be developed entirely separately from Innovator, with no technical dependencies or integration requirements. The insights gained will inform future development directions for MID's product portfolio, including Innovator Orbit (web-based modeling) and MIRA (AI chat assistant).

Key Characteristics:

- Pure frontend prototype with no backend requirements
- Mock AI implementation (simulated intelligent responses)
- Focus on UX, design innovation, and creative problem-solving
- Agile development methodology with iterative feedback cycles

## Goal

The primary objective is to deliver a comprehensive UX/UI concept and functional prototype that demonstrates innovative approaches to AI-assisted diagram modeling, specifically targeting users with limited modeling experience.

**Onboarding & Ideation:**

- Participate in a structured kick-off session where existing research, competitor analysis, current products, and reference tools (Figma, Miro, Lucidchart, etc.) are presented
- Engage in 1–2 guided brainstorming sessions to develop initial concepts and identify key UX opportunities
- Develop a UX/UI concept for AI-assisted diagram creation

**Design Excellence:**

- Create wireframes and high-fidelity mockups in Figma
- Design an interactive click-prototype demonstrating core workflows
- Establish a modern, consistent visual design language

**Prototype Implementation:**

- Build a functional frontend prototype showcasing key interaction patterns
- Implement mock AI service with contextual, scenario-based responses
- Demonstrate at least 3 distinct AI interaction patterns
- Create a usable diagram canvas with basic editing capabilities

**Innovation Focus:**

- Explore how AI can assist users through suggestions, validations, and guidance
- Design an onboarding experience enabling non-experts to create quality diagrams
- Investigate progressive disclosure patterns balancing simplicity with advanced features

**Validation:**

- Conduct usability testing with representative users
- Document findings, learnings, and recommendations for future development

Important Note: This is an exploratory research project. Students are encouraged to be creative and propose their own solutions based on thorough research. The focus is on design thinking, innovation, and well-reasoned decision-making rather than strict adherence to predefined specifications.

## Prerequisites and Requirements

**Required Skills:**

- Basic knowledge of frontend development (HTML, CSS, JavaScript)
- Familiarity with at least one modern frontend framework
- Understanding of UI/UX design principles

**Expected Competencies:**

- Creative problem-solving and design thinking
- Willingness to engage with research materials provided
- Ability to iterate based on feedback
- Good communication and presentation skills

**Provided by MID:**

- Access to GitLab repository for version control
- Microsoft Teams workspace for collaboration
- Figma licenses (if required)
- Example diagrams and modeling templates
- Access to MID design guidelines
- Regular feedback and guidance from project supervisor
- One primary stakeholder for requirements clarification and feedback

**Student Responsibilities:**

- Active participation in sprint planning, reviews, and retrospectives
- Regular communication and status updates
- Documentation of design decisions and technical implementation

## Technologies

The following technologies are recommended for this project. The final technology selection will be made collaboratively with the students during project kickoff, based on team expertise and project requirements.

**Design & Prototyping:**

- Figma – For wireframes, high-fidelity mockups, and interactive click-prototypes
- Alternative design tools may be discussed if team has strong preference

**Frontend Framework (Student Choice):**

- Angular (Recommended)
- Blazor (Recommended)
- React, Vue.js, or other modern frameworks (acceptable)

**Styling & UI Components:**

- Tailwind CSS (Suggested)
- Bootstrap, Material UI, or custom CSS (acceptable)
- Focus should be on design quality rather than specific framework

**Mock AI Implementation:**

- JavaScript/TypeScript modules with predefined JSON response data
- Simple rule-based logic for contextual suggestions
- Scenario-based mock responses for different user workflows

**Version Control & Collaboration:**

- GitLab – Source code repository (provided by MID)
- Microsoft Teams – Communication, meetings, file sharing

**Development Environment:**

- Modern code editor (VS Code, etc.)
- Node.js and npm/yarn for package management
- Git for version control

**No Backend Required:**

- All functionality implemented in frontend
- Mock data stored in JSON files or TypeScript constants
- No database, server, or API integration needed

## Implementation Methodology

The project will be managed using Agile/SCRUM principles, ensuring iterative progress, regular feedback, and adaptability. This methodology supports the exploratory nature of the project while maintaining clear structure and accountability.

**Sprint Structure:**

- Sprint Duration: 2 weeks
- Sprint Planning: Define goals, select backlog items, estimate effort
- Sprint Execution: Development work, daily asynchronous updates
- Sprint Review: Demonstrate progress, gather feedback from stakeholder
- Sprint Retrospective: Reflect on process, identify improvements

**Meeting Cadence:**

- Weekly Check-in: 30 minutes
  - Quick status updates
  - Blocker identification
  - Quick questions and clarifications
- Bi-weekly Sprint Meeting: 1.5 hours (every 2 weeks)
  - Sprint Review: Demonstration of completed work
  - Sprint Retrospective: Process reflection
  - Sprint Planning: Planning for next sprint
- Ad-hoc Sessions: As needed
  - Design reviews
  - Technical deep-dives
  - Usability testing sessions
  - Special topic discussions

**Agile Practices:**

- User stories and acceptance criteria
- Backlog refinement and prioritization
- Incremental delivery
- Continuous feedback and adaptation
- Transparent progress tracking

**Documentation:**

- Design decisions documented in GitLab wiki or shared documents
- Code documentation through comments and README files
- Meeting notes and action items tracked in Teams
- Design rationale captured in Figma

**Quality Assurance:**

- Regular design reviews with supervisor
- Peer reviews within team
- Usability testing with external participants
- Iterative refinement based on feedback

## Backlog Structure and Workflow

The project backlog will be organized around major work streams rather than technical user stories. Students are expected to break down these high-level themes into specific tasks during sprint planning sessions.

**Task States:**

- To Investigate: Item identified but not yet discussed or analyzed.
- To Groom: Item ready to be refined, estimated, and prioritized in the backlog.
- Ready: Well-defined and prioritized item, ready to be pulled into a sprint.
- More Info: Item requiring additional details or clarifications.
- Committed: Item currently in the active sprint and under development.
- To Review: Item completed and tested, awaiting final review.
- Closed: Item fully completed and accepted.

**Workflow:**

- Items will be prioritized collaboratively during sprint planning
- Students propose their own detailed tasks based on research findings
- Acceptance criteria defined together with supervisor
- Progress tracked in GitLab

## Project Milestones

The project is structured into four major milestones:

**1\. Kick-Off & Ideation**

- Kick-off session: Review of existing research, competitor landscape, and product portfolio
- 1–2 brainstorming/ideation workshops to explore approaches

**2\. Design & Wireframing**

- Create wireframes for key user flows
- Develop high-fidelity mockups in Figma
- Build interactive Figma prototype
- Conduct design reviews and iterations

**3\. Prototype Implementation**

- Set up development environment
- Implement frontend prototype based on designs
- Develop mock AI service
- Integrate canvas and AI interaction patterns

**4\. Testing & Finalization**

- Conduct usability testing sessions
- Analyze results and iterate
- Prepare final presentation

The exact details and acceptance criteria of these milestones will be refined during the planning sessions with the students.

## Location / Work Environment

The project work can be conducted entirely remotely. Communication, daily stand-ups, and sprint rituals will be hosted virtually via Microsoft Teams. In-person meetings can be arranged as necessary. All required software, licenses, and resources, including test environments and accounts, will be provided to the team.

## Miscellaneous

- Technology and necessary tools (e.g., software licenses, testing equipment) can be provided or borrowed as needed.
- The project is not subject to confidentiality.
- Remote work is facilitated via secure VPN access if necessary.
- In terms of intellectual property and copyright, all source code and deliverables created during the project remain with MID GmbH

### [TIMETOACT: Web App “License recognizer](https://www.wifa.uni-leipzig.de/institut-fuer-wirtschaftsinformatik/professuren/professur-insbesondere-softwareentwicklung/studium/lehrveranstaltungen/sep\#collapse909410)

## Cross-platform development with web technologies

## INTRODUCTION

Together with the students, we, ATVANTAGE GmbH as part of the TIMETOACT group (in the following mentioned as TIMETOACT) would like to develop a web application to import documents via an OCR and AI based approach. The Web App name proposal is “License recognizer”.

## GOAL

Problem statement: Reduction of manual administration efforts with automation and usage of AI

Scope of the project is the development of a browser-based app solution with a core database / CMDB, a frontend to clear data and a number of interfaces to be named. Main goal of the application is the successful recognition and completion of necessary software license data.

## PREREQUISITES AND REQUIREMENTS

The students should have an affinity for web technologies. Basic knowledge of the programming languages JavaScript, CSS and HTML5 are prerequisites for development. Furthermore, basic knowledge of software design patterns, database and interface designs are useful to better understand the solution architecture. The project mandates the use of open-source technologies and frameworks throughout the software development lifecycle. The working environment and tooling can be Atlassian Jira and Confluence. Both tools can be provided by TIMETOACT.

## TECHNOLOGIES

The project will utilize a range of modern web development and cloud-native technologies tailored to create an interactive and user-friendly web application for IT asset management.

This setup will enable efficient OCR based data recognition, processing supported by AI and results visualization as well as according interfaces.

### Mandatory technologies

| Name | Module | Description |
| --- | --- | --- |
| REST | Application Programming Interface (API) | Mandatory interface architecture to be implemented for a Partner-API (business-to-business API) since relevant source and target systems (e. g. IT asset management tools such as Flexera One, ITSM or CMDB solutions). |
| SQL | Application Programming Interface (API) | Mandatory interface architecture to be implemented for a Partner-API (business-to-business API) since relevant source and target systems (e.g. IT asset management tools such as Flexera FNMS). |
| Microsoft Azure | Cloud Hosting | The choice of Microsoft Azure as the hosting platform guarantees a secure, scalable cloud environment for deploying the web application, ensuring high availability and performance. |
| OAuth 2.0 | Authentication | Implementing OAuth 2.0 ensures that only authorized users can access and interact with the app and safeguarding sensitive IT asset information. |

### Optional technologies

| Name | Module | Description |
| --- | --- | --- |
| VueJS | Web Frontend | Optimal for developing the user interface, Vue.js facilitates building dynamic, responsive web applications. |
| Vuetify | Web Interface | Leveraging Vuetify, a Vue.js UI library with Material Design components, enhances the user interface, making the app visually appealing and easy to navigate. |
| TypeScript with Node.js | Server-side Logic | TypeScript, used along with Node.js, offers a scalable framework for backend logic, including handling questionnaire submissions, data processing, and analytics. TypeScript ensures code reliability and maintainability, which is crucial for complex logic involved in IT asset management assessments. |
| D3.js | Data Visualization | Essential for presenting the questionnaire results, D3.js will be used to create interactive and sophisticated visualizations, offering insights into IT asset management efficiently. |
| Azure DevOps | Continuous Integration/Deployment | Implementing Azure DevOps for CI/CD streamlines the development process, from code integration, testing, to deployment, facilitating continuous delivery with minimal manual intervention. |
| MongoDB | Database | MongoDB's flexible document model is well-suited for storing questionnaire data and results, allowing for scalable storage solutions and easy retrieval of IT asset management information. |
| OCR | Optical Character Recognition for data import | Optical character recognition (OCR) is a technology that changes printed documents into digital image files. It is a digital copy machine that utilizes automation to transform a scanned document into machine-readable PDFs that you can edit and share. |

## PROJECT ORGANIZATION AND IMPLEMENTATION

### **Project team roles:**

- Project Manager
  - Project and meeting coordinator
  - Main reporter of project status
- Business and Data Analyst and Designer (incl. Report Design):
  - Workflow and report design
  - Specification of requirements
- Frontend Developer
  - Software development of frontend
  - Specification of requirements
- Backend and Database Developer
  - Software development of backend and database
  - Specification of requirements
- Test Manager and IT-Security Officer
  - Quality assurance of software development
  - Quality assurance of data integrity and IT-security standards while development

### **Non-functional requirements**

Documentation is key and must be delivered:

- Project plan, meeting schedule and frequent project status
- Documentation of solution architecture and database design
- Documentation of functional requirements (e. g. user stories)
- Documentation of non-functional requirements for solution
- Code documentation mapped to functional requirements
- Mutual agreement on coding guideline (e.g., Google, Mozilla, etc.)
- Basic test documentation

The organizational project set-up can be determined by the students themselves.

TIMETOACT will provide the following technical setup:

- Atlassian Confluence Space for documentation
- Atlassian Jira Board for project and software development tracking
- GitHub as software code repository

### Functional requirements and methodical approach

Development of an importing mechanism for a database/CMDB to store relevant software license data, a graphical user interface (GUI) to manually enrich the stored data and several interfaces to and from third systems.

The following working packages are relevant for the development:

**Phase 1: Kickoff and requirements specification**

- Definition of app architecture and data flow together with TIMETOACT (e. g. in an requirements workshop)
- Definition of the single work packages

**Phase 2: Minimal Viable Product (MVP) implementation**

- Architecture implementation
- Permissions management basis (authentication for web-app and data security)
- Setup of AI and initial training of neuronal nets / AI to create AI decision patterns

**Phase 3: Implementation of enhanced requirements**

- Sophisticated import mechanism for software and license data
  - Import source shall be PDF documents and provided information
  - OCR- or similar technology-based recognition of software and license data
  - Continuous improvement model
- Permissions management
  - Implementation of security methodology / permissions management for database/CMDB, GUI and Interfaces
  - At least two roles
    - Administrator / TIMETOACT
    - User / Customer
- Interface / Import / Export
  - Working and tested inbound and outbound Interface to / from third systems
  - Mandatory interface technologies will be provided
- Data visualization and clearing
  - Representation of stored and imported data in a GUI
  - Editability of stored and imported data in a GUI (Clearing) to complete data sets

Further work packages can be determined together with TIMETOACT. A review of proposed work packages can also be done with TIMETOACT before the project start.

**Phase 4: Project closure**

- Testing of implemented features and non-functional specifications of the developed application
- Technical and user-oriented documentation of the application
- Handover to client and project closure
- Lessons learned

## PROJECT MILESTONES

The following milestones should be planned and implemented with the students:

- Phase 1:
  - Specification of customer requirements and acceptance by TIMETOACT
  - Specification of data model and acceptance by TIMETOACT
- Phase 2:
  - MVP and Mock-up for initial look and feel of solution
  - Basic feature development
- Phase 3:
  - Enhancement feature development
  - Acceptance of developed backlog by TIMETOACT
- Phase 4:
  - Tests of features and non-functional requirements
  - Documentation
  - Handover and project closure
  - Feature launch and acceptance for productive usage by TIMETOACT

The specific requirements are determined collaboratively with the students.

## LOCATION / WHERE TO WORK

Our office for a possible consultation is in downtown Leipzig. The project itself can be carried out completely remotely. For communication, we provide software such as Microsoft Teams free of charge. Team meetings are held on the university premises.

## MISC

- The project is subject to confidentiality.
- In terms of copyright, the source code written by the students as part of the project remains with TIMETOACT.

### [Unite: Autocompletion, Suggestion and Recommendation engine](https://www.wifa.uni-leipzig.de/institut-fuer-wirtschaftsinformatik/professuren/professur-insbesondere-softwareentwicklung/studium/lehrveranstaltungen/sep\#collapse909423)

## Cross-platform development with web technologies and search technologies

## Introduction

The Unite Services GmbH & Co. KG (hereinafter referred to as Unite or we, us, our) is the internal service provider for the Procurement as a Service Platform of Unite, formerly Mercateo. Together with the students, we want to research new technologies to re-build search-engine related features such as autocompletion, suggestions or recommendations.

Our search-engine stack is a crucial part of our platform that supports thousands of our customers every day to fulfill their procurement needs. It is required to stay up to date in terms of both technology and usability.

The entire product development process from conception to delivery is mapped in the project.

We provide appropriate collaboration tools such as our video conference software Microsoft Teams, our whiteboard software Miro, or our ticket and task managing software Jira free of charge.

## **Goal**

The result of the project should be a Proof of Concept of a search service based on Typesense or OpenSearch that supports one or multiple of the following features:

- autocomplete suggestions as users are typing
- provide a “did you mean” style feedback on typos
- basic recommendations such as related items, trending products, personalised feed

Next to the customer-facing functionalities, the operational aspects of observability (logs, metrics, traces), testing, and continuous integration and delivery must be addressed. In the best-case scenario, the project closes with a deliverable release deployed as a Docker container within our pre-production infrastructure.

## Prerequisites and Requirements

The students should have an affinity for web technologies, machine learning, search engines, or related fields. Basic knowledge of the programming languages Java or TypeScript is considered a prerequisite for participation in the project. Basic knowledge of frameworks and tooling such as React, Spring Boot, or Docker, would be an advantage. Furthermore, basic knowledge of software design patterns is useful to understand architectural decisions.

## Methodology

We work based on the agile methodology SCRUM with the following components being used in the project:

| Component | Description |
| --- | --- |
| Sprint | Fixed period of two weeks in which a certain selection of tasks is implemented. |
| Planning | Tasks and requirements are discussed, estimated and planned in sprints. |
| Sync | Coordination meeting among the students for progress, open questions or problems. Based on the students’ availability, it will occur less frequent than the traditional Daily. |
| Sprint Review | Joint appointment to present the completed tasks to interested parties. |
| Retrospective | Review of past sprints and a joint appointment to improve implementation and organisation of the team. |

All project requirements and their implementation will be discussed and planned into so-called sprints during joint planning meetings (Planning). A deliverable software status should be achieved at the end of each sprint.

The duration of a sprint is set to two weeks by default.

The students organize themselves during a sprint, e.g. through regular coordination meetings (Sync), to review their progress and to discuss and solve open questions or problems. In our task and planning software Jira, the progress of the tasks is documented and evaluated.

Each task in the sprint goes through the following intermediate steps:

| Step | Description |
| --- | --- |
| Backlog | Unplanned task that needs to be discussed and scheduled in the planning meeting. |
| Open | Planned and estimated tasks in the active sprint. |
| In progress | Tasks that are currently being implemented. |
| Review | Completed tasks that need to be reviewed for acceptance. |
| Finished | Fully completed and reviewed tasks. |

At the end of each sprint, a public sprint review is taking place to present the achievements to stakeholders and interested parties. Retrospectives are used to review together the team’s performance on how well or badly the implementation went and to discuss opportunities for improvement. Our contacts will support the students in adhering to the SCRUM guidelines.

## Technologies

The project includes various web and server technologies. The programming languages are predominantly Java for the backend and TypeScript for the frontend.

The application is expected to be deployed as a Docker container in one of our existing environments either on-premises or within the cloud (AWS).

The following list of technologies is expected to be used in the project:

| Name | Scope | Description |
| --- | --- | --- |
| TypeScript | UI | Programming language, super set of JavaScript |
| React | UI | JavaScript library for building UI components |
| Spring Boot | Backend | Framework to deliver web applications based on Java |
| Typesense | Backend | Open-source, typo-tolerant search engine optimized for instant search-as-you-type experiences |
| OpenSearch | Backend | Distributed search and analytics engine that supports various use cases, e.g. a search box on a website |
| Cypress | Testing | Test framework for modern web applications |
| GitLab | SCM and CI | Source code repository and CI software |
| Vite | Build and packaging | Build tool for modern web projects |
| Docker | Application container | Framework and Environment for Microservices |

Our source code management system GitLab helps the students to develop together on the project. With the support of code reviews (Merge requests), the students independently ensure high code quality and learn from each other at the same time.

Within the CI (Continuous Integration) functionality of GitLab, pipelines are to be developed that automatically check the software versions for quality (linting), run relevant test suites, and build and package the software for deployment. Developers must ensure that the main branch of the software is always deployable.

## Project milestones

The following milestones should be planned and implemented with the students after initial onboarding with setting up the team and development environments:

- Decision on the system and software architecture based on the requirements engineering.
- Implementing the backend service, including the provision of the required search indices.
- Building mockup screens of the application frontend together with the design team.
- Implementing a working prototype of the application frontend, with access to the backend service.

The exact requirements of any features will be worked out together with the students.

## Location / Where to work

Our company headquarter is located next to the Johannisplatz at Grimmaischer Steinweg 8, which is just a short walking distance from the Augustusplatz into the direction of the GRASSI museum of applied arts. While the project itself can be carried out completely remotely, spending at least one day per week as a team together on-site will boost collaboration and team spirit. We will be happy to provide the appropriate premises for collaborative work and assist in planning appointments.

## Misc

- Technology and work equipment such as software or laptops will be provided free of charge for the duration of the project. The use of private devices is not possible.
- The project is subject to confidentiality and will require the acceptance of internal policies.
- Remote work is possible via private access with multi-factor-authentication.
- Meeting rooms and individual workplaces in our office can be used with prior registration.
- In terms of copyright, the source code written by the students as part of the project remains with Unite.

## Das könnte Sie auch interessieren

Angezeigt wird Element 1 von 3

### Studium

[mehr erfahren](https://www.wifa.uni-leipzig.de/institut-fuer-wirtschaftsinformatik/professuren/professur-insbesondere-softwareentwicklung/studium)

### Lehrveranstaltungen des Lehrstuhls

[mehr erfahren](https://www.wifa.uni-leipzig.de/institut-fuer-wirtschaftsinformatik/professuren/professur-insbesondere-softwareentwicklung/studium/lehrveranstaltungen)

### Team der Professur

[mehr erfahren](https://www.wifa.uni-leipzig.de/institut-fuer-wirtschaftsinformatik/professuren/professur-insbesondere-softwareentwicklung/team)

![Eye-Able Logo](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-able_whitelabel-icon_2.svg)

![Einstellungen zurücksetzten](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-able-reset-top.svg)![Einstellungen öffnen](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/settings.png)

Eye-Able Assistenzsoftware Logo![Eye-Able Assistenzsoftware Logo](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-able_whitelabel-icon_2.svg)![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-able-active-check.svg)[Eye-Able® Assistent](https://eye-able.com/)

![Eye-Able schließen und minimieren](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-able-circle-x.svg)![Info-Fenster öffnen](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-able-info.svg)

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-Schnellmodus.svg)Sofortansicht![Speichern der Sofortansicht](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-Save.svg)

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-Font-Size.svg)Schriftgröße![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-Able-chevron-down.svg)

![Lupe Funktion](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-able-lupe.svg)0

![Schrifgröße verkleinern](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-able-minus.svg)![Schriftgröße zurücksetzten](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-able-main-zoom-reset.svg)![Schriftgröße vergrößern](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-able-plus.svg)

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eyeable-right-arrow.svg) Mehr Einstellungen

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-Kontrastmodus.svg)Kontrastmodus![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-able-reset-top.svg)

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eyeable-right-arrow.svg) Mehr Farben.

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-Bluefilter.svg)Blaufilter aktivieren

Intensität

80%

![Blaufilter reduzieren](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/bluefilter_minusRanger.svg)![Blaufilter verstärken](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/bluefilter_plusRanger.svg)

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-Nightmode.svg)Nachtmodus

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-Vorlesen.svg)Webseite vorlesen

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-Keyboard.svg)Tab Navigation

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-Farbschwaeche.svg)Farbschwäche

Intensität

80%

![Farbfilter reduzieren](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/minusRanger.svg)![Farbfilter zurücksetzten](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/eye-able-main-zoom-reset.svg)![Farbfilter verstärken](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/plusRanger.svg)

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-Image.svg)Bilder ausblenden

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-BigCursor.svg)Mauszeiger vergrößern

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-Animation.svg)Animationen stoppen

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-More-Functions.svg)Mehr Funktionen

![](https://www.wifa.uni-leipzig.de/_assets/89f4369f29e16b23ff4835f5790afe07/EyeAble/public/images/Eye-Able-Main-reset.svg)Alles zurücksetzen

➜ Eye-Able für mich ausblenden

Seite visuell anpassen!

Steuerungshilfe: