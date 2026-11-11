# navigation
Input rows: 136. Output rows: 47.

Confidence note: scored with the sources.md weight table; rule 5 then lifts any lesson that three or more independent books support to high (two books by the same author count once).

## Orientation

- **Show the site, the section and the current page on every screen.** Carry the site identity everywhere, give each page a prominent name that repeats the wording of the link that led there, and mark the active menu item with at least two visual cues (for example color plus weight), because many visitors arrive mid-site from search or a shared link. Confidence: high. Sources: B77 p.86-89; B93 p.202; B18 p.112; B86 p.194-195; B02 p.250-251; B46 p.373-383; B11 p.89-90; B35 p.360; B85 p.126, 176; B78 p.55-56; B59 p.14
- **Keep global navigation in one place, with the same labels and behavior, on every page.** People learn the navigation once and then rely on it; a missing home link or a shifting menu leaves them unable to orient, and toolbars should not reflow when items are disabled. Confidence: high. Sources: B77 p.77-78; B58 p.100, 115-116; B18 p.110-112; B91 p.197-198, 266; B46 p.373-383; B26 p.317-318, 488; B78 p.55
- **Let every screen tell people their location, its contents and their next options.** Provide global navigation to restart from, local aids (anchors, back to top, sort on results), contextual related links and a supplemental index; run this as a check on every screen flow, since it fails late even in polished prototypes. Confidence: high. Sources: B02 p.250-251; B46 p.373-383; B11 p.89-90; B85 p.126, 176; B35 p.360
- **Stress-test navigation from random interior pages.** Land on a deep page without passing the home page and confirm you can name the site, the section and the parent, and predict where each link goes. Confidence: medium. Sources: B93 p.203; B85 p.126, 176
- **Give every dead-end or limited screen an escape route.** Wizards, modals, deep-linked out-of-context pages and 404 pages each need a clear way back to familiar ground, typically a logo that returns home; never ship a page without navigation. Confidence: medium. Sources: B86 p.171-173; B46 p.373-383

## Structure, breadth and depth

- **Prefer broad, shallow hierarchies over deep trees.** Two or three levels outperform deep nesting; novice and intermediate users struggle once content sits three levels down; keep critical content within two to three steps of the home page and on mobile keep the tree to about three levels. Confidence: high. Sources: B46 p.167, 347-349, 376; B26 p.323-324, 604-605; B86 p.134-135; B35 p.240-241
- **Size menu levels by grouping, not by a fixed small cap.** Ungrouped levels work at about 4 to 8 choices; with labeled groups, 18 to 24 items (at most about 10 per group, up to about 64 in total) remain fast; real global navigation bars range from 5 to 9 items and usually stay under 10. Confidence: high. Sources: B46 p.347-349, 352-353, 394; B93 p.169, 183; B35 p.240
- **Judge a path by how hard each click is, not by the click count.** Fixed click limits have no support; extra steps cost little when every step is an obvious, unambiguous choice that visibly moves toward the goal, and roughly three effortless clicks cost the same as one that needs thought. Confidence: high. Sources: B77 p.54; B87 p.46-50; B06 p.248
- **Make discoverability follow frequency of use.** Actions people take often must be visible on screen; rare actions may sit behind search or a menu, the spot where a trigger is hardest to notice; controls nobody can find do not exist for users. Confidence: high. Sources: B14 p.45, 48-49; B21 p.189; B44 p.119
- **Let the most common tasks finish without leaving the page.** Aim for about 80 percent of common use cases to complete on one page without context switches, and give the top tasks (hours, directions, account) direct shortcut links. Confidence: medium. Sources: B86 p.134-135, 155; B44 p.119
- **Limit the number of places a person must go.** Favor a single primary window split into two or three views; a web page carrying over two separate nav zones beside its content starts to feel crowded, and tablets usually hold two panes; every extra dialog needs a reason. Confidence: low. Sources: B26 p.316, 444, 474-476
- **Remove choices instead of reshuffling them.** Decision time grows with the number of options (Hick's law), so present the fewest, most consequential choices first and refine afterward, as filters follow results. Confidence: low. Sources: B57 p.92-93; B33 p.61-62

## Menus

- **Order menu items by natural sequence first, then frequency, then alphabet.** People fixate on the first three positions; alphabetical order searched about four times faster than random order on an 18-item list; keep destructive items away from frequent ones. Confidence: medium. Sources: B46 p.350-352
- **Do not reorder menus adaptively.** Menus that reshuffle by usage slowed people down; consider a split menu only when a small set takes 31 to 89 percent of selections, and a folded menu only above 90 percent. Confidence: medium. Sources: B46 p.354-357
- **Prefer wide mega menus to nested flyouts when the option set is large.** Flyouts that open level by level require exact pointer steering and invite overshooting, while a single wide panel shows many options in one view and proved easier in tests. Confidence: medium. Sources: B02 p.236-239
- **Close a toggled menu with the control that opened it.** Whatever icon or gesture reveals the panel should also dismiss it, the page behind should stay partly visible, and tapping outside should dismiss it. Confidence: low. Sources: B24 p.61

## Visible versus hidden navigation

- **Keep primary navigation visible instead of behind a hamburger icon.** Hidden navigation cuts discoverability roughly in half, makes its options look less important and costs extra taps; large-scale tests found a tab bar beating a side drawer; avoid the hamburger on desktop entirely. Confidence: high. Sources: B02 p.534-535; B07 p.198-201; B85 p.42-43; B24 p.37; B26 p.604; B59 p.11
- **On mobile, put 3 to 5 equal top-level destinations in a persistent bottom tab bar.** Cap the bar at five items (use More as the fifth if needed), use tabs only for navigation and keep screen actions in a toolbar, and make the selected tab unmistakable even next to a prominent action button. Confidence: high. Sources: B24 p.25, 38-39, 44; B93 p.214; B07 p.198-201
- **When a menu must be hidden, label it and place it in thumb reach.** The word Menu outperformed the bare icon for some users; teach a drawer with a single brief open-and-close hint on first launch rather than auto-opening it, and never anchor a drawer to the bottom screen edge where the OS gesture lives. Confidence: high. Sources: B26 p.604; B07 p.198-201; B24 p.49-52
- **Label icon-only tabs and sidebars.** Unlabeled icons force people to tap each one to learn what it holds; bare icons are acceptable only for a few icons used habitually by experts. Confidence: medium. Sources: B24 p.43-44; B07 p.194-195
- **Do not use scrolling tabs or flat icon grids for primary navigation.** Non-scrolling tabs fit roughly three top-level views at most; scrolling tabs belong inside a module; a springboard grid gives every option equal weight, so vary size or group when some destinations matter more. Confidence: low. Sources: B24 p.25-28, 40-41

## Placement conventions

- **Place persistent navigation where people expect it.** Site ID and home link upper left, search and account tools (profile, settings, help, cart, sign out) upper right, global navigation along the top or left in an inverted L, never on the right; persistent bars hold only four or five utilities and the rest go to the footer. Confidence: high. Sources: B86 p.152, 185-186; B77 p.77-81; B46 p.790; B93 p.214
- **Strip navigation down during checkout and rigid multi-step entry.** Reduce the header to site ID, home and essential utilities so people finish or explicitly cancel, but keep a visible exit. Confidence: medium. Sources: B77 p.81; B38 p.75
- **Choose hub-and-spoke or global navigation deliberately.** A hub model routes through a central page with back or breadcrumb links; a global model shows persistent links on nearly every page. Confidence: low. Sources: B38 p.74
- **Keep navigation visually quieter than the content.** Mute its size and color so content leads, and design it after the content is known. Confidence: low. Sources: B78 p.56-57

## Labels and links

- **Write link text that names the destination, and title the destination to match.** Never use click here or bare icons; link the subject itself so the link reads correctly out of context, and keep the page title identical to the link wording. Confidence: high. Sources: B07 p.194-195; B18 p.110-112; B77 p.86-87; B46 p.373-383
- **Make links unmistakable.** Underline links or otherwise reserve a link style, show visited links differently from new ones, never dress ordinary text as a link, and mark links that exit the site or move within the page; one test saw 97 percent versus 76 percent link recognition between two home pages. Confidence: high. Sources: B46 p.378, 387-389; B77 p.72, 201; B59 p.14; B58 p.112
- **Use plain, conventional labels, never slogans or catch-all buckets.** Labels such as Support or Budgets orient people; clever words force guessing, and catch-all labels such as Miscellaneous, Resources or More Info turn into neglected piles; check competitors for the industry-standard term. Confidence: high. Sources: B55 p.105, 139; B33 p.58-59; B23 p.470, 472
- **Keep information scent getting stronger with every click.** People follow whichever option looks most likely to move them forward and keep going only while they sense they are getting nearer, so each label must predict what sits behind it. Confidence: high. Sources: B11 p.99; B33 p.58-59; B77 p.54
- **Put the distinguishing word first in links and menu items.** Screen reader users often hear only the opening words, and sighted scanners read the left edge. Confidence: low. Sources: B39 p.106
- **Make sibling categories mutually exclusive.** If people think an item could belong to two sections, the labels overlap and need rewording. Confidence: low. Sources: B23 p.469
- **List your own resources before external ones and label exits.** Order links by what visitors came for, put links to other organizations last, and say where they go. Confidence: low. Sources: B58 p.112
- **In link-heavy interfaces, style secondary links quietly.** Use weight or a darker color for ancillary links and reveal underline or color on hover, while primary in-text links stay obvious. Confidence: low. Sources: B47 p.126-127
- **Leave the choice of new windows to the user.** Opening a separate window resets its history, which breaks the Back button; let people open tabs themselves. Confidence: low. Sources: B18 p.99

## Multiple routes and supplemental navigation

- **Provide at least two independent ways to reach every page.** Back the main hierarchy with search, a site map or an A to Z index, because any taxonomy fails some people and tasks, and many users with disabilities prefer search or a site map (WCAG 2.4.5 requires multiple ways). A small site of two or three levels may skip the site map; keep redundant routes few enough not to overload. Confidence: high. Sources: B93 p.215-218; B18 p.113, 115; B91 p.264; B26 p.323-324; B40 p.30
- **Make a skip-to-content link the first tab stop.** It must target a valid ID and become visible on focus so keyboard and screen reader users can bypass repeated headers (WCAG 2.4.1). Confidence: high. Sources: B91 p.82, 117, 244; B18 p.113
- **Give critical contextual links their own visible region.** Scanning readers overlook links buried in prose, so important related links belong in a predictable zone or treatment, applied with restraint. Confidence: low. Sources: B93 p.211-212

## Breadcrumbs, steps and paging

- **Place breadcrumbs at the top, built from the hierarchy, not click history.** Use them for two or more levels; each crumb is a linked page title, separators are arrows or slashes, and the last item is the current page, visually distinct and not a link; hierarchical trails orient deep-link arrivals where history trails cannot. Confidence: high. Sources: B77 p.91; B86 p.194-195; B04 p.227-231; B02 p.250-251
- **Show every step in a multi-step process with current and completed states.** Keep the step map on one line with numbers and short titles, let people jump back to finished steps, and disable steps not yet reachable. Confidence: medium. Sources: B86 p.189-190, 193; B11 p.89-90
- **In faceted results, label each crumb with its attribute and let people change its value in place.** Removing a filter only to add a new value is a wasted round trip; keep the keywords editable at the end of the trail. Confidence: low. Sources: B04 p.233-237, 245-247
- **Adapt pagination to the page count.** Link every page for one to five pages and for long sets show only the first, previous, current, next and final page links; typical page sizes are about 10 search results or 20 products. Confidence: low. Sources: B07 p.121
- **Avoid infinite scroll when people need to find, compare, bookmark or reach the footer.** It suits casual browsing only; otherwise use pagination or a load more button. Confidence: low. Sources: B07 p.124-126

## Platform and app specifics

- **In 3D and XR spaces, pick the movement method that fits the journey.** Jump-to-target movement suits places people already know and steering for exploration, vary speed with slow-in near targets, decouple direction from gaze, keep a live you-are-here map without surprise rotation, and space signs so they are read in a glance of under about three seconds. Confidence: medium. Sources: B83 p.477-480, 507-508, 527-529, 543-551; B85 p.186
- **Keep the Back control purely navigational and in its standard spot.** Place it top-left only when there is somewhere to go, remove it when a screen already offers Save and Cancel, and keep well-known buttons in place across releases. Confidence: low. Sources: B52 p.210-213
- **Open notifications onto the item they refer to.** Arriving at the home screen or some other item reads as a bug; retire outdated alerts and reset badge counts after people view them. Confidence: low. Sources: B52 p.183, 242-244
- **Keep the task context visible deep inside a flow.** Restate what the user is doing (the active query or mode) on results screens so they can refine without remembering, and pair each suggested fix with a direct link to where it is made. Confidence: low. Sources: B20 p.740, 773, 789-790
- **Match navigation style to cultural task orientation.** Sequential, step-oriented audiences lean on structured flows, breadcrumbs and site maps; audiences who juggle tasks prefer all inputs on one page and use search. Confidence: low. Sources: B08 p.88, 135
