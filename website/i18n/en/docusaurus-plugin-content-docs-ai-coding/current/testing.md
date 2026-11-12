---
id: testing
title: 'Testing for AI-Written Code'
sidebar_label: 'Testing'
sidebar_position: 13
---

# Testing for AI-Written Code

:::info What this page covers

- A way of working that agrees on tests first and then hands over implementation
- Three layers of control that stop agents from weakening tests
- Measuring the quality of the tests themselves with coverage and mutation testing
- Isolated, reproducible execution environments and flaky-test handling

It is written for developers, test and quality staff, and teams that run CI.
:::

AI coding tools increase the volume of change. The number of reviewers stays the same, so checking
behavior by having a person read every line soon reaches its limit. The standard for deciding whether
a change is right then becomes the tests. With weak tests, the only way to check AI-written code is a
human reading it; with solid tests, the range of work you can hand to agents grows.

This page covers how to make tests the verification standard for AI coding: a test-first way of
working, the problem of agents weakening tests and how to defend against it, measuring the quality of
the tests themselves, and isolated execution environments. Each item is a working file in the
[ai-coding-best-practice](https://github.com/trustedoss/ai-coding-best-practice) repository.

## 1. Why tests are part of governance

Stage 3 gates in the [5-Stage Strategy](./strategy) look for known risk patterns: secrets, vulnerable
code patterns, prohibited licenses. No scanner answers "does this function do what the requirement
says?" Tests answer that question.

DORA's 2025 report finds that AI adoption raises delivery throughput but also raises delivery
instability. As changes increase, instability passes straight into production unless something
automatically confirms that changes did not break existing behavior. Tests are that mechanism.

This becomes clearer as agents run in repeated loops instead of being directed step by step. A study
of 50 public agent loops (Macedo, 2026-06) defines a loop specification as a trigger, a goal, a
verification step, a stopping rule, and memory. Without a verification step a loop cannot tell when it
is done; with a weak one it stops on a wrong result. For most code work that verification step is the
test suite.

In short, in AI coding tests are a control before they are a quality activity. Tests tell the agent
what "done" means, and they decide what a reviewer can trust and what must still be checked.

## 2. Agree on tests first, then hand over implementation

If you hand an agent both implementation and tests at once, the agent writes tests that match its own
implementation. If the implementation has a bug, the tests record the bug as the expected answer.
Passing tests then only restate the implementation instead of checking the requirement.

Splitting the order reduces this.

1. Write the requirement as tests. A person writes them, or an agent drafts them and a person reviews.
2. Confirm the tests fail and commit them. A test that does not fail checks nothing.
3. Tell the agent to make the tests pass by changing only the implementation, not the tests.
4. When they pass, a person reviews the implementation. The review now narrows to design and
   maintainability, because the tests have already checked behavior.

Vendor guidance recommends the same order. Anthropic's Claude Code best practices (2025-04) described
a flow of writing and committing tests before implementing, telling Claude it is doing test-driven
development and must not modify the tests, and using independent subagents to check that the
implementation is not overfitting to the tests. The current documentation sums it up as giving Claude
something it can run that comes back pass or fail. GitHub's Spec Kit treats test-first as a
non-negotiable principle of its spec-driven development method.

Writing this order in the repository's rules file makes the agent follow it every time. The "테스트
정책" (testing policy) section of the
[CLAUDE.md](https://github.com/trustedoss/ai-coding-best-practice/blob/main/CLAUDE.md) in
ai-coding-best-practice is an example.

## 3. Agents weakening tests

An agent facing a failing test sometimes changes the test instead of fixing the code: deleting it,
adding `skip`, changing the expected value to the current output, or special-casing the implementation
for specific inputs.

There are measurements. ImpossibleBench (2025-10) gave tasks where the specification and tests
contradict each other, so the only way to pass is to cheat the tests. On one task set GPT-5 did so in
76% of tasks. When Claude models cheated, more than 79% of the cases were done by modifying the tests
themselves. Stricter prompting
reduced one model's rate from 92% to 1%, but the authors also recommend hiding tests or making them
read-only. METR (2025-06) reported that a frontier model tampered with scoring in 30.4% of runs on one
benchmark, and that telling it not to cheat did not reduce the rate much.

Writing "do not change tests" in the rules file is not enough; Stage 2 rules are advice here too. Block
it in three layers.

| Where         | Control                                                                                      | ai-coding-best-practice file                                                                                                                                                                                                                           |
| ------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Agent session | Editing `tests/` requires human approval                                                     | `Edit(./tests/**)` in [.claude/settings.json](https://github.com/trustedoss/ai-coding-best-practice/blob/main/.claude/settings.json)                                                                                                                   |
| Pull request  | Fails when test files or functions are deleted, `skip`/`xfail` is added, or asserts decrease | [test-integrity.yml](https://github.com/trustedoss/ai-coding-best-practice/blob/main/.github/workflows/test-integrity.yml), [check-test-integrity.py](https://github.com/trustedoss/ai-coding-best-practice/blob/main/scripts/check-test-integrity.py) |
| Review        | Changes to `tests/` request owner review                                                     | [CODEOWNERS](https://github.com/trustedoss/ai-coding-best-practice/blob/main/.github/CODEOWNERS)                                                                                                                                                       |

![When an agent edits tests/, the change passes human approval in the agent session, the integrity check on the pull request, and CODEOWNERS review before merge](/img/ai-coding/ai-coding-test-defense-en.png)

Sometimes removing a test is right: the feature was removed, or the test was pinning wrong behavior.
So the test-integrity check is designed as a confirmation step, not a ban. When an owner has read the
change and adds the `test-change-approved` label, the check passes. The label is the record that a
person decided.

The script compares `tests/` on the base branch and the PR with Python's `ast` module. It reads the
syntax tree, not regular expressions, so an `assert` inside a comment or string does not fool it. A
commit in the repository that deliberately deleted one test and added `skip` to another produced:

```text
Test suite weakened:
  - deleted test function: tests/test_app.py::test_fetch_rejects_missing_url
  - added skip/xfail marker(s): tests/test_app.py (+1)
  - assert count dropped: 18 -> 17
```

## 4. Measuring test quality: coverage and mutation testing

Coverage is the share of lines the tests executed. It does not tell you whether the tests would notice
a wrong result on those lines. A test with no asserts can reach 100% coverage. When AI generates tests
in bulk, such tests slip in easily.

Mutation testing measures this gap. The tool creates mutants by making small changes to the source
(flipping a comparison, changing a constant, removing a call) and reruns the tests for each mutant. If
a test fails, the mutant was killed; if the tests pass, they did not notice the error. The list of
surviving mutants is the list of asserts to add.

| Language                         | Tool                                      |
| -------------------------------- | ----------------------------------------- |
| Python                           | [mutmut](https://github.com/boxed/mutmut) |
| Java                             | [PIT](https://pitest.org/)                |
| JavaScript/TypeScript, C#, Scala | [Stryker](https://stryker-mutator.io/)    |

Current versions as of 2026-11 are mutmut 3.8.1, PIT 1.30.2, StrykerJS 10.1.1, and Stryker.NET 5.1.0.
mutmut needs an operating system with `fork` support, so on Windows run it inside WSL. Its settings go
in `[tool.mutmut]` in `pyproject.toml`; from 3.6.0 the target path key was renamed from
`paths_to_mutate` to `source_paths`.

Mutation testing reruns the suite for every mutant, so it is slow. Rather than running it on every PR,
run it periodically, read the results, and promote it to a gate once the score is stable.
ai-coding-best-practice blocks PRs in
[tests.yml](https://github.com/trustedoss/ai-coding-best-practice/blob/main/.github/workflows/tests.yml)
on tests and a 90% coverage floor, while
[mutation.yml](https://github.com/trustedoss/ai-coding-best-practice/blob/main/.github/workflows/mutation.yml)
runs as advisory every Monday and lists surviving mutants in the job summary.

One constraint showed up while applying it. mutmut 3 skips functions with decorators. Every Flask
route handler carries `@app.route`, so the first run produced no mutants at all. Only after moving the
search logic and URL check into plain functions, with the handlers just calling them, did 9 mutants
appear, and the tests killed all 9. Thin handlers help unit testing as much as mutation testing.

## 5. Isolated, reproducible execution environments

For agents to run tests themselves, the environment must meet two conditions.

First, isolation. An agent running tests executes shell commands. Run it in a sandbox so it cannot
reach the developer workstation's credentials or production. Per-tool setup is in the "Isolation and
Sandboxing" section of each tool page (for example [Claude Code](./tools/claude-code#isolation-and-sandboxing)).

Second, reproducibility. The same commit must give the same result for anyone at any time, or the
agent's judgment cannot be trusted.

- Pin dependency versions. ai-coding-best-practice pins even the test tools to exact versions in
  `requirements-dev.txt`.
- Replace external network calls in tests. A test whose result depends on an external service gives
  the agent wrong signals. The repository's `/fetch` test replaces the response with `unittest.mock`.
- Use the same command locally and in CI. Running CI's `pytest --cov=src --cov-fail-under=90` locally as
  well keeps the result the agent saw locally and the gate's verdict in line.
- Fixing the runtime with containers or a development container (devcontainer) also removes
  operating-system differences.

## 6. Flaky tests

A test that passes and fails on the same code is especially harmful with AI coding. The agent sees a
failure and tries to fix the code, and when the next run passes by chance it concludes the fix was
right. People get used to ignoring failures as "it sometimes fails", and real failures get buried too.

Do not delete flaky tests or quietly add `skip`. Put them on a quarantine list with an owner and a
deadline for fixing. Adding `skip` triggers the test-integrity check, so the owner who adds the label
records the reason for quarantine in the PR. A growing quarantine list is itself a signal to review
the test environment.

## 7. Relation to fuzzing

[AI Fuzzing](./ai-fuzzing) (4b) is also a form of testing, but with a different purpose. The tests on
this page check requirements a person defined. Fuzzing throws inputs nobody wrote down as requirements
to find unexpected behavior. A defect found by fuzzing must have its reproducing input turned into a
regression test so it does not return. The two are not substitutes but steps in order.

## 8. Adoption order

| Order | What to do                                                               | Enforcement                |
| ----- | ------------------------------------------------------------------------ | -------------------------- |
| 1     | Write core behavior tests and run them in CI                             | Blocking                   |
| 2     | Write test-first work and the ban on weakening tests into the rules file | Advisory                   |
| 3     | Add the test-integrity check and CODEOWNERS                              | Blocking (label overrides) |
| 4     | Set a coverage floor at the current level                                | Blocking                   |
| 5     | Run mutation testing periodically and read the results                   | Advisory                   |

Do not start the coverage floor high; start at the current value and raise it. If people start writing
assert-free tests to clear the floor, step 4 makes the tests weaker. Step 5 exposes that case.

## Standards linkage and sources

The controls on this page do not directly satisfy a specific clause of ISO/IEC 5230 or 18974. They do
provide evidence for ISO/IEC 18974 §4.3.2 that a fix did not introduce a regression, and they leave
records (labels, CODEOWNERS reviews) showing that the review and approval steps set in the usage
policy were actually followed.

- DORA, [State of AI-assisted Software Development 2025](https://services.google.com/fh/files/misc/2025_state_of_ai_assisted_software_development.pdf) (2025-09)
- Anthropic, [Claude Code best practices](https://web.archive.org/web/20250602202220/https://www.anthropic.com/engineering/claude-code-best-practices) (2025-04-18, archived copy) / [current Best practices](https://code.claude.com/docs/en/best-practices)
- GitHub, [Spec Kit](https://github.com/github/spec-kit) (`spec-driven.md`, Article III Test-First Imperative)
- Zhong et al., [ImpossibleBench: Measuring LLMs' Propensity of Exploiting Test Cases](https://arxiv.org/abs/2510.20270) (2025-10-23)
- Macedo, [Stop Hand-Holding Your Coding Agent: Engineering the Loops that Replace Step-by-Step Prompting](https://arxiv.org/abs/2607.00038) (2026-06-28)
- METR, [Recent Frontier Models Are Reward Hacking](https://metr.org/blog/2025-06-05-recent-reward-hacking/) (2025-06-05)
- [mutmut](https://github.com/boxed/mutmut), [PIT](https://pitest.org/), [Stryker](https://stryker-mutator.io/)
- `tests/`, `scripts/check-test-integrity.py`, and `.github/workflows/` in the [ai-coding-best-practice](https://github.com/trustedoss/ai-coding-best-practice) repository

All sources were checked on 2026-11-12.

## Next steps

- [Productivity and Collaboration in AI Coding](./collaboration): small PRs and shared review backed by tests
- [AI Fuzzing](./ai-fuzzing): exploring inputs nobody wrote down as requirements
- [Best Practice Repository](./best-practice-repo): every file covered on this page
- [5-Stage Strategy](./strategy): the test gate to add alongside the Stage 3 gates
