# Habit Design (conditional reference, v3)

This reference is invoked only when the surface being reviewed or designed is a retention surface — onboarding, notifications, daily-use product, streaks, badges, loyalty mechanics, or any surface whose job is to bring the user back tomorrow.

Full content lands in v3. This stub captures the framework so commands that route through it have something concrete to apply now.

---

## The Hook Model

Four phases. The product designs a loop that runs through them.

### Trigger

The cue that starts the loop. External triggers come from the world: a notification, an email, a sign on a shelf. Internal triggers come from the user: an emotion, a routine, a context.

What to design: the moment that brings the user back. Identify the internal trigger first; build the external trigger to bridge to it.

What to avoid: a trigger that pulls the user away from what they were doing without a clear payoff. Notifications without earned attention are an unhealthy pattern.

How to test: count the share of returning sessions that begin from an internal trigger versus an external one. As the product matures, the internal share rises.

### Action

The simplest behavior the user takes in anticipation of a reward. The action is the muscle memory of the product — open the app, tap the icon, scan the card.

What to design: minimum friction. The action should be possible in one motion. If the user must think about it, the loop has slipped.

What to avoid: an action that requires authentication every time, that puts a decision tree before the reward, or that varies across sessions in a way that breaks muscle memory.

How to test: time-to-action from trigger. If it exceeds three seconds for a daily-use product, the friction is too high.

### Variable Reward

The payoff. The reward is variable, not fixed — the brain attends to variability. Three classes of variable reward operate inside most products.

- Rewards of the tribe — social validation, recognition, status, the sense of belonging. The reward is other people seeing the user's behavior.
- Rewards of the hunt — material, informational, transactional. The reward is acquisition: points, content, items, money.
- Rewards of the self — mastery, competence, completion. The reward is the user's own sense of progress.

What to design: a reward that the user genuinely wants and that fits the product's purpose. The reward is variable in size, timing, or kind, but always within the bounds of what the user expects the product to deliver.

What to avoid: a reward that feels random in a way that mocks the user's effort. Variability earns attention; arbitrariness erodes trust. The reward is variable; the rules are not.

How to test: ask users what they got. If they cannot name the reward, the reward is too thin. If they describe it as "lucky" rather than "earned," the variability has gone too far.

### Investment

What the user puts into the product that makes future loops more valuable. Stored data, social connections, customized preferences, accumulated content, reputation, history.

What to design: a small ask after the reward is delivered, when the user is most willing to invest. The investment compounds — every visit makes the product more valuable to that user, which strengthens the next trigger.

What to avoid: an investment that benefits the product but not the user. Capturing data the user cannot see or use is extractive. The investment is a loaded next-visit, not a tax.

How to test: count the share of returning users whose stored state changed materially in the last session. If most users return to a product that looks identical to how they left it, investment is missing.

---

## Internal vs External Triggers

External triggers are the product's job at the start. Internal triggers are the goal.

External triggers are noisy and expensive: push notifications, ads, emails, paid acquisition. They work, but they decay; the user habituates.

Internal triggers are quiet and durable: a feeling that the user has learned to resolve with the product. Boredom resolves with the social feed. Loneliness resolves with the messaging app. Curiosity resolves with the search box.

A retention surface earns its name when the internal triggers carry most of the return traffic. A product that depends on external triggers forever has not built habit; it has rented attention.

---

## Variable Rewards: Three Classes

The three classes operate in different products with different intensities. A well-designed retention surface picks the class that fits the product's purpose and the user's context.

- Tribe — works for social, community, status surfaces. Strong but easy to overplay; manufactured social validation reads as hollow.
- Hunt — works for commerce, content discovery, transactional products. Strong and durable; the user comes for the thing and learns to come for the search.
- Self — works for productivity, learning, fitness, finance, loyalty. Quieter but the most defensible; the user becomes invested in their own progress, not in the product's content.

A loyalty product like Dot operates primarily on rewards of the self (tier progress, badge accumulation, the user's own history) and secondarily on rewards of the hunt (redemption, points, real economic value). Tribe rewards are rare in loyalty and risky to introduce — they pull the product toward social mechanics that distract from the loyalty surface's job.

---

## Investment That Builds Future Value

Investment takes five shapes. A retention surface uses at least one; mature products use three or more.

- Stored data — the user's history, accumulated points, transaction record, preferences. The data makes the next visit more useful.
- Social connections — the user's friends, follows, contacts inside the product. Social graph compounds value.
- Customized preferences — themes, settings, defaults, the user's configuration. The product feels like it knows the user.
- Content — what the user has created, saved, shared, annotated. Content is the heaviest investment; it is hard to leave a product that holds the user's work.
- Reputation — the user's standing inside the product: tier, badges, rating, history. Reputation is portable inside the product but not outside, which keeps it sticky.

Each shape of investment costs the user something at the moment of placement. The product's job is to make the deposit feel light at the time and heavy in retrospect.

---

## Anti-Pattern: Dark-Pattern Habit Design

Habit design can be used to build healthy habits or to manufacture forced engagement. The plugin's discipline is the former; the latter is rejected as a ship-block.

Forbidden patterns:
- Streaks that punish missed days with shame, public visibility, or material loss out of proportion to the lapse.
- Variable rewards that are pure randomness with no relationship to user effort — slot machines.
- Notifications that lie about urgency, novelty, or social activity to drive opens.
- Friction added to disengagement (hard-to-find unsubscribe, "are you sure?" loops, hidden settings) that is absent from engagement.
- Engagement metrics that are optimized at the user's expense — time-on-platform without regard for whether the time was useful.

A healthy retention surface is one the user would design for themselves if they understood the loop. If the surface only works because the user does not understand it, the surface is exploitative.

---

## v3 Expansion

The full v3 reference will add, for each phase of the Hook Model:

- A library of concrete patterns drawn from product surfaces.
- An audit checklist for retention surfaces, structured to match the polaris severity scale.
- Anti-pattern callouts specific to MENA-market loyalty mechanics — what reads as motivating in one cultural context and exploitative in another.
- A retention-health scorecard that grades a surface across the four phases and the three reward classes.
- A decision tree for when habit-design language is appropriate to apply to a surface, versus when the surface is not a retention surface and habit-design is the wrong lens.

Until v3 lands, this stub is the operating reference for any command that routes through habit-design.
