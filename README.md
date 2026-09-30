\# DHL Group — Financial \& Operational Performance Analyzer



\## 📊 Project Overview



This project analyzes the financial and operational performance of \*\*DHL Group\*\* using publicly available company-reporting data.



The objective is to understand how DHL converts \*\*revenue, workforce resources and capital investment into operating profit and cash generation\*\*.



The analysis combines:



\* \*\*Python / Pandas\*\* for data preparation and financial analysis

\* \*\*Power BI / DAX\*\* for interactive business intelligence and dashboarding

\* \*\*Public DHL Group Annual Report data\*\* for the underlying financial and segment information



The project is designed as a practical \*\*Finance + Business Analytics + Operations Analytics\*\* portfolio project.



\---



\## 🎯 Business Question



> \*\*How efficiently is DHL Group converting its operating resources and investments into profitable growth and cash generation?\*\*



The analysis investigates:



1\. How is DHL's financial performance changing over time?

2\. Which operating divisions are driving Group performance?

3\. How are workforce resources being used?

4\. How significant is capital investment across divisions?

5\. How does operating profit relate to operating cash generation?



\---



\## 🏢 Company Scope



DHL Group's 2025 reporting identifies five operating divisions:



\* Express

\* Global Forwarding, Freight

\* Supply Chain

\* eCommerce

\* Post \& Parcel Germany



Group Functions are reported separately and are excluded from operating-division comparisons where appropriate.



\---



\## 📈 Financial Analysis



The Group-level analysis covers \*\*2021–2025\*\* and includes:



\* Revenue

\* Revenue Growth

\* EBIT

\* EBIT Margin

\* Net Profit

\* Operating Cash Flow

\* Free Cash Flow

\* Capex

\* Equity Ratio

\* Net Debt



DHL reported 2025 revenue of \*\*€82.855bn\*\*, EBIT of \*\*€6.103bn\*\*, operating cash flow of \*\*€9.119bn\*\*, free cash flow of \*\*€2.295bn\*\*, and capex of \*\*€2.950bn\*\*.



\---



\## 🧩 Segment Analysis



Detailed operating-division analysis uses reported \*\*2024 and 2025\*\* segment data.



The analysis includes:



\* External Revenue

\* Total Segment Revenue

\* Material Expense

\* Staff Costs

\* EBIT

\* EBIT Margin

\* Operating Cash Flow

\* Average FTEs

\* Segment Assets

\* Capex

\* Depreciation \& Amortization



DHL reports these segment measures in its 2025 Annual Report.



\---



\## 👥 Workforce \& Productivity Analysis



The project calculates financial productivity indicators including:



\### Revenue per FTE



`External Revenue / Average FTE`



\### EBIT per FTE



`EBIT / Average FTE`



\### Staff Cost %



`Staff Costs / Total Segment Revenue`



The employee figures in the segment analysis are based on DHL's reported \*\*average FTEs\*\*.



These are financial productivity indicators and should not be interpreted as direct measures of individual employee productivity.



\---



\## 💰 Cash Generation Analysis



The project evaluates:



\* Operating Cash Flow

\* Operating Cash Flow Margin

\* Cash Conversion

\* Free Cash Flow

\* Free Cash Flow Margin



Cash Conversion is an \*\*analyst-derived ratio\*\*:



`Operating Cash Flow / EBIT`



It is used as an analytical indicator and is not presented as an official DHL KPI.



\---



\## 🏗️ Investment \& Capital Efficiency



Investment analysis includes:



\* Acquired-asset Capex

\* Right-of-use asset Capex

\* Total Capex

\* Capex Intensity

\* Segment Asset Intensity

\* Capex / D\&A



DHL's segment reporting separately discloses capex for acquired assets and right-of-use assets.



The project deliberately does \*\*not\*\* treat `EBIT / Capex` as a formal ROI measure because annual capex is a flow while the asset base reflects investments accumulated over time.



\---



\## 🔎 Selected Analytical Findings



The analysis identified several notable 2024–2025 patterns:



\### Group Performance



DHL's reported revenue decreased from \*\*€84.186bn to €82.855bn\*\*, while EBIT increased from \*\*€5.886bn to €6.103bn\*\*. EBIT margin increased from \*\*7.0% to 7.4%\*\*.



\### Express



External revenue decreased while EBIT increased, resulting in an improvement in EBIT margin.



\### Global Forwarding, Freight



External revenue and EBIT both decreased, with the EBIT decline materially larger than the revenue decline.



\### Supply Chain



External revenue increased slightly and EBIT increased, accompanied by an improvement in EBIT margin.



\### eCommerce



External revenue decreased while EBIT increased. The 2025 result requires additional context because DHL reports a positive non-recurring effect within eCommerce EBIT.



\### Post \& Parcel Germany



External revenue and EBIT both increased while average FTEs decreased.



These observations describe reported data and analyst calculations; they do not by themselves establish causation.



\---



\## 📊 Power BI Dashboard



The Power BI report contains three pages:



\### 1. Executive Overview



Provides the Group-level financial snapshot and five-year trends.



Key measures include:



\* Revenue

\* EBIT

\* EBIT Margin

\* Operating Cash Flow

\* Free Cash Flow

\* Capex



\### 2. Segment Performance



Compares DHL's five operating divisions using:



\* Revenue

\* Revenue Growth

\* EBIT

\* EBIT Growth

\* EBIT Margin

\* Cost structure

\* Segment performance matrix



\### 3. Operations \& Investment



Analyzes:



\* Average FTE

\* Revenue per FTE

\* EBIT per FTE

\* Staff Cost %

\* Capex Intensity

\* Asset Intensity

\* Investment relationships



\---



\## 🛠️ Tools \& Technologies



| Tool       | Purpose                       |

| ---------- | ----------------------------- |

| Python     | Data preparation and analysis |

| Pandas     | Data manipulation             |

| NumPy      | Numerical calculations        |

| Matplotlib | Analytical visualizations     |

| Power BI   | Interactive dashboard         |

| DAX        | Dynamic Power BI measures     |

| Git        | Version control               |

| GitHub     | Portfolio hosting             |



\---



\## 🗂️ Project Structure



```text

dhl-financial-operational-performance-analyzer/

│

├── dashboard/

│   ├── DHL\_Dashboard.pdf

│   └── DHL\_Financial\_Operational\_Analyzer.pbix

│

├── data/

│   ├── raw/

│   │   ├── dhl\_group\_financials.csv

│   │   ├── dhl\_segment\_financials.csv

│   │   └── source\_register.csv

│   │

│   ├── processed/

│   └── simulated/

│

├── images/

│   ├── 01\_group\_financial\_performance.png

│   ├── 02\_segment\_revenue\_vs\_ebit\_growth.png

│   ├── 03\_segment\_cost\_structure\_change.png

│   ├── 04\_workforce\_vs\_ebit\_productivity.png

│   ├── 05\_segment\_cash\_generation.png

│   └── 06\_investment\_vs\_ebit.png

│

├── src/

│   ├── calculate\_group\_kpis.py

│   ├── calculate\_segment\_kpis.py

│   ├── analyze\_segment\_changes.py

│   ├── analyze\_cost\_structure.py

│   ├── analyze\_workforce\_productivity.py

│   ├── analyze\_group\_cash\_generation.py

│   ├── analyze\_segment\_cash.py

│   ├── analyze\_investment\_efficiency.py

│   ├── build\_master\_segment\_dataset.py

│   └── validate\_master\_dataset.py

│

└── README.md

```



\---



\## 🔄 Analytical Workflow



```text

DHL Public Reporting

&#x20;       ↓

Raw CSV Data

&#x20;       ↓

Data Validation

&#x20;       ↓

Python / Pandas

&#x20;       ↓

KPI Calculations

&#x20;       ↓

Processed Analytical Data

&#x20;       ↓

Power BI / DAX

&#x20;       ↓

Interactive Dashboard

```



\---



\## ✅ Data Quality



A validation script checks:



\* Duplicate Year + Segment combinations

\* Required columns

\* Missing critical values

\* Revenue consistency

\* Positive FTE values

\* Negative capex/assets

\* Expected operating divisions

\* Expected reporting years

\* Source coverage



The current master segment dataset passed all validation checks.



\---



\## 📚 Data Sources



Primary data source:



\*\*DHL Group — 2025 Annual Report\*\*



https://reporting-hub.group.dhl.com/2025-fy/en/



Key sections used:



\* Key Financial Figures

\* Segment Reporting

\* Revenue by Business Unit

\* Financial Position

\* Combined Management Report



DHL Group's official 2025 reporting is the primary source for the financial and segment data used in this project.



\---



\## ⚠️ Methodology \& Limitations



This project is an \*\*independent portfolio analysis based on publicly available DHL Group reporting\*\*.



Reported DHL financial and segment information is kept separate from analyst-derived calculations.



The project does not use DHL internal systems, confidential information or proprietary operational data.



Where granular operational data is introduced for educational analytical exercises, it will be explicitly labelled as \*\*simulated\*\* and should not be interpreted as actual DHL internal data.



Financial productivity ratios such as Revenue per FTE and EBIT per FTE are analytical indicators rather than direct measures of employee-level productivity.



Similarly, Capex Intensity and Capex / D\&A are analytical measures and should not be interpreted as formal investment-return calculations.



\---



\## 🚀 How to Run the Python Analysis



Create and activate the virtual environment:



```bash

python -m venv .venv

```



Activate it on Windows PowerShell:



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



Install the required packages:



```bash

pip install -r requirements.txt

```



Run the main analysis scripts from the project root:



```bash

python src/calculate\_group\_kpis.py

python src/calculate\_segment\_kpis.py

python src/analyze\_segment\_changes.py

python src/analyze\_segment\_costs.py

python src/analyze\_workforce\_productivity.py

python src/analyze\_group\_cash\_generation.py

python src/analyze\_segment\_cash.py

python src/analyze\_investment\_efficiency.py

python src/build\_master\_segment\_dataset.py

python src/validate\_master\_dataset.py

```



\---



\## 👤 Author



\*\*Prajwal B. Venkatesh\*\*



Master's Student | Finance \& Business Analytics



GitHub:

https://github.com/Prajwal-BengaloreVenkatesh



