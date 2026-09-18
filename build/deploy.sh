#!/bin/zsh
# Rebuild the In Time page from the vault build files and push to helenarong2703/in-time.
# Copies ONLY the listed files. Never copy in-time-private/ (contacts) anywhere.
set -e
set -o pipefail
V="/Users/hr2703/Dropbox/Obsidian Notes/05_RESEARCH/02_Embodied Urban Futures/Venice Biennale 2027 Venice China Pavilion"
BD="$V/in-time-build"; R="$HOME/in-time-exhibition"; MSG="${1:-Update page}"
cd /tmp && python3 "$BD/venice_build.py" "$V" | tail -1
H="$V/In Time - Selected Projects in Six Temporal Dimensions.html"
if grep -qiE "[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}" "$H"; then echo "ABORT: an email address is in the HTML"; grep -oiE "[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}" "$H" | head; exit 1; fi
if grep -q '"contact"' "$BD/venice_pool.json"; then echo "ABORT: contact field in pool json"; exit 1; fi
cp "$H" "$R/index.html"
cp "$BD/venice_build.py" "$BD/venice_pool.json" "$BD/venice_images.json" "$BD/venice_repair2.py" "$BD/deploy.sh" "$R/build/"
cp "$V"/in-time-assets/*.jpg "$R/in-time-assets/"
cd "$R" && git add -A && (git -c user.name="Jane (Protopolis Lab)" -c user.email="hr2703@nyu.edu" commit -q -m "$MSG" || echo "nothing to commit") && git push -q origin main && git log --oneline | head -1
