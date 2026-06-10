# -*- coding: utf-8 -*-
"""Calibración empresarial del simulador a partir de Forbes Global 2000 (2014/2019/2024)."""
import pandas as pd, numpy as np, re, warnings
warnings.filterwarnings("ignore")

UP = "/mnt/user-data/uploads"
PAISES = ["Spain","France","Germany","Italy","Belgium","Portugal","United Kingdom","United States","Canada"]

# ---------------------------------------------------------------- carga
d14 = pd.read_excel(f"{UP}/Forbes_Global_2000_-_2014.xls", engine="xlrd", skiprows=[1])
d14 = d14.rename(columns={"Market Value":"MarketValue"})
for c in ["MarketValue","Sales","Profits","Assets"]:
    d14[c] = pd.to_numeric(d14[c], errors="coerce")

def parse_money(s):
    if pd.isna(s): return np.nan
    s = str(s).replace("$","").replace(",","").strip()
    m = re.match(r"(-?[\d.]+)\s*([BM]?)", s)
    if not m: return np.nan
    v = float(m.group(1))
    return v/1000 if m.group(2)=="M" else v

d19 = pd.read_excel(f"{UP}/Forbes_The_Global_2014__2019__2024.xlsx", sheet_name="2019")
for c in ["Sales","Profits","Assets","Market Value"]:
    d19[c] = d19[c].map(parse_money)
d19 = d19.rename(columns={"Country/Territory":"Country"}).dropna(subset=["Company"])

d24 = pd.read_excel(f"{UP}/Forbes_The_Global_2014__2019__2024.xlsx", sheet_name="2024")
d24 = d24.drop_duplicates(subset=["Name"]).rename(columns={"Name":"Company","Profit":"Profits"})

# ---------------------------------------------------------------- armonización de industrias 2024
MAPA = {
    "Banking":"Banca y finanzas", "Banking and Financial Services":"Banca y finanzas",
    "Diversified Financials":"Banca y finanzas", "Insurance":"Seguros",
    "IT Software & Services":"TI: software y servicios", "Technology Hardware & Equipment":"TI: hardware",
    "Semiconductors":"Semiconductores", "Telecommunications Services":"Telecomunicaciones",
    "Media":"Media y entretenimiento", "Retail and Wholesale":"Comercio", "Retailing":"Comercio",
    "Food Markets":"Comercio", "Oil & Gas Operations":"Petróleo y gas",
    "Utilities":"Utilities", "Construction":"Construcción e inmobiliario",
    "Construction- Chemicals- Raw Materials":"Construcción e inmobiliario", "Real Estate":"Construcción e inmobiliario",
    "Materials":"Materiales y química", "Chemicals":"Materiales y química",
    "Engineering- Manufacturing":"Industria manufacturera", "Capital Goods":"Industria manufacturera",
    "Conglomerate":"Conglomerados", "Conglomerates":"Conglomerados",
    "Pharmaceuticals- Biotechnology":"Farma y biotec", "Drugs & Biotechnology":"Farma y biotec",
    "Health Care Equipment & Services":"Salud", "Healthcare":"Salud",
    "Business Services & Supplies":"Servicios profesionales", "Consumer Services":"Servicios profesionales",
    "Transportation":"Transporte y logística", "Aerospace & Defense":"Aeroespacial y defensa",
    "Food- Drink & Tobacco":"Alimentación y bebidas", "Food Drink & Tobacco":"Alimentación y bebidas",
    "Consumer Durables":"Bienes de consumo", "Household & Personal Products":"Bienes de consumo",
    "Automotive":"Automoción", "Hotels- Restaurants & Leisure":"Hostelería y ocio",
    "Trading Companies":"Comercio",
    "Semiconductors- Electronics- Electrical Engineering":"Semiconductores",
    "Semiconductors- Electronics- Electrical Engineering- Technology Hardware & Equipment":"Semiconductores",
    "Food- Soft Beverages- Alcohol & Tobacco":"Alimentación y bebidas", "Food and Beverage":"Alimentación y bebidas",
    "Food & Drink":"Alimentación y bebidas", "Packaged Goods":"Alimentación y bebidas",
    "Automotive (Automotive and Suppliers)":"Automoción", "Auto Brands":"Automoción",
    "Auto Parts":"Automoción", "Tire Brands":"Automoción", "National Car Dealers":"Automoción",
    "Telecommunications Services- Cable Supplier":"Telecomunicaciones",
    "Transportation and Logistics":"Transporte y logística", "Airlines":"Transporte y logística",
    "Cruise Lines":"Hostelería y ocio", "Travel & Leisure":"Hostelería y ocio",
    "Casinos & Resorts":"Hostelería y ocio", "Hotels":"Hostelería y ocio",
    "Restaurants":"Hostelería y ocio", "Quick- Fast- Casual":"Hostelería y ocio",
    "Clothing- Shoes- Sports Equipment":"Bienes de consumo", "Fashion- Apparel- Shoes":"Bienes de consumo",
    "Home & Furnishings":"Bienes de consumo", "Home Improvement":"Comercio",
    "Department Stores":"Comercio", "Superstores":"Comercio", "Specialty":"Comercio",
    "Media & Advertising":"Media y entretenimiento",
    "Professional Services":"Servicios profesionales", "Professional Service":"Servicios profesionales",
    "Data Analytics & Big Data":"TI: software y servicios", "Software/Programming":"TI: software y servicios",
    "Software & services":"TI: software y servicios", "Technology":"TI: hardware",
    "Technology Hardware":"TI: hardware",
    "Healthcare & Social Services":"Salud", "Medical Devices & Products":"Salud", "Pharmacies":"Salud",
    "Pharmaceuticals":"Farma y biotec",
    "Banks":"Banca y finanzas", "Banking and Finance":"Banca y finanzas", "Credit Card Companies":"Banca y finanzas",
    "Oil & Gas Producers":"Petróleo y gas", "Iron & Steel":"Materiales y química",
}
d24["Sector_h"] = d24["Industry"].map(MAPA).fillna("Otros")

# ---------------------------------------------------------------- ratios por empleado (2024, $ por empleado)
e = d24.dropna(subset=["Employees"]).query("Employees>0").copy()
e["sales_emp"]  = e["Sales"]  * 1e9 / e["Employees"]
e["profit_emp"] = e["Profits"]* 1e9 / e["Employees"]
e["margen"]     = e["Profits"] / e["Sales"]

def agg(df):
    return pd.Series(dict(n=len(df),
        sales_emp_med=df["sales_emp"].median(), profit_emp_med=df["profit_emp"].median(),
        margen_med=df["margen"].median(), empleados_med=df["Employees"].median()))

por_sector = e.groupby("Sector_h").apply(agg).sort_values("sales_emp_med", ascending=False)
por_sector_pais = (e[e["Country"].isin(PAISES)].groupby(["Sector_h","Country"]).apply(agg)
                   .query("n>=3"))

# ---------------------------------------------------------------- concentración: HHI y N efectivo por sector (2024)
def hhi(df):
    s = df["Sales"].dropna(); sh = s / s.sum()
    H = (sh**2).sum()
    return pd.Series(dict(n_firmas=len(s), HHI=H, N_efectivo=1/H if H>0 else np.nan,
                          factor_competitivo=1-H))  # (1-1/N_ef) = 1-HHI
conc = d24.groupby("Sector_h").apply(hhi).sort_values("N_efectivo")

# ---------------------------------------------------------------- panel 2014-2024 (match por nombre)
def norm(s): return re.sub(r"[^a-z0-9]","",str(s).lower())
d14["k"], d24["k"] = d14["Company"].map(norm), d24["Company"].map(norm)
m = d14.merge(d24, on="k", suffixes=("_14","_24"))
m = m[(m["Sales_14"]>0)&(m["Sales_24"]>0)]
m["g_sales"]  = (m["Sales_24"]/m["Sales_14"])**(1/10)-1
m["g_assets"] = (m["Assets_24"]/m["Assets_14"])**(1/10)-1
m["delta_intensidad_capital"] = m["g_assets"] - m["g_sales"]
panel = (m.groupby("Sector_h").agg(n=("k","size"), g_sales_med=("g_sales","median"),
         g_assets_med=("g_assets","median"), delta_K_med=("delta_intensidad_capital","median"))
         .query("n>=8").sort_values("delta_K_med", ascending=False))

# ---------------------------------------------------------------- salida
with pd.ExcelWriter("/home/claude/sim/calibracion_forbes.xlsx") as w:
    pd.DataFrame({"Fuente":["Forbes Global 2000: 2014 (xls original), 2019, 2024 (panel xlsx)"],
                  "Nota":["Ratios en $ corrientes; Sales/Profits/Assets en $B; empleados solo en 2024 (1.943 firmas válidas)"]}
                 ).to_excel(w, sheet_name="LEEME", index=False)
    por_sector.to_excel(w, sheet_name="ratios_sector_2024")
    por_sector_pais.to_excel(w, sheet_name="ratios_sector_pais")
    conc.to_excel(w, sheet_name="concentracion_HHI_N")
    panel.to_excel(w, sheet_name="panel_2014_2024")
    e[["Company","Country","Sector_h","Industry","Sales","Profits","Employees","sales_emp","profit_emp","margen"]]\
        .to_excel(w, sheet_name="microdatos_2024", index=False)

print("=== RATIOS POR EMPLEADO 2024 (mediana, $/empleado) ===")
print(por_sector.round(2).to_string())
print("\n=== CONCENTRACIÓN (HHI sobre ventas, universo G2000) ===")
print(conc.round(3).to_string())
print("\n=== PANEL 2014→2024 (crecimiento anual mediano) ===")
print(panel.round(3).to_string())
print("\nMatch panel:", len(m), "empresas casadas 2014-2024")
