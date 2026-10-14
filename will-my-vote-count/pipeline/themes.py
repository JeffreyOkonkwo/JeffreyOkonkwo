"""Fear themes for Nigerian election comments, each mapped to the INEC process step it touches.

Keyword lists come from research/public_fears.md (survey evidence, news, 2023 studies).
Pidgin items were compiled from common usage and checked against a hand-read sample.
A comment can carry several themes. Matching is case-insensitive on word boundaries.
"""
import re

# id, label, INEC process step (or "Outside INEC"), patterns
THEMES = [
    ("rigging", "Results will be rigged", "6 Collation and declaration", [
        r"rig+(ed|ing|gers?)?\b", r"rig am", r"dem (go|don) rig", r"(written|write|writing) (the )?results?",
        r"results? (are |is )?already (written|decided)", r"stolen mandate", r"stole the (election|mandate)",
        r"electoral robbery", r"daylight robbery", r"selection,? not (an )?election", r"collation",
        r"ec ?8a", r"result sheets?", r"inflated (figures|results|votes)", r"over-?voting", r"ballot (box )?(stuffing|snatch\w*)",
        r"snatch\w*", r"manipulat\w+", r"doctored results?", r"fake results?", r"returning officer"]),
    ("upload", "Results will not be uploaded", "5 Result upload (IReV)", [
        r"e-?transmission", r"electronic(ally)? transmi\w+", r"real[- ]time (transmission|upload)", r"transmi(t|ssion) (of )?(the )?results?",
        r"\bi-?rev\b", r"result viewing portal", r"\bbvas\b", r"bimodal", r"card reader", r"glitch\w*", r"\bupload\w*",
        r"not uploaded", r"blurred", r"section 60", r"manual (collation|transmission)", r"occupy ?nass", r"dem no upload",
        r"bvas no work", r"bypass\w* bvas", r"\bserver\b"]),
    ("violence", "Violence will stop people voting", "4 Voting day security", [
        r"insecurity", r"bandit\w*", r"kidnap\w*", r"terroris\w+", r"boko haram", r"iswap", r"lakurawa", r"herdsm[ae]n",
        r"unknown gunmen", r"sit[- ]at[- ]home", r"\bipob\b", r"polling units? (was |were )?attacked", r"inec office (burnt|attacked|set ablaze)",
        r"\bidps?\b", r"risk my life", r"na life i get", r"safe to vote", r"bloodshed", r"election violence"]),
    ("thugs", "Thugs will intimidate voters", "4 Voting day security", [
        r"thugs?\b", r"thuggery", r"area boys?", r"agberos?", r"touts?\b", r"hoodlums?", r"cultists?", r"intimidat\w+",
        r"dem dey flog", r"scatter (the )?polling", r"box (was )?snatched", r"shooting at", r"machete", r"#?votenotfight"]),
    ("vote_buying", "Votes will be bought", "3 Voting at the polling unit", [
        r"vote[- ]?buy\w*", r"buy(ing)? (of )?votes?", r"vote[- ](trading|selling)", r"sell(ing)? (your|my|their|our) votes?",
        r"stomach infrastructure", r"dibo ko se obe", r"see and buy", r"cash for votes?", r"money for votes?",
        r"dem dey share (money|rice)", r"bags? of rice", r"palliatives?", r"(5|10|20|50)k (per|for|to) vote", r"na money dey talk",
        r"chop (their|dem|una) money", r"collect (their|the) money", r"per vote"]),
    ("inec_trust", "INEC is not neutral or able", "0 INEC as an institution", [
        r"inec (is |na |don )?(so |very |completely )?(biased|compromised|partisan|apc|collect\w*|corrupt|useless|incompetent)", r"(compromised|partisan|biased|useless|corrupt) inec",
        r"(amupitan|inec chairman|yakubu)\b.{0,60}\b(resign\w*|incompeten\w+|bias\w*|compromised|lawless|partisan|fool|liars?|lies|corrupt|problem|guided|shame\w*)", r"materials? (no reach|arrived late|did not arrive)", r"late (arrival of )?materials",
        r"inec wahala", r"trust\w* (in )?inec", r"inec\b.{0,30}\bproblem", r"independen\w+.{0,25}\binec\b", r"\binec\b.{0,25}independen\w+", r"inec cannot be trusted", r"\binec\b.{0,40}\b(fraud|scam|thie(f|ves)|lie|lies|liars?)\b"]),
    ("apathy", "My vote will not count", "Turnout", [
        r"(my|our|your) votes? (no go|will not|won.?t|does not|doesn.?t|do not|don.?t|never) count",
        r"votes? (do not|don.?t|never) count", r"waste of time", r"no need (to|for) vot\w+", r"i no (dey|go) vote",
        r"i (will|would) not vote", r"i won.?t vote", r"i.?a?m not voting", r"na dem dem", r"nothing (go|will) change", r"nothing changes",
        r"apathy", r"low turnout", r"already decided", r"predetermined", r"why (should|would) i vote"]),
    ("courts", "The courts will decide, not voters", "7 Petitions and tribunals", [
        r"tribunal", r"\bpepc\b", r"petition\w*", r"supreme court", r"court of appeal", r"go to court", r"court (will|go) decide",
        r"judgm?ents? for sale", r"cash and carry", r"technicalit(y|ies)", r"judiciary", r"\bjudges\b", r"\bthe judge\b", r"\bcourts?\b", r"nullif\w+", r"my lords?\b"]),
    ("registration", "I cannot register or get my PVC", "1 Registration and PVC", [
        r"\bpvcs?\b", r"permanent voter'?s? cards?", r"voter'?s? cards?", r"\bcvr\b", r"continuous voter registration",
        r"registration (centre|center|portal)", r"collect (my|your|their) pvc", r"voter'?s? register", r"bloated register",
        r"dead voters", r"ghost voters", r"underage", r"double registration", r"revalidation", r"inec portal"]),
    ("misinfo", "Fake news will mislead voters", "Information", [
        r"fake news", r"deep ?fakes?", r"ai[- ](video|generated)", r"doctored video", r"propaganda", r"\bbots?\b",
        r"troll farm", r"paid influencers?", r"\bagbado\b", r"e-?rats?", r"whatsapp broadcast", r"fact-?check\w*"]),
    ("one_party", "One party will dominate", "2 Parties and candidates", [
        r"one[- ]party (state|system|nation)", r"defect\w*", r"decamp\w*", r"cross[- ]carpet\w*", r"carpet[- ]crossing",
        r"opposition is dead", r"dictatorship", r"delisted", r"factions?\b", r"all of them (don )?join apc"]),
    ("diaspora", "Nigerians abroad cannot vote", "1 Registration and PVC", [
        r"\bjapa\b", r"diaspora (voting|vote)", r"nigerians (abroad|in (the )?diaspora)", r"vote from abroad", r"embassy voting"]),
    ("hardship", "Hardship makes votes cheap", "Outside INEC", [
        r"hardship", r"\bhunger\b", r"cost of living", r"inflation", r"food prices?", r"fuel price", r"subsidy removal",
        r"e hard", r"country hard", r"suffering and smiling", r"renewed hopelessness", r"hunger dey", r"we dey suffer",
        r"jobless", r"unemployment", r"endbadgovernance"]),
    ("ethnic", "Tribe and religion will divide us", "Outside INEC", [
        r"tribalis\w+", r"tribalistic", r"\bigbos?\b", r"\byorubas?\b", r"\bhausas?\b", r"\bfulanis?\b", r"ndigbo", r"\barewa\b",
        r"oduduwa", r"biafra\w*", r"northerners", r"southerners", r"zoning", r"power shift", r"muslim[- ]muslim",
        r"emi ?lokan", r"go back to your village"]),
    # Not matched by keywords: analyse.py moves court comments under pre-election court videos here (see PRE_ELECTION_COURT_VIDEOS).
    ("court_pre", "Courts will decide who can run", "2 Parties and candidates", [r"(?!x)x"]),
]

# Videos about pre-election court cases (party deadlines, a recall petition). Court comments under them are about who can run, not about results.
PRE_ELECTION_COURT_VIDEOS = {"rBjasEsAXAw", "fQ8FDQn4go0"}

COMPILED = [(tid, label, step, re.compile(r"(?<![a-z])(" + "|".join(p) + r")", re.I)) for tid, label, step, p in THEMES]
LABEL = {t[0]: t[1] for t in THEMES}
STEP = {t[0]: t[2] for t in THEMES}

ELECTION_WORDS = re.compile(r"\b(inec|elect\w*|vote\w*|voting|voter\w*|poll\w*|ballot|pvc|bvas|irev|collation|rig\w*|tribunal|2027|campaign)\b", re.I)


def tag(text: str) -> list[str]:
    t = text or ""
    found = [tid for tid, _, _, rx in COMPILED if rx.search(t)]
    # Context themes count only when the comment is about the election, so a complaint about food prices alone is not an election fear.
    if found and not ELECTION_WORDS.search(t):
        found = [f for f in found if f not in ("hardship", "ethnic", "violence", "misinfo", "diaspora")]
    return found
