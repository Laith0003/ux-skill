# Color

An invented system kept only in rule files: a palette keyed by step, and
the roles each surface and text plays, in light and dark.

## Palette

| Step | Slate | Fern |
|---|---|---|
| 50 | #f6f7f9 | #effaf2 |
| 500 | #64748b | #2f9e55 |
| 900 | #141821 | #123d22 |

## Roles

| Token | Value | Dark | Notes |
|---|---|---|---|
| `color.surface.page` | {slate.50} | {slate.900} | The page behind everything |
| `ink.body` | {slate.900} | {slate.50} | Running text |
| `accent.fill` | {fern.500} | {fern.500} | Primary buttons |

| Do | Avoid |
|---|---|
| Put body text on the page surface | Put body text on the accent fill |
