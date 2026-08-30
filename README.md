# Gemini Designer

Gemini Designer is a Gemini 3.7 Flash design advisor skill for agents. It helps with UI critique, UX critique, component-choice review, interaction-flow review, design direction, HTML mockups, SVG icons, handwritten wordmarks, and file-based design feedback.

The skill asks Gemini 3.7 Flash for design judgment through the official Google Antigravity CLI (`agy`), then lets the main agent decide how to apply the advice in the current workspace. It does not call ZenMux, OpenCodex, or a provider API directly.

## Install

The easiest way is to give this GitHub repository to an agent such as Codex, Claude Code, or Cursor and ask it to install the skill:

```text
https://github.com/Vontean/gemini-designer
```

You can also install it directly from a terminal:

```bash
npx skills add Vontean/gemini-designer
```

After installation, agents should use the `gemini-designer` skill when a task needs external design judgment.

## Requirement and authorization

Install and sign in to the official [Google Antigravity CLI](https://antigravity.google/docs/cli/install/). Gemini Designer reuses its local Antigravity session and shared agent harness.

Verify the connection with:

```bash
agy models
gemini-designer auth status
```

Gemini Designer reads its own non-secret defaults from:

```text
~/.config/gemini-designer/config.toml
```

The default model is:

```text
gemini-3.7-flash-high
```

Authentication remains owned by Antigravity. Gemini Designer does not read, copy, or store API keys or OAuth tokens.

## What Agents Should Know

- Each Gemini Designer call starts a new Antigravity headless run. It receives the current prompt, embedded text files passed with `-f`, and local image paths passed with `-i`.
- For visual/UI review, use `gemini-designer ui`.
- For UX, component-choice, task-flow, interaction, friction, or state-feedback review, use `gemini-designer ux`.
- For combined UI + UX review, use `gemini-designer ui,ux` or run `ui` and `ux` separately.
- For broad art direction or design imagery markdown, use `gemini-designer direction`.
- For new standalone HTML mockups, use `gemini-designer html`.
- For SVG icons, simple illustrations, and single handwritten wordmarks, use `gemini-designer svg`.
- Pass complete relevant files when Gemini needs to judge an existing design.
- Pass screenshots or visual references with `-i` when the visible result or state sequence matters. Antigravity inspects them with its local image tools.
- Do not ask Gemini to patch project files directly. Use its advice, then apply the changes in the workspace.

## CLI

The skill installs a global command:

```bash
gemini-designer
```

Typical examples:

```bash
gemini-designer ui "给这个页面提视觉/UI设计建议" -f ./design.html -o design-page-ui.md
gemini-designer ux "评审这个页面的任务流、交互摩擦和状态反馈" -f ./design.html -o design-page-ux.md
gemini-designer ui,ux "同时从 UI 和 UX 角度评审这个标签编辑组件" -f ./TagEditor.tsx -o tag-editor-review.md
gemini-designer direction "给这个产品生成设计意象 markdown" -o product-design-imagery.md
gemini-designer html "生成一个完整的产品页面设计稿" -f ./brief.md -o ./designs/product-page.html
gemini-designer svg "为 Museon 生成一个手写 SVG 字标" -o museon-wordmark.svg
```

Bare output filenames are saved under `.gemini-designer/` in the current workspace.

For multi-command markdown review, a single `-o` value is suffixed per command. For example, `-o tag-editor-review.md` writes `tag-editor-review-ui.md` and `tag-editor-review-ux.md`.

## Repository Layout

```text
SKILL.md
scripts/gemini-designer
scripts/install_cli
```

`SKILL.md` tells agents when and how to use Gemini. `scripts/install_cli` installs the CLI into the user's local bin directory. `scripts/gemini-designer` is the command agents call.

The wrapper always invokes `agy` in non-interactive plan mode, pins `gemini-3.7-flash-high` by default, captures JSON output, and keeps generated artifacts under the caller's workspace.
