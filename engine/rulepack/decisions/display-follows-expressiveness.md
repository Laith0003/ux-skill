---
id: display-follows-expressiveness
title: A landing display follows expressiveness and the width, and fits the page's own word in each script
status: active
areas: [type, layout, output]
supersedes: landing-display-step
superseded_by: null
---

# A landing display follows expressiveness and the width, and fits the page's own word in each script

## Context

On 35 award-winning pages measured at 1440 wide, the headline's median was 120px (the middle half 85 to 205px), and it grew with how loud the brand read: about 50, 129 and 234px at expressiveness 0.2, 0.5 and 0.9. On a phone it was about half the desktop size, median 60px. Our landing display ran 56 to 104px, and the fit rule held it near 100px by assuming a 13 letter word in seven of twelve columns for every page. A second study of a component kit put the phone headline at about 0.8 of a small desktop headline.

## Decision

character.expressiveness is 0.7 times energy plus 0.3 times playfulness (one minus formality). character.landing_display_px is 60px times 4 to the power of expressiveness at 1440 wide and body 16px: 60px at the calm corner, 120px at the middle of the axes, 240px at the loud one, scaled with the body size and kept 1.08 times the hero. Its phone size is character.phone_display_for the desktop size: 0.8 of it up to 72px, easing in a straight line to half of 120px, then half, within 36 to 90px, so it never falls as the desktop size grows. The word the display must fit is the page's longest headline word per script when the build is given it (build_system words), else 13 Latin and 10 Arabic letters, recorded in type.fit-word; the column is the landing content width inside the landing margins and container, all of it on a phone and a tablet and, from the laptop up, the columns of twelve its composition sets the headline in (typography.HEADLINE_COLUMNS: 7 for split, 8 for the editorial column, 12 otherwise), recorded in type.fit-columns. Each fit factor is computed per script and the role reads the Arabic one under right to left, so a wide Arabic face never shrinks the Latin headline. The display's factor is its ceiling at the tier's widest column; type.fluid.display.<tier> holds its fluid size in vw, the largest at which the word fits at the tier's narrowest width, from the laptop up no more than its size at 1440 and no less than 1.08 times the hero where the word allows. tokens.css writes the display's size as clamp(hero plus 1px, its fluid size, its size times its factor) and matches the responsive rules on a right to left subtree too. The hero comes down on a phone until a display 1px above it fits the word at 320px, unless the phone order needs it higher. The display-fits check measures the word at each tier's narrowest and widest widths with the fluid size, and the order at each tier in each script.

## Why

Headline size is the strongest measured lever of character, and it grows continuously with how loud the brand is, never with its industry. A size in vw between two bounds scales with the screen the way the measured pages do, and fitting the page's own word, in its own script and its own column, lets a large headline stand where it fits instead of capping every page for the widest case.

## What it touches

character.expressiveness, LANDING_DISPLAY_PX, landing_display_px, PHONE_SHARE, PHONE_KNEE, PHONE_DISPLAY_PX, phone_display_for; typography.FIT_WORD, HEADLINE_COLUMNS, TIER_WIDTHS, REFERENCE_WIDTH, FLUID, Frame, tier_factors, fluid_vw, phone_px, phone_factors, fit_problems, fluid_size and the type.fluid, type.fit-word and type.fit-columns tokens; layout.landing_frame and responsive_css; export._lines; build_system words; guidance/type.md.

## Consequences

A landing page sets its headline in type.text.display at every width and never sizes it by hand. The report names the display size at 1440 and its most on a phone. An exporter for another platform applies the fluid size below its reference width. A nested right to left block reads its own factors.
