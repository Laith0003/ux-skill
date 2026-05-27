# Example briefs

Pass any of these to `ux recommend --brief-file=...` to see the engine in action.

```bash
# From the repo root
python3 -m engine.cli.main recommend --brief-file=examples/briefs/fintech-neobank-mena.json
python3 -m engine.cli.main recommend --brief-file=examples/briefs/dev-tools-dashboard.json
python3 -m engine.cli.main recommend --brief-file=examples/briefs/luxury-fashion-ecom.json
python3 -m engine.cli.main recommend --brief-file=examples/briefs/health-telehealth.json
```

Or as a pip-installed user:

```bash
ux recommend --brief-file=examples/briefs/fintech-neobank-mena.json
```

Each brief is a 9-field JSON document the recommender reads as a `Brief` dataclass. The shape:

```jsonc
{
  "project_type": "landing | dashboard | marketing-site | docs | mobile-app | email | ...",
  "industry": "id-from-industries.json",     // optional — engine infers if omitted
  "audience": ["who specifically"],
  "tone": ["warm", "editorial", "precise"],
  "must_have": ["dark-mode", "rtl-arabic"],
  "forbidden": ["brutalism", "purple-gradients"],
  "stack": "id-from-tech-stacks.json",
  "region": "mena | us | eu | apac | global"
}
```

Use the interactive `ux discover` flow to generate one of these for your own project — it asks 10 questions and saves to `.ux/last-discovery.json`.
