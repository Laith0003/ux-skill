#!/usr/bin/env bash
#
# state.sh — plugin state persistence for the ux plugin
#
# Provides read/write/list operations for `last-*.json` reports stored under
# the .ux/ directory at the root of the target project. Each command in the
# plugin (e.g. /ux-audit, /ux-critique, /ux-a11y) writes its most recent
# report to .ux/last-<command-name>.json so subsequent commands can chain.
#
# Usage:
#   ux_state_init                              create .ux/ and .ux/.gitignore
#   ux_state_write <command> <json-content>    write .ux/last-<command>.json
#   ux_state_read  <command>                   print .ux/last-<command>.json
#   ux_state_latest                            print path of newest report
#   ux_state_summary                           list reports with age + counts
#   ux_state_clear                             delete all .ux/last-*.json
#
# macOS (BSD utils) and Linux (GNU utils) both supported. Avoids GNU-only
# flags. Uses `jq` when available; falls back gracefully when not.

set -euo pipefail

# --- internal helpers --------------------------------------------------------

# Resolve the .ux directory relative to the current working directory.
# Plugin state lives under the target project, not the plugin itself.
_ux_state_dir() {
    printf '%s\n' "$(pwd)/.ux"
}

# Check whether jq is available. Returns 0 if present, 1 if not.
_ux_have_jq() {
    command -v jq >/dev/null 2>&1
}

# Print to stderr.
_ux_err() {
    printf '%s\n' "$@" >&2
}

# Cross-platform "seconds since epoch" for a file's mtime. BSD `stat -f %m`
# vs GNU `stat -c %Y`. Tries BSD first; falls back to GNU.
_ux_file_mtime() {
    local f="$1"
    if stat -f %m "$f" >/dev/null 2>&1; then
        stat -f %m "$f"
    else
        stat -c %Y "$f"
    fi
}

# Format an age in seconds as a short human string ("2m", "1h", "3d").
_ux_format_age() {
    local sec="$1"
    if [ "$sec" -lt 60 ]; then
        printf '%ds\n' "$sec"
    elif [ "$sec" -lt 3600 ]; then
        printf '%dm\n' "$((sec / 60))"
    elif [ "$sec" -lt 86400 ]; then
        printf '%dh\n' "$((sec / 3600))"
    else
        printf '%dd\n' "$((sec / 86400))"
    fi
}

# --- public api --------------------------------------------------------------

# Create .ux/ if missing. Write .ux/.gitignore so the entire directory is
# ignored by git, except the .gitignore file itself (which gets committed
# so the convention travels with the repo).
ux_state_init() {
    local dir
    dir="$(_ux_state_dir)"
    mkdir -p "$dir"
    local gi="$dir/.gitignore"
    if [ ! -f "$gi" ]; then
        printf '*\n!.gitignore\n' > "$gi"
    fi
    printf '%s\n' "$dir"
}

# Atomically write a report. Takes a command name and a JSON payload string.
# Writes to a temp file in the same directory, then renames into place so
# readers never see a partial file.
ux_state_write() {
    if [ "$#" -lt 2 ]; then
        _ux_err "ux_state_write: requires <command-name> <json-content>"
        return 2
    fi
    local cmd="$1"
    local content="$2"
    local dir
    dir="$(ux_state_init)"
    local target="$dir/last-$cmd.json"
    local tmp
    tmp="$(mktemp "$dir/.last-$cmd.XXXXXX")"
    printf '%s' "$content" > "$tmp"
    mv "$tmp" "$target"
    printf '%s\n' "$target"
}

# Read a report by command name. Prints the JSON to stdout. Returns 0 if the
# file exists and was read; 1 if missing.
ux_state_read() {
    if [ "$#" -lt 1 ]; then
        _ux_err "ux_state_read: requires <command-name>"
        return 2
    fi
    local cmd="$1"
    local dir
    dir="$(_ux_state_dir)"
    local target="$dir/last-$cmd.json"
    if [ ! -f "$target" ]; then
        return 1
    fi
    cat "$target"
}

# Print the path of the most recently-modified .ux/last-*.json file. Returns
# 1 if no reports exist.
ux_state_latest() {
    local dir
    dir="$(_ux_state_dir)"
    if [ ! -d "$dir" ]; then
        return 1
    fi
    local newest=""
    local newest_mtime=0
    local f mtime
    # Loop avoids ls/find sort flag incompatibility across BSD/GNU.
    for f in "$dir"/last-*.json; do
        [ -f "$f" ] || continue
        mtime="$(_ux_file_mtime "$f")"
        if [ "$mtime" -gt "$newest_mtime" ]; then
            newest_mtime="$mtime"
            newest="$f"
        fi
    done
    if [ -z "$newest" ]; then
        return 1
    fi
    printf '%s\n' "$newest"
}

# List every report with its command name, age, and finding count. If jq is
# available, the finding count comes from the JSON's `findings` array length.
# If not, the count is reported as "?" with a one-line warning printed once.
ux_state_summary() {
    local dir
    dir="$(_ux_state_dir)"
    if [ ! -d "$dir" ]; then
        _ux_err "no .ux/ directory; nothing to summarize"
        return 1
    fi
    local have_jq=0
    if _ux_have_jq; then
        have_jq=1
    else
        _ux_err "note: jq not found; finding counts shown as '?'"
    fi
    local now
    now="$(date +%s)"
    local f base cmd mtime age count
    local any=0
    printf '%-24s %-8s %s\n' "command" "age" "findings"
    printf '%-24s %-8s %s\n' "-------" "---" "--------"
    for f in "$dir"/last-*.json; do
        [ -f "$f" ] || continue
        any=1
        base="$(basename "$f")"
        cmd="${base#last-}"
        cmd="${cmd%.json}"
        mtime="$(_ux_file_mtime "$f")"
        age="$(_ux_format_age "$((now - mtime))")"
        if [ "$have_jq" -eq 1 ]; then
            count="$(jq -r '(.findings // []) | length' "$f" 2>/dev/null || printf '?')"
        else
            count="?"
        fi
        printf '%-24s %-8s %s\n' "$cmd" "$age" "$count"
    done
    if [ "$any" -eq 0 ]; then
        _ux_err "no reports found in $dir"
        return 1
    fi
}

# Delete all .ux/last-*.json reports. Prompts for confirmation unless the
# environment variable UX_STATE_CLEAR_FORCE is set to "1" (useful for scripts).
ux_state_clear() {
    local dir
    dir="$(_ux_state_dir)"
    if [ ! -d "$dir" ]; then
        _ux_err "no .ux/ directory; nothing to clear"
        return 0
    fi
    local count=0
    local f
    for f in "$dir"/last-*.json; do
        [ -f "$f" ] && count=$((count + 1))
    done
    if [ "$count" -eq 0 ]; then
        _ux_err "no reports to clear"
        return 0
    fi
    if [ "${UX_STATE_CLEAR_FORCE:-0}" != "1" ]; then
        printf 'Delete %d report(s) from %s? [y/N] ' "$count" "$dir" >&2
        local reply
        read -r reply
        case "$reply" in
            y|Y|yes|YES) ;;
            *) _ux_err "aborted"; return 1 ;;
        esac
    fi
    rm -f "$dir"/last-*.json
    _ux_err "cleared $count report(s)"
}

# --- usage -------------------------------------------------------------------

_ux_state_usage() {
    cat <<'USAGE'
state.sh — ux plugin state helpers

Source this file from a shell or another script:
    . path/to/bin/state.sh

Then call:
    ux_state_init                              create .ux/ and .ux/.gitignore
    ux_state_write <command> <json-content>    write .ux/last-<command>.json
    ux_state_read  <command>                   print .ux/last-<command>.json
    ux_state_latest                            print path of newest report
    ux_state_summary                           list reports with age + counts
    ux_state_clear                             delete all .ux/last-*.json

Environment:
    UX_STATE_CLEAR_FORCE=1   skip confirmation prompt on ux_state_clear

Requires: bash. Optional: jq (graceful fallback if missing).
USAGE
}

# When run directly (not sourced), print usage. When sourced, do nothing —
# the caller will invoke the functions.
if [ "${BASH_SOURCE[0]:-$0}" = "${0}" ]; then
    if [ "$#" -eq 0 ] || [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
        _ux_state_usage
        exit 0
    fi
    # Dispatch: allow `state.sh <function> [args...]` for one-off calls.
    fn="ux_state_$1"
    shift
    if declare -F "$fn" >/dev/null 2>&1; then
        "$fn" "$@"
    else
        _ux_err "unknown subcommand: $1"
        _ux_state_usage
        exit 2
    fi
fi
