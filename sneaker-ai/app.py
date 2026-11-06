import os
import random
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "sneaker-studio-dev-key"

# hCaptcha site key (used for client-side captcha display & token requirement)
HCAPTCHA_SITE_KEY = os.environ.get("HCAPTCHA_SITE_KEY", "").strip()

def adjust_hex(hex_color, amount):
    """Lighten or darken a hex color by amount (-255 to 255)."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        return f"#{hex_color}"
    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        r = max(0, min(255, r + amount))
        g = max(0, min(255, g + amount))
        b = max(0, min(255, b + amount))
        return f"#{r:02X}{g:02X}{b:02X}"
    except Exception:
        return f"#{hex_color}"

def get_prefs(data):
    return {
        "style": (data.get("style") or "Casual").capitalize(),
        "material": (data.get("material") or "Leather").capitalize(),
        "occasion": (data.get("occasion") or "Everyday").capitalize(),
        "primary_color": data.get("primary_color") or "#00c3ff",
        "accent_color": data.get("accent_color") or "#ebc9a0",
        "inspiration": (data.get("inspiration") or "").strip()
    }

# Predefined design matrix for procedural concept generation
STYLE_FEATURES = {
    "athletic": [
        "Dynamic high-rebound energy-return foam core",
        "Carbon-composite propulsion torsion shank",
        "Multi-zone anatomical flex groove outsole",
        "Ultralight reflective 3M safety illumination"
    ],
    "casual": [
        "Ergonomic dual-density memory foam footbed",
        "Flexible low-fatigue perimeter cupsole",
        "Breathable cushioned tongue & ankle collar",
        "Reinforced abrasion-resistant heel counter"
    ],
    "luxury": [
        "Hand-burnished Italian perimeter panel edging",
        "Debossed minimal foil serial insignia",
        "Supple glove-leather interior sockliner",
        "Waxed woven cotton laces with brushed metal aglets"
    ],
    "retro": [
        "Vintage-tinted vulcanized rubber cupsole",
        "Heritage archive woven tongue badge",
        "Perforated toe-box aeration matrix",
        "Double-needle structural seam reinforcement"
    ],
    "futuristic": [
        "Deconstructed parametric exoskeleton chassis",
        "Modular quick-cinch tension lacing system",
        "Sculpted geometric aerodynamic midsole",
        "Luminescent cyber-reactive accent piping"
    ],
    "streetwear": [
        "Bold oversized sculptural sole profile",
        "Utility webbing heel pull-tab with industrial branding",
        "Multi-layered tactile panel architecture",
        "High-contrast color-blocked compound outsole"
    ]
}

OCCASION_SOLES = {
    "everyday": "Segmented compound EVA foam with vulcanized rubber ground-contact pods",
    "running": "Supercritical nitrogen-infused dual-density foam with carbon propulsion plate",
    "performance running": "Supercritical nitrogen-infused dual-density foam with carbon propulsion plate",
    "basketball": "Pressurized air-cushioning chamber with lateral outrigger anti-roll barrier",
    "court basketball": "Pressurized air-cushioning chamber with lateral outrigger anti-roll barrier",
    "hiking": "Vibram-grade high-traction lugged rubber compound with integrated rock-shield",
    "trail & hiking": "Vibram-grade high-traction lugged rubber compound with integrated rock-shield",
    "limited ed.": "Bespoke hand-poured sculptural polyurethane midsole with perimeter welt",
    "limited runway": "Bespoke hand-poured sculptural polyurethane midsole with perimeter welt"
}

MATERIAL_SPECS = {
    "leather": [
        "Hand-selected full-grain leather chassis",
        "Micro-perforated breathability lateral panels",
        "Reinforced stitch-stay lace framing"
    ],
    "canvas": [
        "Heavyweight 14oz structured organic canvas",
        "Double-bonded abrasion-resistant side walls",
        "Soft brushed-cotton interior ankle lining"
    ],
    "mesh": [
        "High-tensile diamond-weave ripstop mesh",
        "Thermoweld seamless film structural overlays",
        "Moisture-wicking open-cell aeration matrix"
    ],
    "ripstop mesh": [
        "High-tensile diamond-weave ripstop mesh",
        "Thermoweld seamless film structural overlays",
        "Moisture-wicking open-cell aeration matrix"
    ],
    "suede": [
        "Silky short-nap European calf suede upper",
        "Reinforced split-suede toe bumper lining",
        "Tonal stitch perimeter accents"
    ],
    "knit": [
        "Seamless engineered zone-stretch knit bootie",
        "Variable-density compressive arch banding",
        "Ultra-lightweight breathable open-weave vamp"
    ],
    "engineered knit": [
        "Seamless engineered zone-stretch knit bootie",
        "Variable-density compressive arch banding",
        "Ultra-lightweight breathable open-weave vamp"
    ],
    "recycled": [
        "Circular-economy post-consumer recycled polymer upper",
        "Algae-derived eco-foam cushioned midsole",
        "Zero-waste ultrasonic bonded seam construction"
    ],
    "recycled polymer": [
        "Circular-economy post-consumer recycled polymer upper",
        "Algae-derived eco-foam cushioned midsole",
        "Zero-waste ultrasonic bonded seam construction"
    ]
}

def generate_procedural_concept(prefs):
    """Generate predefined, structured sneaker identity and colorway parameters."""
    style_key = prefs["style"].lower()
    occasion_key = prefs["occasion"].lower()
    material_key = prefs["material"].lower()

    # Dynamic naming matrix
    prefixes = ["AERO", "TERRA", "VORTEX", "NEXUS", "KINETIC", "CHRONO", "ECHO", "SOLAR", "APEX", "STRATA", "CYBER", "HYPER"]
    suffixes = ["RUNNER", "LOW", "DRIFT", "STRYKE", "MATRIX", "PHANTOM", "ZERO", "MODULE", "LAB", "VISION", "SHADOW", "PRIME"]
    name = f"{random.choice(prefixes)} {random.choice(suffixes)} / {prefs['style'].upper()}"

    p_col = prefs["primary_color"]
    a_col = prefs["accent_color"]
    inspo = prefs.get("inspiration", "").strip()

    # Predefined Taglines
    if inspo:
        tagline = f"Infused with {inspo[:40]} aesthetic narrative."
    else:
        tagline_options = [
            f"Engineered for high-agility {prefs['occasion']} traversal.",
            f"Bespoke {prefs['material']} craftsmanship meets modern silhouette.",
            f"Precision-tuned for all-day {prefs['style']} ergonomics.",
            f"A progressive fusion of comfort, durability, and form."
        ]
        tagline = random.choice(tagline_options)

    # Predefined Description
    desc = (
        f"Constructed utilizing a bespoke {prefs['material']} chassis engineered for "
        f"{prefs['occasion']} agility, highlighting custom {prefs['style']} design accents "
        f"and calibrated ergonomics."
    )

    # Predefined materials
    materials = MATERIAL_SPECS.get(material_key) or [
        f"Hand-selected {prefs['material']} paneling",
        "High-tensile micro-mesh articulation zones",
        "Multi-density ergonomic chassis matrix"
    ]

    # Predefined features
    features = STYLE_FEATURES.get(style_key) or [
        "Anatomical impact-cushioning footbed",
        "Directional multi-surface traction geometry",
        "Deconstructed ergonomic tongue & lace cage",
        "Reinforced torsional arch stabilizer"
    ]

    # Predefined sole
    sole = OCCASION_SOLES.get(occasion_key) or "Segmented compound EVA foam with vulcanized rubber stabilizers"

    # Predefined Colorways (Signature, Stealth, High-Voltage)
    is_dark = p_col.lower() in ["#000000", "#111118", "#16161c", "#1a1a2e", "#0d0d12"]
    colorways = [
        {
            "name": "Bespoke Signature",
            "upper": p_col,
            "panel": adjust_hex(p_col, -25),
            "toe": adjust_hex(p_col, 20),
            "accent": a_col,
            "lace": "#FFFFFF" if is_dark else "#1A1A1A",
            "sole": "#EAEAEF",
            "tongue": a_col
        },
        {
            "name": "Stealth Carbon",
            "upper": "#141419",
            "panel": "#202026",
            "toe": "#181820",
            "accent": p_col,
            "lace": "#F0F0F5",
            "sole": "#0C0C0F",
            "tongue": "#22222B"
        },
        {
            "name": "High Voltage",
            "upper": a_col,
            "panel": adjust_hex(a_col, -25),
            "toe": adjust_hex(a_col, 20),
            "accent": p_col,
            "lace": "#202025",
            "sole": "#FAFAFA",
            "tongue": p_col
        }
    ]

    # Predefined retail price bracket
    base_prices = {"luxury": 260, "athletic": 190, "retro": 160, "streetwear": 210, "futuristic": 220, "casual": 150}
    base = base_prices.get(style_key, 170)
    retail_price = f"${base + random.randint(0, 4) * 10} USD"

    return {
        "name": name,
        "tagline": tagline,
        "description": desc,
        "materials": materials,
        "features": features,
        "sole_type": sole,
        "colorways": colorways,
        "target_audience": f"{prefs['occasion']} / Unisex",
        "retail_price": retail_price,
        "style_tags": [prefs["style"].upper(), prefs["material"].upper(), prefs["occasion"].upper()]
    }

@app.route("/")
@app.route("/studio")
@app.route("/history")
def index():
    return render_template("index.html", hcaptcha_site_key=HCAPTCHA_SITE_KEY)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or request.form or {}
    token = data.get("hcaptcha_response") or data.get("h-captcha-response")

    # If hCaptcha site key is set, check that the user completed the widget on the frontend
    if HCAPTCHA_SITE_KEY and not token:
        return jsonify({
            "success": False,
            "error": "Please complete the hCaptcha verification challenge."
        }), 400

    prefs = get_prefs(data)
    concept = generate_procedural_concept(prefs)

    return jsonify({
        "success": True,
        "concept": concept,
        "prefs": prefs
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
