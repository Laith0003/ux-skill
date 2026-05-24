#!/usr/bin/env bash
#
# ux-lint.sh — deterministic linter for the ux plugin
#
# Scans source files for the AI-fingerprint patterns listed in
# references/foundations/anti-patterns.md and reports violations grouped by
# severity. No LLM, no network, no API key — pure regex via perl PCRE
# (preferred) or grep ERE (fallback).
#
# Exit codes:
#   0  no findings, or only findings below --fail-on threshold
#   1  one or more findings at or above --fail-on threshold (default: high)
#   2  rules file missing, unreadable, or zero rules parsed
#   3  invalid CLI usage
#
# Usage: ux-lint.sh [options] [path ...]
#   See `ux-lint.sh --help` for full options.
#
# Portability: POSIX-friendly bash. Tested under macOS BSD utilities and GNU
# coreutils. Patterns in the rules file may use PCRE features (lookaheads,
# non-capturing groups). When `perl` is present the script uses
# `perl -nE` for matching; otherwise it falls back to `grep -E` with a
# best-effort syntax shim that strips PCRE-only constructs.

set -uo pipefail

# --- discovery ---------------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
DEFAULT_RULES_FILE="${PLUGIN_ROOT}/references/foundations/anti-patterns.md"

# --- defaults ----------------------------------------------------------------

RULES_FILE="${UX_LINT_RULES:-${DEFAULT_RULES_FILE}}"
FAIL_ON="high"
MIN_SEVERITY=""
INCLUDE_GLOBS=()
EXCLUDE_GLOBS=(
    "*/node_modules/*"
    "*/.git/*"
    "*/dist/*"
    "*/build/*"
    "*/.next/*"
    "*/vendor/*"
    "*/public/build/*"
    "*/.ux/*"
)
CI_MODE=0
SHOW_RULES=0
TARGET_PATHS=()
DISABLED_RULES=""

# Default extension set when a rule does not declare its own. Targets UI
# source files where the fingerprints actually appear.
DEFAULT_EXTENSIONS=".html,.htm,.jsx,.tsx,.js,.ts,.vue,.svelte,.astro,.blade.php,.css,.scss,.sass,.md"

# --- helpers -----------------------------------------------------------------

usage() {
    cat <<'__UX_LINT_USAGE__'
ux-lint.sh — deterministic regex linter for the ux plugin

Scans files for AI-fingerprint patterns and reports findings grouped by
severity. No LLM, no network. Reads rules from
references/foundations/anti-patterns.md (override with --rules).

Usage:
    ux-lint.sh [options] [path ...]

If no path is given, the current working directory is scanned recursively.

Options:
    --rules <file>          Use a non-default rules file
    --include <glob>        Only scan files matching this glob (repeatable)
    --exclude <glob>        Skip files matching this glob (repeatable)
    --severity <level>      Only report findings at or above this severity.
                            One of: critical, high, medium, cosmetic
    --fail-on <level>       Exit non-zero only if a finding at or above this
                            severity is found. Default: high
    --disable <id[,id...]>  Skip these rule IDs entirely
    --ci                    Machine-readable output on stdout, summary on
                            stderr. Designed for CI logs and grep pipelines.
    --list-rules            Print every rule with its severity and exit
    -h, --help              Print this message and exit

Exit codes:
    0  no findings at or above --fail-on threshold
    1  one or more findings at or above --fail-on threshold
    2  rules file missing or unreadable
    3  invalid CLI usage

Examples:
    ux-lint.sh                              scan current directory
    ux-lint.sh src/                         scan one subdirectory
    ux-lint.sh --severity high              hide medium/cosmetic findings
    ux-lint.sh --fail-on critical           only fail CI on Critical findings
    ux-lint.sh --include '*.tsx'            scope to a single extension
    ux-lint.sh --disable 18,19              skip rules 18 and 19
    ux-lint.sh --ci                         machine-readable for pipelines
__UX_LINT_USAGE__
}

err() {
    printf '%s\n' "$@" >&2
}

# Convert a severity token to a sortable integer. Lower number = higher
# priority. Used to compare a finding's severity against --fail-on and
# --severity thresholds.
severity_rank() {
    case "${1:-}" in
        Critical|critical) printf '1\n' ;;
        High|high)         printf '2\n' ;;
        Medium|medium)     printf '3\n' ;;
        Cosmetic|cosmetic) printf '4\n' ;;
        *)                 printf '99\n' ;;
    esac
}

# Validate a severity name. Returns 0 if valid, 1 if not.
is_valid_severity() {
    case "${1:-}" in
        critical|high|medium|cosmetic) return 0 ;;
        *) return 1 ;;
    esac
}

# Detect whether perl with PCRE support is available. We prefer perl because
# the rules file uses PCRE features (lookaheads, non-capturing groups) that
# BSD grep does not support.
HAVE_PERL=0
if command -v perl >/dev/null 2>&1; then
    HAVE_PERL=1
fi

# --- CLI parsing -------------------------------------------------------------

parse_args() {
    while [ "$#" -gt 0 ]; do
        case "$1" in
            --rules)
                [ "$#" -ge 2 ] || { err "missing value for --rules"; exit 3; }
                RULES_FILE="$2"
                shift 2
                ;;
            --include)
                [ "$#" -ge 2 ] || { err "missing value for --include"; exit 3; }
                INCLUDE_GLOBS+=("$2")
                shift 2
                ;;
            --exclude)
                [ "$#" -ge 2 ] || { err "missing value for --exclude"; exit 3; }
                EXCLUDE_GLOBS+=("$2")
                shift 2
                ;;
            --severity)
                [ "$#" -ge 2 ] || { err "missing value for --severity"; exit 3; }
                if ! is_valid_severity "$2"; then
                    err "invalid severity: $2"
                    err "valid values: critical, high, medium, cosmetic"
                    exit 3
                fi
                MIN_SEVERITY="$2"
                shift 2
                ;;
            --fail-on)
                [ "$#" -ge 2 ] || { err "missing value for --fail-on"; exit 3; }
                if ! is_valid_severity "$2"; then
                    err "invalid severity: $2"
                    err "valid values: critical, high, medium, cosmetic"
                    exit 3
                fi
                FAIL_ON="$2"
                shift 2
                ;;
            --disable)
                [ "$#" -ge 2 ] || { err "missing value for --disable"; exit 3; }
                DISABLED_RULES="$2"
                shift 2
                ;;
            --ci)
                CI_MODE=1
                shift
                ;;
            --list-rules)
                SHOW_RULES=1
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            --)
                shift
                while [ "$#" -gt 0 ]; do
                    TARGET_PATHS+=("$1")
                    shift
                done
                ;;
            -*)
                err "unknown option: $1"
                err "run 'ux-lint.sh --help' for usage"
                exit 3
                ;;
            *)
                TARGET_PATHS+=("$1")
                shift
                ;;
        esac
    done

    if [ "${#TARGET_PATHS[@]}" -eq 0 ]; then
        TARGET_PATHS=(".")
    fi
}

# --- rules parser ------------------------------------------------------------
#
# The rules file is a markdown document. Each rule starts with `#### N. Title`
# and contains:
#   - one or more ```regex fenced blocks holding patterns
#   - **Severity**: Critical|High|Medium|Cosmetic
#   - **Mode**: brand-only|product-only|both
#   - **Better alternative**: <text>
#
# We emit one TSV record per regex block (so a rule with two patterns becomes
# two scan rows that share id/title/severity/better):
#   rule_id<TAB>title<TAB>severity<TAB>mode<TAB>extensions<TAB>pattern<TAB>better

RULES_TMP=""

cleanup_tmp() {
    if [ -n "${RULES_TMP:-}" ] && [ -f "${RULES_TMP:-}" ]; then
        rm -f "${RULES_TMP}"
    fi
}

# Parse the rules file once at startup. Writes a flat TSV cache to a temp file
# so per-file scans don't re-parse on every loop.
parse_rules() {
    if [ ! -f "${RULES_FILE}" ]; then
        err "rules file not found: ${RULES_FILE}"
        err "set UX_LINT_RULES or pass --rules to override"
        exit 2
    fi
    if [ ! -r "${RULES_FILE}" ]; then
        err "rules file not readable: ${RULES_FILE}"
        exit 2
    fi

    RULES_TMP="$(mktemp -t ux-lint-rules.XXXXXX)"

    # State machine:
    #   in_regex = 0/1 — are we currently inside a ```regex block
    # Each rule's patterns are accumulated into an array (pat_count, pats[])
    # and flushed at the next rule header or at EOF — by then Severity, Mode,
    # and the Better alternative line have all been read.
    awk -v out="${RULES_TMP}" -v default_exts="${DEFAULT_EXTENSIONS}" '
        function flush_rule(    i, ext, p) {
            if (id == "" || pat_count == 0 || sev == "") {
                return
            }
            ext = (exts == "" ? default_exts : exts)
            for (i = 1; i <= pat_count; i++) {
                p = pats[i]
                gsub(/^[[:space:]]+|[[:space:]]+$/, "", p)
                if (p == "") continue
                printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\n", \
                    id, title, sev, mode, ext, p, better >> out
            }
        }
        function reset_rule() {
            id = ""; title = ""; sev = ""; mode = ""; exts = ""; better = ""
            pat_count = 0
            delete pats
            cur_pat = ""
            in_regex = 0
        }
        BEGIN {
            reset_rule()
        }
        /^#### [0-9]+\./ {
            flush_rule()
            reset_rule()
            line = $0
            sub(/^#### /, "", line)
            n = match(line, /^[0-9]+/)
            id = substr(line, 1, RLENGTH)
            rest = substr(line, RLENGTH + 1)
            sub(/^\.[[:space:]]*/, "", rest)
            title = rest
            next
        }
        /^```regex[[:space:]]*$/ {
            in_regex = 1
            cur_pat = ""
            next
        }
        /^```[[:space:]]*$/ {
            if (in_regex) {
                in_regex = 0
                pat_count++
                pats[pat_count] = cur_pat
                cur_pat = ""
            }
            next
        }
        in_regex {
            if (cur_pat == "") {
                cur_pat = $0
            } else {
                cur_pat = cur_pat "\n" $0
            }
            next
        }
        /^\*\*Severity\*\*:/ {
            v = $0
            sub(/^\*\*Severity\*\*:[[:space:]]*/, "", v)
            sev = v
            next
        }
        /^\*\*Mode\*\*:/ {
            v = $0
            sub(/^\*\*Mode\*\*:[[:space:]]*/, "", v)
            mode = v
            next
        }
        /^\*\*Better alternative\*\*:/ {
            v = $0
            sub(/^\*\*Better alternative\*\*:[[:space:]]*/, "", v)
            better = v
            next
        }
        /^\*\*Extensions\*\*:/ {
            v = $0
            sub(/^\*\*Extensions\*\*:[[:space:]]*/, "", v)
            exts = v
            next
        }
        END {
            flush_rule()
        }
    ' "${RULES_FILE}"

    if [ ! -s "${RULES_TMP}" ]; then
        err "no rules parsed from ${RULES_FILE}"
        err "check that #### N. Title headers, regex blocks, and Severity lines are well-formed"
        exit 2
    fi
}

# Apply --disable to filter out unwanted rules from the cache.
filter_disabled() {
    [ -z "${DISABLED_RULES}" ] && return 0
    local filtered
    filtered="$(mktemp -t ux-lint-rules.XXXXXX)"
    local id_list
    id_list=",${DISABLED_RULES//[[:space:]]/},"
    while IFS=$'\t' read -r id title sev mode exts pat better; do
        [ -z "${id}" ] && continue
        case "${id_list}" in
            *,"${id}",*) continue ;;
        esac
        printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
            "$id" "$title" "$sev" "$mode" "$exts" "$pat" "$better" >> "${filtered}"
    done < "${RULES_TMP}"
    rm -f "${RULES_TMP}"
    RULES_TMP="${filtered}"
}

# Print the rules table for --list-rules. De-duplicate by rule ID since a
# single rule may have multiple regex patterns and therefore multiple cache
# rows.
list_rules() {
    printf '%-4s  %-10s  %-12s  %s\n' "ID" "Severity" "Mode" "Title"
    printf '%-4s  %-10s  %-12s  %s\n' "----" "--------" "----" "-----"
    awk -F'\t' '!seen[$1]++ { printf "%-4s  %-10s  %-12s  %s\n", $1, $3, $4, $2 }' "${RULES_TMP}"
}

# --- file walker -------------------------------------------------------------

# Collect every file extension declared across all rules. Used as the default
# include set when --include is not passed.
extensions_for_all_rules() {
    awk -F'\t' '{ print $5 }' "${RULES_TMP}" \
        | tr ',' '\n' \
        | sed 's/^[[:space:]]*//; s/[[:space:]]*$//' \
        | grep -v '^$' \
        | sort -u
}

# Build a find expression that walks TARGET_PATHS, applies EXCLUDE_GLOBS as
# pruning rules, and prints files matching at least one of the declared
# extensions or user --include globs.
walk_files() {
    local extensions
    extensions="$(extensions_for_all_rules)"

    local -a name_predicates=()
    if [ "${#INCLUDE_GLOBS[@]}" -gt 0 ]; then
        local g
        for g in "${INCLUDE_GLOBS[@]}"; do
            name_predicates+=("$g")
        done
    else
        local ext
        while IFS= read -r ext; do
            [ -z "$ext" ] && continue
            name_predicates+=("*${ext}")
        done <<< "$extensions"
    fi

    if [ "${#name_predicates[@]}" -eq 0 ]; then
        err "no extensions found in rules file and no --include passed"
        return 1
    fi

    local -a find_args=()
    find_args+=("${TARGET_PATHS[@]}")
    find_args+=("(")
    local first=1
    local excl
    for excl in "${EXCLUDE_GLOBS[@]}"; do
        if [ "$first" -eq 1 ]; then
            find_args+=("-path" "$excl")
            first=0
        else
            find_args+=("-o" "-path" "$excl")
        fi
    done
    find_args+=(")" "-prune" "-o")
    find_args+=("-type" "f" "(")
    first=1
    local glob
    for glob in "${name_predicates[@]}"; do
        if [ "$first" -eq 1 ]; then
            find_args+=("-name" "$glob")
            first=0
        else
            find_args+=("-o" "-name" "$glob")
        fi
    done
    find_args+=(")" "-print")
    find "${find_args[@]}" 2>/dev/null
}

# Return 0 if the file's extension matches any in the comma-separated list.
file_matches_extensions() {
    local file="$1"
    local ext_list="$2"
    local ext
    local IFS=','
    for ext in $ext_list; do
        ext="${ext# }"
        ext="${ext% }"
        [ -z "$ext" ] && continue
        case "$file" in
            *"$ext") return 0 ;;
        esac
    done
    return 1
}

# --- finding tracking --------------------------------------------------------

FINDINGS_TMP=""
init_findings() {
    FINDINGS_TMP="$(mktemp -t ux-lint-findings.XXXXXX)"
}

cleanup_findings() {
    if [ -n "${FINDINGS_TMP:-}" ] && [ -f "${FINDINGS_TMP:-}" ]; then
        rm -f "${FINDINGS_TMP}"
    fi
}
trap 'cleanup_tmp; cleanup_findings' EXIT

# Record one finding. Stored as severity_rank|severity|rule_id|title|file:line|matched_text|better
record_finding() {
    local id="$1"
    local title="$2"
    local sev="$3"
    local file="$4"
    local line="$5"
    local matched="$6"
    local better="$7"
    local rank
    rank="$(severity_rank "$sev")"
    # Use a unit-separator character (\x1f) between fields so file paths and
    # match text containing tabs or pipes don't corrupt the row.
    printf '%s\x1f%s\x1f%s\x1f%s\x1f%s:%s\x1f%s\x1f%s\n' \
        "$rank" "$sev" "$id" "$title" "$file" "$line" "$matched" "$better" \
        >> "${FINDINGS_TMP}"
}

# --- scanning ----------------------------------------------------------------

# Strip ANSI-grep highlighting if anyone has GREP_OPTIONS=--color set.
unset GREP_OPTIONS 2>/dev/null || true
export GREP_COLORS=""

# Strip PCRE-only constructs from a pattern so BSD/GNU grep -E can attempt it.
# This is a best-effort fallback only — used when perl is unavailable. It
# removes `(?:...)` group prefixes (treating as `(...)`) and removes any
# `(?!...)`, `(?=...)`, `(?<=...)`, `(?<!...)` lookarounds entirely.
shim_pcre_to_ere() {
    local p="$1"
    # Drop lookarounds whole. This is lossy — it broadens the match.
    p="$(printf '%s' "$p" | sed -E 's/\(\?[!=][^)]*\)//g; s/\(\?<[!=][^)]*\)//g')"
    # Convert non-capturing groups (?: into capturing (
    p="$(printf '%s' "$p" | sed -E 's/\(\?:/(/g')"
    printf '%s' "$p"
}

# Match `pat` against `file` and emit `lineno:matched_text` rows. Uses perl
# when available (PCRE), grep -E as a fallback. Returns 0 on no error
# regardless of match count; matched rows go to stdout.
match_pattern() {
    local file="$1"
    local pat="$2"

    if [ "$HAVE_PERL" -eq 1 ]; then
        # The rules file uses JavaScript-style `\u{HEX}` for unicode code
        # points. Perl's `\u` means "uppercase the next character" — we have
        # to translate to Perl's `\x{HEX}` first.
        local perl_pat
        perl_pat="$(printf '%s' "$pat" | sed -E 's/\\u\{([0-9A-Fa-f]+)\}/\\x{\1}/g')"
        # `perl -CSD -nE` with -CSD setting STDIN/STDOUT to UTF-8 so unicode
        # ranges compile against the matching code point space. The pattern
        # is passed via env to dodge shell-quoting issues. Errors are routed
        # to a tmp file so we can detect bad patterns and skip the rule
        # rather than abort the whole run.
        local err_file
        err_file="$(mktemp -t ux-lint-perl.XXXXXX)"
        UX_LINT_PAT="$perl_pat" perl -CSD -nE '
            use feature "unicode_strings";
            BEGIN {
                $pat = $ENV{UX_LINT_PAT};
                eval { $re = qr/$pat/u };
                if ($@) { die $@ }
            }
            if ($_ =~ $re) {
                chomp;
                next if /ux-lint-disable/;
                print "$.:$_\n";
            }
        ' "$file" 2>"$err_file"
        local rc=$?
        if [ -s "$err_file" ]; then
            local emsg
            emsg="$(head -1 "$err_file")"
            err "rule pattern failed: ${emsg}"
            rm -f "$err_file"
            return 1
        fi
        rm -f "$err_file"
        return $rc
    fi

    # No perl — fall back to grep -E with a shim. May produce false positives
    # because PCRE-only constructs are dropped.
    local shim_pat
    shim_pat="$(shim_pcre_to_ere "$pat")"
    local out
    out="$(LC_ALL=C grep -nE -- "$shim_pat" "$file" 2>/dev/null)"
    local rc=$?
    if [ "$rc" -eq 2 ]; then
        err "grep rejected pattern: $shim_pat"
        return 1
    fi
    # Filter out ux-lint-disable lines.
    if [ -n "$out" ]; then
        printf '%s\n' "$out" | grep -v 'ux-lint-disable'
    fi
    return 0
}

scan_one() {
    local file="$1"
    local id="$2"
    local title="$3"
    local sev="$4"
    local pat="$5"
    local better="$6"

    local out
    out="$(match_pattern "$file" "$pat")"
    [ -z "$out" ] && return 0

    # Iterate matches.
    while IFS= read -r match_line; do
        [ -z "$match_line" ] && continue
        local lineno text
        lineno="${match_line%%:*}"
        text="${match_line#*:}"
        case "$text" in
            *ux-lint-disable*) continue ;;
        esac
        # Trim leading whitespace from the matched text for cleaner display.
        text="${text#"${text%%[![:space:]]*}"}"
        # Cap match length to avoid wrecking the report layout.
        if [ "${#text}" -gt 120 ]; then
            text="${text:0:117}..."
        fi
        record_finding "$id" "$title" "$sev" "$file" "$lineno" "$text" "$better"
    done <<< "$out"
}

# --- reporting ---------------------------------------------------------------

print_report() {
    local files_scanned="$1"
    local min_rank=99
    if [ -n "$MIN_SEVERITY" ]; then
        min_rank="$(severity_rank "$MIN_SEVERITY")"
    fi

    # Sort findings by severity rank (numeric), then file, then line.
    local sorted=""
    if [ -s "${FINDINGS_TMP}" ]; then
        sorted="$(sort -t $'\x1f' -k1,1n -k5,5 "${FINDINGS_TMP}")"
    fi

    # Count by severity. Deduplicate by rule_id|file|line so the same line
    # being matched by two patterns of the same rule counts once.
    local crit=0 high=0 med=0 cos=0
    if [ -s "${FINDINGS_TMP}" ]; then
        # awk emits one line per unique (rule_id, file:line) pair, then a
        # second awk counts by severity. Using awk for the count avoids the
        # `grep -c` "no match returns 1" gotcha that would mangle the value.
        local counts
        counts="$(awk -F$'\x1f' '
            !seen[$3 "|" $5]++ {
                c[$2]++
            }
            END {
                printf "%d %d %d %d\n", c["Critical"]+0, c["High"]+0, c["Medium"]+0, c["Cosmetic"]+0
            }
        ' "${FINDINGS_TMP}")"
        crit="${counts%% *}"
        local rest="${counts#* }"
        high="${rest%% *}"
        rest="${rest#* }"
        med="${rest%% *}"
        cos="${rest##* }"
    fi
    local total=$((crit + high + med + cos))

    if [ "$CI_MODE" -eq 1 ]; then
        if [ -n "$sorted" ]; then
            local seen=""
            while IFS=$'\x1f' read -r rank sev id title fileline matched better; do
                [ "$rank" -gt "$min_rank" ] && continue
                local key="${id}|${fileline}"
                case "|$seen|" in
                    *"|$key|"*) continue ;;
                esac
                seen="$seen|$key"
                local file="${fileline%:*}"
                local line="${fileline##*:}"
                printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
                    "$sev" "$id" "$title" "$file" "$line" "$matched" "$better"
            done <<< "$sorted"
        fi
        err "ux-lint scanned ${files_scanned} files, found ${total} (critical=${crit} high=${high} medium=${med} cosmetic=${cos})"
        compute_exit_code
        return $?
    fi

    # Human-readable report.
    printf -- '─── /ux-lint report ───\n'
    printf 'Scanned: %s files\n' "$files_scanned"
    printf 'Found:   %s violations\n' "$total"
    printf 'Critical: %s  High: %s  Medium: %s  Cosmetic: %s\n\n' "$crit" "$high" "$med" "$cos"

    if [ "$total" -eq 0 ]; then
        printf 'no findings.\n\n'
    else
        if [ -n "$sorted" ]; then
            local seen=""
            while IFS=$'\x1f' read -r rank sev id title fileline matched better; do
                [ -z "$rank" ] && continue
                [ "$rank" -gt "$min_rank" ] && continue
                local key="${id}|${fileline}"
                case "|$seen|" in
                    *"|$key|"*) continue ;;
                esac
                seen="$seen|$key"
                local sev_upper
                case "$sev" in
                    Critical) sev_upper="CRITICAL" ;;
                    High)     sev_upper="HIGH" ;;
                    Medium)   sev_upper="MEDIUM" ;;
                    Cosmetic) sev_upper="COSMETIC" ;;
                    *)        sev_upper="$sev" ;;
                esac
                printf '[%s] Rule %s — %s\n' "$sev_upper" "$id" "$title"
                printf '  %s  `%s`\n' "$fileline" "$matched"
                printf '  Better: %s\n\n' "$better"
            done <<< "$sorted"
        fi
    fi

    printf -- '─── verdict ───\n'

    compute_exit_code
    local exit_code=$?

    printf '%s critical · %s high · %s medium · %s cosmetic → CI exit code: %s (fail-on: %s)\n' \
        "$crit" "$high" "$med" "$cos" "$exit_code" "$FAIL_ON"
    if [ "$exit_code" -ne 0 ]; then
        printf 'Recommended next: /ux-polish --fix (LLM-driven, addresses both lintable and aesthetic findings)\n'
    fi
    return $exit_code
}

# Compute the exit code based on findings and --fail-on threshold.
compute_exit_code() {
    local threshold_rank
    threshold_rank="$(severity_rank "$FAIL_ON")"
    if [ ! -s "${FINDINGS_TMP}" ]; then
        return 0
    fi
    local worst_rank
    worst_rank="$(awk -F$'\x1f' 'NR==1{min=$1} $1<min{min=$1} END{print min+0}' "${FINDINGS_TMP}")"
    [ -z "$worst_rank" ] && return 0
    if [ "$worst_rank" -le "$threshold_rank" ]; then
        return 1
    fi
    return 0
}

# --- main --------------------------------------------------------------------

main() {
    parse_args "$@"
    parse_rules
    filter_disabled

    if [ "$SHOW_RULES" -eq 1 ]; then
        list_rules
        exit 0
    fi

    init_findings

    # Walk files and scan each one against every applicable rule.
    local files_scanned=0
    local file
    while IFS= read -r file; do
        [ -z "$file" ] && continue
        [ -f "$file" ] || continue
        files_scanned=$((files_scanned + 1))
        # For each cached rule row, check whether the file extension matches.
        while IFS=$'\t' read -r id title sev mode exts pat better; do
            [ -z "$id" ] && continue
            if [ "$exts" = ".*" ] || file_matches_extensions "$file" "$exts"; then
                scan_one "$file" "$id" "$title" "$sev" "$pat" "$better"
            fi
        done < "${RULES_TMP}"
    done < <(walk_files)

    if [ "$files_scanned" -eq 0 ]; then
        if [ "$CI_MODE" -eq 1 ]; then
            err "ux-lint: no files scanned"
        else
            printf -- '─── /ux-lint report ───\n'
            printf 'Scanned: 0 files\n'
            printf 'no files matched. check --include and target paths.\n'
        fi
        exit 0
    fi

    print_report "$files_scanned"
    exit $?
}

main "$@"
