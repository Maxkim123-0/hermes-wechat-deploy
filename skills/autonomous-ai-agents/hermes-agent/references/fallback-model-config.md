# Fallback Model Configuration (Correct Format)

> Real-world fix: the fallback chain silently failed because config was wrong.
> This document records the working format so future sessions don't repeat it.

## Quick Fix

```bash
# REMOVE any fallback config under model: section (WRONG location)
python3 -c "
import yaml
with open('~/.hermes/profiles/<profile>/config.yaml') as f:
    config = yaml.safe_load(f)
config['model'].pop('fallback_providers', None)
config['model'].pop('fallback_model', None)
"

# SET at ROOT level as dict list (CORRECT)
hermes config set fallback_model '[{"provider":"openrouter","model":"deepseek/deepseek-v4-flash"},{"provider":"zai","model":"glm-5"}]'
```

## Correct Format

`fallback_model` must be at **root level** of config.yaml (no indentation), NOT under `model:`.

### Multi-provider chain (recommended):

```yaml
fallback_model:
  - provider: openrouter
    model: deepseek/deepseek-v4-flash
  - provider: zai
    model: glm-5
```

### Single provider:

```yaml
fallback_model:
  provider: openrouter
  model: deepseek/deepseek-v4-flash
```

## Wrong Format (silently ignored)

```yaml
# WRONG — under model: section, system ignores it
model:
  fallback_model: deepseek/deepseek-v4-flash  # string, not dict
  fallback_providers: [openrouter, zai]       # wrong location
```

Also wrong:
```yaml
# WRONG — string at root level
fallback_model: deepseek/deepseek-v4-flash
```

```yaml
# WRONG — empty list, fallback disabled
fallback_providers: []
```

## How the Code Reads It

From `hermes_cli/config.py` line 3090:
```python
fb = config.get("fallback_model")  # reads ROOT level only
```

From `run_agent.py` line 1760:
```python
if isinstance(fallback_model, list):
    # chain of dicts: each must have provider + model
elif isinstance(fallback_model, dict):
    # single dict with provider + model
else:
    self._fallback_chain = []  # string → empty, fallback disabled
```

## Verification

After setting, check:
```bash
grep -A5 '^fallback_model:' ~/.hermes/profiles/<profile>/config.yaml
```

Test fallback works:
```bash
# Break primary key temporarily
sed -i 's/^DEEPSEEK_API_KEY=.*/DEEPSEEK_API_KEY=broken_test/' .env

# Should show "switching to fallback: <model> via <provider>"
hermes chat -q "回复OK即可" --yolo 2>&1 | grep 'switching to fallback'

# RESTORE the key immediately
sed -i 's/^DEEPSEEK_API_KEY=.*/DEEPSEEK_API_KEY=<original_value>/' .env
```

⚠️ Always backup the key before testing. After restoring, verify the key is intact (not a placeholder like `***`).

## Pitfalls

1. **`hermes config set model.fallback_model`** puts config under `model:`, which is WRONG. Use manual config editing instead.
2. **`hermes config set model.fallback_providers`** also goes under `model:` — same problem.
3. **After changing .env keys, restart the gateway** for env changes to take effect.
4. **String fallback_model is silently treated as empty fallback chain** — no error, just doesn't work.
