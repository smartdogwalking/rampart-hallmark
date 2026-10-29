#!/usr/bin/env python3
"""Run pinned Hallmark static checks and retain findings without importing its house style."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
LINTER = ROOT / 'skills/hallmark/scripts/sloplint.mjs'
SOURCE = '8f6969f8922caabde9de1784959eae11ddf68073'
EXPECTED = '05b07befd4a0c24845a29fbd9d4b7c0e4b154eeefa8067e8b11a4f44c9f7ab36'
# Candidates for functional inspection, not automatic evidence of an actual defect.
FUNCTIONAL = {'15', '17', '18', '26a', '27', '33', '39a', '40', '41',
              '53', '56', '62', '70', '73', '76', 'kept'}


def classify(finding):
    gate = str(finding['gate'])
    if gate.startswith('F') or finding.get('tier') == 'finish':
        return 'finish'
    return 'functional-review' if gate in FUNCTIONAL else 'design-review'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('paths', nargs='+', type=Path)
    ap.add_argument('--output', required=True, type=Path)
    ap.add_argument('--scope', choices=['page', 'app', 'component'], default='page')
    ap.add_argument('--stage', choices=['hero', 'page'], default='page')
    ap.add_argument('--mode', choices=['audit', 'before', 'kept'], default='audit')
    args = ap.parse_args()
    if hashlib.sha256(LINTER.read_bytes()).hexdigest() != EXPECTED:
        ap.error('Upstream checker changed: review its source and mapping before changing the pin.')
    paths = [str(p.resolve(strict=True)) for p in args.paths]
    if str(args.output.resolve()) in paths:
        ap.error('The report must not overwrite an input.')
    cmd = ['node', str(LINTER), *paths, '--scope', args.scope,
           '--stage', args.stage, '--json']
    if args.mode != 'audit':
        cmd.append('--' + args.mode)
    # No render flag: browser operations belong to the host's supported browser tool.
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode not in (0, 1):
        raise SystemExit(result.stderr or result.stdout or 'Checker failed')
    raw = json.loads(result.stdout)
    if not raw.get('summary', {}).get('files'):
        raise SystemExit('No source files checked')
    findings = [{**f, 'rampartTier': classify(f), 'requiresVerification': True}
                for f in raw['findings']]
    output = {
        'sourceCommit': SOURCE, 'linterSha256': EXPECTED,
        'mode': args.mode, 'scope': args.scope, 'stage': args.stage,
        'upstreamExitCode': result.returncode,
        'upstreamSummary': raw['summary'],
        'counts': {tier: sum(f['rampartTier'] == tier for f in findings)
                   for tier in ['functional-review', 'design-review', 'finish']},
        'browserChecked': False, 'qualityVerdict': 'not-assessed',
        'limits': 'Static heuristic findings require inspection. No automatic style repair, accessibility certification, taste vote or premium-quality verdict.',
        'findings': findings,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({'report': str(args.output.resolve()), **output['counts'],
                      'browserChecked': False, 'qualityVerdict': 'not-assessed'}))


if __name__ == '__main__':
    main()
