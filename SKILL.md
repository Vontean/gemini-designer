---
name: gemini-designer
description: Use Gemini 3.7 Flash through the local Google Antigravity agent as the required external design advisor when a task needs UI critique, UX critique, component-choice review, interaction-flow review, design imagery markdown, art direction, visual hierarchy judgment, design-system fit, color/type/layout suggestions, HTML mockups, SVG icons, handwritten SVG wordmarks, or file-based feedback on existing UI. Trigger on requests like "design a page", "generate design imagery", "give design advice", "optimize this UI", "improve UX", "optimize user flow", "review interaction", "check usability", "reduce friction", "choose the right component", "review this design", "create an icon", "suggest colors", "UI mockup", "visual direction", "lettering", "wordmark", "handwritten logo", or when another agent needs a second opinion on visual or interaction quality.
---

# Gemini Designer — UI, UX, and Visual Design Advisor

Use Gemini 3.7 Flash through Google Antigravity as an external advisor for visual design, UI finish, UX task flow, interaction friction, art direction, and lightweight design artifacts.

## Critical rules

- In the Codex desktop app, interact with Gemini through a visible, interactive Antigravity CLI (`agy`) running inside a Side Panel Terminal. Do not use the headless `gemini-designer` wrapper as the normal Codex path.
- Open the Side Panel Terminal first. In that exact Terminal, start `agy` with the current workspace, `gemini-3.7-flash-high`, `accept-edits`, and sandbox enabled. Only after the Antigravity TUI is visible and ready should Codex send the design task through the same Terminal session.
- Keep the interactive `agy` process alive while the design task is active. Send refinements, corrections, implementation follow-ups, and related design questions into that same Terminal session so Gemini retains the thread context.
- Start a new interactive `agy` session for an unrelated design goal, a deliberately independent alternative, or a clean-slate review. If a relevant session was closed, resume its exact conversation ID instead of using the workspace's ambiguous most-recent conversation.
- When this skill is used, ask the interactive Agy session before giving UI advice, UX advice, design imagery, art direction, critique, visual advice, HTML, or SVG output. Do not replace Gemini's design judgment with the Codex agent's own judgment.
- Do not call ZenMux, OpenCodex, or a provider API directly. Outside the Codex desktop app, or only when an interactive Side Panel Terminal is unavailable, use the global `gemini-designer` wrapper as the compatibility fallback.
- For visual/UI review, tell the interactive Agy session to focus on visual hierarchy, typography, color, spacing, surfaces, component appearance, consistency, and finish.
- For UX review, tell the session to focus on task model, component choice, flow, friction, affordance, recoverability, validation, navigation, and visible states.
- For requests that need both UI and UX review, ask for both dimensions in the same live session when they inform one design decision. Use independent sessions only when the user wants independent judgment.
- For broad art direction or design imagery, ask the session to act as a visual design director and ground its judgment in the provided product context and references.
- For HTML, SVG, icons, illustrations, or wordmarks, tell the session the exact artifact type and workspace output path, then let Agy create the file directly.
- If the user provides screenshots, mockups, moodboards, or visual references, include relevant images with `-i / --image` when they help Gemini judge visual style, layout, hierarchy, mood, fidelity, interaction sequence, or state transitions.
- A new Gemini conversation is stateless. Give the interactive Agy session the concrete task, relevant workspace paths, screenshots, design rules, and constraints it needs. Once the session has that context, do not resend the entire history on every follow-up.
- Do not run two Codex agents against the same live Agy Terminal. UI and UX may share one interactive thread when they are part of the same design decision; use separate Agy sessions only when independent judgment is intentional.
- Do not ask Gemini to review code quality, technical debt, CSS lint, engineering consistency, performance, or architecture unless the user explicitly asks. Keep Gemini focused on what users can perceive and operate.
- Do not ask Gemini to output code patches or diffs for existing files. Use its design advice, then make the actual edits yourself.
- After Gemini returns UI advice, UX advice, design imagery markdown, visual direction, or an HTML mockup, show the output or a concise summary to the user and wait for confirmation before implementing it in project code, unless the user explicitly asked to implement immediately.
- Because UX changes often affect state logic, routing, form behavior, data loading, or validation, present a summary of structural/logic changes and wait for confirmation before refactoring component logic unless the user explicitly asked to implement immediately.
- After `html` or `svg` returns, do not start an extra AI review, visual critique, browser screenshot check, grep/tail completeness check, or refinement loop unless the user explicitly asked for checking or iteration. The CLI performs structural integrity checks before writing generated HTML/SVG. Read enough to know what Gemini returned, then present it to the user.
- For ordinary HTML, SVG, or icon requests, run the script ONCE per task. Read the output file and proceed.
- Pass the user's stated requirements and concrete project context. Do not add the agent's own style labels, layout choices, color choices, metaphor choices, interaction concepts, or evaluation criteria unless the user explicitly said them.
- Do not pre-design for Gemini. For creative generation, state the user goal, source material, output format, and hard constraints only. Do not name visual directions, metaphors, layouts, palettes, typography, materials, animations, or interaction models unless the user explicitly provided them.
- For multiple alternatives, ask Gemini for independent, clearly different options. Do not assign the options names like "dashboard direction", "editorial direction", or "radar direction" unless the user gave those directions.
- Google Antigravity owns authentication. Do not pre-check authorization before launching the interactive session. If Agy reports an authorization error, tell the user that Antigravity CLI is not authorized.

## Codex Side Panel workflow

The Codex desktop path is an interactive terminal workflow, not a headless subprocess workflow.

1. Create a PTY-backed Terminal in the current Codex task and open it in the Side Panel.
2. In that Terminal, run:

```bash
agy \
  --model gemini-3.7-flash-high \
  --mode accept-edits \
  --sandbox \
  --add-dir "$PWD"
```

3. Wait until the Antigravity TUI shows the signed-in account, model, workspace, and prompt input.
4. Send the design task through that same Terminal session. Keep the task close to the user's wording and include relevant paths or images.
5. Observe Agy's reasoning status, tool calls, permission requests, edits, and response directly in the Side Panel Terminal.
6. For a follow-up on the same design, send another message to the same running Agy session. Do not relaunch Agy and do not reconstruct the earlier context.
7. For HTML, SVG, or another file artifact, tell Agy the exact workspace output path and let it create the file under `accept-edits`; then read that file from Codex.
8. For advisory UI, UX, or direction work, read the completed Agy response from the Terminal and synthesize it for the user.
9. Leave the Agy process running while more iterations are expected. When closing it, retain the exact resume command or conversation ID shown by Agy.

If the Side Panel cannot attach the Terminal, do not silently fall back while claiming the run is visible. Tell the user that the Codex Terminal is not attached, then use the compatibility fallback only if continuing without the visible TUI is acceptable.

## Compatibility fallback CLI

Use `gemini-designer` only outside the Codex desktop app or when an interactive Side Panel Terminal is unavailable and a headless fallback is acceptable.

Do not run install or auth checks before every fallback use.

If the shell reports `command not found`, resolve `/path/to/this-skill` to the directory containing this `SKILL.md`, run `bash /path/to/this-skill/scripts/install_cli` silently, then retry the original `gemini-designer` command. Use `bash` explicitly because archive-based Skill installers may not preserve executable bits. If the installer reports a `path_warning`, use the printed `installed_path` for this turn and tell the user that the CLI directory is not on PATH.

If the CLI reports an Antigravity authorization failure, stop and tell the user to sign in through Antigravity CLI. Do not read, copy, print, or manage API keys or OAuth tokens.

Each fallback command has its own built-in prompt. Choose the right command and pass the user's task plainly; do not add a cross-command prompt framework, design direction, UX solution, or extra output rules unless the user explicitly gave them.

Commands:

- `gemini-designer ui` — Use for visual/UI review: layout, hierarchy, density, typography, color, spacing, surfaces, shadows, component appearance, visual consistency, and UI finish. It may include `-f` and `-i` as reference context, and requires a readable markdown file name with `-o`.
- `gemini-designer ux` — Use for UX and interaction review: task model, component choice, flow, friction, control structure, affordance, recoverability, validation, navigation clarity, accessibility when it affects usability, and loading/error/empty/success/disabled/hover/focus/active states. It may include `-f` and `-i` as reference context, and requires a readable markdown file name with `-o`.
- `gemini-designer ui,ux` — Use when the user wants both visual/UI and UX review. The CLI runs independent markdown review commands and writes one output per command.
- `gemini-designer direction` — Use before implementation when the task needs a stronger idea, art direction, visual metaphor, design imagery markdown, or high-level design direction. Files are optional. Always provide a readable markdown file name with `-o`.
- `gemini-designer html` — Use for a new standalone HTML mockup or concept page. It may include `-f` and `-i` as reference context, but do not use it to directly revise an existing project file.
- `gemini-designer svg` — Use for a new SVG icon, simple illustration, or single handwritten SVG wordmark. It may include `-f` and `-i` as reference context.

When `ui` or `ux` needs to judge existing UI, pass complete relevant files by default. Do not summarize, slice, or annotate the file unless the file is too large for the CLI limit or the user asks for a scoped review. Prompt-only `ui` or `ux` is fine for general design questions.

For `ui`, `ux`, and `direction`, always name the markdown file at call time with `-o`. Prefer a bare readable filename, such as `accounts-filter-ui.md`, `tag-editor-ux.md`, `museon-home-art-direction.md`, or `pricing-page-design-imagery.md`; the CLI saves bare names under `.gemini-designer/`. Use an explicit path only when a specific directory is required.

For multi-command markdown review, pass a single readable `-o` name. The CLI suffixes it per command:

```bash
gemini-designer ui,ux "评审这个标签编辑组件" \
  -f ./TagEditor.tsx \
  -f ./tag-editor.css \
  -o tag-editor-review.md
```

This writes separate outputs such as `tag-editor-review-ui.md` and `tag-editor-review-ux.md`.

For `html` and `svg`, pass files with `-f` when Gemini should reference existing content, design rules, previous mockups, theme tokens, example components, or brand references. Treat those files as context for a new design draft, not as files Gemini will patch in place.

For `html`, describe the design goal only. Do not ask Gemini to save a file, return a `file://` URL, provide a download link, or explain where the file is. The CLI writes the output file; Gemini must return raw complete HTML source only.

For `html`, do not mention asset or dependency policy by default. Let Gemini decide whether images, fonts, scripts, stylesheets, icon libraries, audio, or video help the design. Only add asset constraints when the user explicitly asks for them, such as fully self-contained, offline-safe, no external resources, or use realistic public images.

For handwritten wordmarks, use `svg` when the user wants one asset, and use `html` when the user wants several candidates to compare. Describe the word or words, mood, and any explicit material preference from the user. Do not prescribe neon, metal, sci-fi, or other effect-heavy styles unless the user asked for them. The default direction is readable paper-and-ink SVG lettering with subtle writing animation and tasteful finishing marks when useful.

The built-in `direction`, `html`, and `svg` prompts lightly remind Gemini to avoid generic AI templates and default category stereotypes, keep the subject immediately recognizable through concrete sensory anchors, ground design choices in the product subject and real content, use purposeful contrast when it improves visual communication, spend visual boldness in one important place, and keep surrounding UI quiet.

## Context Rules

An interactive Agy session retains its conversation context. A new session receives only what Codex sends or what Agy reads from the active workspace. The headless fallback receives only the command text, files passed with `-f`, and images passed with `-i`.

The CLI places the final user goal after reference files and image manifests so Gemini sees the concrete task last. Agents should keep the task text close to the user's wording instead of repeating constraints in several places.

When asking about an existing UI, pass the smallest complete set of files needed for the judgment:

- The target file or component being judged
- The project design guide or style reference, if one exists in the workspace
- Related CSS/theme/token files when they materially affect the visual result
- Nearby component files only when they define visible structure, visible states, or reused UI patterns
- State, hook, form, validation, routing, or context files when they materially affect UX behavior
- Screenshots, mockups, moodboards, reference images, exported previews, or sequential state screenshots when the user's question depends on what the UI looks like or how it changes

For `ui`, prioritize visible/rendered context:

- Target component or page files
- CSS/theme/token files
- Design-system or style-reference files
- Screenshots, rendered previews, mockups, or visual references

For `ux`, visual files are not enough. Include context that defines the user's task and state transitions:

- Component files that define controls, states, validation, and visible behavior
- Existing component-library files or nearby examples when the question depends on choosing the right control pattern
- Hooks, context, route, form, schema, or data-loading files that control the flow
- Copy/config files that affect labels, errors, confirmations, empty states, or success states
- Sequential images such as `-i step1.png -i step2.png` when the experience spans multiple states
- The intended user task, if it is not obvious from the files

Prefer complete files over excerpts. Use multiple `-f` flags:

```bash
gemini-designer ui "判断这个页面是否符合项目现有视觉风格，并给出具体优化建议" \
  -f ./design.html \
  -f ./src/styles/tokens.css \
  -f ./src/components/Button.tsx \
  -o design-page-ui.md
```

```bash
gemini-designer ux "评审这个标签编辑组件的任务模型和交互状态" \
  -f ./src/components/TagEditor.tsx \
  -f ./src/hooks/useTags.ts \
  -i ./screenshots/tag-editor-open.png \
  -o tag-editor-ux.md
```

Use `-i` for image context:

```bash
gemini-designer ui "结合截图给这个页面提视觉设计建议" \
  -f ./design.html \
  -i ./screenshots/current.png \
  -o current-page-ui.md

gemini-designer direction "参考这张图，生成设计意象 markdown" \
  -i ./references/moodboard.png \
  -o product-design-imagery.md
```

When images are passed with `-i`, the wrapper gives Antigravity the original local paths and asks it to inspect them with its local image tools. Agents should pass readable absolute or workspace-relative paths.

Do not pass unrelated source files, build output, dependency folders, logs, or implementation details that do not affect the visual result or user-visible interaction. If the needed context is too large, choose representative design-system files and say in the task text what is missing.

If Gemini's `ui` or `ux` output says it needs more context, do not treat that as final advice. Gather the requested files or information when available, then rerun the same command once with the added `-f` or `-i` inputs. If the requested context cannot be found, tell the user exactly what is missing and ask for it.

The built-in `ui` prompt asks Gemini to:

- focus on visual effect, information hierarchy, reading rhythm, typography, color, spacing, surfaces, component appearance, UI finish, and emotional tone
- avoid code review, CSS hygiene critique, technical debt, architecture, business logic, and new feature suggestions
- explain exactly where to change, how to change it, and why the visual result improves
- include pseudo-code, CSS, or JSX snippets when useful, with enough length to explain the change, without outputting a full file
- remind the implementing agent to prefer existing components, selectors, classes, tokens, variables, layout patterns, and interaction patterns
- name reusable components or tokens only when they are visible in the provided files; otherwise do not invent project-specific names
- include a short "do not change" section when there are concrete areas, tokens, components, visual traits, copy, or states that should be preserved
- ask for missing context instead of guessing when a reliable UI judgment is not possible

The built-in `ux` prompt asks Gemini to:

- focus on natural task model, component choice, cognitive load, interaction friction, control structure, affordance, recoverability, validation, navigation clarity, accessibility when it affects usability, and visible state feedback
- judge whether the chosen component or control pattern matches the task, such as using an editable tag/chip editor for tag editing instead of separate add and delete inputs
- evaluate loading, error, empty, success, disabled, hover, focus, and active states when relevant
- avoid pure visual polish unless it directly harms usability
- avoid product strategy, feature bloat, gamification, broad repositioning, code review, CSS hygiene, technical architecture, and file-structure critique
- work within the existing product scope and user goal
- provide concrete structural, component-pattern, interaction, copy, state, or layout changes
- ask for missing state logic, routing, component code, component-library examples, form validation, or sequential screenshots instead of guessing when reliable UX judgment is not possible

## Parallel Review

When the user asks for multiple review dimensions, run each relevant command independently. Do not collapse UI, UX, art direction, HTML, or SVG work into one broad prompt.

For UI + UX review:

1. Run `gemini-designer ui` and `gemini-designer ux` separately, or run `gemini-designer ui,ux` so the CLI writes independent outputs.
2. Pass the same user goal to both commands without adding agent-authored visual styles, interaction metaphors, palettes, layouts, or UX solutions.
3. Give `ui` screenshots, rendered previews, style tokens, theme files, and visible component files.
4. Give `ux` component logic, state files, routing files, component-library examples, form/validation logic, and sequential screenshots when available.
5. After both outputs return, synthesize them for the user:
   - Present UX first: task model, component choice, flow, state feedback, friction, and recoverability.
   - Present UI second: hierarchy, typography, spacing, polish, and visual consistency.
   - If UX and UI advice conflict, prioritize the UX structural decision first and explicitly note which UI advice only applies if the affected element remains.

Useful commands:

```bash
gemini-designer ui "给这个页面提视觉/UI设计建议" -f ./design.html -o design-page-ui.md
gemini-designer ux "评审这个页面的任务流、交互摩擦和状态反馈" -f ./design.html -o design-page-ux.md
gemini-designer ui,ux "同时从 UI 和 UX 角度评审这个标签编辑组件" -f ./TagEditor.tsx -o tag-editor-review.md
gemini-designer ui "结合截图给这个页面提视觉/UI设计建议" -f ./design.html -i ./screenshots/current.png -o page-screenshot-ui.md
gemini-designer direction "给这个产品生成设计意象 markdown" -o product-design-imagery.md
gemini-designer direction "基于这个页面生成设计意象 markdown" -f ./design.html -o page-design-imagery.md
gemini-designer html "基于这个页面生成一个完整、全新的落地页方案。保留产品信息，由你独立判断视觉方向，不要复刻原稿。" -f ./design.html -o ./designs/page.html
gemini-designer html "基于这个页面生成第 1 个完整落地页方案。保留产品信息，由你独立判断视觉方向。后续方案需要彼此明显不同。" -f ./design.html -o ./designs/page-option-1.html
gemini-designer svg "为 Museon 生成一个手写 SVG 字标，气质像策展笔记标题" -o museon-wordmark.svg
gemini-designer html "展示 Museon、Mel、Signal 三个手写 SVG 字标候选，默认偏纸面墨迹和真实笔触" -o wordmark-candidates.html
gemini-designer svg "生成一个设置图标" -f ./brand.md -o ./icons/settings.svg
```

Read every output file before acting. Apply only the suggestions that fit the project.

`ui`, `ux`, and `direction` outputs include a final `原始提示词` section. It records the task text and readable paths for referenced files or images, without copying the full file contents into the appendix.

For advisory outputs (`ui`, `ux`, and `direction`) and HTML mockups from Gemini, do not immediately edit project files. Present Gemini's output or a concise summary, ask the user to choose or confirm the direction, then implement only the confirmed parts. SVG icon output can be saved directly when the user's request is only to create the asset. Do not run a self-review pass just because an HTML or SVG file was created.

The script prints on success:

```text
output_path=<path to output file>
conversation_id=<Antigravity conversation ID>
```

For multi-command review, it prints one path per command:

```text
output_path[ui]=<path to UI output file>
output_path[ux]=<path to UX output file>
conversation_id[ui]=<UI Antigravity conversation ID>
conversation_id[ux]=<UX Antigravity conversation ID>
```

Continue the same design thread with the exact ID:

```bash
gemini-designer ui "根据上一轮反馈继续收敛层级方案" \
  --conversation <conversation-id> \
  -f ./design.html \
  -o design-page-ui-v2.md
```

Headless CLI conversations do not automatically appear in the Antigravity 2.0 desktop conversation list. The official CLI currently exposes the conversation ID for resuming with `agy --conversation <id>`, but does not expose a headless CLI flag that exports or opens that conversation in the desktop client. Do not copy or rewrite Antigravity conversation databases to work around this boundary.

For `html` and `svg`, the script also prints:

```text
integrity=passed
```

Read the file at `output_path` to get Gemini's response.

On failure, the CLI prints stable fields:

```text
error=<code>
message=<short explanation>
hint=<next step>
```

Follow the `hint` when it is actionable. If Antigravity reports an authorization failure, stop and tell the user Antigravity CLI is not authorized.

For generated HTML/SVG, treat `output_path` plus `integrity=passed` as the normal completeness signal. Do not duplicate CLI checks in the agent unless the user asks for additional browser or visual verification.

## Output types

- `gemini-designer ui` — Markdown UI review output.
- `gemini-designer ux` — Markdown UX review output.
- `gemini-designer direction` — Markdown design direction output.
- `gemini-designer html` — Self-contained complete HTML source with inline CSS. Ready to open in browser. The CLI rejects incomplete HTML, missing head/body, file URLs, markdown fences, lorem ipsum, and non-HTML wrapper output.
- `gemini-designer svg` — Clean SVG code for icons, simple illustrations, or single handwritten wordmarks. The CLI rejects invalid XML, wrapper text, markdown fences, and local file URLs. Can be saved directly or embedded in HTML/React.

## Configuration

- The global CLI reads `~/.config/gemini-designer/config.toml`.
- The default model is `gemini-3.7-flash-high`; change the flat `model` value only when the user explicitly wants another Antigravity model slug.
- The wrapper calls `agy` in non-interactive `accept-edits` mode, renders its `stream-json` events as readable live Terminal progress, and parses the terminal result.
- Authentication remains owned by Google Antigravity. Agents should not read, copy, or manage API keys or OAuth tokens.
- Do not check authorization in the normal path. Use `gemini-designer auth status` only when explicitly debugging authorization.

## When to use

- Need Gemini to inspect existing HTML/CSS/TSX and give visual UI advice
- Need Gemini to inspect existing UI and give UX, interaction, task-flow, or state-feedback advice
- Need a concise visual or UX optimization plan based on one or more local files
- Need a visual reference or HTML mockup for a UI component or page
- Need handwritten SVG wordmark, lettering, signature mark, or logo-like text candidates
- Need SVG icons or simple illustrations
- Need color palette, typography, or layout suggestions
- Need design feedback or critique on an existing design
- Want a quick single-page HTML prototype to show a concept

## Workflow

1. Open the Side Panel Terminal and start interactive `agy`.
2. Choose the smallest useful Gemini task: UI, UX, direction, HTML, or SVG.
3. Send the user's task to the running Agy session using the user's wording whenever possible. Add only factual context needed to identify files, product scope, or explicit constraints.
4. Keep related iterations in the same Agy session; start a new session only for unrelated or intentionally independent work.
5. Read Gemini's Terminal response or the file artifact it created.
6. If Gemini says more context is needed, send the missing paths, state details, or screenshots into the same session and continue.
7. When implementing Gemini's advice, first look for existing project components, selectors, classes, tokens, variables, and layout patterns to reuse.
8. If Gemini drifts into code review, correct it in the same session: "只从 UI/UX 角度判断，不要评论代码规范或工程债。"
9. Present advisory outputs or HTML mockups to the user for confirmation before editing project code, unless the user explicitly asked to implement immediately.
10. Base the final response on Gemini's output. You may summarize, select, or implement useful parts, but do not replace Gemini's design judgment with your own generated design direction.

## Tips

- Keep the task prompt close to the user's request.
- If the user did not specify a style, color, font, layout, metaphor, visual direction, or interaction model, do not invent one in the prompt.
- Do not split multiple Gemini generations by agent-authored themes. Use neutral wording such as "第 1 个独立方案 / 第 2 个独立方案 / 第 3 个独立方案" and ask Gemini to make them clearly different through its own judgment.
- When passing a reference design, say whether Gemini may preserve or should avoid copying it. Do not replace that with your own alternate concepts.
- For HTML mockups, do not mention asset or dependency rules unless the user asks. Unnecessary constraints can weaken Gemini's design judgment.
- Only pass explicit user preferences, such as "dark mode" or "use blue", when the user actually said so.
- When the task asks for design insight, direction, or an HTML mockup, do not ask Gemini for long explanatory copy. Let Gemini express ideas through visible UI structure, states, examples, hierarchy, and interaction when possible.
- Do not translate "more designed" into visual noise. Strong visual treatment should support key actions, brand memory, and key content entry points; supporting areas should stay quiet, stable, and easy to scan.
- Let Gemini decide how to avoid cliches. Do not add your own list of banned styles, but pass explicit user constraints such as "避免俗套科技感、赛博朋克感" when the user says them.
- Let Gemini actively consider motion, inline SVG, material, and micro-interaction opportunities, but do not prescribe a specific animation or material style unless the user asked for it.
- Do not add your own anti-template checklist to the task prompt. The CLI already gives Gemini light reminders about generic AI aesthetics, memorable visual ideas, restraint, real content, and UI copy.
- Chinese prompts work well — Gemini responds in the same language.
