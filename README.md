## Indiana Public Employee Salaries

URL = https://gateway.ifionline.org/report_builder/
Data on state and county public employee salaries from 2012--2017 from 
https://gateway.ifionline.org/report_builder/

The python script [indiana_salaries.py](indiana_salaries.py) iterates through dropdowns and creates 2 CSVs: [state.csv](state.csv), and [counties.csv](counties.csv). Each of the CSVs has the following columns: `employee, department, job_title_duties, city, compensation, year, county, reporting_unit`

### Notes: 

1. The state data includes data on universities. 
2. There is no state data for 2017.
3. From the website:

    "Gateway provides a direct one-of-a-kind link between local officials and their constituents. Since local officials submit information directly through Gateway, and Gateway makes the same information available publicly to citizens, there is no “middle man” causing delays or altering the data in any way. The information is available almost immediately, and the public can be confident that the data viewed on the website is exactly what the local official reported.

    State agencies, such as the Department of Local Government Finance (DLGF) and the State Board of Accounts (SBOA), will later review, audit and certify the data submitted by local officials. In the event there are changes during this process in accordance with statutory requirements, those figures will be presented separately on the Gateway website as “certified” or “audited” figures. However, since the information presented as “published” and “adopted” are the unaudited submissions from local officials,...(line truncated)...

    The Indiana Business Research Center and the state agencies make no warranty as to the completeness or accuracy of the data submitted by local officials and displayed as “published” or “adopted” amounts.

    If you are a local official and would like to make corrections to the information that was submitted, please contact gateway@dlgf.in.gov.

    Reporting Compliance and Values Listed as “NA”
    Indiana law places responsibility on local officials to submit financial information to the State. Budget forms are to be submitted by November 3 of each year. Debt information and annual financial reports must be supplied by March 1 of each year. However, not all units of government comply with these reporting requirements. Whenever the term “NA” is presented in a report, this indicates that the unit of government did not supply the information. This could mean that the particular item did not apply to...(line truncated)...

    In the event that a unit of government does not report the required information, a series of consequences occur:

    For a unit that does not submit budget paperwork, the Department of Local Government Finance will not grant any increases in the budget or property taxes from the previous year. The unit of government will be “defaulted” to the previous year’s amounts.
    Beginning in 2012, the Department of Local Government Finance will not grant authority to spend or impose property tax for a debt that is not reported.
    Beginning in 2012, units of government that have not submitted an annual financial report for the previous year will not be permitted to spend money for any purpose until the report is filed.
    Units of government that spend money without authority to do so are presented with audit findings from the State. In severe instances, local officials may be criminally charged."
