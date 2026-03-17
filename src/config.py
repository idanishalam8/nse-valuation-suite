# ─────────────────────────────────────────────────────────────────────────────
# config.py  ·  NSE Valuation Suite — Central Configuration
# ─────────────────────────────────────────────────────────────────────────────

# ── NSE 500 Universe: sector → list of (ticker, company_name, market_cap_tier)
# market_cap_tier: "large" >20000Cr, "mid" 5000-20000Cr, "small" <5000Cr
NSE500 = {
    "Information Technology": [
        ("TCS.NS","Tata Consultancy Services","large"),
        ("INFY.NS","Infosys","large"),
        ("WIPRO.NS","Wipro","large"),
        ("HCLTECH.NS","HCL Technologies","large"),
        ("TECHM.NS","Tech Mahindra","large"),
        ("LTIM.NS","LTIMindtree","large"),
        ("PERSISTENT.NS","Persistent Systems","mid"),
        ("MPHASIS.NS","Mphasis","mid"),
        ("COFORGE.NS","Coforge","mid"),
        ("OFSS.NS","Oracle Financial Services","mid"),
        ("KPIT.NS","KPIT Technologies","mid"),
        ("TATAELXSI.NS","Tata Elxsi","mid"),
        ("CYIENT.NS","Cyient","mid"),
        ("MASTEK.NS","Mastek","small"),
        ("ZENSAR.NS","Zensar Technologies","small"),
    ],
    "Banking": [
        ("HDFCBANK.NS","HDFC Bank","large"),
        ("ICICIBANK.NS","ICICI Bank","large"),
        ("KOTAKBANK.NS","Kotak Mahindra Bank","large"),
        ("AXISBANK.NS","Axis Bank","large"),
        ("SBIN.NS","State Bank of India","large"),
        ("INDUSINDBK.NS","IndusInd Bank","large"),
        ("BANDHANBNK.NS","Bandhan Bank","mid"),
        ("FEDERALBNK.NS","Federal Bank","mid"),
        ("IDFCFIRSTB.NS","IDFC First Bank","mid"),
        ("PNB.NS","Punjab National Bank","large"),
        ("CANBK.NS","Canara Bank","large"),
        ("BANKBARODA.NS","Bank of Baroda","large"),
        ("AUBANK.NS","AU Small Finance Bank","mid"),
        ("RBLBANK.NS","RBL Bank","mid"),
        ("KARURVYSYA.NS","Karur Vysya Bank","small"),
    ],
    "FMCG": [
        ("HINDUNILVR.NS","Hindustan Unilever","large"),
        ("ITC.NS","ITC","large"),
        ("NESTLEIND.NS","Nestle India","large"),
        ("BRITANNIA.NS","Britannia Industries","large"),
        ("DABUR.NS","Dabur India","large"),
        ("GODREJCP.NS","Godrej Consumer Products","large"),
        ("MARICO.NS","Marico","large"),
        ("COLPAL.NS","Colgate-Palmolive","large"),
        ("EMAMILTD.NS","Emami","mid"),
        ("TATACONSUM.NS","Tata Consumer Products","large"),
        ("VBL.NS","Varun Beverages","large"),
        ("PGHH.NS","Procter & Gamble Hygiene","mid"),
        ("GILLETTE.NS","Gillette India","mid"),
        ("ZYDUSWELL.NS","Zydus Wellness","mid"),
        ("RADICO.NS","Radico Khaitan","mid"),
    ],
    "Automobiles": [
        ("MARUTI.NS","Maruti Suzuki","large"),
        ("TATAMOTORS.NS","Tata Motors","large"),
        ("M&M.NS","Mahindra & Mahindra","large"),
        ("BAJAJ-AUTO.NS","Bajaj Auto","large"),
        ("EICHERMOT.NS","Eicher Motors","large"),
        ("HEROMOTOCO.NS","Hero MotoCorp","large"),
        ("TVSMOTORS.NS","TVS Motor Company","large"),
        ("ASHOKLEY.NS","Ashok Leyland","large"),
        ("BALKRISIND.NS","Balkrishna Industries","mid"),
        ("TIINDIA.NS","Tube Investments","mid"),
        ("MOTHERSON.NS","Samvardhana Motherson","large"),
        ("BOSCHLTD.NS","Bosch","large"),
        ("APOLLOTYRE.NS","Apollo Tyres","mid"),
        ("MRF.NS","MRF","large"),
        ("CEATLTD.NS","CEAT","mid"),
    ],
    "Pharmaceuticals": [
        ("SUNPHARMA.NS","Sun Pharmaceutical","large"),
        ("DRREDDY.NS","Dr. Reddy's Laboratories","large"),
        ("CIPLA.NS","Cipla","large"),
        ("DIVISLAB.NS","Divi's Laboratories","large"),
        ("BIOCON.NS","Biocon","large"),
        ("LUPIN.NS","Lupin","large"),
        ("AUROPHARMA.NS","Aurobindo Pharma","large"),
        ("TORNTPHARM.NS","Torrent Pharmaceuticals","large"),
        ("ALKEM.NS","Alkem Laboratories","mid"),
        ("IPCALAB.NS","IPCA Laboratories","mid"),
        ("GLENMARK.NS","Glenmark Pharmaceuticals","mid"),
        ("ABBOTINDIA.NS","Abbott India","mid"),
        ("PFIZER.NS","Pfizer","mid"),
        ("GLAXO.NS","GSK Pharmaceuticals","mid"),
        ("NATCOPHARM.NS","Natco Pharma","small"),
    ],
    "Metals & Mining": [
        ("TATASTEEL.NS","Tata Steel","large"),
        ("JSWSTEEL.NS","JSW Steel","large"),
        ("HINDALCO.NS","Hindalco Industries","large"),
        ("VEDL.NS","Vedanta","large"),
        ("COALINDIA.NS","Coal India","large"),
        ("NMDC.NS","NMDC","large"),
        ("SAIL.NS","Steel Authority of India","large"),
        ("NATIONALUM.NS","National Aluminium","mid"),
        ("HINDCOPPER.NS","Hindustan Copper","mid"),
        ("APLAPOLLO.NS","APL Apollo Tubes","mid"),
        ("JSWENERGY.NS","JSW Energy","large"),
        ("WELCORP.NS","Welspun Corp","mid"),
        ("RATNAMANI.NS","Ratnamani Metals","small"),
        ("JINDALSAW.NS","Jindal Saw","small"),
        ("MOIL.NS","MOIL","small"),
    ],
    "Energy & Oil Gas": [
        ("RELIANCE.NS","Reliance Industries","large"),
        ("ONGC.NS","Oil & Natural Gas Corporation","large"),
        ("NTPC.NS","NTPC","large"),
        ("POWERGRID.NS","Power Grid Corporation","large"),
        ("IOC.NS","Indian Oil Corporation","large"),
        ("BPCL.NS","Bharat Petroleum","large"),
        ("GAIL.NS","GAIL India","large"),
        ("TATAPOWER.NS","Tata Power","large"),
        ("ADANIGREEN.NS","Adani Green Energy","large"),
        ("ADANIPOWER.NS","Adani Power","large"),
        ("TORNTPOWER.NS","Torrent Power","mid"),
        ("CESC.NS","CESC","mid"),
        ("PETRONET.NS","Petronet LNG","large"),
        ("IGL.NS","Indraprastha Gas","mid"),
        ("MGL.NS","Mahanagar Gas","mid"),
    ],
    "Financial Services": [
        ("BAJFINANCE.NS","Bajaj Finance","large"),
        ("BAJAJFINSV.NS","Bajaj Finserv","large"),
        ("HDFCLIFE.NS","HDFC Life Insurance","large"),
        ("SBILIFE.NS","SBI Life Insurance","large"),
        ("ICICIGI.NS","ICICI Lombard","large"),
        ("MUTHOOTFIN.NS","Muthoot Finance","large"),
        ("CHOLAFIN.NS","Cholamandalam Finance","large"),
        ("LICHSGFIN.NS","LIC Housing Finance","large"),
        ("MANAPPURAM.NS","Manappuram Finance","mid"),
        ("M&MFIN.NS","M&M Financial Services","mid"),
        ("SHRIRAMFIN.NS","Shriram Finance","large"),
        ("PNBHOUSING.NS","PNB Housing Finance","mid"),
        ("CANFINHOME.NS","Can Fin Homes","mid"),
        ("AAVAS.NS","Aavas Financiers","mid"),
        ("HOMEFIRST.NS","Home First Finance","small"),
    ],
    "Consumer Durables": [
        ("TITAN.NS","Titan Company","large"),
        ("HAVELLS.NS","Havells India","large"),
        ("CROMPTON.NS","Crompton Greaves Consumer","mid"),
        ("VOLTAS.NS","Voltas","mid"),
        ("WHIRLPOOL.NS","Whirlpool of India","mid"),
        ("BLUESTARCO.NS","Blue Star","mid"),
        ("BATAINDIA.NS","Bata India","mid"),
        ("PAGEIND.NS","Page Industries","large"),
        ("KAJARIACER.NS","Kajaria Ceramics","mid"),
        ("VGUARD.NS","V-Guard Industries","mid"),
        ("ORIENTELEC.NS","Orient Electric","small"),
        ("SYMPHONY.NS","Symphony","small"),
        ("AMBER.NS","Amber Enterprises","mid"),
        ("DIXON.NS","Dixon Technologies","mid"),
        ("VEDANT.NS","Vedant Fashions","mid"),
    ],
    "Healthcare": [
        ("APOLLOHOSP.NS","Apollo Hospitals","large"),
        ("FORTIS.NS","Fortis Healthcare","large"),
        ("MAXHEALTH.NS","Max Healthcare","large"),
        ("NARAYANHLT.NS","Narayana Hrudayalaya","mid"),
        ("METROPOLIS.NS","Metropolis Healthcare","mid"),
        ("DRLALPATH.NS","Dr Lal PathLabs","mid"),
        ("THYROCARE.NS","Thyrocare Technologies","small"),
        ("POLYMED.NS","Poly Medicure","small"),
        ("KIMS.NS","KIMS Hospital","mid"),
        ("ASTER.NS","Aster DM Healthcare","mid"),
        ("RAINBOW.NS","Rainbow Children's Medicare","small"),
        ("VIJAYA.NS","Vijaya Diagnostic Centre","small"),
        ("MEDANTA.NS","Global Health (Medanta)","mid"),
        ("HEALTHIUM.NS","Healthium Medtech","small"),
        ("SYNGENE.NS","Syngene International","mid"),
    ],
    "Real Estate": [
        ("DLF.NS","DLF","large"),
        ("GODREJPROP.NS","Godrej Properties","large"),
        ("OBEROIRLTY.NS","Oberoi Realty","large"),
        ("PHOENIXLTD.NS","Phoenix Mills","large"),
        ("PRESTIGE.NS","Prestige Estates","large"),
        ("BRIGADE.NS","Brigade Enterprises","mid"),
        ("SOBHA.NS","Sobha","mid"),
        ("SUNTECK.NS","Sunteck Realty","mid"),
        ("KOLTEPATIL.NS","Kolte-Patil Developers","small"),
        ("MAHINDCIE.NS","Mahindra Lifespace","small"),
        ("LODHA.NS","Lodha (Macrotech)","large"),
        ("SIGNATUREGLO.NS","Signature Global","mid"),
        ("ANANTRAJ.NS","Anant Raj","small"),
        ("ARVIND.NS","Arvind SmartSpaces","small"),
        ("NESCO.NS","NESCO","small"),
    ],
    "Capital Goods & Infra": [
        ("LT.NS","Larsen & Toubro","large"),
        ("ULTRACEMCO.NS","UltraTech Cement","large"),
        ("GRASIM.NS","Grasim Industries","large"),
        ("ABB.NS","ABB India","large"),
        ("SIEMENS.NS","Siemens India","large"),
        ("BHEL.NS","Bharat Heavy Electricals","large"),
        ("CUMMINSIND.NS","Cummins India","large"),
        ("THERMAX.NS","Thermax","mid"),
        ("KEC.NS","KEC International","mid"),
        ("KALPATPOWR.NS","Kalpataru Projects","mid"),
        ("GRINDWELL.NS","Grindwell Norton","mid"),
        ("SCHAEFFLER.NS","Schaeffler India","mid"),
        ("TIMKEN.NS","Timken India","mid"),
        ("CRAFTSMAN.NS","Craftsman Automation","small"),
        ("ELECON.NS","Elecon Engineering","small"),
    ],
}

# All tickers flat list (for CCA search)
ALL_TICKERS = {}
for sector, companies in NSE500.items():
    for ticker, name, cap_tier in companies:
        ALL_TICKERS[ticker] = {"name": name, "sector": sector, "cap_tier": cap_tier}

# Sector index map for heat map historical data
SECTOR_INDEX_MAP = {
    "Information Technology": "NIFTY IT",
    "Banking":                "NIFTY BANK",
    "FMCG":                   "NIFTY FMCG",
    "Automobiles":            "NIFTY AUTO",
    "Pharmaceuticals":        "NIFTY PHARMA",
    "Metals & Mining":        "NIFTY METAL",
    "Energy & Oil Gas":       "NIFTY ENERGY",
    "Financial Services":     "NIFTY FIN SERVICE",
    "Consumer Durables":      "NIFTY CONSR DURBL",
    "Healthcare":             "NIFTY HEALTHCARE",
    "Real Estate":            "NIFTY REALTY",
    "Capital Goods & Infra":  "NIFTY INFRA",
}

# CCA — multiples to compute
CCA_METRICS = {
    "pe":        {"label": "P/E",        "suffix": "x", "higher_is_expensive": True},
    "fwd_pe":    {"label": "Fwd P/E",    "suffix": "x", "higher_is_expensive": True},
    "ev_ebitda": {"label": "EV/EBITDA",  "suffix": "x", "higher_is_expensive": True},
    "ev_sales":  {"label": "EV/Sales",   "suffix": "x", "higher_is_expensive": True},
    "pb":        {"label": "P/BV",       "suffix": "x", "higher_is_expensive": True},
    "div_yield": {"label": "Div Yield",  "suffix": "%", "higher_is_expensive": False},
}

# Heat map — metric relevance per sector
SECTOR_METRIC_RELEVANCE = {
    "Banking":           ["pe","pb","div_yield"],
    "Financial Services":["pe","pb","ev_ebitda"],
    "Metals & Mining":   ["ev_ebitda","pb","div_yield"],
    "Energy & Oil Gas":  ["ev_ebitda","ev_sales","div_yield"],
    "Real Estate":       ["pb","pe","ev_sales"],
}

# Composite score weights (default)
DEFAULT_WEIGHTS = {"pe": 0.35, "ev_ebitda": 0.30, "pb": 0.25, "div_yield": 0.10}
SECTOR_WEIGHTS  = {
    "Banking":           {"pe": 0.15, "ev_ebitda": 0.05, "pb": 0.60, "div_yield": 0.20},
    "Financial Services":{"pe": 0.20, "ev_ebitda": 0.10, "pb": 0.55, "div_yield": 0.15},
    "Metals & Mining":   {"pe": 0.20, "ev_ebitda": 0.50, "pb": 0.20, "div_yield": 0.10},
    "Energy & Oil Gas":  {"pe": 0.25, "ev_ebitda": 0.40, "pb": 0.15, "div_yield": 0.20},
}

# Richness zones
ZONES = {
    "Very Cheap":    (0,   20),
    "Cheap":         (20,  35),
    "Fair":          (35,  65),
    "Expensive":     (65,  80),
    "Very Expensive":(80, 101),
}
ZONE_COLORS = {
    "Very Cheap":    "#1D9E75",
    "Cheap":         "#5DCAA5",
    "Fair":          "#888780",
    "Expensive":     "#EF9F27",
    "Very Expensive":"#E24B4A",
}

LOOKBACK_OPTIONS = {"5 Years": 5, "7 Years": 7, "10 Years": 10}
NUMERIC_COLS     = ["pe", "pb", "ev_ebitda", "div_yield"]

# Peer matching: cap tier adjacency
CAP_ADJACENCY = {
    "large": ["large", "mid"],
    "mid":   ["large", "mid", "small"],
    "small": ["mid",   "small"],
}

# Historical distribution params for synthetic fallback
SECTOR_HIST_PARAMS = {
    "Information Technology": {"pe":(14,42,25,6),  "pb":(3.5,9.5,6.0,1.5),"ev_ebitda":(10,28,18,4), "div_yield":(0.8,2.8,1.6,0.4)},
    "Banking":                {"pe":(8,22,14,3),   "pb":(1.2,3.8,2.2,0.6),"ev_ebitda":(4,14,8,2),   "div_yield":(0.8,3.0,1.8,0.5)},
    "FMCG":                   {"pe":(28,60,42,8),  "pb":(8,24,14,3.5),    "ev_ebitda":(20,45,30,6), "div_yield":(1.2,3.5,2.2,0.5)},
    "Automobiles":            {"pe":(10,32,20,5),  "pb":(2.0,6.5,3.5,1.0),"ev_ebitda":(6,18,11,3),  "div_yield":(0.5,2.5,1.2,0.4)},
    "Pharmaceuticals":        {"pe":(18,50,30,7),  "pb":(3.0,8.0,5.0,1.2),"ev_ebitda":(12,32,20,5), "div_yield":(0.3,1.5,0.7,0.3)},
    "Metals & Mining":        {"pe":(5,28,12,5),   "pb":(0.8,3.5,1.8,0.6),"ev_ebitda":(3,12,6,2),   "div_yield":(1.0,5.0,2.5,0.8)},
    "Energy & Oil Gas":       {"pe":(8,20,13,3),   "pb":(1.0,3.5,2.0,0.5),"ev_ebitda":(4,12,7,2),   "div_yield":(2.0,6.5,3.5,0.9)},
    "Financial Services":     {"pe":(12,40,22,6),  "pb":(2.0,7.0,4.0,1.2),"ev_ebitda":(6,20,11,3),  "div_yield":(0.3,1.5,0.7,0.3)},
    "Consumer Durables":      {"pe":(30,80,50,12), "pb":(6,22,12,4),      "ev_ebitda":(18,50,32,8), "div_yield":(0.3,1.5,0.7,0.3)},
    "Healthcare":             {"pe":(25,70,40,10), "pb":(4,15,8,2.5),     "ev_ebitda":(16,45,26,7), "div_yield":(0.2,1.2,0.5,0.2)},
    "Real Estate":            {"pe":(12,60,25,10), "pb":(1.5,6.0,3.0,1.0),"ev_ebitda":(8,30,15,5),  "div_yield":(0.2,1.5,0.5,0.3)},
    "Capital Goods & Infra":  {"pe":(14,35,22,5),  "pb":(2.0,6.0,3.5,0.8),"ev_ebitda":(8,22,13,3),  "div_yield":(0.5,2.5,1.2,0.4)},
}
